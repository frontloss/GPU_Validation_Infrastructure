namespace Intel.VPG.Display.FlickerTestSuite.MPO
{
    using System;
    using System.Text;
    using System.Runtime.InteropServices;
    using System.Collections.Generic;

    public class ULT_Framework
    {
        public static uint ESCDATA_SIZE = 0x3cdc;

        public enum GFX_ESCAPE_CODE_T
        {
            // IMPORTANT:- When adding new escape code, add it at the end of the list, 
            // just before GFX_MAX_ESCAPE_CODES. the reason is that external test apps 
            // depend on the current order.

            // DO NOT ADD NEGATIVE ENUMERATORS
            GFX_ESCAPE_CODE_DEBUG_CONTROL = 0, // DO NOT CHANGE 
            GFX_ESCAPE_CUICOM_CONTROL,
            GFX_ESCAPE_GMM_CONTROL,
            GFX_ESCAPE_CAMARILLO_CONTROL,
            GFX_ESCAPE_ROTATION_CONTROL,
            GFX_ESCAPE_PAVP_CONTROL,
            GFX_ESCAPE_UMD_GENERAL_CONTROL,
            GFX_ESCAPE_RESOURCE_CONTROL,
            GFX_ESCAPE_SOFTBIOS_CONTROL,
            GFX_ESCAPE_ACPI_CONTROL,
            GFX_ESCAPE_CODE_KM_DAF,
            GFX_ESCAPE_CODE_PERF_CONTROL,
            GFX_ESCAPE_IGPA_INSTRUMENTATION_CONTROL,
            GFX_ESCAPE_CODE_OCA_TEST_CONTROL,
            GFX_ESCAPE_AUTHCHANNEL,
            GFX_ESCAPE_SHARED_RESOURCE,
            GFX_ESCAPE_PWRCONS_CONTROL,
            GFX_ESCAPE_KMD,
            GFX_ESCAPE_DDE,
            GFX_ESCAPE_IFFS,
            GFX_ESCAPE_TOOLS_CONTROL, //Escape for Tools
            GFX_ESCAPE_ULT_FW,
            // IMPORTANT:- Force it to 50, so GBG app code works even when we add new escape types..All escapes belonging to this escape ID will
            //      be processed by IGD itself
            GFX_ESCAPE_GBG_ESCAPE_TO_PROCESS = 50,
            // IMPORTANT:- Force it to 51, so GBG app code works even when we add new escape types..All escape codes sent with this escape ID will
            //      be forwarded to GBG helper agent library (as appropriate, the helper library will send it back to IGD)
            GFX_ESCAPE_GBG_ESCAPES_TO_FORWARD = 51,

            GFX_ESCAPE_KM_GUC,
            GFX_ESCAPE_EVENT_PROFILING,
            GFX_ESCAPE_WAFTR,

            GFX_ESCAPE_PERF_STATS = 100,


            GFX_ESCAPE_SW_DECRYPTION,

            GFX_ESCAPE_CHECK_PRESENT_DURATION_SUPPORT = 102,
            // NOTE: WHEN YOU ADD NEW ENUMERATOR, PLEASE UPDATE 
            //       InitializeEscapeCodeTable in miniport\LHDM\Display\AdapterEscape.c

            GFX_MAX_ESCAPE_CODES // MUST BE LAST 
        }


        internal enum GFX_ESCAPE_CODE
        {
            GFX_ESCAPE_CUICOM_CONTROL = 1,
            GFX_ESCAPE_SOFTBIOS_CONTROL = 8
        }

        public enum TOOLS_ESCAPE_CODE
        {
            TOOL_ESC_READ_MMIO_REGISTER,//DP Applet Tool, Test Automation
            TOOL_ESC_DP_APPLET_MISC_FUNC,//DP Applet Tool
            TOOL_ESC_GET_PNM_PIXELCLK_DATA,//PNM TOOL
            TOOL_ESC_SET_PNM_PIXELCLK_DATA,//PNM TOOL
            TOOL_ESC_GET_PSR_RESIDENCY_COUNTER,//BLA Tool 
            TOOL_ESC_QUERY_DISPLAY_DETAILS,//DP Applet Tool 
            TOOL_ESC_SIMULATE_DP12_TOPOLOGY,//DP Topology Simulator
            // MAX_CUI_COM_FUNCTIONS should be the last value in this enum
            MAX_TOOLS_ESCAPES
        }

        #region Tool_ESC_RegisterReadStructures


        [StructLayout(LayoutKind.Sequential)]
        public class TOOL_ESC_EscapeData_RegisterOperation
        {
            public GFX_ESCAPE_HEADER_T header;
            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 8 /*Size of escape data structure*/)]
            public byte[] dataBytes;
        }

        [StructLayout(LayoutKind.Sequential)]
        public class TOOL_ESC_READ_MMIO_REGISTER_ARGS
        {
            public uint offset;
            public uint value;
        }
        #endregion

        public ULT_Framework()
        {
        }
        
        private const int D3DKMT_ESCAPE_DRIVERPRIVATE = 0;

        #region ULT_Framework_Structures


        [StructLayout(LayoutKind.Sequential)]
        public struct GFX_ESCAPE_HEADER_T
        {
            public uint ulReserved;
            public uint ulMinorInterfaceVersion;
            public uint uiMajorEscapeCode;
            public uint uiMinorEscapeCode;
        }

        [StructLayout(LayoutKind.Sequential)]
        public struct LUID
        {
            public uint LowPart;
            public int HighPart;
        }
        [StructLayout(LayoutKind.Sequential)]
        public struct D3DKMT_OPENADAPTERFROMHDC
        {
            public IntPtr hDc;
            public UInt32 hAdapter;
            public LUID AdapterLuid;
            public UInt32 VidPnSourceId;
        }

        [StructLayout(LayoutKind.Sequential)]
        public class ULT_Framework_EscapeData
        {
            public GFX_ESCAPE_HEADER_T header;

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 0x3cdc)]
            public byte[] dataBytes;
        }
        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]
        public struct DISPLAY_DEVICE
        {
            public int cb;
            [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
            public string DeviceName;
            [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 128)]
            public string DeviceString;
            public int StateFlags;
            [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 128)]
            public string DeviceID;
            [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 128)]
            public string DeviceKey;
        }

        [StructLayout(LayoutKind.Sequential)]
        public struct D3DKMT_ESCAPE
        {
            public UInt32 hAdapter;
            public UInt32 hDevice;
            public UInt32 Type;
            public UInt32 Flags;
            public IntPtr pPrivateDriverData;
            public UInt32 PrivateDriverDataSize;
            public UInt32 hContext;
        }

        [StructLayout(LayoutKind.Sequential)]
        public struct D3DKMT_CLOSEADAPTER
        {
            public UInt32 hAdapter;
        }

        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        private static extern int D3DKMTCloseAdapter(
            ref D3DKMT_CLOSEADAPTER closeAdapter
        );
        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        private static extern int D3DKMTEscape(
             ref D3DKMT_ESCAPE escapeData
        );


        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        private static extern int D3DKMTOpenAdapterFromHdc(
            [In, Out] ref D3DKMT_OPENADAPTERFROMHDC openAdapterData
        );

        [DllImport("User32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        private static extern bool EnumDisplayDevices(string lpDevice, uint iDevNum, ref DISPLAY_DEVICE lpDisplayDevice, uint dwFlags);
        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        private static extern IntPtr CreateDC(
            string lpszDriver,
            string lpszDevice,
            string lpszOutput,
            IntPtr lpInitData
        );

        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        private static extern bool DeleteDC(IntPtr hdc);

        [DllImport("kernel32.dll", CallingConvention = CallingConvention.StdCall)]
        private static extern int GetLastError();
#endregion

        public bool SetMethod(object argMessage)
        {
            if (argMessage != null)
            {
                ULT_FW_EscapeParams escParams = argMessage as ULT_FW_EscapeParams;
                ULT_Framework_EscapeData ULT_Esc_EscapeData = new ULT_Framework_EscapeData();

                if (PerformDriverEscape(escParams.driverEscapeData, ULT_Esc_EscapeData, GFX_ESCAPE_CODE_T.GFX_ESCAPE_ULT_FW, TOOLS_ESCAPE_CODE.TOOL_ESC_READ_MMIO_REGISTER))
                {
                    Console.WriteLine("Escape call passed");
                    return true;
                }

               // return _commands[escParams.ULT_Escape_Type](escParams.driverEscapeData);
            }
            return false;
        }

        /// <summary>
        /// This escape call is used for ULT Framework.
        /// </summary>
        /// <param name="escDataStruct"></param>
        /// <param name="escapeData"></param>
        /// <param name="escapeCode"></param>
        /// <returns></returns>
        public static bool PerformDriverEscape(Object escDataStruct, Object escapeData, GFX_ESCAPE_CODE_T majorVersion, TOOLS_ESCAPE_CODE escapeCode)
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
                while (EnumDisplayDevices(null, devId++, ref deviceName, 0))
                {
                    hdc = CreateDC(null, deviceName.DeviceName, null, IntPtr.Zero);
                    if (hdc == IntPtr.Zero)
                    {
                        Console.WriteLine("ERROR: Unable to create device context with CreateDC:{0}", GetLastError());
                        return false;
                    }

                    openAdapterData.hDc = hdc;
                    if (D3DKMTOpenAdapterFromHdc(ref openAdapterData) != 0)
                    {
                        Console.WriteLine("ERROR: Unable to get adapter handle with OpenAdapterFromHDC:{0}", GetLastError());
                        return false;
                    }

                    D3DKMT_ESCAPE kmtEscape = new D3DKMT_ESCAPE();
                    kmtEscape.hAdapter = openAdapterData.hAdapter;
                    kmtEscape.Type = D3DKMT_ESCAPE_DRIVERPRIVATE;

                    GFX_ESCAPE_HEADER_T escHeader = new GFX_ESCAPE_HEADER_T();
                    uint sizeofEscHeader = (uint)Marshal.SizeOf(escHeader);
                    escHeader.ulReserved = ESCDATA_SIZE;//sizeofEscDataStruct;
                    escHeader.ulMinorInterfaceVersion = 1; // Calculate the checksum, if not assign it to zero.
                    escHeader.uiMajorEscapeCode = (uint)majorVersion;
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
                    uint sizeofEscapeData = (uint)bEscapeData.Length; //(uint)Marshal.SizeOf(escHeader) + sizeofEscDataStruct;
                    IntPtr escapeDataPtr = Marshal.AllocHGlobal((int)sizeofEscapeData);

                    // 3. Convert escape data (to IntPtr)
                    Marshal.StructureToPtr(escapeData, escapeDataPtr, true);
                    kmtEscape.pPrivateDriverData = escapeDataPtr;
                    kmtEscape.PrivateDriverDataSize = sizeofEscapeData;

                    // 4. Perform escape call
                    uint retval = (uint)D3DKMTEscape(ref kmtEscape);
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
                Console.WriteLine(String.Format("{Exception Caught: {0}", e.Message.ToString()));
                return false;
            }
            finally
            {
                //Release handles
                if (!DeleteDC(hdc))
                    Console.WriteLine("ERROR: Unable to clear device context: {0}", GetLastError());
                D3DKMT_CLOSEADAPTER closeAdapter = new D3DKMT_CLOSEADAPTER();
                closeAdapter.hAdapter = openAdapterData.hAdapter;

                if (D3DKMTCloseAdapter(ref closeAdapter) != 0)
                    Console.WriteLine("ERROR: Unable to close adapter handle: {0}", GetLastError());
            }
        }

        public static byte[] GetDataBytes(object InputData)
        {
            uint dataSize = (uint)Marshal.SizeOf(InputData);

            IntPtr ptr = Marshal.AllocHGlobal((int)dataSize);
            byte[] byteData = new byte[dataSize];
            Marshal.StructureToPtr(InputData, ptr, true);
            Marshal.Copy(ptr, byteData, 0, (int)dataSize);
            return byteData;
        }
        public static void GetDataFromBytes(byte[] InputData, ref object OutputData)
        {
            int OutputDataSize = Marshal.SizeOf(OutputData);
            IntPtr ptr = Marshal.AllocHGlobal(OutputDataSize);

            Marshal.Copy(InputData, 0, ptr, OutputDataSize);

            Marshal.PtrToStructure(ptr, OutputData);
            Marshal.FreeHGlobal(ptr);
        }
    }
}
