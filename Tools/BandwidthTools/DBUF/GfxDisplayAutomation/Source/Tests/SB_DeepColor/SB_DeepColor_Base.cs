namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Threading;
    using System.Linq;
    using System.IO;
    using System.Diagnostics;
    using IgfxExtBridge_DotNet;
    class SB_DeepColor_Base : TestBase
    {
        protected const int HDMI_BPC_VALUE = 12;
        protected const int DP_BPC_VALUE = 10;
        protected const string DC_ENABLE = "DEEPCOLOR_ENABLED";
        protected const string DC_DISABLE = "DEEPCOLOR_DISABLED";
        protected const string DITHERING_BPC = "DITHERING_BPC";

        
        protected string edidFile = "HDMI_DELL_U2711_XVYCC.EDID";
        protected Dictionary<DisplayType, string> _defaultEDIDMap = null;
        protected Dictionary<DisplayType, string> _nonDeepColorEDIDMap = null;

        protected System.Action _actionAfterEnable = null;
        protected System.Action _actionAfterDisable = null;

        public SB_DeepColor_Base()
            : base()
        {
            _defaultEDIDMap = new Dictionary<DisplayType, string>();
            _nonDeepColorEDIDMap = new Dictionary<DisplayType, string>();

            _defaultEDIDMap.Add(DisplayType.HDMI, edidFile);
            _nonDeepColorEDIDMap.Add(DisplayType.HDMI, "HDMI_DELL_U2711_DeepClr_8bpc.EDID");

            _defaultEDIDMap.Add(DisplayType.HDMI_2, edidFile);
            _nonDeepColorEDIDMap.Add(DisplayType.HDMI_2, "HDMI_DELL_U2711_DeepClr_10bpc.EDID");
            _defaultEDIDMap.Add(DisplayType.DP, "DP_3011.EDID");
            _defaultEDIDMap.Add(DisplayType.DP_2, "DP_HP_ZR2240W.EDID");
        }

        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestPreCondition()
        {
            Log.Message("Test PreConditions start.");
            HotPlugDeepColorPanels();

            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, CurrentConfig))
                Log.Success("Successfully Applied {0}", CurrentConfig.GetCurrentConfigStr());
        }

        [Test(Type = TestType.PostCondition, Order = 12)]
        public virtual void TestCleanup()
        {
            Log.Message("Cleanup start.");
            base.CurrentConfig.PluggableDisplayList.ForEach(curDisp =>
            {
                Log.Message("HotUnplug {0} Deepcolor supported panel.", curDisp);
                base.HotUnPlug(curDisp);
            });
        }

        protected void InstallDirectX()
        {
            if (Directory.Exists(@"C:\Program Files (x86)\Microsoft DirectX SDK (June 2010)") || (Directory.Exists(@"C:\Program Files\Microsoft DirectX SDK (June 2010)")))
            {
                Log.Message("DirectX is installed");
            }
            else
            {
                Log.Message("Installing DirectX SDK. Do not touch any UI buttons.");
                Process p = Process.Start(base.ApplicationManager.ApplicationSettings.DirectX, "/U");
                p.WaitForExit();
                Log.Message("Installion of  DirectX SDK was successfull");
            }
        }
        protected void EnableDeepColor(DeepColorAppType AppType)
        {
            switch (AppType)
            {
                case DeepColorAppType.FP16:
                    EnableFP16();
                    break;
                case DeepColorAppType.DPApplet:
                    EnableDPApplet();
                    break;
                case DeepColorAppType.N10BitScanOut:
                    Enable10BitScanout();
                    break;
                default:
                    Log.Fail("Wrong AppType {0} passed.", AppType);
                    break;
            }
        }
        protected void DisableDeepColor(DeepColorAppType AppType)
        {
            switch (AppType)
            {
                case DeepColorAppType.FP16:
                    DisableFP16();
                    break;
                case DeepColorAppType.DPApplet:
                    DisableDPApplet();
                    break;
                case DeepColorAppType.N10BitScanOut:
                    Disable10BitScanout();
                    break;
                default:
                    Log.Fail("Wrong AppType {0} passed.", AppType);
                    break;
            }
        }
        protected void EnableFP16()
        {
            //Enabling Deep color Feature
            Log.Message(true, "Enabling Deepcolor Feature : FP16");
            DeepColorParams DPParam = new DeepColorParams();
            DPParam.DeepColorAppType = DeepColorAppType.FP16;
            DPParam.DeepColorOptions = DeepColorOptions.Enable;
            AccessInterface.SetFeature<DeepColorParams>(Features.DeepColor, Action.Set, DPParam);

            Log.Success("Enabled Deepcolor Feature : FP16");
        }

        protected void DisableFP16()
        {
            Log.Message(true, "Disabling Deepcolor Feature : FP16");
            
            DeepColorParams DPParam = new DeepColorParams();
            DPParam.DeepColorAppType = DeepColorAppType.FP16;
            DPParam.DeepColorOptions = DeepColorOptions.Disable;
            AccessInterface.SetFeature<DeepColorParams>(Features.DeepColor, Action.Set, DPParam);

            Log.Message("Disabled Deepcolor Feature : FP16");
        }

        protected void MoveFP16(DisplayHierarchy pDispHierarchy)
        {
            //Moving Deep color Instant
            Log.Message(true, "Moving Deepcolor FP16 player to {0}", pDispHierarchy);
            DeepColorParams DPParam = new DeepColorParams();
            DPParam.DeepColorAppType = DeepColorAppType.FP16;
            DPParam.CurrentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            DPParam.DeepColorOptions = DeepColorOptions.Move;
            DPParam.DisplayHierarchy = pDispHierarchy;
            AccessInterface.SetFeature<DeepColorParams>(Features.DeepColor, Action.Set, DPParam);

            Log.Success("Moved Deepcolor Feature to {0}", pDispHierarchy);
        }

        protected void CloseApp(DeepColorAppType AppType)
        {
            //Closing Deep color App
            Log.Message(true, "Closing DeepColor App: {0}", AppType);
            DeepColorParams DPParam = new DeepColorParams();
            DPParam.DeepColorAppType = AppType;
            DPParam.DeepColorOptions = DeepColorOptions.Close;
            AccessInterface.SetFeature<DeepColorParams>(Features.DeepColor, Action.Set, DPParam);

            Log.Success("Closed DeepColor App: {0}", AppType);
        }

        protected void EnableDPApplet()
        {
            Log.Message(true, "Enabling Deepcolor Feature : DPApplet");

            DeepColorParams DPParam = new DeepColorParams();
            DPParam.DeepColorAppType = DeepColorAppType.DPApplet;
            DPParam.DeepColorOptions = DeepColorOptions.Enable;
            AccessInterface.SetFeature<DeepColorParams>(Features.DeepColor, Action.Set, DPParam);

            ChangeMode();

            Log.Success("Enabled Deepcolor Feature : DPApplet");
        }

        protected void DisableDPApplet()
        {
            Log.Message(true, "Disabling Deepcolor Feature : DPApplet");
            DeepColorParams DPParam = new DeepColorParams();
            DPParam.DeepColorAppType = DeepColorAppType.DPApplet;
            DPParam.DeepColorOptions = DeepColorOptions.Disable;
            AccessInterface.SetFeature<DeepColorParams>(Features.DeepColor, Action.Set, DPParam);

            ChangeMode();

            Log.Success("Disabled Deepcolor Feature : DPApplet");
        }

        protected void ChangeMode()
        {
            DisplayConfig pDisplayConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            // Finding Supported modes for all displays
            List<DisplayModeList> displayModeList_OSPage = GetEDIDModes(pDisplayConfig);
            
            pDisplayConfig.CustomDisplayList.ForEach(dp =>
            {
                DisplayMode displayMode;
                List<DisplayMode> supportedMode = displayModeList_OSPage.Where(dML => dML.display == dp).Select(dML => dML.supportedModes).FirstOrDefault();

                if (supportedMode.Count > 0)
                {
                    // Get Current DisplayMode.
                    DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Find(dp1 => dp1.DisplayType == dp);
                    DisplayMode currentDisplayMode_OSPage = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);

                    // Apply resolution other than current resolution for deepcolor to get disabled/enabled.
                    if (!currentDisplayMode_OSPage.Equals(supportedMode.First(), currentDisplayMode_OSPage))
                        displayMode = supportedMode.First();
                    else
                        displayMode = supportedMode.Last();


                    Log.Message("Setting Mode : {0} for {1}", displayMode.ToString(), displayMode.display);
                    if (!AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, displayMode))
                        Log.Fail("Fail to apply Mode");
                    else
                        Log.Success("Mode applied successfully");
                }
            });
        }

        private List<DisplayModeList> GetEDIDModes(DisplayConfig pDisplayConfig)
        {
            List<DisplayModeList> trimmedList = new List<DisplayModeList>();
            List<DisplayModeList> displayModeList_OSPage = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, pDisplayConfig.CustomDisplayList);

            displayModeList_OSPage.ForEach(currentModeList =>
            {
                DisplayModeList tempModeList = new DisplayModeList();
                tempModeList.display = currentModeList.display;
                currentModeList.supportedModes.ForEach(eachMode =>
                {
                    if (eachMode.ScalingOptions.Contains((uint)ScalingOptions.Maintain_Display_Scaling))
                    {
                        DisplayMode tempMode = eachMode;
                        tempMode.ScalingOptions.Clear();
                        tempMode.ScalingOptions.Add((uint)ScalingOptions.Maintain_Display_Scaling);
                        tempModeList.supportedModes.Add(tempMode);
                    }
                });

                trimmedList.Add(tempModeList);

            });

            return trimmedList;
        }

        protected void Enable10BitScanout()
        {
            Log.Message(true, "Enabling Deepcolor Feature : 10 Bit Scanner");

            DisplayConfig dispConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            DeepColorParams DPParam = new DeepColorParams();
            DPParam.CurrentConfig = dispConfig;
            DPParam.DeepColorAppType = DeepColorAppType.N10BitScanOut;
            DPParam.DeepColorOptions = DeepColorOptions.Enable;
            AccessInterface.SetFeature<DeepColorParams>(Features.DeepColor, Action.Set, DPParam);

            //waiting for 15 Sec
            Thread.Sleep((15) * 1000);

            Log.Success("Enabled Deepcolor Feature : 10 Bit Scanner");
        }

        protected void Disable10BitScanout()
        {
            Log.Message(true, "Disabling Deepcolor Feature : 10 bit Scanner");
            DisplayConfig dispConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            DeepColorParams DPParam = new DeepColorParams();
            DPParam.CurrentConfig = dispConfig;
            DPParam.DeepColorAppType = DeepColorAppType.N10BitScanOut;
            DPParam.DeepColorOptions = DeepColorOptions.Disable;
            AccessInterface.SetFeature<DeepColorParams>(Features.DeepColor, Action.Set, DPParam);

            Log.Success("Disabled Deepcolor Feature : 10 bit scanner");
        }

        /// <summary>
        /// playerhierarchy : Indicates the player in which the deepcolor application need to be played.
        /// DispConfig: Indicates the display configuration.
        /// </summary>
        protected void CheckDeepColorconditions(DisplayInfo DispInfo, PipePlaneParams pipePlane, DeepColorAppType DeepColorAppType, bool enableStatus, DisplayConfig  DispConfig,DisplayHierarchy playerhierarchy)
        {  
            //check if the mode is extended mode.
            Boolean _isExtendedMode = DispConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Extended ? true : false;
            DisplayHierarchy displayhierarchy = DispConfig.GetDispHierarchy(DispInfo.DisplayType);
            if (_isExtendedMode && enableStatus == true)
            {
                if (DeepColorAppType == DeepColorAppType.N10BitScanOut && base.MachineInfo.OS.Type == OSType.WINTHRESHOLD)
                {
                    if (displayhierarchy != playerhierarchy)
                    {
                        enableStatus = false;
                    }
                }
                if (DeepColorAppType == DeepColorAppType.FP16)
                {
                    enableStatus = false;
                    if (displayhierarchy == playerhierarchy)
                    {
                        enableStatus = true;
                    }

                }
            }

            // dee DEEP COLOR Enable for DVMU
            if (DispInfo.DvmuPort != DVMU_PORT.None)
            {
                InfoFrame _infoFrame = new InfoFrame();
                _infoFrame.infoFrameType = InfoFrameType.GCP;
                _infoFrame.functionInfoFrame = FunctionInfoFrame.GetDeepColor;
                _infoFrame.port = DispInfo.DvmuPort;

                Thread.Sleep(7000);
                InfoFrame deepColorInfoframe = AccessInterface.GetFeature<InfoFrame, InfoFrame>(Features.InfoFrameParsing, Action.GetMethod, Source.AccessAPI, _infoFrame);

                string bpc = null;
                deepColorInfoframe.infoFrameData.ForEach(dpf => { Log.Message("the dfp is {0} and bpc {1}", dpf, bpc); bpc += dpf; });
                if (enableStatus)
                {

                    if (bpc.Contains(HDMI_BPC_VALUE.ToString()))
                        Log.Success("Deep color Enabled , DVMU BPC : {0}", bpc);
                    else
                        Log.Alert("Deep Color is not enabled on DVMU : {0} BPC : {1}", DispInfo.DisplayType, bpc);
                }
                else
                {
                    Log.Message("bpc: {0} amd {1}", bpc, HDMI_BPC_VALUE);
                    if (bpc.Contains(HDMI_BPC_VALUE.ToString()))
                        Log.Success("Deep color Enabled , DVMU BPC : {0}", bpc);
                    else
                        Log.Alert("Deep Color is not enabled on DVMU : {0} BPC : {1}", DispInfo.DisplayType, bpc);
                }
            }
            CheckDeepRegisterStatus(DispInfo, pipePlane, DeepColorAppType, enableStatus);
            CheckDitheringBPC(DispInfo, pipePlane);
        }

        int GetSourceBPC(DeepColorAppType AppType, bool enableStatus)
        {
            int sourceBPC = 8;

            if (enableStatus)
            {
                if (AppType == DeepColorAppType.N10BitScanOut)
                {
                    sourceBPC = 10;
                }
                else if (AppType == DeepColorAppType.FP16 || AppType == DeepColorAppType.DPApplet)
                {
                    sourceBPC = 16;
                }
            }

            return sourceBPC;
        }

        private void CheckDeepRegisterStatus(DisplayInfo dispInfo, PipePlaneParams pipePlane, DeepColorAppType AppType, bool enableStatus)
        {
            int CurrentBPCValue = 0;
            int MaxEdidBPC = 0;
            string eventName = default(string);
            int sourceBPC = GetSourceBPC(AppType, enableStatus);
            
            Log.Message(true, "Verifying DeepColor status for {0} ", dispInfo.DisplayType);

            MaxEdidBPC = dispInfo.ColorInfo.MaxDeepColorValue;
            CurrentBPCValue = Math.Min(MaxEdidBPC, sourceBPC);

            if (dispInfo.DisplayType == DisplayType.HDMI && CurrentBPCValue == 10)
            {
                Log.Message("Max BPC value for HDMI must not be 10, doing the min with 8BPC."); //This logic need to be changed when 10b HDMI is enabled.
                CurrentBPCValue = Math.Min(8, sourceBPC);
            }

            if (dispInfo.DisplayType == DisplayType.HDMI && CurrentBPCValue > 8)//Replace this check with Pixel Clock
            {
                DisplayMode targetResolution = base.GetTargetResolution(dispInfo.DisplayType);

                if (targetResolution.HzRes >= 1920 && targetResolution.VtRes > 1080)
                {
                    CurrentBPCValue = Math.Min(8, sourceBPC);
                }
            }

            eventName = "BPC" + "_" + CurrentBPCValue.ToString();  //ex: BPC_12 or BPC_10

            if (VerifyRegisters(eventName, pipePlane.Pipe, pipePlane.Plane, dispInfo.Port, true))
                Log.Success("DeepColor Register values matched for {0}.", dispInfo.DisplayType);
        }

        protected bool CheckDitheringBPC(DisplayInfo pDisplay, PipePlaneParams pPipePlane)
        {
            if (base.MachineInfo.PlatformDetails.Platform == Platform.BDW)
            {
                Dictionary<string, uint> ditheringBPC = new Dictionary<string, uint>() { { "0", 8 }, { "20", 10 }, { "40", 6 }, { "60", 12 } };
                Log.Message("{0} : Dithering Conditions", pDisplay.DisplayType);
                if (VerifyRegisters("DITHERING_ENABLE", pPipePlane.Pipe, pPipePlane.Plane, pDisplay.Port, false))
                {
                    Log.Success("Dithering is enabled FOR {0}", pDisplay.DisplayType);

                    EventInfo returnEventInfo = GetEventInfo(DITHERING_BPC, pPipePlane.Pipe, pPipePlane.Plane, pDisplay.Port);
                    foreach (RegisterInf reginfo in returnEventInfo.listRegisters)
                    {
                        DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
                        driverData.input = Convert.ToUInt32(reginfo.Offset, 16);
                        DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
                        if (!AccessInterface.SetFeature<bool, DriverEscapeParams>(Features.DriverEscape, Action.SetMethod, driverParams))
                            Log.Abort("Failed to read Register with offset as {0}", driverData.input);
                        else
                        {
                            uint bit = Convert.ToUInt32(reginfo.Bitmap, 16);
                            Log.Verbose("Bitmap in uint = {0}", bit);

                            uint hex = Convert.ToUInt32(String.Format("{0:X}", driverData.output), 16);
                            Log.Verbose("value from reg read in uint = {0}", hex);

                            string value = String.Format("{0:X}", hex & bit);
                            Log.Verbose("after bitmap = {0}", value);

                            if (ditheringBPC.Keys.Contains(value))
                            {
                                uint dithering_bpc_value = ditheringBPC[value];
                                Log.Message("Dithering BPC: {0}", dithering_bpc_value);
                                if (pDisplay.ColorInfo.MaxDeepColorValue == dithering_bpc_value)
                                {
                                    Log.Success("Dithering BPC {0} for {1} match the expected Value", dithering_bpc_value, pDisplay.DisplayType);
                                }
                                else
                                {
                                    Log.Fail("Dithering BPC {0} for {1} does not match the expected Value {2}", dithering_bpc_value, pDisplay.DisplayType, pDisplay.ColorInfo.MaxDeepColorValue);
                                }
                            }
                            else
                            {
                                Log.Fail("{0} is not an entry in the dictionary", value);
                            }
                        }
                    }
                    return true;
                }
                else
                {
                    Log.Alert("Dithering BPC is not enabled for {0}",pDisplay.DisplayType);
                }
            }
            return false;
        }
        
        protected EventInfo GetEventInfo(string pRegisterEvent, PIPE pPipe, PLANE pPlane, PORT pPort)
        {
            Log.Message("Verifying Register for event : {0} Pipe : {1}", pRegisterEvent, pPipe);

            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = pPipe;
            eventInfo.plane = pPlane;
            eventInfo.port = pPort;
            eventInfo.eventName = pRegisterEvent;
            EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);
            return returnEventInfo;
        }

        protected PipePlaneParams GetPipePlane(DisplayInfo pDisplayInfo)
        {
            // Geting PIPE , Plane information for pannels
            PipePlaneParams pipePlane = new PipePlaneParams(pDisplayInfo.DisplayType);
            pipePlane = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane);
            Log.Message("For display : {0}  @@@  PORT : {1} @@@ PIPE : {2} @@@ PLANE : {3}", pDisplayInfo.DisplayType, pDisplayInfo.Port, pipePlane.Pipe, pipePlane.Plane);

            return pipePlane;
        }

        protected bool Hotplug(FunctionName FuncArg, DisplayType DisTypeArg, DVMU_PORT PortArg)
        {
            HotPlugUnplug hotPlugUnplug = new HotPlugUnplug(FuncArg, PortArg, "HDMI_DELL_U2711_XVYCC.EDID");
            bool status = AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, hotPlugUnplug);

            return status;
        }

        protected bool CheckEnumeratedDisplayContents(DisplayType DispType)
        {
            if (base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == DispType).Select(dI => dI.DisplayType).FirstOrDefault() != DisplayType.None)
                return true;
            else
                return false;
        }

        protected void HotPlugDeepColorPanels()
        {
            base.CurrentConfig.PluggableDisplayList.ForEach(curDisp =>
            {
                Log.Message("Hotplug {0} Deepcolor supported panel.", curDisp);
                base.HotPlug(curDisp, _defaultEDIDMap[curDisp]);
            });
        }
    }
}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      