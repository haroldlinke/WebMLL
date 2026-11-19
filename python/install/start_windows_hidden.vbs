' Datei-Version: 1.00 (2026-11-18) - start_windows_hidden.vbs
Option Explicit
Dim shell, files, folder, script, app
Set shell = CreateObject("WScript.Shell")
Set files = CreateObject("Scripting.FileSystemObject")
folder = files.GetParentFolderName(WScript.ScriptFullName)
app = files.GetParentFolderName(folder)
If Not files.FileExists(app & "\venv_web\Scripts\python.exe") Then
    MsgBox "Bitte zuerst install_windows.bat ausfuehren.", vbExclamation, "webMobaLedLib"
    WScript.Quit 1
End If
script = folder & "\start_windows.bat"
shell.Environment("Process")("MLL_HIDDEN_START") = "1"
shell.Run Chr(34) & script & Chr(34), 0, False
