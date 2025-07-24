@echo off

set GFXTrace="%~dp0DACTrace.etl"
SET GUID="%~dp0Conf/guid.dat"

goto comment
set "timestamp=%DATE:/=-%@%TIME::=-%"
set "timestamp=%timestamp: =%"
set GFXTrace=%~dp0GFXTrace_%timestamp%.etl  
:comment 

echo.
logman stop "GfxDriverLogs" -ets > NUL

echo.
echo Stop Tracing. ETL file: %GFXTrace%
echo.






