#------------------------------------------------------------------------------
# Description: 
# This script makes use of 'MSBuild.exe' to build all the projects in 
# 'DIVA_FW.sln'.
# 
# Note:
# Starting with VS-2013, 'MSBuild' is installed as part of VS, rather than as 
# part of the .NET Framework. The 'MSBuild' version number with VS-2013 is '12.0' 
# with VS-2015 is '14.0'.
# Following are the 'MSBuild' install locations: 
# (*) 32-bit machines: C:\Program Files\MSBuild\*\bin
# (*) 32-bit toolset on 64-bit machines: C:\Program Files (x86)\MSBuild\*\bin
# (*) 64-bit toolset on 64-bit machines: C:\Program Files (x86)\MSBuild\*\bin\amd64
# 
# It suffices to use 32-bit toolset on 64-bit machines unless targeting for 
# extended memory access.
# 
# Pre-requisites: 
# (1) Microsoft Visual Studio with VC-tools
# (2) .NET Framework - 4.5
# 
# Input Parameters:
# BuildDir      = <Fully qualified path to hold build-output>
# DivaSolnPath  = <Fully qualified path of DIVA-VS solution>
# Configuration = Debug | Release (Default)
# Platform      = Win32 | x86 | x64 (Default)
#
# Example command-line: 
# Assuming that script is being executed from '...\DivaScripts' folder:
# .\Build_DIVA-Package.ps1 -BuildDir ..\DivaBuild -DivaSolnPath ..\
# Make sure that '..\DivaBuild' exists.
# 
#------------------------------------------------------------------------------
Param(
    [Parameter(Mandatory=$true)]
    [ValidateScript(
        {
            If ((Test-Path -Path ($_)))
            {
                $true
            }
            Else 
            {
                Throw "`r`nBuild output location:`"$_`" isn't a valid directory!!!"
            }
        }
    )]
    [String] $BuildDir, 

    [Parameter(Mandatory=$true)]
    [ValidateScript(
        {
            If ((Test-Path -Path ($_ + "\DIVA_FW.sln")))
            {
                $true
            }
            Else
            {
                Throw "`r`n`"$_`" isn't a valid path or doesn't contain DIVA-VS solution!!!"
            }
        }
    )]
    [String] $DivaSolnPath, 

    [ValidateSet("Debug", "Release")]
    [String] $Configuration = "Release",

    [ValidateSet("Win32", "x86", "x64")]
    [String] $Platform = "x64"
)

# Overwrite value 'Win32' with 'x86' for Platform
If ($Platform -ne 'x64')
{
    $Platform = "x86";
}

# Display input parameters
"`r`nInput parameters: ";
"`tBuild output path  = $BuildDir";
"`tDIVA solution path = $DivaSolnPath";
"`tConfiguration      = $Configuration";
"`tPlatform           = $Platform`n";

# List script-level variables
$MSBuildCmd = ""; # Fully qualified 'MSBuild.exe' name

# Derive Build-machine's OS-architecture
$OSInfoObj = Get-CimInstance Win32_OperatingSystem;
$OSArch    = $OSInfoObj.OSArchitecture;

#------------------------------------------------------------------------------
# Description: 
# This function verifies whether all the pre-requisite SW components are 
# available in the build-system.
#
# Input Parameters: 
# 
#------------------------------------------------------------------------------
function Check-Requisites ()
{
    # Check whether some version of visual studio is installed or not; 
    # If so, get path of the latest version
    $VSEnvVars = (dir Env:).Name -match "VS[0-9]{1,3}COMNTOOLS"
    $LatestVS = $VSEnvVars | Sort-Object | Select -Last 1

    $MsvcPath = (Get-Content Env:\$LatestVS) + "..\..\VC";
    If ((Test-Path -Path ($MsvcPath + "\bin\CL.exe")) -eq $false)
    {
        Throw "`r`nCouldn't locate Visual Studio C++ tools!!!";
    }

    # Check whether at least .NET Framework-4.5 is installed or not
    $DotNetFWObj = Get-ChildItem 'HKLM:\SOFTWARE\Microsoft\NET Framework Setup\NDP' -recurse | 
                   Get-ItemProperty -name Version -ErrorAction SilentlyContinue | 
                   Where {$_.PSChildName -match '^(?!S)\p{L}'} | 
                   Sort-Object -Property Version | 
                   Select -Last 1;
    $DotNetVersion = $DotNetFWObj.Version;
    If ($DotNetVersion -lt '4.5')
    {
        Throw "`r`n.NET Framework >= v4.5 is required!!!";
    }

    # Set path of 'MSBuild.exe' based on OS-architecture
    If ($script:OSArch -eq '64-bit')
    {
        # Note: Only 32-bit toolset is used
        $script:MSBuildCmd = (Resolve-Path "C:\Program Files (x86)\MSBuild\*\Bin\MSBuild.exe" | Sort-Object | Select -Last 1).Path;
    }
    Else
    {
        $script:MSBuildCmd = (Resolve-Path "C:\Program Files\MSBuild\*\Bin\MSBuild.exe" | Sort-Object | Select -Last 1).Path;
    }

    Return;
} # end 'Check-Requisites'

