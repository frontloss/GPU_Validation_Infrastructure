REM @ECHO off
setlocal enabledelayedexpansion

SET myPath=%~dp0
SET ValDiTarget=C:\ValDi\
SET dumpFolder=C:\temp
SET drvPDBPath=C:\Windows\System32\drivers\igdkmd64.pdb

IF NOT EXIST %ValDiTarget% (
mkdir %ValDiTarget%
)

IF NOT EXIST %dumpFolder% (
mkdir %dumpFolder%
)

IF NOT %myPath% == %ValDiTarget% (
xcopy /s /Y %myPath%*.* %ValDiTarget%
)

%ValDiTarget%ValDiTest.exe -state
IF %ERRORLEVEL% LEQ 0 (
    ECHO Installing ValDi...	 
    start %ValDiTarget%iClick.exe /arm
    %ValDiTarget%PreValDi.exe -i
    IF !ERRORLEVEL! NEQ 0 (
        ECHO ValDi deployment error
        goto :eof
    )
    ECHO Done.
    start %ValDiTarget%iClick.exe /disarm
)

REM Disable Windows On-screen notifications
reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Notifications\Settings /t REG_DWORD /v NOC_GLOBAL_SETTING_TOASTS_ENABLED /d 0 /f
reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced /t REG_DWORD /v ShowInfoTip /d 0 /f
reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced /t REG_DWORD /v EnableBalloonTips /d 0 /f

reg add HKLM\SYSTEM\CurrentControlSet\Services\ValDi\Parameters /t REG_DWORD /v TraceMMIOAccess /d 0 /f
reg add HKLM\SYSTEM\CurrentControlSet\Services\ValDi\Parameters /t REG_DWORD /v TraceMMIOTimings /d 1 /f
REM reg add HKLM\SYSTEM\CurrentControlSet\Services\ValDi\Parameters /t REG_DWORD /v TracePipeUnderruns /d 0 /f
REM reg add HKLM\SYSTEM\CurrentControlSet\Services\ValDi\Parameters /t REG_DWORD /v TraceByCRCDoneInt /d 1 /f

%ValDiTarget%ValDiTest.exe -state
IF %ERRORLEVEL% LSS 17 (
    %ValDiTarget%devcon.exe disable =display *
    regsvr32 %ValDiTarget%msdia110.dll /s
    %ValDiTarget%PreValDi.exe -bp %drvPDBPath%
    IF !ERRORLEVEL! LSS 0 (
        ECHO Error parsing driver PDB file.
        %ValDiTarget%devcon.exe enable =display *
        goto :eof
    )
    %ValDiTarget%devcon.exe enable =display *
)
	
%ValDiTarget%ValDiTest.exe -restart
