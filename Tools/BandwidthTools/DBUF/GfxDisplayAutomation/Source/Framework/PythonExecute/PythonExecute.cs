namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Reflection;
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Security.Principal;

    public class PythonExecute
    {
        private IApplicationManager _appManager = null;
        private List<DisplayInfo> enumeratedDisplays;

        public List<DisplayInfo> EnumeratedDisplays
        {
            get { return this.enumeratedDisplays; }
            set { this.enumeratedDisplays = value; }
        }
        public IApplicationManager AppManager
        {
            get { return this._appManager; }
            set { this._appManager = value; }
        }
        private static bool _exceptionLogged = false;
        private const string QuickBuildVersion = "version.txt";

        //[STAThread]
        public void Init(string testName)
        {
            string[] args = new string[3] { testName, "SD", "EDP" };
            
            AppDomain.CurrentDomain.UnhandledException += new UnhandledExceptionEventHandler(GlobalExceptionHandler);
            IApplicationSettings appSettings = ApplicationSettings.Instance;
            CommandLineParser parser = new CommandLineParser();
            CommonExtensions.Init(appSettings, args);
            //UIExtensions.Load(appSettings);

            parser.Parse<string>(args, ArgumentType.TestName);
            parser.Parse<string>(args, ArgumentType.Config);
            parser.Parse<string>(args, ArgumentType.Display);

            bool rebootFileExists = CommonExtensions.HasRebootFile();
            //if (appSettings.AlternateLogFile)
            //    Log.Init(testName, appSettings.ReportLogLevel, true, rebootFileExists, true, true);
            //else
            //    Log.Init(testName, appSettings.ReportLogLevel, true, rebootFileExists, true, false);

            if (!new WindowsPrincipal(WindowsIdentity.GetCurrent()).IsInRole(WindowsBuiltInRole.Administrator))
                Log.Abort("Run the test in Administrator mode!");
            if (!rebootFileExists)
            {
                Log.Message(true, "Test Command Line:: Execute.exe {0}", string.Join(" ", args));               
                if (System.IO.File.Exists(QuickBuildVersion))
                {
                    string[] stVersionInfo = System.IO.File.ReadAllLines(QuickBuildVersion);

                    if (stVersionInfo.Length != 0)
                        Log.Verbose("Quick Build version:: {0}", stVersionInfo[0]);
                }
            }
            CommonExtensions.FlushRecordedLogMsgs();
            
            EnvPreparedness.RunTask(_appManager, Features.InitAssemblies);
            _appManager = new ApplicationManager(parser.ParamInfo, appSettings);
            DisplayExtensions.InitAccessInterface(_appManager.AccessInterface);
            EnvPreparedness.Init(_appManager, rebootFileExists);
            EnvPreparedness.RunTask(_appManager, Features.InitPlugSimulatedDisplays);
            EnvPreparedness.RunTask(_appManager, Features.InitEnumerateDisplays);
            enumeratedDisplays = (List<DisplayInfo>)parser.ParamInfo[ArgumentType.Enumeration];
        }


        private void GlobalExceptionHandler(object sender, UnhandledExceptionEventArgs e)
        {
            HandleException(e.ExceptionObject as Exception);
        }
        private void HandleException(object argException)
        {
            if (!_exceptionLogged)
            {
                _exceptionLogged = true;
                Exception exception = argException as Exception;
                if (null != exception.InnerException)
                    exception = exception.InnerException;
                if (typeof(TestException).Equals(argException.GetType()))
                {
                    TestException testException = exception as TestException;
                    exception = testException.OriginalException;
                    if (null != exception.InnerException)
                    {
                        Log.Verbose("InnerException.Message:: {0}{1}", Environment.NewLine, exception.InnerException.Message);
                        Log.Verbose("{0}", exception.InnerException.StackTrace);
                    }
                }
                Log.Verbose("{0}", exception.StackTrace);
                Log.Fail(exception.Message);
            }
            EnvPreparedness.RunTask(_appManager, Features.InitTestCleanUp);
            CommonExtensions.Exit(-1);
        }

        public void DeInit()
        {
            Console.WriteLine("Cleanup started");
            CommonExtensions.ClearRebootFile();
           // EnvPreparedness.RunTask(_appManager, Features.InitTestCleanUp);
            CommonExtensions.Exit(0);
        }




        public List<DisplayInfo> GetEnumeratedDisplays()
        {
            return EnumeratedDisplays;
        }

        /// <summary>
        /// Sets the configuration passed.
        /// </summary>
        /// <param name="displayConfigType">Display Config Type eg.  SD or DDC or ED or TDC or TED</param>
        /// <param name="display1">Primary Display eg. EDP or CRT or DP or DP_2 or DP_3 
        /// or HDMI or HDMI_2 or  HDMI_3 or MIPI or WIDI or DVI or WIGIG_DP1 or WIGIG_DP2 </param>
        /// <param name="display2">Secondary Display eg.None or EDP or CRT or DP or DP_2 or DP_3 
        /// or HDMI or HDMI_2 or  HDMI_3 or MIPI or WIDI or DVI or WIGIG_DP1 or WIGIG_DP2 </param>
        /// <param name="display3">Tertiary Display eg.None or EDP or CRT or DP or DP_2 or DP_3 
        /// or HDMI or HDMI_2 or  HDMI_3 or MIPI or WIDI or DVI or WIGIG_DP1 or WIGIG_DP2 </param>
        public bool SetConfig(string displayConfigType,
                        string display1,
                        string display2,
                        string display3)
        {
            DisplayConfig displayConfig = new DisplayConfig();
            DisplayType tmpEnum = DisplayType.None;
            DisplayConfigType tmpEnum1 = DisplayConfigType.None;

            ConvertStringToDisplayConfigType(displayConfigType, ref tmpEnum1);
            displayConfig.ConfigType = tmpEnum1;

            ConvertStringToDisplayType(display1, ref tmpEnum);
            displayConfig.PrimaryDisplay = tmpEnum;

            ConvertStringToDisplayType(display2, ref tmpEnum);
            displayConfig.SecondaryDisplay = tmpEnum;

            ConvertStringToDisplayType(display3, ref tmpEnum);
            displayConfig.TertiaryDisplay = tmpEnum;

            return _appManager.AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, displayConfig);
        }

        /// <summary>
        /// Gets the current configuration.
        /// </summary>
        /// <param name="displayConfigType">Display Config Type eg.  SD or DDC or ED or TDC or TED</param>
        /// <param name="display1">Primary Display eg. EDP or CRT or DP or DP_2 or DP_3 
        /// or HDMI or HDMI_2 or  HDMI_3 or MIPI or WIDI or DVI or WIGIG_DP1 or WIGIG_DP2 </param>
        /// <param name="display2">Secondary Display eg.None or EDP or CRT or DP or DP_2 or DP_3 
        /// or HDMI or HDMI_2 or  HDMI_3 or MIPI or WIDI or DVI or WIGIG_DP1 or WIGIG_DP2 </param>
        /// <param name="display3">Tertiary Display eg.None or EDP or CRT or DP or DP_2 or DP_3 
        /// or HDMI or HDMI_2 or  HDMI_3 or MIPI or WIDI or DVI or WIGIG_DP1 or WIGIG_DP2 </param>
        public void GetConfig(ref string displayConfigType,
                       ref string display1,
                       ref string display2,
                       ref string display3)
        {
            DisplayConfig currentConfig = _appManager.AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);

           displayConfigType = Enum.GetName(typeof(DisplayConfigType), currentConfig.ConfigType);
            display1 = Enum.GetName(typeof(DisplayType), currentConfig.PrimaryDisplay);
            display2 = Enum.GetName(typeof(DisplayType), currentConfig.SecondaryDisplay);
            display3 = Enum.GetName(typeof(DisplayType), currentConfig.TertiaryDisplay);
        }

        /// <summary>
        /// Sets the resolution passed.
        /// </summary>
        /// <param name="displayType">Type of Display eg.None or EDP or CRT or DP or DP_2 or DP_3 
        /// or HDMI or HDMI_2 or  HDMI_3 or MIPI or WIDI or DVI or WIGIG_DP1 or WIGIG_DP2 </param>
        /// <param name="x">Horizontal resolution</param>
        /// <param name="y">Vertical resolution</param>
        /// <param name="rr">refresh rate</param>
        /// <param name="angle">rotation angle eg. 0 or 90 or 180 or 270.</param>
        /// <param name="bpp">color depth. 16 or 32</param>
        /// <param name="scaling">Scaling options eg., Center_Image or Scale_Full_Screen 
        /// or Maintain_Aspect_Ratio or Customize_Aspect_Ratio or Maintain_Display_Scaling </param>
        public void SetMode(string displayType,
                            uint x, 
                            uint y, 
                            uint rr,
                            uint angle,
                            uint bpp,
                            string scaling)
        {
            DisplayType currentDisplay = DisplayType.None;
            ScalingOptions scalingOption = ScalingOptions.None;

            DisplayMode argSelectedMode = new DisplayMode();
            argSelectedMode.HzRes = x;
            argSelectedMode.VtRes = y;
            argSelectedMode.RR = rr;
            argSelectedMode.Angle = angle;
            argSelectedMode.Bpp = bpp;

            ConvertStringToScalingOptions(scaling, ref scalingOption);
            argSelectedMode.ScalingOptions = new List<uint>();
            argSelectedMode.ScalingOptions.Add((uint)scalingOption);

            ConvertStringToDisplayType(displayType, ref currentDisplay);
            argSelectedMode.display = currentDisplay;

            Log.Message(true, "Set supported mode {0} for {1}", argSelectedMode.GetCurrentModeStr(false), argSelectedMode.display);
            if (_appManager.AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argSelectedMode))
                Log.Success("Mode applied Successfully");
            else
                Log.Fail("Fail to apply Mode");
        }

        /// <summary>
        /// Gets the current resolution of the passed display.
        /// </summary>
        /// <param name="displayType">Type of Display eg.None or EDP or CRT or DP or DP_2 or DP_3 
        /// or HDMI or HDMI_2 or  HDMI_3 or MIPI or WIDI or DVI or WIGIG_DP1 or WIGIG_DP2 </param>
        /// <param name="x">Horizontal resolution</param>
        /// <param name="y">Vertical resolution</param>
        /// <param name="rr">refresh rate</param>
        /// <param name="angle">rotation angle eg. 0 or 90 or 180 or 270.</param>
        /// <param name="bpp">color depth. 16 or 32</param>
        /// <param name="scaling">Scaling options eg., Center_Image or Scale_Full_Screen 
        /// or Maintain_Aspect_Ratio or Customize_Aspect_Ratio or Maintain_Display_Scaling </param>
        public void GetMode(string displayType,
                           ref int x,
                           ref int y,
                           ref int rr,
                           ref int angle,
                           ref int bpp,
                           ref string scaling)
        {
            DisplayType currentDisplay = DisplayType.None;
            DisplayMode argSelectedMode = new DisplayMode();

            ConvertStringToDisplayType(displayType, ref currentDisplay);
            argSelectedMode.display = currentDisplay;

            DisplayInfo displayInfo = EnumeratedDisplays.Where(dI => dI.DisplayType == currentDisplay).FirstOrDefault();
            argSelectedMode = _appManager.AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);

            Log.Verbose("Mode {0} is for {1}", argSelectedMode.GetCurrentModeStr(false), currentDisplay);

            x = (int)argSelectedMode.HzRes;
            y = (int)argSelectedMode.VtRes;
            rr = (int)argSelectedMode.RR;
            angle = (int)argSelectedMode.Angle;
            bpp = (int)argSelectedMode.Bpp;
            scaling = Enum.GetName(typeof(ScalingOptions), (ScalingOptions)argSelectedMode.ScalingOptions[0]);
        }

        /// <summary>
        /// Gets all the supported resolutions of the display passed.
        /// </summary>
        /// <param name="argDisplayType">Type of Display eg.None or EDP or CRT or DP or DP_2 or DP_3 
        /// or HDMI or HDMI_2 or  HDMI_3 or MIPI or WIDI or DVI or WIGIG_DP1 or WIGIG_DP2 </param>
        /// <returns>Returns list of supported resolutions.</returns>
        public List<DisplayMode> GetAllSupportedModes(String argDisplayType)
        {
            List<DisplayModeList> listDisplayMode = new List<DisplayModeList>();
            DisplayType currentDisplay = DisplayType.None;

            ConvertStringToDisplayType(argDisplayType, ref currentDisplay);

            DisplayConfig currentConfig = _appManager.AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            List<DisplayModeList> allModeList = _appManager.AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, currentConfig.CustomDisplayList);

            return allModeList.Where(DML => DML.display == currentDisplay).FirstOrDefault().supportedModes;
        }

        /// <summary>
        /// This function call is used to plug a display.
        /// </summary>
        /// <param name="argDisplayType">Type of Display eg.None or EDP or CRT or DP or DP_2 or DP_3 
        /// or HDMI or HDMI_2 or  HDMI_3 or MIPI or WIDI or DVI or WIGIG_DP1 or WIGIG_DP2 </param>
        /// <param name="edid">EDID File Path</param>
        /// <param name="IsLowPower">Pass true if plug to be done in LowPowerState else false</param>
        /// <returns>returns true if hotplug is success.</returns>
        protected bool HotPlug(String argDisplayType, string edid, bool IsLowPower)
        {
            DisplayType currentDisplay = DisplayType.None;
            ConvertStringToDisplayType(argDisplayType, ref currentDisplay);

            HotPlugUnplug _HotPlugUnplug = new HotPlugUnplug();
            _HotPlugUnplug.display = currentDisplay;
            _HotPlugUnplug.FunctionName = FunctionName.PLUG;
            _HotPlugUnplug.InLowPowerState = IsLowPower;
            if (!string.IsNullOrEmpty(edid))
            {
                _HotPlugUnplug.EdidFilePath = _HotPlugUnplug.EdidFilePath + edid;
            }
            if (!_appManager.ApplicationSettings.UseDivaFramework && !_appManager.ApplicationSettings.UseULTFramework)
            {// If Plugging display using DVMU
                return _appManager.AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, _HotPlugUnplug);
            }
            else
            {//Plugging display through DFT framework
                return _appManager.AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.SimulatedHotPlugDisplay, Action.SetMethod, _HotPlugUnplug);
            }
        }

        /// <summary>
        /// This function call is used to plug a display.
        /// </summary>
        /// <param name="useWindowsID">Pass true if plug call to be based on passed windows monitor id.</param>
        /// <param name="windowsMonitorID">windows monitor id of the display to be plugged.</param>
        /// <param name="argEdidName">EDID File Path</param>
        /// <param name="IsLowerPower">Pass true if plug to be done in LowPowerState else false</param>
        /// <returns>returns true if hotplug is success.</returns>
        //protected bool HotPlug(bool useWindowsID, uint windowsMonitorID, string argEdidName, bool IsLowerPower)
        //{
        //    HotPlugUnplug obj = new HotPlugUnplug(FunctionName.PLUG, useWindowsID, windowsMonitorID, argEdidName, IsLowerPower);
        //    bool status = _appManager.AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.SimulatedHotPlugDisplay, Action.SetMethod, obj);

        //    return status;
        //}

        /// <summary>
        /// This function call is used to unplug a display in normal mode or low power state.
        /// </summary>
        /// <param name="argDisplayType">Type of Display eg.None or EDP or CRT or DP or DP_2 or DP_3 
        /// or HDMI or HDMI_2 or  HDMI_3 or MIPI or WIDI or DVI or WIGIG_DP1 or WIGIG_DP2 </param>
        /// <param name="IsLowPower">Pass true if unplug need to be performed in LowPoweState else false.</param>
        /// <returns>returns true if hotunplug is success.</returns>
        protected bool HotUnPlug(String argDisplayType, bool IsLowPower)
        {
            DisplayType currentDisplay = DisplayType.None;
            ConvertStringToDisplayType(argDisplayType, ref currentDisplay);

            Log.Message("Performing HotUnPlug of display {0} ", currentDisplay);
            HotPlugUnplug _HotPlugUnplug = new HotPlugUnplug();
            _HotPlugUnplug.FunctionName = FunctionName.UNPLUG;
            _HotPlugUnplug.display = currentDisplay;
            _HotPlugUnplug.InLowPowerState = IsLowPower;
            if (!_appManager.ApplicationSettings.UseDivaFramework && !_appManager.ApplicationSettings.UseULTFramework)
            {//Unplugging display using DVMU
                return _appManager.AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, _HotPlugUnplug);
            }
            //Unplugging Dispaly using DFT framework
            return _appManager.AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.SimulatedHotPlugDisplay, Action.SetMethod, _HotPlugUnplug);
        }

        /// <summary>
        /// This function call is used to perform power states.
        /// </summary>
        /// <param name="strPowerState">Possible PowerStates are S3 or S4 or S5 or CS</param>
        /// <param name="delay">Time delay in Seconds to resume from powerstate.</param>
        /// <returns>returns true if we are able to perform power state.</returns>
        public bool GoToPowerState(String strPowerState, 
                                uint delay)
        {
            PowerStates powerState = PowerStates.S3;
            PowerParams powerParams = new PowerParams();
            powerParams.Delay = 30;

            ConvertStringToPowerState(strPowerState, ref powerState);
            powerParams.PowerStates = powerState;

            return _appManager.AccessInterface.SetFeature<bool, PowerParams>(Features.PowerEvent, Action.SetMethod, powerParams);
        }

        /// <summary>
        /// This function call returns the current crc pipe/port.(Note: DIVA driver should have installed for this call.)
        /// </summary>
        /// <param name="argDisplayType">Type of Display eg.None or EDP or CRT or DP or DP_2 or DP_3 
        /// or HDMI or HDMI_2 or  HDMI_3 or MIPI or WIDI or DVI or WIGIG_DP1 or WIGIG_DP2 </param>
        /// <param name="IspipeCRC">pass true if pipe crc is required, pass false for port crc.</param>
        /// <param name="currentCRC">current crc value</param>
        /// <returns>returns true if crc value is obtained.</returns>
        public bool GetCRC(String argDisplayType, 
                            bool IspipeCRC, 
                            ref int currentCRC)
        {
            bool status = false;
            DisplayType currentDisplay = DisplayType.None;
            ConvertStringToDisplayType(argDisplayType, ref currentDisplay);
            
            CRCArgs obj = new CRCArgs();
            obj.displayType = currentDisplay;
            obj.port = EnumeratedDisplays.Where(dI => dI.DisplayType == currentDisplay).FirstOrDefault().Port;
            obj.ComputePipeCRC = true;
            obj = _appManager.AccessInterface.GetFeature<CRCArgs, CRCArgs>(Features.CRC, Action.GetMethod, Source.AccessAPI, obj);

            if (obj.CRCValue != 0)
            {
                status = true;
                currentCRC = (int)obj.CRCValue;
            }

            return status;
        }

        /// <summary>
        /// This function call returns the offset, bitmap and expected value for the passed event.
        /// </summary>
        /// <param name="argEventName"> This represents the feature which we are interested</param>
        /// <param name="argDisplayType">Type of Display eg.None or EDP or CRT or DP or DP_2 or DP_3 
        /// or HDMI or HDMI_2 or  HDMI_3 or MIPI or WIDI or DVI or WIGIG_DP1 or WIGIG_DP2 </param>
        /// <param name="offset">offset mapped to the eventName</param>
        /// <param name="bitmap">bitmap mapped to the eventName</param>
        /// <param name="expectedValue">expected value mapped to the eventName</param>
        /// <returns>returns true if we are able to read the register.</returns>
        public bool GetEventRegisterInfo(String argEventName,
                                        String argDisplayType,
                                        ref int offset, 
                                        ref int bitmap, 
                                        ref int expectedValue)
        {
            bool status = false;

            DisplayType currentDisplay = DisplayType.None;
            ConvertStringToDisplayType(argDisplayType, ref currentDisplay);

            EventInfo returnEventInfo = GetEventInfo(currentDisplay, argEventName);

            if (returnEventInfo.listRegisters.Count > 0)
            {
                status = true;
                offset = Convert.ToInt32(returnEventInfo.listRegisters[0].Offset, 16);
                bitmap = Convert.ToInt32(returnEventInfo.listRegisters[0].Bitmap, 16);
                expectedValue = Convert.ToInt32(returnEventInfo.listRegisters[0].Value, 16);
            }
            return status;
        }


        /// <summary>
        /// Verifies all the registers for the specified event.
        /// </summary>
        /// <param name="argEventName">This represents the feature which we are interested</param>
        /// <param name="argDisplayType">Type of Display eg.None or EDP or CRT or DP or DP_2 or DP_3 
        /// or HDMI or HDMI_2 or  HDMI_3 or MIPI or WIDI or DVI or WIGIG_DP1 or WIGIG_DP2 </param>
        /// <returns>returns true if the current value matched with the expected value associated for the event.</returns>
        public bool VerifyRegisters(String argEventName, String argDisplayType)
        {
            bool status = true;

            DisplayType currentDisplay = DisplayType.None;
            ConvertStringToDisplayType(argDisplayType, ref currentDisplay);

            EventInfo returnEventInfo = GetEventInfo(currentDisplay, argEventName);

            foreach (RegisterInf reginfo in returnEventInfo.listRegisters)
            {
                Log.Message("Offset being checked = {0} Bitmap being checked {1}  Value to be got = {2}", reginfo.Offset, reginfo.Bitmap, reginfo.Value);
                
                uint argOffset = Convert.ToUInt32(reginfo.Offset, 16);
                UInt32 argValue =0;

                if (GetRegisterValue((int)argOffset, ref argValue))
                    if (!CompareRegisters((uint)argValue, reginfo))
                    {
                        Log.Fail("Register with offset {0} doesnot match required values", reginfo.Offset);
                        status = false;
                    }
            }

            return status;
        }
        
        /// <summary>
        /// Returns teh register value from the offset given.
        /// </summary>
        /// <param name="argOffset">Offset of the register we are interested.</param>
        /// <param name="argValue">Returns the value for the passed register offset.</param>
        /// <returns>returns true if the call succeeds.</returns>
        public bool GetRegisterValue(int argOffset, ref UInt32 argValue)
        {
            bool status = true;
            DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
            driverData.input = (uint)argOffset;
            DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
            if (!_appManager.AccessInterface.SetFeature<bool, DriverEscapeParams>(Features.DriverEscape, Action.SetMethod, driverParams))
            {
                status = false;
                Log.Fail("Failed to read Register with offset as {0}", driverData.input);
            }
            else
            {
                argValue = driverData.output;
            }

            return status;
        }

        /// <summary>
        /// Computes the value after bitmapping the argRegisterValue with the bitmap associated with the passed event.
        /// </summary>
        /// <param name="argEventName">This represents the feature which we are interested</param>
        /// <param name="argDisplayType">Type of Display eg.None or EDP or CRT or DP or DP_2 or DP_3 
        /// or HDMI or HDMI_2 or  HDMI_3 or MIPI or WIDI or DVI or WIGIG_DP1 or WIGIG_DP2 </param>
        /// <param name="argRegisterValue">This argument represents the value nts the bitmapped value associated with the event.</param>
        /// <param name="bitmappedValue">Returns the value after bitmapping the argRegisterValue with the bitmap associated with the passed event.</param>
        /// <returns>returns true if call is succeeded.</returns>
        public bool GetBitmappedRegisterValue(String argEventName,
                                       String argDisplayType,
                                       long argRegisterValue,
                                       ref int bitmappedValue)
        {
            bool status = false;
            int count = 0;

            DisplayType currentDisplay = DisplayType.None;
            ConvertStringToDisplayType(argDisplayType, ref currentDisplay);

            EventInfo returnEventInfo = GetEventInfo(currentDisplay, argEventName);

            int regBitmap = Convert.ToInt32(returnEventInfo.listRegisters[0].Bitmap, 16);
            string bitmapBinValue = Convert.ToString(regBitmap, 2);
            while (bitmapBinValue.EndsWith("0") != false)
            {
                bitmapBinValue = bitmapBinValue.Substring(0, bitmapBinValue.Length - 1);
                count++;
            }

            argRegisterValue &= regBitmap;
            bitmappedValue = (int)(argRegisterValue >> count);

            return status;
        }

        /// <summary>
        /// Computes the value after bitmapping the RegisterValue from register with the bitmap associated with the passed event.
        /// </summary>
        /// <param name="argEventName">This represents the feature which we are interested</param>
        /// <param name="argDisplayType">Type of Display eg.None or EDP or CRT or DP or DP_2 or DP_3 
        /// or HDMI or HDMI_2 or  HDMI_3 or MIPI or WIDI or DVI or WIGIG_DP1 or WIGIG_DP2 </param>
        /// <param name="bitmappedValue">Returns the value after bitmapping the RegisterValue from register with the bitmap associated with the passed event.</param>
        /// <returns>returns true if call is succeeded.</returns>
        public bool GetBitmappedRegisterValue(String argEventName,
                                       String argDisplayType,
                                       ref int bitmappedValue)
        {
            bool status = true;
            int count = 0, offset = 0;
            UInt32 registerValue = 0;

            DisplayType currentDisplay = DisplayType.None;
            ConvertStringToDisplayType(argDisplayType, ref currentDisplay);

            EventInfo returnEventInfo = GetEventInfo(currentDisplay, argEventName);
            
            //Reading register.
            offset = Convert.ToInt32(returnEventInfo.listRegisters[0].Offset, 16);
            status = GetRegisterValue(offset, ref registerValue);
            
            if (status)
            {
                UInt32 regBitmap = Convert.ToUInt32(returnEventInfo.listRegisters[0].Bitmap, 16);
                string bitmapBinValue = Convert.ToString(regBitmap, 2);
                Log.Message("Register Offset: {0} || Offset: {1} || Value: {2:X}", returnEventInfo.listRegisters[0].Offset, returnEventInfo.listRegisters[0].Bitmap, registerValue);
                while (bitmapBinValue.EndsWith("0") != false)
                {
                    bitmapBinValue = bitmapBinValue.Substring(0, bitmapBinValue.Length - 1);
                    count++;
                }

                registerValue &= regBitmap;

                bitmappedValue =  (int) (registerValue >> count);
            }
            return status;
        }

        private bool CompareRegisters(uint argDriverData, RegisterInf argRegInfo)
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

        private EventInfo GetEventInfo(DisplayType displayType, String argEventName)
        {
            PipePlaneParams pipePlane = new PipePlaneParams(displayType);
            pipePlane = _appManager.AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane);

            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = pipePlane.Pipe;
            eventInfo.plane = pipePlane.Plane;
            eventInfo.port = EnumeratedDisplays.Where(dI => dI.DisplayType == displayType).FirstOrDefault().Port;
            eventInfo.eventName = argEventName;

            Log.Verbose("Event being checked = {0}", eventInfo.eventName);
            EventInfo returnEventInfo = _appManager.AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);

            return returnEventInfo;
        }

        private bool ConvertStringToPowerState(string strDisplayType, ref PowerStates powerState)
        {
            bool status = true;
            PowerStates tmpEnum;

            if (!Enum.TryParse(strDisplayType, true, out tmpEnum))
            {
                powerState = PowerStates.S3;
                status = false;
            }
            else
            {
                powerState = tmpEnum;
            }

            return status;
        }

        private bool ConvertStringToDisplayType(string strDisplayType, ref DisplayType currentDisplay)
        {
            bool status = true;
            DisplayType tmpEnum;

            if (!Enum.TryParse(strDisplayType, true, out tmpEnum))
            {
                currentDisplay = DisplayType.None;
                status = false;
            }
            else
            {
                currentDisplay = tmpEnum;
            }

            return status;
        }

        private bool ConvertStringToDisplayConfigType(string strConfigType, ref DisplayConfigType currentConfigType)
        {
            bool status = true;
            DisplayConfigType tmpEnum;

            if (!Enum.TryParse(strConfigType, true, out tmpEnum))
            {
                currentConfigType = DisplayConfigType.None;
                status = false;
            }
            else
            {
                currentConfigType = tmpEnum;
            }

            return status;
        }

        private bool ConvertStringToScalingOptions(string strScalingType, ref ScalingOptions scalingOption)
        {
            bool status = true;
            ScalingOptions tmpEnum;

            if (!Enum.TryParse(strScalingType, true, out tmpEnum))
            {
                scalingOption = ScalingOptions.None;
                status = false;
            }
            else
            {
                scalingOption = tmpEnum;
            }

            return status;
        }
    }
}
