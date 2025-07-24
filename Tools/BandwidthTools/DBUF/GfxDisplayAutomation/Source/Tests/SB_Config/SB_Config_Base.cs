namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    using System.Text.RegularExpressions;
    public class SB_Config_Base : TestBase
    {
       protected List<DisplayType> _pluggableDisplays  = null;
       protected Dictionary<DisplayType, string> _availableDisplays = null;
       public SB_Config_Base()
       {
           _pluggableDisplays = new List<DisplayType>();
           _availableDisplays = new Dictionary<DisplayType, string>();

           _availableDisplays.Add(DisplayType.HDMI, "HDMI_DELL.EDID");
           _availableDisplays.Add(DisplayType.HDMI_2, "HDMI_Dell_3011.EDID");
           _availableDisplays.Add(DisplayType.DP, "DP_3011.EDID");
           _availableDisplays.Add(DisplayType.DP_2, "DP_HP_ZR2240W.EDID");
       }
        protected System.Action<DisplayType> _Corruption = null;
        protected void ApplyConfigOS(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());
        }
        public virtual void VerifyConfigOS(DisplayConfig argDisplayConfig)
        {
            Log.Message(true, "Verifying config {0} via OS", argDisplayConfig.GetCurrentConfigStr());
            
            DisplayInfo priDisplayInfo = base.EnumeratedDisplays.Where(cI => cI.DisplayType == argDisplayConfig.PrimaryDisplay).FirstOrDefault();

            if ( argDisplayConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone
                && base.MachineInfo.PlatformDetails.IsLowpower
                && priDisplayInfo.IsPortraitPanel == true
                && (!base.MachineInfo.OS.IsGreaterThan(OSType.WINTHRESHOLD))
                && priDisplayInfo.displayExtnInformation.Equals(DisplayExtensionInfo.Internal))
            {
                Log.Alert("{0} This Configuration Is Not Applicable",argDisplayConfig);
            }
            else
            {
                DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
                if (currentConfig.GetCurrentConfigStr().Equals(argDisplayConfig.GetCurrentConfigStr()))
                {
                    Log.Success("{0} is verified by OS", argDisplayConfig.GetCurrentConfigStr());
                    if (argDisplayConfig.DisplayList.Contains(DisplayType.HDMI))
                        CheckCorruptionViaDVMU(DisplayType.HDMI);
                }
                else
                    Log.Fail("Config {0} does not match with current config {1}", currentConfig.GetCurrentConfigStr(), argDisplayConfig.GetCurrentConfigStr());
            }
        }
        protected void VerifyModeOS(DisplayMode argSelectedMode, DisplayType argDisplayType)
        {
            Log.Message(true, "Verify the selected mode got applied for {0} through OS", argDisplayType);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplayType).First();
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            if (actualMode.GetCurrentModeStr(true).Equals(argSelectedMode.GetCurrentModeStr(true)))
            {
                Log.Success("Mode {0} is verified for {1}", actualMode.GetCurrentModeStr(false), argDisplayType);
                CheckCorruptionViaDVMU(argDisplayType);
            }
            else
                Log.Fail("Mode chosen {0} is not applied for {1}! Actual is {2}", argSelectedMode.GetCurrentModeStr(false), argDisplayType, actualMode.GetCurrentModeStr(false));
        }
        protected DisplayMode GetAppliedMode(DisplayType argDisplayType)
        {
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplayType).First();
            DisplayMode currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            return currentMode;
        }
        protected void VerifyConfigCUI(DisplayConfig argDispConfig)
        {
            Log.Message(true, "Verifying config {0} via CUI", argDispConfig.GetCurrentConfigStr());
            DisplayConfig curConfig = AccessInterface.GetFeature<DisplayConfig>(Features.SDKConfig, Action.Get);
            if (argDispConfig.GetCurrentConfigStr() == curConfig.GetCurrentConfigStr())
            {
                Log.Success("The config {0} is verified by CUI", curConfig.GetCurrentConfigStr());
            }
            else
            {
                Log.Fail("The config {0} does not match with that in CUI {1}", argDispConfig.GetCurrentConfigStr(), curConfig.GetCurrentConfigStr());
            }
        }
        protected void CheckCorruptionViaDVMU(DisplayType argDispType)
        {
            if (this._Corruption != null)
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
        protected string GetDisplayModeToString(DisplayType argDispType)
        {
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDispType).First();
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);

            string modeStr = string.Concat(actualMode.display, "_", actualMode.HzRes, "_", actualMode.VtRes, "_", actualMode.RR, actualMode.InterlacedFlag.Equals(0) ? "p_Hz" : "i_Hz", "_", actualMode.Bpp, "_Bit", "_", actualMode.Angle, "_Deg");
            if (null != actualMode.ScalingOptions && !actualMode.ScalingOptions.Count.Equals(0))
                modeStr = string.Concat(modeStr, "_", (ScalingOptions)actualMode.ScalingOptions.First());
            return modeStr;
        }        
        #region Modes

        protected List<DisplayModeList> GetDiffRefreshRate(List<DisplayModeList> allModeList, List<DisplayMode> argmodeList)
        {
            List<DisplayModeList> modesList = new List<DisplayModeList>();
            Dictionary<DisplayType, List<uint>> commonRR = new Dictionary<DisplayType, List<uint>>();
            argmodeList.ForEach(curDisp =>
            {
                List<DisplayMode> dispModes = allModeList.Where(dI => dI.display == curDisp.display).Select(dI => dI.supportedModes).FirstOrDefault();
                List<uint> RefreshRateListOS = dispModes.Where(dI => dI.HzRes == curDisp.HzRes && dI.VtRes == curDisp.VtRes).Select(dI => dI.RR).ToList();
                commonRR.Add(curDisp.display, RefreshRateListOS);
            });
            Dictionary<DisplayType, uint> displayRR = new Dictionary<DisplayType, uint>();
            if (commonRR.Count() == 1)
            {
                //single display
                displayRR.Add(commonRR.First().Key, commonRR.First().Value.ElementAt(commonRR.First().Value.Count() / 2));
            }
            else
            {
                int count = 0;
                while (count < commonRR.Count())
                {
                    if (count != commonRR.Count() - 1)
                    {
                        List<uint> uniqueRR = commonRR.ElementAt(count).Value.Except(commonRR.ElementAt(count + 1).Value).ToList();
                        if (uniqueRR.Count() != 0)
                            displayRR.Add(commonRR.ElementAt(count).Key, uniqueRR.First());
                        else
                            displayRR.Add(commonRR.ElementAt(count).Key, commonRR.ElementAt(count).Value.First());
                    }
                    else
                    {
                        List<uint> uniqueRR = commonRR.ElementAt(count).Value.Except(commonRR.First().Value).ToList();
                        if (uniqueRR.Count() != 0)
                            displayRR.Add(commonRR.ElementAt(count).Key, uniqueRR.First());
                        else
                            displayRR.Add(commonRR.ElementAt(count).Key, commonRR.ElementAt(count).Value.First());
                    }
                    count++;
                }
            }
            foreach (DisplayType curDisp in displayRR.Keys)
            {
                DisplayMode dispMode = argmodeList.Where(dI => dI.display == curDisp).FirstOrDefault();
                List<DisplayMode> dispModeList = new List<DisplayMode>();
                dispModeList = allModeList.Where(dI => dI.display == curDisp).Select(dI => dI.supportedModes).FirstOrDefault();
                dispModeList.ForEach(curMode =>
                {
                    if (curMode.HzRes == dispMode.HzRes && curMode.VtRes == dispMode.VtRes && curMode.RR == displayRR[curDisp] && curMode.Bpp == dispMode.Bpp)
                    {
                        DisplayModeList curModeList = new DisplayModeList();
                        curModeList.display = curMode.display;
                        curModeList.supportedModes = new List<DisplayMode>();
                        curModeList.supportedModes.Add(curMode);
                        modesList.Add(curModeList);
                    }
                });

            }
            return modesList;
        }

        protected List<DisplayModeList> GetMinModeForConfig(List<DisplayType> argDisplayType, DisplayUnifiedConfig argConfigType)
        {
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, argDisplayType);
            List<DisplayMode> minModeList = new List<DisplayMode>();
            if (argConfigType == DisplayUnifiedConfig.Clone)
            {
                List<uint> resolution = GetCommonResolutionListForClone(allModeList, (float)0.0);
                uint hzRes = resolution.First();
                uint vtRes = resolution.Last();

                allModeList.ForEach(curDisp =>
                {
                    if (curDisp == allModeList.Last() && base.MachineInfo.OS.Type == OSType.WIN7)
                    {
                        DisplayMode curMode = curDisp.supportedModes.Where(dI => dI.Bpp == 16 && dI.HzRes == hzRes && dI.VtRes == vtRes).FirstOrDefault();
                        if (curMode.Bpp != 0)
                            minModeList.Add(curMode);
                        else
                        {
                            curMode = curDisp.supportedModes.Where(dI => dI.HzRes == hzRes && dI.VtRes == vtRes).FirstOrDefault();
                            if (curMode.Bpp != 0)
                                minModeList.Add(curMode);
                        }
                    }
                    else
                    {
                        DisplayMode curMode = curDisp.supportedModes.Where(dI => dI.HzRes == hzRes && dI.VtRes == vtRes).FirstOrDefault();
                        if (curMode.Bpp != 0)
                            minModeList.Add(curMode);
                    }
                });
            }
            else
            {
                allModeList.ForEach(curDisp =>
                {
                    if (curDisp == allModeList.First() && base.MachineInfo.OS.Type == OSType.WIN7)
                    {
                        DisplayMode curMode = curDisp.supportedModes.Where(dI => dI.Bpp == 16).FirstOrDefault();
                        if (curMode.Bpp != 0)
                            minModeList.Add(curMode);
                        else
                            minModeList.Add(curDisp.supportedModes.First());
                    }
                    else
                    {
                        minModeList.Add(curDisp.supportedModes.First());
                    }
                });
            }
            return GetDiffRefreshRate(allModeList, minModeList);
        }
        protected List<DisplayModeList> GetMaxModeForConfig(List<DisplayType> argDisplayType, DisplayUnifiedConfig argConfigType)
        {
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, argDisplayType);
            List<DisplayMode> maxModeList = new List<DisplayMode>();
            if (argConfigType == DisplayUnifiedConfig.Clone)
            {
                List<uint> resolution = GetCommonResolutionListForClone(allModeList, (float)1.0);
                uint hzRes = resolution.First();
                uint vtRes = resolution.Last();

                allModeList.ForEach(curDisp =>
                {
                    if (curDisp == allModeList.Last() && base.MachineInfo.OS.Type == OSType.WIN7)
                    {
                        DisplayMode curMode = curDisp.supportedModes.Where(dI => dI.Bpp == 16 && dI.HzRes == hzRes && dI.VtRes == vtRes).FirstOrDefault();
                        if (curMode.Bpp != 0)
                            maxModeList.Add(curMode);
                        else
                        {
                            curMode = curDisp.supportedModes.Where(dI => dI.HzRes == hzRes && dI.VtRes == vtRes).FirstOrDefault();
                            if (curMode.Bpp != 0)
                                maxModeList.Add(curMode);
                        }
                    }
                    else
                    {
                        DisplayMode curMode = curDisp.supportedModes.Where(dI => dI.HzRes == hzRes && dI.VtRes == vtRes).FirstOrDefault();
                        if (curMode.Bpp != 0)
                            maxModeList.Add(curMode);
                    }
                });
            }
            else
            {
                allModeList.ForEach(curDisp =>
                {
                    if (curDisp == allModeList.Last() && base.MachineInfo.OS.Type == OSType.WIN7)
                    {
                        curDisp.supportedModes.Reverse();
                        DisplayMode curMode = curDisp.supportedModes.Where(dI => dI.Bpp == 16).FirstOrDefault();
                        if (curMode.Bpp != 0)
                            maxModeList.Add(curMode);
                        else
                            maxModeList.Add(curDisp.supportedModes.Last());
                    }
                    else
                    {
                        maxModeList.Add(curDisp.supportedModes.Last());
                    }

                });
            }

            return GetDiffRefreshRate(allModeList, maxModeList);
        }
        protected List<DisplayModeList> GetIntermediateModeForConfig(List<DisplayType> argDisplayType, DisplayUnifiedConfig argConfigType)
        {
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, argDisplayType);
            List<DisplayMode> intermediateModeList = new List<DisplayMode>();
            if (argConfigType == DisplayUnifiedConfig.Clone)
            {
                List<uint> resolution = GetCommonResolutionListForClone(allModeList, (float)0.5);
                uint hzRes = resolution.First();
                uint vtRes = resolution.Last();

                allModeList.ForEach(curDisp =>
                {
                    if (curDisp == allModeList.ElementAt(allModeList.Count() / 2) && base.MachineInfo.OS.Type == OSType.WIN7)
                    {
                        DisplayMode curMode = curDisp.supportedModes.Where(dI => dI.Bpp == 16 && dI.HzRes == hzRes && dI.VtRes == vtRes).FirstOrDefault();
                        if (curMode.Bpp != 0)
                            intermediateModeList.Add(curMode);
                        else
                        {
                            curMode = curDisp.supportedModes.Where(dI => dI.HzRes == hzRes && dI.VtRes == vtRes).FirstOrDefault();
                            if (curMode.Bpp != 0)
                                intermediateModeList.Add(curMode);
                        }
                    }
                    else
                    {
                        DisplayMode curMode = curDisp.supportedModes.Where(dI => dI.HzRes == hzRes && dI.VtRes == vtRes).FirstOrDefault();
                        if (curMode.Bpp != 0)
                            intermediateModeList.Add(curMode);
                    }
                });
            }
            else
            {
                allModeList.ForEach(curDisp =>
                {
                    if (curDisp == allModeList.ElementAt(allModeList.Count() / 2) && base.MachineInfo.OS.Type == OSType.WIN7)
                    {
                        uint minHzres = curDisp.supportedModes.First().HzRes;
                        uint minVtres = curDisp.supportedModes.First().VtRes;
                        DisplayMode curMode = curDisp.supportedModes.Where(dI => dI.HzRes != minHzres && dI.VtRes != minVtres && dI.Bpp == 16).FirstOrDefault();
                        if (curMode.Bpp != 0)
                            intermediateModeList.Add(curMode);
                        else
                            intermediateModeList.Add(curDisp.supportedModes.ElementAt(curDisp.supportedModes.Count() / 2));
                    }
                    else
                    {
                        intermediateModeList.Add(curDisp.supportedModes.ElementAt(curDisp.supportedModes.Count() / 2));
                    }
                });
            }
            return GetDiffRefreshRate(allModeList, intermediateModeList);
        }
        protected List<uint> GetCommonResolutionListForClone(List<DisplayModeList> argAllModeList, float argIndex)
        {
            Dictionary<DisplayType, List<string>> commonResolution = new Dictionary<DisplayType, List<string>>();
            argAllModeList.ForEach(curDisp =>
            {
                List<string> curDispResolution = new List<string>();
                curDisp.supportedModes.ForEach(curMode =>
                {
                    string curRes = curMode.HzRes + " x " + curMode.VtRes;
                    if (!curDispResolution.Contains(curRes))
                        curDispResolution.Add(curRes);
                });
                commonResolution.Add(curDisp.display, curDispResolution);
            });
            List<string> resultResolution = new List<string>();
            resultResolution = commonResolution.First().Value;
            foreach (DisplayType curDisp in commonResolution.Keys)
            {
                resultResolution = resultResolution.Intersect(commonResolution[curDisp]).ToList();
            }
            int index = (int)(argIndex * resultResolution.Count());
            if (index == resultResolution.Count())
                index--;
            string resolution = resultResolution.ElementAt(index);
            uint hZres = Convert.ToUInt32(Regex.Match(resolution, @"\d+").Value);
            uint vTres = Convert.ToUInt32(resolution.Split('x').Last().Trim());
            return new List<uint>() { hZres, vTres };
        }
        protected void ApplyModeOS(DisplayMode argSelectedMode, DisplayType argDisplayType)
        {
            Log.Message(true, "Set supported mode {0} for {1}", argSelectedMode.GetCurrentModeStr(false), argDisplayType);
            argSelectedMode.display = argDisplayType;
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argSelectedMode))
                Log.Success("Mode applied Successfully");
            else
                Log.Fail("Fail to apply Mode");
        }
       
        protected DisplayHierarchy GetDispHierarchy(List<DisplayType> argCustomDisplayList, DisplayType argDisplayType)
        {
            int index = argCustomDisplayList.FindIndex(dT => dT != DisplayType.None && dT == argDisplayType);
            switch (index)
            {
                case 0:
                    return DisplayHierarchy.Display_1;
                case 1:
                    return DisplayHierarchy.Display_2;
                case 2:
                    return DisplayHierarchy.Display_3;
                case 3:
                    return DisplayHierarchy.Display_4;
                case 4:
                    return DisplayHierarchy.Display_5;
                default:
                    return DisplayHierarchy.Unsupported;
            }
        }
        protected void PlayAndMoveVideo(DisplayHierarchy displayHierarchy, DisplayConfig displayConfig)
        {
            base.OverlayOperations(displayHierarchy, displayConfig, OverlayPlaybackOptions.MovePlayer);
        }
        protected void FullScreenVideo(DisplayHierarchy displayHierarchy, DisplayConfig displayConfig)
        {
            base.OverlayOperations(displayHierarchy, displayConfig, OverlayPlaybackOptions.MovePlayer);
        }
        protected void StopVideo(DisplayHierarchy displayHierarchy, DisplayConfig displayConfig)
        {
            base.OverlayOperations(displayHierarchy, displayConfig, OverlayPlaybackOptions.ClosePlayer);
        }
        protected void MoveCursor(DisplayHierarchy displayHierarchy, DisplayConfig currentConfig, DisplayType disp)
        {
            
            MoveCursorPos moveTo = new MoveCursorPos()
            {
                displayType = disp,
                displayHierarchy = displayHierarchy,
                currentConfig = currentConfig
            };
            if(AccessInterface.SetFeature<bool, MoveCursorPos>(Features.MoveCursor, Action.SetMethod, moveTo))
                Log.Message(true, "Moved Cursor to display {0}", disp);
        }
        protected void PlugDisplays()
        {
            base.CurrentConfig.PluggableDisplayList.ForEach(curDisp =>
            {
                base.HotPlug(curDisp, _availableDisplays[curDisp]);
                _pluggableDisplays.Add(curDisp);
            });
        }
        protected void UnPlugDisplays()
        {
            base.CurrentConfig.PluggableDisplayList.ForEach(curDisp =>
            {
                base.HotUnPlug(curDisp);
            });
            base.CleanUpHotplugFramework();
        }
        #endregion
    }
}
