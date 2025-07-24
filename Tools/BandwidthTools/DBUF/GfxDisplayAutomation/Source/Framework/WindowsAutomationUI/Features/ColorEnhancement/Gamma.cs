namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Threading;
    using System.Windows.Automation;

    public class Gamma :FunctionalBase,  ISet, IGet
    {
        private AutomationElement element, sliderelement = null;
        int reTry = 0;
        public Gamma()
        {
            Log.Verbose("In Gamma (Windows Automation UI)");
            Thread.Sleep(200);
            while (element == null && reTry < 3)
            {
                element = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.Gamma].AutomationId, ControlType.Custom);
                if (element == null) Log.Verbose("Failed to fetch the Feature,{0} at {1} attempt, Trying again", Features.Gamma.ToString(), ++reTry);
                System.Threading.Thread.Sleep(1000);
            }
            if (element == null)
                sliderelement = UIABaseHandler.SelectElementAutomationIdControlType(UIExtensions.FeaturesDictionary[Features.Gamma].AutomationId, ControlType.Slider);
            else
                sliderelement = UIABaseHandler.selectChildElement(element, "sliderName");
        }
        public object Get
        {
            get
            {
                return Math.Round(UIABaseHandler.getRangeValue(sliderelement), 2);
            }
        }
        public object Set
        {
            set
            {
                UIABaseHandler.setRangeValue(sliderelement, double.Parse(value.ToString()));
            }
        }
    }
}
