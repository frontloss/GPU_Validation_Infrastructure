namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;

    internal class ArcSoft : PlayerBase
    {
        internal override Process Instance(IApplicationSettings argAppSettings, int argCurrMethodIdx)
        {
            base.AppSettings = argAppSettings;
            base.CurrMethodIdx = argCurrMethodIdx;

            if (string.IsNullOrEmpty(base.OverlayParams.Player))
                base.OverlayParams.Player = "uTotalMediaTheatre5.exe";
            Process playerProcess = this.GetPlayerProcess();
            if (null == playerProcess)
            {
                GetFilePath();
             //   playerProcess.StartInfo.FileName = this.GetFilePath();
            }
                return playerProcess;
        }
        internal override void Stop(Process argProcess)
        {
            base.StopPlayback(argProcess, "o");
        }
        internal override void Move(Process argProcess)
        {
            if (base.IsMoveApplicable())
            {
                base.Move(argProcess);
                Thread.Sleep(15000);
            }
        }
        internal override void FullScreen(Process argProcess)
        {
            base.FullScreenPlayback(argProcess, "z");
        }
        internal override void Play(Process argProcess)
        {
            if (null != argProcess)
            {
                base.Close(argProcess);
                Thread.Sleep(2000);
            }
            Log.Verbose("Running {0}", base.OverlayParams.VideoFile);
            string videoFile = string.Format("{0}\\{1}", base.AppSettings.OverlayPlayersPath, base.OverlayParams.VideoFile);
            base.CheckVideoFileExists(videoFile);
            argProcess = CommonExtensions.StartProcess(this.GetFilePath(), videoFile, 0);
            this.IsPlayerLoaded();
            Thread.Sleep(5000);
        }

        private Process GetPlayerProcess()
        {
            return Process.GetProcessesByName(base.OverlayParams.Player.Substring(0, base.OverlayParams.Player.IndexOf("."))).FirstOrDefault();
        }
        private void IsPlayerLoaded()
        {
            bool notExists = true;
            while (notExists)
            {
                try
                {
                    notExists = (null == this.GetPlayerProcess());
                    Thread.Sleep(5000);
                }
                catch (Exception ex)
                {
                    Log.Sporadic(false, "ArcSoftPlayerStart:: {0}", ex.Message);
                    Log.Verbose("{0}", ex.StackTrace);
                    Thread.Sleep(5000);
                }
            }
        }
        private string GetFilePath()
        {
            string installDir = "\\ArcSoft\\TotalMedia Theatre 5\\";
            string filePath = string.Format("{0}{1}{2}", Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86), installDir, base.OverlayParams.Player);
            if (!File.Exists(filePath))
                filePath = string.Format("{0}{1}{2}", Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles), installDir, base.OverlayParams.Player);
            if (!File.Exists(filePath))
            {
                ArcSoftInstallation install = new ArcSoftInstallation();
                install.AppSettings = base.AppSettings;
                install.CurrentMethodIndex = base.CurrMethodIdx;
                install.StartInstallation();
            }
            return filePath;
        }
    }
}