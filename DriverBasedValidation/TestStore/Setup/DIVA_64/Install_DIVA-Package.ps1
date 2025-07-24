#------------------------------------------------------------------------------
# Description: 
# This script installs DIVA-KMD & copies DIVA-Utilities to 'system32' folder.
# 
# Assumptions:
# (*) 'DivaKmd.sys' is properly signed & relevant catalog file - 'DivaKmd.cat' 
#     is available. See note below for signing related info.
# (*) The PS-Script is executed from Admin-Shell; add/remove action for a 
#     driver requires Admin-privileges.
# (*) 'DevconXX.exe' is available at the same folder as this script.
#
# Note: 
# Manual KMCS catalog file creation & signing can be performed from following 
# uBit-link: https://ubit-gfx.intel.com/overview/2318
# 
# Instructions to perform signing are available at:
# https://softwarecentralwiki.intel.com/index.php?title=Manual_KMCS_Signing
# 
# Input Parameters:
# InstallAction = Add (Default) | Remove
# DivaPkgPath   = <Add: Fully qualified path of DIVA package directory>
#                 <Remove: Fully qualified path of DIVA-INF file>
#
# Example command-lines:
# Add: .\Install_DIVA-Package.ps1 -DivaPkgPath C:\Intel\DIVA
# Remove: .\Install_DIVA-Package.ps1 -InstallAction Remove -DivaPkgPath C:\Intel\DIVA
# 
#------------------------------------------------------------------------------
Param(
    [Parameter(Mandatory=$true)]
    [ValidateScript(
        {
            If ((Test-Path -Path ($_ + "\DivaKmd.sys")))
            {
                $true
            }
            Else 
            {
                Throw "`r`n`n`"$_`" isn't a valid path or doesn't contain DIVA binaries!!!"
            }
        }
    )]
    [String] $DivaPkgPath, 

    [ValidateSet("Add", "Remove")]
    [String] $InstallAction = "Add"
)

# Get current OS Architecture
$OSInfoObj = Get-WmiObject -Class Win32_OperatingSystem;
$OSArch    = $OSInfoObj.OSArchitecture;
$OSVersion = $OSInfoObj.Version;
$OSVersion = $OSVersion.Substring(0, $OSVersion.LastIndexOf("."));

#------------------------------------------------------------------------------
# Description: 
# This function adds DIVA-catalogue file to 'Trusted Publisher Store' in OSes 
# up to Win-8.1.
#
# Note: 
# Any certificate used for signing DIVA-KMD needs to be added to the trusted 
# publisher store so that installation can proceed.
# 
# Input Parameters: 
# 
#------------------------------------------------------------------------------
function Add-Catalog-Win8 ()
{
    $LogMsg = "";

    # Check whether DIVA-Catalog file exists or not
    If ((Test-Path -Path ($DivaPkgPath + "\DivaKmd.cat")) -eq $false)
    {
        $LogMsg = "`r`n`nCouldn't locate DIVA-catalog file!!!";
        Throw $LogMsg;
    }

    # Prepare command-line switches for 'CertUtil.exe'
    $CertArgs = @(
        " -f", # Force overwrite
        " -addstore", # Add a certificate to the store
        " `"TrustedPublisher`"", # Certificate store name
        " $DivaPkgPath\DivaKmd.cat" # Catalog file name
    );

    # Invoke 'CertUtil.exe'
    $CertCmd = "$env:windir\System32\CertUtil.exe";
    $CertProcess = Start-Process $CertCmd -ArgumentList "$CertArgs" -Wait -NoNewWindow -PassThru

    If ($CertProcess.ExitCode -ne 0)
    {
        $LogMsg  = "`r`n`nDIVA-Add: Certificate configuration process (ID = 0x" + "{0:X}" -f $($CertProcess.Id);
        $LogMsg += ") has errored out, with code: 0x" + "{0:X}" -f $($CertProcess.ExitCode);
        Throw $LogMsg;
    }
    Else
    {
        $LogMsg = "`r`nDIVA-Add: Certificate configuration process (ID = 0x" + "{0:X}" -f $($CertProcess.Id);
        $LogMsg += ") has succeeded...";
        $LogMsg;
    }

    Return;
} # end 'Add-Catalog-Win8'

#------------------------------------------------------------------------------
# Description: 
# This function adds DIVA-catalogue file to 'Trusted Publisher Store' in OSes 
# beyond Win-10.0.
#
# Note: 
# '..\System32\CertUtil.exe' is not working on Win-10, so this function is an 
# exclusive fix for Win-10.
#
# Input Parameters: 
# 
#------------------------------------------------------------------------------
function Add-Catalog-Win10 ()
{
    $LogMsg = "";

    # Initialize instance of X.509 store, which is a physical store where 
    # certificates are persisted & managed.
    Try
    {
        $StoreName     = "TrustedPublisher";
        $StoreLocation = "LocalMachine";
        $Store = New-Object System.Security.Cryptography.X509Certificates.X509Store($StoreName, $StoreLocation); 
    }
    Catch
    {
        $LogMsg  = "`r`n`nFailed to initialize new instance of 'X.509-Store' using Store-Name: " + $StoreName;
        $LogMsg += " & Store-Location: " + $StoreLocation;
        Throw $LogMsg; 
    }

    # Open X.509 store with highest allowed access
    Try
    {
        $Store.Open([System.Security.Cryptography.X509Certificates.OpenFlags]::MaxAllowed);
    }
    Catch
    {
        $LogMsg  = "`r`n`nFailed to open 'X.509-Store' using highest allowed access permission...";
        Throw $LogMsg; 
    }

    # Create a X.509 certificate for DIVA using Catalog-File
    Try
    {
        $DivaCert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2($DivaPkgPath + "\divakmd.cat");
    }
    Catch
    {
        $LogMsg = "`r`n`nFailed to initialize new instance of 'X.509-Certificate' using DIVA-Catlalog file...";
        Throw $LogMsg; 
    }

    # Add DIVA-X.509 Certificate to Store
    Try
    {
        $Store.Add($DivaCert);
    }
    Catch
    {
        $LogMsg = "`r`n`nFailed to add 'DIVA-Catalog file' to 'X.509 Certificate Store'...";
        Throw $LogMsg; 
    }

    # Close X.509 Certificate Store to release all resources associated with store
    $Store.Close();

    $LogMsg = "`r`nDIVA-Add: Certificate configuration process has succeeded...";
    $LogMsg;
    Return;
} # end 'Add-Catalog-Win10'

#------------------------------------------------------------------------------
# Description: 
# This function installs DIVA-KMD and copies associated user-mode DIVA-Utility 
# DLLs to 'System32' folder.
#
# Note-1: 
# Installation of DIVA-KMD is carried out using the tool Device Console (Devcon).
# The Devcon tool logs high-level installation information and error messages 
# in a log file (%windir%\inf\setupapi.dev.log). SetupAPI log file is a plain-text 
# file that contains device installation information and can be used to verify the 
# instllation of a device and troubleshoot device installation problems.
#
# Note-2:
# DevCon returns an integer that can be used in programs and scripts to determine 
# the success of a DevCon command (for example, return = devcon hwids *).
# Devcon return codes are specified here:
# https://msdn.microsoft.com/en-us/library/windows/hardware/ff544766(v=vs.85).aspx
# 
#------------------------------------------------------------------------------
function Add-DIVA ()
{
    $LogMsg = "";

    # Check whether DIVA-INF file exists or not
    If ((Test-Path -Path ($DivaPkgPath + "\DivaKmd.inf")) -eq $false)
    {
        $LogMsg = "`r`n`nCouldn't locate DIVA-INF file!!!";
        Throw $LogMsg;
    }

    $InfFile = $DivaPkgPath + "\DivaKmd.inf"

    # Prepare command-line switches for 'Devcon.exe'
    $DevconArgs = @(
        " install", # Devcon command to be processed
        " $InfFile", # Installation information file name
        " DivaSwKmd" # Hardware Id
    );

    # Invoke 'Devcon.exe'
    If ($script:OSArch -eq '64-bit')
    {
        $Devcon = $DivaPkgPath + "\Devcon64.exe";
    }
    Else
    {
        $Devcon = $DivaPkgPath + "\Devcon32.exe";
    }

    $DevconInstallProcess = Start-Process $Devcon -ArgumentList "$DevconArgs" -Wait -NoNewWindow -PassThru

    $InstallStatus = $DevconInstallProcess.ExitCode

    If ( ($InstallStatus -eq 2) -or ($Installstatus -eq 3)) # Return code 3 or 2 indicates error
    {
        $LogMsg  = "`r`n`nDIVA-Add: Installation process (ID = 0x" + "{0:X}" -f $($DevconInstallProcess.Id);
        $LogMsg += ") has errored out, with code: 0x" + "{0:X}" -f $($DevconInstallProcess.ExitCode);
        $LogMsg += "`r`nSee '%windir%\inf\setupapi.dev.log' for more details...";
        Throw $LogMsg;
    }
    Else
    {
        $LogMsg = "`r`nDIVA-Add: Installation process (ID = 0x" + "{0:X}" -f $($DevconInstallProcess.Id);
        $LogMsg += ") has succeeded...";
        $LogMsg;
    }

    # Copy DIVA-Utility & Co-installer DLLs to 'System32' folder
    Get-ChildItem -Path $DivaPkgPath -Filter *.dll | Copy-Item -Destination "$env:windir\System32" -Force;

    $LogMsg = "`r`nDIVA-Add: Copied DIVA-Utility & Co-installer DLLs to '$env:windir\System32'";
    $LogMsg;

    If ($InstallStatus -eq 1) # Return code 1 indicates success, but reboot required
    {
        $LogMsg = "System reboot required...";
        Write-Host -ForegroundColor Red $LogMsg;
    }

    Return;
} # end 'Add-DIVA'

#------------------------------------------------------------------------------
# Description: 
# This function un-installs DIVA-KMD and deletes user-mode DIVA-Utility DLLs 
# from 'System32' folder.
#
# Note: 
# In case of Win-7, the WDF-Coinstaller DLL isn't deleted as it may be needed 
# by other drivers.
#
# Input Parameters: 
# 
#------------------------------------------------------------------------------
function Remove-DIVA ()
{
    $LogMsg = "";

    # Check whether DIVA-INF file exists or not
    If ((Test-Path -Path ($DivaPkgPath + "\DivaKmd.inf")) -eq $false)
    {
        $LogMsg = "`r`n`nCouldn't locate DIVA-INF file!!!";
        Throw $LogMsg;
    }

    # Prepare command-line switches for 'Devcon.exe'
    $DevconArgs = @(
        " remove", # Devcon command to be processed
        " DivaSwKmd" # Hardware Id
    );

    # Invoke 'Devcon.exe'
    If ($script:OSArch -eq '64-bit')
    {
        $Devcon = ".\Devcon64.exe";
    }
    Else
    {
        $Devcon = ".\Devcon32.exe";
    }
    $DevconProcess = Start-Process $Devcon -ArgumentList "$DevconArgs" -Wait -NoNewWindow -PassThru

    If (($DevconProcess.ExitCode -eq 3) -or ($DevconProcess.ExitCode -eq 2)) # Return code 3 or 2 indicates error
    {
        $LogMsg  = "`r`n`nDIVA-Remove: Uninstallation process (ID = 0x" + "{0:X}" -f $($DevconProcess.Id);
        $LogMsg += ") has errored out, with code: 0x" + "{0:X}" -f $($DevconProcess.ExitCode);
        Throw $LogMsg;
    }
    Else
    {
        $LogMsg = "`r`nDIVA-Remove: Uninstallation process (ID = 0x" + "{0:X}" -f $($DevconProcess.Id);
        $LogMsg += ") has succeeded...";
        $LogMsg;
    }

    # Remove DIVA-Utility DLLs from 'System32' folder
    Get-ChildItem -Path "$env:windir\System32" -Filter DivaUtility*.dll | Remove-Item -Force;

    $LogMsg = "`r`nDIVA-Remove: Deleted DIVA-Utility DLLs from '$env:windir\System32'";
    $LogMsg;

    If ($DevconProcess.ExitCode -eq 1) # Return code 1 indicates success, but reboot required
    {
        $LogMsg = "System reboot required...";
        Write-Host -ForegroundColor Red $LogMsg;
    }

    Return;
} # end 'Remove-DIVA'

# Perform Add / Remove action
If ($InstallAction -eq 'Add')
{
    # Add DIVA-catalog file to trusted publisher store
    If($OSVersion -match "6.*") # Win-7: 6.1.7600, Win-8: 6.2.9200, Win-8.1: 6.3.9600
    {
        Add-Catalog-Win8;
    }
    Else
    {
        Add-Catalog-Win10;
    }

    # Install DIVA-KMD
    Add-DIVA;
}
Else
{
    # Uninstall DIVA-KMD
    Remove-DIVA;
}

Return;