#------------------------------------------------------------------------------
# Description: 
# This function cleans previous build of 'DIVA_FW.sln'.
#
# Input Parameters: 
# 
#------------------------------------------------------------------------------
function Clean-Solution ()
{
    $TimeStamp = "[UTC: " + (Get-Date).ToUniversalTime().ToString() + "]";
    "`r`n$TimeStamp DIVA-SLN: Cleaning DIVA-Solution before Build...";

    # Prepare command-line switches for 'MSBuild.exe'
    $MSBuildArgs = @(
        " $DivaSolnPath\DIVA_FW.sln", # Name of the solution
        " /target:Clean", # Target Action
        " /property:Configuration=$Configuration;Platform=$Platform" # Properties defined in project files
    );

    # Launch MSBuild-process using 'System.Diagnostics.Process' object.
    $MSBuildProcess = New-Object System.Diagnostics.Process;
    $MSBuildProcess.StartInfo.FileName  = $script:MSBuildCmd;
    $MSBuildProcess.StartInfo.Arguments = $MSBuildArgs;
    $MSBuildProcess.StartInfo.RedirectStandardOutput = $true;
    $MSBuildProcess.StartInfo.RedirectStandardError  = $true;
    $MSBuildProcess.StartInfo.UseShellExecute        = $false; # Mandatory with STD-OUT/ERR redirection
    $MSBuildProcess.Start() | Out-Null;

    Write-Host $MSBuildProcess.StandardOutput.ReadToEnd();
    Write-Host $MSBuildProcess.StandardError.ReadToEnd();
    $MSBuildProcess.WaitForExit();

    # $MSBuildProcess = Start-Process $script:MSBuildCmd -ArgumentList "$MSBuildArgs" -Wait -NoNewWindow -PassThru

    $TimeStamp = "[UTC: " + (Get-Date).ToUniversalTime().ToString() + "]";
    If ($MSBuildProcess.ExitCode -ne 0)
    {
        Throw "`r$TimeStamp DIVA-SLN: Clean process (ID = $($MSBuildProcess.Id)) has errored out, with code: $($MSBuildProcess.ExitCode)";
    }
    Else
    {
        "`r$TimeStamp DIVA-SLN: Clean process (ID = " + $($MSBuildProcess.Id) + ") has succeeded...";
    }

    Return;
} # end 'Clean-Solution'

