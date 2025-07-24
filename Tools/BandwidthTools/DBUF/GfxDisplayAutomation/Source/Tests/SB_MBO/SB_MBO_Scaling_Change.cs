using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_MBO_Scaling_Change : SB_MBO_Basic
    {
        DisplayMode mode;
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            int mid = 0;
            mode = base.GetAppliedMode(DisplayType.EDP);
            DisplayMode originalMode = mode;
            if(mode.ScalingOptions.Count <= 1)
            {
                List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);
                allModeList.ForEach(curDisp =>
                {
                    mid = curDisp.supportedModes.Count / 2;
                    mode = curDisp.supportedModes.ElementAt(mid);
                    while ((mode.ScalingOptions.Count <= 1) && (mid < curDisp.supportedModes.Count))
                    {
                        mid++;
                        mode = curDisp.supportedModes.ElementAt(mid);
                    }
                    base.ApplyModeOS(mode, mode.display);
                });
            }
            this.ApplyandVerifyScaling(mode);
            base.ApplyModeOS(originalMode, originalMode.display);
            base.StopVideo();
            base.CleanUpHotplugFramework();
        }
        private void ApplyandVerifyScaling(DisplayMode curMode)
        {
            DisplayScaling curr_Scaling = AccessInterface.GetFeature<DisplayScaling, DisplayType>(Features.Scaling, Action.GetMethod, Source.AccessAPI, curMode.display);
            curMode.ScalingOptions.ForEach(scale =>
            {
                ScalingOptions scaleOption = (ScalingOptions)scale;
                if (!scaleOption.Equals(curr_Scaling))
                {
                    DisplayScaling dsScaling = new DisplayScaling(curMode.display, scaleOption);
                    AccessInterface.SetFeature<bool, DisplayScaling>(Features.Scaling, Action.SetMethod, dsScaling);
                    curr_Scaling = AccessInterface.GetFeature<DisplayScaling, DisplayType>(Features.Scaling, Action.GetMethod, Source.AccessAPI, curMode.display);
                    if (dsScaling.Equals(curr_Scaling))
                        Log.Success("Current Scaling : {0}  ------  Expected(Applied) Scalling : {1}", curr_Scaling.ToString(), dsScaling);
                    else
                        Log.Fail("Scaling Differ - Current Scaling from SDK Manager : {0} Expected(Applied) Scalling : {1}", curr_Scaling.ToString(), dsScaling);
                    base.VerifyMBOEnable();
                }
            });
        }
    }
}
