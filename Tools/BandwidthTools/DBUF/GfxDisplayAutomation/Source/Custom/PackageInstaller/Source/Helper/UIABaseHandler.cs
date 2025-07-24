using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Automation;
using System.Reflection;
using System.Threading;
using System.Windows;

namespace PackageInstaller
{
    public class UIABaseHandler
    {
        private static Condition condition = null;        
        public static AutomationElement selectChildElement(AutomationElement element, string childAutomationId)
        {
            condition = new PropertyCondition(AutomationElement.AutomationIdProperty, childAutomationId);
            return element.FindFirst(TreeScope.Descendants, condition);
        }

        public static AutomationElement selectChildElement(AutomationElement element, ControlType ct)
        {
            condition = new PropertyCondition(AutomationElement.ControlTypeProperty, ct);
            return element.FindFirst(TreeScope.Descendants, condition);
        }

        public static AutomationElement SelectElementNameControlType(string name, ControlType ct)
        {
            return SelectElementNameControlType(AutomationElement.RootElement, name, ct);
        }

        public static AutomationElement SelectElementNameControlType(AutomationElement parentelement, string name, ControlType ct)
        {
            condition = new AndCondition(
                       new PropertyCondition(AutomationElement.NameProperty, name, PropertyConditionFlags.IgnoreCase),
                       new PropertyCondition(AutomationElement.ControlTypeProperty, ct)
                       );
            //  Thread.Sleep(2000);
            return parentelement.FindFirst(TreeScope.Descendants, condition);
        }

        public static AutomationElement SelectElementClassNameControlType(AutomationElement parentelement, string ClassName, ControlType ct)
        {
            condition = new AndCondition(
                       new PropertyCondition(AutomationElement.ClassNameProperty, ClassName, PropertyConditionFlags.IgnoreCase),
                       new PropertyCondition(AutomationElement.ControlTypeProperty, ct)
                       );
            //   Thread.Sleep(2000);
            return parentelement.FindFirst(TreeScope.Descendants, condition);
        }

        public static AutomationElement SelectElementNameAutomationId(AutomationElement parentelement, string name, String automationId)
        {
            condition = new AndCondition(
                       new PropertyCondition(AutomationElement.NameProperty, name, PropertyConditionFlags.IgnoreCase),
                       new PropertyCondition(AutomationElement.AutomationIdProperty, automationId, PropertyConditionFlags.IgnoreCase)
                       );
            //  Thread.Sleep(2000);
            return parentelement.FindFirst(TreeScope.Descendants, condition);
        }

        public static AutomationElement SelectElementAutomationIdControlType(string automationId, ControlType ct)
        {
            return SelectElementAutomationIdControlType(AutomationElement.RootElement, automationId, ct);
        }
        public static AutomationElement SelectElementAutomationIdControlType(AutomationElement parentelement, string automationId, ControlType ct)
        {
            condition = new AndCondition(
                       new PropertyCondition(AutomationElement.AutomationIdProperty, automationId, PropertyConditionFlags.IgnoreCase),
                       new PropertyCondition(AutomationElement.ControlTypeProperty, ct)
                       );
            //  Thread.Sleep(2000);
            return parentelement.FindFirst(TreeScope.Descendants, condition);
        }

        public void SelectionItem(AutomationElement element)
        {
            if (element != null)
            {
                SelectionItemPattern pattern = element.GetCurrentPattern(SelectionItemPattern.Pattern) as SelectionItemPattern;
                pattern.Select();
            }
        }

        public bool SelectedItem(AutomationElement element)
        {
            if (element != null)
            {
                SelectionItemPattern pattern = element.GetCurrentPattern(SelectionItemPattern.Pattern) as SelectionItemPattern;
                return pattern.Current.IsSelected;
            }
            else return false;
        }

        public static ToggleState getToggleState(AutomationElement element)
        {
            TogglePattern pattern = element.GetCurrentPattern(TogglePattern.Pattern) as TogglePattern;
            return pattern.Current.ToggleState;
        }

