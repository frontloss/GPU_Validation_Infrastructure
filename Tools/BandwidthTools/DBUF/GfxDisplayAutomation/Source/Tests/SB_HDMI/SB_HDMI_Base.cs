namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using IgfxExtBridge_DotNet;
    using System;
    using System.Threading;
    using System.Runtime.InteropServices;
    class SB_HDMI_Base : TestBase
    {
        protected string nonHDMIPanelEvent = "NON_HDMI_PANEL";
        protected string nonHDMIPanelEventSprite = "NON_HDMI_PANEL_SPRITE";
        protected string cloneModeSecondaryOverlay = "CLONE_MODE_SPRITE_DISABLE";
        protected string cursorEvent = "";

        protected void Hotplug(FunctionName FuncArg, DisplayType DisTypeArg, DVMU_PORT PortArg)
        {
            HotPlugUnplug _HotPlugUnplug = null;
            _HotPlugUnplug = new HotPlugUnplug(FuncArg, DisTypeArg, PortArg);
            bool status = AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, _HotPlugUnplug);
        }
        protected void Hotplug(FunctionName FuncArg, DisplayType DisTypeArg, DVMU_PORT PortArg, string edidFile)
        {
            HotPlugUnplug _HotPlugUnplug = null;
            _HotPlugUnplug = new HotPlugUnplug(FuncArg, PortArg, edidFile);
            bool status = AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, _HotPlugUnplug);
        }

        protected bool RegisterCheck(DisplayType display, DisplayInfo displayInfo, DisplayHierarchy displayHierarchy, string eventName)
        {
            bool match = false;
            DisplayMode targetMode;
            PipePlaneParams pipePlaneObject = new PipePlaneParams(display);
            if (eventName.Contains("SPRITE") && !eventName.Contains("CLONE") && !eventName.Contains("NON_HDMI") && base.MachineInfo.OS.Type == OSType.WIN7)
                eventName += "_Win7";

            if (eventName.Contains("XVYCC_DISABLE"))
            {
                targetMode = this.GetTargetResolution(display);
                if (targetMode.VtRes == 1080 || targetMode.VtRes == 720)
                    eventName += "_1080";
                if ((displayHierarchy != DisplayHierarchy.Display_1) && (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone) && eventName.Contains("SPRITE"))
                    eventName += "_SPRITE";
            }
            PipePlaneParams pipePlaneParams = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlaneObject);
            if (VerifyRegisters(eventName, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port,true))
            {
                Log.Success("Registers verified for event {0} on display {1}", eventName, display);
                match = true;
            }
            Log.Message("Check if Cursor exists, if Cursor connected verify Cursor registers");
            //if (CursorConnected())
            if(IsCursorEnabled(pipePlaneParams))
            {
                Log.Message("Cursor is connected, Checking for Cursor registers");
                cursorEvent = String.Concat(eventName, "_CURSOR");
                Thread.Sleep(2000);
                MoveCursorPosition(displayHierarchy, base.CurrentConfig, display);
                Thread.Sleep(2000);
                if (VerifyRegisters(cursorEvent, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, true))
                {
                    Log.Success("Cursor registers match");
                    match = match & true;
                }
                else
                {
                    Log.Fail("Cursor Registers dont match");
                    match = false;
                }
            }
            else
                Log.Message("Cursor not connected, skipping the check for Cursor registers");
            return match;
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
        protected bool CursorConnected()
        {
            cursorInfo cursorInfo = AccessInterface.GetFeature<cursorInfo>(Features.CursorEvent, Action.GetMethod, Source.AccessAPI);
            if (!(cursorInfo.hCursor == (IntPtr)0))
                return true;
            else
                return false;
        }
        protected bool IsCursorEnabled(PipePlaneParams pipePlaneParams)
        {
            string eventName = "CURSOR_STATUS";
            if (VerifyRegisters(eventName, PIPE.NONE, pipePlaneParams.Plane, PORT.NONE, false))
            {
                return false;
            }
            return true;
        }
        protected void CheckConfigChange(DisplayConfig argInitialConfig)
        {
            DisplayConfig DispConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            if (argInitialConfig.GetCurrentConfigStr().Equals(DispConfig.GetCurrentConfigStr()))
                Log.Message("No change in config");
            else
            {
                if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                    Log.Success("Config applied successfully");
                else
                {
                    base.ListEnumeratedDisplays();
                    Log.Abort("Config not applied!");
                }
            }
        }
        protected void MoveCursorToPrimary(DisplayConfig currentConfig)
        {
            MoveCursorPos moveToPri = new MoveCursorPos()
            {
                displayType = currentConfig.PrimaryDisplay,
                displayHierarchy = DisplayHierarchy.Display_1,
                currentConfig = currentConfig
            };
            AccessInterface.SetFeature<MoveCursorPos>(Features.MoveCursor, Action.Set, moveToPri);
        }
        protected void MoveCursorPosition(DisplayHierarchy displayHierarchy, DisplayConfig currentConfig, DisplayType display)
        {
            if (((int)displayHierarchy > 1 && currentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Extended))
            {
                MoveCursorPos moveCursorObject = new MoveCursorPos()
                {
                    displayType = display,
                    displayHierarchy = displayHierarchy,
                    currentConfig = currentConfig
                };
                bool shiftCursor = AccessInterface.SetFeature<bool, MoveCursorPos>(Features.MoveCursor, Action.SetMethod, moveCursorObject);
            }
        }
        protected void VerifyNonXvyccYcvcrPanel(DisplayType display)
        {
            if (!AccessInterface.SetFeature<bool, DecisionActions>(Features.LaunchCUI, Action.SetMethod, DecisionActions.No))
                Log.Fail(false, "Unable to launch CUI!");
            AccessInterface.Navigate(Features.SelectDisplay);
            AccessInterface.SetFeature(Features.SelectDisplay, Action.Set, display);
            PanelType panelType = AccessInterface.GetFeature<PanelType>(Features.XvyccYcbcr, Action.GetMethod, Source.AccessUI);
            if (panelType == PanelType.RGB)
                Log.Success("A non XVYCC/YCBCR panel hotplugged");
            else
                Log.Fail("Failure in plugging a non XVYCC/YCBCR Panel");
            AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
        }
        protected void PlayAndMoveVideo(DisplayHierarchy displayHierarchy, DisplayConfig displayConfig)
        {
            base.OverlayOperations(displayHierarchy, displayConfig, OverlayPlaybackOptions.MovePlayer);
            //OverlayParams overlayObject = new OverlayParams()
            //{
            //    PlaybackOptions = OverlayPlaybackOptions.PlayVideo,
            //    DisplayHierarchy = displayHierarchy,
            //    CurrentConfig = displayConfig
            //};
            //AccessInterface.SetFeature<OverlayParams>(Features.Overlay, Action.Set, overlayObject);
            //Thread.Sleep(2000);
            //OverlayParams overlayObj = new OverlayParams()
            //{
            //    PlaybackOptions = OverlayPlaybackOptions.MovePlayer,
            //    DisplayHierarchy = displayHierarchy,
            //    CurrentConfig = displayConfig
            //};
            //AccessInterface.SetFeature<OverlayParams>(Features.Overlay, Action.Set, overlayObj);
        }
        protected void StopVideo(DisplayHierarchy displayHierarchy, DisplayConfig displayConfig)
        {
            base.OverlayOperations(displayHierarchy, displayConfig, OverlayPlaybackOptions.ClosePlayer);

            ////if (base.MachineInfo.OS.Type == OSInfo.WIN7)
            ////{
            //OverlayParams overlayObject = new OverlayParams()
            //{
            //    PlaybackOptions = OverlayPlaybackOptions.ClosePlayer
            //};
            //AccessInterface.SetFeature<OverlayParams>(Features.Overlay, Action.Set, overlayObject);
            ////}
        }
        public bool GetSystemConfiguration(ref IGFX_SYSTEM_CONFIG_DATA_N_VIEWS sysConfigData)
        {
            IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.UNKNOWN_ERROR;
            string errorDesc = "";
            int tryCount = 1;
            DisplayUtil displayUtil = new DisplayUtil();

            while (tryCount <= 5)
            {
                Log.Verbose("Fetching system configuration data - Attempt={0}", tryCount);
                displayUtil.GetSystemConfigDataNViews(ref sysConfigData, out igfxErrorCode, out errorDesc);
                if (igfxErrorCode != IGFX_ERROR_CODES.IGFX_SUCCESS)
                {
                    Log.Fail("{0}:Unable to get system configuration data-{1}", igfxErrorCode.ToString(), errorDesc);
                    return false;
                }
                else
                {
                    Log.Verbose("System configuration data obtained successfully");
                    if (sysConfigData.dwOpMode == 0 || sysConfigData.DispCfg[0].dwDisplayUID == 0)
                    {
                        Log.Alert("Invalid opmode/displayUID obtained.. Attempting to retry");
                        Log.Alert("OpMode : {0} , Primary Display ID : {1}", sysConfigData.dwOpMode, sysConfigData.DispCfg[0].dwDisplayUID);
                    }
                    else
                    {
                        return true;
                    }
                }
                tryCount++;
                igfxErrorCode = IGFX_ERROR_CODES.UNKNOWN_ERROR;
                errorDesc = "";
                System.Threading.Thread.Sleep(5000);
            }

            Log.Fail("Invalid system configuration data obtained");
            return false;
        }
        private DisplayConfig GetDisplayConfigFromSystemConfigData(IGFX_SYSTEM_CONFIG_DATA_N_VIEWS systemConfigData)
        {
            DisplayConfig displayConfig = new DisplayConfig();
            displayConfig.PrimaryDisplay = base.CurrentConfig.PrimaryDisplay;
            if (systemConfigData.dwOpMode == 1)
            {
                displayConfig.ConfigType = DisplayConfigType.SD;
            }
            else
            {
                displayConfig.SecondaryDisplay = base.CurrentConfig.SecondaryDisplay;

                if (systemConfigData.dwOpMode == 3)
                {
                    if (systemConfigData.uiNDisplays == 3)
                    {
                        displayConfig.ConfigType = DisplayConfigType.TDC;
                        displayConfig.TertiaryDisplay = base.CurrentConfig.TertiaryDisplay;
                    }
                    else
                    {
                        displayConfig.ConfigType = DisplayConfigType.DDC;
                    }
                }
                else if (systemConfigData.dwOpMode == 5)
                {
                    if (systemConfigData.uiNDisplays == 3)
                    {
                        displayConfig.ConfigType = DisplayConfigType.TED;
                        displayConfig.TertiaryDisplay = base.CurrentConfig.TertiaryDisplay;
                    }
                    else
                    {
                        displayConfig.ConfigType = DisplayConfigType.ED;
                    }
                }
            }

            return displayConfig;
        }
        //protected void CheckCRC()
        //{
        //    if (this.MachineInfo.PlatformEnum == Platform.BDW)
        //        return;

        //    DisplayConfig currConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
        //    if (base.MachineInfo.Platform == Platform.HSWM.ToString())
        //    {
        //        if (currConfig.CustomDisplayList.Contains(DisplayType.EDP) && currConfig.PrimaryDisplay == DisplayType.EDP)
        //        {
        //            Log.Message(true, "Checking CRC");
        //            CRCDataMapper cd = new CRCDataMapper();
        //            cd.CurrentDisplayConfig = currConfig;
        //            cd.GetCRCDispType = DisplayType.EDP;
        //            AccessInterface.GetFeature<bool, CRCDataMapper>(Features.CRCCapture, Action.GetMethod, Source.CrcGenerator, cd);
        //        }
        //    }
        //}

        protected DisplayMode GetTargetResolution(DisplayType display)
        {
            DisplayMode targetMode = new DisplayMode();
            List<ScalingOptions> scalingOption = new List<ScalingOptions>();
            IGFX_SYSTEM_CONFIG_DATA_N_VIEWS systemConfigData = new IGFX_SYSTEM_CONFIG_DATA_N_VIEWS();
            this.GetSystemConfiguration(ref systemConfigData);
            DisplayConfig currentConfig = GetDisplayConfigFromSystemConfigData(systemConfigData);
            DisplayHierarchy dH = this.GetDispHierarchy(base.CurrentConfig.CustomDisplayList, display);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
            DisplayMode optimalMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            Log.Message("Current Resolution is {0}", optimalMode.ToString());            
           
            ScalingOptions scalingOptionSet = (ScalingOptions)Enum.Parse(typeof(ScalingOptions), optimalMode.ScalingOptions[0].ToString()); 

            Log.Message("Scaling value is {0}", optimalMode.ScalingOptions[0].ToString()); 
            Log.Message("Current Scaling is {0}", scalingOptionSet.ToString());

            Log.Message("Native Resolution is {0}", displayInfo.DisplayMode.ToString());
            
            if (scalingOptionSet == ScalingOptions.Center_Image || scalingOptionSet == ScalingOptions.Maintain_Aspect_Ratio || scalingOptionSet == ScalingOptions.Scale_Full_Screen)
            {
                targetMode.HzRes = displayInfo.DisplayMode.HzRes;
                targetMode.VtRes = displayInfo.DisplayMode.VtRes;
                targetMode.RR = displayInfo.DisplayMode.RR;
                targetMode.Bpp = displayInfo.DisplayMode.Bpp;
                targetMode.InterlacedFlag = displayInfo.DisplayMode.InterlacedFlag;
                int rr = Convert.ToInt32(systemConfigData.DispCfg[(int)dH].Resolution.dwRR);
                targetMode.RR = (uint)rr;
            }
            else if (scalingOptionSet == ScalingOptions.Maintain_Display_Scaling || scalingOptionSet == ScalingOptions.Customize_Aspect_Ratio)
            {
                targetMode = optimalMode;
            }
            else
            {
                Log.Fail("Wrong Scaling option passed. {0}", scalingOptionSet);
            }
            return targetMode;
        }
    }
}