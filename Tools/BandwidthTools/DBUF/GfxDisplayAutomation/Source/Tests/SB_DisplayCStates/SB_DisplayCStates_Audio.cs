namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using System;

    class SB_DisplayCStates_Audio : SB_DisplayCStates_BasicFeature
    {
        private SetAudioParam _inParam = null;
        private AudioInputSource _audioInputSource;
        private AudioDataProvider _audioEndpointData = null;
        public Dictionary<int, DisplayType> displaySequence = new Dictionary<int, DisplayType>();
        public List<DisplayType> externalDisplayList = new List<DisplayType>();
        private uint DMCVersion = 0;

        [Test(Type = TestType.PreCondition, Order = 1)]
        public new void TestPreCondition()
        {
            DMCVersion = GetRegisterValue("DMC_VERSION", PIPE.NONE, PLANE.NONE, PORT.NONE);
            Log.Message(true, "DMC Version for {0}", DMCVersion);   
            _audioInputSource = AudioInputSource.Single;
            _inParam = new SetAudioParam();
            if (base.CurrentConfig.DisplayList.Count < 2)
                Log.Abort("Minimum two display required to run the test");
            //       base.TestPreCondition();
            Log.Message(true, "Set current config");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
            Log.Message(true, "Check Audio endpoint and verify AUD_PIN_ELD_CP_VLD Register");
            CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void DisplaySwitch()
        {
            Log.Message(true, "Check Audio endpoint and verify AUD_PIN_ELD_CP_VLD Register");
            Log.Message(true, "Set current config");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
            Log.Message(true, "Check Audio endpoint and verify AUD_PIN_ELD_CP_VLD Register");
            CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
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

            //   VerifyAudioDriverStatus();

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