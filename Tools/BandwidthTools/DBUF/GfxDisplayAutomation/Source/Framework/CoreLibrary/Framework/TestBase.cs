namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System;
    using System.IO;
    using System.Threading;

    public class TestBase
    {
        private DisplayConfig _currentConfig = null;
        private int _newInvokeMethodIdx = -1;
        protected bool _verifyWatermark = false;

        protected IApplicationManager ApplicationManager { get; private set; }
        protected IAccessInterface AccessInterface
        {
            get { return this.ApplicationManager.AccessInterface; }
        }
        protected MachineInfo MachineInfo
        {
            get { return this.ApplicationManager.MachineInfo; }
        }
        private List<DisplayInfo> _enumeratedDisplays;
        public List<DisplayInfo> EnumeratedDisplays
        {
            get
            {
                if (this.ApplicationManager != null)
                {
                    _enumeratedDisplays = this.ApplicationManager.ParamInfo[ArgumentType.Enumeration] as List<DisplayInfo>;
                    return _enumeratedDisplays;
                }
                else
                    return null;
            }
        }
        protected DisplayConfig CurrentConfig
        {
            get
            {
                if (null == this._currentConfig)
                {
                    this._currentConfig = new DisplayConfig();
                    this._currentConfig.EnumeratedDisplays = this.ApplicationManager.ParamInfo.Get<List<DisplayInfo>>(ArgumentType.Enumeration);
                    this._currentConfig.PluggedDisplayList = new List<DisplayType>();
                    DisplayConfigList dcList = this.ApplicationManager.ParamInfo.Get<DisplayConfigList>(ArgumentType.Config);
                    if (null != dcList)
                        this._currentConfig.ConfigType = dcList.First();
                    DisplayList displayList = this.ApplicationManager.ParamInfo.Get<DisplayList>(ArgumentType.Display);
                    if (null == displayList && this._currentConfig.ConfigType == DisplayConfigType.None)
                    {
                        Log.Verbose("Display Config & Display Type(s) not passed in command line");
                        Log.Verbose("Display Type derived from enumerated list");
                        this._currentConfig.DisplayList = this._currentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType != DisplayType.None).Select(dI => dI.DisplayType).ToList();
                        this._currentConfig.ConfigType = this.DeriveConfigType();
                        Log.Verbose("Display Config assumed to {0}", this._currentConfig.ConfigType);
                    }
                    else
                    {
                        if (null != displayList)
                            this._currentConfig.DisplayList = displayList.Where(d => d != DisplayType.None).ToList();
                        if (this._currentConfig.ConfigType == DisplayConfigType.None)
                        {
                            Log.Verbose("Display Config not passed in command line");
                            this._currentConfig.ConfigType = this.DeriveConfigType();
                            Log.Verbose("Display Config assumed to {0}", this._currentConfig.ConfigType);
                        }
                    }

                    this._currentConfig.PrimaryDisplay = this._currentConfig.DisplayList.GetDisplay(DisplayHierarchy.Display_1);
                    this._currentConfig.SecondaryDisplay = this._currentConfig.DisplayList.GetDisplay(DisplayHierarchy.Display_2);
                    this._currentConfig.TertiaryDisplay = this._currentConfig.DisplayList.GetDisplay(DisplayHierarchy.Display_3);
                }
                else
                {
                    this._currentConfig.EnumeratedDisplays = this.ApplicationManager.ParamInfo.Get<List<DisplayInfo>>(ArgumentType.Enumeration);
                    this._currentConfig.PluggedDisplayList = DisplayExtensions.pluggedDisplayList;
                }
                #region Add Pluggable Display List and Display Sequence.
                this._currentConfig.PluggableDisplayList = new List<DisplayType>();
                this._currentConfig.displaySequence = new DisplaySequence();

                int index = 0;
                
                foreach (DisplayType DT in this._currentConfig.DisplayList)
                {
                    this._currentConfig.displaySequence.Add(index++, DT);
                    if (!ApplicationManager.ApplicationSettings.UseDivaFramework && !ApplicationManager.ApplicationSettings.UseULTFramework && !ApplicationManager.ApplicationSettings.UseSHEFramework)    //SHE
                    {// Add DVMU Pluggable Display List
                        DVMUPluggableDisplay DISP = DVMUPluggableDisplay.None;
                        if (Enum.TryParse<DVMUPluggableDisplay>(DT.ToString(), out DISP))
                        {
                            this._currentConfig.displaySequence.PluggableDisplayList.Add(DT);
                            if (!(_currentConfig.EnumeratedDisplays.Any(dI => dI.DisplayType == DT)))
                            {
                                this._currentConfig.PluggableDisplayList.Add(DT);
                            }
                        }
                    }
                    else
                    {
                        // Add DFT Pluggable Display List
                        DFTPluggableDisplay DISP = DFTPluggableDisplay.None;
                        if (Enum.TryParse<DFTPluggableDisplay>(DT.ToString(), out DISP))
                        {
                            this._currentConfig.displaySequence.PluggableDisplayList.Add(DT);
                            if (!(_currentConfig.EnumeratedDisplays.Any(dI => dI.DisplayType == DT)))
                            {
                                this._currentConfig.PluggableDisplayList.Add(DT);
                            }
                        }
                    }
                }
                #endregion

                return this._currentConfig;
            }
        }
        protected void SkipToMethod(int argNewIndex)
        {
            this._newInvokeMethodIdx = argNewIndex - 1;
        }
        #region Common Routines
        protected void AssertDriverState(Features argFeature, DriverState argState, int[] argStepNumbers)
        {
            this.CommonRoutines.AssertDriverState(argFeature, argState, argStepNumbers);
        }
        protected bool ChangeDriverState(Features argFeature, DriverState argState, int[] argStepNumbers)
        {
            return this.CommonRoutines.ChangeDriverState(argFeature, argState, argStepNumbers);
        }
        protected void DisableNVerifyIGDWithDTCM(int argStepNumber)
        {
            this.CommonRoutines.DisableNVerifyIGDWithDTCM(argStepNumber);
        }
        protected void EnableNVerifyIGDBasic(int argStepNumber)
        {
            this.CommonRoutines.EnableNVerifyIGDBasic(argStepNumber);
        }
        protected bool InvokePowerEvent(PowerParams argPowerParams, PowerStates argState)
        {
            return this.CommonRoutines.InvokePowerEvent(argPowerParams, argState);
        }
        protected void EventResult(PowerStates argState, bool argResult)
        {
            this.CommonRoutines.EventResult(argState, argResult);
        }
        protected void GetOSDriverVersionNStatus(List<string> argDriverNameStrList)
        {
            this.CommonRoutines.GetOSDriverVersionNStatus(argDriverNameStrList);
        }
        protected void GetOSDriverVersionNStatus(List<string> argDriverNameStrList, string argDriverVersion)
        {
            this.CommonRoutines.GetOSDriverVersionNStatus(argDriverNameStrList, argDriverVersion);
        }
        protected void GetOSDriverVersionNStatus(List<string> argDriverNameStrList, bool argNullDriverVersion)
        {
            this.CommonRoutines.GetOSDriverVersionNStatus(argDriverNameStrList, argNullDriverVersion);
        }
        protected bool CheckOSDriverVersionNStatus(List<string> argDriverNameStrList)
        {
            return this.CommonRoutines.CheckOSDriverVersionNStatus(argDriverNameStrList);
        }
        protected List<uint> ListEnumeratedDisplays()
        {
            return this.CommonRoutines.ListEnumeratedDisplays();
        }
        protected void UninstallThruUI()
        {
            this.CommonRoutines.UninstallThruUI();
        }
        protected bool InstallThruUI(string driverPath)
        {
            return this.CommonRoutines.InstallThruUI(driverPath);
        }
        protected void SetBCDEditOptions(string disableIntegrityChecks, string testSigning)
        {
            this.CommonRoutines.SetBCDEditOptions(disableIntegrityChecks, testSigning);
        }
        protected void CheckBCDEditOptions(string loadOptions, string testSigning)
        {
            this.CommonRoutines.CheckBCDEditOptions(loadOptions, testSigning);
        }
        #endregion

        [Framework(ComponentType.ApplicationManager)]
        private void SetApplicationManager(IApplicationManager argManager)
        {
            this.ApplicationManager = argManager;
        }
        [Framework(ComponentType.CurrentMethodIndex)]
        private void SetCurrentMethodIndex(int argCurrentMethodIndex)
        {
            this.ApplicationManager.AccessInterface.CurrentMethodIndex = argCurrentMethodIndex;
        }
        private CommonRoutines CommonRoutines
        {
            get { return new CommonRoutines(this.ApplicationManager); }
        }
        private DisplayConfigType DeriveConfigType()
        {
            int displayCount = this._currentConfig.DisplayList.Count > 3 ? 3 : this._currentConfig.DisplayList.Count;
            int platformBasedCount = DisplayExtensions.GetDisplaysCount(this.MachineInfo.PlatformDetails.Platform);
            if (displayCount > platformBasedCount)
                displayCount = platformBasedCount;
            return DisplayExtensions.GetConfigTypeByCount(displayCount);

        }
        protected bool VerifyRegisters(string registerEvent, PIPE pipe, PLANE plane, PORT port, bool printStatusLog)
        {
            bool match = false;
            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = pipe;
            eventInfo.plane = plane;
            eventInfo.port = port;
            eventInfo.eventName = registerEvent;

            Log.Verbose("Event being checked = {0}", eventInfo.eventName);
            EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);

            foreach (RegisterInf reginfo in returnEventInfo.listRegisters)
            {
                Log.Message("Offset being checked = {0} Bitmap being checked {1}  Value to be got = {2}", reginfo.Offset, reginfo.Bitmap, reginfo.Value);
                DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
                driverData.input = Convert.ToUInt32(reginfo.Offset, 16);
                DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
                if (!AccessInterface.SetFeature<bool, DriverEscapeParams>(Features.DriverEscape, Action.SetMethod, driverParams))
                    Log.Abort("Failed to read Register with offset as {0}", driverData.input);
                else
                    if (!CompareRegisters(driverData.output, reginfo))
                    {
                        if (printStatusLog == true)
                            Log.Fail("Register with offset {0} doesnot match required values", driverData.input.ToString("X"));

                        match = true;
                    }
            }
            if (match)
                return false;
            return true;
        }
        protected bool CompareRegisters(uint argDriverData, RegisterInf argRegInfo)
        {
            uint bit = Convert.ToUInt32(argRegInfo.Bitmap, 16);
            string binary = argDriverData.ToString("X");
            Log.Verbose("value from reg read in hex = {0}", binary);
            uint hex = Convert.ToUInt32(String.Format("{0:X}", argDriverData), 16);
            string valu = String.Format("{0:X}", hex & bit);
            Log.Verbose("after bitmap = {0}", valu);
            if (String.Equals(valu, argRegInfo.Value))
                return true;
            return false;
        }
        protected uint GetRegisterValue(string registerEvent, PIPE pipe, PLANE plane, PORT port)
        {
            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = pipe;
            eventInfo.plane = plane;
            eventInfo.port = port;
            eventInfo.eventName = registerEvent;

            Log.Verbose("Event being checked = {0}", eventInfo.eventName);
            EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);

            RegisterInf reginfo = returnEventInfo.listRegisters[0];
            Log.Verbose("Offset being checked = {0} Bitmap {1}", reginfo.Offset, reginfo.Bitmap);

            return reginfo.BitmappedValue;
        }
        protected uint GetRegisterValue(uint RegisterValue, int start, int end)
        {
            uint value = RegisterValue << (31 - end);
            value >>= (31 - end + start);
            return value;
        }
        protected bool HotPlug(DisplayType dispType)
        {
            return HotPlug(dispType, string.Empty, false);
        }
        protected bool HotPlug(DisplayType dispType, bool IsLowPower)
        {
            return HotPlug(dispType, string.Empty, IsLowPower);
        }
        protected bool HotPlug(DisplayType dispType, string edid)
        {
            return HotPlug(dispType, edid, false);
        }

        protected bool SwitchToAC(bool InLowPowerState = false) //SHE
        {

            Log.Message("SHE - Performing Switching of Power State TO AC ");
            bool status = false;
            string plugDelay = "0";
            if (InLowPowerState)
            {
                plugDelay = "15";
            }
           
            SHEDLL.serialPortAccess portaccess = new SHEDLL.serialPortAccess();

            status = portaccess.SerialWrite("11", plugDelay);
            if (status == true)
            {
                Log.Success("SHE - Switched Power State TO AC");
            }
            else
            {
                Log.Fail("SHE - Failed Switched Power State TO AC");
            }            
            return status;            
        }   

        protected bool SwitchToDC(bool InLowPowerState = false)  //SHE
        {

            Log.Message("SHE - Performing Switching of Power State TO DC ");
            bool status = false;
            string plugDelay = "0";
            if (InLowPowerState)
            {
                plugDelay = "15";
            }

            SHEDLL.serialPortAccess portaccess = new SHEDLL.serialPortAccess();

            status = portaccess.SerialWrite("12", plugDelay);
            if (status == true)
            {
                Log.Success("SHE - Switched Power State TO DC");
            }
            else
            {
                Log.Fail("SHE - Failed Switched Power State TO DC");
            }
            return status;
        }
        protected bool HotPlug(DisplayType dispType, string edid, bool IsLowPower)
        {
            HotPlugUnplug _HotPlugUnplug = new HotPlugUnplug();
            _HotPlugUnplug.display = dispType;
            _HotPlugUnplug.FunctionName = FunctionName.PLUG;
            _HotPlugUnplug.InLowPowerState = IsLowPower;
            if (!string.IsNullOrEmpty(edid))
            {
                _HotPlugUnplug.EdidFilePath = _HotPlugUnplug.EdidFilePath + edid;
            }
            if (!ApplicationManager.ApplicationSettings.UseDivaFramework && !ApplicationManager.ApplicationSettings.UseULTFramework && !ApplicationManager.ApplicationSettings.UseSHEFramework)    //SHE
            {// If Plugging display using DVMU
                return AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, _HotPlugUnplug);
            }
            else
            {//Plugging display through DFT framework
                return AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.SimulatedHotPlugDisplay, Action.SetMethod, _HotPlugUnplug);
            }
        }
        protected bool HotPlug(DisplayType dispType, bool useWindowsID, uint windowsMonitorID, string argEdidName, bool IsLowerPower = false, string argDpcdFilePath = "")
        {
            HotPlugUnplug obj = new HotPlugUnplug(FunctionName.PLUG, dispType, useWindowsID, windowsMonitorID, argEdidName, IsLowerPower, argDpcdFilePath);
            bool status = AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.SimulatedHotPlugDisplay, Action.SetMethod, obj);

            return status;
        }
        protected bool HotUnPlug(DisplayType dispType)
        {
            return HotUnPlug(dispType, false);
        }
        protected bool HotUnPlug(DisplayType dispType, bool IsLowPower)
        {
            Log.Message("Performing HotUnPlug of display {0} ", dispType);
            HotPlugUnplug _HotPlugUnplug = new HotPlugUnplug();
            _HotPlugUnplug.FunctionName = FunctionName.UNPLUG;
            _HotPlugUnplug.display = dispType;
            _HotPlugUnplug.InLowPowerState = IsLowPower;
            if (!ApplicationManager.ApplicationSettings.UseDivaFramework && !ApplicationManager.ApplicationSettings.UseULTFramework && !ApplicationManager.ApplicationSettings.UseSHEFramework)    //SHE
            {//Unplugging display using DVMU
                return AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, _HotPlugUnplug);
            }
            //Unplugging Dispaly using DFT framework
            return AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.SimulatedHotPlugDisplay, Action.SetMethod, _HotPlugUnplug);
        }
        protected void EnableDFT(bool status)
        {
            HotPlugUnplug argSimulationFramework = new HotPlugUnplug(FunctionName.SimulationFramework, status);
            AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.SimulatedHotPlugDisplay, Action.SetMethod, argSimulationFramework);
        }
        protected void InitializeHotplugFramework()
        {
            if (!ApplicationManager.ApplicationSettings.UseDivaFramework && !ApplicationManager.ApplicationSettings.UseULTFramework && !ApplicationManager.ApplicationSettings.UseSHEFramework)   //SHE
            {
                HotPlugUnplug HotPlugUnplug = new HotPlugUnplug(FunctionName.OPEN, DisplayType.HDMI, DVMU_PORT.PORTA);
                AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, HotPlugUnplug);
            }
            else
            {
                HotPlugUnplug argSimulationFramework = new HotPlugUnplug(FunctionName.SimulationFramework, true);
                AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.SimulatedHotPlugDisplay, Action.SetMethod, argSimulationFramework);

                HotPlugUnplug argSimulationFeature = new HotPlugUnplug(FunctionName.SimulationFeature, true);
                AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.SimulatedHotPlugDisplay, Action.SetMethod, argSimulationFeature);
            }
        }
        protected void CleanUpHotplugFramework()
        {
            if (ApplicationManager.ApplicationSettings.UseDivaFramework || ApplicationManager.ApplicationSettings.UseULTFramework && ApplicationManager.ApplicationSettings.UseSHEFramework)   //SHE
            {
                HotPlugUnplug argSimulationFeature = new HotPlugUnplug(FunctionName.SimulationFeature, false);
                AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.SimulatedHotPlugDisplay, Action.SetMethod, argSimulationFeature);
            }
        }
        protected DisplayMode GetTargetResolution(DisplayType display)
        {
            DisplayMode targetMode = new DisplayMode();
            DisplayInfo displayInfo = this.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
            DisplayMode currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            Log.Message("Current Resolution is {0}", currentMode.ToString());

            ScalingOptions scalingOptionSet = (ScalingOptions)Enum.Parse(typeof(ScalingOptions), currentMode.ScalingOptions[0].ToString());

            Log.Message("Scaling value is {0}", currentMode.ScalingOptions[0].ToString());
            Log.Message("Current Scaling is {0}", scalingOptionSet.ToString());

            Log.Message("Native Resolution is {0}", displayInfo.DisplayMode.ToString());

            if (scalingOptionSet == ScalingOptions.Center_Image || scalingOptionSet == ScalingOptions.Maintain_Aspect_Ratio || scalingOptionSet == ScalingOptions.Scale_Full_Screen)
            {
                targetMode = displayInfo.DisplayMode;
            }
            else if (scalingOptionSet == ScalingOptions.Maintain_Display_Scaling || scalingOptionSet == ScalingOptions.Customize_Aspect_Ratio)
            {
                targetMode = currentMode;
            }
            else
            {
                Log.Fail("Wrong Scaling option passed. {0}", scalingOptionSet);
            }
            return targetMode;
        }
        protected void CheckWatermark(DisplayType currentDisplay)
        {
            if (this._verifyWatermark == true)
            {
                DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
                CheckWatermark(currentDisplay, currentConfig);
            }
        }
        protected void CheckWatermark(DisplayType currentDisplay, DisplayConfig currentConfig)
        {
            if (this._verifyWatermark == true)
            {
                Watermark_Params watermarkParams = new Watermark_Params(currentDisplay);
                watermarkParams.DisplayParametersList = new Dictionary<DisplayType, Watermark_Params.DisplayParams>();
                watermarkParams.CurrentConfig = currentConfig;

                currentConfig.CustomDisplayList.ForEach(display =>
                {
                    Watermark_Params.DisplayParams disp = new Watermark_Params.DisplayParams();

                    PipePlaneParams pipePlaneParam = new PipePlaneParams(display);
                    disp.pipePlaneParams = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlaneParam);

                    DisplayInfo displayInfo = CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
                    disp.displayMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);

                    watermarkParams.DisplayParametersList.Add(display, disp);
                });

                if (AccessInterface.GetFeature<bool, Watermark_Params>(Features.Watermark, Action.GetMethod, Source.AccessAPI, watermarkParams))
                    Log.Success("Watermark values matched for " + watermarkParams.CurrentConfig.ToString());
                else
                    Log.Fail("Watermark values not matched for " + watermarkParams.CurrentConfig.ToString());
            }
        }
        protected DisplayType GetInternalDisplay()
        {
            return EnumeratedDisplays.Find(DI => DI.displayExtnInformation.Equals(DisplayExtensionInfo.Internal)).DisplayType;
        }
        protected void OverlayOperations(DisplayHierarchy displayHierarchy, DisplayConfig displayConfig, OverlayPlaybackOptions playOption)
        {
            if (playOption != OverlayPlaybackOptions.ClosePlayer)
            {
                List<DisplayModeList> allModeList = new List<DisplayModeList>();
                allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, displayConfig.CustomDisplayList);
                if (allModeList == null)
                    Log.Abort("Mode list is empty");

                if ((displayConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Single) || (displayConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
                {
                    DisplayType display = allModeList.First().display;
                    List<DisplayMode> supportedModeList = allModeList.First().supportedModes;

                    DisplayInfo displayInfo = this.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
                    DisplayMode currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);

                    if (currentMode.HzRes < 1024 || currentMode.VtRes < 768)
                    {
                        Log.Alert("Current resolution is {0} which is less than 1024*768", currentMode.ToString());
                        for (int i = 0; i < supportedModeList.Count; i++)
                        {
                            if (supportedModeList[i].HzRes >= 1024 && supportedModeList[i].VtRes >= 768)
                            {
                                if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, supportedModeList[i]))
                                    Log.Success("Mode applied Successfully");
                                else
                                    Log.Fail("Fail to apply Mode");
                                break;
                            }
                        }
                    }
                }
                else if (displayConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Extended)
                {
                    for (int j = 0; j < (int)displayHierarchy + 1; j++)
                    {
                        DisplayType display = allModeList[j].display;
                        List<DisplayMode> supportedModeList = allModeList[j].supportedModes;

                        DisplayInfo displayInfo = this.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
                        DisplayMode currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);

                        if (currentMode.HzRes < 1024 || currentMode.VtRes < 768)
                        {
                            Log.Alert("Current resolution is {0} which is less than 1024*768", currentMode.ToString());
                            for (int i = 0; i < supportedModeList.Count; i++)
                            {
                                if (supportedModeList[i].HzRes >= 1024 && supportedModeList[i].VtRes >= 768)
                                {
                                    if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, supportedModeList[i]))
                                        Log.Success("Mode applied Successfully");
                                    else
                                        Log.Fail("Fail to apply Mode");
                                    break;
                                }
                            }
                        }
                    }
                }
            }
            OverlayParams overlayObject = new OverlayParams()
            {
                PlaybackOptions = playOption,
                DisplayHierarchy = displayHierarchy,
                CurrentConfig = displayConfig,
                overlayApp = OverlayApp.MovingWorld,
                colorFormat = ColorFormat.RGB
            };
            AccessInterface.SetFeature<OverlayParams>(Features.Overlay, Action.Set, overlayObject);
            Thread.Sleep(5000);
        }
    }
}