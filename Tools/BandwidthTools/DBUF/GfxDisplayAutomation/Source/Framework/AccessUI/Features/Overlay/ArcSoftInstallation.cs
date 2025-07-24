namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Threading;
    using System.Windows.Automation;
    using System.Collections.Generic;

    internal class ArcSoftInstallation : FunctionalBase
    {
        private List<ControlParams> _elementSequence = new List<ControlParams>()
        {
            new ControlParams() { Class = "Button", Delay = 1, Name = "next" },
            new ControlParams() { Class = "Button", Delay = 2, Name = "yes" },
            new ControlParams() { Class = "Edit", Delay = 2, Name = "license key" },
            new ControlParams() { Class = "Button", Delay = 1, Name = "next" },
            new ControlParams() { Class = "Button", Delay = 2, Name = "next" },
            new ControlParams() { Class = "Button", Delay = 2, Name = "next" },
            new ControlParams() { Class = "Button", Delay = 60, Name = "restart my computer later" },
            new ControlParams() { Class = "Button", Delay = 1, Name = "finish" }
        };

        internal void StartInstallation()
        {
            Log.Verbose("ArcSoft Installation Start");
            string installerPath = base.AppSettings.OverlayPlayersPath;
            if (installerPath.EndsWith(@"\"))
                installerPath = installerPath.Remove(installerPath.Length - 1);

            if (string.IsNullOrEmpty(installerPath))
                Log.Abort("ArcSoft installation path is missing!");

            Log.Verbose("ArcSoft installation path : {0}", installerPath);
            CommonExtensions.StartProcess(string.Format(@"{0}\TotalMediaTheatre_5.1.1.110_Platinum.exe", installerPath), string.Empty, 0);
            Thread.Sleep(15 * 1000);

            if (Next(0))
            {
                Log.Success("ArcSoft Installation succeeded!");
                //AccessUIExtensions.RebootHandler(base.CurrentMethodIndex);
            }
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

            while (timer < 48)
            {
                param = _elementSequence[argElementIndex];
                Thread.Sleep(param.Delay * 1000);
                regCondition = new PropertyCondition(AutomationElement.ClassNameProperty, param.Class);
                appElementColn = rootElement.FindAll(TreeScope.Descendants, regCondition);
                foreach (AutomationElement element in appElementColn)
                {
                    if (element.Current.Name.ToLower().Contains(param.Name))
                    {
                        appElement = element;
                        break;
                    }
                }

                if (appElement != null && ((bool)appElement.GetCurrentPropertyValue(AutomationElement.IsEnabledProperty, true)))
                    break;
                timer++;
            }

            if (appElement == null)
                Log.Abort("Element {0} not found!", _elementSequence.ElementAt(argElementIndex));

            ClickElement(appElement);
            return Next(++argElementIndex);
        }
        private void ClickElement(AutomationElement argElement)
        {
            if (null != argElement)
            {
                if (argElement.Current.ControlType.Equals(ControlType.RadioButton))
                {
                    Log.Verbose("Selecting {0} ", argElement.Current.Name);
                    SelectionItemPattern pattern = argElement.GetCurrentPattern(SelectionItemPattern.Pattern) as SelectionItemPattern;
                    pattern.Select();
                }
                else if (argElement.Current.ControlType.Equals(ControlType.Button))
                {
                    Log.Verbose("Clicking {0} ", argElement.Current.Name);
                    InvokePattern pattern = argElement.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
                    pattern.Invoke();
                }
                else if (argElement.Current.ControlType.Equals(ControlType.Edit))
                {
                    Log.Verbose("Entering serial number {0}", base.AppSettings.ARCSoftSerialKey);
                    ValuePattern pattern = argElement.GetCurrentPattern(ValuePattern.Pattern) as ValuePattern;
                    pattern.SetValue(base.AppSettings.ARCSoftSerialKey);
                }
            }
        }
    }
}
