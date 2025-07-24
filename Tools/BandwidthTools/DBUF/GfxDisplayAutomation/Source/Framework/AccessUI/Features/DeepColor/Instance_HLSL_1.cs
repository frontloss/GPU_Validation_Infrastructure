namespace Intel.VPG.Display.Automation
{
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.Windows.Automation;

    internal class Instance_HLSL : DeepColorBase
    {
        internal override Process Instance(IApplicationSettings argAppSettings, int argCurrMethodIdx)
        {
            base.AppSettings = argAppSettings;
            base.CurrMethodIdx = argCurrMethodIdx;
            string playerName = "Instance_HLSL_1.exe";

            if (string.IsNullOrEmpty(base.DeepcolorParams.DeepColorApplication))
                base.DeepcolorParams.DeepColorApplication = string.Format("{0}\\XRnBGR\\{1}", base.AppSettings.OverlayPlayersPath, playerName);
            if (!File.Exists(base.DeepcolorParams.DeepColorApplication))
                Log.Abort("{0} does not exist!", base.DeepcolorParams.DeepColorApplication);

            Process playerProcess = Process.GetProcessesByName(playerName.Substring(0, playerName.IndexOf("."))).FirstOrDefault();
            if (null == playerProcess)
            {
                Log.Verbose("Launching {0}", playerName);
                playerProcess = CommonExtensions.StartProcess(base.DeepcolorParams.DeepColorApplication, "-fs -hal -fl 10.0 -fmt FP16", 0);
            }
            return playerProcess;
        }

        internal override void Move(Process argProcess)
        {
            if (base.IsMoveApplicable())
            {
                base.Move(argProcess);
            }
        }
    }
}