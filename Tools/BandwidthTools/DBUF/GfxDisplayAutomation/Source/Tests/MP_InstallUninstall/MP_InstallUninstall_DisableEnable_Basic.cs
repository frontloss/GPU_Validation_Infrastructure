namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;

    class MP_InstallUninstall_DisableEnable_Basic : TestBase
    {
        DriverInfo drivInfo;
        [Test(Type = TestType.Method, Order = 0)]
        public void TestPreCondition()
        {
            Log.Verbose("Connect all the displays planned in the grid");
            foreach (DisplayType DT in base.CurrentConfig.PluggableDisplayList)
            {
                Log.Message("Display {0} is not enumerated, plugging it back", DT);
                base.HotPlug(DT);
            }
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Fail("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            List<DisplayModeList> allSupportedModes = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.Default, base.CurrentConfig.DisplayList);
            List<DisplayModeList> testModes = new List<DisplayModeList>();
            if (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
            {
                List<DisplayMode> commonModes = null;
                commonModes = allSupportedModes.Where(dML => dML.display == base.CurrentConfig.PrimaryDisplay).Select(dML => dML.supportedModes).FirstOrDefault();
                allSupportedModes.Skip(1).ToList().ForEach(dML => commonModes = commonModes.Intersect(dML.supportedModes, new DisplayMode()).ToList());
                if (commonModes.Count() > 0)
                {
                    testModes.Add(
                        new DisplayModeList()
                        {
                            display = allSupportedModes.First().display,
                            supportedModes = new List<DisplayMode>()
                        });
                    testModes.First().supportedModes.Add(commonModes.First());
                    DisplayMode newMode = this.GetModeCombo(commonModes.First());
                    if (!newMode.HzRes.Equals(0))
                        testModes.First().supportedModes.Add(newMode);
                    newMode = this.GetModeCombo(commonModes, commonModes.First());
                    if (!newMode.HzRes.Equals(0))
                        testModes.First().supportedModes.Add(newMode);
                    testModes.First().supportedModes.Add(commonModes[commonModes.Count / 2]);
                    testModes.First().supportedModes.Add(commonModes.Last());
                }
            }
            else
            {
                allSupportedModes.ForEach(dML =>
                    {
                        testModes.Add(
                            new DisplayModeList()
                            {
                                display = dML.display,
                                supportedModes = new List<DisplayMode>()
                            });
                        List<DisplayMode> testSupporteModes = testModes.Where(idML => idML.display == dML.display).Select(idML => idML.supportedModes).First();
                        testSupporteModes.Add(dML.supportedModes.First());
                        DisplayMode newMode = this.GetModeCombo(dML.supportedModes.First());
                        if (!newMode.HzRes.Equals(0))
                            testSupporteModes.Add(newMode);
                        newMode = this.GetModeCombo(dML.supportedModes, dML.supportedModes.First());
                        if (!newMode.HzRes.Equals(0))
                            testSupporteModes.Add(newMode);
                        testSupporteModes.Add(dML.supportedModes[dML.supportedModes.Count / 2]);
                        testSupporteModes.Add(dML.supportedModes.Last());
                    });
            }

            testModes.ForEach(dML =>
                {
                    dML.supportedModes.ForEach(dM =>
                        {
                            Log.Message(true, "Set {0} on {1}", dM.GetCurrentModeStr(false), dML.display);
                            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, dM))
                            {
                                Log.Success("Mode set successful");
                                Log.Message("Disable the driver");
                                base.AssertDriverState(Features.DisableDriver, DriverState.Disabled, new[] { 3, 4 });

                                drivInfo = AccessInterface.GetFeature<DriverInfo, DriverAdapterType>(Features.DriverFunction, Action.GetMethod, Source.AccessAPI, DriverAdapterType.Intel);
                                if (drivInfo.Status.ToLower().Equals("disabled"))
                                    Log.Success("IGD Disabled.");
                                else
                                    Log.Fail("IGD not Disabled.");

                                Log.Message("Enable the driver");
                                base.AssertDriverState(Features.EnableDriver, DriverState.Running, new[] { 5, 6 });

                                drivInfo = AccessInterface.GetFeature<DriverInfo, DriverAdapterType>(Features.DriverFunction, Action.GetMethod, Source.AccessAPI, DriverAdapterType.Intel);
                                if (drivInfo.Status.ToLower().Equals("running"))
                                    Log.Success("IGD Enabled.");                                    
                                else
                                    Log.Fail("IGD not Enabled.");
                                TestPreCondition();
                            }
                            else
                                Log.Fail(false, "Mode set failed!");
                        });                    
                });
        }

        private DisplayMode GetModeCombo(DisplayMode argMode)
        {
            DisplayMode newMode = new DisplayMode();
            if (argMode.ScalingOptions.Count > 1)
            {
                newMode.Copy(argMode);
                newMode.ScalingOptions.Remove(argMode.ScalingOptions.First());
            }
            return newMode;
        }
        private DisplayMode GetModeCombo(List<DisplayMode> argModesList, DisplayMode argContext)
        {
            return argModesList.Where(dM => dM.GetCurrentModeStr(true).Equals(argContext.GetCurrentModeStr(true)) && !dM.RR.Equals(argContext.RR)).FirstOrDefault();
        }
    }
}