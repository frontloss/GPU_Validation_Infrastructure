namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading;
    using System.Windows.Automation;
    class WiDiAPPInstaller
    {
        List<string> InstallSequence;
        bool done;
        Condition condition;
        AutomationElement clickEvent;
        AutomationElement _rootElement;
        public WiDiAPPInstaller()
        {
            InstallSequence = new List<string>();
            InstallSequence.Add("I accept the terms in the license agreement");
            InstallSequence.Add("Next >");
            InstallSequence.Add("Finish");
            done = false;
            condition = null;
            clickEvent = null;
            _rootElement = AutomationElement.RootElement;
        }

        public bool Install()
        {
            condition = new PropertyCondition(AutomationElement.NameProperty, "Intel(R) WiDi");
            clickEvent = _rootElement.FindFirst(TreeScope.Descendants, condition);
            if (clickEvent != null)
            {
                #region check if WiDi App already install in the test system");
                condition = new PropertyCondition(AutomationElement.NameProperty, "This Product is already Installed on this system.");
                clickEvent = _rootElement.FindFirst(TreeScope.Descendants, condition);
                if (clickEvent != null)
                {
                    Log.Verbose("This Product is already Installed on this system.");
                    condition = new PropertyCondition(AutomationElement.NameProperty, "OK");
                    clickEvent = _rootElement.FindFirst(TreeScope.Descendants, condition);
                    ClickElement(clickEvent);
                    Thread.Sleep(3000);
                    condition = new PropertyCondition(AutomationElement.NameProperty, "Finish");
                    clickEvent = _rootElement.FindFirst(TreeScope.Descendants, condition);
                    ClickElement(clickEvent);
                    done = true;
                }
                #endregion

                #region Check for Update
                condition = new PropertyCondition(AutomationElement.NameProperty, "Upgrade >");
                clickEvent = _rootElement.FindFirst(TreeScope.Descendants, condition);
                if (null != clickEvent)
                {
                    Log.Verbose("Updating WiDi App");
                    ClickElement(clickEvent);
                    SequenceAction();
                    done = true;
                }
                #endregion

                #region fresh Installation
                condition = new PropertyCondition(AutomationElement.NameProperty, "Next >");
                clickEvent = _rootElement.FindFirst(TreeScope.Descendants, condition);
                if (null != clickEvent)
                {
                    Log.Verbose("Installing WiDi Application");
                    ClickElement(clickEvent);
                    SequenceAction();
                    done = true;
                }
                #endregion

            }
            return done;
        }

        private void SequenceAction()
        {
            foreach (string item in InstallSequence)
            {
                condition = new PropertyCondition(AutomationElement.NameProperty, item);
                clickEvent = _rootElement.FindFirst(TreeScope.Descendants, condition);
                ClickElement(clickEvent);
                if (item.Contains("Next"))
                    Thread.Sleep((100) * 1000);
            }
        }

        private void ClickElement(AutomationElement element)
        {
            if (null != element)
            {
                if (element.Current.ControlType.Equals(ControlType.Button))
                {
                    InvokePattern pat = element.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
                    pat.Invoke();
                }
                else if (element.Current.ControlType.Equals(ControlType.RadioButton))
                {
                    SelectionItemPattern pat = element.GetCurrentPattern(SelectionItemPattern.Pattern) as SelectionItemPattern;
                    pat.Select();
                }
                Thread.Sleep(1500);
            }
        }
        public bool LicenseAgrement()
        {
            condition = new PropertyCondition(AutomationElement.NameProperty, "Intel® WiDi");
            AutomationElement Element = _rootElement.FindFirst(TreeScope.Descendants, condition);
            if (Element != null)
            {
                condition = new PropertyCondition(AutomationElement.AutomationIdProperty, "EulaAgreeButton");
                clickEvent = _rootElement.FindFirst(TreeScope.Descendants, condition);
                if (clickEvent != null)
                {
                    Log.Verbose("Accepting License Agrement");
                    ClickElement(clickEvent);
                    Thread.Sleep(40000);
                }
                return true;
            }
            return false;
        }
    }
}
