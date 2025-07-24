 using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    using System.Text.RegularExpressions;
    using System.Runtime.InteropServices;
    using System.IO;
namespace Intel.VPG.Display.Automation
{
    class SB_VRR_GenerateFlip_Base:TestBase
    {
        
        protected string[] fileEntries;
        protected const int MAX_PLANES = 13;
        protected const int MAX_PIPES = 3;
        protected const string MPORegisterEvent = "MPO";
        protected const string NV12RegisterEvent = "NV12";
        protected const string Plane_Scalars_Enabled = "Plane_Scalars_Enabled";
        protected Dictionary<string, string> _dumpsDictionary = null;
        protected Dictionary<string, string> _paramsDictionary = null;


        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            this._dumpsDictionary = new Dictionary<string, string>()
            {
                 { "YTile", string.Concat(base.ApplicationManager.ApplicationSettings.ULTDumpFiles,"\\YtileDumps")},  
                 { "Charms", string.Concat(base.ApplicationManager.ApplicationSettings.ULTDumpFiles,"\\CharmsDumps")},
                 { "NV12", string.Concat(base.ApplicationManager.ApplicationSettings.ULTDumpFiles,"\\NV12Dumps")},
                 { "RC", string.Concat(base.ApplicationManager.ApplicationSettings.ULTDumpFiles,"\\RCDumps")},
            };
            this._paramsDictionary = new Dictionary<string, string>()
            {
                 { "YTile", string.Concat(Directory.GetCurrentDirectory(), "\\Mapper\\YTilingPlaneParams.xml")},  
                 { "Charms", string.Concat(Directory.GetCurrentDirectory(), "\\Mapper\\CharmsPlaneParams.xml")},
                 { "NV12", string.Concat(Directory.GetCurrentDirectory(), "\\Mapper\\NV12PlaneParams.xml")}
            };
        }
        protected void ApplyConfigOS(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());
        }
        
        protected void VerifyConfigOS(DisplayConfig argDisplayConfig)
        {
            Log.Message(true, "Verifying config {0} via OS", argDisplayConfig.GetCurrentConfigStr());
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            if (currentConfig.GetCurrentConfigStr().Equals(argDisplayConfig.GetCurrentConfigStr()))
                Log.Success("{0} is verified by OS", argDisplayConfig.GetCurrentConfigStr());
            else
                Log.Fail("Config {0} does not match with current config {1}", argDisplayConfig.GetCurrentConfigStr(), currentConfig.GetCurrentConfigStr());
        }

        //checks VRR status register and returns the VRR enable live status.        
        public uint IsVRREnabled(DisplayType disp)
        {
            uint ret = 0;
            PipePlaneParams pipePlane1 = new PipePlaneParams(disp);
            pipePlane1 = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane1);
            ret= base.GetRegisterValue("VRR_Status", pipePlane1.Pipe, PLANE.NONE, PORT.NONE);
            return ret;
        }
        
        //checks VRR capability of all connected displays and adds to displayList
        public void GetVRRCapableDisplays(DisplayList displayList)
        {
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                if(curDisp == DisplayType.EDP || curDisp == DisplayType.DP)
                {
                    //get MSA_timing_par_ignored from DPCD (offset 00007h: bit 6)
                    DpcdInfo dpcd = new DpcdInfo();
                    dpcd.Offset = Convert.ToUInt32("00007", 16);
                    DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).First();
                    dpcd.DispInfo = displayInfo;
                    AccessInterface.GetFeature<DpcdInfo, DpcdInfo>(Features.DpcdRegister, Action.GetMethod, Source.AccessAPI, dpcd);
                    uint msa_timing_par_ignored= (dpcd.Value & 0x40) >> 6;

                    //get continuous_freq_sup, VRR_min and VRR_max from EDID
                    if(msa_timing_par_ignored==1 && displayInfo.VRRInfo.ContFreqSup && displayInfo.VRRInfo.RR_min!=0 && displayInfo.VRRInfo.RR_max!=0)
                    {
                        displayList.Add(curDisp);
                    }                   
                }
            });
        }
        protected void InvokePowerEvent(PowerStates argPowerState)
        {
            Log.Message(true, "Invoking power event {0}", argPowerState);
            PowerParams powerParams = new PowerParams() { Delay = 30 };
            powerParams.PowerStates = argPowerState;
            base.EventResult(powerParams.PowerStates, base.InvokePowerEvent(powerParams, powerParams.PowerStates));
        }
        protected bool RegisterCheck(DisplayType display, DisplayInfo displayInfo, string eventName, int expectedPlanesEnabled, int expectedNV12Surfaces)
        {
            bool match = false;
            PipePlaneParams pipePlaneObject = new PipePlaneParams(display);
            PipePlaneParams pipePlaneParams = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlaneObject);
            if (VerifyMPORegisters(eventName, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, expectedPlanesEnabled, expectedNV12Surfaces))
            {
                Log.Success("Registers verified for event {0} on display {1}", eventName, display);
                match = true;
            }
            return match;
        }
        private bool VerifyMPORegisters(string registerEvent, PIPE pipe, PLANE plane, PORT port, int expectedPlanesEnabled, int expectedNV12Surfaces)
        {
            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = pipe;
            eventInfo.plane = plane;
            eventInfo.port = port;
            eventInfo.eventName = registerEvent;
            int countEnabledPlanesPerPipe = 0;
            int countNV12Surfaces = 0;

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
                {
                    if (registerEvent == MPORegisterEvent)
                    {
                        if (!CompareRegisters(driverData.output, reginfo))
                        {
                            Log.Message("Plane offset {0} is not enabled", driverData.input.ToString("X"));
                        }
                        else
                        {
                            Log.Message("Plane offset {0} is enabled", driverData.input.ToString("X"));
                            countEnabledPlanesPerPipe = countEnabledPlanesPerPipe + 1;
                        }
                    }
                    else
                    {
                        if (!CompareRegisters(driverData.output, reginfo))
                        {
                            Log.Message("Plane offset {0} not in NV12 Color Format", driverData.input.ToString("X"));
                        }
                        else
                        {
                            Log.Message("Plane offset {0} is in NV12 color format", driverData.input.ToString("X"));
                            countNV12Surfaces = countNV12Surfaces + 1;
                        }
                    }
                }
            }
            if (expectedNV12Surfaces != 999)
            {
                if (countNV12Surfaces == expectedNV12Surfaces)
                    return true;
                else
                {
                    Log.Fail("Mismatch in NV12 formats of planes; Expected NV12 planes enabled = {0}, actual enabled planes = {1}", expectedNV12Surfaces, countNV12Surfaces);
                    return false;
                }

            }
            else
            {
                if (countEnabledPlanesPerPipe == expectedPlanesEnabled)
                    return true;
                else
                {
                    Log.Fail("Mismatch in planes enabled; Expected number of planes enabled = {0}, actual enabled planes = {1}", expectedPlanesEnabled, countEnabledPlanesPerPipe);
                    return false;
                }

            }
        }
        protected void EnableDisableCursor(bool enable)
        {
            SetUpDesktopArgs driverParams = new SetUpDesktopArgs(SetUpDesktopArgs.SetUpDesktopOperation.ShowCursor);
            if (enable == false)
                driverParams.FunctionName = SetUpDesktopArgs.SetUpDesktopOperation.HideCursor;

            if (!AccessInterface.SetFeature<bool, SetUpDesktopArgs>(Features.SetUpDesktop, Action.SetMethod, driverParams))
                Log.Fail("Failed to {0} Cursor", enable ? "enable" : "disable");
        }

        protected int GetMaxScalarsAvailable(DisplayConfig argDisplayConfig, DisplayType display)
        {
            int availableScalars = GetScalarsAvailable(display);

            if (argDisplayConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
            {
                if (argDisplayConfig.TertiaryDisplay != DisplayType.None)
                {
                    availableScalars = Math.Min(availableScalars, GetScalarsAvailable(argDisplayConfig.TertiaryDisplay));
                }
                availableScalars = Math.Min(availableScalars, GetScalarsAvailable(argDisplayConfig.SecondaryDisplay));
            }
            return availableScalars;
        }

        protected int GetScalarsAvailable(DisplayType display)
        {
            int availableScalars = 2;
            PipePlaneParams pipePlaneObject = new PipePlaneParams(display);
            PipePlaneParams pipePlaneParams = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlaneObject);

            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = pipePlaneParams.Pipe;
            eventInfo.plane = pipePlaneParams.Plane;
            eventInfo.port = PORT.NONE;
            eventInfo.eventName = Plane_Scalars_Enabled;
            

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
                {
                    if (!CompareRegisters(driverData.output, reginfo))
                    {
                        Log.Message("scalar {0} is not enabled", driverData.input.ToString("X"));
                    }
                    else
                    {
                        Log.Message("scalar {0} is enabled", driverData.input.ToString("X"));
                        availableScalars = availableScalars - 1;
                    }
                }
            }
            return availableScalars;
        }

        private bool DoULTEscape(ULT_ESCAPE_CODE escapeCode, object Ult_Esc_Args)
        {
            bool status = true;
            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(escapeCode, Ult_Esc_Args);
            if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
            {
                Log.Fail(String.Format("Failed to perform: {0}", escapeParams.ULT_Escape_Type));
                status = false;
            }
            return status;
        }

        protected void EnableFeature(bool status, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE featureType)
        {
            ULT_ESC_ENABLE_DISABLE_FEATURE_ARGS ult_Esc_Args = new ULT_ESC_ENABLE_DISABLE_FEATURE_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_ESC_ENABLE_DISABLE_FEATURE;
            ult_Esc_Args.bEnableFeature = status;
            ult_Esc_Args.eFeatureEnable = featureType;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;

            if (!DoULTEscape(ULT_ESCAPE_CODE.ULT_ESC_ENABLE_DISABLE_FEATURE, ult_Esc_Args))
                Console.WriteLine("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                if (ult_Esc_Args.dwRetErrorCode != 0)
                {
                    CommonExtensions.PrintULTErrorCodes(ult_Esc_Args.dwRetErrorCode);
                }
            }
        }
        protected bool ULT_FW_Create_Resource(uint x, uint y, ULT_PIXELFORMAT SRC_Pixel_Format, ULT_TILE_FORMATS Tile_Format,bool Is_RC_Format, ref UInt64 pGmmBlock, ref IntPtr pUserVirtualAddress, ref UInt64 surfaceSize)
        {
            ULT_CREATE_RES_ARGS ult_Esc_Args = new ULT_CREATE_RES_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_CREATE_RESOURCE;
            ult_Esc_Args.ulBaseWidth = x;
            ult_Esc_Args.ulBaseHeight = y;
            ult_Esc_Args.Format = SRC_Pixel_Format;
            ult_Esc_Args.TileFormat = Tile_Format;
            ult_Esc_Args.AuxSurf = Is_RC_Format;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;

            if (!DoULTEscape(ULT_ESCAPE_CODE.ULT_CREATE_RESOURCE, ult_Esc_Args))
                Log.Abort("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                if (ult_Esc_Args.dwRetErrorCode != 0)
                {
                    CommonExtensions.PrintULTErrorCodes(ult_Esc_Args.dwRetErrorCode);
                    return false;
                }
                else
                {
                    pGmmBlock = ult_Esc_Args.pGmmBlock;
                    pUserVirtualAddress = (IntPtr)ult_Esc_Args.pUserVirtualAddress;
                    surfaceSize = ult_Esc_Args.u64SurfaceSize;
                    return true;
                }
            }
            return false;
        }

        protected bool ULT_FW_Free_Resource(UInt64 pGmmBlock)
        {
            ULT_FREE_RES_ARGS ult_Esc_Args = new ULT_FREE_RES_ARGS();
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_FREE_RESOURCE;
            ult_Esc_Args.pGmmBlock = pGmmBlock;

            if (!DoULTEscape(ULT_ESCAPE_CODE.ULT_FREE_RESOURCE, ult_Esc_Args))
                Log.Abort("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                if (ult_Esc_Args.dwRetErrorCode != 0)
                {
                    CommonExtensions.PrintULTErrorCodes(ult_Esc_Args.dwRetErrorCode);
                    return false;
                }
                else
                {
                    Log.Message("Freed the resource");
                }
                return true;
            }
            return false;
        }

        protected bool ULT_FW_Set_Source_Address(UInt64 pGmmBlock, uint sourceID, uint dataSize, ULT_SETVIDPNSOURCEADDRESS_FLAGS Flag)
        {
            ULT_ESC_SET_SRC_ADD_ARGS ult_Esc_Args = new ULT_ESC_SET_SRC_ADD_ARGS();
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_SET_SRC_ADDRESS;
            ult_Esc_Args.pGmmBlock = pGmmBlock;
            ult_Esc_Args.ulSrcID = sourceID;
            ult_Esc_Args.ulDataSize = 0x7f8000;
          //  ult_Esc_Args.ulDataSize = 8294400;//dataSize;
            ult_Esc_Args.Flags = Flag;

            if (!DoULTEscape(ULT_ESCAPE_CODE.ULT_SET_SRC_ADDRESS, ult_Esc_Args))
                Log.Abort("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                if (ult_Esc_Args.dwRetErrorCode != 0)
                {
                    CommonExtensions.PrintULTErrorCodes(ult_Esc_Args.dwRetErrorCode);
                    return false;
                }
                else
                {
                   // Log.Message("Set Source Address Successful");
                }
                return true;
            }
            return false;
        }
        protected bool ULT_FW_Get_MPO_Caps(uint sourceID, ref ULT_MPO_CAPS argMpoCaps)
        {
            ULT_ESC_MPO_CAPS_ARGS ult_Esc_Args = new ULT_ESC_MPO_CAPS_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_GET_MPO_CAPS;
            ult_Esc_Args.ulVidpnSourceID = sourceID;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;

            if (!DoULTEscape(ULT_ESCAPE_CODE.ULT_GET_MPO_CAPS, ult_Esc_Args))
                Log.Abort("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                if (ult_Esc_Args.dwRetErrorCode != 0)
                {
                    CommonExtensions.PrintULTErrorCodes(ult_Esc_Args.dwRetErrorCode);
                    return false;
                }
                else
                {
                    argMpoCaps = ult_Esc_Args.stMPOCaps;
                }
                return true;
            }
            return false;
        }
        internal bool ULT_FW_MPO_Group_Caps(uint sourceID, uint groupIndex, ref ULT_MPO_GROUP_CAPS argMpoGroupCaps)
        {
            ULT_MPO_GROUP_CAPS_ARGS ult_Esc_Args = new ULT_MPO_GROUP_CAPS_ARGS();
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_MPO_GROUP_CAPS;
            ult_Esc_Args.ulVidpnSourceID = sourceID;
            ult_Esc_Args.uiGroupIndex = groupIndex;

            if (!DoULTEscape(ULT_ESCAPE_CODE.ULT_MPO_GROUP_CAPS, ult_Esc_Args))
                Log.Abort("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                if (ult_Esc_Args.dwRetErrorCode != 0)
                {
                    CommonExtensions.PrintULTErrorCodes(ult_Esc_Args.dwRetErrorCode);
                    return false;
                }
                else
                {
                    argMpoGroupCaps = ult_Esc_Args.stMPOGroupCaps;
                }
                return true;
            }
            return false;
        }
        internal bool ULT_FW_Check_MPO(SB_MPO_CHECKMPOSUPPORT_PATH_INFO[] sbMpoCheckMpoSupportPathInfo, uint numPaths, uint config, ref bool supported, ref uint failureReason, ref CHECKMPOSUPPORT_RETURN_INFO checkMpoSupportReturnInfo)
        {
            SB_MPO_CHECKMPOSUPPORT_ARGS ult_Esc_Args = new SB_MPO_CHECKMPOSUPPORT_ARGS();
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ult_Esc_Args.dwSourceID = 0;
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_CHECK_MPO;
            ult_Esc_Args.stCheckMPOPathInfo = sbMpoCheckMpoSupportPathInfo;
            ult_Esc_Args.ulNumPaths = numPaths;
            ult_Esc_Args.ulConfig = config;
            ult_Esc_Args.stMPOCheckSuppReturnInfo = new CHECKMPOSUPPORT_RETURN_INFO();

            if (!DoULTEscape(ULT_ESCAPE_CODE.ULT_CHECK_MPO, ult_Esc_Args))
                Log.Abort("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                if (ult_Esc_Args.dwRetErrorCode != 0)
                {
                    CommonExtensions.PrintULTErrorCodes(ult_Esc_Args.dwRetErrorCode);
                    return false;
                }
                else
                {
                    failureReason = ult_Esc_Args.ulFailureReason;
                    supported = ult_Esc_Args.bSupported;
                    checkMpoSupportReturnInfo = ult_Esc_Args.stMPOCheckSuppReturnInfo;
                }
                return true;
            }
            return false;
        }
        internal bool ULT_FW_Set_Source_Address_MPO(MPO_FLIP_PLANE_INFO[] mpoFlipPlaneInfo, uint numPlanes, ULT_SETVIDPNSOURCEADDRESS_FLAGS Flag, uint sourceId)
        {
            ULT_SET_SRC_ADD_MPO_ARG ult_Esc_Args = new ULT_SET_SRC_ADD_MPO_ARG();
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_SET_SRC_ADD_MPO;
            ult_Esc_Args.stDxgkMPOPlaneArgs = mpoFlipPlaneInfo;
            ult_Esc_Args.ulNumPlanes = numPlanes;
            ult_Esc_Args.ulFlags = Flag;
            ult_Esc_Args.dwSourceID = sourceId;

            if (!DoULTEscape(ULT_ESCAPE_CODE.ULT_SET_SRC_ADD_MPO, ult_Esc_Args))
                Log.Abort("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                if (ult_Esc_Args.dwRetErrorCode != 0)
                {
                    CommonExtensions.PrintULTErrorCodes(ult_Esc_Args.dwRetErrorCode);
                    return false;
                }
                return true;
            }
            return false;
        }

        protected List<UInt64> CreateYTileResource(uint width, uint height)
        {
            Log.Message(true, "Create resource for all the Y-Tiling Dump Files");
            List<UInt64> argGmmBlockList = new List<UInt64>();
            List<IntPtr> pUserVirtualAddressList = new List<IntPtr>();
            fileEntries = Directory.GetFiles(_dumpsDictionary["YTile"]);
            foreach (string file in fileEntries)
            {
                UInt64 pGmmBlock_temp = 0;
                IntPtr pUserVirtualAddress_temp = default(IntPtr);
                UInt64 SurfaceSize = 0;
                ULT_TILE_FORMATS ultTileFormat = ULT_TILE_FORMATS.ULT_TILE_FORMAT_Y;
                ULT_PIXELFORMAT ultSourcePixelFormat = ULT_PIXELFORMAT.SB_B8G8R8A8;
                byte[] array = File.ReadAllBytes(file);
                this.ULT_FW_Create_Resource(width, height, ultSourcePixelFormat, ultTileFormat,false, ref pGmmBlock_temp, ref pUserVirtualAddress_temp, ref SurfaceSize);
                argGmmBlockList.Add(pGmmBlock_temp);
                pUserVirtualAddressList.Add(pUserVirtualAddress_temp);
                int arrLength = (int)SurfaceSize;
                Marshal.Copy(array, 0, pUserVirtualAddress_temp, array.Length);
            }
            return argGmmBlockList;
        }
        protected List<UInt64> CreateNV12Resource(uint width, uint height)
        {
            Log.Message(true, "Create resource for all NV12 Dump Files");
            List<UInt64> argGmmBlockList = new List<UInt64>();
            List<IntPtr> pUserVirtualAddressList = new List<IntPtr>();
            fileEntries = Directory.GetFiles(_dumpsDictionary["NV12"]);
            foreach (string file in fileEntries)
            {
                string fileName = Path.GetFileNameWithoutExtension(file);
                UInt64 pGmmBlock_temp = 0;
                IntPtr pUserVirtualAddress_temp = default(IntPtr);
                string[] splitFileName = fileName.Split('_');
                uint width1 = Convert.ToUInt32(splitFileName[1]);
                uint height1 = Convert.ToUInt32(splitFileName[2]);
                UInt64 SurfaceSize = 0;
                ULT_TILE_FORMATS ultTileFormat = ULT_TILE_FORMATS.ULT_TILE_FORMAT_Y;
                ULT_PIXELFORMAT ultSourcePixelFormat = ULT_PIXELFORMAT.SB_NV12YUV420;
                byte[] array = File.ReadAllBytes(file);
                this.ULT_FW_Create_Resource(width1, height1, ultSourcePixelFormat, ultTileFormat, false, ref pGmmBlock_temp, ref pUserVirtualAddress_temp, ref SurfaceSize);
                argGmmBlockList.Add(pGmmBlock_temp);
                pUserVirtualAddressList.Add(pUserVirtualAddress_temp);
                int arrLength = (int)SurfaceSize;
                Marshal.Copy(array, 0, pUserVirtualAddress_temp, array.Length);
            }
            return argGmmBlockList;
        }
        protected List<UInt64> CreateMMIOResource(uint width, uint height)
        {
            Log.Message(true, "Create resource for all MMIO Dump Files");
            List<UInt64> argGmmBlockList = new List<UInt64>();
            List<IntPtr> pUserVirtualAddressList = new List<IntPtr>();
            fileEntries = Directory.GetFiles(_dumpsDictionary["YTile"]);
            foreach (string file in fileEntries)
            {
                UInt64 pGmmBlock_temp = 0;
                IntPtr pUserVirtualAddress_temp = default(IntPtr);
                UInt64 SurfaceSize = 0;
                ULT_TILE_FORMATS ultTileFormat = ULT_TILE_FORMATS.ULT_TILE_FORMAT_Y;
                ULT_PIXELFORMAT ultSourcePixelFormat = ULT_PIXELFORMAT.SB_B8G8R8A8;
                byte[] array = File.ReadAllBytes(file);
                this.ULT_FW_Create_Resource(width, height, ultSourcePixelFormat, ultTileFormat, false, ref pGmmBlock_temp, ref pUserVirtualAddress_temp, ref SurfaceSize);
                argGmmBlockList.Add(pGmmBlock_temp);
                pUserVirtualAddressList.Add(pUserVirtualAddress_temp);
                int arrLength = (int)SurfaceSize;
                Marshal.Copy(array, 0, pUserVirtualAddress_temp, array.Length);
            }
            return argGmmBlockList;
        }
        protected List<UInt64> CreateCharmResource(uint width, uint height)
        {
            Log.Message(true, "Create resource for all Charm Dump Files");
            List<UInt64> argGmmBlockList = new List<UInt64>();
            List<IntPtr> pUserVirtualAddressList = new List<IntPtr>();
            fileEntries = Directory.GetFiles(_dumpsDictionary["Charms"]);
            foreach (string file in fileEntries)
            {
                UInt64 pGmmBlock_temp = 0;
                IntPtr pUserVirtualAddress_temp = default(IntPtr);
                UInt64 SurfaceSize = 0;
                ULT_TILE_FORMATS ultTileFormat = ULT_TILE_FORMATS.ULT_TILE_FORMAT_Y;
                ULT_PIXELFORMAT ultSourcePixelFormat = ULT_PIXELFORMAT.SB_B8G8R8A8;
                byte[] array = File.ReadAllBytes(file);
                for (int i = 3; i < array.Length; i = i + 4)
                {
                    if (array[i] == 255)
                        array[i] = 0;
                }
                this.ULT_FW_Create_Resource(width, height, ultSourcePixelFormat, ultTileFormat, false, ref pGmmBlock_temp, ref pUserVirtualAddress_temp, ref SurfaceSize);
                argGmmBlockList.Add(pGmmBlock_temp);
                pUserVirtualAddressList.Add(pUserVirtualAddress_temp);
                int arrLength = (int)SurfaceSize;
                Marshal.Copy(array, 0, pUserVirtualAddress_temp, array.Length);
            }
            return argGmmBlockList;
        }
        protected List<UInt64> CreateRCResource(uint width, uint height)
        {
            Log.Message(true, "Create resource for all the RC Dump Files");
            List<UInt64> argGmmBlockList = new List<UInt64>();
            List<IntPtr> pUserVirtualAddressList = new List<IntPtr>();
            fileEntries = Directory.GetFiles(_dumpsDictionary["YTile"]);
            foreach (string file in fileEntries)
            {
                UInt64 pGmmBlock_temp = 0;
                IntPtr pUserVirtualAddress_temp = default(IntPtr);
                UInt64 SurfaceSize = 0;
                ULT_TILE_FORMATS ultTileFormat = ULT_TILE_FORMATS.ULT_TILE_FORMAT_Y;
                ULT_PIXELFORMAT ultSourcePixelFormat = ULT_PIXELFORMAT.SB_B8G8R8A8;
                byte[] array = File.ReadAllBytes(file);
                this.ULT_FW_Create_Resource(width, height, ultSourcePixelFormat, ultTileFormat,true, ref pGmmBlock_temp, ref pUserVirtualAddress_temp, ref SurfaceSize);
                argGmmBlockList.Add(pGmmBlock_temp);
                pUserVirtualAddressList.Add(pUserVirtualAddress_temp);
                int arrLength = (int)SurfaceSize;
                Marshal.Copy(array, 0, pUserVirtualAddress_temp, array.Length);
            }
            return argGmmBlockList;
        }
    }
}

