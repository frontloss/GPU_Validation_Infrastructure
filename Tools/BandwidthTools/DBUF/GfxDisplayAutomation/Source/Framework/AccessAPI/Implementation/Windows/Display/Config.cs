namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Linq;
    using System.Threading;
    using System.Collections.Generic;

    internal class Config : FunctionalBase, ISetMethod, IParse, IGet
    {
        //SDC Flags
        const uint SDC_TOPOLOGY_INTERNAL = 0x00000001;
        const uint SDC_TOPOLOGY_CLONE = 0x00000002;
        const uint SDC_TOPOLOGY_EXTEND = 0x00000004;
        const uint SDC_TOPOLOGY_EXTERNAL = 0x00000008;
        const uint SDC_TOPOLOGY_SUPPLIED = 0x00000010;
        const uint SDC_USE_DATABASE_CURRENT = (SDC_TOPOLOGY_INTERNAL | SDC_TOPOLOGY_CLONE | SDC_TOPOLOGY_EXTEND | SDC_TOPOLOGY_EXTERNAL);
        const uint SDC_USE_SUPPLIED_DISPLAY_CONFIG = 0x00000020;
        const uint SDC_VALIDATE = 0x00000040;
        const uint SDC_APPLY = 0x00000080;
        const uint SDC_NO_OPTIMIZATION = 0x00000100;
        const uint SDC_SAVE_TO_DATABASE = 0x00000200;
        const uint SDC_ALLOW_CHANGES = 0x00000400;
        const uint SDC_PATH_PERSIST_IF_REQUIRED = 0x00000800;
        const uint SDC_FORCE_MODE_ENUMERATION = 0x00001000;
        const uint HSYNC_SDC_NUM = 4;
        const uint HSYNC_SDC_DENOM = 0;
        const UInt32 DISPLAYCONFIG_PATH_ACTIVE = 0x00000001;
        const int PRECISION3DEC = 1000;

        public bool SetMethod(object argMessage)
        {
            bool result = this.SetConfig(argMessage as DisplayConfig);
            if (!result)
            {
                Log.Sporadic(false, "Trying to apply config again!");
                result = this.SetConfig(argMessage as DisplayConfig);
            }
            return result;
        }
        public object Get
        {
            get { return GetConfig(); }
        }
        [ParseAttribute(InterfaceName = InterfaceType.ISetMethod, InterfaceData = new string[] { "DisplayConfigType:DisplayConfig:sp", "DisplayType:PrimaryDisplay:+", "DisplayType:SecondaryDisplay:+", "DisplayType:TertiaryDisplay" }, Comment = "Sets the Display configuration")]
        [ParseAttribute(InterfaceName = InterfaceType.IGet, Comment = "Gets the current display Configuration")]        
        public void Parse(string[] args)
        {
            if (args.Length.Equals(1) && args[0].ToLower().Contains("get"))
            {
                DisplayConfig currentConfig = (DisplayConfig)this.Get;
                Log.Verbose("Current System Configuration - {0} : {1} + {2} + {3}", currentConfig.ConfigType, currentConfig.PrimaryDisplay,
                    currentConfig.SecondaryDisplay, currentConfig.TertiaryDisplay);
            }
            else if (args.Length.Equals(3) && args[0].ToLower().Contains("set"))
            {
                DisplayConfig testConfig = new DisplayConfig();
                DisplayConfigType configType;
                Enum.TryParse<DisplayConfigType>(args[1], true, out configType);
                testConfig.ConfigType = configType;

                DisplayType displayType;
                testConfig.DisplayList = new List<DisplayType>();
                args[2].Split(new[] { '+', ',' }, StringSplitOptions.RemoveEmptyEntries).ToList().ForEach(d =>
                {
                    Enum.TryParse<DisplayType>(d, true, out displayType);
                    testConfig.DisplayList.Add(displayType);
                });
                testConfig.PrimaryDisplay = testConfig.DisplayList.GetDisplay(DisplayHierarchy.Display_1);
                testConfig.SecondaryDisplay = testConfig.DisplayList.GetDisplay(DisplayHierarchy.Display_2);
                testConfig.TertiaryDisplay = testConfig.DisplayList.GetDisplay(DisplayHierarchy.Display_3);

                if (this.SetMethod(testConfig))
                    Log.Success("Config set successfully");
                else
                    Log.Fail("Failed to apply config");
            }
            else
                this.HelpText();
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("Usage for a GET Operation::").Append(Environment.NewLine);
            sb.Append("..\\>Execute Config GetCurrentConfig").Append(Environment.NewLine);

            sb.Append("Usage for a SET Operation::").Append(Environment.NewLine);
            sb.Append("..\\>Execute Config SetConfiguration [ConfigType] [Displays]").Append(Environment.NewLine);
            sb.Append("[ConfigType = SD/DDC/ED/TDC/TED]").Append(Environment.NewLine);
            sb.Append("[Displays = CRT EDP DP HDMI.....]").Append(Environment.NewLine);
            Log.Verbose(sb.ToString());

        }

        private DisplayConfig GetConfig()
        {
            DisplayConfig dispConfig = new DisplayConfig();
            dispConfig.DisplayList = new List<DisplayType>();
            UInt32 numPathArrayElements = 0, numModeInfoArrayElements = 0;
            int returnVal = Interop.GetDisplayConfigBufferSizes((uint)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, ref numModeInfoArrayElements);
            DISPLAYCONFIG_PATH_INFO[] pathInfo = new DISPLAYCONFIG_PATH_INFO[numPathArrayElements];
            DISPLAYCONFIG_MODE_INFO[] modeInfo = new DISPLAYCONFIG_MODE_INFO[numModeInfoArrayElements];
            DISPLAYCONFIG_TOPOLOGY_ID topologyId = DISPLAYCONFIG_TOPOLOGY_ID.DISPLAYCONFIG_TOPOLOGY_NULL;
            returnVal = Interop.QueryDisplayConfig((UInt32)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, pathInfo,
            ref numModeInfoArrayElements, modeInfo, topologyId);
            Log.Verbose("Return value of QDC call : {0}", returnVal);
            if (returnVal != (int)QDC_SDC_StatusCode.SUCCESS)
            {
                Log.Verbose("Failed to fetch mode!");
                return dispConfig;
            }

            uint primaryWindowsId = CommonExtensions.GetMaskedWindowsId(base.AppManager.MachineInfo.OS.Type, pathInfo[0].targetInfo.id);
            if (numModeInfoArrayElements == 2 && numPathArrayElements == 1)
            {
                dispConfig.ConfigType = DisplayConfigType.SD;
                dispConfig.PrimaryDisplay = base.GetDisplayTypeByWinMonitorID(primaryWindowsId);
                dispConfig.SecondaryDisplay = DisplayType.None;
                dispConfig.TertiaryDisplay = DisplayType.None;
            }
            else if (numPathArrayElements == 2)
            {
                uint secondaryWindowsId = CommonExtensions.GetMaskedWindowsId(base.AppManager.MachineInfo.OS.Type, pathInfo[1].targetInfo.id);
                if (numModeInfoArrayElements == 3)
                {
                    dispConfig.ConfigType = DisplayConfigType.DDC;
                    dispConfig.PrimaryDisplay = base.GetDisplayTypeByWinMonitorID(primaryWindowsId);
                    dispConfig.SecondaryDisplay = base.GetDisplayTypeByWinMonitorID(secondaryWindowsId);
                    dispConfig.TertiaryDisplay = DisplayType.None;
                }
                else if(numModeInfoArrayElements == 4)
                {
                    dispConfig.ConfigType = DisplayConfigType.ED;
                    dispConfig.PrimaryDisplay = base.GetDisplayTypeByWinMonitorID(primaryWindowsId);
                    dispConfig.SecondaryDisplay = base.GetDisplayTypeByWinMonitorID(secondaryWindowsId);
                    dispConfig.TertiaryDisplay = DisplayType.None;
                }
            }
            else if (numPathArrayElements == 3)
            {
                uint secondaryWindowsId = CommonExtensions.GetMaskedWindowsId(base.AppManager.MachineInfo.OS.Type, pathInfo[1].targetInfo.id);
                uint tertiaryWindowsId = CommonExtensions.GetMaskedWindowsId(base.AppManager.MachineInfo.OS.Type, pathInfo[2].targetInfo.id);
                if (numModeInfoArrayElements == 4)
                {
                    dispConfig.ConfigType = DisplayConfigType.TDC;
                    dispConfig.PrimaryDisplay = base.GetDisplayTypeByWinMonitorID(primaryWindowsId);
                    dispConfig.SecondaryDisplay = base.GetDisplayTypeByWinMonitorID(secondaryWindowsId);
                    dispConfig.TertiaryDisplay = base.GetDisplayTypeByWinMonitorID(tertiaryWindowsId);
                }
                else if (numModeInfoArrayElements == 6) //Tri Extended Config   
                {
                    dispConfig.ConfigType = DisplayConfigType.TED;
                    dispConfig.PrimaryDisplay = base.GetDisplayTypeByWinMonitorID(primaryWindowsId);
                    dispConfig.SecondaryDisplay = base.GetDisplayTypeByWinMonitorID(secondaryWindowsId);
                    dispConfig.TertiaryDisplay = base.GetDisplayTypeByWinMonitorID(tertiaryWindowsId);
                }
            }
            return dispConfig;
        }

        private bool SetConfig(DisplayConfig dispCfg)
        {
            DisplayMode resolution = new DisplayMode();
            resolution.HzRes = 1024;
            resolution.VtRes = 768;
            resolution.RR = 60;
            resolution.Bpp = 32;
            resolution.InterlacedFlag = 0;
            
            DisplayInfo priDisplayInfo = base.EnumeratedDisplays.Where(cI => cI.DisplayType == dispCfg.PrimaryDisplay).FirstOrDefault();
            
            if ( dispCfg.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone
                && base.MachineInfo.PlatformDetails.IsLowpower
                && priDisplayInfo.IsPortraitPanel == true
                && (!base.MachineInfo.OS.IsGreaterThan(OSType.WINTHRESHOLD))
                && priDisplayInfo.displayExtnInformation.Equals(DisplayExtensionInfo.Internal))
            {
                Log.Alert("{0} This Configuration Is Not Applicable",dispCfg);
                return true;
            }
            switch (dispCfg.ConfigType)
                {
                    case DisplayConfigType.SD:
                        Log.Message("Config to be set - {0} : {1}", dispCfg.ConfigType, dispCfg.PrimaryDisplay);
                        return SingleDisplaySwitch(dispCfg, base.GetDisplayModeByDisplayType(dispCfg.PrimaryDisplay));

                    case DisplayConfigType.DDC:
                        Log.Message("Config to be set - {0}: {1} + {2}", dispCfg.ConfigType,
                            dispCfg.PrimaryDisplay, dispCfg.SecondaryDisplay);

                        return DualDisplayCloneSwitch(dispCfg, resolution, resolution);//hardcoding to 10x7 resolution.
                    //return DualDisplayCloneSwitch(dispCfg, base.GetDisplayModeByDisplayType(dispCfg.PrimaryDisplay), 
                    //    base.GetDisplayModeByDisplayType(dispCfg.SecondaryDisplay));

                    case DisplayConfigType.TDC:
                        Log.Message("Config to be set - {0}: {1} + {2} + {3}", dispCfg.ConfigType,
                            dispCfg.PrimaryDisplay, dispCfg.SecondaryDisplay, dispCfg.TertiaryDisplay);

                        return TriDisplayCloneSwitch(dispCfg, resolution, resolution, resolution);//hardcoding to 10x7 resolution.
                    //return TriDisplayCloneSwitch(dispCfg, base.GetDisplayModeByDisplayType(dispCfg.PrimaryDisplay), 
                    //    base.GetDisplayModeByDisplayType(dispCfg.SecondaryDisplay), base.GetDisplayModeByDisplayType(dispCfg.TertiaryDisplay));

                    case DisplayConfigType.ED:
                        Log.Message("Config to be set - {0}: {1} + {2}", dispCfg.ConfigType,
                            dispCfg.PrimaryDisplay, dispCfg.SecondaryDisplay);

                        return ExtendedDisplaySwitch(dispCfg, base.GetDisplayModeByDisplayType(dispCfg.PrimaryDisplay),
                            base.GetDisplayModeByDisplayType(dispCfg.SecondaryDisplay));

                    case DisplayConfigType.TED:
                        Log.Message("Config to be set - {0}: {1} + {2} + {3}", dispCfg.ConfigType,
                            dispCfg.PrimaryDisplay, dispCfg.SecondaryDisplay, dispCfg.TertiaryDisplay);

                        return TriExtendedDisplaySwitch(dispCfg, base.GetDisplayModeByDisplayType(dispCfg.PrimaryDisplay),
                            base.GetDisplayModeByDisplayType(dispCfg.SecondaryDisplay), base.GetDisplayModeByDisplayType(dispCfg.TertiaryDisplay));
                }
            return false;
        }

        public void PrintPathAndModeInfo(UInt32 numPathArrayElements, DISPLAYCONFIG_PATH_INFO[] SDC_pathArray, UInt32 numModeInfoArrayElements, DISPLAYCONFIG_MODE_INFO[] SDC_modeInfoArray)
        {
            Log.Verbose("DumpData");

            for (int i = 0; i < SDC_pathArray.Length;i++ )
            {
                DISPLAYCONFIG_PATH_INFO eachPath = SDC_pathArray[i];
                Log.Verbose( eachPath.ToString());
                Log.Verbose("--------------------------------------------------------");
            }

            for (int i = 0; i < SDC_modeInfoArray.Length; i++)
            {
                DISPLAYCONFIG_MODE_INFO eachPath = SDC_modeInfoArray[i];
                Log.Verbose(eachPath.ToString());
                Log.Verbose("--------------------------------------------------------");
            }
        }

        /// <summary>
        /// Apply Single display config.
        /// </summary>
        private bool SingleDisplaySwitch(DisplayConfig dispCfg, DisplayMode mode)
        {
            uint pixelClk = 0, htotalVtotal = 0;
            UInt32 numPathArrayElements = 0, numModeInfoArrayElements = 0;
            int returnVal = Interop.GetDisplayConfigBufferSizes((uint)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, ref numModeInfoArrayElements);
            DISPLAYCONFIG_PATH_INFO[] pathInfo = new DISPLAYCONFIG_PATH_INFO[numPathArrayElements];
            DISPLAYCONFIG_MODE_INFO[] modeInfo = new DISPLAYCONFIG_MODE_INFO[numModeInfoArrayElements];
            DISPLAYCONFIG_TOPOLOGY_ID topologyId = DISPLAYCONFIG_TOPOLOGY_ID.DISPLAYCONFIG_TOPOLOGY_NULL;
            returnVal = Interop.QueryDisplayConfig((UInt32)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, pathInfo,
            ref numModeInfoArrayElements, modeInfo, topologyId);
            if (returnVal != (int)QDC_SDC_StatusCode.SUCCESS)
            {
                Log.Verbose("Failed to fetch mode !!! Return value of QDC call : {0}", (QDC_SDC_StatusCode)returnVal);
                return false;
            }

            DISPLAYCONFIG_PATH_INFO[] SDC_pathArray = new DISPLAYCONFIG_PATH_INFO[1];
            DISPLAYCONFIG_MODE_INFO[] SDC_modeInfoArray = new DISPLAYCONFIG_MODE_INFO[1];
            FillInConstantPathValues(ref SDC_pathArray[0], pathInfo[0]);
            FillInConstantModeValues(ref SDC_modeInfoArray[0], modeInfo[1].adapterId.HighPart,
                modeInfo[1].adapterId.LowPart);
            if (Convert.ToBoolean(mode.InterlacedFlag))
            {
                ConvertRRtoRational((ulong)mode.HzRes, (ulong)mode.VtRes, (ulong)mode.RR, false, out pixelClk, out htotalVtotal);
            }
            else
            {
                ConvertRRtoRational((ulong)mode.HzRes, (ulong)mode.VtRes, (ulong)mode.RR, true, out pixelClk, out htotalVtotal);
            }
            SDC_pathArray[0].targetInfo.refreshRate.Numerator = pixelClk;
            SDC_pathArray[0].targetInfo.refreshRate.Denominator = htotalVtotal;
            SDC_modeInfoArray[0].mode.sourceMode.width = mode.HzRes;
            SDC_modeInfoArray[0].mode.sourceMode.height = mode.VtRes;
            SDC_modeInfoArray[0].mode.targetMode.targetVideoSignalInfo.hSyncFreq.Numerator = HSYNC_SDC_NUM;
            SDC_modeInfoArray[0].mode.targetMode.targetVideoSignalInfo.hSyncFreq.Denominator = HSYNC_SDC_DENOM;
            SDC_modeInfoArray[0].mode.sourceMode.pixelFormat = GetPixelFormat(mode.Bpp);
            uint attempt = 0;
            AssignOutputTechAndId(dispCfg.PrimaryDisplay, ref SDC_pathArray[0].targetInfo.outputTechnology,
                   ref SDC_pathArray[0].targetInfo.id, attempt);

            if (Convert.ToBoolean(mode.InterlacedFlag))
            {
                SDC_pathArray[0].targetInfo.scanlineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
                SDC_modeInfoArray[0].mode.targetMode.targetVideoSignalInfo.scanLineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
            }
            returnVal = Interop.SetDisplayConfig(1, SDC_pathArray, 1, SDC_modeInfoArray,
                    SDC_APPLY | SDC_USE_SUPPLIED_DISPLAY_CONFIG |
                    SDC_SAVE_TO_DATABASE | SDC_ALLOW_CHANGES);
            if (returnVal == (long)QDC_SDC_StatusCode.SUCCESS)
            {
                Log.Verbose("Return value of SDC call : {0}", (QDC_SDC_StatusCode)returnVal);
                Thread.Sleep(5000);

                DisplayConfig tempConfig = GetConfig();
                if (!(tempConfig.ConfigType == dispCfg.ConfigType && tempConfig.PrimaryDisplay ==dispCfg.PrimaryDisplay && 
                    tempConfig.SecondaryDisplay == dispCfg.SecondaryDisplay && tempConfig.TertiaryDisplay==dispCfg.TertiaryDisplay))
                {
                    Log.Fail("Config {0} does not match with current config {1}", dispCfg.GetCurrentConfigStr(), tempConfig.GetCurrentConfigStr());

                    PrintPathAndModeInfo(1, SDC_pathArray, 1, SDC_modeInfoArray);
                    Log.Verbose("Flags" + " " + SDC_APPLY.ToString() + " " + SDC_USE_SUPPLIED_DISPLAY_CONFIG.ToString() + " " +
                            SDC_SAVE_TO_DATABASE.ToString() + " " + SDC_ALLOW_CHANGES.ToString());
                    return false;
                }
                else
                    Log.Message("Config {0} applied Successfully", dispCfg.GetCurrentConfigStr());

                return true;
            }

            Log.Alert("Error in applying Config !!!! Return value of SDC call : {0}", (QDC_SDC_StatusCode)returnVal);

            PrintPathAndModeInfo(1, SDC_pathArray,1, SDC_modeInfoArray);
            Log.Verbose("Flags" + SDC_APPLY.ToString() + SDC_USE_SUPPLIED_DISPLAY_CONFIG.ToString()+
                    SDC_SAVE_TO_DATABASE.ToString() + SDC_ALLOW_CHANGES.ToString());
            return false;
        }

        /// <summary>
        /// Apply Dual display config.
        /// </summary>

        private bool DualDisplayCloneSwitch(DisplayConfig dispCfg, DisplayMode primMode, DisplayMode secMode)
        {
            UInt32 numPathArrayElements = 0, numModeInfoArrayElements = 0;
            int returnVal = Interop.GetDisplayConfigBufferSizes((uint)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, ref numModeInfoArrayElements);
            DISPLAYCONFIG_PATH_INFO[] pathInfo = new DISPLAYCONFIG_PATH_INFO[numPathArrayElements];
            DISPLAYCONFIG_MODE_INFO[] modeInfo = new DISPLAYCONFIG_MODE_INFO[numModeInfoArrayElements];
            DISPLAYCONFIG_TOPOLOGY_ID topologyId = DISPLAYCONFIG_TOPOLOGY_ID.DISPLAYCONFIG_TOPOLOGY_NULL;
            returnVal = Interop.QueryDisplayConfig((UInt32)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, pathInfo,
            ref numModeInfoArrayElements, modeInfo, topologyId);

            if (returnVal != (int)QDC_SDC_StatusCode.SUCCESS)
            {
                Log.Verbose("Failed to fetch mode !!! Return value of QDC call : {0}", (QDC_SDC_StatusCode)returnVal);
                return false;
            }

            DisplayInfo priDisplayInfo = base.EnumeratedDisplays.Where(cI => cI.DisplayType == dispCfg.PrimaryDisplay).FirstOrDefault();
            DisplayInfo secDisplayInfo = base.EnumeratedDisplays.Where(cI => cI.DisplayType == dispCfg.SecondaryDisplay).FirstOrDefault();

            DISPLAYCONFIG_PATH_INFO[] SDC_pathArray = new DISPLAYCONFIG_PATH_INFO[2];
            DISPLAYCONFIG_MODE_INFO[] SDC_modeInfoArray = new DISPLAYCONFIG_MODE_INFO[2];
            FillInConstantPathValues(ref SDC_pathArray[0], pathInfo[0]);
            FillInConstantModeValues(ref SDC_modeInfoArray[0], modeInfo[1].adapterId.HighPart,
                modeInfo[1].adapterId.LowPart);
            FillInConstantPathValues(ref SDC_pathArray[1], pathInfo[0]);

            uint pixelClk = 0, htotalVtotal = 0;

            if (Convert.ToBoolean(primMode.InterlacedFlag))
            {
                ConvertRRtoRational(primMode.HzRes, primMode.VtRes, primMode.RR, false,
                   out pixelClk, out htotalVtotal);
            }
            else
            {
                ConvertRRtoRational(primMode.HzRes, primMode.VtRes, primMode.RR, true,
                    out pixelClk, out htotalVtotal);
            }

            //Primary & secondary display
            SDC_pathArray[0].targetInfo.refreshRate.Numerator = pixelClk; //38216000;
            SDC_pathArray[0].targetInfo.refreshRate.Denominator = htotalVtotal; //1024*622;
            SDC_modeInfoArray[0].mode.sourceMode.width = primMode.HzRes;
            SDC_modeInfoArray[0].mode.sourceMode.height = primMode.VtRes;
            SDC_modeInfoArray[0].mode.targetMode.targetVideoSignalInfo.hSyncFreq.Numerator = HSYNC_SDC_NUM;
            SDC_modeInfoArray[0].mode.targetMode.targetVideoSignalInfo.hSyncFreq.Denominator = HSYNC_SDC_DENOM;

            pixelClk = 0; htotalVtotal = 0;
            if (Convert.ToBoolean(secMode.InterlacedFlag))
            {
                ConvertRRtoRational(secMode.HzRes, secMode.VtRes, secMode.RR, false,
                    out pixelClk, out htotalVtotal);
            }
            else
            {
                ConvertRRtoRational(secMode.HzRes, secMode.VtRes, secMode.RR, true,
                    out pixelClk, out htotalVtotal);
            }
            SDC_pathArray[1].targetInfo.refreshRate.Numerator = pixelClk; //38216000;
            SDC_pathArray[1].targetInfo.refreshRate.Denominator = htotalVtotal; //1024*622;     

            SDC_modeInfoArray[0].mode.sourceMode.pixelFormat = GetPixelFormat(primMode.Bpp); //(bpp);
            SDC_modeInfoArray[1].mode.sourceMode.pixelFormat = GetPixelFormat(secMode.Bpp); //(bpp);

            //Position is to be set for clone
            SDC_modeInfoArray[1].mode.sourceMode.position.px = (int)SDC_modeInfoArray[0].mode.sourceMode.width;

            AssignOutputTechAndId(dispCfg.PrimaryDisplay, ref SDC_pathArray[0].targetInfo.outputTechnology,
                  ref SDC_pathArray[0].targetInfo.id, 0);
            AssignOutputTechAndId(dispCfg.SecondaryDisplay, ref SDC_pathArray[1].targetInfo.outputTechnology,
                  ref SDC_pathArray[1].targetInfo.id, 0);

            if (Convert.ToBoolean(primMode.InterlacedFlag))
            {
                SDC_pathArray[0].targetInfo.scanlineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
                SDC_modeInfoArray[0].mode.targetMode.targetVideoSignalInfo.scanLineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
            }
            if (Convert.ToBoolean(secMode.InterlacedFlag))
            {
                SDC_pathArray[1].targetInfo.scanlineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
                SDC_modeInfoArray[1].mode.targetMode.targetVideoSignalInfo.scanLineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
            }

            if (priDisplayInfo.IsPortraitPanel)
            {
                SDC_pathArray[0].targetInfo.rotation = DISPLAYCONFIG_ROTATION.DISPLAYCONFIG_ROTATION_ROTATE270;
            }
            if (secDisplayInfo.IsPortraitPanel)
            {
                SDC_pathArray[1].targetInfo.rotation = DISPLAYCONFIG_ROTATION.DISPLAYCONFIG_ROTATION_ROTATE270;
            }

            returnVal = Interop.SetDisplayConfig(2, SDC_pathArray, 1, SDC_modeInfoArray,
                SDC_APPLY | SDC_USE_SUPPLIED_DISPLAY_CONFIG | SDC_SAVE_TO_DATABASE | SDC_ALLOW_CHANGES | SDC_NO_OPTIMIZATION);

            if (returnVal == (long)QDC_SDC_StatusCode.SUCCESS)
            {
                Log.Verbose("Config applied. Return value of SDC call : {0}", (QDC_SDC_StatusCode)returnVal);
                Thread.Sleep(7000);

                DisplayConfig tempConfig = GetConfig();
                if (!(tempConfig.ConfigType == dispCfg.ConfigType && tempConfig.PrimaryDisplay == dispCfg.PrimaryDisplay 
                    && tempConfig.SecondaryDisplay == dispCfg.SecondaryDisplay && tempConfig.TertiaryDisplay == dispCfg.TertiaryDisplay))
                {
                    Log.Fail("Config {0} does not match with current config {1}", dispCfg.GetCurrentConfigStr(), tempConfig.GetCurrentConfigStr());

                    PrintPathAndModeInfo(2, SDC_pathArray, 1, SDC_modeInfoArray);
                    Log.Verbose("Flags" + " " + SDC_APPLY.ToString() + " " + SDC_USE_SUPPLIED_DISPLAY_CONFIG.ToString() + " " +
                            SDC_SAVE_TO_DATABASE.ToString() + " " + SDC_ALLOW_CHANGES.ToString() + " " + SDC_NO_OPTIMIZATION.ToString());
                    return false;
                }
                else
                    Log.Message("Config {0} applied Successfully", dispCfg.GetCurrentConfigStr());

                return true;
            }

            Log.Alert("Error in applying Config !!!! Return value of SDC call : {0}", (QDC_SDC_StatusCode)returnVal);

            PrintPathAndModeInfo(2, SDC_pathArray, 1, SDC_modeInfoArray);
            Log.Verbose("Flags" + SDC_APPLY.ToString() + SDC_USE_SUPPLIED_DISPLAY_CONFIG.ToString() +
                    SDC_SAVE_TO_DATABASE.ToString() + SDC_ALLOW_CHANGES.ToString() + SDC_NO_OPTIMIZATION.ToString());
            return false;
        }

        /// <summary>
        /// Apply Tri display config.
        /// </summary>
        private bool TriDisplayCloneSwitch(DisplayConfig dispCfg, DisplayMode primMode, DisplayMode secMode, DisplayMode terMode)
        {
            UInt32 numPathArrayElements = 0, numModeInfoArrayElements = 0;
            int returnVal = Interop.GetDisplayConfigBufferSizes((uint)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, ref numModeInfoArrayElements);
            DISPLAYCONFIG_PATH_INFO[] pathInfo = new DISPLAYCONFIG_PATH_INFO[numPathArrayElements];
            DISPLAYCONFIG_MODE_INFO[] modeInfo = new DISPLAYCONFIG_MODE_INFO[numModeInfoArrayElements];
            DISPLAYCONFIG_TOPOLOGY_ID topologyId = DISPLAYCONFIG_TOPOLOGY_ID.DISPLAYCONFIG_TOPOLOGY_NULL;
            returnVal = Interop.QueryDisplayConfig((UInt32)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, pathInfo,
            ref numModeInfoArrayElements, modeInfo, topologyId);

            if (returnVal != (int)QDC_SDC_StatusCode.SUCCESS)
            {
                Log.Verbose("Failed to fetch mode !!! Return value of QDC call : {0}", (QDC_SDC_StatusCode)returnVal);
                return false;
            }

            DisplayInfo priDisplayInfo = base.EnumeratedDisplays.Where(cI => cI.DisplayType == dispCfg.PrimaryDisplay).FirstOrDefault();
            DisplayInfo secDisplayInfo = base.EnumeratedDisplays.Where(cI => cI.DisplayType == dispCfg.SecondaryDisplay).FirstOrDefault();
            DisplayInfo terDisplayInfo = base.EnumeratedDisplays.Where(cI => cI.DisplayType == dispCfg.TertiaryDisplay).FirstOrDefault();

            DISPLAYCONFIG_PATH_INFO[] SDC_pathArray = new DISPLAYCONFIG_PATH_INFO[3];
            DISPLAYCONFIG_MODE_INFO[] SDC_modeInfoArray = new DISPLAYCONFIG_MODE_INFO[3];

            FillInConstantPathValues(ref SDC_pathArray[0], pathInfo[0]);
            FillInConstantModeValues(ref SDC_modeInfoArray[0], modeInfo[1].adapterId.HighPart,
                modeInfo[1].adapterId.LowPart);
            FillInConstantPathValues(ref SDC_pathArray[1], pathInfo[0]);
            FillInConstantPathValues(ref SDC_pathArray[2], pathInfo[0]);

            uint pixelClk = 0, htotalVtotal = 0;

            if (Convert.ToBoolean(primMode.InterlacedFlag))
            {
                ConvertRRtoRational(primMode.HzRes, primMode.VtRes, primMode.RR, false,
                   out pixelClk, out htotalVtotal);
            }
            else
            {
                ConvertRRtoRational(primMode.HzRes, primMode.VtRes, primMode.RR, true,
                    out pixelClk, out htotalVtotal);
            }

            //Primary & secondary display
            SDC_pathArray[0].targetInfo.refreshRate.Numerator = pixelClk; //38216000;
            SDC_pathArray[0].targetInfo.refreshRate.Denominator = htotalVtotal; //1024*622;
            SDC_modeInfoArray[0].mode.sourceMode.width = primMode.HzRes;
            SDC_modeInfoArray[0].mode.sourceMode.height = primMode.VtRes;
            SDC_modeInfoArray[0].mode.targetMode.targetVideoSignalInfo.hSyncFreq.Numerator = HSYNC_SDC_NUM;
            SDC_modeInfoArray[0].mode.targetMode.targetVideoSignalInfo.hSyncFreq.Denominator = HSYNC_SDC_DENOM;

            pixelClk = 0; htotalVtotal = 0;
            if (Convert.ToBoolean(secMode.InterlacedFlag))
            {
                ConvertRRtoRational(secMode.HzRes, secMode.VtRes, secMode.RR, false,
                    out pixelClk, out htotalVtotal);
            }
            else
            {
                ConvertRRtoRational(secMode.HzRes, secMode.VtRes, secMode.RR, true,
                    out pixelClk, out htotalVtotal);
            }
            SDC_pathArray[1].targetInfo.refreshRate.Numerator = pixelClk; //38216000;
            SDC_pathArray[1].targetInfo.refreshRate.Denominator = htotalVtotal; //1024*622;     

            pixelClk = 0; htotalVtotal = 0;
            if (Convert.ToBoolean(terMode.InterlacedFlag))
            {
                ConvertRRtoRational(terMode.HzRes, terMode.VtRes, terMode.RR, false,
                    out pixelClk, out htotalVtotal);
            }
            else
            {
                ConvertRRtoRational(terMode.HzRes, terMode.VtRes, terMode.RR, true,
                    out pixelClk, out htotalVtotal);
            }
            SDC_pathArray[2].targetInfo.refreshRate.Numerator = pixelClk; //38216000;
            SDC_pathArray[2].targetInfo.refreshRate.Denominator = htotalVtotal; //1024*622;     

            SDC_modeInfoArray[0].mode.sourceMode.pixelFormat = GetPixelFormat(primMode.Bpp); //(bpp);
            SDC_modeInfoArray[1].mode.sourceMode.pixelFormat = GetPixelFormat(secMode.Bpp); //(bpp);
            SDC_modeInfoArray[2].mode.sourceMode.pixelFormat = GetPixelFormat(terMode.Bpp); //(bpp);

            //Position is to be set for clone
            SDC_modeInfoArray[1].mode.sourceMode.position.px = (int)SDC_modeInfoArray[0].mode.sourceMode.width;
            SDC_modeInfoArray[2].mode.sourceMode.position.px = SDC_modeInfoArray[1].mode.sourceMode.position.px + (int)SDC_modeInfoArray[1].mode.sourceMode.width;

            AssignOutputTechAndId(dispCfg.PrimaryDisplay, ref SDC_pathArray[0].targetInfo.outputTechnology,
                  ref SDC_pathArray[0].targetInfo.id, 0);
            AssignOutputTechAndId(dispCfg.SecondaryDisplay, ref SDC_pathArray[1].targetInfo.outputTechnology,
                  ref SDC_pathArray[1].targetInfo.id, 0);
            AssignOutputTechAndId(dispCfg.TertiaryDisplay, ref SDC_pathArray[2].targetInfo.outputTechnology,
                  ref SDC_pathArray[2].targetInfo.id, 0);

            if (Convert.ToBoolean(primMode.InterlacedFlag))
            {
                SDC_pathArray[0].targetInfo.scanlineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
                SDC_modeInfoArray[0].mode.targetMode.targetVideoSignalInfo.scanLineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
            }
            if (Convert.ToBoolean(secMode.InterlacedFlag))
            {
                SDC_pathArray[1].targetInfo.scanlineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
                SDC_modeInfoArray[1].mode.targetMode.targetVideoSignalInfo.scanLineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
            }
            if (Convert.ToBoolean(terMode.InterlacedFlag))
            {
                SDC_pathArray[2].targetInfo.scanlineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
                SDC_modeInfoArray[2].mode.targetMode.targetVideoSignalInfo.scanLineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
            }

            if (priDisplayInfo.IsPortraitPanel)
            {
                SDC_pathArray[0].targetInfo.rotation = DISPLAYCONFIG_ROTATION.DISPLAYCONFIG_ROTATION_ROTATE270;
            }
            if (secDisplayInfo.IsPortraitPanel)
            {
                SDC_pathArray[1].targetInfo.rotation = DISPLAYCONFIG_ROTATION.DISPLAYCONFIG_ROTATION_ROTATE270;
            }
            if (terDisplayInfo.IsPortraitPanel)
            {
                SDC_pathArray[2].targetInfo.rotation = DISPLAYCONFIG_ROTATION.DISPLAYCONFIG_ROTATION_ROTATE270;
            }

            returnVal = Interop.SetDisplayConfig(3, SDC_pathArray, 1, SDC_modeInfoArray,
                SDC_APPLY | SDC_USE_SUPPLIED_DISPLAY_CONFIG | SDC_SAVE_TO_DATABASE | SDC_ALLOW_CHANGES | SDC_NO_OPTIMIZATION);

            if (returnVal == (long)QDC_SDC_StatusCode.SUCCESS)
            {
                Log.Verbose("Config applied. Return value of SDC call : {0}", (QDC_SDC_StatusCode)returnVal);
                Thread.Sleep(7000);

                DisplayConfig tempConfig = GetConfig();
                if (!(tempConfig.ConfigType == dispCfg.ConfigType && tempConfig.PrimaryDisplay == dispCfg.PrimaryDisplay &&
                    tempConfig.SecondaryDisplay == dispCfg.SecondaryDisplay && tempConfig.TertiaryDisplay == dispCfg.TertiaryDisplay))
                {
                    Log.Fail("Config {0} does not match with current config {1}", dispCfg.GetCurrentConfigStr(), tempConfig.GetCurrentConfigStr());

                    PrintPathAndModeInfo(3, SDC_pathArray, 1, SDC_modeInfoArray);
                    Log.Verbose("Flags" + " " + SDC_APPLY.ToString() + " " + SDC_USE_SUPPLIED_DISPLAY_CONFIG.ToString() + " " +
                            SDC_SAVE_TO_DATABASE.ToString() + " " + SDC_ALLOW_CHANGES.ToString() + " " + SDC_NO_OPTIMIZATION.ToString());
                    return false;
                }
                else
                    Log.Message("Config {0} applied Successfully", dispCfg.GetCurrentConfigStr());

                return true;
            }

            Log.Alert("Error in applying Config !!!! Return value of SDC call : {0}", (QDC_SDC_StatusCode)returnVal);

            PrintPathAndModeInfo(3, SDC_pathArray, 1, SDC_modeInfoArray);
            Log.Verbose("Flags" + SDC_APPLY.ToString() + SDC_USE_SUPPLIED_DISPLAY_CONFIG.ToString() +
                    SDC_SAVE_TO_DATABASE.ToString() + SDC_ALLOW_CHANGES.ToString() + SDC_NO_OPTIMIZATION.ToString());
            return false;
        }

        /// <summary>
        /// Apply Tri display config.
        /// </summary>
        private bool ExtendedDisplaySwitch(DisplayConfig dispCfg, DisplayMode primMode, DisplayMode secMode)
        {
            UInt32 numPathArrayElements = 0, numModeInfoArrayElements = 0;
            int returnVal = Interop.GetDisplayConfigBufferSizes((uint)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, ref numModeInfoArrayElements);
            DISPLAYCONFIG_PATH_INFO[] pathInfo = new DISPLAYCONFIG_PATH_INFO[numPathArrayElements];
            DISPLAYCONFIG_MODE_INFO[] modeInfo = new DISPLAYCONFIG_MODE_INFO[numModeInfoArrayElements];
            DISPLAYCONFIG_TOPOLOGY_ID topologyId = DISPLAYCONFIG_TOPOLOGY_ID.DISPLAYCONFIG_TOPOLOGY_NULL;
            returnVal = Interop.QueryDisplayConfig((UInt32)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, pathInfo,
            ref numModeInfoArrayElements, modeInfo, topologyId);

            if (returnVal != (int)QDC_SDC_StatusCode.SUCCESS)
            {
                Log.Verbose("Failed to fetch mode !!! Return value of QDC call : {0}", (QDC_SDC_StatusCode)returnVal);
                return false;
            }

            DISPLAYCONFIG_PATH_INFO[] SDC_pathArray = new DISPLAYCONFIG_PATH_INFO[2];
            DISPLAYCONFIG_MODE_INFO[] SDC_modeInfoArray = new DISPLAYCONFIG_MODE_INFO[2];
            FillInConstantPathValues(ref SDC_pathArray[0], pathInfo[0]);
            FillInConstantPathValues(ref SDC_pathArray[1], pathInfo[0]);
            FillInConstantModeValues(ref SDC_modeInfoArray[0], modeInfo[1].adapterId.HighPart,
                modeInfo[1].adapterId.LowPart);
            FillInConstantModeValues(ref SDC_modeInfoArray[1], modeInfo[1].adapterId.HighPart,
                modeInfo[1].adapterId.LowPart);
            uint pixelClk = 0, htotalVtotal = 0;

            if (Convert.ToBoolean(primMode.InterlacedFlag))
            {
                ConvertRRtoRational(primMode.HzRes, primMode.VtRes, primMode.RR, false,
                    out pixelClk, out htotalVtotal);
            }
            else
            {
                ConvertRRtoRational(primMode.HzRes, primMode.VtRes, primMode.RR, true,
                    out pixelClk, out htotalVtotal);
            }

            //Applies 1024*768*60*32 for both primary display
            SDC_pathArray[0].targetInfo.refreshRate.Numerator = pixelClk; //38216000;
            SDC_pathArray[0].targetInfo.refreshRate.Denominator = htotalVtotal; //1024*622;
            SDC_modeInfoArray[0].mode.sourceMode.width = primMode.HzRes;
            SDC_modeInfoArray[0].mode.sourceMode.height = primMode.VtRes;
            SDC_modeInfoArray[0].mode.targetMode.targetVideoSignalInfo.hSyncFreq.Numerator = HSYNC_SDC_NUM;
            SDC_modeInfoArray[0].mode.targetMode.targetVideoSignalInfo.hSyncFreq.Denominator = HSYNC_SDC_DENOM;

            pixelClk = 0; htotalVtotal = 0;

            if (Convert.ToBoolean(secMode.InterlacedFlag))
            {
                ConvertRRtoRational(secMode.HzRes, secMode.VtRes, secMode.RR, false,
                   out pixelClk, out htotalVtotal);
            }
            else
            {
                ConvertRRtoRational(secMode.HzRes, secMode.VtRes, secMode.RR, true,
                    out pixelClk, out htotalVtotal);
            }

            //Applies 1024*768*60*32 for secondary display
            SDC_pathArray[1].targetInfo.refreshRate.Numerator = pixelClk; //38216000;
            SDC_pathArray[1].targetInfo.refreshRate.Denominator = htotalVtotal; //1024*622;       
            SDC_modeInfoArray[1].mode.sourceMode.width = secMode.HzRes;
            SDC_modeInfoArray[1].mode.sourceMode.height = secMode.VtRes;
            SDC_modeInfoArray[1].mode.targetMode.targetVideoSignalInfo.hSyncFreq.Numerator = HSYNC_SDC_NUM;
            SDC_modeInfoArray[1].mode.targetMode.targetVideoSignalInfo.hSyncFreq.Denominator = HSYNC_SDC_DENOM;

            //Parameters to be set for extended
            SDC_modeInfoArray[1].id = 1;
            SDC_pathArray[1].sourceInfo.id = 1;
            SDC_pathArray[1].sourceInfo.modeInfoIdx = 1;
            SDC_modeInfoArray[1].mode.sourceMode.position.px = (int)SDC_modeInfoArray[0].mode.sourceMode.width;

            SDC_modeInfoArray[0].mode.sourceMode.pixelFormat = GetPixelFormat(primMode.Bpp);
            SDC_modeInfoArray[1].mode.sourceMode.pixelFormat = GetPixelFormat(secMode.Bpp);

            AssignOutputTechAndId(dispCfg.PrimaryDisplay, ref SDC_pathArray[0].targetInfo.outputTechnology,
                  ref SDC_pathArray[0].targetInfo.id, 0);
            AssignOutputTechAndId(dispCfg.SecondaryDisplay, ref SDC_pathArray[1].targetInfo.outputTechnology,
                  ref SDC_pathArray[1].targetInfo.id, 0);

            if (Convert.ToBoolean(primMode.InterlacedFlag))
            {
                SDC_pathArray[0].targetInfo.scanlineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
                SDC_modeInfoArray[0].mode.targetMode.targetVideoSignalInfo.scanLineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
            }
            if (Convert.ToBoolean(secMode.InterlacedFlag))
            {
                SDC_pathArray[1].targetInfo.scanlineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
                SDC_modeInfoArray[1].mode.targetMode.targetVideoSignalInfo.scanLineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
            }

            returnVal = Interop.SetDisplayConfig(2, SDC_pathArray, 2, SDC_modeInfoArray,
                SDC_APPLY | SDC_USE_SUPPLIED_DISPLAY_CONFIG | SDC_SAVE_TO_DATABASE | SDC_ALLOW_CHANGES);

            if (returnVal == (long)QDC_SDC_StatusCode.SUCCESS)
            {
                Log.Verbose("Config applied. Return value of SDC call : {0}", (QDC_SDC_StatusCode)returnVal);
                if (base.MachineInfo.PlatformDetails.FormFactor == FormFactor.APL)
                {
                    Thread.Sleep(14000);
                }
                else 
                {
                    Thread.Sleep(7000);
                }

                DisplayConfig tempConfig = GetConfig();
                if (!(tempConfig.ConfigType == dispCfg.ConfigType && tempConfig.PrimaryDisplay == dispCfg.PrimaryDisplay &&
                    tempConfig.SecondaryDisplay == dispCfg.SecondaryDisplay && tempConfig.TertiaryDisplay == dispCfg.TertiaryDisplay))
                {
                    Log.Fail("Config {0} does not match with current config {1}", dispCfg.GetCurrentConfigStr(), tempConfig.GetCurrentConfigStr());

                    PrintPathAndModeInfo(2, SDC_pathArray, 2, SDC_modeInfoArray);
                    Log.Verbose("Flags" + " " + SDC_APPLY.ToString() + " " + SDC_USE_SUPPLIED_DISPLAY_CONFIG.ToString() + " " +
                            SDC_SAVE_TO_DATABASE.ToString() + " " + SDC_ALLOW_CHANGES.ToString());
                    return false;
                }
                else
                    Log.Message("Config {0} applied Successfully", dispCfg.GetCurrentConfigStr());

                return true;
            }

            Log.Alert("Error in applying Config !!!! Return value of SDC call : {0}", (QDC_SDC_StatusCode)returnVal);

             PrintPathAndModeInfo(2, SDC_pathArray, 2, SDC_modeInfoArray);
            Log.Verbose("Flags" + SDC_APPLY.ToString() + SDC_USE_SUPPLIED_DISPLAY_CONFIG.ToString() +
                    SDC_SAVE_TO_DATABASE.ToString() + SDC_ALLOW_CHANGES.ToString());
            return false;

        }

        /// <summary>
        /// Apply Tri display config.
        /// </summary>

        private bool TriExtendedDisplaySwitch(DisplayConfig dispCfg, DisplayMode primMode, DisplayMode secMode, DisplayMode terMode)
        {
            UInt32 numPathArrayElements = 0, numModeInfoArrayElements = 0;
            int returnVal = Interop.GetDisplayConfigBufferSizes((uint)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, ref numModeInfoArrayElements);
            DISPLAYCONFIG_PATH_INFO[] pathInfo = new DISPLAYCONFIG_PATH_INFO[numPathArrayElements];
            DISPLAYCONFIG_MODE_INFO[] modeInfo = new DISPLAYCONFIG_MODE_INFO[numModeInfoArrayElements];
            DISPLAYCONFIG_TOPOLOGY_ID topologyId = DISPLAYCONFIG_TOPOLOGY_ID.DISPLAYCONFIG_TOPOLOGY_NULL;
            returnVal = Interop.QueryDisplayConfig((UInt32)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, pathInfo,
            ref numModeInfoArrayElements, modeInfo, topologyId);

            if (returnVal != (int)QDC_SDC_StatusCode.SUCCESS)
            {
                Log.Verbose("Failed to fetch mode !!! Return value of QDC call : {0}", (QDC_SDC_StatusCode)returnVal);
                return false;
            }

            DISPLAYCONFIG_PATH_INFO[] SDC_pathArray = new DISPLAYCONFIG_PATH_INFO[3];
            DISPLAYCONFIG_MODE_INFO[] SDC_modeInfoArray = new DISPLAYCONFIG_MODE_INFO[3];
            for (int index = 0; index < 3; index++)
            {
                FillInConstantPathValues(ref SDC_pathArray[index], pathInfo[0]);
            }
            for (int index = 0; index < 3; index++)
            {
                FillInConstantModeValues(ref SDC_modeInfoArray[index], modeInfo[1].adapterId.HighPart,
                    modeInfo[1].adapterId.LowPart);
            }

            uint pixelClk = 0, htotalVtotal = 0;
            if (Convert.ToBoolean(primMode.InterlacedFlag))
            {
                ConvertRRtoRational(primMode.HzRes, primMode.VtRes, primMode.RR, false,
                    out pixelClk, out htotalVtotal);
            }
            else
            {
                ConvertRRtoRational(primMode.HzRes, primMode.VtRes, primMode.RR, true,
                    out pixelClk, out htotalVtotal);
            }

            //Primary display
            SDC_pathArray[0].targetInfo.refreshRate.Numerator = pixelClk; //38216000;
            SDC_pathArray[0].targetInfo.refreshRate.Denominator = htotalVtotal; //1024*622;
            SDC_modeInfoArray[0].mode.sourceMode.width = primMode.HzRes;
            SDC_modeInfoArray[0].mode.sourceMode.height = primMode.VtRes;
            SDC_modeInfoArray[0].mode.targetMode.targetVideoSignalInfo.hSyncFreq.Numerator = HSYNC_SDC_NUM;
            SDC_modeInfoArray[0].mode.targetMode.targetVideoSignalInfo.hSyncFreq.Denominator = HSYNC_SDC_DENOM;

            pixelClk = 0; htotalVtotal = 0;
            if (Convert.ToBoolean(secMode.InterlacedFlag))
            {
                ConvertRRtoRational(secMode.HzRes, secMode.VtRes, secMode.RR, false,
                    out pixelClk, out htotalVtotal);
            }
            else
            {
                ConvertRRtoRational(secMode.HzRes, secMode.VtRes, secMode.RR, true,
                    out pixelClk, out htotalVtotal);
            }
            //Secondary display
            SDC_pathArray[1].targetInfo.refreshRate.Numerator = pixelClk; //38216000;
            SDC_pathArray[1].targetInfo.refreshRate.Denominator = htotalVtotal; //1024*622;       
            SDC_modeInfoArray[1].mode.sourceMode.width = secMode.HzRes;
            SDC_modeInfoArray[1].mode.sourceMode.height = secMode.VtRes;
            SDC_modeInfoArray[1].mode.targetMode.targetVideoSignalInfo.hSyncFreq.Numerator = HSYNC_SDC_NUM;
            SDC_modeInfoArray[1].mode.targetMode.targetVideoSignalInfo.hSyncFreq.Denominator = HSYNC_SDC_DENOM;


            pixelClk = 0; htotalVtotal = 0;
            if (Convert.ToBoolean(terMode.InterlacedFlag))
            {
                ConvertRRtoRational(terMode.HzRes, terMode.VtRes, terMode.RR, false,
                    out pixelClk, out htotalVtotal);
            }
            else
            {
                ConvertRRtoRational(terMode.HzRes, terMode.VtRes, terMode.RR, true,
                    out pixelClk, out htotalVtotal);
            }
            //Third Display
            SDC_pathArray[2].targetInfo.refreshRate.Numerator = pixelClk; //38216000;
            SDC_pathArray[2].targetInfo.refreshRate.Denominator = htotalVtotal; //1024*622;       
            SDC_modeInfoArray[2].mode.sourceMode.width = terMode.HzRes;
            SDC_modeInfoArray[2].mode.sourceMode.height = terMode.VtRes;
            SDC_modeInfoArray[2].mode.targetMode.targetVideoSignalInfo.hSyncFreq.Numerator = HSYNC_SDC_NUM;
            SDC_modeInfoArray[2].mode.targetMode.targetVideoSignalInfo.hSyncFreq.Denominator = HSYNC_SDC_DENOM;

            SDC_modeInfoArray[0].mode.sourceMode.pixelFormat = GetPixelFormat(terMode.Bpp); //(bpp);
            SDC_modeInfoArray[1].mode.sourceMode.pixelFormat = GetPixelFormat(secMode.Bpp); //(bpp);
            SDC_modeInfoArray[2].mode.sourceMode.pixelFormat = GetPixelFormat(terMode.Bpp);

            SDC_pathArray[0].sourceInfo.modeInfoIdx = 0;

            //Parameters to be set for extended
            SDC_modeInfoArray[1].id = 1;
            SDC_pathArray[1].sourceInfo.id = 1;
            SDC_pathArray[1].sourceInfo.modeInfoIdx = 1;
            SDC_modeInfoArray[1].mode.sourceMode.position.px = (int)SDC_modeInfoArray[0].mode.sourceMode.width;

            //Parameters to be set for Tri ED
            SDC_modeInfoArray[2].id = 2;
            SDC_pathArray[2].sourceInfo.id = 2;
            SDC_pathArray[2].sourceInfo.modeInfoIdx = 2;
            SDC_modeInfoArray[2].mode.sourceMode.position.px = ((int)(SDC_modeInfoArray[0].mode.sourceMode.width)) + ((int)(SDC_modeInfoArray[1].mode.sourceMode.width));


            AssignOutputTechAndId(dispCfg.PrimaryDisplay, ref SDC_pathArray[0].targetInfo.outputTechnology,
                      ref SDC_pathArray[0].targetInfo.id, 0);
            AssignOutputTechAndId(dispCfg.SecondaryDisplay, ref SDC_pathArray[1].targetInfo.outputTechnology,
                      ref SDC_pathArray[1].targetInfo.id, 0);
            AssignOutputTechAndId(dispCfg.TertiaryDisplay, ref SDC_pathArray[2].targetInfo.outputTechnology,
                       ref SDC_pathArray[2].targetInfo.id, 0);

            if (Convert.ToBoolean(primMode.InterlacedFlag))
            {
                SDC_pathArray[0].targetInfo.scanlineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
                SDC_modeInfoArray[0].mode.targetMode.targetVideoSignalInfo.scanLineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
            }
            if (Convert.ToBoolean(secMode.InterlacedFlag))
            {
                SDC_pathArray[1].targetInfo.scanlineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
                SDC_modeInfoArray[1].mode.targetMode.targetVideoSignalInfo.scanLineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
            }
            if (Convert.ToBoolean(terMode.InterlacedFlag))
            {
                SDC_pathArray[2].targetInfo.scanlineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
                SDC_modeInfoArray[2].mode.targetMode.targetVideoSignalInfo.scanLineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
            }

            returnVal = Interop.SetDisplayConfig(3, SDC_pathArray, 3, SDC_modeInfoArray,
                SDC_APPLY | SDC_USE_SUPPLIED_DISPLAY_CONFIG | SDC_SAVE_TO_DATABASE | SDC_ALLOW_CHANGES | SDC_NO_OPTIMIZATION);

            if (returnVal == (long)QDC_SDC_StatusCode.SUCCESS)
            {
                Log.Verbose("Config applied. Return value of SDC call : {0}", (QDC_SDC_StatusCode)returnVal);
                Thread.Sleep(7000);
                if(base.MachineInfo.PlatformDetails.FormFactor == FormFactor.APL)
                {
                    Thread.Sleep(14000);
                }
                else
                {
                    Thread.Sleep(7000);
                }

                DisplayConfig tempConfig = GetConfig();
                if (!(tempConfig.ConfigType == dispCfg.ConfigType && tempConfig.PrimaryDisplay == dispCfg.PrimaryDisplay &&
                    tempConfig.SecondaryDisplay == dispCfg.SecondaryDisplay && tempConfig.TertiaryDisplay == dispCfg.TertiaryDisplay))
                {
                    Log.Fail("Config {0} does not match with current config {1}", dispCfg.GetCurrentConfigStr(), tempConfig.GetCurrentConfigStr());

                    PrintPathAndModeInfo(3, SDC_pathArray, 3, SDC_modeInfoArray);
                    Log.Verbose("Flags" + " " + SDC_APPLY.ToString() + " " + SDC_USE_SUPPLIED_DISPLAY_CONFIG.ToString() + " " +
                            SDC_SAVE_TO_DATABASE.ToString() + " " + SDC_ALLOW_CHANGES.ToString() + " " + SDC_NO_OPTIMIZATION.ToString());
                    return false;
                }
                else
                    Log.Message("Config {0} applied Successfully", dispCfg.GetCurrentConfigStr());

                return true;
            }

            Log.Alert("Error in applying Config !!!! Return value of SDC call : {0}", (QDC_SDC_StatusCode)returnVal);

            PrintPathAndModeInfo(3, SDC_pathArray, 3, SDC_modeInfoArray);
            Log.Verbose("Flags" + SDC_APPLY.ToString() + SDC_USE_SUPPLIED_DISPLAY_CONFIG.ToString() +
                    SDC_SAVE_TO_DATABASE.ToString() + SDC_ALLOW_CHANGES.ToString() + SDC_NO_OPTIMIZATION.ToString());
            return false;
        }


        private void FillInConstantPathValues(ref DISPLAYCONFIG_PATH_INFO pathInfo,
                                                    DISPLAYCONFIG_PATH_INFO pathInfofromQDC)
        {
            // Constant Path Values
            pathInfo.flags = DISPLAYCONFIG_PATH_ACTIVE;
            pathInfo.sourceInfo.id = 0;
            pathInfo.sourceInfo.modeInfoIdx = 0;
            pathInfo.sourceInfo.statusFlags = 0;
            pathInfo.sourceInfo.adapterId.HighPart = pathInfofromQDC.sourceInfo.adapterId.HighPart;
            pathInfo.sourceInfo.adapterId.LowPart = pathInfofromQDC.sourceInfo.adapterId.LowPart;
            pathInfo.targetInfo.adapterId.HighPart = pathInfofromQDC.targetInfo.adapterId.HighPart;
            pathInfo.targetInfo.adapterId.LowPart = pathInfofromQDC.targetInfo.adapterId.LowPart;
            pathInfo.targetInfo.modeInfoIdx = 4294967295;
            pathInfo.targetInfo.rotation = DISPLAYCONFIG_ROTATION.DISPLAYCONFIG_ROTATION_IDENTITY;
            pathInfo.targetInfo.scaling = DISPLAYCONFIG_SCALING.DISPLAYCONFIG_SCALING_IDENTITY;
            pathInfo.targetInfo.scanlineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_PROGRESSIVE;
            pathInfo.targetInfo.statusFlags = 0;
            pathInfo.targetInfo.targetAvailable = Convert.ToBoolean(0);
        }

        private void FillInConstantModeValues(ref DISPLAYCONFIG_MODE_INFO modeInfo,
                                                    int adapterIdHigh, uint adapterIdLow)
        {
            // Constant Mode Values
            modeInfo.adapterId.HighPart = adapterIdHigh;
            modeInfo.adapterId.LowPart = adapterIdLow;
            modeInfo.id = 0;
            modeInfo.infoType = DISPLAYCONFIG_MODE_INFO_TYPE.DISPLAYCONFIG_MODE_INFO_TYPE_SOURCE;
            modeInfo.mode.sourceMode.position.px = 0;
            modeInfo.mode.sourceMode.position.py = 0;
            modeInfo.mode.targetMode.targetVideoSignalInfo.activeSize.cx = 0;
            modeInfo.mode.targetMode.targetVideoSignalInfo.activeSize.cy = 0;
            modeInfo.mode.targetMode.targetVideoSignalInfo.scanLineOrdering =
                DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_PROGRESSIVE;
            modeInfo.mode.targetMode.targetVideoSignalInfo.totalSize.cx = 0;
            modeInfo.mode.targetMode.targetVideoSignalInfo.totalSize.cy = 0;
            modeInfo.mode.targetMode.targetVideoSignalInfo.videoStandard = 0;
            modeInfo.mode.targetMode.targetVideoSignalInfo.vSyncFreq.Numerator = 0;
            modeInfo.mode.targetMode.targetVideoSignalInfo.vSyncFreq.Denominator = 0;
        }
        /// <summary>
        /// Converts RR to Rational format (x/y i.e., pixelclock/htotal*vtotal)
        /// </summary>
        /// CAUTION!! The following code for calculating the pixel clock, vtotal & htotal is taken from the SB driver code
        /// If SDC call fails because of RR value, make sure this code is in sync with SB driver code
        private void ConvertRRtoRational(ulong ulXRes, ulong ulYRes, ulong ulRRate, bool bProgressiveMode,
            out uint pixelClock, out uint HtotalVtotal)
        {
            //fixed defines as per VESA spec
            //double flMarginPerct = 1.80;//size of top and bottom overscan margin as percentage of active vertical image
            double flCellGran = 8.0;  //cell granularity
            ulong ulMinPorch = 1;    // 1 line/char cell
            ulong ulVSyncRqd = 3;    //width of vsync in lines
            float flHSynchPerct = 8.0F;//width of hsync as a percentage of total line period
            float flMin_Vsync_BP = 550.0F;//Minimum time of vertical sync + back porch interval (us).
            double flBlankingGradient_M = 600.0;//The blanking formula gradient 
            double flBlankingOffset_C = 40.0;//The blanking formula offset
            double flBlankingScaling_K = 128.0;//The blanking formula scaling factor
            double flBlankingScalWeighing_J = 20.0;//The blanking formula scaling factor weighting
            //Spec defination ends here

            //Calculation of C',M'
            //C' = Basic offset constant
            //M' = Basic gradient constant
            double flCPrime = (flBlankingOffset_C - flBlankingScalWeighing_J) * (flBlankingScaling_K) / 256.0
                            + flBlankingScalWeighing_J;
            double flMPrime = flBlankingScaling_K / 256 * flBlankingGradient_M;

            bool bInterLaced = !bProgressiveMode;

            //calculation of timing paramters
            // Step 1: Round the Horizontal Resolution to nearest 8 pixel
            ulong ulHPixels = ulXRes;
            ulong ulHPixelsRnd = (ulong)(((int)((ulHPixels / flCellGran) + (0.5))) * flCellGran);

            // Step 2: Calculate Vertical line rounded to nearest integer   
            float flVLines = (float)ulYRes;
            ulong ulVLinesRnd = (ulong)((int)((bInterLaced ? flVLines / 2 : flVLines) + 0.5));

            // Step 3: Find the field rate required (only useful for interlaced)
            float flVFieldRateRqd = (float)(bInterLaced ? ulRRate * 2 : ulRRate);

            // Step 4 and 5: Calculate top and bottom margins, we assumed zero for now
            //assumption top/bottom margins are unused, if a requirement comes for use of
            //margin then it has to added as function input parameter
            ulong ulTopMargin = 0;
            ulong ulBottomMargin = 0;

            // Step 6: If Interlaced set this value which is used in the other calculations 
            float flInterLaced = (float)(bInterLaced ? 0.5 : 0);

            // Step 7: Estimate the Horizontal period in usec per line
            float flHPeriodEst = ((1 / flVFieldRateRqd) - (flMin_Vsync_BP / 1000000)) /
                                    (ulVLinesRnd + 2 * ulTopMargin + ulMinPorch + flInterLaced) * 1000000;

            // Step 8: Find the number of lines in V sync + back porch
            ulong ulVSync_BP = (ulong)((int)((flMin_Vsync_BP / flHPeriodEst) + 0.5));

            // Step 9: Find the number of lines in V back porch alone
            ulong ulVBackPorch = ulVSync_BP - ulVSyncRqd;

            // Step 10: Find the total number of lines in vertical field
            float flTotalVLines = ulVLinesRnd + ulTopMargin + ulBottomMargin + ulVSync_BP + flInterLaced
                                  + ulMinPorch;

            // Step 11: Estimate the vertical field frequency
            float flVFieldRateEst = 1 / flHPeriodEst / flTotalVLines * 1000000;

            // Step 12: Find actual horizontal period
            float flHPeriod = flHPeriodEst / (flVFieldRateRqd / flVFieldRateEst);

            // Step 13: Find the actual vertical field frequency
            float flVFieldRate = (1 / flHPeriod / flTotalVLines) * 1000000;

            // Step 14: Find the actual vertical frame frequency
            float flVFrameRate = bInterLaced ? flVFieldRate / 2 : flVFieldRate;

            // Step 15,16: Find the number of pixels in the left, right margins, we assume they are zero 
            ulong ulLeftMargin = 0, ulRightMargin = 0;

            // Step 17: Find total number of active pixels in one line plus the margins 
            ulong ulTotalActivePixels = ulHPixelsRnd + ulRightMargin + ulLeftMargin;

            // Step 18: Find the ideal blanking duty cycle form blanking duty cycle equation
            float flIdealDutyCycle = (float)(flCPrime - (flMPrime * flHPeriod / 1000));

            // Step 19: Find the number of pixels in the blanking time to the nearest double charactr cell
            ulong ulHBlankPixels = (ulong)(((int)((ulTotalActivePixels * flIdealDutyCycle / (100 - flIdealDutyCycle) / (2 * flCellGran)) + 0.5)) * (2 * flCellGran));

            // Step 20: Find total number of pixels in one line
            ulong ulTotalPixels = ulTotalActivePixels + ulHBlankPixels;

            // Step 21: Find pixel clock frequency
            //currently we are taking value till 3 places after decimal
            //If the precision need to be increased to 4 places of decimal replace the
            //PRECISION3DEC by PRECISION4DEC
            ulong ulDecPrecisonPoint = PRECISION3DEC;
            //Get the pixel clcok till 3 places of decimals
            ulong ulPixelClock = (ulong)((int)((ulTotalPixels / flHPeriod) * ulDecPrecisonPoint) + 0.5);

            // Step 22:  Get the horizontal frequency
            float flHFreq = (1000 / flHPeriod) * 1000;

            ulong ulHSyncPixles = (ulong)(((int)(((ulTotalPixels / flCellGran) * (flHSynchPerct / 100)) + 0.5)) * flCellGran);
            ulong ulHSyncStart = ulTotalActivePixels + (ulHBlankPixels / 2) - ulHSyncPixles;
            ulong ulHSyncEnd = ulTotalActivePixels + (ulHBlankPixels / 2) - 1;
            //Gtf calculations ends here

            //This is the per frame total no of vertical lines
            ulong ulTotalVLines = (ulong)((int)((bInterLaced ? 2 * flTotalVLines : flTotalVLines) + 0.5));

            //This is done to get the pixel clock in Hz
            ulong dwDotClock = ulPixelClock * (1000000 / ulDecPrecisonPoint);    // from step 21
            ulong dwHTotal = ulTotalPixels;          // from step 20

            //calculate in case of interlaced the frame based parameters
            //instead of per field basis
            ulong dwVTotal = ulTotalVLines;  // from step 10

            pixelClock = (uint)dwDotClock;
            HtotalVtotal = (uint)(dwHTotal * dwVTotal);
            if (!bProgressiveMode)
            {
                HtotalVtotal = HtotalVtotal / 2;
            }
        }

        private DISPLAYCONFIG_PIXELFORMAT GetPixelFormat(uint bpp)
        {
            switch (bpp)
            {
                case 8:
                    return DISPLAYCONFIG_PIXELFORMAT.DISPLAYCONFIG_PIXELFORMAT_8BPP;
                case 16:
                    return DISPLAYCONFIG_PIXELFORMAT.DISPLAYCONFIG_PIXELFORMAT_16BPP;
                case 24:
                    return DISPLAYCONFIG_PIXELFORMAT.DISPLAYCONFIG_PIXELFORMAT_24BPP;
                case 32:
                    return DISPLAYCONFIG_PIXELFORMAT.DISPLAYCONFIG_PIXELFORMAT_32BPP;
                default:
                    return DISPLAYCONFIG_PIXELFORMAT.DISPLAYCONFIG_PIXELFORMAT_FORCE_UINT32;
            }
        }

        private bool AssignOutputTechAndId(DisplayType display, ref DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY outputTech,
                                                ref uint dispID, uint count)
        {
            switch (display)
            {
                case DisplayType.CRT:
                    outputTech =
                        DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_HD15;
                    break;
                //case DisplayType.LFP:
                case DisplayType.EDP:
                    outputTech =
                        DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_INTERNAL;
                    break;
                case DisplayType.DP:
                    outputTech = DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_DISPLAYPORT_EXTERNAL;
                    break;
                case DisplayType.HDMI:
                    outputTech = DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_HDMI;
                    break;
            }
            dispID = base.GetWinMonitorIDByDisplayType(display);
            return true;
        }
    }
}