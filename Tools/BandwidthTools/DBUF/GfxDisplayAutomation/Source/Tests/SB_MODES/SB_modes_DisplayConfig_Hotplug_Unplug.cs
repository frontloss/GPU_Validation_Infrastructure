namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_modes_DisplayConfig_Hotplug_Unplug : SB_Modes_DisplayConfig_Basic
    {
        protected List<DisplayType> _pluggableDisplay = null;
        [Test(Type = TestType.Method, Order = 1)]
        public override void TestStep1()
        {
            _pluggableDisplay = new List<DisplayType>();
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                if (base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).Select(dI => dI.DisplayType).FirstOrDefault() == DisplayType.None)
                {
                    HotPlug(curDisp, _defaultEDIDMap[curDisp]);
                    _pluggableDisplay.Add(curDisp);
                }
            });
            if (_pluggableDisplay.Count() == 0)
                Log.Abort("This test requires atleast one pluggable display");
            base.TestStep1();
        }
        [Test(Type = TestType.Method, Order = 2)]
        public override void TestStep2()
        {
            _displayConfigSwitchOrder.ForEach(curConfig =>
            {
                _currentConfig = curConfig;
                ApplyConfigCUI(curConfig);
                if (_pluggableDisplay.Contains(curConfig.PrimaryDisplay) || _pluggableDisplay.Contains(curConfig.SecondaryDisplay) || _pluggableDisplay.Contains(curConfig.TertiaryDisplay))
                {
                    PerformHotplugUnplug(curConfig);
                }
                _veriftConfigSwitch[_currentConfig.ConfigType.GetUnifiedConfig()]();
            });
        }
        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep3()
        {
            Log.Message(true, "Test clean up- Unplug all displays");
            base.CurrentConfig.DisplayList.Intersect(_pluggableDisplay).ToList().ForEach(curDisp =>
            {
                HotUnPlug(curDisp);
            });
        }
        protected virtual void PerformHotplugUnplug(DisplayConfig argDispConfig)
        {
            Log.Message(true, "Performing Hotplug and Unplug ");

            base.CurrentConfig.DisplayList.Intersect(_pluggableDisplay).ToList().ForEach(curDisp =>
            {
                HotUnPlug(curDisp);
            });
            base.CurrentConfig.DisplayList.Intersect(_pluggableDisplay).ToList().ForEach(curDisp =>
            {
                HotPlug(curDisp, _defaultEDIDMap[curDisp]);
            });
        }
    }
}
