using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;

namespace PlaneScaler
{
    public class RegisterInterface
    {

        private static RegisterInterface _self = null;

        public static RegisterInterface Instance
        {
            get
            {
                if (_self == null)
                {
                    _self = new RegisterInterface();
                }
                return _self;
            }
        }

        public enum RegisterOperation
        {
            READ = 0,
            WRITE
        };

        private const int D3DKMT_ESCAPE_DRIVERPRIVATE = 0;
        private const int GFX_ESCAPE_SOFTBIOS_CONTROL = 8;
        private const int TOOL_ESC_READ_MMIO_REGISTER = 0;
        private const int GFX_ESCAPE_DDRW_MMIO = 21;
        private const int DDRW_ESC_READ_MMIO = 0;
        private const uint MMIO_REGISTER_FUNCTIONCODE = 0x5F66;
        private const int GETMMIOREG_SUBFUNC = 0; //Read register
        private const int SETMMIOREG_SUBFUNC = 1; //Write register
        
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
       [StructLayout(LayoutKind.Sequential)]
        public class MMIOArgs
        {
            public uint offset;
            public uint value;
        }

        public struct GFX_ESCAPE_HEADER
        {
            public uint size;
            public uint checkSum;
            public int escapeCode;
            public uint ulReserved;
        }
            [StructLayout(LayoutKind.Sequential)]
        public struct GFX_ESCAPE_HEADER_T
        {
            public uint ulReserved;
            public uint ulMinorInterfaceVersion;
            public uint uiMajorEscapeCode;
            public uint uiMinorEscapeCode;
        }

