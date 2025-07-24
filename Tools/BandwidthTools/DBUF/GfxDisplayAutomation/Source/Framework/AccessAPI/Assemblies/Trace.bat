@set XPERF_BIN=x86\xperf.exe
@if '%PROCESSOR_ARCHITECTURE%' EQU 'AMD64' set XPERF_BIN=x64\xperf.exe

@%XPERF_BIN% -start GfxTrace -on Intel-Gfx-Driver
@REM %XPERF_BIN% -start GfxTrace -on Microsoft-Windows-DxgKrnl
@pause
@%XPERF_BIN% -stop GfxTrace -d GfxTrace.etl
