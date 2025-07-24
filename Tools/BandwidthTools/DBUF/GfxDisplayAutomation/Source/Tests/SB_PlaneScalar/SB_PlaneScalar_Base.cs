using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Text.RegularExpressions;
using System.Runtime.InteropServices;
using System.IO;
using System.Xml.Linq;
using System.Xml.Serialization;
using System.Xml;
namespace Intel.VPG.Display.Automation
{
    public class SB_PlaneScalar_Base:TestBase
    {
        protected XDocument ultParserDoc = null;
        protected DisplayMode displayMode;
        protected string[] fileEntries;
        protected const int MAX_PLANES = 13;
        protected const int MAX_PIPES = 3;
        protected const string MPORegisterEvent = "MPO";
        protected const string NV12RegisterEvent = "NV12";
        protected Dictionary<string, string> _dumpsDictionary = null;
        protected Dictionary<string, string> _paramsDictionary = null;
        private const uint OCR_NORMAL = 32512;
        protected DisplayMode actualMode;

        [DllImport("user32.dll")]
        internal static extern IntPtr LoadCursorFromFile(string lpFileName);

        [DllImport("user32.dll")]
        internal static extern bool SetSystemCursor(IntPtr hcur, uint id);

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {
            Log.Message(true, "Set config passed in command line");
            //if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
            //    Log.Success("Config applied successfully");
            //else
            //{
            //    base.ListEnumeratedDisplays();
            //    Log.Abort("Config not applied!");
            //}
            if (!Directory.Exists(base.ApplicationManager.ApplicationSettings.ULTDumpFiles))
            {
                Log.Abort("Coun't find {0} SB to run the test", base.ApplicationManager.ApplicationSettings.ULTDumpFiles);
            }
            // this.DisableCursor();
            this._dumpsDictionary = new Dictionary<string, string>()
            {
                 { "YTile", string.Concat(base.ApplicationManager.ApplicationSettings.ULTDumpFiles,"\\YtileDumps")},  
                 { "Charms", string.Concat(base.ApplicationManager.ApplicationSettings.ULTDumpFiles,"\\CharmsDumps")},
                 { "NV12", string.Concat(base.ApplicationManager.ApplicationSettings.ULTDumpFiles,"\\NV12Dumps")},
            };
            this._paramsDictionary = new Dictionary<string, string>()
            {
                 { "YTile", string.Concat(Directory.GetCurrentDirectory(), "\\Mapper\\YTilingPlaneParams.xml")},  
                 { "Charms", string.Concat(Directory.GetCurrentDirectory(), "\\Mapper\\CharmsPlaneParams.xml")},
                 { "NV12", string.Concat(Directory.GetCurrentDirectory(), "\\Mapper\\NV12PlaneParams.xml")}
            };
        }
        [Test(Type = TestType.PreCondition, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Get mode of Primary Display");
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays[0];
            displayMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
        }

        protected void DisableCursor()
        {
            IntPtr cursor = LoadCursorFromFile(Path.Combine(Directory.GetCurrentDirectory(), "blank.cur"));
            SetSystemCursor(cursor, OCR_NORMAL);
        }
        protected void EnableULT(bool status)
        {
            Log.Message(true, "Set ULT Status to {0}", status);
            ULT_ESC_ENABLE_ULT_ARG ult_Esc_Args = new ULT_ESC_ENABLE_ULT_ARG();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_ESC_ENABLE_ULT;
            ult_Esc_Args.bEnableULT = status;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_ESC_ENABLE_ULT, ult_Esc_Args);
            if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
                Log.Abort("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);

            if (ult_Esc_Args.dwRetErrorCode != 0)
            {
                CommonExtensions.PrintULTErrorCodes(ult_Esc_Args.dwRetErrorCode);
                status = false;
            }

        }

        protected void EnableFeature(bool status, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE featureType)
        {
            Log.Message(true, "Set Status of feature {0} to {1}", featureType, status);
            ULT_ESC_ENABLE_DISABLE_FEATURE_ARGS ult_Esc_Args = new ULT_ESC_ENABLE_DISABLE_FEATURE_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_ESC_ENABLE_DISABLE_FEATURE;
            ult_Esc_Args.bEnableFeature = status;
            ult_Esc_Args.eFeatureEnable = featureType;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;

            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_ESC_ENABLE_DISABLE_FEATURE, ult_Esc_Args);
            if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
                Log.Abort("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);

            if (ult_Esc_Args.dwRetErrorCode != 0)
            {
                CommonExtensions.PrintULTErrorCodes(ult_Esc_Args.dwRetErrorCode);
                status = false;
            }

        }


        protected bool ULT_FW_Create_Resource(uint x, uint y, ULT_PIXELFORMAT SRC_Pixel_Format, ULT_TILE_FORMATS Tile_Format, ref UInt64 pGmmBlock, ref IntPtr pUserVirtualAddress, ref UInt64 surfaceSize)
        {
            ULT_CREATE_RES_ARGS ult_Esc_Args = new ULT_CREATE_RES_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_CREATE_RESOURCE;
            ult_Esc_Args.ulBaseWidth = x;
            ult_Esc_Args.ulBaseHeight = y;
            ult_Esc_Args.Format = SRC_Pixel_Format;
            ult_Esc_Args.TileFormat = Tile_Format;
            ult_Esc_Args.AuxSurf = false;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;

            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_CREATE_RESOURCE, ult_Esc_Args);

            if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
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

            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_FREE_RESOURCE, ult_Esc_Args);

