namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Text;
    using System.IO;
    using System;
    using System.Collections.Generic;
    using System.Threading;
    using Microsoft.Win32;
    using System.Runtime.InteropServices;
    using System.Windows.Forms;
    [Test(Type = TestType.HasReboot)]
    class SB_WideGamut_Base : TestBase
    {
        protected Dictionary<WideGamutLevel, string> _wbLevelEventMap = null;
        protected string _cscEvent = "PIPE_CSC";
        protected string _wideGamutLP = "WIDEGAMUT_LP";
        protected WideGamutLevel _wideGamutLevel = WideGamutLevel.Unsupported;
        protected Dictionary<DisplayType, DVMU_PORT> _pluggableDisplay = null;
        protected Dictionary<DisplayType, int> _wideGamutInfValue = null;
        protected Dictionary<DisplayType, string> _defaultEDIDMap = null;
        protected List<DisplayType> _pluggableDisplaySim = null;
        public SB_WideGamut_Base()
        {
            _wbLevelEventMap = new Dictionary<WideGamutLevel, string>() { { WideGamutLevel.NATURAL, "WB_SLIDER_LEVEL1" }, 
            { WideGamutLevel.LEVEL2, "WB_SLIDER_LEVEL2" },
            { WideGamutLevel.LEVEL3, "WB_SLIDER_LEVEL3" },
            {WideGamutLevel.LEVEL4, "WB_SLIDER_LEVEL4"  },
           // {WideGamutLevel.VIVID, "WB_SLIDER_LEVEL5"}
            };

            _wideGamutInfValue = new Dictionary<DisplayType, int>() {{DisplayType.EDP,1},
            {DisplayType.DP,2},{DisplayType.HDMI,4}};

            _pluggableDisplay = new Dictionary<DisplayType, DVMU_PORT>() { {DisplayType.HDMI,DVMU_PORT.PORTA},
            {DisplayType.HDMI_2,DVMU_PORT.PORTB}};

            _defaultEDIDMap = new Dictionary<DisplayType, string>();
            _defaultEDIDMap.Add(DisplayType.HDMI, "HDMI_DELL.EDID");
            _defaultEDIDMap.Add(DisplayType.HDMI_2, "HDMI_Dell_3011.EDID");

            _defaultEDIDMap.Add(DisplayType.DP, "DP_3011.EDID");
            _defaultEDIDMap.Add(DisplayType.DP_2, "DP_HP_ZR2240W.EDID");

            _pluggableDisplaySim = new List<DisplayType>();

         }
        
        protected void WideGamutDriver(int argValue)
        {
            Log.Message(true, "Make changes in Registry for Enabling Wide Gamut");
            RegistryParams registryParams = new RegistryParams();
            registryParams.value = argValue;
            registryParams.infChanges = InfChanges.ModifyInf;
            registryParams.registryKey = Registry.LocalMachine;
            registryParams.keyName = "WideGamutFeatureEnable";
            AccessInterface.SetFeature<bool, RegistryParams>(Features.RegistryInf, Action.SetMethod, registryParams);

            //if (!Directory.Exists(base.ApplicationManager.ApplicationSettings.ProdDriverPath)
            //   || Directory.GetFiles(base.ApplicationManager.ApplicationSettings.ProdDriverPath, "Setup.exe").Count().Equals(0))
            //    Log.Abort("Setup file(s) in {0} path not found!", base.ApplicationManager.ApplicationSettings.ProdDriverPath);

            //string infPath = string.Concat(base.ApplicationManager.ApplicationSettings.ProdDriverPath, "\\Graphics");
            //if (!Directory.Exists(infPath) || Directory.GetFiles(infPath, "*.inf").Count().Equals(0))
            //    Log.Abort("INF file in {0} path not found", infPath);

            //Log.Message(true, "Make changes in INF file & Install driver, wide Gamut Value {0}", argValue);
            //infPath = string.Concat(base.ApplicationManager.ApplicationSettings.ProdDriverPath, "\\Graphics");
            //string str = "HKR,, WideGamutFeatureEnable,%REG_DWORD%, ";
            //if (INFFileChanges(infPath, str, str + "0x0" + argValue + " \t"))
            //{
            //    InstallUnInstallParams param = new InstallUnInstallParams();
            //    param.ProdPath = base.ApplicationManager.ApplicationSettings.ProdDriverPath;
            //    if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.InstallDriver, Action.SetMethod, param))
            //        Log.Success("Driver successfully installed");
            //    else
            //    {
            //        Log.Message("Installing through UI approach");
            //        if (!base.InstallThruUI(base.ApplicationManager.ApplicationSettings.ProdDriverPath))
            //            Log.Fail("Driver Installation failed");
            //    }
            //}
            //else
            //{
            //    Log.Message("Driver has {0} as wide gamut value, hence not re installing the driver", argValue);
            //}
        }
        private bool INFFileChanges(string infPath, string argStartsWith, string toBeReplaced)
        {
            //HKR,, WideGamutFeatureEnable,%REG_DWORD%, 0x01 	; 0x01- Enable for LFP, 0x02 - Enable for DP, 0x04 - Enable for HDMI... 
            string fileName = "\\igdlh64.inf";
            StringBuilder newfile = new StringBuilder();
            if (MachineInfo.OS.Architecture.Contains("32"))
                fileName = "\\igdlh.inf";

            Log.Verbose("{0}", string.Concat(infPath, fileName));
            string[] file = File.ReadAllLines(string.Concat(infPath, fileName));

            string temp = "";
            foreach (string line in file)
            {
                if (line.Contains(argStartsWith))
                {
                    string oldString = line.Split(';').First();
                    //if (oldString.Equals(toBeReplaced))
                    //{
                    //    Log.Message("driver nneed not be reinstalled");
                    //    return false;
                    //}
                    //else
                    //{
                    temp = line.Replace(oldString, toBeReplaced);
                    newfile.Append(temp + "\r\n");
                    //}
                    continue;
                }
                newfile.Append(line + "\r\n");
            }
            File.WriteAllText(string.Concat(infPath, fileName), newfile.ToString());
            return true;
        }
        protected bool VerifyInfValue(int argInfValue, DisplayType argWideGamutDisplay)
        {
            string infPath = string.Concat(base.ApplicationManager.ApplicationSettings.ProdDriverPath, "\\Graphics");
            string argStartsWith = "HKR,, WideGamutFeatureEnable,%REG_DWORD%, ";
            string fileName = "\\igdlh64.inf";
            StringBuilder newfile = new StringBuilder();
            if (MachineInfo.OS.Architecture.Contains("32"))
                fileName = "\\igdlh.inf";

            Log.Verbose("{0}", string.Concat(infPath, fileName));
            string[] file = File.ReadAllLines(string.Concat(infPath, fileName));

            foreach (string line in file)
            {
                if (line.Contains(argStartsWith))
                {
                    string oldString = line.Split(';').First();
                    if (oldString.Trim().EndsWith(argInfValue.ToString()))
                    {
                        Log.Success("Inf change {0} is success", argInfValue);
                        WideGamutParams wgObj = new WideGamutParams() { DisplayType = argWideGamutDisplay };
                        WideGamutParams par = AccessInterface.GetFeature<WideGamutParams, WideGamutParams>(Features.WideGamut, Action.GetMethod, Source.AccessAPI, wgObj);
                        if (par.WideGamutLevel != WideGamutLevel.Unsupported)
                        {
                            Log.Success("Wide Gamut is supported");
                            return true;
                        }
                        else
                        {
                            Log.Abort("Wide Gamut is not supported");
                        }
                    }
                    else
                    {
                        Log.Abort("Failed to change Inf value to {0}, current Inf value {1}", argInfValue, oldString);

                    }
                }
            }

            return false;
        }
        protected bool VerifyRegisters(string pRegisterEvent, PIPE pPipe, PLANE pPlane, PORT pPort, bool compare = true)
        {
            Log.Message("Verifying Register for event : {0}", pRegisterEvent);
            bool regValueMatched = true;

            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = pPipe;
            eventInfo.plane = pPlane;
            eventInfo.port = pPort;
            eventInfo.eventName = pRegisterEvent;
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
                    if (compare)
                    {
                        if (!CompareRegisters(driverData.output, reginfo))
                        {
                            Log.Message("Register with offset {0} doesnot match required values", reginfo.Offset);
                            regValueMatched = false;
                        }
                    }
            }

            return regValueMatched;
        }

        protected bool CompareRegisters(uint argDriverData, RegisterInf argRegInfo)
        {
            uint bit = Convert.ToUInt32(argRegInfo.Bitmap, 16);
            Log.Verbose("Bitmap in uint = {0}, Value from register read = {1}", bit, argDriverData);
            uint hex = Convert.ToUInt32(String.Format("{0:X}", argDriverData), 16);
            Log.Verbose("value from reg read in ubit = {0}", hex);
            string valu = String.Format("{0:X}", hex & bit);
            Log.Verbose("after bitmap = {0}", valu);
            if (String.Equals(valu, argRegInfo.Value))
            {
                Log.Message("Register Values Matched");
                return true;
            }
            return false;
        }
        protected bool ApplyWideGamutToDisplay(DisplayType argDispType, WideGamutLevel argWbLevel)
        {
            Log.Message(true, "Applying widegamut {0} to {1}", argWbLevel, argDispType);
                WideGamutParams wbObj = new WideGamutParams();
                wbObj.WideGamutLevel = argWbLevel;
                wbObj.DisplayType = argDispType;
                AccessInterface.SetFeature<WideGamutParams>(Features.WideGamut, Action.Set, Source.AccessAPI, wbObj);
                return true;
        }
        protected Dictionary<WideGamutLevel, string> WBSliderValues()
        {
            if (base.MachineInfo.PlatformDetails.IsLowpower)
            {
                return _wbLevelEventMap.Where(curWbLevel => curWbLevel.Value.Contains("WB_SLIDER_LEVEL1")).ToDictionary(curWbLevel => curWbLevel.Key, curWbLevel => curWbLevel.Value);
            }
            else
            {
                return _wbLevelEventMap;
            }
        }
        protected void ApplyConfigOS(DisplayConfig argDispConfig)
        {
            Log.Message(true, "Applying Config {0}", argDispConfig.GetCurrentConfigStr());
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
            {
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            }
            else
            {
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());
            }
        }
        protected bool VerifyConfig(DisplayConfig argDisplayConfig)
        {
            Log.Message(true, "Verifying config {0} via OS", argDisplayConfig.GetCurrentConfigStr());
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            if (currentConfig.GetCurrentConfigStr().Equals(argDisplayConfig.GetCurrentConfigStr()))
            {
                Log.Success("{0} is verified by OS", argDisplayConfig.GetCurrentConfigStr());
                return true;
            }
            else
            {
                Log.Fail("Config {0} does not match with current config {1}", currentConfig.GetCurrentConfigStr(), argDisplayConfig.GetCurrentConfigStr());
                return false;
            }
        }
        protected void VerifyWideGamutValue(DisplayType argDispType, WideGamutLevel argWbLevel)
        {
            Log.Message(true, "Verifying {0} & CSC for {1}", argWbLevel, argDispType);

            PipePlaneParams pipePlane1 = new PipePlaneParams(argDispType);
            pipePlane1 = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane1);
            Log.Message("For display : {0}  @@@  PIPE : {1} @@@ PLANE : {2}", argDispType, pipePlane1.Pipe, pipePlane1.Plane);

            if (base.MachineInfo.PlatformDetails.IsLowpower)
            {
                if (VerifyRegisters(_wideGamutLP, pipePlane1.Pipe, PLANE.NONE, PORT.NONE))
                    Log.Success("Wide Gamut is enabled for {0}", argDispType);
                else
                    Log.Fail("Wide Gamut is not enabled for {0}", argDispType);

                if (base.MachineInfo.PlatformDetails.Platform == Platform.CHV)
                {
                    if (VerifyRegisters("WIDEGAMUT_LP_DE_GAMMA", pipePlane1.Pipe, PLANE.NONE, PORT.NONE))
                        Log.Success("De Gamma is enabled for {0}", argDispType);
                    else
                        Log.Fail("De Gamma is not enabled for {0}", argDispType);
                }
                Log.Message("WideGamutLevel's are not supported on LP Platforms");
            }
            else
            {
                if (VerifyRegisters(_wbLevelEventMap[argWbLevel], PIPE.NONE, pipePlane1.Plane, PORT.NONE))
                    Log.Success("WideGamut {0} IS VERIFIED for {1}", argWbLevel, argDispType);
                else
                    Log.Fail("WB Slider value is not {0} for {1}", argWbLevel, argDispType);

                if (VerifyRegisters(_cscEvent, PIPE.NONE, pipePlane1.Plane, PORT.NONE))
                    Log.Success("CSC IS VERIFIED for {0}", argDispType);
                else
                    Log.Fail("CSC is not enabled for {0}", argDispType);
            }
        }
        protected virtual void InvokePowerEvent(PowerStates argPowerState)
        {
            Log.Message(true, "Invoking power event {0}", argPowerState);
            PowerParams powerParams = new PowerParams() { Delay = 30 };
            powerParams.PowerStates = argPowerState;
            powerParams.Delay = 30;
            base.EventResult(powerParams.PowerStates, base.InvokePowerEvent(powerParams, powerParams.PowerStates));
        }
        protected void PlugDisplays()
        {
            base.CurrentConfig.PluggableDisplayList.ForEach(curDisp =>
            {
                if (base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).Select(dI => dI.DisplayType).FirstOrDefault() == DisplayType.None)
                {
                    base.HotPlug(curDisp, _defaultEDIDMap[curDisp]);
                    _pluggableDisplaySim.Add(curDisp);
                }
            });
        }
        protected void UnPlugDisplays()
        {
            _pluggableDisplaySim.ForEach(curDisp =>
            {
                base.HotUnPlug(curDisp);
            });
            base.CleanUpHotplugFramework();
        }
    }
}
