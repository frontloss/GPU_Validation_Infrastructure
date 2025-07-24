;
; AutoIt Version: 3.0
;
; Script Function:
;   Get out of Metro UI and back into desktop.
;

; Block user input while this script runs
BlockInput(1)

Local $notepad_Title = "Untitled - Notepad"

;Open notepad
Run("Notepad")
Sleep(1000)

;activate the window
WinActivate($notepad_Title)

If WinExists($notepad_Title) Then
    ;Close notepad
    WinClose($notepad_Title)
EndIf

; Restore user unput
BlockInput(0)


; Finished!
