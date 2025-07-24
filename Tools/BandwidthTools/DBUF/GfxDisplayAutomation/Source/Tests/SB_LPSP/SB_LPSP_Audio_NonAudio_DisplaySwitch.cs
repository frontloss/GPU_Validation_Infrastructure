namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System.Text.RegularExpressions;

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_LPSP_Audio_NonAudio_DisplaySwitch : SB_LPSP_Base
    {
        protected AudioDataProvider _audioEndpointData = null;
        private SetAudioParam _inParam = null;
        protected AudioInputSource _audioInputSource;

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            _audioInputSource = AudioInputSource.Single;
            _inParam = new SetAudioParam();
            if (base.CurrentConfig.DisplayList.Count < 2)
                Log.Abort("Minimum two display required to run the test");
            ApplyNativeMode();            
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Verify LPSP Registers");
            LPSPRegisterVerify(true);
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3() 
        {
            ApplyNonNativeMode();            
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Verify LPSP Registers");
            LPSPRegisterVerify();
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
           
            Log.Message(true, "Plug audio capable panel");
            base.CurrentConfig.PluggableDisplayList.ForEach(curDisp =>
            {

                    base.HotPlug(curDisp);
                    Log.Message(true, "Switch to SD {0}", curDisp);
                    DisplayConfig dispConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = curDisp};
                    if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dispConfig))
                        Log.Success("Config SET : SD - {0}", curDisp);
                    else
                        Log.Abort("Failed to set Config : SD - {0}", curDisp);
                    Log.Message(true, "Checking audio End point");
                    CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
                    Log.Message(true, "Verify LPSP status");
                    base.LPSPRegisterVerify(false);
                    Log.Message(true, "Unplug {0}", curDisp);
                    base.HotUnPlug(curDisp);
                    Log.Message(true, "Switch to SD EDP");
                    dispConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = DisplayType.EDP };
                    if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dispConfig))
                        Log.Success("Config SET : SD - EDP");
                    else
                        Log.Abort("Failed to set Config : SD - EDP");
                    Log.Message(true, "Apply non-native mode");
                    ApplyNonNativeMode();
                    Log.Message(true, "Verify LPSP Registers");
                    LPSPRegisterVerify();
                
            });
           
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            Log.Message(true, "Switch to SD EDP");
            DisplayConfig dispConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = DisplayType.EDP };
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dispConfig))
                Log.Success("Config SET : SD - EDP");
            else
                Log.Abort("Failed to set Config : SD - EDP");
        }
     
        internal void SetAudioSource()
        {
            DisplayConfig configParam = null;
            if (base.CurrentConfig.CustomDisplayList.Count == 2)
                configParam = new DisplayConfig
                {
                    ConfigType = DisplayConfigType.DDC,
                    PrimaryDisplay = base.CurrentConfig.PrimaryDisplay,
                    SecondaryDisplay = base.CurrentConfig.SecondaryDisplay
                };
            else if (base.CurrentConfig.CustomDisplayList.Count == 3)
                configParam = new DisplayConfig
                {
                    ConfigType = DisplayConfigType.TDC,
                    PrimaryDisplay = base.CurrentConfig.PrimaryDisplay,
                    SecondaryDisplay = base.CurrentConfig.SecondaryDisplay,
                    TertiaryDisplay = base.CurrentConfig.TertiaryDisplay
                };
            else
                Log.Abort("Test required atleast one external display to run");
            if (!AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, configParam))
                Log.Abort("Unable to set display config {0} ", configParam.GetCurrentConfigStr());
            _inParam.setAudioInfo = Automation.SetAudioSource.SetAudioTopology;
            _inParam.audioTopology = _audioInputSource;
            Log.Message("Change audio source to {0} through CUI SDK", _audioInputSource.ToString());
            if (AccessInterface.SetFeature<bool, SetAudioParam>(Features.AudioEnumeration, Action.SetMethod, _inParam))
            {
                Log.Success("Audio topology changed successfully");
            }
            else
                Log.Abort("Failed to change audio topology");
        }
        internal void CheckAudioEndPoint(AudioDataProvider argAudioEndpointData)
        {
            bool SUCCESS = true;
            _audioEndpointData = argAudioEndpointData;
            DisplayConfig currentDisplayConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);

            if (_audioInputSource == AudioInputSource.Single && currentDisplayConfig.ConfigType == DisplayConfigType.SD && currentDisplayConfig.PrimaryDisplay == DisplayType.EDP)
            {
                Log.Message("Current display config is {0}, not checking audio enumeration", currentDisplayConfig.GetCurrentConfigStr());
                return;
            }

            VerifyAudioDriverStatus();

            if (_audioInputSource == AudioInputSource.Single && (DisplayExtensions.AudioWTVideoEnable == false && DisplayExtensions.EnableMonitorTurnOff == true) &&
                    argAudioEndpointData.ListAudioEndpointDevice.Count != 1 && currentDisplayConfig.ConfigType != DisplayConfigType.TED)
            {
                Log.Fail("Single source audio endpoint enumeration is not as expected");
                Log.Message("Current audio endpoint device are {0} ", argAudioEndpointData.GetCurrentAudioEndpointDevice());
            }
            else if (_audioInputSource == AudioInputSource.Multiple && argAudioEndpointData.ActiveAudioEndpointDevice == argAudioEndpointData.MaxSupportedAudioEndpoint &&
                      currentDisplayConfig.ConfigType == DisplayConfigType.TED && (DisplayExtensions.AudioWTVideoEnable == false && DisplayExtensions.EnableMonitorTurnOff == true) &&
                        argAudioEndpointData.ListAudioEndpointDevice.Count != argAudioEndpointData.MaxSupportedAudioEndpoint)
            {
                Log.Fail("Multi source audio config end point enumeration are not as expected");
                Log.Message("Current audio endpoint device are {0} ", argAudioEndpointData.GetCurrentAudioEndpointDevice());
            }

            else
                Log.Message("Audio endpoint enumeration are as expected");
            Log.Message("AUD_PIN_ELD_CP_VLD Register Value is {0}", argAudioEndpointData.ListAudioDisplayInfo[0].AUD_PIN_ELD_Reg_Value);
            Log.Verbose("Checking Audio register ELD, CP, PD bit are programed correctly or not");
            foreach (AudioDisplayInfo auxDispInfo in argAudioEndpointData.ListAudioDisplayInfo)
            {
                if (!auxDispInfo.isValidRegisterEntry)
                {
                    Log.Fail("Registers are not programed correctly for {0} -> {1}, expected is {2} and actual value is {3}",
                        auxDispInfo.dispType, auxDispInfo.planeInfo, auxDispInfo.expectedRegValue, auxDispInfo.PlaneRegValue);
                    SUCCESS = SUCCESS & false;
                }
            }
            if (SUCCESS)
                Log.Success("Registers are programed correctly for all active display");
        }
        internal void VerifyAudioDriverStatus()
        {
            if (base.MachineInfo.Driver.AudioDriverStatus.ToString().ToLower().Contains("ok"))
                Log.Verbose("Intel(R) Audio Driver is Status Verified");
            else
            {
                DriverInfo driverInfo = AccessInterface.GetFeature<DriverInfo, DriverAdapterType>(Features.DriverFunction, Action.GetMethod, Source.AccessAPI, DriverAdapterType.Audio);
                if (driverInfo.AudioDriverStatus.ToString().ToLower().Contains("ok"))
                    Log.Verbose("Intel(R) Audio Driver is Status Verified");
                else
                    Log.Abort("Intel Audio Driver is not installed Under Sound,Video and game controllers");
            }
        }

    } 
}