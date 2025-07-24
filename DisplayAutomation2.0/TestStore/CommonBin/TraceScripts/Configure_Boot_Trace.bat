set args_count=0
set reg=GfxBootTrace.reg
for %%x in (%*) do Set /A args_count+=1
if %args_count%==0 goto SKIP
if %args_count%==1 if %1==PC set reg=GfxPcBootTrace.reg
:SKIP
echo %reg%
@set XPERF_BIN=xperf\x86\xperf.exe
@if '%PROCESSOR_ARCHITECTURE%' EQU 'AMD64' set XPERF_BIN=xperf\amd64\xperf.exe
@regedit /s Reg\%reg%
@del /F /Q c:\Windows\System32\LogFiles\WMI\GfxBootTrace.etl
