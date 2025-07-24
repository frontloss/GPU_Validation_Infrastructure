namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;

    class MP_ACPI_HK_DisplaySwitch_Default : MP_ACPI_Base
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestPreCondition()
        {
            base.ReadACPIDataFromFile();
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            PerformTest(base.MachineInfo.PlatformDetails.Platform.ToString(), "F1");
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            PerformTest(base.MachineInfo.PlatformDetails.Platform.ToString(), "F2");
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            PerformTest(base.MachineInfo.PlatformDetails.Platform.ToString(), "F3");
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            PerformTest(base.MachineInfo.PlatformDetails.Platform.ToString(), "F4");
        }

        private void PerformTest(string argPlatform, string argKey)
        {
            Log.Message(true, "Performing acpi default switch for key {0} in {1}", argKey, argPlatform);
            List<DisplayConfig> toggleSequence = new List<DisplayConfig>();
            if (base._acpiToggle.ContainsKey(argKey))
            {
                toggleSequence = base._acpiToggle[argKey];
                DisplayConfig initialConfig = toggleSequence.First();
                if ((base.MachineInfo.OS.Type == OSType.WINTHRESHOLD) &&
                    (DisplayExtensions.GetUnifiedConfig(initialConfig.ConfigType).Equals(DisplayUnifiedConfig.Clone)))
                {
                    Log.Message("Initial config is {0} so returning from key {1}", initialConfig.ConfigType, argKey);
                    return;
                }
                base.SetConfig(initialConfig);
                DisplayConfig osConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
                Log.Verbose(osConfig.GetCurrentConfigStr());

                toggleSequence.RemoveAt(0);
                foreach (DisplayConfig currentDispConfig in toggleSequence)
                {
                    AccessInterface.SetFeature<bool, string>(Features.ACPIFunctions, Action.SetMethod, argKey);
                    osConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
                    Log.Verbose(osConfig.GetCurrentConfigStr());
                    if (osConfig.ConfigType != currentDispConfig.ConfigType)
                    {
                        if (base.MachineInfo.OS.Type == OSType.WIN7)
                        {//win7 delay for ED/TED config
                            System.Threading.Thread.Sleep(15000);
                            osConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
                            Log.Verbose(osConfig.GetCurrentConfigStr());
                            if (osConfig.ConfigType == currentDispConfig.ConfigType)
                            {
                                Log.Success("ACPI switch configutaion {0} match the expected sequence for Key: {1}", osConfig.GetCurrentConfigStr(), argKey);
                            }
                            else
                            {
                                Log.Fail(false, "Mismatch in config in key {0} Expected Configuration:{1} Current Configuration:{2}", argKey, currentDispConfig.GetCurrentConfigStr(), osConfig.GetCurrentConfigStr());
                                break;
                            }
                        }
                        else
                        {
                            Log.Fail(false, "Mismatch in config in key {0} Expected Configuration:{1} Current Configuration:{2}", argKey, currentDispConfig.GetCurrentConfigStr(), osConfig.GetCurrentConfigStr());
                            break;
                        }
                        
                    }
                    else
                    {
                        Log.Success("ACPI switch configutaion {0} match the expected sequence for Key: {1}", osConfig.GetCurrentConfigStr(), argKey);

                        if ((base.MachineInfo.OS.Type == OSType.WINTHRESHOLD) && 
                           (DisplayExtensions.GetUnifiedConfig(osConfig.ConfigType).Equals(DisplayUnifiedConfig.Clone)))
                        {
                            DisplayConfig dConfig = new DisplayConfig()
                            {
                                ConfigType = DisplayConfigType.SD,
                                PrimaryDisplay = base.CurrentConfig.PrimaryDisplay
                            };
                            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dConfig))
                                Log.Message("Config (SD {0}) applied successfully", dConfig.PrimaryDisplay);
                            else
                                Log.Fail("Config (SD {0}) not applied!", dConfig.PrimaryDisplay);
                            break;
                        }

                    }
                }
            }
            else
                Log.Message("Toggle sequence eliminated for key {0}", argKey);
        }
    }
}



