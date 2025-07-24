namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;
    using System.Text.RegularExpressions;

    class MP_Mode_ListAllModes_OSPage : TestBase
    {
        private List<DisplayModeList> allModeList = new List<DisplayModeList>();

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            if (!base.CurrentConfig.DisplayList.Count.Equals(base.CurrentConfig.ConfigType.GetDisplaysCount()))
                Log.Abort("<DualConfig>/<TriConfig>  test requires atleast <2>/<3> displays connected!");

            Log.Message(true, "Set Current config via OS call");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                List<uint> winMonitorIdList = base.ListEnumeratedDisplays();
                List<uint> enumeratedWinMonIDList = base.CurrentConfig.EnumeratedDisplays.Where(dI => !dI.WindowsMonitorID.Equals(0)).Select(dI => dI.WindowsMonitorID).ToList();
                if (!enumeratedWinMonIDList.Count.Equals(winMonitorIdList.Count) && !CommonExtensions.HasRetryThruRebootFile())
                {
                    Log.Verbose("Currently enumerated displays mismatch! A reboot is required.");
                    CommonExtensions.WriteRetryThruRebootInfo();
                    base.InvokePowerEvent(new PowerParams() { Delay = 5, PowerStates = PowerStates.S5}, PowerStates.S5);
                }
                else
                    CommonExtensions.ClearRetryThruRebootFile();
                Log.Abort("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            DisplayInfo currentDisplayInfo = null;
            List<DisplayMode> testModes = null;

            if (!allModeList.Count.Equals(0))
            {
                allModeList.ForEach(dML =>
                {
                    currentDisplayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == dML.display).First();
                    testModes = this.TestModes(dML.supportedModes);
                    testModes.ForEach(dM => ApplyAndVerify(dM, currentDisplayInfo));
                });
            }
            else
                Log.Fail(false, "No modes returned!");
        }
        /*[Test(Type = TestType.PostCondition, Order = 3)]
        public void TestPostCondition()
        {
            AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
        }*/

       
        /*private List<DisplayMode> ModesRefreshRates(List<DisplayMode> testMode, List<DisplayMode> entireModeList)
        {
            List<DisplayMode> modeRefreshRate = new List<DisplayMode>();
            for (int i = 0; i < testMode.Count; i++)
            {
                for (int j = 0; j < entireModeList.Count; j++)
                {
                    if ((testMode[i].HzRes == entireModeList[j].HzRes) && (testMode[i].VtRes == entireModeList[j].VtRes))
                        modeRefreshRate.Add(entireModeList[j]);
                }
            }
            return modeRefreshRate;
        }
        private void GetDisplayModesFromCUI(List<DisplayModeList> argDisplayModeList)
        {
            Log.Message("DisplayModeList preparing through CUI");

            //AccessInterface.SetFeature<bool>(Features.LaunchCUI, Action.SetNoArgs);
            List<uint> bppList = GetBpp();

            //AccessInterface.Navigate(Features.DisplaySettings);

            base.CurrentConfig.DisplayList.ForEach(dT =>
            {
                DisplayModeList displayModeList = new DisplayModeList();
                displayModeList.display = dT;

                AccessInterface.SetFeature(Features.SelectDisplay, Action.Set, dT);
                List<string> allSupportedResolutions = AccessInterface.GetFeature<List<string>>(Features.Modes, Action.GetAll);

                // Only consider Min and Max Resolutions 
                List<string> minMaxResolutions = PrepareResolutionList(allSupportedResolutions);

                minMaxResolutions.ForEach(rS =>
                {
                    AccessInterface.SetFeature(Features.Modes, Action.Set, rS);
                    List<string> allRefreshRateList = AccessInterface.GetFeature<List<string>>(Features.RefreshRate, Action.GetAll);

                    allRefreshRateList.ForEach(rF =>
                    {
                        AccessInterface.SetFeature(Features.RefreshRate, Action.Set, rF);
                        List<ScalingOptions> scalingOptionsList = AccessInterface.GetFeature<List<ScalingOptions>>(Features.Scaling, Action.GetAll, Source.AccessUI);
                        List<uint> scalingOptions = GetScaling(scalingOptionsList);

                        uint isInterlaced = Convert.ToUInt32(rF.Contains("p") ? 0 : 1);
                        rF = rF.Split(isInterlaced == 1 ? 'i' : 'p').First().Trim();
                        bppList.ForEach(bPP =>
                        {
                            displayModeList.supportedModes.Add(new DisplayMode() { HzRes = Convert.ToUInt32(rS.Split('x').First().Trim()), VtRes = Convert.ToUInt32(rS.Split('x').Last().Trim()), Bpp = bPP, RR = Convert.ToUInt32(rF), InterlacedFlag = isInterlaced, display = dT, Angle = Convert.ToUInt32(0), ScalingOptions = scalingOptions });
                        }); // End Bpp Loop

                    }); // End RefreshRate Loop

                }); // End Resolution Loop 

                argDisplayModeList.Add(displayModeList);

            }); // End DisplayType Foreach loop

        } // End GetDisplayModesFromCUI method */


        private bool ApplyAndVerify(DisplayMode argDispMode, DisplayInfo argDisplayInfo)
        {
            Log.Message(true, "Setting Mode : {0} for {1}", argDispMode.GetCurrentModeStr(true), argDispMode.display);
            if (!AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argDispMode))
            {
                Log.Fail("Fail to apply Mode");
                return false;
            }
            else
                Log.Success("Mode applied successfully");

            // Get Current DisplayMode
            DisplayMode currentDisplayMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, argDisplayInfo);

            if (currentDisplayMode.GetCurrentModeStr(true).Equals(argDispMode.GetCurrentModeStr(true)))
                Log.Success("Mode applied and CUI are in sync", argDispMode.display);
            else
            {
                Log.Fail("Applied Mode {0} . Current OS Page Mode : {1}  ", argDispMode.GetCurrentModeStr(true), currentDisplayMode.GetCurrentModeStr(true));
                return false;
            }
            
            /*Log.Message("Verify Refresh Rate set Properly via CUI");
            if (argDispMode.RR == currentDisplayMode.RR)
                Log.Success("Refresh Rate verified through CUI");
            else
            {
                Log.Fail("Refresh Rate in CUI is {0}, expected Refresh rate is {1}", currentDisplayMode.RR, argDispMode.RR);
                return false;
            }*/
            return true;
        }
        private List<DisplayMode> TestModes(List<DisplayMode> displayModeList)
        {
            List<DisplayMode> testModes = new List<DisplayMode>();
            testModes.Add(displayModeList.First());
            testModes.Add(displayModeList[displayModeList.Count / 2]);
            List<DisplayMode> interlacedModeList = displayModeList.FindAll(DT => DT.InterlacedFlag.Equals(1));
            if (interlacedModeList.Count != 0)
                testModes.Add(interlacedModeList.First());
            testModes.Add(displayModeList.Last());
            return testModes;
        }
        /*private List<string> PrepareResolutionList(List<string> argResolutionList)
        {
            List<string> minMaxResolutions = new List<string>();
            minMaxResolutions.Add(argResolutionList.First());
            minMaxResolutions.Add(argResolutionList.Last());
            return minMaxResolutions;
        }*/

        /*private List<uint> GetScaling(List<ScalingOptions> argScalingOptionsList)
        {
            List<uint> scalingOptionList = new List<uint>();
            argScalingOptionsList.Remove(ScalingOptions.Customize_Aspect_Ratio);

            if (argScalingOptionsList.Count > 1)
                argScalingOptionsList.Remove(ScalingOptions.Maintain_Display_Scaling);

            argScalingOptionsList.ForEach(sO =>
            {
                scalingOptionList.Add(Convert.ToUInt32(sO));
            });

            return scalingOptionList;
        }

        private List<uint> GetBpp()
        {
            List<uint> bppList = new List<uint>();
            //AccessInterface.Navigate(Features.ColorDepth);
            List<ColorDepthOptions> allSupportedColordepths = AccessInterface.GetFeature<List<ColorDepthOptions>>(Features.ColorDepth, Action.GetAll);

            allSupportedColordepths.ForEach(cD =>
            {
                bppList.Add(Convert.ToUInt32(cD));
            });

            return bppList;
        }*/

    } //  End MP_Modes_ListAllModes_OSPage class	
}