@regedit /s ./Reg/EventUnRegistration.reg
@if exist "%ProgramFiles%\Intel\Graphics" rmdir /S /Q "%ProgramFiles%\Intel\Graphics"
