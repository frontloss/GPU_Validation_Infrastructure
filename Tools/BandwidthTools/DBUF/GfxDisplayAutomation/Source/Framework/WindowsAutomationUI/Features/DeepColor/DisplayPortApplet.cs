namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Windows.Automation;

    internal class DisplayPortapplet : DeepColorBase
    {
        private enum AppletAction
        {
            Enable,
            Disable,
            ForceDeepColor,
            Reset,
            Popup
        }
        private Dictionary<AppletAction, ControlParams> _appActions = null;

        internal override Process Instance(IApplicationSettings argAppSettings, int argCurrMethodIdx)
        {
            base.AppSettings = argAppSettings;
            base.CurrMethodIdx = argCurrMethodIdx;
            string playerName = "DisplayPortApplet.exe";

            if (string.IsNullOrEmpty(base.DeepcolorParams.DeepColorApplication))
                base.DeepcolorParams.DeepColorApplication = string.Format("{0}\\{1}", base.AppSettings.DisplayToolsPath, playerName);
            if (!File.Exists(base.DeepcolorParams.DeepColorApplication))
                Log.Abort("{0} does not exist!", base.DeepcolorParams.DeepColorApplication);

            if (_appActions == null)
            {
                _appActions = new Dictionary<AppletAction, ControlParams>();
                _appActions.Add(AppletAction.Enable, new ControlParams() { ControlType = ControlType.ListItem, Name = "force deep color", AutomationID = "1038" });
                _appActions.Add(AppletAction.Disable, new ControlParams() { ControlType = ControlType.ListItem, Name = "normal mode(best bpc)", AutomationID = "1038" });
                _appActions.Add(AppletAction.ForceDeepColor, new ControlParams() { ControlType = ControlType.Button, AutomationID = "1039" });
                _appActions.Add(AppletAction.Reset, new ControlParams() { ControlType = ControlType.Button, AutomationID = "1022" });
                _appActions.Add(AppletAction.Popup, new ControlParams() { ControlType = ControlType.Button, AutomationID = "2" });
            }

            Process playerProcess = Process.GetProcessesByName(playerName.Substring(0, playerName.IndexOf("."))).FirstOrDefault();
            if (null == playerProcess)
            {
                Log.Verbose("Launching {0}", base.DeepcolorParams.DeepColorApplication);
                playerProcess = CommonExtensions.StartProcess(base.DeepcolorParams.DeepColorApplication, string.Empty, 0);
            }

            //Used for cleanup of DPApplet during test cleanup.
            TestPostProcessing.RegisterPlayersProcess(playerProcess);

            return playerProcess;
        }

        internal override void Move(Process argProcess)
        {

        }

        internal override void EnableDeepColor(Process argProcess)
        {
            Log.Verbose("Enabling DeepColor");
            PerformAction(AppletAction.Enable);
            PerformAction(AppletAction.ForceDeepColor);
        }

        internal override void DisableDeepColor(Process argProcess)
        {
            Log.Verbose("Disabling DeepColor");
            PerformAction(AppletAction.Disable);
            PerformAction(AppletAction.ForceDeepColor);
        }

        private void PerformAction(AppletAction appletAction)
        {
            ControlParams popUpParam = _appActions[AppletAction.Popup];
            AutomationElement PopUpAppElement = null;
            Log.Verbose("before popupelement");
            PopUpAppElement = AutomationElement.RootElement.FindFirst(TreeScope.Descendants, new PropertyCondition(AutomationElement.AutomationIdProperty, popUpParam.AutomationID));
            Thread.Sleep(5000);
            Log.Verbose("after popupelement");
            if (PopUpAppElement != null)
            {
                Log.Verbose("not null");
                InvokePattern pattern1 = PopUpAppElement.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
                Log.Verbose("after pattern");
                if (pattern1 == null)
                    Log.Abort("Unable to get handle for the button with AutomationID:{0}", popUpParam.AutomationID);
                Log.Verbose("before invoke");
                pattern1.Invoke();
                Log.Verbose("after invoke");
            }

            AutomationElement appElement = null;
            ControlParams param = null;

            param = _appActions[appletAction];

            appElement = AutomationElement.RootElement.FindFirst(TreeScope.Descendants, new PropertyCondition(AutomationElement.AutomationIdProperty, param.AutomationID));

            if (param.ControlType == ControlType.Button)
            {
                InvokePattern pattern = appElement.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
                if (pattern == null)
                    Log.Abort("Unable to get handle for the button with AutomationID:{0}", param.AutomationID);
                pattern.Invoke();
            }
            else if (param.ControlType == ControlType.ListItem)
            {
                appElement = appElement.FindFirst(TreeScope.Children, new PropertyCondition(AutomationElement.NameProperty, param.Name, PropertyConditionFlags.IgnoreCase));

                SelectionItemPattern rpa = appElement.GetCurrentPattern(SelectionItemPattern.Pattern) as SelectionItemPattern;
                if (rpa == null)
                    Log.Abort("Unable to get handle for the ListItem:{0}", param.Name);
                rpa.Select();
            }
        }
    }
}