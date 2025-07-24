@set XPERF_BIN=xperf\x86\xperf.exe
@if '%PROCESSOR_ARCHITECTURE%' EQU 'AMD64' set XPERF_BIN=xperf\amd64\xperf.exe
%XPERF_BIN% -stop Intel-Gfx-BootTrace
@regedit /s Reg\StopGfxBootTrace.reg
@copy C:\Windows\System32\LogFiles\WMI\GfxBootTrace.etl GfxBootTrace.etl
