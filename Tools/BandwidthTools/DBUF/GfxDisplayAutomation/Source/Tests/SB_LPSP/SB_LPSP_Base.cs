namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

    class SB_LPSP_Base : TestBase
    {
        protected const string LPSP_REGISTER_EVENT = "LPSP_ENABLE" ;
        protected const string OVERLAY_REGISTER_EVENT = "OVERLAY_ENABLE";

        protected Dictionary<System.Action, System.Action> _applyMode = new Dictionary<System.Action, System.Action>();  

        public SB_LPSP_Base()
        {
            _applyMode.Add(ApplyNativeMode, LPSPRegisterVerifyTrue);
            _applyMode.Add(ApplyNonNativeMode, LPSPRegisterVerify);    
        }

        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (!CurrentConfig.CustomDisplayList.Contains(DisplayType.EDP))
                Log.Abort("EDP must be connected to run the Test");

            DisplayConfig dispConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = DisplayType.EDP };
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dispConfig))
                Log.Success("Config SET : SD - EDP");
            else
                Log.Abort("Failed to set Config : SD - EDP");            
        }

        protected void OverlayRegisterVerify(bool pEnable , DisplayType pDisplayType) 
        {
            // Geting PIPE , Plane information for pannels
            PipePlaneParams pipePlane1 = new PipePlaneParams(pDisplayType);
            pipePlane1 = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane1);
            Log.Message("For display : {0}  @@@  PIPE : {1} @@@ PLANE : {2}", pDisplayType, pipePlane1.Pipe, pipePlane1.Plane);

            if (VerifyRegisters(OVERLAY_REGISTER_EVENT, PIPE.NONE, pipePlane1.Plane, PORT.NONE,false))
            {
                if (pEnable)
                    Log.Success("Overlay is Enable for {0}" , pDisplayType);
                else
                    Log.Fail("Overlay is Enable for {0} which is not expected.", pDisplayType);
            }
            else
            {
                if (!pEnable)
                    Log.Success("Overlay is Disable for {0}", pDisplayType);
                else
                    Log.Fail("Overlay is Disable for {0} which is not expected.", pDisplayType);
            }
        }

        protected void LPSPRegisterVerifyTrue() 
        {
            LPSPRegisterVerify(true);
        }

        protected void LPSPRegisterVerify()
        {
            // bool lpspStatus = this.MachineInfo.PlatformEnum == Platform.BDW ? true : false;
            bool lpspStatus = true;
            List<Platform> panelFitter = new List<Platform>() { Platform.HSW};
            if (panelFitter.Contains(this.MachineInfo.PlatformDetails.Platform) && !IsNativeResolution(DisplayType.EDP))
            {
                if(base.MachineInfo.OS.Type != OSType.WINTHRESHOLD) //For WinTH, Due to virtual modeset, LPSP is enabled for all the resolutions.
                    lpspStatus = false;
            }
            LPSPRegisterVerify(lpspStatus);
        }

        protected void LPSPRegisterVerify(bool pEnable)
        {
            if (VerifyRegisters(LPSP_REGISTER_EVENT, PIPE.NONE, PLANE.NONE, PORT.PORTA, false))
            {
                if (pEnable)
                    Log.Success("LPSP is Enable");
                else
                    Log.Fail("LPSP is Enable which is not expected.");
            }
            else 
            {
                if (!pEnable)
                    Log.Success("LPSP is Disable");
                else
                    Log.Fail("LPSP is Disable which is not expected.");            
            }
        }

        protected List<DisplayMode> GetModesForTest(DisplayType pDisplayType)
        {
            List<DisplayType> displays = new List<DisplayType>();
            displays.Add(pDisplayType);
            List<DisplayModeList> displayModeList_OSPage = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, displays);
            List<DisplayMode> dispModes = displayModeList_OSPage.Where(dML => dML.display == pDisplayType).Select(dML => dML.supportedModes).FirstOrDefault();
            return dispModes;
        }

        protected void ApplyNativeMode()
        {
            Log.Message(true,"Applying Native Mode");

            // Finding Native Mode
            List<DisplayMode> displayModes = GetModesForTest(DisplayType.EDP) ;
            
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, displayModes.Last()))
                Log.Success("Native Mode Applied");
            else
                Log.Fail("Failed to apply Native Mode");            
        }
       
        protected void ApplyNonNativeMode()
        {
            Log.Message(true, "Applying Non Native Mode");

            // Finding Non Native Mode
            List<DisplayMode> displayModes = GetModesForTest(DisplayType.EDP);

            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, displayModes.ElementAt(displayModes.Count / 2)))
                Log.Success("Non Native Mode Applied");
            else
                Log.Fail("Failed to apply Non Native Mode");            
        }
        
        protected void ApplyConfig(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());
        }

        public bool IsNativeResolution(DisplayType display)
        {
            bool status = true;
            DisplayConfig  currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);

            if (currentConfig.CustomDisplayList.Contains(display))
            {
                DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
                DisplayMode currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
                var enums = Enum.GetValues(typeof(ScalingOptions));
                ScalingOptions scalingOptionSet = (ScalingOptions)enums.GetValue(currentMode.ScalingOptions[0]); ;
                DisplayMode ores = displayInfo.DisplayMode;

                DisplayMode d = new DisplayMode();
                if (!(d.Equals(ores, currentMode) && scalingOptionSet== ScalingOptions.Maintain_Display_Scaling))
                    status = false;
            }
            return status;
        }
   }
}
