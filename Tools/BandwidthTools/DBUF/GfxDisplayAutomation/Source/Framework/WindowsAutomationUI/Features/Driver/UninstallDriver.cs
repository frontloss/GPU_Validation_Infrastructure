namespace Intel.VPG.Display.Automation
{
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.Windows.Automation;
    using System.Collections.Generic;

    internal class UninstallDriver : FunctionalBase, ISetNoArgs
    {
        private List<ControlParams> _elementSequence = new List<ControlParams>();

        public bool SetNoArgs()
        {
            if (Directory.Exists(base.AppSettings.ProdDriverPath))
            {
                string[] driverBaselineFiles = Directory.GetFiles(base.AppSettings.ProdDriverPath);
                if (Path.GetFileNameWithoutExtension(driverBaselineFiles.First()).StartsWith("1"))
                    File.Delete(driverBaselineFiles.First());
            }
            Log.Verbose("Driver UnInstallation Steps Prep");
            this._elementSequence.Add(new ControlParams() { ControlType = ControlType.TreeItem, Delay = 2, Name = "display adapters" });
            this._elementSequence.Add(new ControlParams() { ControlType = ControlType.TreeItem, Delay = 2, Name = base.MachineInfo.Driver.Name.ToLower() });
            this._elementSequence.Add(new ControlParams() { ControlType = ControlType.Button, Delay = 2, Name = "uninstall", AutomationID = "item 23" });
            this._elementSequence.Add(new ControlParams() { ControlType = ControlType.CheckBox, Delay = 2, Name = "delete the driver software", AutomationID = "118", Class = "button" });
            this._elementSequence.Add(new ControlParams() { ControlType = ControlType.Button, Delay = 2, Name = "ok", AutomationID = "1", Class = "button" });
            this._elementSequence.Add(new ControlParams() { ControlType = ControlType.Button, Delay = 60, Name = "no", AutomationID = "commandbutton_7", Class = "ccpushbutton" });

            Log.Verbose("Launching Device Manager");
            Process.Start("devmgmt.msc");


            Log.Verbose("Driver UnInstallation Start");
            if (Next(0))
            {
                Log.Message("Driver UnInstallation task completed via UI!");
                //File.WriteAllText(CommonExtensions.UninstallFile, "Uninstall Complete");
                return AccessUIExtensions.RebootHandler(base.CurrentMethodIndex, RebootReason.DriverModify);
            }
            Log.Alert(false, "Driver UnInstallation incomplete via UI!");
            return false;
        }

        private bool Next(int argElementIndex)
        {
            if (argElementIndex == _elementSequence.Count)
                return true;

            uint timer = 0;
            AutomationElement rootElement = AutomationElement.RootElement;
            Condition regCondition = null;
            AutomationElementCollection appElementColn = null;
            AutomationElement appElement = null;
            ControlParams param = null;

            while (timer < 2)
            {
                param = _elementSequence[argElementIndex];
                Thread.Sleep(param.Delay * 1000);
                regCondition = new PropertyCondition(AutomationElement.ControlTypeProperty, param.ControlType);
                appElementColn = rootElement.FindAll(TreeScope.Descendants, regCondition);
                foreach (AutomationElement element in appElementColn)
                {
                    if (element.Current.Name.ToLower().Contains(param.Name) && element.Current.AutomationId.ToLower().Equals(param.AutomationID) && element.Current.ClassName.ToLower().Equals(param.Class))
                    {
                        appElement = element;
                        break;
                    }
                }

                if (appElement != null && ((bool)appElement.GetCurrentPropertyValue(AutomationElement.IsEnabledProperty, true)))
                    break;
                Log.Verbose("Waiting to find {0}", param.Name);
                timer++;
            }

            if (appElement == null)
                Log.Alert("Element {0} not found!", param.Name);
            else
                ClickElement(appElement);

            return Next(++argElementIndex);
        }
        private void ClickElement(AutomationElement argElement)
        {
            if (null != argElement)
            {
                if (argElement.Current.ControlType.Equals(ControlType.TreeItem))
                {
                    Log.Verbose("Selecting {0} ", argElement.Current.Name);
                    ExpandCollapsePattern ecPattern = argElement.GetCurrentPattern(ExpandCollapsePattern.Pattern) as ExpandCollapsePattern;
                    if (ecPattern.Current.ExpandCollapseState == ExpandCollapseState.Collapsed)
                        ecPattern.Expand();
                    else if (ecPattern.Current.ExpandCollapseState == ExpandCollapseState.LeafNode)
                    {
                        SelectionItemPattern siPattern = argElement.GetCurrentPattern(SelectionItemPattern.Pattern) as SelectionItemPattern;
                        siPattern.Select();
                    }
                }
                else if (argElement.Current.ControlType.Equals(ControlType.Button))
                {
                    Log.Verbose("Clicking {0} ", argElement.Current.Name);
                    InvokePattern pattern = argElement.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
                    pattern.Invoke();
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
    }
}
