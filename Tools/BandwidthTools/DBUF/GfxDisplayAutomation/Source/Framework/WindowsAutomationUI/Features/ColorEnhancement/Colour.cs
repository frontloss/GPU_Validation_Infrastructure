namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;
    using System.Windows.Automation;

    public class Colour :FunctionalBase, ISet, IGet
    {
        private List<AutomationElement> _colorsList = null;
        UIABaseHandler uiaBaseHandler = new UIABaseHandler();
        public Colour()
        {
            Log.Verbose("In color enhancement (Windows Automation UI)");
            if (null == this._colorsList)
            {
                this._colorsList = new List<AutomationElement>();
                this._colorsList.Add(UIABaseHandler.SelectElementAutomationIdControlType("imgAllColors", ControlType.Image));
                this._colorsList.Add(UIABaseHandler.SelectElementAutomationIdControlType("imgRed", ControlType.Image));
                this._colorsList.Add(UIABaseHandler.SelectElementAutomationIdControlType("imgGreen", ControlType.Image));
                this._colorsList.Add(UIABaseHandler.SelectElementAutomationIdControlType("imgBlue", ControlType.Image));
            }
        }
     
        public object Get
        {
            get { return Enum.Parse(typeof(ColorOptions),UIABaseHandler.SelectElementAutomationIdControlType("lblRGB", ControlType.Text).Current.Name.Replace("Colors", string.Empty).Trim()); }
        }
        public object Set
        {
            set
            {
                uiaBaseHandler.SendKey(this._colorsList[(int)Enum.Parse(typeof(ColorOptions), value.ToString())]);
            }
        }
    }
}
