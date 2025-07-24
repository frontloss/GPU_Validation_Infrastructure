namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    using System.Threading;
    [Test(Type = TestType.HasPlugUnPlug)]
   public class SB_Config_Hotplug_Unplug_Basic : SB_Config_Base
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.ConfigTypeCount != base.CurrentConfig.DisplayList.Count())
                Log.Abort("This test requires atleast {0} displays , current display count: {1}", base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());

            if (!( base.CurrentConfig.DisplayList.Intersect(_availableDisplays.Keys.ToList()).ToList().Count > 0))
                Log.Abort("Hotplug unplug test requires atleast one pluggable display");

            base.CurrentConfig.DisplayList.ForEach(item =>
            {
                if (_availableDisplays.Keys.Contains(item))
                    _pluggableDisplays.Add(item);
            });
        }
        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                if (_pluggableDisplays.Contains(curDisp))
                    HotPlug(curDisp);
            });
            ApplyConfigOS(base.CurrentConfig);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            Log.Message(true, "Unplug pluggable displays");
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                if (_pluggableDisplays.Contains(curDisp))
                    HotUnPlug(curDisp);
            });
            DisplayConfig curConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            Log.Message(true, "The configuration after unplug {0}", curConfig.GetCurrentConfigStr());
        }
        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep3()
        {
            Log.Message(true, "Hotplug pluggable displays");
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                if (_pluggableDisplays.Contains(curDisp))
                    HotPlug(curDisp);
            });
            VerifyConfigOS(base.CurrentConfig);
        }

        [Test(Type = TestType.Method, Order = 4)]
        public virtual void TestStep4()
        {
            CleanUpHotplugFramework();
        }
    }
}