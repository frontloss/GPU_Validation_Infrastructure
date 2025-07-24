namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    [Test(Type = TestType.HasPlugUnPlug)]
    public class SB_modes_Hotplug_Unplug_Basic : SB_MODES_Base
    {
        protected List<DisplayType> _pluggableDisplay = null;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.ConfigTypeCount > base.CurrentConfig.DisplayList.Count())
                Log.Abort("{0} requires atleast {1} Displays to be enumerated, current Display count: {2}", base.CurrentConfig.ConfigType, base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
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
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
            {
                Log.Success("{0} Applied successfully", base.CurrentConfig.GetCurrentConfigStr());
                base.CurrentConfig.CustomDisplayList.ForEach(eachDisp => CheckWatermark(eachDisp));
            }
            else
                Log.Fail("Failed to Apply {0}", base.CurrentConfig.GetCurrentConfigStr());
        }
        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            List<DisplayModeList> ModeList = base.GetMinModeForConfig(base.CurrentConfig.DisplayList, base.CurrentConfig.ConfigType.GetUnifiedConfig());
            ApplyMode(ModeList);
            PerformHotplugUnplug();
            VerifyMode(ModeList);

            ModeList = base.GetMaxModeForConfig(base.CurrentConfig.DisplayList, base.CurrentConfig.ConfigType.GetUnifiedConfig());
            ApplyMode(ModeList);
            PerformHotplugUnplug();
            VerifyMode(ModeList);
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
        protected virtual void PerformHotplugUnplug()
        {
            Log.Message(true, "Performing Hotplug Unplug and plug");
            base.CurrentConfig.DisplayList.Intersect(_pluggableDisplay).ToList().ForEach(curDisp =>
            {
                HotUnPlug(curDisp);
                DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
                currentConfig.CustomDisplayList.ForEach(eachDisplay => CheckWatermark(eachDisplay));
            });
            base.CurrentConfig.DisplayList.Intersect(_pluggableDisplay).ToList().ForEach(curDisp =>
            {
                HotPlug(curDisp, _defaultEDIDMap[curDisp]);
            });
        }

        protected virtual void ApplyMode(List<DisplayModeList> argDispModeList)
        {
            argDispModeList.ForEach(curDisp =>
            {
                curDisp.supportedModes.ForEach(curMode =>
                {
                    base.ApplyModeOS(curMode, curMode.display);
                });
            });
        }
        protected virtual void VerifyMode(List<DisplayModeList> argDispModeList)
        {
            argDispModeList.ForEach(curDisp =>
            {
                curDisp.supportedModes.ForEach(curMode =>
                {
                    base.VerifyModeOS(curMode, curMode.display);
                });
            });
        }
    }

}