            if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
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
                    return true;
                }
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
            // ult_Esc_Args.ulDataSize = 8294400;//dataSize;
            ult_Esc_Args.Flags = Flag;

            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_SET_SRC_ADDRESS, ult_Esc_Args);

            if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
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
                    Log.Message("Set Source Address Successful");
                    return true;
                }
            }
            return false;
        }
        protected bool ULT_FW_Get_MPO_Caps(uint sourceID, ref ULT_MPO_CAPS argMpoCaps)
        {
            Log.Message(true, "Get MPO Caps");
            Log.Alert("MPO enabled on Primary display only, source Id passed as {0}", sourceID);
            ULT_ESC_MPO_CAPS_ARGS ult_Esc_Args = new ULT_ESC_MPO_CAPS_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_GET_MPO_CAPS;
            ult_Esc_Args.ulVidpnSourceID = sourceID;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;

            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_GET_MPO_CAPS, ult_Esc_Args);

            if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
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
                    return true;
                }
            }
            return false;
        }
        internal bool ULT_FW_MPO_Group_Caps(uint sourceID, uint groupIndex, ref ULT_MPO_GROUP_CAPS argMpoGroupCaps)
        {
            Log.Message(true, "Get MPO Group Caps for groupIndex = {0}", groupIndex);
            ULT_MPO_GROUP_CAPS_ARGS ult_Esc_Args = new ULT_MPO_GROUP_CAPS_ARGS();
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_MPO_GROUP_CAPS;
            ult_Esc_Args.ulVidpnSourceID = sourceID;
            ult_Esc_Args.uiGroupIndex = groupIndex;
            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_MPO_GROUP_CAPS, ult_Esc_Args);

            if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
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
                    return true;
                }
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

            //for (int i = 0; i < 8; i++)
            //{
            //    ult_Esc_Args.stCheckMPOPathInfo[1].stMPOPlaneInfo[0].stPlaneAttributes.DIRTYRECTS[i] = new M_RECT();
            //}

            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_CHECK_MPO, ult_Esc_Args);

            if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
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
                    return true;
                }
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

            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_SET_SRC_ADD_MPO, ult_Esc_Args);

            if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
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

        //internal bool ULT_FW_PlugDisplay(bool plug, DisplayType display, PORT port, string edidFile)
        //{
        //    ULT_ESC_GET_SET_DEVICE_CONNECTIVITY_ARGS escParams = new ULT_ESC_GET_SET_DEVICE_CONNECTIVITY_ARGS();
        //    escParams.stDeviceInfo = new ULT_DEVICE_INFO[5];
        //    escParams.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_DEVICE_CONNECTIVITY;
        //    escParams.ulNumDevices = 1;

        //    ULT_DEVICE_INFO ult_Device_Info = new ULT_DEVICE_INFO();
        //    ult_Device_Info.bAttach = plug;
        //    ult_Device_Info.OpType = 1;
        //    ult_Device_Info.ulPort = GetPortType(display, port);
        //    ult_Device_Info.bDisplayEdid = new byte[768];
        //    ult_Device_Info.bDPCDRxCaps = new byte[14];

        //    byte[] array = File.ReadAllBytes(edidFile);

        //    for (int i = 0; i < array.Length; i++)
        //    {
        //        ult_Device_Info.bDisplayEdid[i] = array[i];
        //    }

        //    if (display == DisplayType.DP)
        //    {
        //        byte[] dpcdData = File.ReadAllBytes(edidFile.Substring(0, edidFile.Length - 4) + "_DPCD.bin");
        //        for (int i = 0; i < 14; i++)
        //        {
        //            ult_Device_Info.bDPCDRxCaps[i] = dpcdData[i];
        //        }

        //    }
        //    escParams.stDeviceInfo[0] = ult_Device_Info;

        //    int sizeStruct = Marshal.SizeOf(ult_Device_Info);
        //    int sizeTotalStruct = Marshal.SizeOf(escParams);

        //    ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_DEVICE_CONNECTIVITY, escParams);

        //    if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
        //        Log.Fail("Failed to enable {0}", escParams.eULTEscapeCode);
        //    else
        //    {
        //        return true;
        //    }
        //    return false;
        //}
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
        //private PORT_TYPES GetPortType(DisplayType display, PORT port)
        //{
        //    PORT_TYPES portType = PORT_TYPES.NULL_PORT_TYPE;

        //    switch (display)
        //    {
        //        case DisplayType.EDP:
        //        case DisplayType.DP:
        //        case DisplayType.DP_2:
        //        case DisplayType.DP_3:
        //            switch (port)
        //            {
        //                case PORT.PORTA:
        //                    portType = PORT_TYPES.INTDPA_PORT;
        //                    break;
        //                case PORT.PORTB:
        //                    portType = PORT_TYPES.INTDPB_PORT;
        //                    break;
        //                case PORT.PORTC:
        //                    portType = PORT_TYPES.INTDPC_PORT;
        //                    break;
        //                case PORT.PORTD:
        //                    portType = PORT_TYPES.INTDPD_PORT;
        //                    break;
        //            }
        //            break;
        //        case DisplayType.HDMI:
        //        case DisplayType.HDMI_2:
        //        case DisplayType.HDMI_3:
        //            switch (port)
        //            {
        //                case PORT.PORTB:
        //                    portType = PORT_TYPES.INTHDMIB_PORT;
        //                    break;
        //                case PORT.PORTC:
        //                    portType = PORT_TYPES.INTHDMIC_PORT;
        //                    break;
        //                case PORT.PORTD:
        //                    portType = PORT_TYPES.INTHDMID_PORT;
        //                    break;
        //            }
        //            break;
        //        case DisplayType.MIPI:
        //            switch (port)
        //            {
        //                case PORT.PORTA:
        //                    portType = PORT_TYPES.INTMIPIA_PORT;
        //                    break;
        //                case PORT.PORTC:
        //                    portType = PORT_TYPES.INTMIPIC_PORT;
        //                    break;
        //            }
        //            break;
        //        case DisplayType.CRT:
        //            portType = PORT_TYPES.ANALOG_PORT;
        //            break;
        //    }

        //    return portType;
        //}
        protected void VerifyRotation(DisplayType argPrimaryDisplay, uint argAngle)
        {
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argPrimaryDisplay).First();
            DisplayMode currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            if (currentMode.Angle == actualMode.Angle)
                Log.Success("Display {0} in {1}", argPrimaryDisplay, currentMode.Angle);
            else
                Log.Fail("Angle mismatch, Display {0} in {1}, expected is {2}", argPrimaryDisplay, currentMode.Angle, actualMode.Angle);
        }
        protected void RotateDisplay(uint argAngle)
        {
            DisplayConfig currentOSPageConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.PrimaryDisplay).First();
            DisplayMode mode = new DisplayMode();
            mode = displayInfo.DisplayMode;
            mode.Angle = argAngle;
            // actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            actualMode.Angle = argAngle;
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, mode))
            {
                Log.Success("Display {0} rotated to {1}", currentOSPageConfig.PrimaryDisplay, mode.Angle);
            }
            else
                Log.Fail("Display {0} not rotated to {1}", currentOSPageConfig.PrimaryDisplay, mode.Angle);
        }
        protected List<UInt64> CreateYTileResource()
        {
            Log.Message(true, "Create resource for all the Y-Tiling Dump Files");
            List<UInt64> argGmmBlockList = new List<UInt64>();
            List<IntPtr> pUserVirtualAddressList = new List<IntPtr>();
            fileEntries = Directory.GetFiles(_dumpsDictionary["YTile"]);
            foreach (string file in fileEntries)
            {
                UInt64 pGmmBlock_temp = 0;
                IntPtr pUserVirtualAddress_temp = default(IntPtr);
                uint width = 1920;
                uint height = 1080;
                UInt64 SurfaceSize = 0;
                ULT_TILE_FORMATS ultTileFormat = ULT_TILE_FORMATS.ULT_TILE_FORMAT_Y;
                ULT_PIXELFORMAT ultSourcePixelFormat = ULT_PIXELFORMAT.SB_B8G8R8A8;
                byte[] array = File.ReadAllBytes(file);
                this.ULT_FW_Create_Resource(width, height, ultSourcePixelFormat, ultTileFormat, ref pGmmBlock_temp, ref pUserVirtualAddress_temp, ref SurfaceSize);
                argGmmBlockList.Add(pGmmBlock_temp);
                pUserVirtualAddressList.Add(pUserVirtualAddress_temp);
                int arrLength = (int)SurfaceSize;
                Marshal.Copy(array, 0, pUserVirtualAddress_temp, array.Length);
            }
            return argGmmBlockList;
        }
        protected List<UInt64> CreateNV12Resource()
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
                uint width = Convert.ToUInt32(splitFileName[1]);
                uint height = Convert.ToUInt32(splitFileName[2]);
                UInt64 SurfaceSize = 0;
                ULT_TILE_FORMATS ultTileFormat = ULT_TILE_FORMATS.ULT_TILE_FORMAT_Y;
                ULT_PIXELFORMAT ultSourcePixelFormat = ULT_PIXELFORMAT.SB_NV12YUV420;
                byte[] array = File.ReadAllBytes(file);
                this.ULT_FW_Create_Resource(width, height, ultSourcePixelFormat, ultTileFormat, ref pGmmBlock_temp, ref pUserVirtualAddress_temp, ref SurfaceSize);
                argGmmBlockList.Add(pGmmBlock_temp);
                pUserVirtualAddressList.Add(pUserVirtualAddress_temp);
                int arrLength = (int)SurfaceSize;
                Marshal.Copy(array, 0, pUserVirtualAddress_temp, array.Length);
            }
            return argGmmBlockList;
        }
        protected List<UInt64> CreateMMIOResource()
        {
            Log.Message(true, "Create resource for all MMIO Dump Files");
            List<UInt64> argGmmBlockList = new List<UInt64>();
            List<IntPtr> pUserVirtualAddressList = new List<IntPtr>();
            fileEntries = Directory.GetFiles(_dumpsDictionary["YTile"]);
            foreach (string file in fileEntries)
            {
                UInt64 pGmmBlock_temp = 0;
                IntPtr pUserVirtualAddress_temp = default(IntPtr);
                uint width = displayMode.HzRes;
                uint height = displayMode.VtRes;
                UInt64 SurfaceSize = 0;
                ULT_TILE_FORMATS ultTileFormat = ULT_TILE_FORMATS.ULT_TILE_FORMAT_Y;
                ULT_PIXELFORMAT ultSourcePixelFormat = ULT_PIXELFORMAT.SB_B8G8R8A8;
                byte[] array = File.ReadAllBytes(file);
                this.ULT_FW_Create_Resource(width, height, ultSourcePixelFormat, ultTileFormat, ref pGmmBlock_temp, ref pUserVirtualAddress_temp, ref SurfaceSize);
                argGmmBlockList.Add(pGmmBlock_temp);
                pUserVirtualAddressList.Add(pUserVirtualAddress_temp);
                int arrLength = (int)SurfaceSize;
                Marshal.Copy(array, 0, pUserVirtualAddress_temp, array.Length);
            }
            return argGmmBlockList;
        }
        protected List<UInt64> CreateCharmResource()
        {
            Log.Message(true, "Create resource for all Charm Dump Files");
            List<UInt64> argGmmBlockList = new List<UInt64>();
            List<IntPtr> pUserVirtualAddressList = new List<IntPtr>();
            fileEntries = Directory.GetFiles(_dumpsDictionary["Charms"]);
            foreach (string file in fileEntries)
            {
                UInt64 pGmmBlock_temp = 0;
                IntPtr pUserVirtualAddress_temp = default(IntPtr);
                uint width = displayMode.HzRes;
                uint height = displayMode.VtRes;
                UInt64 SurfaceSize = 0;
                ULT_TILE_FORMATS ultTileFormat = ULT_TILE_FORMATS.ULT_TILE_FORMAT_Y;
                ULT_PIXELFORMAT ultSourcePixelFormat = ULT_PIXELFORMAT.SB_B8G8R8A8;
                byte[] array = File.ReadAllBytes(file);
                for (int i = 3; i < array.Length; i = i + 4)
                {
                    if (array[i] == 255)
                        array[i] = 0;
                }
                this.ULT_FW_Create_Resource(width, height, ultSourcePixelFormat, ultTileFormat, ref pGmmBlock_temp, ref pUserVirtualAddress_temp, ref SurfaceSize);
                argGmmBlockList.Add(pGmmBlock_temp);
                pUserVirtualAddressList.Add(pUserVirtualAddress_temp);
                int arrLength = (int)SurfaceSize;
                Marshal.Copy(array, 0, pUserVirtualAddress_temp, array.Length);
            }
            return argGmmBlockList;
        }
    }
}
