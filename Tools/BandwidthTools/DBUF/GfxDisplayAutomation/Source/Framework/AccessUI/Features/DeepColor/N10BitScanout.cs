namespace Intel.VPG.Display.Automation
{
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.Windows.Automation;
    using System;

    internal class N10BitScanout : DeepColorBase
    {
        const string DxSdk_Installer = "DXSDK_Jun10.exe";
        const string installDir = "\\Microsoft DirectX SDK (June 2010)\\Samples\\C++\\Direct3D10\\Bin\\";
        const string AppName = "10BitScanout10.exe";

        internal override Process Instance(IApplicationSettings argAppSettings, int argCurrMethodIdx)
        {
            base.AppSettings = argAppSettings;
            base.CurrMethodIdx = argCurrMethodIdx;
            base.DeepcolorParams.DeepColorApplication = AppName;

            Process playerProcess = Process.GetProcessesByName(base.DeepcolorParams.DeepColorApplication.Substring
                (0, base.DeepcolorParams.DeepColorApplication.IndexOf("."))).FirstOrDefault();

            if (null == playerProcess)
            {
                string programFilesPath = Environment.Is64BitOperatingSystem ? Environment.GetFolderPath(
                    Environment.SpecialFolder.ProgramFilesX86) : Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles);

                string applicationPath = "";
                if (IntPtr.Size.Equals(8))
                {
                    applicationPath = string.Format("{0}{1}x64\\{2}", programFilesPath, installDir,
                    base.DeepcolorParams.DeepColorApplication);
                }
                else
                {
                    applicationPath = string.Format("{0}{1}x86\\{2}", programFilesPath, installDir,
                   base.DeepcolorParams.DeepColorApplication);
                }

                if (!File.Exists(applicationPath))
                {
                    Log.Verbose("Installing {0}", DxSdk_Installer);
                    InstallDxSDK();
                }

                Log.Verbose("Launching {0}", base.DeepcolorParams.DeepColorApplication);
                playerProcess = new Process();
                playerProcess.StartInfo.FileName = applicationPath;
                playerProcess.Start();
            }
            return playerProcess;
        }

        internal override void Move(Process argProcess)
        {
        }

        private void InstallDxSDK()
        {
            string installerPath = string.Format("{0}\\{1}", base.AppSettings.OverlayPlayersPath, DxSdk_Installer);
            if (!File.Exists(installerPath))
                Log.Abort("{0} does not exist!", installerPath);

            Log.Verbose("Installing {0} from {1}", DxSdk_Installer, installerPath);
            Process p = Process.Start(installerPath, "/U");
            p.WaitForExit();
        }
    }
}