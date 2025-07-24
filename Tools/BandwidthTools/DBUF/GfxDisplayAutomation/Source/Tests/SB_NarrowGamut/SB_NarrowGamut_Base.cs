using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Threading;
using Microsoft.Win32;
namespace Intel.VPG.Display.Automation
{
    class SB_NarrowGamut_Base : TestBase
    {
        protected List<DisplayType> _pluggableDisplaySim = null;
        protected Dictionary<DisplayType, string> _defaultEDIDMap = null;
        public SB_NarrowGamut_Base()
        {
            _defaultEDIDMap = new Dictionary<DisplayType, string>();
            _defaultEDIDMap.Add(DisplayType.HDMI, "HDMI_DELL.EDID");
            _defaultEDIDMap.Add(DisplayType.HDMI_2, "HDMI_Dell_3011.EDID");

            _defaultEDIDMap.Add(DisplayType.DP, "DP_3011.EDID");
            _defaultEDIDMap.Add(DisplayType.DP_2, "DP_HP_ZR2240W.EDID");

            _pluggableDisplaySim = new List<DisplayType>();
        }
        protected List<DisplayType> NarrowGamutSupportedDisplays
        {
            get
            {
                List<DisplayType> narrowGamutSupportedDisplays = new List<DisplayType>() { DisplayType.EDP,DisplayType.MIPI };
                return narrowGamutSupportedDisplays;
            }
        }
        protected void NarrowGamutDriver(NarrowGamutOption argNGOption,bool argInstallDriver=true)
        {
            if (!Directory.Exists(base.ApplicationManager.ApplicationSettings.ProdDriverPath)
                   || Directory.GetFiles(base.ApplicationManager.ApplicationSettings.ProdDriverPath, "Setup.exe").Count().Equals(0))
                Log.Abort("Setup file(s) in {0} path not found!", base.ApplicationManager.ApplicationSettings.ProdDriverPath);

            string infPath = string.Concat(base.ApplicationManager.ApplicationSettings.ProdDriverPath, "\\Graphics");
            if (!Directory.Exists(infPath) || Directory.GetFiles(infPath, "*.inf").Count().Equals(0))
                Log.Abort("INF file in {0} path not found", infPath);

            Log.Message(true, "Make changes in INF file & Install driver, Narrow Gamut option: {0}",argNGOption.ToString());
            infPath = string.Concat(base.ApplicationManager.ApplicationSettings.ProdDriverPath, "\\Graphics");

            NarrowGamutParams NGParam = new NarrowGamutParams()
            {
                INFFilePath = infPath,
                narrowGamutOption = argNGOption
            };
            AccessInterface.SetFeature<NarrowGamutParams>(Features.NarrowGamut, Action.Set, Source.AccessAPI, NGParam);
            if (argInstallDriver)
            InstallDriver();
        }
        protected void SetNarrowGamutStatus(DisplayType argDispType, NarrowGamutOption argNgOption, bool argDriverStatus=true)
        {
            NarrowGamutParams obj = new NarrowGamutParams();
            obj.DisplayType = argDispType;
            obj.narrowGamutOption = argNgOption;
            obj.driverStatus=argDriverStatus;
            AccessInterface.SetFeature<NarrowGamutParams>(Features.NarrowGamut, Action.Set, Source.AccessAPI, obj);
            if(argDriverStatus)
            CheckNarrowGamutRegister(argDispType, argNgOption);
        }
        protected void CheckNarrowGamutRegister(DisplayType argDispType, NarrowGamutOption argNgOption)
        {
            Log.Message(true, "Verifying CSC for {0}", argDispType);
            PipePlaneParams pipePlane1 = new PipePlaneParams(argDispType);
            pipePlane1 = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane1);
            Log.Message("For display : {0}  @@@  PIPE : {1} @@@ PLANE : {2}", argDispType, pipePlane1.Pipe, pipePlane1.Plane);

            
            if (argNgOption == NarrowGamutOption.EnableNarrowGamut)
            {
                VerifyRegisters("NARROW_GAMUT_ENABLE", PIPE.NONE, pipePlane1.Plane, PORT.NONE);
               
                if (VerifyRegisters("CURSOR_STATUS", PIPE.NONE, pipePlane1.Plane, PORT.NONE, false))
                {
                    Log.Success("Cursor is enabled for {0} on {1}", argDispType, pipePlane1.Plane);
                    if (base.MachineInfo.PlatformDetails.Platform != Platform.CHV)
                    {
                        if (VerifyRegisters("CURSOR_CSC_ENABLE", PIPE.NONE, pipePlane1.Plane, PORT.NONE))
                        {
                            Log.Success("cursor CSC is enabled");
                        }
                        else
                            Log.Fail("Cursor CSC is disabled");
                    }
                }
                else
                {
                    Log.Alert("Cursor is not enabled for {0}",argDispType);
                }
                if (base.MachineInfo.PlatformDetails.Platform == Platform.SKL)
                {
                    VerifyRegisters("PIPE_ENABLE", pipePlane1.Pipe, PLANE.NONE, PORT.NONE);
                }
            }
            else
            {
                VerifyRegisters("NARROW_GAMUT_DISABLE", PIPE.NONE, pipePlane1.Plane, PORT.NONE);
            }

        }
       
