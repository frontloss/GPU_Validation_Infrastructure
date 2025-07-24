using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using System.IO;
using Microsoft.Win32;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    public class SB_Config_Tri_Swap_Switch : SB_Config_Base
    {     
        protected Dictionary<DisplayType, string> _displayPersistance = new Dictionary<DisplayType, string>();
        protected List<DisplayConfig> _dispSwitchOrder = null;       
        DisplayConfig triConfig = null;
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.DisplayList.Count() != 3)
                Log.Abort("This test requires atleast 3 displays , current display count: {0}",base.CurrentConfig.DisplayList.Count());
            if ((base.CurrentConfig.ConfigType != DisplayConfigType.TDC && base.CurrentConfig.ConfigType != DisplayConfigType.TED))
                Log.Abort("Test supports only TDC or TED ,Current config {0}", base.CurrentConfig.ConfigType.ToString());          
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.CurrentConfig.PluggableDisplayList.ForEach(curDisp =>
            {
                base.HotPlug(curDisp, _availableDisplays[curDisp]);
                _pluggableDisplays.Add(curDisp);
                if (curDisp == base.CurrentConfig.SecondaryDisplay)
                {
                    DisplayConfig ddcConfig = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
                    ApplyConfigOS(ddcConfig);
                    ddcConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
                    _displayPersistance.Add(base.CurrentConfig.TertiaryDisplay, ddcConfig.GetCurrentConfigStr());
                }
                if (curDisp == base.CurrentConfig.TertiaryDisplay && _pluggableDisplays.Count == 2)
                {
                    if (_pluggableDisplays.Contains(base.CurrentConfig.PrimaryDisplay))
                    {
                        base.HotUnPlug(base.CurrentConfig.PrimaryDisplay);
                        DisplayConfig ddcConfig = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay };
                        ApplyConfigOS(ddcConfig);
                        ddcConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
                        _displayPersistance.Add(base.CurrentConfig.PrimaryDisplay, ddcConfig.GetCurrentConfigStr());
                        base.HotPlug(base.CurrentConfig.PrimaryDisplay, _availableDisplays[base.CurrentConfig.PrimaryDisplay]);
                    }
                    else if (_pluggableDisplays.Contains(base.CurrentConfig.SecondaryDisplay))
                    {
                        base.HotUnPlug(base.CurrentConfig.SecondaryDisplay);
                        DisplayConfig ddcConfig = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay };
                        ApplyConfigOS(ddcConfig);
                        ddcConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
                        _displayPersistance.Add(base.CurrentConfig.SecondaryDisplay, ddcConfig.GetCurrentConfigStr());
                        base.HotPlug(base.CurrentConfig.SecondaryDisplay, _availableDisplays[base.CurrentConfig.SecondaryDisplay]);
                    }
                }
            });
            ApplyConfigOS(base.CurrentConfig);
            triConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Unplug display and plug display");
            base.CurrentConfig.PluggableDisplayList.ForEach(curDisp =>
            {
                DisplayInfo displayInfo = base.EnumeratedDisplays.Where(item => item.DisplayType == curDisp).FirstOrDefault();
                base.HotUnPlug(curDisp);

                DisplayConfig curConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
                Log.Message(true, "The configuration after unplug {0}", curConfig.GetCurrentConfigStr());
                if (curConfig.GetCurrentConfigStr().Equals(_displayPersistance[curDisp], StringComparison.OrdinalIgnoreCase))
                {
                    Log.Message(true, "Config is matching after Unplug");
                    VerifyConfigOS(curConfig);
                }
                else
                    Log.Fail(true, "Config is not matching after Unplug");

                base.HotPlug(curDisp, _availableDisplays[curDisp]);

                curConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
                Log.Message(true, "The configuration after plug {0}", curConfig.GetCurrentConfigStr());
                if (curConfig.GetCurrentConfigStr().Equals(triConfig.GetCurrentConfigStr(), StringComparison.OrdinalIgnoreCase))
                {
                    Log.Message(true, "Config is matching after Plug");
                    VerifyConfigOS(curConfig);
                }
                else
                    Log.Fail(true, "Config is not matching after Plug");
            });            
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            this.DisplaySwitch_3pipe();
            _dispSwitchOrder.ForEach(curConfig =>
            {
                ApplyConfigOS(curConfig);
                VerifyConfigOS(curConfig);
            });
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Test clean up- Unplug all displays");
            base.UnPlugDisplays();
        }
        public virtual void DisplaySwitch_3pipe()
        {
            DisplayConfig dispSwitch1 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay, TertiaryDisplay = base.CurrentConfig.PrimaryDisplay };
            DisplayConfig dispSwitch2 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig dispSwitch3 = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig dispSwitch4 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig dispSwitch5 = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay };
            DisplayConfig dispSwitch6 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay, TertiaryDisplay = base.CurrentConfig.PrimaryDisplay };
            DisplayConfig dispSwitch7 = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay };
            DisplayConfig dispSwitch8 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay, TertiaryDisplay = base.CurrentConfig.PrimaryDisplay };
            DisplayConfig dispSwitch9 = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig dispSwitch10 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
            DisplayConfig dispSwitch11 = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay };
            DisplayConfig dispSwitch12 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
            DisplayConfig dispSwitch13 = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay };
            DisplayConfig dispSwitch14 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig dispSwitch15 = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay };
            DisplayConfig dispSwitch16 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig dispSwitch17 = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig dispSwitch18 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig dispSwitch19 = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay };
            _dispSwitchOrder = new List<DisplayConfig>() {dispSwitch1, dispSwitch2, dispSwitch3, dispSwitch4, dispSwitch5,
                                                             dispSwitch6,dispSwitch7,dispSwitch8,dispSwitch9,dispSwitch10,
                                                             dispSwitch11,dispSwitch12,dispSwitch13,dispSwitch14,dispSwitch15,
                                                             dispSwitch16,dispSwitch17,dispSwitch18,dispSwitch19};
        }
    }
}
