namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    class SB_YTiling_Base : TestBase
    {
        private List<string> FeatureMap
        {
            get
            {
                List<string> _featureMap = new List<string>() { "PLANE_1_A", "PLANE_1_B", "PLANE_1_C", "PLANE_2_A", "PLANE_2_B", "PLANE_2_C",
            "PLANE_3_A","PLANE_3_B","PLANE_3_C" };
                return _featureMap;
            }
        }

        private void ReadYTilingInfo()
        {
            FeatureMap.ForEach(curEvent =>
            {
                VerifyRegisters(curEvent);
            });
        }
        protected void ApplyConfigVerifyRegister(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());
            ReadYTilingInfo();
        }
        private void VerifyRegisters(string pRegisterEvent)
        {
            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = PIPE.NONE;
            eventInfo.plane = PLANE.NONE;
            eventInfo.port = PORT.NONE;
            eventInfo.eventName = pRegisterEvent;
            EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);

            MMIORW mmiorwObj = new MMIORW();
            mmiorwObj.FeatureName = pRegisterEvent;
            mmiorwObj.RegInfList = returnEventInfo.listRegisters;

            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            AccessInterface.GetFeature<bool, MMIORW>(Features.YTiling, Action.GetMethod, Source.AccessAPI, mmiorwObj);
        }
    }
}
