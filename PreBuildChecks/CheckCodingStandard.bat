@echo off

:: usage
:: no arg - scans source folder
:: arg 1 (required) Full Binaries path - full path to the binaries root directory (FolderPath where ValDisplay folder exists)
:: arg 2 (optional) Full Source Path - Full scans given path (Path to file/folder to be formatted)

set errorCnt=0
set startTime=%TIME%

:: Default while running batch file is to EDIT the files using clang-format
set Edit=0

:: Binary directory has to be provided using /p option
set BINARY_DIR=

echo ----------------------------------------------------------------------------------
echo Starting Display Syntax checking at %startTime%

set SRC_PATH=%~dp0..\DisplayAutomation2.0
set CLANG_CHECKER=%~dp0ValDisplayCodingStandard.py
set SYNTAX_CHECKER=%~dp0SyntaxChecker.py

set OPTION=%1
shift

if "%OPTION%" == "/?" (
  goto usage
)

:loop
if "%OPTION%" == "/p" ( 
    set BINARY_DIR=%1
    shift
)

if "%OPTION%" == "Edit" (
  set Edit=1
)

if "%OPTION%" == "/s" ( 
  set SRC_PATH=%1
  shift
)

if "%1" == "" (
  goto continue 
) else (
  set OPTION=%1
  shift
  goto loop
)

:: Continue to run clang-format and syntax checker scripts
:continue

if "%BINARY_DIR%" == "" (
  goto usage
)

:: Clang-format checker: 
set CLANG_FORMAT=%BINARY_DIR%\build\python2-win32\python.exe %CLANG_CHECKER%

if %Edit% == 0 (
  %CLANG_FORMAT% -p %BINARY_DIR% -s %SRC_PATH%
) else (
  %CLANG_FORMAT% -p %BINARY_DIR% -s %SRC_PATH% --edit
)

set /a errorCnt=%errorCnt%+%ERRORLEVEL%

IF %errorCnt% GTR 0 (
    echo Run ValDisplay/PreBuildChecker/CheckCodingStandard.bat /p [Base Repo Path] /s [Source Path] [Edit] to correct clang-format errors
    echo.
)

:: Display syntax checker - Custom rules which is defined in SyntaxChecker.py
set CHECKER_SCRIPT=%BINARY_DIR%\build\python2-win32\python.exe %SYNTAX_CHECKER%

%CHECKER_SCRIPT% %SRC_PATH%
set /a errorCnt=%errorCnt%+%ERRORLEVEL%


if %errorCnt% GTR 0 (
    echo Completed Display Coding Standard Checker in time %startTime% to %TIME% with %errorCnt% error[s]
) else (
    echo Display Coding Standard Checker succeeded in time %startTime% to %TIME% .
)

echo ----------------------------------------------------------------------------------

exit /b %errorCnt%

:usage
echo  Usage: CheckCodingStandard.bat /p [Base Repo Path] [/s Source Path] [Edit]
echo
echo         Repo Path - Binary path where the artifactory tools exists (FolderPath where ValDisplay folder exists)
echo         Source Path - Optional. Default is ..\DisplayAutomation2.0\ Can provide directory or file name as path
echo         Edit - Corrects the clang-format errors and formats the file(s) in Source Path file
echo  Example: (Assuming cwd=ValDisplay\)
echo         PreBuildChecks\CheckCodingStandard.bat /p ..\ /s DisplayAutomation2.0\Src\Logger\log.c Edit
echo.
exit /B 1

PAUSE
