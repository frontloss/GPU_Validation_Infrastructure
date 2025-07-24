using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using System.Text.RegularExpressions;

namespace Intel.VPG.Display.Automation
{
    public class SB_Overlay_Base:TestBase
    {
        protected const string OVERLAY_ENABLE = "OVERLAY_ENABLE";

        protected void ApplyConfig(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());
        }
        public virtual void VerifyConfig(DisplayConfig argDisplayConfig)
        {
            Log.Message(true, "Verifying config {0}", argDisplayConfig.GetCurrentConfigStr());
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            if (currentConfig.GetCurrentConfigStr().Equals(argDisplayConfig.GetCurrentConfigStr()))
            {
                Log.Success("{0} is verified.", argDisplayConfig.GetCurrentConfigStr());
            }
            else
                Log.Fail("Config {0} does not match with current config {1}", currentConfig.GetCurrentConfigStr(), argDisplayConfig.GetCurrentConfigStr());
        }
        
        protected void PlayAndMoveVideo(DisplayHierarchy displayHierarchy, DisplayConfig displayConfig)
        {
            base.OverlayOperations(displayHierarchy, displayConfig,OverlayPlaybackOptions.MovePlayer);
        }
        protected void StopVideo()
        {
            base.OverlayOperations(DisplayHierarchy.Unsupported, base.CurrentConfig, OverlayPlaybackOptions.ClosePlayer);
        }
        protected void FullScreen(DisplayHierarchy displayHierarchy, DisplayConfig displayConfig)
        {
            base.OverlayOperations(displayHierarchy, displayConfig, OverlayPlaybackOptions.FullScreen);
        }

       
        protected uint ReadRegister(string pRegisterEvent, PIPE pPipe, PLANE pPlane, PORT pPort)
        {
            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = pPipe;
            eventInfo.plane = pPlane;
            eventInfo.port = pPort;
            eventInfo.eventName = pRegisterEvent;
            
            Log.Verbose("Event being checked = {0}", eventInfo.eventName);
            EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);


            if (returnEventInfo.listRegisters.Count == 0)
                Log.Fail("Unable to fetch registers for event " + pRegisterEvent);

            foreach (RegisterInf reginfo in returnEventInfo.listRegisters)
            {
                DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
                driverData.input = Convert.ToUInt32(reginfo.Offset, 16);
                uint bitmap = Convert.ToUInt32(reginfo.Bitmap, 16);
                DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
                
                if (!AccessInterface.SetFeature<bool, DriverEscapeParams>(Features.DriverEscape, Action.SetMethod, driverParams))
                    Log.Abort("Failed to read Register with offset as {0}", driverData.input);
                else
                    Log.Message("Offset: {0} Bitmap: {1}  Value from registers = {2}", reginfo.Offset, reginfo.Bitmap, driverData.output.ToString("X"));

                return GetRegisterValue(driverData.output, bitmap);
            }

            return 0;
        }

        protected void VerifyRegisterForDisplay(DisplayType display, bool isSecondaryTernary, bool printStatus = false)
        {
            DisplayInfo displayInfo = this.CurrentConfig.EnumeratedDisplays.Find(dispInfo => dispInfo.DisplayType == display);
            PipePlaneParams pipePlaneObject = new PipePlaneParams(display);
            PipePlaneParams pipePlaneParams = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlaneObject);

            if (base.VerifyRegisters(OVERLAY_ENABLE, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, printStatus))
            {
                Log.Success("Overlay is running on display: {0}", display);
                CheckWatermark(display);
            }
            else
            {
                if (isSecondaryTernary)
                {
                    Log.Success("Overlay is not running on display: {0}", display);
                    CheckWatermark(display);
                }
                else
                    Log.Fail("Overlay is not running on display: {0}", display);
            }
        }
        protected void VerifyRegistersForDisplay(DisplayType display, bool isOverlayRunning)
        {
            DisplayInfo displayInfo = this.CurrentConfig.EnumeratedDisplays.Find(dispInfo => dispInfo.DisplayType == display);
            PipePlaneParams pipePlaneObject = new PipePlaneParams(display);
            PipePlaneParams pipePlaneParams = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlaneObject);

            bool currentStatus = base.VerifyRegisters(OVERLAY_ENABLE, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, false);

            if (currentStatus)
            {
                if (isOverlayRunning)
                {
                    Log.Success("Overlay is enabled on display: {0}", display);
                    CheckWatermark(display);
                }
                else
                    Log.Fail("Overlay is enabled on display: {0}", display);
            }
            else
            {
                if (!isOverlayRunning)
                {
                    Log.Success("Overlay is not enabled on display: {0}", display);
                    CheckWatermark(display);
                }
                else
                    Log.Fail("Overlay is not enabled on display: {0}", display);
            }
        }

        private uint GetRegisterValue(uint regValue, uint regBitmap)
        {
            int count = 0;
            string bitvalue = regBitmap.ToString("X");
            while (bitvalue.EndsWith("0") != false)
            {
                bitvalue = bitvalue.Substring(0, bitvalue.Length - 1);
                count++;
            }

            regValue &= regBitmap;
            string currentValue = regValue.ToString("X");
            if (currentValue != "0")
                currentValue = currentValue.Substring(0, currentValue.Length - count);

            return Convert.ToUInt32(currentValue, 16);
        }
       
        protected List<DisplayModeList> GetMinModeForConfig(List<DisplayType> argDisplayType, DisplayUnifiedConfig argConfigType)
        {
            List<DisplayModeList> allModeList = GetAllRsolutionAbove10_7(argDisplayType);
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
            List<DisplayModeList> allModeList = GetAllRsolutionAbove10_7(argDisplayType); 
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
            List<DisplayModeList> allModeList = GetAllRsolutionAbove10_7(argDisplayType);
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

        protected void ApplyMode(DisplayMode argSelectedMode, DisplayType argDisplayType)
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

        protected List<DisplayModeList> GetAllRsolutionAbove10_7(List<DisplayType> argDisplayType)
        {
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, argDisplayType);
           
            for (int indexprod = 0; indexprod < allModeList.Count; indexprod++)
            {
                for (int index = 0; index < allModeList[indexprod].supportedModes.Count; index++)
                {
                    if (allModeList[indexprod].supportedModes[index].HzRes < 1024 || allModeList[indexprod].supportedModes[index].VtRes < 768)
                    {

                        allModeList[indexprod].supportedModes.Remove(allModeList[indexprod].supportedModes[index]);
                        index--;
                    }
                }
            }

            return allModeList;
        }
    }
}
    