# Datei-Version: 1.00 (2026-11-27) - test_ansi_screen.py
# ----------------------------------------------------------------------------------------------
# Name:           test_ansi_screen.py
# Path:           test_ansi_screen.py
# Version:        1.00
# Last Update:    2026-11-27
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-27  Neu: Tests fuer _web/web_ansi.py (Terminal-Emulator des Log-Fensters)
# ----------------------------------------------------------------------------------------------
# Tests fuer _web/web_ansi.py (Terminal-Emulator des Log-Fensters). Aufruf: python test_ansi_screen.py
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _web.web_ansi import AnsiScreen  # noqa: E402


def screen_of(*chunks, **kwargs):
    s = AnsiScreen(**kwargs)
    for c in chunks:
        s.write(c)
    return s


def plain(screen):
    import re
    return [re.sub(r"<[^>]+>", "", h).replace("&nbsp;", "").replace("&lt;", "<").replace("&amp;", "&")
            for h in screen.html_rows()]


class AnsiScreenTests(unittest.TestCase):
    def test_plain_lines(self):
        s = screen_of("eins\nzwei\n")
        self.assertEqual(plain(s), ["eins", "zwei"])

    def test_no_trailing_empty_row(self):
        s = screen_of("eins\n\n\n")
        self.assertEqual(plain(s), ["eins"])

    def test_carriage_return_overwrites(self):
        s = screen_of("10%\r50%\r100%\n")
        self.assertEqual(plain(s), ["100%"])

    def test_progress_bar_chunks(self):
        s = AnsiScreen()
        s.write("[=   ] 1\r")
        self.assertEqual(plain(s), ["[=   ] 1"])
        s.write("[==  ] 2\r")
        self.assertEqual(plain(s), ["[==  ] 2"])
        s.write("fertig\x1b[K\n")  # wie ein Terminal: der Rest der alten Zeile muss weg
        self.assertEqual(plain(s), ["fertig"])

    def test_cursor_up_and_erase_line(self):
        s = screen_of("zeile1\nzeile2\n\x1b[1A\x1b[2Kgeaendert\n")
        self.assertEqual(plain(s), ["zeile1", "geaendert"])

    def test_erase_to_end_of_line(self):
        s = screen_of("abcdef\r\x1b[3C\x1b[K\n")
        self.assertEqual(plain(s), ["abc"])

    def test_red_text_is_span_with_color(self):
        s = screen_of("\x1b[31mFehler\x1b[0m ok\n")
        self.assertEqual(s.html_rows(), ['<span style="color:#c62828">Fehler</span> ok'])

    def test_bold_and_reset(self):
        s = screen_of("\x1b[1mfett\x1b[22m normal\x1b[m\n")
        self.assertEqual(s.html_rows(), ['<span style="font-weight:bold">fett</span> normal'])

    def test_html_is_escaped(self):
        s = screen_of("<b>&amp;</b>\n")
        self.assertEqual(s.html_rows(), ["&lt;b&gt;&amp;amp;&lt;/b&gt;"])

    def test_escape_sequence_split_between_blocks(self):
        s = AnsiScreen()
        s.write("\x1b[3")
        s.write("1mX\x1b[0m\n")
        self.assertEqual(s.html_rows(), ['<span style="color:#c62828">X</span>'])

    def test_background_and_bright_colors(self):
        s = screen_of("\x1b[44;93mB\n")
        self.assertEqual(s.html_rows(), ['<span style="color:#b58900;background-color:#1565c0">B</span>'])

    def test_256_and_rgb_colors(self):
        s = screen_of("\x1b[38;5;196mA\x1b[38;2;10;20;30mB\n")
        self.assertEqual(s.html_rows(), [
            '<span style="color:#ff0000">A</span><span style="color:#0a141e">B</span>'])

    def test_css_class_from_write(self):
        s = AnsiScreen()
        s.write("warnung\n", cls="text-red-8")
        self.assertEqual(s.html_rows(), ['<span class="text-red-8">warnung</span>'])

    def test_unknown_sequences_ignored(self):
        s = screen_of("\x1b[?25l\x1b]0;Titel\x07text\x1b(B\n")
        self.assertEqual(plain(s), ["text"])

    def test_tab_and_backspace(self):
        s = screen_of("a\tb\x08c\n")
        self.assertEqual(plain(s), ["a       c"])

    def test_hidden_line_is_removed(self):
        seen = []

        def on_end(text, is_error):
            seen.append((text, is_error))
            return text.startswith("noise")
        s = screen_of("eins\nnoise: x\nzwei\n", on_line_end=on_end)
        self.assertEqual(plain(s), ["eins", "zwei"])
        self.assertEqual(seen[0], ("eins", False))

    def test_nul_marks_line(self):
        seen = []
        s = AnsiScreen(on_line_end=lambda text, err: seen.append(text) or False)
        s.write("pa\x00ket\n")
        self.assertEqual(seen, ["paket\x00"])

    def test_error_flag_from_class(self):
        seen = []
        s = AnsiScreen(on_line_end=lambda text, err: seen.append(err) or False)
        s.write("Fehler\n", cls="text-red-8")
        self.assertEqual(seen, [True])

    def test_history_is_limited(self):
        s = AnsiScreen(max_rows=5)
        for i in range(12):
            s.write("zeile %d\n" % i)
        rows = plain(s)
        self.assertLessEqual(len(s.rows), 5)
        self.assertEqual(rows[-1], "zeile 11")
        self.assertNotIn("zeile 0", rows)
        self.assertGreater(s.removed, 0)

    def test_last_text(self):
        s = screen_of("abc\ndef\n\n")
        self.assertEqual(s.last_text(), "def")


if __name__ == "__main__":
    unittest.main()