#------------------------------------------------------------------------------
# Description: 
# This function builds 'DIVA_FW.sln'.
#
# Input Parameters: 
# 
#------------------------------------------------------------------------------
function Build-Solution ()
{
    $TimeStamp = "[UTC: " + (Get-Date).ToUniversalTime().ToString() + "]";
    "`r`n$TimeStamp DIVA-SLN: Building DIVA-Solution...";

    # Prepare command-line switches for 'MSBuild.exe'
    $MSBuildArgs = @(
        " $DivaSolnPath\DIVA_FW.sln", # Name of the solution
        " /target:Build", # Target Action
        " /property:Configuration=$Configuration;Platform=$Platform" # Properties defined in project files
    );

    # Append build related pre-processor macros defined by QB.
    If($env:QB_COREVAL_BUILD_VERSION) # Format: M.m.b <Major-Version.Minor-Version.Build-Number>
    {
        $MSBuildArgs += " /property:DefineConstants=`"BUILD_VERSION=$env:QB_COREVAL_BUILD_VERSION`"";
    }

    If($env:QB_COREVAL_BUILD_BRANCH) # Example: <Mainline, INT_GEN9_2015, ...>
    {
        $MSBuildArgs += " /property:DefineConstants=`"BUILD_BRANCH=$env:QB_COREVAL_BUILD_BRANCH`"";
    }

    If($env:QB_COREVAL_BUILD_STREAM) # Example: CoreVal/<CI / Production / Developer>
    {
        $MSBuildArgs += " /property:DefineConstants=`"BUILD_STREAM=$env:QB_COREVAL_BUILD_STREAM`"";
    }

    If($env:QB_COREVAL_BUILD_LOCATION) # Example: <CoreVal-Build-System, Desktop, ...>
    {
        $MSBuildArgs += " /property:DefineConstants=`"BUILD_LOCATION=$env:QB_COREVAL_BUILD_LOCATION`"";
    }

    # Launch MSBuild-process using 'System.Diagnostics.Process' object.
    $MSBuildProcess = New-Object System.Diagnostics.Process;
    $MSBuildProcess.StartInfo.FileName  = $script:MSBuildCmd;
    $MSBuildProcess.StartInfo.Arguments = $MSBuildArgs;
    $MSBuildProcess.StartInfo.RedirectStandardOutput = $true;
    $MSBuildProcess.StartInfo.RedirectStandardError  = $true;
    $MSBuildProcess.StartInfo.UseShellExecute        = $false; # Mandatory with STD-OUT/ERR redirection
    $MSBuildProcess.Start() | Out-Null;

    Write-Host $MSBuildProcess.StandardOutput.ReadToEnd();
    Write-Host $MSBuildProcess.StandardError.ReadToEnd();
    $MSBuildProcess.WaitForExit();

    # $MSBuildProcess = Start-Process $script:MSBuildCmd -ArgumentList "$MSBuildArgs" -Wait -NoNewWindow -PassThru

    $TimeStamp = "[UTC: " + (Get-Date).ToUniversalTime().ToString() + "]";
    If ($MSBuildProcess.ExitCode -ne 0)
    {
        Throw "`r$TimeStamp DIVA-SLN: Build process (ID = $($MSBuildProcess.Id)) has errored out, with code: $($MSBuildProcess.ExitCode)";
    }
    Else
    {
        "`r$TimeStamp DIVA-SLN: Build process (ID = " + $($MSBuildProcess.Id) + ") has succeeded...";
    }

    Return;
} # end 'Build-Solution'


#------------------------------------------------------------------------------
# Description: 
# This function copies pre-built DIVA binaries to the specified directory.
#
# Input Parameters: 
# 
#------------------------------------------------------------------------------
function Copy-Package ()
{
    $TimeStamp = "[UTC: " + (Get-Date).ToUniversalTime().ToString() + "]";
    "`r`n$TimeStamp Copying pre-built DIVA-binaries to destination-folder..."

    $DivaBinaryPath = $DivaSolnPath; # Root solution directory
    If ($Platform -eq 'x64')
    {
        $DivaBinaryPath += '\x64'; # Location of 'x64' binaries
    }
    $DivaBinaryPath += ('\' + $Configuration); # Navigating to binary location

    # Create list of DIVA-package items
    # (1) *.inf
    # (2) *.sys
    # (3) *.dll
    # (4) *.pdb
    # (5) *.exe
    $DivaPkg = Get-ChildItem -Path $DivaBinaryPath -Recurse -Include *.inf, *.sys, *.dll, *.pdb, *.exe -ErrorAction SilentlyContinue;

    # Clear previous contents of 'Build-Output' directory
    Get-ChildItem $BuildDir\*.* -Recurse | Remove-Item -Force;

    # Copy DIVA-package items to 'Build-Output' directory
    $DivaPkg | Copy-Item -Destination $BuildDir;

    $TimeStamp = "[UTC: " + (Get-Date).ToUniversalTime().ToString() + "]";
    "`r$TimeStamp Copy completed..."

    Return;
} # end 'Copy-Package'

# Check whether all pre-requisites are available or not
Check-Requisites;

# Clean prevous build contents
Clean-Solution;

# Build new DIVA binaries
Build-Solution;

# Copy the newly built binaries to output directory
Copy-Package;

"`r`nHurrah!!! DIVA-QB package created..."