        public static void Toggle(AutomationElement element)
        {
            TogglePattern pattern = element.GetCurrentPattern(TogglePattern.Pattern) as TogglePattern;
            pattern.Toggle();
        }

        public void Invoke(AutomationElement element)
        {
            DateTime startTime = DateTime.Now;
            DateTime add = startTime.AddSeconds(15);
            while (startTime.AddSeconds(15) > DateTime.Now)
            {
                if (element != null && element.Current.IsOffscreen == false && element.Current.IsEnabled == true)
                {
                    InvokePattern pattern = element.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
                    pattern.Invoke();
                    break;
                }
            }
        }
        public static void InvokeElement(AutomationElement element)
        {
            DateTime startTime = DateTime.Now;
            while (startTime.AddSeconds(15) > DateTime.Now)
            {
                if (element != null && element.Current.IsOffscreen == false && element.Current.IsEnabled == true)
                {
                    InvokePattern pattern = element.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
                    pattern.Invoke();
                    break;
                }
            }
        }
        public static void InvokeDriverElement(AutomationElement element)
        {
            if (element != null)
            {
                InvokePattern pattern = element.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
                pattern.Invoke();
            }
        }
        public static void Select(AutomationElement element)
        {
            DateTime startTime = DateTime.Now;
            while (startTime.AddSeconds(15) > DateTime.Now)
            {
                if (element != null && element.Current.IsOffscreen == false && element.Current.IsEnabled == true)
                {
                    element.SetFocus();
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    break;
                }
            }
        }
        public void SendKey(AutomationElement element)
        {
            DateTime startTime = DateTime.Now;
            while (startTime.AddSeconds(15) > DateTime.Now)
            {
                if (element != null && element.Current.IsOffscreen == false && element.Current.IsEnabled == true)
                {
                    element.SetFocus();
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    break;
                }
            }
        }

        public void ExpandCollapse(AutomationElement element)
        {
            DateTime startTime = DateTime.Now;
            while (startTime.AddSeconds(15) > DateTime.Now)
            {
                if (element != null && element.Current.IsOffscreen == false && element.Current.IsEnabled == true)
                {
                    ExpandCollapsePattern pattern = element.GetCurrentPattern(ExpandCollapsePattern.Pattern) as ExpandCollapsePattern;
                    if (pattern.Current.ExpandCollapseState == ExpandCollapseState.Collapsed)
                        pattern.Expand();
                    break;
                }
            }
        }

        public static string Value(AutomationElement element)
        {
            if (element != null)
            {
                ValuePattern pattern = element.GetCurrentPattern(ValuePattern.Pattern) as ValuePattern;
                return pattern.Current.Value;
            }
            return null;
        }

        public void Value(AutomationElement element, string value)
        {
            if (element != null)
            {
                ValuePattern pattern = element.GetCurrentPattern(ValuePattern.Pattern) as ValuePattern;
                pattern.SetValue(value);
            }
        }

        public static double getRangeValue(AutomationElement element)
        {
            RangeValuePattern pattern = element.GetCurrentPattern(RangeValuePattern.Pattern) as RangeValuePattern;
            return pattern.Current.Value;
        }

        public static void setRangeValue(AutomationElement element, double value)
        {
            RangeValuePattern pattern = element.GetCurrentPattern(RangeValuePattern.Pattern) as RangeValuePattern;
            pattern.SetValue(value);
        }

        public void TilesInvoke(AutomationElement element)
        {
            DateTime startTime = DateTime.Now;
            DateTime end = startTime.AddSeconds(15);
            while (end > DateTime.Now)
            {
                if (element != null && element.Current.IsOffscreen == false && element.Current.IsEnabled == true)
                {
                    Invoke(TreeWalker.ControlViewWalker.GetParent(element));
                    break;
                }
            }
        }
    }
}
