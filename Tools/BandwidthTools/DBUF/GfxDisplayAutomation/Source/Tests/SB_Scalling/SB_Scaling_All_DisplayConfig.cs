namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;

    class SB_Scaling_All_DisplayConfig : SB_Scaling_DisplayConfig
    {

        protected override void ApplyAndVerifyScalling(DisplayType pDisplayType, bool pApplyMode)
        {
            List<DisplayMode> dispModes = GetAllModesForTest(pDisplayType);
            DisplayScaling dsScaling = null;

            dispModes.ForEach(dm =>
            {
                AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, dm);

                dm.ScalingOptions.ForEach(sc =>
                {
                    ScalingOptions apply_Scaling = (ScalingOptions)sc;

                    // Not considering CAR : as it covered in different test scenario
                    if (apply_Scaling != ScalingOptions.Customize_Aspect_Ratio)
                    {
                        Log.Message(true, "{0}", apply_Scaling);
                        dsScaling = new DisplayScaling(pDisplayType, apply_Scaling);
                        AccessInterface.SetFeature<bool, DisplayScaling>(Features.Scaling, Action.SetMethod, dsScaling);

                        DisplayScaling curr_Scalling_SDK_Manager = AccessInterface.GetFeature<DisplayScaling, DisplayType>(Features.Scaling, Action.GetMethod, Source.AccessAPI, pDisplayType);

                        if (dsScaling.Equals(curr_Scalling_SDK_Manager))
                            Log.Success("Current Scalling : {0}  ------  Expected(Applied) Scalling : {1}", curr_Scalling_SDK_Manager.ToString(), apply_Scaling);
                        else
                            Log.Fail("Scalling Differ - Current Scalling from SDK Manager : {0} Expected(Applied) Scalling : {1}", curr_Scalling_SDK_Manager.ToString(), apply_Scaling);

                    }
                });

            });
        }

        private List<DisplayMode> GetAllModesForTest(DisplayType pDisplayType)
        {            
            List<DisplayModeList> displayModeList_OSPage = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, new List<DisplayType>() { pDisplayType});
            List<DisplayMode> dispModes = displayModeList_OSPage.Where(dML => dML.display == pDisplayType).Select(dML => dML.supportedModes).FirstOrDefault();

            return dispModes;
        }        

    } // End SB_Scaling_All_DisplayConfig
}