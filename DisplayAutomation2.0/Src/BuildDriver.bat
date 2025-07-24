echo "BuildDriver.bat has been called with the following args: " %*

if exist "%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" (
    @echo Found vswhere.exe
    set vswhere_path="%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"
    goto success
)

:noVisualStudio
@echo ERROR: Visual Studio 2017 is not installed
exit /b -1

:success
REM Find the path to where Visual Studio is installed using vswhere.exe
for /f "usebackq tokens=*" %%i in (`%%vswhere_path%% -version 15.0 -products * -requires Microsoft.Component.MSBuild -property installationPath`) do (
  set VCINSTALLDIR=%%i
  set MSBUILDDIR=%%i\MSBuild\15.0\Bin
)

call "%VCINSTALLDIR%\VC\Auxiliary\Build\vcvars64.bat"

REM Set the VCINSTALLDIR variable so that the BuildDriver.wsf script can read the variable
REM and reconstruct the path to MSBuild.exe
if not exist "%MSBUILDDIR%\MSBuild.exe" goto noVisualStudio

REM echo " setmsbuild" 
REM set msbuild="%VCINSTALLDIR%\MSBuild\15.0\Bin\MSBuild.exe"

echo "Building ValDisplay next"
MSBuild.exe MasterSolution.sln /p:Configuration=Release /p:Platform=x64
if %ERRORLEVEL% NEQ 0 (
 echo %ERRORLEVEL% found in DisplayAutomation2.0\Src\MasterSolution build
 exit /b %ERRORLEVEL%
)

echo "Building TestApp next"
MSBuild.exe TestApp.sln /p:Configuration=Release /p:Platform=x64
if %ERRORLEVEL% NEQ 0 (
 echo %ERRORLEVEL% found in DisplayAutomation2.0\Src\TestApp build
 exit /b %ERRORLEVEL%
)

set error_level=%ERRORLEVEL%
echo Exiting BuildDriver.bat with %error_level%
exit /b %error_level%
