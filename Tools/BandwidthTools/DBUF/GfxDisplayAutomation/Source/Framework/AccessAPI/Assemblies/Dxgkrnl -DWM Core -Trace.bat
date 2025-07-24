@set XPERF_BIN=x86\xperf.exe
@if '%PROCESSOR_ARCHITECTURE%' EQU 'AMD64' set XPERF_BIN=x64\xperf.exe

@%XPERF_BIN% -start GfxTrace -on Intel-Gfx-Driver+Microsoft-Windows-DxgKrnl:0x01+Microsoft-Windows-Dwm-Core
@REM +Microsoft-Windows-Dwm-Api+Microsoft-Windows-Dwm-Dwm+Microsoft-Windows-Dwm-Redir+Microsoft-Windows-Dwm-Udwm
@pause
@%XPERF_BIN% -stop GfxTrace -d GfxTrace.etl
