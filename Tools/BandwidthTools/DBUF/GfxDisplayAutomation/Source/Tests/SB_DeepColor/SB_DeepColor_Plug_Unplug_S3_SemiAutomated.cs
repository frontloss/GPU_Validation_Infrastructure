namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;

    class SB_DeepColor_Plug_Unplug_S3_SemiAutomated : SB_DeepColor_Base
    {
        DisplayInfo _PluggedDisplay;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public override void TestPreCondition()
        {
            AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod,CurrentConfig);            
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            if (!AccessInterface.SetFeature<bool, String>(Features.PromptMessage, Action.SetMethod, "Plug DeepColor Panel to continue test"))
                Log.Abort("User rejected Semi Automated Request");

            List<DisplayInfo> enumeratedDisplays = AccessInterface.GetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);

            if (enumeratedDisplays.Count <= CurrentConfig.EnumeratedDisplays.Count)
                Log.Abort("Please Plug the display");

            _PluggedDisplay = FindPluggedDisplay(enumeratedDisplays);

            if (_PluggedDisplay == null)
                Log.Abort("Please Connect Display , Could not find Newly connected display");


            if (!((_PluggedDisplay.DisplayType == DisplayType.HDMI && _PluggedDisplay.ColorInfo.MaxDeepColorValue == HDMI_BPC_VALUE) || (_PluggedDisplay.DisplayType == DisplayType.HDMI_2 && _PluggedDisplay.ColorInfo.MaxDeepColorValue == HDMI_BPC_VALUE) || (_PluggedDisplay.DisplayType == DisplayType.DP && _PluggedDisplay.ColorInfo.MaxDeepColorValue == DP_BPC_VALUE)))
                Log.Abort("Connected Pannel is not Supporting DeepColor");

            CurrentConfig.EnumeratedDisplays.Clear();
            CurrentConfig.EnumeratedDisplays.AddRange(enumeratedDisplays); 
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            DisplayConfig dispConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD , PrimaryDisplay = _PluggedDisplay.DisplayType};
            AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dispConfig);            
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            EnableDPApplet();
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            DisplayConfig dispConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = _PluggedDisplay.DisplayType };
            PipePlaneParams pipePlane = GetPipePlane(_PluggedDisplay);
            CheckDeepColorconditions(_PluggedDisplay, pipePlane, DeepColorAppType.DPApplet, true, dispConfig, DisplayHierarchy.Display_1);
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            if (!AccessInterface.SetFeature<bool, String>(Features.PromptMessage, Action.SetMethod, "Plug Non DeepColor Panel when system goes to S3"))
                Log.Abort("User rejected Semi Automated Request");

            Log.Message("Putting the system into {0} state & resume", PowerStates.S3);
            PowerParams powerParams = new PowerParams();
            powerParams.Delay = 15;
            base.InvokePowerEvent(powerParams, PowerStates.S3);
            Log.Success("Put the system into {0} state & resumed", PowerStates.S3);

            List<DisplayInfo> enumeratedDisplays = AccessInterface.GetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);

            if (enumeratedDisplays.Count < CurrentConfig.EnumeratedDisplays.Count)
                Log.Abort("Please Plug the display");

            _PluggedDisplay = FindPluggedDisplay(enumeratedDisplays);

            if (_PluggedDisplay == null)
                Log.Abort("Please Connect Display , Could not find Newly connected display");

            if (((_PluggedDisplay.DisplayType == DisplayType.HDMI && _PluggedDisplay.ColorInfo.MaxDeepColorValue == HDMI_BPC_VALUE) || (_PluggedDisplay.DisplayType == DisplayType.HDMI_2 && _PluggedDisplay.ColorInfo.MaxDeepColorValue == HDMI_BPC_VALUE) || (_PluggedDisplay.DisplayType == DisplayType.DP && _PluggedDisplay.ColorInfo.MaxDeepColorValue == DP_BPC_VALUE)))
                Log.Abort("Connected Pannel is Supporting DeepColor");

            CurrentConfig.EnumeratedDisplays.Clear();
            CurrentConfig.EnumeratedDisplays.AddRange(enumeratedDisplays); 
        }

        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            PipePlaneParams pipePlane = GetPipePlane(_PluggedDisplay);
            DisplayConfig dispConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = _PluggedDisplay.DisplayType };
            CheckDeepColorconditions(_PluggedDisplay, pipePlane, DeepColorAppType.DPApplet, false, dispConfig, DisplayHierarchy.Display_1);
        }

        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            CloseApp(DeepColorAppType.DPApplet);
        }

        private DisplayInfo FindPluggedDisplay(List<DisplayInfo> pNewEnumeratedDisplays)
        {
            Boolean isdisplayNew = true;
            DisplayInfo newDisplay = null;

            pNewEnumeratedDisplays.ForEach(nD =>
            {
                isdisplayNew = true;

                CurrentConfig.CustomDisplayList.ForEach(bD =>
                {
                    if (nD.DisplayType == bD)
                        isdisplayNew = false;
                });

                if (isdisplayNew)
                    newDisplay = nD;
            });

            return newDisplay;
        }
    }
}