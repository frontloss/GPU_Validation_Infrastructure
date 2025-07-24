namespace Intel.VPG.Display.Automation
{
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.Windows.Automation;
    using System.Windows.Forms;

    internal class MPlayerC : PlayerBase
    {
        internal override Process Instance(IApplicationSettings argAppSettings, int argCurrMethodIdx)
        {
            base.AppSettings = argAppSettings;
            base.CurrMethodIdx = argCurrMethodIdx;

            string playerName = "mplayerc.exe";
            if (string.IsNullOrEmpty(base.OverlayParams.Player))
                base.OverlayParams.Player = string.Format("{0}\\{1}", base.AppSettings.DisplayToolsPath, playerName);
            if (!File.Exists(base.OverlayParams.Player))
                Log.Abort("{0} does not exist!", base.OverlayParams.Player);

            Process playerProcess = Process.GetProcessesByName(playerName.Substring(0, playerName.IndexOf("."))).FirstOrDefault();
            if (null == playerProcess)
            {
                Log.Verbose("Launching {0}", base.OverlayParams.Player);
                playerProcess = CommonExtensions.StartProcess(base.OverlayParams.Player, string.Empty, 0);

                #region EnableOverlayMixer
                Thread.Sleep(1000);
                AutomationElement rootElement = AutomationElement.RootElement;
                Condition regCondition = null;
                AutomationElement appElement = null;

                base.SetWindowFocus(playerProcess);

                Thread.Sleep(1000);
                Log.Verbose("Launching options window");
                SendKeys.SendWait("o");

                Thread.Sleep(1000);
                Log.Verbose("Selecting playback output");
                SendKeys.SendWait("o");

                Thread.Sleep(1000);
                Log.Verbose("Locating overlay mixer option");
                regCondition = new PropertyCondition(AutomationElement.NameProperty, "Overlay Mixer *", PropertyConditionFlags.IgnoreCase);
                appElement = rootElement.FindFirst(TreeScope.Descendants, regCondition);
                if (appElement != null && appElement.Current.ControlType.Equals(ControlType.RadioButton))
                {
                    Thread.Sleep(1000);
                    Log.Verbose("Selecting overlay mixer option");
                    SelectionItemPattern pattern = appElement.GetCurrentPattern(SelectionItemPattern.Pattern) as SelectionItemPattern;
                    pattern.Select();
                }

                regCondition = new PropertyCondition(AutomationElement.NameProperty, "OK", PropertyConditionFlags.IgnoreCase);
                appElement = rootElement.FindFirst(TreeScope.Descendants, regCondition);
                if (appElement != null && appElement.Current.ControlType.Equals(ControlType.Button))
                {
                    Thread.Sleep(1000);
                    Log.Verbose("Committing option window");
                    InvokePattern pattern = appElement.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
                    pattern.Invoke();
                }
                #endregion
            }
            else
                playerProcess.StartInfo.FileName = base.OverlayParams.Player;

            return playerProcess;
        }

        internal override void Stop(Process argProcess)
        {
            base.StopPlayback(argProcess, ".");
        }
        internal override void Move(Process argProcess)
        {
            if (base.IsMoveApplicable())
            {
                base.Move(argProcess);
                base.StopPlayback(argProcess, ".");
                base.Play(argProcess);
            }
        }
        internal override void FullScreen(Process argProcess)
        {
            base.FullScreenPlayback(argProcess, "{LMenu down}{Enter}{LMenu up}");
        }
    }
}