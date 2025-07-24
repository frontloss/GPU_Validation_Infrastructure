namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Management;
    using System.Linq;
    using System.Xml.Linq;
    using System.Collections.Generic;
    using System.Threading;
    using System.Text;
    using System.Diagnostics;
    using System.Windows.Forms;

    public delegate void PSRCaptureDelegate();

    class MP_SwitchableGraphics_Base : TestBase
    {
        protected List<DisplayModeList> commonDisplayModeList = new List<DisplayModeList>();
        private DisplayConfig testConfig = new DisplayConfig();

        protected List<DisplayType> displayPassedInCommandline = null;
        protected int iTestRunDuration = 30;
        protected bool bIsDMCEnabled = true;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {
            Log.Message(true, "Install Switchable Graphics Driver if not installed");
            DriverInfo driverInfo = AccessInterface.GetFeature<DriverInfo, DriverAdapterType>(Features.DriverFunction, Action.GetMethod, Source.AccessAPI, DriverAdapterType.ATI);
            if (driverInfo == null)
            {
                if (!Directory.Exists(base.ApplicationManager.ApplicationSettings.SwitchableGraphicsDriverPath))
                {
                    Log.Abort("Coun't find {0} SB to run the test", base.ApplicationManager.ApplicationSettings.SwitchableGraphicsDriverPath);
                }
                Log.Message("Installing ATI Adapter");
                InstallUnInstallParams installParams = new InstallUnInstallParams();
                installParams.ProdPath = string.Format(@"{0}\{1}", base.ApplicationManager.ApplicationSettings.SwitchableGraphicsDriverPath, "WinUnified");
                installParams.AdapterType = DriverAdapterType.ATI;
                bool retInstall = AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.InstallDriver, Action.SetMethod, installParams);
            }
        }
        protected void Hotplug(FunctionName FuncArg, DisplayType DisTypeArg, DVMU_PORT PortArg)
        {
            HotPlugUnplug _HotPlugUnplug = null;
            _HotPlugUnplug = new HotPlugUnplug(FuncArg, DisTypeArg, PortArg);
            bool status = AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, _HotPlugUnplug);
        }
        protected bool WiDiReConnect(bool isExpected = false)
        {
            if (!isExpected)
            {
                if (base.MachineInfo.OS.Type == OSType.WINBLUE)
                    Log.Alert("WiDi Display not enumerated try to reconnect to run the test");
                else
                    Log.Fail("WiDi Display not enumerated try to reconnect to run the test");
            }

            Log.Verbose("Verify EDP is connected ");
            DisplayConfig displayConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = DisplayType.EDP };
            Log.Message("Set the initial configuration as SD {0}", displayConfig.PrimaryDisplay);
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, displayConfig))
                Log.Message("Config (SD {0}) applied successfully", displayConfig.PrimaryDisplay);
            else
                Log.Abort("Config (SD {0}) not applied!", displayConfig.PrimaryDisplay);
            if (AccessInterface.SetFeature<bool>(Features.WiDiDisplayConnection, Action.SetNoArgs))
            {
                Log.Success("WiDi Connection Successful");
                List<DisplayInfo> currentDisplayEnum = base.CurrentConfig.EnumeratedDisplays;
                List<DisplayInfo> enumeratedDisplay = AccessInterface.SetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);
                List<uint> winMonIDList = AccessInterface.GetFeature<List<uint>>(Features.WindowsMonitorID, Action.GetAll);
                List<uint> currentWinMonIDList = base.CurrentConfig.EnumeratedDisplays.Where(dI => !dI.WindowsMonitorID.Equals(0)).Select(dI => dI.WindowsMonitorID).ToList();
                List<uint> diffMonitorIdList = winMonIDList.Except(currentWinMonIDList).ToList();
                if (enumeratedDisplay.Count > currentDisplayEnum.Count)
                {
                    base.CurrentConfig.EnumeratedDisplays.Clear();
                    base.CurrentConfig.EnumeratedDisplays.AddRange(enumeratedDisplay);
                }
                AccessInterface.GetFeature<bool, List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetMethod, Source.AccessAPI, enumeratedDisplay);
                return true;
            }
            return false;
        }

        protected int CurrentMonitorBrightness()
        {
            ManagementObjectSearcher query = new ManagementObjectSearcher("root\\WMI", "SELECT * FROM WmiMonitorBrightness");
            ManagementObject mgmtObject = query.Get().Cast<ManagementObject>().FirstOrDefault();
            if (null != mgmtObject)
            {
                IEnumerable<PropertyData> pDColn = mgmtObject.Properties.Cast<PropertyData>();
                int currentBr = pDColn.Where(pD => pD.Name.Equals("CurrentBrightness")).Select(pD => Convert.ToInt32(pD.Value)).FirstOrDefault();
                return currentBr;
            }
            return 0;
        }
        protected bool SetNValidateConfig(DisplayConfig argConfig)
        {
            if (argConfig.ConfigType == DisplayConfigType.TDC || argConfig.ConfigType == DisplayConfigType.TED)
                Thread.Sleep(5000);
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argConfig))
            {
                DisplayConfig testConfig = argConfig;
                Log.Success("Switch successful to {0} ", argConfig.GetCurrentConfigStr());
                Log.Message("Set the maximum display mode on all the active displays");
                return true;
            }
            else
                Log.Abort("Config not applied!");
            return false;
        }
        protected string GetConfigString(DisplayConfig argConfig)
        {
            StringBuilder sb = new StringBuilder(argConfig.ConfigType.ToString()).Append(" ");
            sb.Append(argConfig.PrimaryDisplay.ToString()).Append(" ");
            if (argConfig.SecondaryDisplay != DisplayType.None)
                sb.Append(argConfig.SecondaryDisplay.ToString()).Append(" ");
            if (argConfig.TertiaryDisplay != DisplayType.None)
                sb.Append(argConfig.TertiaryDisplay.ToString()).Append(" ");
            return sb.ToString();
        }
        protected void CheckWiDiStatus()
        {
            if (!IsWiDiConnected())
            {
                Log.Fail(false, "WiDi displays are not enumerated, WiDi connection drops");
                Log.Abort("!!!!!!!!!! Exiting from test execution !!!!!!!!!!");
            }
        }
        protected bool IsWiDiConnected()
        {
            List<DisplayInfo> enumeratedDisplays = AccessInterface.SetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);
            base.CurrentConfig.EnumeratedDisplays = enumeratedDisplays;
            if (enumeratedDisplays.Any(DI => DI.DisplayType == DisplayType.WIDI))
                return true;
            else
                return false;
        }
        internal bool WiDIDisconnect()
        {
            if (base.MachineInfo.OS.Type == OSType.WINBLUE)
            {
                Log.Message("Disconnect WiDi by setting single display EDP");
                DisplayConfig displayConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = DisplayType.EDP };
                Log.Message("Set the initial configuration as SD {0}", displayConfig.PrimaryDisplay);
                if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, displayConfig))
                    Log.Message("Config (SD {0}) applied successfully", displayConfig.PrimaryDisplay);
                else
                    Log.Abort("Config (SD {0}) not applied!", displayConfig.PrimaryDisplay);
            }
            else
                KillProcess("WiDiApp");
            List<uint> winMonIDs = AccessInterface.GetFeature<List<uint>>(Features.WindowsMonitorID, Action.GetAll);
            if (winMonIDs.Count < base.CurrentConfig.EnumeratedDisplays.Count)
            {
                List<DisplayInfo> enumeratedDisplay = AccessInterface.SetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);
                base.CurrentConfig.EnumeratedDisplays.Clear();
                base.CurrentConfig.EnumeratedDisplays.AddRange(enumeratedDisplay);
            }
            return true;
        }
        private void KillProcess(string processName)
        {
            Process[] processList = Process.GetProcessesByName(processName);
            if (processList.Length >= 1)
            {
                Log.Verbose("Found {0} WiDi app running in test system", processList.Length);
            }
            foreach (Process eachProcess in processList)
            {
                eachProcess.Kill();
                Log.Verbose("Exiting from {0} process successfully", processName);
                Thread.Sleep(8000);
            }
        }
        protected List<DisplayModeList> GetAllModesForActiceDisplay(DisplayConfig argDisplayConfig)
        {
            if (commonDisplayModeList.Count != 0)
                return commonDisplayModeList;
            else
            {
                WiDiConnectionPersistence();
                Log.Verbose("Getting all suppored modes for all active display");
                List<DisplayModeList> displayModeList_OSPage = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, argDisplayConfig.DisplayList);
                List<DisplayMode> commonModes = null;
                if (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
                {
                    commonModes = displayModeList_OSPage.Where(dML => dML.display == argDisplayConfig.PrimaryDisplay).Select(dML => dML.supportedModes).FirstOrDefault();
                    displayModeList_OSPage.Skip(1).ToList().ForEach(dML => commonModes = commonModes.Intersect(dML.supportedModes, new DisplayMode()).ToList());
                    if (commonModes.Count() > 0)
                        commonDisplayModeList.Add(new DisplayModeList() { display = argDisplayConfig.PrimaryDisplay, supportedModes = commonModes });
                }
                else
                    commonDisplayModeList = displayModeList_OSPage;
                return commonDisplayModeList;
            }
        }
        private void WiDiConnectionPersistence()
        {
            if (!IsWiDiConnected())
            {
                if (!WiDiReConnect())
                    CheckWiDiStatus();
                if (!AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, testConfig))
                    Log.Abort("Failed to Switch {0} ", testConfig.GetCurrentConfigStr());
            }
        }
        protected void ApplyModeAndVerify(DisplayMode argDispMode, bool connectWiDi = true)
        {
            if (connectWiDi)
            {
                if (!IsWiDiConnected())
                    WiDiReConnect();
            }
            Log.Message("Setting Mode : {0} for {1}", GetModeStr(argDispMode), argDispMode.display);
            if (!AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argDispMode))
                Log.Fail("Fail to apply Mode");
            else
                Log.Success("Mode applied successfully");
        }
        protected string GetModeStr(DisplayMode argMode)
        {
            return string.Concat(argMode.HzRes, "x", argMode.VtRes, "x", argMode.RR, argMode.InterlacedFlag.Equals(0) ? "p Hz" : "i Hz", "x", argMode.Bpp);
        }
        protected void VerifyProtectionHDCP(DisplayType argDisplayType, string argOnOff, int argLevel, Dictionary<DisplayType, string> argMyDictionary)
        {
            string hdcpStatus = String.Concat("Calling set HDCP with level = ", argLevel, " (OPM_HDCP_", argOnOff, ")");
            if (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
                VerifyProtectionForAllDisplays(hdcpStatus, argMyDictionary);
            else
            {
                Log.Message(true, "Verify HDCP Protection in log for {0} is {1}", argDisplayType, argMyDictionary[argDisplayType]);
                int flagSuccess = 0;
                string[] directories = Directory.GetDirectories(Directory.GetCurrentDirectory(), "OPM*");
                string logFileName = Directory.GetFiles(directories.First(), "*.txt").FirstOrDefault();
                string line;
                System.IO.StreamReader file = new System.IO.StreamReader(logFileName);
                while ((line = file.ReadLine()) != null)
                {
                    if (line.Contains(hdcpStatus))
                    {
                        string nextLine;
                        while ((nextLine = file.ReadLine()) != null)
                        {
                            if (nextLine.Contains(argMyDictionary[argDisplayType]))
                            {
                                flagSuccess = 1;
                                Log.Success("Log file for {0} contains {1}", argDisplayType, argMyDictionary[argDisplayType]);
                            }
                        }
                    }
                }
                if (flagSuccess == 0)
                    Log.Fail("Log file for {0} does not contains {1}", argDisplayType, argMyDictionary[argDisplayType]);
                file.Close();
            }
        }
        private void VerifyProtectionForAllDisplays(string argHdcpStatus, Dictionary<DisplayType, string> argMyDictionary)
        {
            List<int> supportedUnsupported = GetTotalSupportedUnsupportedHdcpDisplays(base.CurrentConfig.CustomDisplayList);
            List<int> supportedUnsupportedLogFile = new List<int>();
            Log.Message(true, "Verify HDCP Protection in log for all displays in configuration");
            string[] directories = Directory.GetDirectories(Directory.GetCurrentDirectory(), "OPM*");
            string logFileName = Directory.GetFiles(directories.First(), "*.txt").FirstOrDefault();
            string line;
            int supported = 0;
            int unsupported = 0;
            System.IO.StreamReader file = new System.IO.StreamReader(logFileName);
            while ((line = file.ReadLine()) != null)
            {
                if (line.Contains(argHdcpStatus))
                {
                    string nextLine;
                    while ((nextLine = file.ReadLine()) != null)
                    {
                        DisplayType[] key = argMyDictionary.Where(x => nextLine.Contains(x.Value.ToString())).Select(pair => pair.Key).ToArray();
                        foreach (DisplayType dT in key)
                        {
                            if (dT == DisplayType.EDP || dT == DisplayType.CRT)
                            {
                                if (base.CurrentConfig.CustomDisplayList.Contains(dT))
                                    supported += 1;
                            }
                            else
                            {
                                if (base.CurrentConfig.CustomDisplayList.Contains(dT))
                                    unsupported += 1;
                            }
                        }
                    }
                }
            }
            supportedUnsupportedLogFile.Add(supported);
            supportedUnsupportedLogFile.Add(unsupported);
            List<int> result = supportedUnsupported.Except(supportedUnsupportedLogFile).ToList();
            if (result.Count == 0)
                Log.Success("HDCP protection levels verified for all displays in configuration");
            else
                Log.Fail("HDCP protection levels not matching for some displays in configuration");
            file.Close();
        }
        private List<int> GetTotalSupportedUnsupportedHdcpDisplays(List<DisplayType> argCustomDisplayList)
        {
            List<int> _supportedUnsupported = new List<int>();
            int supported = 0;
            int unsupported = 0;
            for (int i = 0; i < argCustomDisplayList.Count; i++)
            {
                if (argCustomDisplayList[i] == DisplayType.EDP || argCustomDisplayList[i] == DisplayType.CRT)
                    unsupported += 1;
                else
                    supported += 1;
            }
            _supportedUnsupported.Add(supported);
            _supportedUnsupported.Add(unsupported);
            return _supportedUnsupported;
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

        protected void ApplySDConfigNativeModeOnEdp()
        {
            Log.Message("Applying SD config, Native mode on eDP");

            base.CurrentConfig.ConfigType = DisplayConfigType.SD;
            base.CurrentConfig.PrimaryDisplay = DisplayType.EDP;
            base.CurrentConfig.SecondaryDisplay = DisplayType.None;
            base.CurrentConfig.TertiaryDisplay = DisplayType.None;
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Successfully applied {0} eDP", base.CurrentConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to apply {0} eDP", base.CurrentConfig.GetCurrentConfigStr());

            ApplyNativeModeOnEdp();
        }

        protected void ApplyNativeModeOnEdp()
        {
            Log.Message("Applying native mode on eDP");

            // Finding Native Mode (get all modes and last mode is th native)
            List<DisplayMode> displayModes = GetModesForTest(DisplayType.EDP);

            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, displayModes.Last()))
                Log.Success("Native mode is applied on eDP");
            else
                Log.Fail("Failed to apply native mode on eDP");
        }
        protected List<DisplayMode> GetModesForTest(DisplayType pDisplayType)
        {
            List<DisplayType> displays = new List<DisplayType>();
            displays.Add(pDisplayType);
            List<DisplayModeList> displayModeList_OSPage = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, displays);
            List<DisplayMode> dispModes = displayModeList_OSPage.Where(dML => dML.display == pDisplayType).Select(dML => dML.supportedModes).FirstOrDefault();
            return dispModes;
        }

        protected bool PrintPSRStatusResult(PsrStatus psrStatus)
        {
            bool bRetVal = true;
            if (psrStatus.psrWorkingState == PsrWorkingState.PsrEnabledAndWorkingProperly)
            {
                Log.Success("PSR Passed (PSR Active Count = " + (psrStatus.psrCapturedData.currentEntryExitCount.ToString()) + " )");
            }
            else if (psrStatus.psrWorkingState == PsrWorkingState.PsrEnabledButLessEntryExitCount)
            {
                Log.Success("PSR Passed with less count (PSR Active Count = " + (psrStatus.psrCapturedData.currentEntryExitCount.ToString()) + " )");
            }
            else
            {
                Log.Fail("PSR Failed (PSR Active Count = " + (psrStatus.psrCapturedData.currentEntryExitCount.ToString()) + " )");
                bRetVal = false;
            }

            Platform platform = base.MachineInfo.PlatformDetails.Platform;
            if (platform != Platform.VLV && platform != Platform.CHV)
            {
                if (bIsDMCEnabled && !(platform == Platform.HSW))
                {
                    Log.Message("PSR residency check is skipped as DMC (c9) is enabled (Counter doesn\'t work)");
                }
                else
                {
                    if (psrStatus.psrCapturedData.currentResidencyTime >= psrStatus.psrCapturedData.requiredResidencyTime) // residency value comes les due to HW optimization
                    {
                        Log.Success("PSR residency check passed (PSR Perf Count = {0}ms)", psrStatus.psrCapturedData.currentResidencyTime);
                    }
                    else
                    {
                        Log.Fail("PSR residency check failed (PSR Perf Count = {0}ms)", psrStatus.psrCapturedData.currentResidencyTime);
                        bRetVal = false;
                    }
                }
            }
            return bRetVal;
        }

        protected bool RunTDR()
        {
            Log.Message("Running TDR");
            if (!AccessInterface.SetFeature<bool>(Features.ForceTDR, Action.SetNoArgs))
            {
                if (!CommonExtensions.HasRetryThruRebootFile())
                {
                    Log.Sporadic(true, "TDR unsuccessful! A reboot may be required.");
                    this.InvokePowerEvent(new PowerParams() { Delay = 5, PowerStates = PowerStates.S5 }, PowerStates.S5);
                }
                else
                    CommonExtensions.ClearRetryThruRebootFile();
            }
            else
            {
                CommonExtensions.ClearRetryThruRebootFile();
                return true;
            }
            return false;
        }
        public void verifyEDPConnected()
        {
            if (false == base.CurrentConfig.DisplayList.Contains(DisplayType.EDP))
                Log.Abort("verifyEDPConnected() : PSR supports only in SD EDP.As EDP display is not connected so aborting");
        }

        public void ApplyConfigOS(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());
        }


    }
}

