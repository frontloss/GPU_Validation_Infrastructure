namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.IO;
    using System.Linq;
    using System.Text;
    using System.Threading;
    using System.Windows.Automation;

    [Test(Type = TestType.WiDi)]
    public class MP_WIDIBase : TestBase
    {
        private Dictionary<int, Action<List<DisplayConfigWrapper>>> _switchPatternList = null;
        internal Dictionary<int, Action<List<DisplayConfigWrapper>>> SwitchPatternList
        {
            get
            {
                if (null == this._switchPatternList)
                {
                    this._switchPatternList = new Dictionary<int, Action<List<DisplayConfigWrapper>>>();
                    this._switchPatternList.Add(2, this.GetSwitchPatternForDualDisplayMode);
                    this._switchPatternList.Add(3, this.GetSwitchPatternForTriDisplayMode);
                }
                return this._switchPatternList;
            }
        }
        internal List<DisplayConfigWrapper> switchPatternList = null;
        protected List<DisplayModeList> commonDisplayModeList = new List<DisplayModeList>();
        public DisplayConfig testConfig = new DisplayConfig();
        public List<DisplayType> externalDisplayList = new List<DisplayType>();
        public List<DisplayType> pDisplayList = new List<DisplayType>();
        private PowerParams _powerParams = null;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            foreach (DisplayType T in base.CurrentConfig.CustomDisplayList)
            {
                if (T == DisplayType.WIDI)
                    continue;
                else if (!base.CurrentConfig.EnumeratedDisplays.Any(DT => DT.DisplayType == T))
                    Log.Abort("Display type {0} not connected, please connect display to run the test", T.ToString());
            }

            if (!base.CurrentConfig.EnumeratedDisplays.Any(DI => DI.DisplayType == DisplayType.WIDI))
            {
                if (!WiDiReConnect(true))
                    Log.Abort("Unable to connect");
            }
        }

        internal bool WiDiReConnect(bool isExpected = false)
        {
            if (!base.CurrentConfig.CustomDisplayList.Contains(DisplayType.WIDI))
                return true;
            if (!isExpected)
            {
                if (base.MachineInfo.OS.Type == OSType.WINBLUE)
                    Log.Alert("WiDi Display not enumerated try to reconnect to run the test");
                else
                    Log.Fail("WiDi Display not enumerated try to reconnect to run the test");
            }

            Log.Verbose("Verify EDP/MIPI is connected ");
            DisplayConfig displayConfig = null;
            displayConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.GetInternalDisplay() };
            Log.Message("Set the initial configuration as SD {0}", displayConfig.PrimaryDisplay);
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, displayConfig))
                Log.Message("Config (SD {0}) applied successfully", displayConfig.PrimaryDisplay);
            else
                Log.Abort("Config (SD {0}) not applied!", displayConfig.PrimaryDisplay);
            if (AccessInterface.SetFeature<bool>(Features.WiDiDisplayConnection, Action.SetNoArgs))
            {
                List<DisplayInfo> currentDisplayEnum = base.CurrentConfig.EnumeratedDisplays;
                List<DisplayInfo> enumeratedDisplay = AccessInterface.SetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);
                List<uint> winMonIDList = AccessInterface.GetFeature<List<uint>>(Features.WindowsMonitorID, Action.GetAll);
                List<uint> currentWinMonIDList = base.CurrentConfig.EnumeratedDisplays.Where(dI => !dI.WindowsMonitorID.Equals(0)).Select(dI => dI.WindowsMonitorID).ToList();
                List<uint> diffMonitorIdList = winMonIDList.Except(currentWinMonIDList).ToList();
                if (enumeratedDisplay.Count > currentDisplayEnum.Count)
                {
                    AccessInterface.GetFeature<bool, List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetMethod, Source.AccessAPI, enumeratedDisplay);
                    return true;
                }
            }
            return false;
        }
        internal bool WiDIDisconnect()
        {
            if (base.MachineInfo.OS.Type == OSType.WINBLUE)
            {
                Log.Message("Disconnect WiDi by setting single display {0}", base.GetInternalDisplay());
                DisplayConfig displayConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.GetInternalDisplay() };
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

        internal void GetSwitchPatternForDualDisplayMode(List<DisplayConfigWrapper> argList)
        {
            Log.Verbose("Preparing Switch Pattern for DualDisplay Mode");
            DisplayConfigWrapper displayWrapper = null;

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay });
            argList.Add(displayWrapper);
        }
        internal void GetSwitchPatternForTriDisplayMode(List<DisplayConfigWrapper> argList)
        {
            Log.Verbose("Preparing Switch Pattern for TriDisplay Mode");
            DisplayConfigWrapper displayWrapper = null;
            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(displayWrapper);
            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay });
            argList.Add(displayWrapper);
            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay });
            argList.Add(displayWrapper);

        }

        protected bool SetNValidateConfig(DisplayConfig argConfig)
        {
            if (argConfig.ConfigType == DisplayConfigType.TDC || argConfig.ConfigType == DisplayConfigType.TED)
                Thread.Sleep(5000);
            if (!IsWiDiConnected())
            {
                if (!WiDiReConnect())
                    CheckWiDiStatus();
            }
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argConfig))
            {
                testConfig = argConfig;
                Log.Success("Switch successful to {0} ", argConfig.GetCurrentConfigStr());
                Log.Message("Set the maximum display mode on all the active displays");
                return true;
            }
            else
                Log.Abort("Config not applied!");
            return false;
        }

        protected List<DisplayModeList> GetAllModesForActiceDisplay()
        {
            if (commonDisplayModeList.Count != 0)
                return commonDisplayModeList;
            else
            {
                WiDiConnectionPersistence();
                Log.Verbose("Getting all suppored modes for all active display");
                commonDisplayModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);
                return commonDisplayModeList;
            }
        }

        protected List<DisplayMode> TestModes(List<DisplayMode> displayModeList)
        {
            List<DisplayMode> testModes = new List<DisplayMode>();
            testModes.Add(displayModeList.First());
            testModes.Add(displayModeList[displayModeList.Count / 2]);
            testModes.Add(displayModeList.Last());
            return testModes;
        }

        protected void ApplyModeAndVerify(DisplayMode argDispMode, bool connectWiDi = true)
        {
            if (connectWiDi)
            {
                if (!IsWiDiConnected())
                    WiDiReConnect();
            }
            if (argDispMode.InterlacedFlag == 0)
            {
                Log.Message(true, "Setting Mode : {0} for {1}", GetModeStr(argDispMode), argDispMode.display);
                if (!AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argDispMode))
                    Log.Fail("Fail to apply Mode");
                else
                    Log.Success("Mode applied successfully");
            }
        }

        protected void ApplyModeNVerify_CUI(DisplayMode argDispMode)
        {
            if (!IsWiDiConnected())
                WiDiReConnect();
            Log.Message(true, "Setting Mode : {0} for {1}", GetModeStr(argDispMode), argDispMode.display);
            AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argDispMode);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDispMode.display).First();
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            if (actualMode.HzRes == argDispMode.HzRes && actualMode.VtRes == argDispMode.VtRes && actualMode.RR == argDispMode.RR)
                Log.Success("Mode applied successfully");
            else
                Log.Fail("Fail to apply Mode");
        }

        protected void RotateNVerify(DisplayMode argMode, uint argAngle)
        {
            if (!IsWiDiConnected())
                WiDiReConnect();
            DisplayMode actualMode;
            argMode.Angle = argAngle;
            Log.Message(true, "Rotating the display {0} through OS call to {1}, {2} Deg", argMode.display, argMode.GetCurrentModeStr(true), argAngle);
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argMode))
            {
                actualMode = VerifyRotation(argMode.display, argMode);
                if (actualMode.HzRes != argMode.HzRes ||
                    actualMode.VtRes != argMode.VtRes ||
                    actualMode.Bpp != argMode.Bpp ||
                    actualMode.RR != argMode.RR ||
                    actualMode.Angle != argMode.Angle ||
                    actualMode.InterlacedFlag != argMode.InterlacedFlag)
                {
                    Log.Fail(false, "Mode set failed for display {0}: SetMode - {1}, CurrentMode - {2}. Trying again!", actualMode.display, argMode.GetCurrentModeStr(false), actualMode.GetCurrentModeStr(false));
                }
                else
                    Log.Success("Mode is set Successfully for display {0}: {1}", actualMode.display, actualMode.GetCurrentModeStr(false));
            }
            else
                Log.Fail(false, "Desired mode is not set !!!");
        }
        private DisplayMode VerifyRotation(DisplayType argDisplay, DisplayMode argSetMode)
        {
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplay).First();
            DisplayMode currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            if (currentMode.InterlacedFlag > 0)
                argSetMode.RR = currentMode.RR;
            if (currentMode.CanFlip())
            {
                uint temp = currentMode.HzRes;
                currentMode.HzRes = currentMode.VtRes;
                currentMode.VtRes = temp;
            }
            return currentMode;
        }

        protected string GetModeStr(DisplayMode argMode)
        {
            return string.Concat(argMode.HzRes, "x", argMode.VtRes, "x", argMode.RR, argMode.InterlacedFlag.Equals(0) ? "p Hz" : "i Hz", "x", argMode.Bpp);
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
        protected List<DisplayMode> FilterModeLists(List<DisplayMode> displayMode)
        {
            List<DisplayMode> modeList = new List<DisplayMode>();
            List<DisplayMode> supportedModes = new List<DisplayMode>();
            for (int i = 0; i < displayMode.Count; i++)
            {
                int j = i + 1;
                supportedModes.Add(displayMode[i]);
                for (; j < displayMode.Count; j++)
                {
                    if (displayMode[i].HzRes == displayMode[j].HzRes &&
                        displayMode[i].VtRes == displayMode[j].VtRes)
                    {
                        i = j;
                        supportedModes.Add(displayMode[j]);
                    }
                }
                supportedModes.Sort((x, y) => x.RR.CompareTo(y.RR));
                modeList.AddRange(supportedModes);
                supportedModes.Clear();
            }
            return modeList;
        }

        internal void GetExternalDisplay()
        {
            Log.Verbose("base.CurrentConfig.DisplayList {0}", base.CurrentConfig.DisplayList.Count);
            foreach (DisplayType DT in base.CurrentConfig.CustomDisplayList)
            {
                switch (DT)
                {
                    case DisplayType.EDP:
                        pDisplayList.Add(DT);
                        break;
                    case DisplayType.HDMI:
                    case DisplayType.HDMI_2:
                    case DisplayType.HDMI_3:
                        Log.Verbose("display {0} added", DT); 
                        externalDisplayList.Add(DT);
                        pDisplayList.Add(DT);
                        break;
                    case DisplayType.DP:
                    case DisplayType.DP_2:
                    case DisplayType.DP_3:
                        Log.Verbose("display {0} added", DT); 
                        externalDisplayList.Add(DT);
                        pDisplayList.Add(DT);
                        break;
                }
            }
        }

        protected void VerifyProtectionHDCP(DisplayType argDisplayType, string argOnOff, int argLevel, string argMyDictionary)
        {
            string hdcpStatus = String.Concat("Calling set HDCP with level = ", argLevel, " (OPM_HDCP_", argOnOff, ")");
            Log.Message(true, "Verify HDCP Protection in log for {0} is {1}", argDisplayType, argMyDictionary);
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
                        if (nextLine.Contains(argMyDictionary))
                        {
                            flagSuccess = 1;
                            Log.Success("Log file for {0} contains {1}", argDisplayType, argMyDictionary);
                        }
                    }
                }
            }
            if (flagSuccess == 0)
                Log.Fail("Log file for {0} does not contains {1}", argDisplayType, argMyDictionary);
            file.Close();
        }

        protected void RunOPMTester(DisplayConfig config)
        {
            RemoveOPMInstances();
            Log.Message(true, "Run OPM tester and activate HDCP on WIDI display");
            DisplayHierarchy dH = DisplayExtensions.GetDispHierarchy(config, DisplayType.WIDI);
            Log.Message("Run OPM Tester and choose Activate HDCP from menu");
            HDCPParams hdcpParams = new HDCPParams()
            {
                HDCPPlayerInstance = HDCPPlayerInstance.Player_1,
                HDCPOptions = HDCPOptions.ActivateHDCP,
                HDCPApplication = HDCPApplication.OPMTester,
                DisplayHierarchy = dH,
                CurrentConfig = config
            };
            AccessInterface.SetFeature<HDCPParams>(Features.HDCP, Action.Set, hdcpParams);
            VerifyProtectionHDCP(DisplayType.WIDI, "ON", 1, "SetProtection HDCP succeeded");
            hdcpParams.HDCPOptions = HDCPOptions.Close;
            AccessInterface.SetFeature<HDCPParams>(Features.HDCP, Action.Set, hdcpParams);
        }
        public void SwitchToPowerEvent(PowerParams powerParams)
        {
            Log.Message(true, "Put the system into {0} state & resume", powerParams.PowerStates.ToString());
            base.EventResult(powerParams.PowerStates, base.InvokePowerEvent(powerParams, powerParams.PowerStates));
            Log.Verbose("Verifying audio register and endpoints are correct or not.");
        }

        public void RemoveOPMInstances()
        {
            Log.Message(true, "Remove any instances of OPM tester in binary");
            string[] directories = Directory.GetDirectories(Directory.GetCurrentDirectory(), "OPM*");
            foreach (string dir in directories)
            {
                string[] files = Directory.GetFiles(dir);
                foreach (string g in files)
                {
                    File.SetAttributes(g, FileAttributes.Normal);
                    Thread.Sleep(1000);
                    File.Delete(g);
                }
                Directory.Delete(dir);
            }
        }

        public bool VerifyMEDriver()
        {
            Log.Verbose("Verifying ME Driver Status");
            Process MEInstallProcess = CommonExtensions.StartProcess("wmic", " product where \"Name like '%Management Engine Components%'\" get Name", 0);
            MEInstallProcess.WaitForExit();
            StreamReader reader = MEInstallProcess.StandardOutput;
            string output = reader.ReadToEnd();
            if (output.Contains("Management Engine Components"))
            {
                Log.Verbose("ME Driver is already installed.");
                return true;
            }
            else
            {
                Log.Verbose("ME Driver is not installed on DUT");
                return false;
            }
        }

        public void InstallMEDriver()
        {
            if (!Directory.Exists(base.ApplicationManager.ApplicationSettings.WIDiAppPath))
                Log.Abort("ME Driver not found in {0}", base.ApplicationManager.ApplicationSettings.WIDiAppPath);
            else
            {
                Log.Message("Installing ME Driver");
                string path = base.ApplicationManager.ApplicationSettings.WIDiAppPath + "\\SetupME.exe";
                CommonExtensions.StartProcess(path, " /s");
                Thread.Sleep(5000);
                UIABaseHandler uiaBaseHandler = new UIABaseHandler();

                AutomationElement rootElement = AutomationElement.RootElement;
                AutomationElement appElement = null;
                Condition regCondition = null;
                regCondition = new PropertyCondition(AutomationElement.NameProperty, "Install");
                appElement = rootElement.FindFirst(TreeScope.Descendants, regCondition);
                if (appElement != null)
                {
                    AutomationElement elem = UIABaseHandler.SelectElementNameControlType("Install", ControlType.Button);
                    uiaBaseHandler.Invoke(elem);
                    Thread.Sleep(10000);
                    this._powerParams = new PowerParams();
                    this._powerParams.Delay = 5;
                    base.InvokePowerEvent(this._powerParams, PowerStates.S5);
                }
            }
        }
    }
}
