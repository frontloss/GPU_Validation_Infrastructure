namespace AudioEndpointVerification
{
    using System;
    using System.Text;
    using System.Runtime.InteropServices;
    using System.Collections.Generic;

    internal class DriverEscape
    {
        public Dictionary<DriverEscapeType, Func<object, bool>> _commands = null;

        public DriverEscape()
        {
            this._commands = new Dictionary<DriverEscapeType, Func<object, bool>>();
            this._commands.Add(DriverEscapeType.Register, this.ParseRegisterRead);
            this._commands.Add(DriverEscapeType.PortName, this.ParsePortName);
        }

        private const int D3DKMT_ESCAPE_DRIVERPRIVATE = 0;

        #region RegisterReadStructures

        private const uint MMIO_REGISTER_FUNCTIONCODE = 0x5F66;
        private const int GETMMIOREG_SUBFUNC = 0; //Read register
        private const int SETMMIOREG_SUBFUNC = 1; //Write register


        [StructLayout(LayoutKind.Sequential)]
        private class EscapeData_RegisterOperation
        {
            public GFX_ESCAPE_HEADER header;
            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 12 /*Size of escape data structure*/)]
            public byte[] dataBytes;
        }

        [StructLayout(LayoutKind.Sequential)]
        private class MMIOArgs
        {
            public uint cmd;
            public uint offset;
            public uint value;
        }

        #endregion

        #region GetPortNameStructures

        private const uint Query_DisplayDetails_FuncCode = 0x5F64;
        private const uint Query_DisplayDetails_GetSubFuncCode = 0x0F;

        // Display details flag enum 
        public enum DISPLAY_DETAILS_FLAG
        {
            QUERY_DISPLAYUID = 1,
            QUERY_DISPLAYTYPE_INDEX
        }

        //  Display port type enumeration
        public enum PORT_TYPES
        {
            NULL_PORT_TYPE = -1,
            ANALOG_PORT = 0,
            DVOA_PORT,
            DVOB_PORT,
            DVOC_PORT,
            DVOD_PORT,
            LVDS_PORT,
            RESERVED_PORT,
            INTHDMIB_PORT,
            INTHDMIC_PORT,
            INTHDMID_PORT,
            INT_DVI_PORT, //NA
            INTDPA_PORT, //Embedded DP For ILK
            INTDPB_PORT,
            INTDPC_PORT,
            INTDPD_PORT,
            TPV_PORT,  //This is for all the TPV Ports..
            INTMIPIA_PORT,
            INTMIPIC_PORT,
            MAX_PORTS
        }

        // Enum added for distinguishing various display types
        public enum DISPLAY_TYPE
        {
            // DONOT change the order of type definitions
            // Add new types just before MAX_DISPLAY_TYPES & increment value of MAX_DISPLAY_TYPES
            NULL_DISPLAY_TYPE = 0,
            CRT_TYPE,
            TV_TYPE,
            DFP_TYPE,
            LFP_TYPE,
            MAX_DISPLAY_TYPES = LFP_TYPE
        }

        [StructLayout(LayoutKind.Sequential)]
        public class SB_QUERY_DISPLAY_DETAILS_ARGS
        {
            public uint Command;    //Always 

            public QUERY_DISPLAY_DETAILS_ARGS SbInfo;
        };

        [StructLayout(LayoutKind.Sequential)]//, Pack = 1 /*To allocate 1 byte for char/bool*/)]
        public class QUERY_DISPLAY_DETAILS_ARGS
        {
            //eflag = QUERY_DISPLAYUID -> Indicates that Display Type & Index will be sent & we need to return DisplayUID & bExternalEncoderDriven
            //eflag = QUERY_DISPLAYTYPE_INDEX -> Indicates that DisplayUID will be sent & we need to return  Display Type ,Index & bExternalEncoderDriven
            public DISPLAY_DETAILS_FLAG eflag;

            public uint ulDisplayUID;

            DISPLAY_TYPE eType;
            public char ucIndex;

            // Is display ID driven by external encoder?
            [MarshalAs(UnmanagedType.I1)]//, SizeConst = 1)]
            public bool bExternalEncoderDriven; //Includes both sDVO and NIVO Displays

            [MarshalAs(UnmanagedType.I1)]//, SizeConst = 1)]
            public bool bTPVDrivenEncoder;

            // Type of Port Used.
            public PORT_TYPES ePortType;

            // This interprets logical port mapping for physical connector.
            // This indicates mapping multiple encoders to the same port
            public char ucLogicalPortIndex;
        }

        [StructLayout(LayoutKind.Sequential)]
        public class EscapeData_QueryDisplayDetailsArgs
        {
            public GFX_ESCAPE_HEADER header;
            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 28)]
            public byte[] dataBytes;
        }

        #endregion

        #region Tool_ESC_GetPortNameStructures

        [StructLayout(LayoutKind.Sequential, Pack = 1 /*To allocate 1 byte for char/bool*/)]
        public class TOOL_ESC_QUERY_DISPLAY_DETAILS_ARGS
        {
            public uint ulDisplayUID;
            DISPLAY_TYPE eType;
            public char ucIndex;
            public PORT_TYPES ePortType;// Type of Port Used.
        }

        [StructLayout(LayoutKind.Sequential)]
        public class TOOL_ESC_EscapeData_QueryDisplayDetailsArgs
        {
            public GFX_ESCAPE_HEADER_T header;
            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 13)]
            public byte[] dataBytes;
        }

        #endregion

        #region Tool_ESC_RegisterReadStructures

        [StructLayout(LayoutKind.Sequential)]
        private class TOOL_ESC_EscapeData_RegisterOperation
        {
            public GFX_ESCAPE_HEADER_T header;
            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 8 /*Size of escape data structure*/)]
            public byte[] dataBytes;
        }

        [StructLayout(LayoutKind.Sequential)]
        private class TOOL_ESC_READ_MMIO_REGISTER_ARGS
        {
            public uint offset;
            public uint value;
        }
        #endregion

        [DllImport("Utilities.dll")]
        private static extern UInt32 readMMIOReg(UInt32 offset, ref UInt32 value);

        [DllImport("Utilities.dll")]
        private static extern UInt32 writeMMIOReg(UInt32 dwOffset, UInt32 dwValue);

        public bool SetMethod(object argMessage)
        {
            if (argMessage != null)
            {
                DriverEscapeParams escParams = argMessage as DriverEscapeParams;

                return _commands[escParams.driverEscapeType](escParams.driverEscapeData);
            }
            return false;
        }

        internal bool ParseRegisterRead<I>(I args)
        {
            DriverEscapeData<uint, uint> RegisterData = args as DriverEscapeData<uint, uint>;

            TOOL_ESC_EscapeData_RegisterOperation Tool_Esc_EscapeData = new TOOL_ESC_EscapeData_RegisterOperation();
            TOOL_ESC_READ_MMIO_REGISTER_ARGS Tool_Esc_mmioArgs = new TOOL_ESC_READ_MMIO_REGISTER_ARGS();
            Tool_Esc_mmioArgs.offset = RegisterData.input;
            Tool_Esc_mmioArgs.value = 0;

            if (PerformDriverEscape(Tool_Esc_mmioArgs, Tool_Esc_EscapeData, TOOLS_ESCAPE_CODE.TOOL_ESC_READ_MMIO_REGISTER))
            {
                RegisterData.output = Tool_Esc_mmioArgs.value;
                return true;
            }
            else
            {
                EscapeData_RegisterOperation EscapeData = new EscapeData_RegisterOperation();
                MMIOArgs mmioArgs = new MMIOArgs();
                mmioArgs.offset = RegisterData.input;

                mmioArgs.cmd = (MMIO_REGISTER_FUNCTIONCODE << 16) | (GETMMIOREG_SUBFUNC);
                mmioArgs.value = 0;

                Object temp = mmioArgs;
                APIExtensions.GetDataFromBytes(APIExtensions.GetMagicDataBytes(mmioArgs), ref temp);

                if (PerformDriverEscape(mmioArgs, EscapeData, GFX_ESCAPE_CODE.GFX_ESCAPE_SOFTBIOS_CONTROL))
                {
                    RegisterData.output = mmioArgs.value;
                    return true;
                }
            }
            return false;
        }

        internal static bool PerformDriverEscape(Object escDataStruct, Object escapeData, GFX_ESCAPE_CODE escapeCode)
        {
            IntPtr hdc = IntPtr.Zero;
            D3DKMT_OPENADAPTERFROMHDC openAdapterData = new D3DKMT_OPENADAPTERFROMHDC();
            bool bCreateDC = true;
            bool bOpenAdapter = true;
            try
            {
                DISPLAY_DEVICE deviceName = new DISPLAY_DEVICE();
                deviceName.cb = Marshal.SizeOf(deviceName);
                uint devID = 0;
                uint sizeofEscDataStruct = (uint)Marshal.SizeOf(escDataStruct);

                hdc = Interop.CreateDC("\\\\.\\Display1", null, null, IntPtr.Zero);
                if (hdc == IntPtr.Zero)
                {
                    
                    // Usually DISPLAY1 is used. While is to comprehend multi-mon where some displays might be driven from DISPLAY2
                    while (Interop.EnumDisplayDevices(null, devID++, ref deviceName, 0))
                    {
                        hdc = Interop.CreateDC(deviceName.DeviceName, null, null, IntPtr.Zero);
                        // hdc = Interop.GetDC(IntPtr.Zero);

                        if (hdc == IntPtr.Zero)
                        {
                            
                        }
                        else
                            break; // Currently only DISPLAY1 is used. User can include logic for other display adapters also.
                    }
                }

                if (hdc == IntPtr.Zero)
                {
                    bCreateDC = false;
                    
                    return false;
                }
                openAdapterData.hDc = hdc;
                if (Interop.D3DKMTOpenAdapterFromHdc(ref openAdapterData) != 0)
                {
                    bOpenAdapter = false;
                    
                    return false;
                }

                D3DKMT_ESCAPE kmtEscape = new D3DKMT_ESCAPE();
                kmtEscape.hAdapter = openAdapterData.hAdapter;
                kmtEscape.Type = D3DKMT_ESCAPE_DRIVERPRIVATE;

                GFX_ESCAPE_HEADER escHeader = new GFX_ESCAPE_HEADER();
                uint sizeofEscHeader = (uint)Marshal.SizeOf(escHeader);
                escHeader.Size = sizeofEscDataStruct;
                escHeader.CheckSum = 0; // Calculate the checksum, if not assign it to zero.
                escHeader.EscapeCode = (uint)escapeCode;

                Object oEscHeader = escHeader;
                byte[] bEscapeData = APIExtensions.GetDataBytes(escapeData);
                byte[] bEscHeader = APIExtensions.GetDataBytes(oEscHeader);
                byte[] bEscDataStruct = APIExtensions.GetDataBytes(escDataStruct);

                // Escape data refers to Header + Escape data structure
                // 1. Populate escape data (byte format)
                for (uint index = 0; index < sizeofEscHeader; index++)
                {
                    bEscapeData[index] = bEscHeader[index];
                }

                for (uint index = 0; index < sizeofEscDataStruct; index++)
                {
                    bEscapeData[index + sizeofEscHeader] = bEscDataStruct[index];
                }

                // 2. Convert escape data (structure format)
                APIExtensions.GetDataFromBytes(bEscapeData, ref escapeData);
                uint sizeofEscapeData = (uint)Marshal.SizeOf(escHeader) + sizeofEscDataStruct;
                IntPtr escapeDataPtr = Marshal.AllocHGlobal((int)sizeofEscapeData);

                // 3. Convert escape data (to IntPtr)
                Marshal.StructureToPtr(escapeData, escapeDataPtr, true);
                kmtEscape.pPrivateDriverData = escapeDataPtr;
                kmtEscape.PrivateDriverDataSize = sizeofEscapeData;

                // 4. Perform escape call
                uint retval = (uint)Interop.D3DKMTEscape(ref kmtEscape);
                if (retval != 0)
                {
                    
                    return false;
                }

                // 5. Convert escape data (structure format)
                Marshal.PtrToStructure(escapeDataPtr, escapeData);

                // 6. Get escape data (byte format)
                bEscapeData = APIExtensions.GetDataBytes(escapeData);

                // 7. Extract escape data structure (byte format) from escape data
                for (uint index = 0; index < sizeofEscDataStruct; index++)
                {
                    bEscDataStruct[index] = bEscapeData[index + sizeofEscHeader];
                }

                // 8. Get meaningful data from the escape data structure
                APIExtensions.GetDataFromBytes(bEscDataStruct, ref escDataStruct);

                //    break; // Currently only DISPLAY1 is used. User can include logic for other display adapters also.
                //}
                return true;
            }
            catch (Exception e)
            {
               
                return false;
            }
            finally
            {
                if (bCreateDC == true)
                {
                    //Release handles
                    if (!Interop.DeleteDC(hdc))
                    { }
                }
                if (bOpenAdapter == true)
                {
                    D3DKMT_CLOSEADAPTER closeAdapter = new D3DKMT_CLOSEADAPTER();
                    closeAdapter.hAdapter = openAdapterData.hAdapter;

                    if (Interop.D3DKMTCloseAdapter(ref closeAdapter) != 0)
                    { }
                }
            }
        }

        internal static bool PerformDriverEscape(Object escDataStruct, Object escapeData, TOOLS_ESCAPE_CODE escapeCode)
        {
            IntPtr hdc = IntPtr.Zero;
            D3DKMT_OPENADAPTERFROMHDC openAdapterData = new D3DKMT_OPENADAPTERFROMHDC();
            bool bCreateDC = true;
            bool bOpenAdapter = true;
            try
            {
                DISPLAY_DEVICE deviceName = new DISPLAY_DEVICE();
                deviceName.cb = Marshal.SizeOf(deviceName);
                uint devID = 0;
                uint sizeofEscDataStruct = (uint)Marshal.SizeOf(escDataStruct);

                hdc = Interop.CreateDC("\\\\.\\Display1", null, null, IntPtr.Zero);
                if (hdc == IntPtr.Zero)
                {
                    while (Interop.EnumDisplayDevices(null, devID++, ref deviceName, 0))
                    {
                        hdc = Interop.CreateDC(deviceName.DeviceName, null, null, IntPtr.Zero);
                        if (hdc == IntPtr.Zero)
                        {
                            
                        }
                        else
                            break;
                    }
                }

                if (hdc == IntPtr.Zero)
                {
                    bCreateDC = false;
                    return false;
                }

                openAdapterData.hDc = hdc;
                if (Interop.D3DKMTOpenAdapterFromHdc(ref openAdapterData) != 0)
                {
                    bOpenAdapter = false;
                    return false;
                }

                D3DKMT_ESCAPE kmtEscape = new D3DKMT_ESCAPE();
                kmtEscape.hAdapter = openAdapterData.hAdapter;
                kmtEscape.Type = D3DKMT_ESCAPE_DRIVERPRIVATE;

                GFX_ESCAPE_HEADER_T escHeader = new GFX_ESCAPE_HEADER_T();
                uint sizeofEscHeader = (uint)Marshal.SizeOf(escHeader);
                escHeader.ulReserved = sizeofEscDataStruct;
                escHeader.ulMinorInterfaceVersion = 1; // Calculate the checksum, if not assign it to zero.
                escHeader.uiMajorEscapeCode = 20;
                escHeader.uiMinorEscapeCode = (uint)escapeCode;

                Object oEscHeader = escHeader;
                byte[] bEscapeData = APIExtensions.GetDataBytes(escapeData);
                byte[] bEscHeader = APIExtensions.GetDataBytes(oEscHeader);
                byte[] bEscDataStruct = APIExtensions.GetDataBytes(escDataStruct);

                // Escape data refers to Header + Escape data structure
                // 1. Populate escape data (byte format)
                for (uint index = 0; index < sizeofEscHeader; index++)
                {
                    bEscapeData[index] = bEscHeader[index];
                }

                for (uint index = 0; index < sizeofEscDataStruct; index++)
                {
                    bEscapeData[index + sizeofEscHeader] = bEscDataStruct[index];
                }

                // 2. Convert escape data (structure format)
                APIExtensions.GetDataFromBytes(bEscapeData, ref escapeData);
                uint sizeofEscapeData = (uint)Marshal.SizeOf(escHeader) + sizeofEscDataStruct;
                IntPtr escapeDataPtr = Marshal.AllocHGlobal((int)sizeofEscapeData);

                // 3. Convert escape data (to IntPtr)
                Marshal.StructureToPtr(escapeData, escapeDataPtr, true);
                kmtEscape.pPrivateDriverData = escapeDataPtr;
                kmtEscape.PrivateDriverDataSize = sizeofEscapeData;

                // 4. Perform escape call
                uint retval = (uint)Interop.D3DKMTEscape(ref kmtEscape);
                if (retval != 0)
                {
                    return false;
                }

                // 5. Convert escape data (structure format)
                Marshal.PtrToStructure(escapeDataPtr, escapeData);

                // 6. Get escape data (byte format)
                bEscapeData = APIExtensions.GetDataBytes(escapeData);

                // 7. Extract escape data structure (byte format) from escape data
                for (uint index = 0; index < sizeofEscDataStruct; index++)
                {
                    bEscDataStruct[index] = bEscapeData[index + sizeofEscHeader];
                }

                // 8. Get meaningful data from the escape data structure
                APIExtensions.GetDataFromBytes(bEscDataStruct, ref escDataStruct);

                //    break; // Currently only DISPLAY1 is used. User can include logic for other display adapters also.
                //}
                return true;
            }
            catch (Exception e)
            {
                return false;
            }
            finally
            {
                if (bCreateDC == true)
                {
                    //Release handles
                    if (!Interop.DeleteDC(hdc))
                    {
                    }
                }
                if (bOpenAdapter == true)
                {
                    D3DKMT_CLOSEADAPTER closeAdapter = new D3DKMT_CLOSEADAPTER();
                    closeAdapter.hAdapter = openAdapterData.hAdapter;

                    if (Interop.D3DKMTCloseAdapter(ref closeAdapter) != 0)
                    {
                    }
                }
            }
        }

        private bool GetDriverPortInfo(uint winId, ref PORT_TYPES driverPort)
        {
            uint tempWinID = winId;
            TOOL_ESC_EscapeData_QueryDisplayDetailsArgs Tool_Esc_escapeQueryDisplayData = new TOOL_ESC_EscapeData_QueryDisplayDetailsArgs();
            TOOL_ESC_QUERY_DISPLAY_DETAILS_ARGS Tool_Esc_SbInfo = new TOOL_ESC_QUERY_DISPLAY_DETAILS_ARGS();

            //workaround for Threshold OS issue for Windows ID.
            tempWinID = tempWinID & 0x0FFFFFFF;

            Tool_Esc_SbInfo.ulDisplayUID = tempWinID;
            if (PerformDriverEscape(Tool_Esc_SbInfo, Tool_Esc_escapeQueryDisplayData, TOOLS_ESCAPE_CODE.TOOL_ESC_QUERY_DISPLAY_DETAILS))
            {
                driverPort = Tool_Esc_SbInfo.ePortType;
                return true;
            }
            else
            {
                EscapeData_QueryDisplayDetailsArgs escapeQueryDisplayData = new EscapeData_QueryDisplayDetailsArgs();
                SB_QUERY_DISPLAY_DETAILS_ARGS SbQueryDisplayDetailsArgs = new SB_QUERY_DISPLAY_DETAILS_ARGS();
                SbQueryDisplayDetailsArgs.SbInfo = new QUERY_DISPLAY_DETAILS_ARGS();

                SbQueryDisplayDetailsArgs.Command = (Query_DisplayDetails_FuncCode << 16) | (Query_DisplayDetails_GetSubFuncCode);

                SbQueryDisplayDetailsArgs.SbInfo.ulDisplayUID = tempWinID;
                SbQueryDisplayDetailsArgs.SbInfo.eflag = DISPLAY_DETAILS_FLAG.QUERY_DISPLAYTYPE_INDEX;

                Object temp = SbQueryDisplayDetailsArgs;
                APIExtensions.GetDataFromBytes(APIExtensions.GetMagicDataBytes(SbQueryDisplayDetailsArgs), ref temp);

                if (PerformDriverEscape(SbQueryDisplayDetailsArgs, escapeQueryDisplayData, GFX_ESCAPE_CODE.GFX_ESCAPE_SOFTBIOS_CONTROL))
                {
                    driverPort = SbQueryDisplayDetailsArgs.SbInfo.ePortType;
                    return true;
                }
            }
            return false;
        }

        internal bool ParsePortName<I>(I args)
        {
            DriverEscapeData<uint, PORT> PortData = args as DriverEscapeData<uint, PORT>;
            PORT_TYPES driverPort = PORT_TYPES.NULL_PORT_TYPE;
            PORT tempPort = PORT.NONE;
            if (GetDriverPortInfo(PortData.input, ref driverPort) == true)
            {
                GetActualPort(driverPort, ref tempPort);
                PortData.output = tempPort;
                return true;
            }
            return false;
        }


        internal bool ParseConnectorType<I>(I args)
        {
            DriverEscapeData<uint, DisplayType> PortData = args as DriverEscapeData<uint, DisplayType>;
            PORT_TYPES driverPort = PORT_TYPES.NULL_PORT_TYPE;
            if (GetDriverPortInfo(PortData.input, ref driverPort) == true)
            {
                PortData.output = GetConnectorType(driverPort);
                return true;
            }
            return false;
        }
        internal DisplayType GetConnectorType(PORT_TYPES displayPort)
        {
            switch (displayPort)
            {
                case PORT_TYPES.INTDPB_PORT:
                case PORT_TYPES.INTDPC_PORT:
                case PORT_TYPES.INTDPD_PORT:
                    return DisplayType.DP;
                case PORT_TYPES.INTHDMIB_PORT:
                case PORT_TYPES.INTHDMIC_PORT:
                case PORT_TYPES.INTHDMID_PORT:
                    return DisplayType.HDMI;
                case PORT_TYPES.INTDPA_PORT:
                    return DisplayType.EDP;
                case PORT_TYPES.ANALOG_PORT:
                    return DisplayType.CRT;
                case PORT_TYPES.INTMIPIA_PORT:
                case PORT_TYPES.INTMIPIC_PORT:
                    return DisplayType.MIPI;
                default:
                    return DisplayType.None;
            }
        }

        private void GetActualPort(PORT_TYPES displayPort, ref PORT actualPort)
        {
            switch (displayPort)
            {
                case PORT_TYPES.INTDPA_PORT:
                case PORT_TYPES.DVOA_PORT:
                case PORT_TYPES.INTMIPIA_PORT:
                case PORT_TYPES.LVDS_PORT:
                    actualPort = PORT.PORTA;
                    break;
                case PORT_TYPES.INTDPB_PORT:
                case PORT_TYPES.DVOB_PORT:
                case PORT_TYPES.INTHDMIB_PORT:
                    actualPort = PORT.PORTB;
                    break;
                case PORT_TYPES.INTDPC_PORT:
                case PORT_TYPES.DVOC_PORT:
                case PORT_TYPES.INTHDMIC_PORT:
                case PORT_TYPES.INTMIPIC_PORT:
                    actualPort = PORT.PORTC;
                    break;
                case PORT_TYPES.INTDPD_PORT:
                case PORT_TYPES.DVOD_PORT:
                case PORT_TYPES.INTHDMID_PORT:
                    actualPort = PORT.PORTD;
                    break;
                case PORT_TYPES.ANALOG_PORT:
                    actualPort = PORT.PORTE;
                    break;
                case PORT_TYPES.TPV_PORT:
                    actualPort = PORT.TVPORT;
                    break;
                default:
                    actualPort = PORT.NONE;
                    break;
            }

        }
    }
}
