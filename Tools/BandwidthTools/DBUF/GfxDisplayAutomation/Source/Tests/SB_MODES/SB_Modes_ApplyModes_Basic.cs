namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    using System.Text.RegularExpressions;
    public class SB_Modes_ApplyModes_Basic : SB_MODES_Base
    {
        protected List<DisplayModeList> _modesList = null;
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.ConfigTypeCount > base.CurrentConfig.DisplayList.Count())
                Log.Abort("{0} requires atleast {1} Displays to be enumerated, current Display count: {2}", base.CurrentConfig.ConfigType, base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
            {
                Log.Success("{0} Applied successfully", base.CurrentConfig.GetCurrentConfigStr());

                base.CurrentConfig.DisplayList.ForEach(disp => CheckWatermark(disp));//watermark
            }
            else
                Log.Fail("Failed to Apply {0}", base.CurrentConfig.GetCurrentConfigStr());
        }
        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            List<DisplayModeList> modesListMin = base.GetMinModeForConfig(base.CurrentConfig.CustomDisplayList, base.CurrentConfig.ConfigType.GetUnifiedConfig());
            ApplyMode(modesListMin);
            VerifyMode(modesListMin);
            List<DisplayModeList> modesListIntermediate = base.GetIntermediateModeForConfig(base.CurrentConfig.CustomDisplayList, base.CurrentConfig.ConfigType.GetUnifiedConfig());
            ApplyMode(modesListIntermediate);
            VerifyMode(modesListIntermediate);
            List<DisplayModeList> modesListMax = base.GetMaxModeForConfig(base.CurrentConfig.CustomDisplayList, base.CurrentConfig.ConfigType.GetUnifiedConfig());
            ApplyMode(modesListMax);
            VerifyMode(modesListMax);
        }

        protected virtual void ApplyMode(List<DisplayModeList> argDispModeList)
        {
            argDispModeList.ForEach(curDisp =>
            {
                curDisp.supportedModes.ForEach(curMode =>
                {
                    base.ApplyModeOS(curMode, curMode.display);

                    //CheckWatermark(curMode.display);//watermark
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
                    VerifyTiming(curMode);
                });
            });
        }

        protected virtual void VerifyTiming(DisplayMode displayMode)
        {

        }
    }
}



