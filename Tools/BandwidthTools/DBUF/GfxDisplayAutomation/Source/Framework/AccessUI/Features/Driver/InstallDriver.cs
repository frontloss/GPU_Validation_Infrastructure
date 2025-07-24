namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Windows.Automation;
    using System.Threading;
    using System.IO;
    using System.Timers;
    public class InstallDriver : FunctionalBase, ISetMethod
    {
        private class VerifyOption
        {
            internal string name;
            internal string ID;
            internal bool status;
        }
        private List<VerifyOption> _verify = new List<VerifyOption>();
        private List<ControlParams> _elementSequence = new List<ControlParams>();
        private string setUpFilePath = string.Empty;
        private bool SUCCESS_STATUS = false;
        private DateTime startTime = DateTime.Now;
        private DateTime endTime;
        public bool SetMethod(object argMessage)
        {
            InstallUnInstallParams param = argMessage as InstallUnInstallParams;
            string driverPath = param.ProdPath;
            string infFilePath = CommonExtensions.IdentifyDriverFile(driverPath);
            if (base.MachineInfo.Driver.Version == DisplayExtensions.GetDriverVesion(infFilePath).Trim().Split(',').Last() &&
                !base.AppManager.ListTestTypeAttribute.Contains(TestType.HasINFModify))
            {
                Log.Verbose("Same Driver already installed, returning from Driver installation");
                return true;
            }
            if (string.IsNullOrEmpty(driverPath))
                Log.Abort("Driver Path is empty");
            if (driverPath.EndsWith(@"\"))
                driverPath = driverPath.Remove(driverPath.Length - 1);
            setUpFilePath = Directory.GetFiles(driverPath, "Setup.exe").First();
            if (string.IsNullOrEmpty(setUpFilePath))
                Log.Abort("Unable to find setup.exe in {0}", driverPath);

            Log.Verbose("Driver Installation Steps Prep");
            this._elementSequence.Add(new ControlParams() { ControlType = ControlType.Button, AutomationID = "6", Name = "Yes" });
            this._elementSequence.Add(new ControlParams() { ControlType = ControlType.Button, AutomationID = "1001", Name = "Next >" });
            this._elementSequence.Add(new ControlParams() { ControlType = ControlType.Button, AutomationID = "1146", Name = "Yes" });
            this._elementSequence.Add(new ControlParams() { ControlType = ControlType.Button, AutomationID = "1001", Name = "Next >" });
            this._elementSequence.Add(new ControlParams() { ControlType = ControlType.CheckBox, AutomationID = "VerificationCheckBox", Name = string.Empty });
            this._elementSequence.Add(new ControlParams() { ControlType = ControlType.Button, AutomationID = "CommandButton_1", Name = "Install" });
            this._elementSequence.Add(new ControlParams() { ControlType = ControlType.Button, AutomationID = "CommandButton_1", Name = "Install" });
            this._elementSequence.Add(new ControlParams() { ControlType = ControlType.Button, AutomationID = "CommandLink_1", Name = string.Empty });
            this._elementSequence.Add(new ControlParams() { ControlType = ControlType.Button, AutomationID = "1001", Name = "Next >" });
            this._elementSequence.Add(new ControlParams() { ControlType = ControlType.RadioButton, AutomationID = "1128", Name = "No, I will restart this computer later." });
            this._elementSequence.Add(new ControlParams() { ControlType = ControlType.Button, AutomationID = "1064", Name = "Finish" });
            this._elementSequence.Add(new ControlParams() { ControlType = ControlType.Button, AutomationID = "CommandButton_2", Name = "Restart Later" });

            this._verify.Add(new VerifyOption() { name = "No, I will restart this computer later.", ID = "1128", status = false });
            this._verify.Add(new VerifyOption() { name = "Finish", ID = "1064", status = false });

            Log.Verbose("Running Setup.exe");
            CommonExtensions.StartProcess(setUpFilePath, null, 0, Path.GetDirectoryName(setUpFilePath));
            UIActivity();
            if (SUCCESS_STATUS)
            {
                Log.Message("Driver Installation task completed via UI!");
                return AccessUIExtensions.RebootHandler(base.CurrentMethodIndex, RebootReason.DriverModify);
            }
            Log.Alert(false, "Driver Installation incomplete via UI!");
            return false;
        }

        private void UIActivity()
        {
            AutomationElement rootElement = AutomationElement.RootElement;
            Condition regCondition = null;
            AutomationElement appElement = null;
            while (true)
            {
                Thread.Sleep(2000);
                endTime = DateTime.Now;
                TimeSpan diff = endTime.Subtract(startTime);
                if (diff.Days <= 0 && diff.Minutes >= 5)
                    break;
                foreach (ControlParams eachParam in _elementSequence)
                {
                    if (eachParam.Name != string.Empty)
                    {
                        regCondition = new AndCondition(new PropertyCondition(AutomationElement.AutomationIdProperty, eachParam.AutomationID),
                         (new PropertyCondition(AutomationElement.NameProperty, eachParam.Name)));
                    }
                    else
                        regCondition = new PropertyCondition(AutomationElement.AutomationIdProperty, eachParam.AutomationID);
                    if (!eachParam.ClickStatus)
                    {
                        appElement = rootElement.FindFirst(TreeScope.Descendants, regCondition);
                        if (appElement != null && ((bool)appElement.GetCurrentPropertyValue(AutomationElement.IsEnabledProperty, true)))
                        {
                            ClickElement(appElement);
                            break;
                        }
                    }
                }
                SUCCESS_STATUS = InstallStatus();
                if (SUCCESS_STATUS)
                    break;
            }
        }
        private void ClickElement(AutomationElement argElement)
        {
            if (null != argElement)
            {
                ControlParams param = _elementSequence.Find(F => F.AutomationID.Equals(argElement.Current.AutomationId));
                if (param != null)
                    param.ClickStatus = true;

                VerifyOption find = _verify.Find(F => F.name.Equals(argElement.Current.Name));
                if (find != null)
                {
                    if (find.ID.Equals(argElement.Current.AutomationId))
                        find.status = true;
                }
                if (argElement.Current.ControlType.Equals(ControlType.Button))
                {
                    Log.Verbose("Clicking {0} ", argElement.Current.Name);
                    InvokePattern pattern = argElement.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
                    pattern.Invoke();
                }
                else if (argElement.Current.ControlType.Equals(ControlType.RadioButton))
                {
                    Log.Verbose("Selecting {0} ", argElement.Current.Name);
                    SelectionItemPattern pattern = argElement.GetCurrentPattern(SelectionItemPattern.Pattern) as SelectionItemPattern;
                    pattern.Select();
                }
                else if (argElement.Current.ControlType.Equals(ControlType.CheckBox))
                {
                    Log.Verbose("Selecting {0} ", argElement.Current.Name);
                    TogglePattern pattern = argElement.GetCurrentPattern(TogglePattern.Pattern) as TogglePattern;
                    if (pattern.Current.ToggleState == ToggleState.Off)
                        pattern.Toggle();
                }
            }
        }
        private bool InstallStatus()
        {
            foreach (VerifyOption findOption in _verify)
            {
                if (!findOption.status)
                    return false;
            }
            return true;
        }
    }
}
