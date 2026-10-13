from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLA_Application as X02
import ExcelAPI.XLC_Excel_Consts as X01
import pattgen.M01_Public_Constants_a_Var as M01
import pattgen.M09_Language as M09
import pattgen.M08_Load_Sheet_Data
import pattgen.M07_Save_Sheet_Data
import pattgen.M30_Tools as M30
import pattgen.M65_Special_Modules
import pattgen.M80_Multiplexer_INI_Handling
import mlpyproggen.Pattern_Generator as PG
# at85neu.py
import pattgen.at85neu



import ExcelAPI.XLF_FormGenerator as XLF
import pattgen.D00_Forms as D00


global_AttinyAdress = None

# --- 1. DEFINITIONEN (MÜSSEN VOR DER MASKE STEHEN) ---

def CloseButton_Click():
    D00.MainMenu_Form.Hide()

def Close2Button_Click():
    CloseButton_Click()

def Close3Button_Click():
    CloseButton_Click()

def HelpButton_Click():
    X02.Shell('Explorer https://wiki.mobaledlib.de/anleitungen/spezial/patterngenerator')

def LinkGitHub_Click():
    X02.ActiveWorkbook.FollowHyperlink('https://github.com/Hardi-St/MobaLedLib')

def LinkStummi_Click():
    X02.ActiveWorkbook.FollowHyperlink('https://www.stummiforum.de/viewtopic.php?t=165060')

def LoadAllExamlesButton_Click():
    pattgen.M08_Load_Sheet_Data.Load_AllExamples_Sheets()

def LoadAllExamplesButton_Click(): # Falls mit 'p' geschrieben
    LoadAllExamlesButton_Click()

def LoadExampleButton_Click():
    Res = Variant()
    if M01.ExampleName == '':
        M01.ExampleName = pattgen.M07_Save_Sheet_Data.Get_MyExampleDir() + '/TestExample.MLL_pcf'
    Res = X02.Application.GetOpenFilename(fileFilter='Pattern configurator example (*.MLL_pcf), *.MLL_pcf')
    if Res != "":
        pattgen.M08_Load_Sheet_Data.Load_Sheets(Res, '')

def DeleteActualPageButton_Click():
    pass # Hier deine Lösch-Logik falls nötig

def DeleteAlleExamplesButton_Click():
    pattgen.M08_Load_Sheet_Data.Del_All_Sheets_Excep_Main()

def SaveActualExampleButton_Click():
    pass 

def SaveAllExamplesButton_Click():
    pass

def Multiplexer_Editor_Click():
    pattgen.M80_Multiplexer_INI_Handling.Load_Multiplexer()

# --- DEAKTIVIERTE SPEZIAL-MODULE (pass = macht nichts) ---
# def Prog_ISP_Button_Click(): pass

def Prog_ISP_Button_Click():
    import subprocess
    import sys
    import os

    # Pfad zur flashuno.py ermitteln (liegt im selben Ordner)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, "flashuno.py")
    
    # Hauptmaske verstecken
    D00.MainMenu_Form.Hide()
    
    try:
        # Startet flashuno.py als komplett neuen, frischen Prozess
        # .run() pausiert das Hauptprogramm, bis flashuno beendet wird
        subprocess.run([sys.executable, script_path])
    except Exception as e:
        print(f"Fehler beim Starten von flashuno.py: {e}")
    finally:
        # Erscheint wieder, wenn flashuno geschlossen wurde
        D00.MainMenu_Form.Show()

# -------------------------------------------------------------------
def Prog_Charlieplex_Button_Click(): pass


def Prog_Servo_Button_Click():
    import subprocess
    import os
    import sys
    
    # Pfad zur at85neu.py ermitteln (die liegt im selben Ordner)
    script_dir = os.path.dirname(__file__)
    script_path = os.path.join(script_dir, "at85neu.py")
    
    # Wir starten das Programm als separaten Linux-Prozess
    try:
        # 'sys.executable' stellt sicher, dass das gleiche Python genutzt wird
        subprocess.Popen([sys.executable, script_path])
    except Exception as e:
        print(f"Fehler beim Starten des externen Tools: {e}")
        
        # <--- Hier kommt dein at85neu rein
    
    
def Prog_Servo_2_Button_Click(): pass
def Prog_ServoMP3_Button_Click(): pass
def Prog_Servo_2_LED_Button_Click(): pass
def Prog_Attiny_Bootloader_Button_Click(): pass
def Prog_Attiny_Bootloader_no_status_led_Button_Click(): pass

