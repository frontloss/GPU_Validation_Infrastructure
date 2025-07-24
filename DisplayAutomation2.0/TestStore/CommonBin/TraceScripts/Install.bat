@if exist "%ProgramFiles%\Intel\Graphics" rmdir /S /Q "%ProgramFiles%\Intel\Graphics"
@mkdir "%ProgramFiles%\Intel\Graphics"
@copy /Y GfxEvents.exe "%ProgramFiles%\Intel\Graphics"
@copy /Y GfxEventsDisp.exe "%ProgramFiles%\Intel\Graphics"
@regedit /s ./Reg/EventRegistration.reg
@echo Completed the Installation...

