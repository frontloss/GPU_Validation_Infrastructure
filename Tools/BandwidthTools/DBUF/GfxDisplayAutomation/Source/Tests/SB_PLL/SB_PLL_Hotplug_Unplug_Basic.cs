using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_PLL_Hotplug_Unplug_Basic : SB_PLL_Base_Chv
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.PluggableDisplayList.Count == 0)
                Log.Abort("Test needs atleast 1 pluggable Display");
        }
        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            base.CurrentConfig.PluggableDisplayList.ForEach(curDisp =>
            {
                HotPlug(curDisp);
            });
            base.ApplyConfig(base.CurrentConfig);
            base.VerifyPLLRegister(base.CurrentConfig);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            base.CurrentConfig.PluggableDisplayList.ForEach(curDisp =>
            {
                HotUnPlug(curDisp);
            });
            base.CurrentConfig.PluggableDisplayList.ForEach(curDisp =>
            {
                HotPlug(curDisp);
            });
        }
        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep3()
        {
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            if (currentConfig.GetCurrentConfigStr().Equals(base.CurrentConfig.GetCurrentConfigStr()))
            {
                Log.Success("Config {0} retained after plug unplug", currentConfig.GetCurrentConfigStr());
                VerifyPLLRegister(currentConfig);
            }
            else
                Log.Fail("Config {0} has switched to {1} after unplug and plug", base.CurrentConfig.GetCurrentConfigStr(), currentConfig.GetCurrentConfigStr());
        }

       //protected Dictionary<DisplayType, DVMU_PORT> _pluggableDisplay = new Dictionary<DisplayType, DVMU_PORT>() { { DisplayType.HDMI, DVMU_PORT.PORTA }, { DisplayType.HDMI_2, DVMU_PORT.PORTB } };

       // [Test(Type = TestType.PreCondition, Order = 0)]
       // public virtual void TestStep0()
       // {
       //     if (base.CurrentConfig.DisplayList.Intersect(_pluggableDisplay.Keys.ToList()).ToList().Count == 0)
       //         Log.Abort("Test needs atleast 1 pluggable Display");
       // }
       // [Test(Type = TestType.Method, Order = 1)]
       // public virtual void TestStep1()
       // {
       //     Hotplug(FunctionName.OPEN, DisplayType.HDMI, DVMU_PORT.PORTA);
       //     _pluggableDisplay.Keys.ToList().Intersect(base.CurrentConfig.DisplayList).ToList().ForEach(curDisp =>
       //         {
       //             Hotplug(FunctionName.PLUG, curDisp, _pluggableDisplay[curDisp]);
       //         });
       //     base.ApplyConfig(base.CurrentConfig);
       //     base.VerifyPLLRegister(base.CurrentConfig);
       // }
       // [Test(Type = TestType.Method, Order = 2)]
       // public virtual void TestStep2()
       // {
       //     _pluggableDisplay.Keys.ToList().Intersect(base.CurrentConfig.DisplayList).ToList().ForEach(curDisp =>
       //     {
       //         Hotplug(FunctionName.UNPLUG, curDisp, _pluggableDisplay[curDisp]);
       //     });
       //     _pluggableDisplay.Keys.ToList().Intersect(base.CurrentConfig.DisplayList).ToList().ForEach(curDisp =>
       //     {
       //         Hotplug(FunctionName.PLUG, curDisp, _pluggableDisplay[curDisp]);
       //     });
       // }
       // [Test(Type = TestType.Method, Order = 3)]
       // public virtual void TestStep3()
       // {
       //     DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
       //     if (currentConfig.GetCurrentConfigStr().Equals(base.CurrentConfig.GetCurrentConfigStr()))
       //     {
       //         Log.Success("Config {0} retained after plug unplug", currentConfig.GetCurrentConfigStr());
       //         VerifyPLLRegister(currentConfig);
       //     }
       //     else
       //         Log.Fail("Config {0} has switched to {1} after unplug and plug", base.CurrentConfig.GetCurrentConfigStr(), currentConfig.GetCurrentConfigStr());
       // }
       // protected virtual void Hotplug(FunctionName FuncArg, DisplayType DisTypeArg, DVMU_PORT PortArg)
       // {
       //     HotPlugUnplug obj = new HotPlugUnplug(FuncArg, DisTypeArg, PortArg);
       //     // obj.EdidFilePath = "DELL_XvYcc_U2410.EDID";
       //     bool status = AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, obj);
       // }
    }
}