        public struct DriverData
        {
            public GFX_ESCAPE_HEADER header;
            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 12)]
            public byte[] dataBytes;
        }
         [StructLayout(LayoutKind.Sequential)]
        public struct DriverData_T
        {
            public GFX_ESCAPE_HEADER_T header;
            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 8)]
            public byte[] dataBytes;
        }

        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        static extern IntPtr CreateDC(
            string lpszDriver,
            string lpszDevice,
           string lpszOutput,
            IntPtr lpInitData
        );

        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        public static extern int D3DKMTOpenAdapterFromHdc(
            [In, Out] ref D3DKMT_OPENADAPTERFROMHDC openAdapterData
        );

        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        public static extern int D3DKMTEscape(
             ref D3DKMT_ESCAPE escapeData
        );

        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        public static extern int D3DKMTCloseAdapter(
            ref D3DKMT_CLOSEADAPTER closeAdapter
        );

        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        static extern bool DeleteDC(
            IntPtr hdc
        );
        [DllImport("User32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern bool EnumDisplayDevices(string lpDevice, uint iDevNum, ref DISPLAY_DEVICE lpDisplayDevice, uint dwFlags);


        [DllImport("kernel32.dll", CallingConvention = CallingConvention.StdCall)]
        private static extern int GetLastError();

        private uint CheckSum(MMIOArgs mmioArgs)
        {
            uint sum = 0;
            sum += mmioArgs.offset;
            sum += mmioArgs.value;
            return sum;
        }
          [StructLayout(LayoutKind.Sequential)]
        private class TOOL_ESC_EscapeData_RegisterOperation
        {
            public GFX_ESCAPE_HEADER_T header;
            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 8 /*Size of escape data structure*/)]
            public byte[] dataBytes;
        }

        internal struct DISPLAY_DEVICE
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

        //private byte[] GetDataBytes(MMIOArgs mmioArgs)
        //{
        //    uint len = (uint)Marshal.SizeOf(mmioArgs);

        //    IntPtr ptr = Marshal.AllocHGlobal((int)len);
        //    byte[] data = new byte[len];
        //    Marshal.StructureToPtr(mmioArgs, ptr, true);
        //    Marshal.Copy(ptr, data, 0, (int)len);

        //    byte[] encryptedData = new byte[len];
        //    //byte magicNumber = 0xAA;

        //    //for (uint count = 0; count < len; count++)
        //    //{
        //    //    encryptedData[count] = (byte)(data[count] ^ magicNumber);
        //    //}
        //    //return encryptedData;
        //    return data;
        //}

        private uint GetRegisterValue(IntPtr dataPtr, uint len)
        {
            DriverData_T driverData = new DriverData_T();
            MMIOArgs mmioArgs = new MMIOArgs();
            driverData = (DriverData_T)Marshal.PtrToStructure(dataPtr, typeof(DriverData_T));

            IntPtr resPtr = Marshal.AllocHGlobal((int)len);
            Marshal.Copy(driverData.dataBytes, 0, resPtr, Marshal.SizeOf(mmioArgs));
            mmioArgs = (MMIOArgs)Marshal.PtrToStructure(resPtr, typeof(MMIOArgs));

            return mmioArgs.value;
        }

        internal static void GetDataFromBytes(byte[] InputData, ref object OutputData)
        {
            int OutputDataSize = Marshal.SizeOf(OutputData);
            IntPtr ptr = Marshal.AllocHGlobal(OutputDataSize);

            Marshal.Copy(InputData, 0, ptr, OutputDataSize);

            Marshal.PtrToStructure(ptr, OutputData);
            Marshal.FreeHGlobal(ptr);
        }

        internal static byte[] GetDataBytes(object InputData)
        {
            uint dataSize = (uint)Marshal.SizeOf(InputData);

            IntPtr ptr = Marshal.AllocHGlobal((int)dataSize);
            byte[] byteData = new byte[dataSize];
            Marshal.StructureToPtr(InputData, ptr, true);
            Marshal.Copy(ptr, byteData, 0, (int)dataSize);
            return byteData;
        }
        internal static bool PerformDriverEscape(Object escDataStruct, Object escapeData)
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
                        //Console.WriteLine( "ERROR: Unable to create device context with CreateDC");
                        continue;
                    }

                    openAdapterData.hDc = hdc;
                    if (D3DKMTOpenAdapterFromHdc(ref openAdapterData) != 0)
                    {
                        Console.WriteLine("ERROR: Unable to get adapter handle with OpenAdapterFromHDC");
                        return false;
                    }

                    D3DKMT_ESCAPE kmtEscape = new D3DKMT_ESCAPE();
                    kmtEscape.hAdapter = openAdapterData.hAdapter;
                    kmtEscape.Type = D3DKMT_ESCAPE_DRIVERPRIVATE;

                    GFX_ESCAPE_HEADER_T escHeader = new GFX_ESCAPE_HEADER_T();
                    uint sizeofEscHeader = (uint)Marshal.SizeOf(escHeader);
                    escHeader.ulReserved = sizeofEscDataStruct;
                    escHeader.ulMinorInterfaceVersion = 1; // Calculate the checksum, if not assign it to zero.
                    if (!MPOPlaneScaler.IsDDRW)
                    {
                        escHeader.uiMajorEscapeCode = 20;
                        escHeader.uiMinorEscapeCode = TOOL_ESC_READ_MMIO_REGISTER;
                    }
                    else
                    {
                        escHeader.uiMajorEscapeCode = GFX_ESCAPE_DDRW_MMIO;
                        escHeader.uiMinorEscapeCode = DDRW_ESC_READ_MMIO;
                    }
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
                    uint retval = (uint)D3DKMTEscape(ref kmtEscape);
                    if (retval != 0)
                    {
                        Console.WriteLine( "Escape call returned {0}", retval);
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
                Console.WriteLine("{Exception Caught: {0}", e.Message.ToString());
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


        internal bool ReadWriteRegister(RegisterOperation regOperation, uint offset, out uint value)
        {
            TOOL_ESC_EscapeData_RegisterOperation Tool_Esc_EscapeData = new TOOL_ESC_EscapeData_RegisterOperation();
            MMIOArgs Tool_Esc_mmioArgs = new MMIOArgs();
            Tool_Esc_mmioArgs.offset = offset;
            Tool_Esc_mmioArgs.value = 0;

            if (PerformDriverEscape(Tool_Esc_mmioArgs, Tool_Esc_EscapeData))
            {
                value = Tool_Esc_mmioArgs.value;
                return true;
            }
            else
            {
                value = 0;
                return false;
            }
        }
            //value = 0;
            //IntPtr hdc = IntPtr.Zero;
            //D3DKMT_OPENADAPTERFROMHDC openAdapterData = new D3DKMT_OPENADAPTERFROMHDC();

            //try
            //{
            //    hdc = CreateDC(null, "\\\\.\\DISPLAY1", null, IntPtr.Zero);
            //    if (hdc == IntPtr.Zero)
            //    {
            //        //SimpleLogger.Error(String.Format("Unable to create device context with CreateDC:{0}", GetLastError()));
            //        return false;
            //    }

            //    openAdapterData.hDc = hdc;
            //    if (D3DKMTOpenAdapterFromHdc(ref openAdapterData) != 0)
            //    {
            //        //SimpleLogger.Error(String.Format("Unable to get adapter handle with OpenAdapterFromHDC:{0}", GetLastError()));
            //        return false;
            //    }

            //    MMIOArgs mmioArgs = new MMIOArgs();
            //    mmioArgs.offset = offset;
            //    mmioArgs.value = 0;
            //    //if (regOperation == RegisterOperation.READ)
            //    //{
            //    //    mmioArgs.cmd = (MMIO_REGISTER_FUNCTIONCODE << 16) | (GETMMIOREG_SUBFUNC);
            //    //    mmioArgs.value = 0;
            //    //}
            //    //else
            //    //{
            //    //    mmioArgs.cmd = (MMIO_REGISTER_FUNCTIONCODE << 16) | (SETMMIOREG_SUBFUNC);
            //    //    mmioArgs.value = value;
            //    //}


            //    GFX_ESCAPE_HEADER_T escHeader = new GFX_ESCAPE_HEADER_T();
            //    uint len = (uint)Marshal.SizeOf(escHeader);
            //    escHeader.ulReserved = len;
            //    escHeader.ulMinorInterfaceVersion = 1;
            //    escHeader.uiMajorEscapeCode = 20;
            //    escHeader.uiMinorEscapeCode = TOOL_ESC_READ_MMIO_REGISTER;

            //    DriverData_T driverData = new DriverData_T();
            //    driverData.header = escHeader;
            //    driverData.dataBytes = GetDataBytes(mmioArgs);

            //    int dataLen = Marshal.SizeOf(driverData);
            //    IntPtr dataPtr = Marshal.AllocHGlobal(dataLen);
            //    Marshal.StructureToPtr(driverData, dataPtr, true);

            //    D3DKMT_ESCAPE kmtEscape = new D3DKMT_ESCAPE();
            //    kmtEscape.hAdapter = openAdapterData.hAdapter;
            //    kmtEscape.Type = D3DKMT_ESCAPE_DRIVERPRIVATE;
            //    kmtEscape.pPrivateDriverData = dataPtr;
            //    kmtEscape.PrivateDriverDataSize = (uint)Marshal.SizeOf(driverData);

            //    if (D3DKMTEscape(ref kmtEscape) != 0)
            //    {
            //        Console.WriteLine(String.Format("Unable to {0} register value - {1}", regOperation, GetLastError()));
            //        return false;
            //    }
            //    else
            //    {
            //        //SimpleLogger.Debug("Register operation successful");
            //        if (regOperation == RegisterOperation.READ)
            //        {
            //            value = GetRegisterValue(kmtEscape.pPrivateDriverData, kmtEscape.PrivateDriverDataSize);
            //        }
            //    }
            //    return true;
            //}
            //catch (Exception e)
            //{
            //    Console.WriteLine(String.Format("Unable to {0} register value:{1}", regOperation, e.ToString()));
            //    return false;
            //}
            //finally
            //{
            //    //Release handles
            //    if (!DeleteDC(hdc))
            //    {
            //        Console.WriteLine(String.Format("Unable to clear device context:{0}", GetLastError()));

            //    }
            //    D3DKMT_CLOSEADAPTER closeAdapter = new D3DKMT_CLOSEADAPTER();
            //    closeAdapter.hAdapter = openAdapterData.hAdapter;

            //    if (D3DKMTCloseAdapter(ref closeAdapter) != 0)
            //    {
            //        Console.WriteLine(String.Format("Unable to close adapter handle:{0}", GetLastError()));
            //    }
            //}
        //}
    }
}
