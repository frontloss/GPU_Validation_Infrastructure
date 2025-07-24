REM @ECHO OFF
SET myPath=%~dp0
SET traceMask=c:\*.valdi
SET ValDiTarget=c:\ValDi\
SET dumpFolder=c:\temp\

IF NOT EXIST %dumpFolder% (
mkdir %dumpFolder%
)

%ValDiTarget%ValDiTest.exe -finalize
IF %ERRORLEVEL% NEQ 0 (
    ECHO ValDi trace finalzie error
	TIMEOUT 5 > nul
	%ValDiTarget%ValDiTest.exe -finalize
)

TIMEOUT 1 > nul

move /Y %traceMask% %dumpFolder%

exit /b 0