        protected bool VerifyRegisters(string pRegisterEvent, PIPE pPipe, PLANE pPlane, PORT pPort, bool compare = true)
        {
            Log.Message(true, "Verifying Register for event : {0}", pRegisterEvent);
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
                            Log.Fail("Register with offset {0} doesnot match required values", reginfo.Offset);
                            regValueMatched = false;
                        }
                    }
                    else
                    {
                        uint bit = Convert.ToUInt32(reginfo.Bitmap, 16);
                        Log.Verbose("Bitmap in uint = {0}, Value from register read = {1}", bit, driverData.output);
                        uint hex = Convert.ToUInt32(String.Format("{0:X}", driverData.output), 16);
                        Log.Verbose("value from reg read in ubit = {0}", hex);
                        string valu = String.Format("{0:X}", hex & bit);
                        Log.Verbose("after bitmap = {0}", valu);
                        if (String.Equals(valu, reginfo.Value))
                        {
                            Log.Alert("Register with offset {0}  have value {1}", reginfo.Offset, reginfo.Value);
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
                Log.Success("Register Values Matched");
                return true;
            }
            return false;
        }

        protected void ApplyConfig(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());

            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            if (currentConfig.GetCurrentConfigStr().Equals(argDispConfig.GetCurrentConfigStr()))
            {
                Log.Success("{0} is verified by OS", argDispConfig.GetCurrentConfigStr());
               // MoveCursorPosition(argDispConfig, NarrowGamutSupportedDisplays.First());
            }
            else
                Log.Fail(" current Config {0} does not match with expected config {1}", currentConfig.GetCurrentConfigStr(), argDispConfig.GetCurrentConfigStr());

        }
        protected void PowerEvent(PowerStates argPowerState)
        {
            Log.Message(true, " Invoking Power State {0}", argPowerState);
            PowerParams obj = new PowerParams()
            {
                PowerStates = argPowerState,
                Delay = 30
            };
            base.InvokePowerEvent(obj, argPowerState);
        }
        protected void VerifyInfChanges(NarrowGamutOption argNGOption)
        {
            if (!Directory.Exists(base.ApplicationManager.ApplicationSettings.ProdDriverPath)
                   || Directory.GetFiles(base.ApplicationManager.ApplicationSettings.ProdDriverPath, "Setup.exe").Count().Equals(0))
                Log.Abort("Setup file(s) in {0} path not found!", base.ApplicationManager.ApplicationSettings.ProdDriverPath);

            string infPath = string.Concat(base.ApplicationManager.ApplicationSettings.ProdDriverPath, "\\Graphics");
            if (!Directory.Exists(infPath) || Directory.GetFiles(infPath, "*.inf").Count().Equals(0))
                Log.Abort("INF file in {0} path not found", infPath);

            Log.Message(true, "Make changes in INF file & Install driver, Narrow Gamut");
            infPath = string.Concat(base.ApplicationManager.ApplicationSettings.ProdDriverPath, "\\Graphics");

            NarrowGamutParams NGParam = new NarrowGamutParams() { narrowGamutOption = argNGOption, INFFilePath = infPath };
            AccessInterface.SetFeature<NarrowGamutParams>(Features.NarrowGamut, Action.Set, Source.AccessAPI, NGParam);
        }
        protected bool RegisterCheck(DisplayType display, DisplayInfo displayInfo, string eventName)
        {
            bool match = false;
            DisplayMode targetMode;
            PipePlaneParams pipePlaneObject = new PipePlaneParams(display);
            if (eventName.Contains("SPRITE") && !eventName.Contains("CLONE") && !eventName.Contains("NON_HDMI") && base.MachineInfo.OS.Type == OSType.WIN7)
                eventName += "_Win7";


            PipePlaneParams pipePlaneParams = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlaneObject);
            if (VerifyRegisters(eventName, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, true))
            {
                Log.Success("Registers verified for event {0} on display {1}", eventName, display);
                match = true;
            }
            Log.Message("Check if Cursor exixts, if Cursor connected verify Cursor registers");
            //if (CursorConnected())

            return match;
        }
        protected void SetWideGamut(DisplayType argDispType, WideGamutLevel argWBLevel)
        {
            Log.Message(true, "Applying widegamut level {0}  to {1}", argDispType, argWBLevel);
            WideGamutParams wbObj = new WideGamutParams()
            {
                DisplayType = argDispType,
                option = WideGamutOption.SetWideGamut,
                WideGamutLevel = argWBLevel
            };
            AccessInterface.SetFeature<WideGamutParams>(Features.WideGamut, Action.Set, Source.AccessAPI, wbObj);
        }
        protected void InstallDriver()
        {
            InstallUnInstallParams param = new InstallUnInstallParams();
            param.ProdPath = base.ApplicationManager.ApplicationSettings.ProdDriverPath;
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.InstallDriver, Action.SetMethod, param))
                Log.Success("Driver successfully installed");
            else
            {
                Log.Message("Installing through UI approach");
                if (!base.InstallThruUI(base.ApplicationManager.ApplicationSettings.ProdDriverPath))
                    Log.Fail("Driver Installation failed");
            }
        }
        protected void UnistallDriver()
        {
            Log.Message(true, "Uninstall the driver.");
            InstallUnInstallParams param = new InstallUnInstallParams();
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.UnInstallDriver, Action.SetMethod, param))
                Log.Success("Successfully unInstall driver package");
            else
                Log.Fail("Failed to UnInstall driver package");
        }
        protected void copyBack()
        {
            string temp = string.Concat(base.ApplicationManager.ApplicationSettings.ProdDriverPath, "\\Graphics");

              string fileName = "\\igdlh64.inf";
            StringBuilder newfile = new StringBuilder();
            if (MachineInfo.OS.Architecture.Contains("32"))
                fileName = "\\igdlh.inf";

            string infPath=Path.Combine(temp,fileName);
            string directoryPath=Path.Combine(base.ApplicationManager.ApplicationSettings.ProdDriverPath,"Copy");
            Directory.CreateDirectory(directoryPath);
            File.Copy(infPath, directoryPath);
        }
        protected void RevertNarrowGamutChanges()
        {
            NarrowGamutDriver(NarrowGamutOption.ResetINF, false);
            //Log.Message(true, "Make changes in Registry for Disabling Narrow Gamut");
            //RegistryParams registryParams = new RegistryParams();
            //registryParams.value = 0;
            //registryParams.infChanges = InfChanges.RevertInf;
            //registryParams.registryKey = Registry.LocalMachine;
            //registryParams.keyName = "NarrowGamutFeatureEnable";
            //AccessInterface.SetFeature<bool, RegistryParams>(Features.RegistryInf, Action.SetMethod, registryParams);

            //Log.Message(true, "Make changes in Registry for Disabling over ride chromaticity ");
            //RegistryParams registryParams1 = new RegistryParams();
            //registryParams1.value = 0;
            //registryParams1.infChanges = InfChanges.RevertInf;
            //registryParams1.registryKey = Registry.LocalMachine;
            //registryParams1.keyName = "OverRideChromaticityData";
            //AccessInterface.SetFeature<bool, RegistryParams>(Features.RegistryInf, Action.SetMethod, registryParams1); 
        }
        protected void VerifyNarrowGamutChangesOnRevert()
        {
            //NarrowGamutSupportedDisplays.Intersect(base.CurrentConfig.DisplayList).ToList().ForEach(curDisp =>
            //{
            //    SetNarrowGamutStatus(curDisp, NarrowGamutOption.EnableNarrowGamut, false);
            //});
        }
    }
}
