===============================================================================
    DIVA KMD INSTALLATION: Script Usage Overview
===============================================================================

1. Extract the following files in the same folder on the DUT
- DivaKmd.sys
- DivaKmd.inf
- DivaKmd.cat 
- Devcon32/64.exe
- Install_DIVA-Package.ps1

2. Install the DIVA KMD by opening an admin command prompt and issue command:

powershell.exe -ExecutionPolicy Bypass -Command .\Install_DIVA-Package.ps1 -DivaPkgPath C:\Path\To\Folder\

3. Verify installation by opening Device Manager and look for DIVA under System Devices.

4. Remove the DIVA KMD by opening an admin command prompt and issue command:

powershell.exe -ExecutionPolicy Bypass -Command .\Install_DIVA-Package.ps1 -InstallAction Remove -DivaPkgPath C:\Path\To\Folder\


* PAVE uses execution vector to install the DIVA. 
* Build system dumps the binary artifacts in "Release" folder based on the architecture.
* Extract the Release folder from build system
* Use Diva-Add_x64.bat or Diva-Remove_x64.bat to install/ uninstall


===============================================================================
    DIVA INSTALLATION: BAT file usage overview
===============================================================================

0. Only DIVA folder named "Release" is supported, ensure whatever version you download is in a folder called "Release"

1. Download DIVA package and InstallTools folders

2. Copy all files from InstallTools to the same level as the Release folder

3. Open an admin command prompt and CD to the directory at step 2.

4. Issue command: Diva-Add_x64.bat

5. To uninstall: Diva-Remove_x64.bat