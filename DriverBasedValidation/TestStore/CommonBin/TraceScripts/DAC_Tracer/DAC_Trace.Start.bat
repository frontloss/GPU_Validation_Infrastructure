@echo off

set GFXTrace="%~dp0DACTrace.etl"
SET GUID="%~dp0Conf/guid.dat"

goto comment
set "timestamp=%DATE:/=-%@%TIME::=-%"
set "timestamp=%timestamp: =%"
set GFXTrace=%~dp0GFXTrace_%timestamp%.etl  
:comment 

echo.
echo Start Tracing ...
logman create trace "GfxDriverLogs" -pf %GUID% -o %GFXTrace% -ets > NUL





