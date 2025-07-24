namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Windows.Automation;
    using System.Threading;


    public class ConfirmationPopup : FunctionalBase, ISet
    {
        UIABaseHandler uiaBaseHandler = new UIABaseHandler();
        private Dictionary<DecisionActions, AutomationElement> _buttonList = new Dictionary<DecisionActions, AutomationElement>();

        public ConfirmationPopup()
        {
            Log.Verbose("In Confirmation Pop Up (Windows Automation UI)");
            this._buttonList.Add(DecisionActions.No, UIABaseHandler.SelectElementNameControlType("No", ControlType.Button));
            this._buttonList.Add(DecisionActions.Yes, UIABaseHandler.SelectElementNameControlType("Yes", ControlType.Button));
        }
        public object Set
        {
            set
            {
                if (this._buttonList[(DecisionActions)value] == null)
                {
                    Log.Message("Clicking enter as automation element is null");
                    Thread.Sleep(2000);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    Thread.Sleep(6000);
                }
                else
                {
                    UIABaseHandler.InvokeElement(this._buttonList[(DecisionActions)value]);
                    Thread.Sleep(6000);
                }
            }
        }
    }
}
