namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Runtime.InteropServices;

    class DriverEscape
    {
        private Dictionary<DriverEscapeType, Func<object, int>> _commands = null;
        private const int D3DKMT_ESCAPE_DRIVERPRIVATE = 0;
        private const uint MMIO_REGISTER_FUNCTIONCODE = 0x5F66;
        private const int GETMMIOREG_SUBFUNC = 0; //Read register
        private const int SETMMIOREG_SUBFUNC = 1; //Write register
        private const uint Query_DisplayDetails_FuncCode = 0x5F64;
        private const uint Query_DisplayDetails_GetSubFuncCode = 0x0F;

        internal DriverEscape()
        {
            this._commands = new Dictionary<DriverEscapeType, Func<object, int>>();
            this._commands.Add(DriverEscapeType.Register, this.ParseRegisterRead);
            this._commands.Add(DriverEscapeType.PortName, this.ParsePortName);
        }

        internal int ParsePortName<I>(I args)
        {
            DriverEscapeData<uint, PORT> PortData = args as DriverEscapeData<uint, PORT>;
            PORT_TYPES driverPort = PORT_TYPES.NULL_PORT_TYPE;
            PORT tempPort = PORT.NONE;
            if (GetDriverPortInfo(PortData.input, ref driverPort) == true)
            {
                GetActualPort(driverPort, ref tempPort);
                PortData.output = tempPort;
                return (int)driverPort;
            }
            return -1;
        }
        internal bool ParseConnectorType<I>(I args)
        {
            DriverEscapeData<uint, DisplayType> PortData = args as DriverEscapeData<uint, DisplayType>;
            PORT_TYPES driverPort = PORT_TYPES.NULL_PORT_TYPE;
            //Console.WriteLine("Fetching PortName by WindowsId: {0}", PortData.input);
            if (GetDriverPortInfo(PortData.input, ref driverPort) == true)
            {
                PortData.output = GetConnectorType(driverPort);
                return true;
            }
            return false;
        }

        private bool PerformDriverEscape(Object escDataStruct, Object escapeData, GFX_ESCAPE_CODE escapeCode)
        {
            IntPtr hdc = IntPtr.Zero;
            D3DKMT_OPENADAPTERFROMHDC openAdapterData = new D3DKMT_OPENADAPTERFROMHDC();
            try
            {
                DISPLAY_DEVICE deviceName = new DISPLAY_DEVICE();
                deviceName.cb = Marshal.SizeOf(deviceName);
                uint devId = 0;
                uint sizeofEscDataStruct = (uint)Marshal.SizeOf(escDataStruct);

                // Usually DISPLAY1 is used. While is to comprehend multi-mon where some displays might be driven from DISPLAY2
                while (Interop.EnumDisplayDevices(null, devId++, ref deviceName, 0))
                {
                    hdc = DriverInterop.CreateDC(null, deviceName.DeviceName, null, IntPtr.Zero);
                    if (hdc == IntPtr.Zero)
                    {
                        Console.WriteLine("ERROR: Unable to create device context with CreateDC:{0}", DriverInterop.GetLastError());
                        return false;
                    }

                    openAdapterData.hDc = hdc;
                    if (DriverInterop.D3DKMTOpenAdapterFromHdc(ref openAdapterData) != 0)
                    {
                        Console.WriteLine("ERROR: Unable to get adapter handle with OpenAdapterFromHDC:{0}", DriverInterop.GetLastError());
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
                    byte[] bEscapeData = GetDataBytes(escapeData);
                    byte[] bEscHeader = GetDataBytes(oEscHeader);
                    byte[] bEscDataStruct = GetDataBytes(escDataStruct);

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
                    GetDataFromBytes(bEscapeData, ref escapeData);
                    uint sizeofEscapeData = (uint)Marshal.SizeOf(escHeader) + sizeofEscDataStruct;
                    IntPtr escapeDataPtr = Marshal.AllocHGlobal((int)sizeofEscapeData);

                    // 3. Convert escape data (to IntPtr)
                    Marshal.StructureToPtr(escapeData, escapeDataPtr, true);
                    kmtEscape.pPrivateDriverData = escapeDataPtr;
                    kmtEscape.PrivateDriverDataSize = sizeofEscapeData;

                    // 4. Perform escape call
                    uint retval = (uint)DriverInterop.D3DKMTEscape(ref kmtEscape);
                    if (retval != 0)
                    {
                        Console.WriteLine("Escape call returned {0}", retval);
                        return false;
                    }

                    // 5. Convert escape data (structure format)
                    Marshal.PtrToStructure(escapeDataPtr, escapeData);

                    // 6. Get escape data (byte format)
                    bEscapeData = GetDataBytes(escapeData);

                    // 7. Extract escape data structure (byte format) from escape data
                    for (uint index = 0; index < sizeofEscDataStruct; index++)
                    {
                        bEscDataStruct[index] = bEscapeData[index + sizeofEscHeader];
                    }

                    // 8. Get meaningful data from the escape data structure
                    GetDataFromBytes(bEscDataStruct, ref escDataStruct);

                    break; // Currently only DISPLAY1 is used. User can include logic for other display adapters also.
                }
                return true;
            }
            catch (Exception e)
            {
                Console.WriteLine("{Exception Caught: {1}", e.Message.ToString());
                return false;
            }
            finally
            {
                //Release handles
                if (!DriverInterop.DeleteDC(hdc))
                    Console.WriteLine("ERROR: Unable to clear device context: {0}", DriverInterop.GetLastError());
                D3DKMT_CLOSEADAPTER closeAdapter = new D3DKMT_CLOSEADAPTER();
                closeAdapter.hAdapter = openAdapterData.hAdapter;

                if (DriverInterop.D3DKMTCloseAdapter(ref closeAdapter) != 0)
                    Console.WriteLine("ERROR: Unable to close adapter handle: {0}", DriverInterop.GetLastError());
            }
        }

        /// <summary>
        /// This escape call is used for 15_Main and 15_36 or gen8 branches.
        /// </summary>
        /// <param name="escDataStruct"></param>
        /// <param name="escapeData"></param>
        /// <param name="escapeCode"></param>
        /// <returns></returns>
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

                // Usually DISPLAY1 is used. While is to comprehend multi-mon where some displays might be driven from DISPLAY2
                while (Interop.EnumDisplayDevices(null, devID++, ref deviceName, 0))
                {
                    hdc = DriverInterop.CreateDC(deviceName.DeviceName, null, null, IntPtr.Zero);
                    // hdc = Interop.GetDC(IntPtr.Zero);

                    if (hdc == IntPtr.Zero)
                    {
                        Console.WriteLine("Unable to create device context with CreateDC with {0} -> {1}", deviceName.DeviceName, DriverInterop.GetLastError());
                    }
                    else
                        break; // Currently only DISPLAY1 is used. User can include logic for other display adapters also.
                }

                if (hdc == IntPtr.Zero)
                {
                    bCreateDC = false;
                    Console.WriteLine("ERROR: Unable to create device context with CreateDC:{0}", DriverInterop.GetLastError());
                    return false;
                }

                openAdapterData.hDc = hdc;
                if (DriverInterop.D3DKMTOpenAdapterFromHdc(ref openAdapterData) != 0)
                {
                    bOpenAdapter = false;
                    Console.WriteLine("ERROR: Unable to get adapter handle with OpenAdapterFromHDC:{0}", DriverInterop.GetLastError());
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
                byte[] bEscapeData = GetDataBytes(escapeData);
                byte[] bEscHeader = GetDataBytes(oEscHeader);
                byte[] bEscDataStruct = GetDataBytes(escDataStruct);

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
                GetDataFromBytes(bEscapeData, ref escapeData);
                uint sizeofEscapeData = (uint)Marshal.SizeOf(escHeader) + sizeofEscDataStruct;
                IntPtr escapeDataPtr = Marshal.AllocHGlobal((int)sizeofEscapeData);

                // 3. Convert escape data (to IntPtr)
                Marshal.StructureToPtr(escapeData, escapeDataPtr, true);
                kmtEscape.pPrivateDriverData = escapeDataPtr;
                kmtEscape.PrivateDriverDataSize = sizeofEscapeData;

                // 4. Perform escape call
                uint retval = (uint)DriverInterop.D3DKMTEscape(ref kmtEscape);
                if (retval != 0)
                {
                    Console.WriteLine("Error: Escape call returned {0}", retval);
                    return false;
                }

                // 5. Convert escape data (structure format)
                Marshal.PtrToStructure(escapeDataPtr, escapeData);

                // 6. Get escape data (byte format)
                bEscapeData = GetDataBytes(escapeData);

                // 7. Extract escape data structure (byte format) from escape data
                for (uint index = 0; index < sizeofEscDataStruct; index++)
                {
                    bEscDataStruct[index] = bEscapeData[index + sizeofEscHeader];
                }

                // 8. Get meaningful data from the escape data structure
                GetDataFromBytes(bEscDataStruct, ref escDataStruct);

                //    break; // Currently only DISPLAY1 is used. User can include logic for other display adapters also.
                //}
                return true;
            }
            catch (Exception e)
            {
                Console.WriteLine("{Exception Caught: {1}", e.Message.ToString());
                return false;
            }
            finally
            {
                if (bCreateDC == true)
                {
                    //Release handles
                    if (!DriverInterop.DeleteDC(hdc))
                        Console.WriteLine("ERROR: Unable to clear device context: {0}", DriverInterop.GetLastError());
                }
                if (bOpenAdapter == true)
                {
                    D3DKMT_CLOSEADAPTER closeAdapter = new D3DKMT_CLOSEADAPTER();
                    closeAdapter.hAdapter = openAdapterData.hAdapter;

                    if (DriverInterop.D3DKMTCloseAdapter(ref closeAdapter) != 0)
                        Console.WriteLine("ERROR: Unable to close adapter handle: {0}", DriverInterop.GetLastError());
                }
            }
        }
        private int ParseRegisterRead<I>(I args)
        {
            DriverEscapeData<uint, uint> RegisterData = args as DriverEscapeData<uint, uint>;

            EscapeData_RegisterOperation EscapeData = new EscapeData_RegisterOperation();
            MMIOArgs mmioArgs = new MMIOArgs();
            mmioArgs.offset = RegisterData.input;

            mmioArgs.cmd = (MMIO_REGISTER_FUNCTIONCODE << 16) | (GETMMIOREG_SUBFUNC);
            mmioArgs.value = 0;

            Object temp = mmioArgs;
            GetDataFromBytes(GetMagicDataBytes(mmioArgs), ref temp);

            if (PerformDriverEscape(mmioArgs, EscapeData, GFX_ESCAPE_CODE.GFX_ESCAPE_SOFTBIOS_CONTROL))
            {
                RegisterData.output = mmioArgs.value;
                return 1;
            }
            return 0;
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

                SbQueryDisplayDetailsArgs.SbInfo.ulDisplayUID = winId;
                SbQueryDisplayDetailsArgs.SbInfo.eflag = DISPLAY_DETAILS_FLAG.QUERY_DISPLAYTYPE_INDEX;

                Object temp = SbQueryDisplayDetailsArgs;
                GetDataFromBytes(GetMagicDataBytes(SbQueryDisplayDetailsArgs), ref temp);

                if (PerformDriverEscape(SbQueryDisplayDetailsArgs, escapeQueryDisplayData, GFX_ESCAPE_CODE.GFX_ESCAPE_SOFTBIOS_CONTROL))
                {
                    driverPort = SbQueryDisplayDetailsArgs.SbInfo.ePortType;
                    return true;
                }
            }
            return false;
        }
        private DisplayType GetConnectorType(PORT_TYPES displayPort)
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
        private static byte[] GetDataBytes(object InputData)
        {
            uint dataSize = (uint)Marshal.SizeOf(InputData);

            IntPtr ptr = Marshal.AllocHGlobal((int)dataSize);
            byte[] byteData = new byte[dataSize];
            Marshal.StructureToPtr(InputData, ptr, true);
            Marshal.Copy(ptr, byteData, 0, (int)dataSize);
            return byteData;
        }
        private static void GetDataFromBytes(byte[] InputData, ref object OutputData)
        {
            int OutputDataSize = Marshal.SizeOf(OutputData);
            IntPtr ptr = Marshal.AllocHGlobal(OutputDataSize);

            Marshal.Copy(InputData, 0, ptr, OutputDataSize);

            Marshal.PtrToStructure(ptr, OutputData);
            Marshal.FreeHGlobal(ptr);
        }
        private byte[] GetMagicDataBytes(object InputData)
        {
            byte[] byteData = GetDataBytes(InputData);
            byte magicNumber = 0xAA;

            for (int count = 0; count < byteData.Length; count++)
            {
                byteData[count] ^= magicNumber;
            }

            return byteData;
        }
    }
}
