@echo off
setlocal enabledelayedexpansion

echo "Doxygen_Checker.bat has been called:"

rem curr_path will have path of current working directory ValDisplay/DisplayAutomation2.0/Src
SET curr_path=%CD%

rem get the full parent path(DisplayAutomation2.0 path) of current Src path
for %%a in ("%curr_path%") do set "disp_automation=%%~dpa"

rem get the full parent path(ValDisplay path) of current DisplayAutomation2.0 path
for %%a in (%disp_automation:~0,-1%) do set "val_display=%%~dpa"

set errorcnt=0
SET TEMPLATE_CHECKER_OUTPUT_FILE="%disp_automation%Logs\doxygen_template_checker_output.txt"
SET PARSER_OUTPUT_FILE="%disp_automation%Logs\doxygen_parser_output.txt"

IF EXIST %TEMPLATE_CHECKER_OUTPUT_FILE% DEL /F %TEMPLATE_CHECKER_OUTPUT_FILE%
IF EXIST %PARSER_OUTPUT_FILE% DEL /F %PARSER_OUTPUT_FILE%

FOR  %%A IN (Libs Tests) DO (
python %val_display%PreBuildChecks\doxygenTemplateChecker.py -i %disp_automation%%%A
if !ERRORLEVEL! GEQ 1 set /a errorcnt=errorcnt+1
python %val_display%PreBuildChecks\doxygenLogParser.py -i %disp_automation%%%A
if !ERRORLEVEL! GEQ 1 set /a errorcnt=errorcnt+1

)

if %errorcnt% NEQ 0 (
echo Check the below files for warnings
echo %TEMPLATE_CHECKER_OUTPUT_FILE%
echo %PARSER_OUTPUT_FILE%
rem exit /b 1 can be used after successful checkin of well documented code
exit /b 0
)
pause