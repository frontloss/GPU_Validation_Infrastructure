namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System;
    using System.Text.RegularExpressions;
    using System.Runtime.InteropServices;
    public class SB_MODES_Base : TestBase
    {
        protected System.Action<DisplayType> _Corruption = null;
        protected List<DisplayType> _semiAutomatedDispList = null;
        protected Dictionary<DisplayType, string> _defaultEDIDMap = null;
        public SB_MODES_Base()
        {
            _semiAutomatedDispList = new List<DisplayType>() { DisplayType.CRT, DisplayType.DP, DisplayType.DP_2 };

            _defaultEDIDMap = new Dictionary<DisplayType, string>();
            _defaultEDIDMap.Add(DisplayType.HDMI, "HDMI_DELL.EDID");
            _defaultEDIDMap.Add(DisplayType.HDMI_2, "HDMI_Dell_3011.EDID");

            _defaultEDIDMap.Add(DisplayType.DP, "DP_3011.EDID");
            _defaultEDIDMap.Add(DisplayType.DP_2, "DP_HP_ZR2240W.EDID");
        }

        protected List<DisplayModeList> GetAllModes(List<DisplayType> argCustomDisplayList)
        {
            List<DisplayModeList> listDisplayMode = new List<DisplayModeList>();
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, argCustomDisplayList);
            List<DisplayMode> commonModes = null;

            if (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
            {
                commonModes = allModeList.Where(dML => dML.display == base.CurrentConfig.PrimaryDisplay).Select(dML => dML.supportedModes).FirstOrDefault();
                allModeList.Skip(1).ToList().ForEach(dML => commonModes = commonModes.Intersect(dML.supportedModes, new DisplayMode()).ToList());
                if (commonModes.Count() > 0)
                    listDisplayMode.Add(new DisplayModeList() { display = base.CurrentConfig.PrimaryDisplay, supportedModes = commonModes });
            }
            else
                listDisplayMode = allModeList;
            return listDisplayMode;
        }
        protected void ApplyConfigOS(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());
        }
        public virtual bool VerifyConfigOS(DisplayConfig argDisplayConfig)
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
        protected void ApplyConfigCUI(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.SDKConfig, Action.SetMethod, argDispConfig))
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());
        }
        protected void ApplyModeOS(DisplayMode argSelectedMode, DisplayType argDisplayType)
        {
            Log.Message(true, "Set supported mode {0} for {1}", argSelectedMode.GetCurrentModeStr(false), argDisplayType);
            argSelectedMode.display = argDisplayType;
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argSelectedMode))
            {
                Log.Success("Mode applied Successfully");
            }
            else
                Log.Fail("Fail to apply Mode");
        }
        protected DisplayMode GetModeCUI(DisplayType argDisplayType)
        {
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplayType).First();
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            return actualMode;
        }
        protected void VerifyModeOS(DisplayMode argSelectedMode, DisplayType argDisplayType)
        {
            Log.Message(true, "Verify the  mode  for {0} through OS", argDisplayType);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplayType).First();
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            if (actualMode.GetCurrentModeStr(true).Equals(argSelectedMode.GetCurrentModeStr(true)))
            {
                Log.Success("Mode {0} is verified for {1}", actualMode.GetCurrentModeStr(false), argDisplayType);
                CheckWatermark(argDisplayType);
                CheckCorruptionViaDVMU(argDisplayType);
                CheckCorruptionViaPortCRC(argDisplayType);
            }
            else
                Log.Fail("Mode chosen {0} is not applied for {1}! Actual is {2}", argSelectedMode.GetCurrentModeStr(false), argDisplayType, actualMode.GetCurrentModeStr(false));
        }

        protected List<DisplayModeList> GetDiffRefreshRate(List<DisplayModeList> allModeList, List<DisplayMode> argmodeList)
        {
            List<DisplayModeList> modesList = new List<DisplayModeList>();
            Dictionary<DisplayType, List<uint>> commonRR = new Dictionary<DisplayType, List<uint>>();
            argmodeList.ForEach(curDisp =>
            {
                List<DisplayMode> dispModes = allModeList.Where(dI => dI.display == curDisp.display).Select(dI => dI.supportedModes).FirstOrDefault();
                List<uint> RefreshRateListOS = dispModes.Where(dI => dI.HzRes == curDisp.HzRes && dI.VtRes == curDisp.VtRes).Select(dI => dI.RR).ToList();
                //string res = curDisp.HzRes + " x " + curDisp.VtRes;
                //List<uint> cuiRR = GetRefreshRateListFromCUI(curDisp.display, res);
                //List<uint> dispCommonRR = RefreshRateListOS.Intersect(cuiRR).ToList();
                //if (dispCommonRR.Count() != 0)
                //    commonRR.Add(curDisp.display, dispCommonRR);
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
        protected void UnplugSemiautomated(string argSemiAutomated)
        {
            Log.Message(true, "{0} semi automated", argSemiAutomated);
            AccessInterface.SetFeature<bool, string>(Features.PromptMessage, Action.SetMethod, argSemiAutomated);
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

        protected void CheckCorruptionViaPortCRC(DisplayType argDispType)
        {
            if (this.ApplicationManager.ApplicationSettings.CheckCorruption == true)
            {
                if (argDispType == DisplayType.HDMI || argDispType == DisplayType.DP || argDispType == DisplayType.EDP)
                {
                    CRCComputation(argDispType);
                }
            }
        }

        protected void CRCComputation(DisplayType display)
        {
            VerifyCRCArgs driverParams = new VerifyCRCArgs();
            driverParams.display = display;
            driverParams.currentConfig = base.CurrentConfig;

            //Port CRC verification
            AccessInterface.GetFeature<bool, VerifyCRCArgs>(Features.VerifyCRC, Action.GetMethod, Source.AccessAPI, driverParams);

            System.Threading.Thread.Sleep(10000);

            //computing Pipe CRC verification.
            driverParams.ComputePipeCRC = true;
            AccessInterface.GetFeature<bool, VerifyCRCArgs>(Features.VerifyCRC, Action.GetMethod, Source.AccessAPI, driverParams);
                
        }

        //protected void CRCComputation(DisplayType display)
        //{
        //    uint currentCRC = 0;
        //    uint pipeCRC = 0;
        //    uint goldenCRC = 0;

        //    DisplayInfo curDispInfo = base.CurrentConfig.EnumeratedDisplays.Where(di => di.DisplayType == display).FirstOrDefault();
        //    DisplayMode curDispMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, curDispInfo);

        //    if (curDispMode.InterlacedFlag == 1)
        //    {
        //        Log.Alert("Skipping corruption check for Interlaced mode: {0}", curDispMode.GetCurrentModeStr(false));
        //        return;
        //    }

        //    SetUpDesktopArgs driverParams = new SetUpDesktopArgs(SetUpDesktopArgs.SetUpDesktopOperation.PrepareDesktop);
        //    driverParams.display = display;
        //    driverParams.currentConfig = base.CurrentConfig;
        //    driverParams.displayMode = curDispMode;

        //    if (!AccessInterface.SetFeature<bool, SetUpDesktopArgs>(Features.SetUpDesktop, Action.SetMethod, driverParams))
        //        Log.Fail("Failed to Prepare Desktop.");
        //    else
        //    {
        //        //verifying Port CRC.
        //        if (GetGoldenCRC(curDispInfo, curDispMode, false, ref goldenCRC))
        //        {
        //            GetCRC(display, curDispInfo.Port, false, ref currentCRC);

        //            if (currentCRC == 0 || goldenCRC == 0)
        //                Log.Fail("CRC should not be zero. Expected:{0}, Current CRC:{1}.", goldenCRC, currentCRC);
        //            else
        //            {
        //                if (currentCRC == goldenCRC)
        //                {
        //                    Log.Success("Port CRC Matched for {0}", curDispMode.GetCurrentModeStr(false));
        //                }
        //                else
        //                {
        //                    Log.Alert("Port CRC mismatch. Sleep for 10sec and compute crc again.");
        //                    System.Threading.Thread.Sleep(10000);

        //                    GetCRC(display, curDispInfo.Port, false, ref currentCRC);

        //                    if (currentCRC == 0 || goldenCRC == 0)
        //                        Log.Fail("CRC should not be zero. Expected:{0}, Current CRC:{1}.", goldenCRC, currentCRC);
        //                    else
        //                    {
        //                        if (currentCRC == goldenCRC)
        //                        {
        //                            Log.Success("Port CRC Matched for {0}", curDispMode.GetCurrentModeStr(false));
        //                        }
        //                        else
        //                        {
        //                            Log.Fail("Port CRC Not Matched. Expected:0x{0}, Current CRC:0x{1} for {2}: {3}", goldenCRC.ToString("X"), currentCRC.ToString("X"), curDispMode.display, curDispMode.GetCurrentModeStr(false));
        //                        }
        //                    }
        //                    //Log.Fail("CRC Not Matched. Expected:0x{0}, Current CRC:0x{1} for {2}: {3}", goldenCRC.ToString("X"), currentCRC.ToString("X"), curDispMode.display, curDispMode.GetCurrentModeStr(false));
        //                }
        //            }
        //        }
        //        else
        //            Log.Fail("Golden CRC not available for {0}", curDispMode.GetCurrentModeStr(false));


        //        driverParams = new SetUpDesktopArgs(SetUpDesktopArgs.SetUpDesktopOperation.RestoreDesktop);
        //        if (!AccessInterface.SetFeature<bool, SetUpDesktopArgs>(Features.SetUpDesktop, Action.SetMethod, driverParams))
        //            Log.Fail("Failed to Restore Desktop.");
        //    }
        //}

        private void ShowMMIOFlip(DisplayMode curDispMode, bool enable)
        {
            SetUpDesktopArgs driverParams = new SetUpDesktopArgs(SetUpDesktopArgs.SetUpDesktopOperation.ShowMMIOFlip);
            driverParams.displayMode = curDispMode;

            if (enable == false)
                driverParams.FunctionName = SetUpDesktopArgs.SetUpDesktopOperation.HideMMIOFlip;

            if (!AccessInterface.SetFeature<bool, SetUpDesktopArgs>(Features.SetUpDesktop, Action.SetMethod, driverParams))
                Log.Fail("Failed to {0} MMIO Flip", enable ? "enable" : "disable");
        }
        private void EnableDisableCursor(bool enable)
        {
            SetUpDesktopArgs driverParams = new SetUpDesktopArgs(SetUpDesktopArgs.SetUpDesktopOperation.ShowCursor);
            if (enable == false)
                driverParams.FunctionName = SetUpDesktopArgs.SetUpDesktopOperation.HideCursor;

            if (!AccessInterface.SetFeature<bool, SetUpDesktopArgs>(Features.SetUpDesktop, Action.SetMethod, driverParams))
                Log.Fail("Failed to {0} Cursor", enable ? "enable" : "disable");
        }

        private bool GetCRC(DisplayType display, PORT port, bool computePipeCRC, ref uint crcValue)
        {
            bool status = true;
            CRCArgs obj = new CRCArgs();
            obj.displayType = display;
            obj.port = port;
            obj.ComputePipeCRC = computePipeCRC;
            obj = AccessInterface.GetFeature<CRCArgs, CRCArgs>(Features.CRC, Action.GetMethod, Source.AccessAPI, obj);

            crcValue = obj.CRCValue;
            
            if (crcValue == 0)
                status = false;

            return status;
        }

        private bool GetGoldenCRC(DisplayInfo curDispInfo, DisplayMode curDispMode, bool isPipeCRC, ref uint crcValue)
        {
            bool status = true;

            CrcGoldenDataArgs obj = new CrcGoldenDataArgs();
            obj.displayInfo = curDispInfo;
            obj.displayMode = curDispMode;
            obj.IsPipeCRC = isPipeCRC;
            obj = AccessInterface.GetFeature<CrcGoldenDataArgs, CrcGoldenDataArgs>(Features.CrcGoldenData, Action.GetMethod, Source.AccessAPI, obj);

            crcValue = obj.CRCValue;

            if (crcValue == 0 || obj.IsCRCPresent==false)
                status = false;

            return status;
        }
    }
}