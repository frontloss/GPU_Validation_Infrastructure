namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_Config_Hotplug_Unplug_Semiautomated : SB_Config_Hotplug_Unplug_Basic
    {
        protected Dictionary<DisplayType, System.Action> _unplugDisplay = null;
        protected string _semiAutomatedDisplay;
        public SB_Config_Hotplug_Unplug_Semiautomated()
        {
            _unplugDisplay = new Dictionary<DisplayType, System.Action>();
            _unplugDisplay.Add(DisplayType.CRT, UnplugSemiautomated);
            _unplugDisplay.Add(DisplayType.DP, UnplugSemiautomated);
            _unplugDisplay.Add(DisplayType.DP_2, UnplugSemiautomated);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public override void TestStep2()
        {
            PerformSemiAutomated("Unplug");
            base.TestStep2();
        }
        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            PerformSemiAutomated("Plug");
            List<DisplayInfo> enumeratedDisplay = AccessInterface.GetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);
            base.CurrentConfig.EnumeratedDisplays.Clear();
            base.CurrentConfig.EnumeratedDisplays.AddRange(enumeratedDisplay);
            base.TestStep3();
        }
        private void PerformSemiAutomated(string argMessage)
        {
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                if (_unplugDisplay.ContainsKey(curDisp))
                {
                    _semiAutomatedDisplay = argMessage + " " + curDisp;
                    _unplugDisplay[curDisp]();
                }
            });
        }
        protected void UnplugSemiautomated()
        {
            Log.Message(true, "{0} semi automated", _semiAutomatedDisplay);
            AccessInterface.SetFeature<bool, string>(Features.PromptMessage, Action.SetMethod, _semiAutomatedDisplay);
        }
    }
}
