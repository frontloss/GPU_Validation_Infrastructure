@echo off

SET myPATH=%~dp0
SET myPathiClick=%~dp0
start %myPathiClick%iClick.exe /arm

if /i "%~1" EQU "i" goto INSTALL
if /i "%~1" EQU "u" goto UNINSTALL

:EXIT
goto DONE


:INSTALL
%myPATH%\devcon.exe install %myPATH%\GfxValSimDriver.inf root\umbus
goto DONE

:UNINSTALL

rem Disabling GFX Adapter before actually uninstalling Val Sim Driver

%myPATH%\devcon.exe disable =display PCI\VEN_8086*

rem Uninstall Val Sim Driver

%myPATH%\devcon.exe /r remove root\umbus

rem RE-enabling GFX Adapter

%myPATH%\devcon.exe enable =display PCI\VEN_8086*

rem Clearing Persistence File

DEL /F /Q C:\Windows\SimDrvPersistenceFile.txt

goto DONE

:DONE
start %myPathiClick%iClick.exe /disarm