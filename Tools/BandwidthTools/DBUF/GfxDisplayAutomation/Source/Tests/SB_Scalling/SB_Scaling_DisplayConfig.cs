namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;

    public class SB_Scaling_DisplayConfig : TestBase
    {
        protected bool _considerMinRes = false;
        protected System.Action<DisplayType> _Corruption = null;
        [Test(Type = TestType.Method, Order = 0)]
        public virtual void TestStep0()
        {
            AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig);
        }

        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            // For DDC and TDC Mode only first time Mode will be applied
            bool applyMode = base.CurrentConfig.ConfigType == DisplayConfigType.DDC || base.CurrentConfig.ConfigType == DisplayConfigType.TDC ? false : true;

            Log.Message(true, "Apply and Verify Scaling for Display - {0}", base.CurrentConfig.PrimaryDisplay);
            ApplyAndVerifyScalling(base.CurrentConfig.PrimaryDisplay, true);

            if (base.CurrentConfig.ConfigTypeCount >= 2)
            {
                Log.Message(true, "Apply and Verify Scaling for Display - {0}", base.CurrentConfig.SecondaryDisplay);
                ApplyAndVerifyScalling(base.CurrentConfig.SecondaryDisplay, applyMode);

            }

            if (base.CurrentConfig.ConfigTypeCount == 3)
            {
                Log.Message(true, "Apply and Verify Scaling for Display - {0}", base.CurrentConfig.TertiaryDisplay);
                ApplyAndVerifyScalling(base.CurrentConfig.TertiaryDisplay, applyMode);
            }

        }

        protected virtual void ApplyAndVerifyScalling(DisplayType pDisplayType, bool pApplyMode)
        {
            List<DisplayMode> dispModes = GetModesForTest(pDisplayType);
            DisplayScaling dsScaling = null;
            bool status = true;
            dispModes.ForEach(dm =>
            {
                if (pApplyMode)
                {
                 status =   AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, dm);
                 if (!status)
                     Log.Fail("Failed to apply {0} for {1}", dm.GetCurrentModeStr(false), dm.display);
                }

                if (status == true)
                {
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
                            {
                                Log.Success("Current Scalling : {0}  ------  Expected(Applied) Scalling : {1}", curr_Scalling_SDK_Manager.ToString(), apply_Scaling);
                                if (pDisplayType == DisplayType.HDMI)
                                {
                                    CheckCorruptionViaDVMU(pDisplayType);
                                }
                            }
                            else
                                Log.Fail("Scalling Differ - Current Scalling from SDK Manager : {0} Expected(Applied) Scalling : {1}", curr_Scalling_SDK_Manager.ToString(), apply_Scaling);

                        }
                    });
                }
            });
        }

        protected List<DisplayMode> GetModesForTest(DisplayType pDisplayType)
        {
            List<DisplayModeList> displayModeList_OSPage = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, new List<DisplayType>() { pDisplayType });
            List<DisplayMode> dispModes = displayModeList_OSPage.Where(dML => dML.display == pDisplayType).Select(dML => dML.supportedModes).FirstOrDefault();

            // Intermediate Mode is considered for Operation
            List<DisplayMode> dispModesForOperation = new List<DisplayMode>();
            dispModesForOperation.Add(dispModes.ElementAt(dispModes.Count / 2));

            if (_considerMinRes)
                dispModesForOperation.Add(dispModes.First());

            return dispModesForOperation;
        }
        protected void CheckCorruptionViaDVMU(DisplayType argDispType)
        {
            if (this._Corruption != null)
            {
                if (base.MachineInfo.PlatformDetails.Platform != Platform.VLV)
                {
                    if (argDispType == DisplayType.HDMI)
                    {
                        string fileName = GetDisplayModeToString(argDispType);
                        //hides taskbar          
                        SetUpDesktopArgs desktopArgs = new SetUpDesktopArgs(SetUpDesktopArgs.SetUpDesktopOperation.HideTaskBar);
                        AccessInterface.SetFeature<bool, SetUpDesktopArgs>(Features.SetUpDesktop, Action.SetMethod, desktopArgs);

                        HotPlugUnplug obj = new HotPlugUnplug();
                        obj.FunctionName = FunctionName.CaptureFrame;
                        obj.FrameFileName = fileName;
                        AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, obj);

                        Log.Message(true, "Compare Image");
                        ImageProcessingParams imageParams = new ImageProcessingParams();
                        imageParams.ImageProcessingOption = ImageProcessOptions.CompareImages;
                        imageParams.SourceImage = base.ApplicationManager.ApplicationSettings.HDMIGoldenImage + "\\" + fileName + ".bmp";
                        imageParams.TargetImage = fileName + ".bmp";

                        if (AccessInterface.SetFeature<bool, ImageProcessingParams>(Features.ImageProcessing, Action.SetMethod, imageParams))
                        {
                            Log.Success("Image Capture Done, and match with golden image");
                        }
                        else
                        {
                            Log.Fail("Image does not match with golden");
                        }
                    }
                }
            }
        }
        protected string GetDisplayModeToString(DisplayType argDispType)
        {
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDispType).First();
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);

            string modeStr = string.Concat(actualMode.display, "_", actualMode.HzRes, "_", actualMode.VtRes, "_", actualMode.RR, actualMode.InterlacedFlag.Equals(0) ? "p_Hz" : "i_Hz", "_", actualMode.Bpp, "_Bit", "_", actualMode.Angle, "_Deg");
            if (null != actualMode.ScalingOptions && !actualMode.ScalingOptions.Count.Equals(0))
                modeStr = string.Concat(modeStr, "_", (ScalingOptions)actualMode.ScalingOptions.First());
            return modeStr;
        }

        protected bool ApplyConfigOS(DisplayConfig argDispConfig)
        {
            bool status = true;
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            else
            {
                status = false;
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());
            }
            return status;
        }
        protected bool VerifyConfigOS(DisplayConfig argDisplayConfig)
        {
            bool status = true;
            Log.Message(true, "Verifying config {0} via OS", argDisplayConfig.GetCurrentConfigStr());
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            if (currentConfig.GetCurrentConfigStr().Equals(argDisplayConfig.GetCurrentConfigStr()))
            {
                Log.Success("{0} is verified by OS", argDisplayConfig.GetCurrentConfigStr());
            }
            else
            {
                status = false;
                Log.Fail("Config {0} does not match with current config {1}", currentConfig.GetCurrentConfigStr(), argDisplayConfig.GetCurrentConfigStr());
            }
            return status;
        }
    } // End SB_Scaling_DisplayConfig
}