def UserForm_Initialize():
    M09.Change_Language_in_Dialog(D00.MainMenu_Form)

#################################################################################################
    
Main_Menu_Form_RSC = {"UserForm":{
                        "Name"          : "MainMenuForm",
                        "BackColor"     : "#000008",
                        "BorderColor"   : "#000012",
                        "Caption"       : "Pattern Configurator",
                        "Height"        : 413.25,
                        "Left"          : 0,
                        "Top"           : 0,
                        "Type"          : "MainWindow",
                        "Visible"       : True,
                        "Width"         : 500,
                        "Components"    : [{"Name":"Multipage1","Height": 372,"Left": 6,"Top": 6,"Type": "MultiPage","Visible": True,"Width": 472,                            
                            "Components": [{"Name":"page1","Caption":"Beispiele","Type": "Page","Visible": True,
                                "Components":[{"Name":"Label3","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Achtung: Bei den Schaltern wurde bewusst auf die 'Sind sie sicher...' Abfragen verzichtet. Wenn ein Knopf gedrückt wird, dann löst er die entsprechende Aktion sofort aus.",
                                                "ControlTipText":"Tooltip1","ForeColor":"#000012","Height":30,"Left":6,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":300},
                                              {"Name":"Label2","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"by Hardi",
                                               "ControlTipText":"Tooltip2","ForeColor":"#FF0000","Height":12,"Left":318,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":36},
                                              {"Name":"CloseButton","Accelerator":"d","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Dialog schließen",
                                               "Command":CloseButton_Click,"ControlTipText":"","ForeColor":"#000012","Height":25,"Left":282,"Top":312,"Type":"CommandButton","Visible":True,"Width":72},
                                              {"Name":"HelpButton","Accelerator":"h","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Hilfe",
                                               "Command":HelpButton_Click,"ControlTipText":"","ForeColor":"#000012","Height":25,"Left":204,"Top":312,"Type":"CommandButton","Visible":True,"Width":72},
                                              {"Name":"Frame1","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Laden",
                                               "ControlTipText":"","ForeColor":"#000012","Height":84,"Left":6,"SpecialEffect":"fmSpecialEffectEtched","Top":42,"Type":"Frame","Visible":True,"Width":448,
                                               "Components":[{"Name":"Label1","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Lädt ausgewählte Standard Beispiele aus Verzeichnis'Pattern_Config_Examples'.",
                                                              "ControlTipText":"","ForeColor":"#000012","Height":36,"Left":132,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":204},
                                                             {"Name":"Label5","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Öffnet einen Auswahldialog mit dem eine TextDatei mit einem oder mehreren Pattern geladen wird.",
                                                              "ControlTipText":"","ForeColor":"#000012","Height":30,"Left":132,"TextAlign":"fmTextAlignLeft","Top":42,"Type":"Label","Visible":True,"Width":210},
                                                             {"Name":"LoadAllExamplesButton","Accelerator":"A","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Lade Beispiele",
                                                              "Command":LoadAllExamlesButton_Click,"ControlTipText":"","ForeColor":"#000012","Height":25,"Left":6,"Top":6,"Type":"CommandButton","Visible":True,"Width":114},
                                                             {"Name":"LoadExampleButton","Accelerator":"B","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Eigene Daten laden",
                                                              "Command":LoadExampleButton_Click,"ControlTipText":"","ForeColor":"#000012","Height":25,"Left":6,"Top":42,"Type":"CommandButton","Visible":True,"Width":114}]
                                               },
                                              {"Name":"Frame2","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Speichern",
                                               "ControlTipText":"","ForeColor":"#000012","Height":84,"Left":6,"SpecialEffect":"fmSpecialEffectEtched","Top":132,"Type":"Frame","Visible":True,"Width":448,
                                               "Components":[{"Name":"Label4","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Speichert alle Patternseiten in der Datei\n'MyExamples.MLL_pcf' im Verzeichnis\n'EigeneDokumente\\MyPattern_Config_Examples'.",
                                                              "ControlTipText":"","ForeColor":"#000012","Height":36,"Left":132,"TextAlign":"fmTextAlignLeft","Top":0,"Type":"Label","Visible":True,"Width":204},
                                                             {"Name":"Label6","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Speichert die aktuelle, oder alle ausgewählten Seiten in einer Datei.(Mit Strg+Klick auf den Seiten namen können mehrere Seiten ausgewählt werden.)",
                                                              "ControlTipText":"","ForeColor":"#000012","Height":36,"Left":132,"TextAlign":"fmTextAlignLeft","Top":36,"Type":"Label","Visible":True,"Width":210},
                                                             {"Name":"SaveAllExamplesButton","Accelerator":"s","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Alle Seiten speichern",
                                                              "Command":SaveAllExamplesButton_Click,"ControlTipText":"","ForeColor":"#000012","Height":25,"Left":6,"Top":6,"Type":"CommandButton","Visible":True,"Width":114},
                                                             {"Name":"SaveActualExampleButton","Accelerator":"p","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Aktuelle Seite(n) speichern",
                                                              "Command":SaveActualExampleButton_Click,"ControlTipText":"","ForeColor":"#000012","Height":25,"Left":6,"Top":42,"Type":"CommandButton","Visible":True,"Width":114}
                                                             ]},
                                              {"Name":"Frame3","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Löschen",
                                               "ControlTipText":"","ForeColor":"#000012","Height":84,"Left":6,"SpecialEffect":"fmSpecialEffectEtched","Top":222,"Type":"Frame","Visible":True,"Width":448,
                                               "Components":[{"Name":"Label7","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Löscht ALLE Datenseiten.",
                                                              "ControlTipText":"","ForeColor":"#000012","Height":36,"Left":132,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":204},
                                                             {"Name":"Label8","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Löscht die aktuelle, oder alle ausgewählten Seiten.\n(Mehrere Seiten können mit Strg+Klick auf den Seitennamen ausgewählt werden.)",
                                                              "ControlTipText":"","ForeColor":"#000012","Height":36,"Left":132,"TextAlign":"fmTextAlignLeft","Top":36,"Type":"Label","Visible":True,"Width":210},
                                                             {"Name":"DeleteAlleExamplesButton","Accelerator":"l","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Alle Datenseiten löschen",
                                                              "Command":DeleteAlleExamplesButton_Click,"ControlTipText":"","ForeColor":"#000012","Height":25,"Left":6,"Top":6,"Type":"CommandButton","Visible":True,"Width":114},
                                                             {"Name":"SaveActualExampleButton","Accelerator":"ö","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Aktuelle Seite(n) löschen",
                                                              "Command":DeleteActualPageButton_Click,"ControlTipText":"","ForeColor":"#000012","Height":25,"Left":6,"Top":42,"Type":"CommandButton","Visible":True,"Width":114}
                                                             ]}
                                              ]},
                                           {"Name": "page2",
                                            "Caption": "Spezielle Module",
                                            "Type": "Page","Visible": True,
                                            "Components"    : [{"Name":"Label9","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                                "Caption"       : "Diese Seite enthält Funktionen mit denen spezielle, auf dem ATTiny basierte Module programmiert und getestet werden können.",
                                                                "ControlTipText": "","ForeColor": "#000012","Height": 30,"Left": 6,"TextAlign": "fmTextAlignLeft","Top": 6,"Type": "Label","Visible": True,"Width": 400},
                                                               {"Name": "Label10","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                                                "Caption": "by Hardi",
                                                                "ControlTipText": "","ForeColor": "#FF0000","Height": 12,"Left": 318,"TextAlign": "fmTextAlignLeft","Top": 6,"Type": "Label","Visible": True,"Width": 36},
                                                               {"Name": "Close2Button","BackColor": "#00000F","BorderColor": "#000006","BorderStyle"   : "fmBorderStyleNone",
                                                                "Caption": "Dialog schließen",
                                                                "Command": Close2Button_Click,"ControlTipText": "","ForeColor": "#000012","Height": 25,"Left": 282,"Top": 312,"Type": "CommandButton","Visible": True,"Width": 72},
                                                               {"Name": "Frame4","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                                                "Caption"       : "Programmieradapter",
                                                                "ControlTipText": "","ForeColor": "#000012","Height": 114,"Left": 6,"Top": 42,"Type": "Frame","Visible": True,"Width": 454,
                                                                "Components"    : [{"Name": "Label11","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                                                                    "Caption": "Ein ATTiny hat keinen USB Anschluss. Darum benötigt man zur Programmierung einen Programmieradapter. Das kann ein Arduino mit besonderem Programm sein. Mit dem <Prog. ISP> Button wird das Programm zum Arduino übertragen.",
                                                                                    "ControlTipText": "","ForeColor": "#000012","Height": 48,"Left": 84,"TextAlign": "fmTextAlignLeft","Top": 6,"Type": "Label","Visible": True,"Width": 344},
                                                                                   {"Name": "Label13","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                                                                    "Caption": "Dieses Programm kann auf dem Tiny_UniProg(Platine 400) und auf einem 'Nackten' Arduino in einem Steckbrett eingesetzt werden.\nDer 'HV Reset' ist allerdings nur mit der 'Tiny_UniProg' Platine möglich. Er wird für das Programmieren des Servo Programms benötigt.",
                                                                                    "ControlTipText": "","ForeColor": "#000012","Height": 60,"Left": 6,"TextAlign": "fmTextAlignLeft","Top": 54,"Type": "Label","Visible": True,"Width": 442},
                                                                                   {"Name": "Prog_ISP_Button","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                                                                    "Caption": "Prog. ISP",
                                                                                    "Command": Prog_ISP_Button_Click,"ControlTipText": "","ForeColor": "#000012","Height": 25,"Left": 6,"Top": 12,"Type": "CommandButton","Visible": True,"Width": 72
                                                                                    }]
                                                                },
                                                                
                                                               
                                                               
                                                               
                                                               
                                                                
                                                               {"Name": "MultiPage2","BackColor": "#00000F","ControlTipText": "","ForeColor": "#000012","Height": 150,"Left": 6,"Top": 162,"Type": "MultiPage","Visible": True,"Width": 454,
                                                                   "Components": [{"Name": "page5",
                                                                                   "Caption":"ATTiny85 (Servo / MP3)",
                                                                                  "Type": "Page","Visible": True,
                                                                                 "Components"    : [{"Name": "Label4","BackColor": "#00000F","BorderColor": "#000006","BorderStyle"   : "fmBorderStyleNone",
                                                                                                       "Caption": "Das Servo Modul (Platine 510) kann bis zu 3 Servos ansteuern.\n\nZur Programmierung des ATTiny85 wird ein Programmieradapter benötigt (siehe oben) in der der ATTiny eingesteckt wird.",
                                                                                                      "ControlTipText": "","ForeColor": "#000012", "Height": 96,"Left": 84,"TextAlign": "fmTextAlignLeft","Top": 12,"Type": "Label","Visible": True,"Width": 264},
                                                                                                      {"Name": "Prog_Servo_Button","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                                                                                       "Caption": "Prog. ATTiny 85",
                                                                                                       "Command": Prog_Servo_Button_Click,"ControlTipText": "","ForeColor" : "#000012","Height": 25,"Left": 6,"Top": 12,"Type": "CommandButton","Visible": True,"Width": 72}
                                                                                                      ]},
                                                                                                 
#

#                                                                                                  
#                                                                                      
   #                                                                            {"Name": "page5",
    #                                                                               "Caption":"ATTiny85 (Servo / MP3)",
     #                                                                             "Type": "Page","Visible": True,
       #                                                                          "Components"    : [{"Name": "Label4","BackColor": "#00000F","BorderColor": "#000006","BorderStyle"   : "fmBorderStyleNone",
   #                                                                                                    "Caption": "Das Servo Modul (Platine 510) kann bis zu 3 Servos ansteuern.\n\nZur Programmierung des ATTiny85 wird ein Programmieradapter benötigt (siehe oben) in der der ATTiny eingesteckt wird.",
 #                                                                                                     "ControlTipText": "","ForeColor": "#000012", "Height": 96,"Left": 84,"TextAlign": "fmTextAlignLeft","Top": 12,"Type": "Label","Visible": True,"Width": 264},
 #                                                                                                     {"Name": "Prog_Servo_Button","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
 ##                                                                                                     "Caption": "Prog. Servo",
 #                                                                                                      "Command": Prog_Servo_Button_Click,"ControlTipText": "","ForeColor" : "#000012","Height": 25,"Left": 6,"Top": 12,"Type": "CommandButton","Visible": True,"Width": 72}
#                                                                                                      ]},
                                                                                                      
#                                                                                                     
#                                                                                              
#                                                                                  {"Name": "page6",
#                                                                                   "Caption":"Servo-MP3",
#                                                                                   "Type": "Page","Visible": True,
#                                                                                   "Components"    : [{"Name": "Label34","BackColor": "#00000F","BorderColor": "#000006","BorderStyle"   : "fmBorderStyleNone",
#                                                                                                       "Caption": "Man das Servo-Modul auf zur Ansteuerung von Soundmodulen nutzen (JQ6500/MP3-TF-16p) nutzen.\n\nDabei werden die Soundmodule mit je einem 1k Widerstand an die Signal-Pins der Servoausgänge angeschlossen. Zusätzlich ist die Masse zu verbinden. Die Stromversorgung kann man getrennt lösen - meist funktioniert es aber auch die 5V von den Servoanschlüssen zu nutzen.\n\nZur Programmierung des ATTiny85 wird ein Programmieradapter benötigt (siehe oben) in der der ATTiny eingesteckt wird.",
#                                                                                                       "ControlTipText": "","ForeColor": "#000012", "Height": 120,"Left": 84,"TextAlign": "fmTextAlignLeft","Top": 6,"Type": "Label","Visible": True,"Width": 264},
#                                                                                                      {"Name": "Prog_ServoMP3_Button","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
#                                                                                                       "Caption": "Prog.Servo/MP3",
#                                                                                                       "Command": Prog_ServoMP3_Button_Click,"ControlTipText": "","ForeColor" : "#000012","Height": 25,"Left": 6,"Top": 12,"Type": "CommandButton","Visible": True,"Width": 72},
#                                                                                                      ]},
#                                                                                  {"Name": "page7",
#                                                                                   "Caption":"Servo DM(511)",
#                                                                                   "Type": "Page","Visible": True,
#                                                                                   "Components"    : [{"Name": "Label64","BackColor": "#00000F","BorderColor": "#000006","BorderStyle"   : "fmBorderStyleNone",
#                                                                                                       "Caption": "Direct Mode Servo Platine von Eckhart (Platine 511 oder modifzierte Servoplatine 510)\nDas Servo Modul kann bis zu 3 Servos ansteuern.\nZur Programmierung des ATTiny85 wird ein Programmieradapter benötigt (siehe oben) in der der ATTiny eingesteckt wird.\nAchtung: Bei der Version mit LED kann der Attiny NUR mit dem Programmieradapter Tiny-Uniprog (Platine 400) programmiert werden.",
#                                                                                                       "ControlTipText": "","ForeColor": "#000012", "Height": 108,"Left": 84,"TextAlign": "fmTextAlignLeft","Top": 12,"Type": "Label","Visible": True,"Width": 344},
#                                                                                                      {"Name": "Prog_Servo2_Button","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
#                                                                                                       "Caption": "Prog. DM-Servo ohne LED",
#                                                                                                       "Command": Prog_Servo_2_Button_Click,"ControlTipText": "","ForeColor" : "#000012","Height": 25,"Left": 6,"Top": 12,"Type": "CommandButton","Visible": True,"Width": 72}, 
#                                                                                                      {"Name": "Prog_Servo2_LED_Button","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
#                                                                                                       "Caption": "Prog. DM-Servo mit LED",
#                                                                                                       "Command": Prog_Servo_2_LED_Button_Click,"ControlTipText": "","ForeColor" : "#000012","Height": 25,"Left": 6,"Top": 50,"Type": "CommandButton","Visible": True,"Width": 72}
#                                                                                                      ]},
#                                                                                  {"Name": "page8",
#                                                                                   "Caption":"Attiny DirektProg ",
#                                                                                   "Type": "Page","Visible": True,
#                                                                                   "Components"    : [{"Name": "Label64","BackColor": "#00000F","BorderColor": "#000006","BorderStyle"   : "fmBorderStyleNone",
#                                                                                                       "Caption": "ACHTUNG - Noch nicht vollständig implementiert. Nur für interen Tests!!!\nDer Attiny DirektProg Modus ermöglicht es, die Firmware des Attinys auszutauschen, während der Attiny im normal im WS2812-Bus hängt.\nEs wird kein Programmieradapter mehr benötigt.\nZuerst muß ein Bootlaoder auf dem Attiny installiert werden. Button <Bootloader>. Der Attiny muß dazu in einem Programmieradapter stecken.\nDanach wird der Attiny in die Zielplatine gesteckt und mit dem WS2812-Bus verbunden. Die Programmierung erfolgt dann über die Servo2 Seite.\n",
#                                                                                                       "ControlTipText": "","ForeColor": "#000012", "Height": 108,"Left": 84,"TextAlign": "fmTextAlignLeft","Top": 12,"Type": "Label","Visible": True,"Width": 364},
#                                                                                                      {"Name": "Prog_Attiny_Bootloader_Button","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
#                                                                                                       "Caption": "Prog. Attiny Bootloader",
#                                                                                                       "Command": Prog_Attiny_Bootloader_Button_Click,"ControlTipText": "","ForeColor" : "#000012","Height": 25,"Left": 6,"Top": 12,"Type": "CommandButton","Visible": True,"Width": 72}, 
#                                                                                                      {"Name": "Prog_Attiny_Bootloader_no_status_led_Button","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
#                                                                                                       "Caption": "Bootloader ohne blaue LED",
#                                                                                                       "Command": Prog_Attiny_Bootloader_no_status_led_Button_Click,"ControlTipText": "","ForeColor" : "#000012","Height": 25,"Left": 6,"Top": 50,"Type": "CommandButton","Visible": True,"Width": 72}
#                                                                                                      ]},                                                                                     
                                                                                  ]}
                                                               ]},
                                           {"Name": "page3",
                                            "Caption": "Extras",
                                            "Type": "Page","Visible": True,
                                            "Components"    : [{"Name":"Label31","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                                "Caption"       : "Diese Seite enthält zusätzliche Programme, die die Arbeit mit der MobaLedLib unterstützen.",
                                                                "ControlTipText": "","ForeColor": "#000012","Height": 30,"Left": 6,"TextAlign": "fmTextAlignLeft","Top": 6,"Type": "Label","Visible": True,"Width": 246},
                                                               {"Name": "Frame9","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                                                "Caption"       : "Pattern Multiplexer",
                                                                "ControlTipText": "","ForeColor": "#000012","Height": 120,"Left": 6,"Top": 36,"Type": "Frame","Visible": True,"Width": 354,
                                                                "Components"    : [{"Name":"Label32","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                                                    "Caption" : "Mit dem Mustermultiplexer können Sie mehrere Muster kombinieren und in beliebiger Kombination verwenden. Mit dem Multiplexer-Editor können Multiplexer erstellt und die gewünschten Muster ausgewählt und eingefügt werden.",
                                                                                    "ControlTipText": "","ForeColor": "#000012","Height": 48,"Left": 102,"TextAlign": "fmTextAlignLeft","Top": 6,"Type": "Label","Visible": True,"Width": 246}, 
                                                                                   {"Name": "Label33","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                                                                    "Caption": "Die erstellten Multiplexer können einfach über einen MLL-Makro im Programmgenerator ausgewählt und eingestellt werden. Mit einer Option im Makro können die Multiplexer auch einfach mehrfach multipliziert werden. Infolgedessen sind weniger Einstellungen für ein sich wiederholendes Muster erforderlich.",
                                                                                    "ControlTipText": "","ForeColor": "#000012","Height": 60,"Left": 6,"Top": 54,"Type": "Label","Visible": True,"Width": 342},
                                                                                   {"Name": "Multiplexer_Editor","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                                                                    "Caption": "Multiplexer Editor",
                                                                                    "Command": Multiplexer_Editor_Click,"ControlTipText": "","ForeColor": "#000012","Height": 25,"Left": 6,"TextAlign": "fmTextAlignLeft","Top": 12,"Type": "CommandButton","Visible": True,"Width": 84
                                                                                    }]
                                                                },
                                                               ]
                                            }]
                            }]
                        }}
""

# --- 3. DIE KLASSE (RAHMEN) ---

class CMainMenu_Form:
    def __init__(self, controller):
        self.controller = controller
        self.IsActive = False
        self.Form = None
        self.Controls = []
        self.Controls_Dict = {}
    
    def __UserForm_Initialize(self):
        # Nutzt die oben definierte RSC Variable
        self.Form = XLF.generate_form(Main_Menu_Form_RSC, self.controller, dlg=self, jump_table=PG.ThisWorkbook.jumptable, defaultfont=X02.DefaultFont)
                
    def Hide(self):
        self.IsActive = False
        self.Form.destroy()
        
    def AddControl(self, control):
        self.Controls.append(control)
        self.Controls_Dict[control.Name] = control
        
    def Show(self, page1=None, page2=None, AttinyAdress=None):
        self.IsActive = True
        self.__UserForm_Initialize()
        # Falls du willst, dass er auf Seite 1 startet, lassen wir select() weg
        self.controller.wait_window(self.Form)
