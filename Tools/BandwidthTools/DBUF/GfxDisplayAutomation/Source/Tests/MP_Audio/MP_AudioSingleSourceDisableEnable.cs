namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using System.Threading;
    class MP_AudioSingleSourceDisableEnable : MP_Audio_Base
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void SetAudioSource()
        {
            base.SetAudioSource();
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void SetConfigMethod()
        {
            Log.Message(true, "Set Current config via OS call");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                Log.Abort("Config not applied!");
            }
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void GetAudioEndpoint()
        {
            Log.Message(true, "Check Audio endpoint and verify AUD_PIN_ELD_CP_VLD Register");
            base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void DisableEnableDriver()
        {
            Log.Message(true, "Disabling Audio Driver");
            if (AccessInterface.SetFeature<bool, DriverAdapterType>(Features.DisableDriver, Action.SetMethod, DriverAdapterType.Audio))
            {
                Log.Success("Successfully disabled audio driver");
                validateEndpoint(false);
            }
            else
            {
                Log.Fail("Unable to disable Audio Driver");
            }
            Thread.Sleep(30000);
            Log.Message(true, "Enabling Audio Driver");
            if (AccessInterface.SetFeature<bool, DriverAdapterType>(Features.EnableDriver, Action.SetMethod, DriverAdapterType.Audio))
            {
                Log.Success("Successfully enabled audio driver");
                validateEndpoint(true);
            }
            else
            {
                Log.Fail("Unable to enable Audio Driver");
            }
            Log.Message(true, "Disabling Gfx Driver");
            if (AccessInterface.SetFeature<bool, DriverAdapterType>(Features.DisableDriver, Action.SetMethod, DriverAdapterType.Intel))
            {
                Log.Success("Successfully disabled Gfx driver");
                validateEndpoint(false, true);
            }
            else
            {
                Log.Fail("Unable to disabled Gfx driver");
            }
            Log.Message(true,"Enabling Gfx Driver");
            if (AccessInterface.SetFeature<bool, DriverAdapterType>(Features.EnableDriver, Action.SetMethod, DriverAdapterType.Intel))
            {
                Log.Success("Successfully enabled Gfx driver");
                DisplayConfig currentDisplayConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);

                if (currentDisplayConfig.ConfigType == DisplayConfigType.SD && currentDisplayConfig.PrimaryDisplay == DisplayType.EDP)
                {
                    foreach (DisplayType DT in base.CurrentConfig.PluggableDisplayList)
                    {
                        Log.Message("{0} is not enumerated..Plugging it", DT);
                        if (base.HotPlug(DT))
                        {
                            Log.Success("Display {0} is plugged successfully", DT);
                        }
                        else
                            Log.Fail("Unable to hot plug display {0}", DT);
                    }
                    if (base.CurrentConfig.EnumeratedDisplays.Count == base.CurrentConfig.PluggableDisplayList.Count)
                    {
                        SetConfigMethod();
                        validateEndpoint(true);
                    }
                }
            }
            else
                Log.Fail("Unable to enabled Gfx Driver");
        }

        private void validateEndpoint(bool statusCheck, bool IsIGFXDisabled = false)
        {
            bool SUCCESS = true;
            AudioDataProvider audioEndpointData = AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI);
            _audioEndpointData = audioEndpointData;
            if (!statusCheck)
            {
                if (audioEndpointData.ListAudioEndpointDevice.Count.Equals(0))
                    Log.Success("Audio endpoint as expected, there is no audio endpoint");
                else
                {
                    Log.Fail("Audio endpoint is not as expected, Gfx enumerate audio endpoint");
                    Log.Verbose("Default audio endpoint device is {0}", base.GetDefaultEndPoint().FriendlyName);
                }
            }
            else
            {
                if (audioEndpointData.ListAudioEndpointDevice.Count.Equals(0))
                    Log.Fail("Audio endpoint is not as expected, there is no audio endpoint");
                else
                {
                    Log.Success("Audio endpoint as expected");
                    Log.Verbose("Default audio endpoint device is {0}", base.GetDefaultEndPoint().FriendlyName);
                }
            }
            if (!IsIGFXDisabled)
            {
                Log.Message("AUD_PIN_ELD_CP_VLD Register Value is {0}", audioEndpointData.ListAudioDisplayInfo[0].AUD_PIN_ELD_Reg_Value);
                Log.Verbose("Checking Audio register ELD, CP, PD bit are programed correctly or not");
                foreach (AudioDisplayInfo auxDispInfo in audioEndpointData.ListAudioDisplayInfo)
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
        }
    }
}
