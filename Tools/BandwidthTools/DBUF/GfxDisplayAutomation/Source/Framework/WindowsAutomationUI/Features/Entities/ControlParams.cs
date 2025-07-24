namespace Intel.VPG.Display.Automation
{
    using System.Windows.Automation;

    internal class ControlParams
    {
        private string _name = string.Empty;
        private string _class = string.Empty;
        private int _delay = 0;
        private ControlType _controlType;
        private string _automationID = string.Empty;
        private bool _clickStatus = false;
        internal bool ClickStatus
        {
            get { return _clickStatus; }
            set { _clickStatus = value; }
        }

        internal string Name
        {
            get { return _name; }
            set { _name = value; }
        }
        internal string Class
        {
            get { return _class; }
            set { _class = value; }
        }
        internal int Delay
        {
            get { return _delay; }
            set { _delay = value; }
        }
        internal ControlType ControlType
        {
            get { return _controlType; }
            set { _controlType = value; }
        }
        internal string AutomationID
        {
            get { return _automationID; }
            set { _automationID = value; }
        }
    }
}