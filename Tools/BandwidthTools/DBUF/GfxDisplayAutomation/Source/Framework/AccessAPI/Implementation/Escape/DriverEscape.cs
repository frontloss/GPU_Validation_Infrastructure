namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Runtime.InteropServices;
    using System.Collections.Generic;
    using Microsoft.Win32.SafeHandles;

    internal class DriverEscape : FunctionalBase, ISetMethod, IParse
    {
        public Dictionary<DriverEscapeType, Func<object, bool>> _commands = null;

        public DriverEscape()
        {
            this._commands = new Dictionary<DriverEscapeType, Func<object, bool>>();
            this._commands.Add(DriverEscapeType.Register, this.ParseRegisterRead);
            this._commands.Add(DriverEscapeType.PortName, this.ParsePortName);
            this._commands.Add(DriverEscapeType.GTARegisterRead, this.ParseGTARegisterRead);
            this._commands.Add(DriverEscapeType.GTARegisterWrite, this.ParseGTARegisterWrite);
            this._commands.Add(DriverEscapeType.VBTByteRead, this.ParseVBTByteRead);
            this._commands.Add(DriverEscapeType.SBRegisterRead, this.ParseSBRegisterRead);
            this._commands.Add(DriverEscapeType.DIVARegisterEscape, this.ParseDIVARegisterEscapeRead);
            this._commands.Add(DriverEscapeType.DIVAMMIORead, this.ParseDIVAMMIORead);
            this._commands.Add(DriverEscapeType.DIVAMMIOWrite, this.ParseDIVAMMIOWrite);
        }

        private const int D3DKMT_ESCAPE_DRIVERPRIVATE = 0;

        #region 15_33_RegisterReadStructures

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

        #region 15_33_GetPortNameStructures

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
            INTDPE_PORT,
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
            WIGIG_PORT,
            DVOF_PORT,
            INTHDMIF_PORT,
            INTDPF_PORT,
            DVOE_PORT,     // For Gen11, DDIE can be used for HDMI
            INTHDMIE_PORT, // For Gen11, DDIE can be used for HDMI
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

        [DllImport("Utilities.dll")]
        private static extern UInt32 readMMIOReg(UInt32 offset, ref UInt32 value);

        [DllImport("Utilities.dll")]
        private static extern UInt32 writeMMIOReg(UInt32 dwOffset, UInt32 dwValue);

        [DllImport("Utilities.dll")]
        private static extern UInt32 readVBT_BYTE(UInt32 dwOffset);

        [DllImport("Utilities.dll")]
        private static extern UInt32 ReadSBRegister(UInt32 DSP_SS_PM_REG, UInt32 PUNIT_PORT_ID);

        public bool SetMethod(object argMessage)
        {
            if (argMessage != null)
            {
                DriverEscapeParams escParams = argMessage as DriverEscapeParams;

                return _commands[escParams.driverEscapeType](escParams.driverEscapeData);
            }
            return false;
        }

        /// <summary>
        /// This is a unified call for 15.33 branch.
        /// </summary>
        /// <param name="escDataStruct"></param>
        /// <param name="escapeData"></param>
        /// <param name="escapeCode"></param>
        /// <returns></returns>
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

                // Usually DISPLAY1 is used. While is to comprehend multi-mon where some displays might be driven from DISPLAY2
                while (Interop.EnumDisplayDevices(null, devID++, ref deviceName, 0))
                {
                    hdc = Interop.CreateDC(deviceName.DeviceName, null, null, IntPtr.Zero);
                    // hdc = Interop.GetDC(IntPtr.Zero);

                    if (hdc == IntPtr.Zero)
                    {
                        //Log.Verbose(false, "Unable to create device context with CreateDC with {0} -> {1}", deviceName.DeviceName, Interop.GetLastError());
                    }
                    else
                        break;
                }


                if (hdc == IntPtr.Zero)
                {
                    bCreateDC = false;
                    Log.Fail(false, "ERROR: Unable to create device context with CreateDC:{0}", Interop.GetLastError());
                    return false;
                }
                openAdapterData.hDc = hdc;
                if (Interop.D3DKMTOpenAdapterFromHdc(ref openAdapterData) != 0)
                {
                    bOpenAdapter = false;
                    Log.Fail(false, "ERROR: Unable to get adapter handle with OpenAdapterFromHDC:{0}", Interop.GetLastError());
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
                    Log.Fail(false, "Escape call returned {0}", retval);
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
                Log.Fail(false, "{Exception Caught: {1}", e.Message.ToString());
                return false;
            }
            finally
            {
                if (bCreateDC == true)
                {
                    //Release handles
                    if (!Interop.DeleteDC(hdc))
                        Log.Fail(false, "ERROR: Unable to clear device context: {0}", Interop.GetLastError());
                }
                if (bOpenAdapter == true)
                {
                    D3DKMT_CLOSEADAPTER closeAdapter = new D3DKMT_CLOSEADAPTER();
                    closeAdapter.hAdapter = openAdapterData.hAdapter;

                    if (Interop.D3DKMTCloseAdapter(ref closeAdapter) != 0)
                        Log.Fail(false, "ERROR: Unable to close adapter handle: {0}", Interop.GetLastError());
                }
            }
        }

        internal bool ParseDIVAMMIORead<I>(I args)
        {
            bool status = true;
            DriverEscapeData<uint, uint> RegisterData = args as DriverEscapeData<uint, uint>;

            // Create CLR-Utility handle
            DivaUtilityCLR DivaUtility = new DivaUtilityCLR();

            // Get DIVA device handle
            SafeFileHandle hDivaDevice = DivaUtility.GetDivaDeviceHandle();

            // Create 'Generic GFX Access DIVA CLR Utility'
            DivaGenericGfxAccessUtilityCLR DivaGfxAccessUtility = new DivaGenericGfxAccessUtilityCLR(hDivaDevice);

            // Create data structure to read MMIO
            DIVA_MMIO_ACCESS_ARGS_CLR MmioAccessArgs = new DIVA_MMIO_ACCESS_ARGS_CLR();
            MmioAccessArgs.Offset = RegisterData.input;

            try
            {
                // Read MMIO
                DivaGfxAccessUtility.ReadMmio(MmioAccessArgs);
                Log.Message("INFO: DIRECT-MMIO-READ Value @ Offset: 0x{0:X} = 0x{1:X}",
                    MmioAccessArgs.Offset,
                    MmioAccessArgs.Value);
                RegisterData.output = MmioAccessArgs.Value;
            }
            catch (Exception Exp)
            {
                Log.Fail("ERROR: Exception in DIRECT-MMIO-READ: {0}",
                    Exp.Message);
                status = false;
            }
            return status;
        }

        internal bool ParseDIVAMMIOWrite<I>(I args)
        {
            bool status = true;
            DriverEscapeData<uint, uint> RegisterData = args as DriverEscapeData<uint, uint>;

            // Create CLR-Utility handle
            DivaUtilityCLR DivaUtility = new DivaUtilityCLR();

            // Get DIVA device handle
            SafeFileHandle hDivaDevice = DivaUtility.GetDivaDeviceHandle();

            // Create 'Generic GFX Access DIVA CLR Utility'
            DivaGenericGfxAccessUtilityCLR DivaGfxAccessUtility = new DivaGenericGfxAccessUtilityCLR(hDivaDevice);

            // Create data structure to Write MMIO
            DIVA_MMIO_ACCESS_ARGS_CLR MmioAccessArgs = new DIVA_MMIO_ACCESS_ARGS_CLR();
            MmioAccessArgs.Offset = RegisterData.input;
            MmioAccessArgs.Value = RegisterData.output;

            try
            {
                // Write MMIO
                DivaGfxAccessUtility.WriteMmio(MmioAccessArgs);
                Log.Message("INFO: DIRECT-MMIO-Write @ Offset: 0x{0:X} = 0x{1:X}",
                    MmioAccessArgs.Offset,
                    MmioAccessArgs.Value);
            }
            catch (Exception Exp)
            {
                Log.Fail("ERROR: Exception in DIRECT-MMIO-WRITE: {0}",
                    Exp.Message);
                status = false;
            }
            return status;
        }

//
// Structure for making Thunk Escape calls
// 
        [StructLayout(LayoutKind.Sequential)]
        public class DIVA_ESC_MMIO_ACCESS_ARGS
        {
            [MarshalAs(UnmanagedType.U4)]
            public UInt32 ulReserved1;

            [MarshalAs(UnmanagedType.U4)]
            public UInt32 ulMinorInterfaceVersion;

            [MarshalAs(UnmanagedType.U4)]
            public UInt32 ulMajorEscapeCode;

            [MarshalAs(UnmanagedType.U4)]
            public UInt32 uiMinorEscapeCode;

            [MarshalAs(UnmanagedType.U4)]
            public UInt32 Offset;

            [MarshalAs(UnmanagedType.U4)]
            public UInt32 Value;
        }

        internal bool ParseDIVARegisterEscapeRead<I>(I args)
        {
            DriverEscapeData<uint, uint> RegisterData = args as DriverEscapeData<uint, uint>;

            uint reg_value = 0;

            if (PerformDIVADriverEscape(RegisterData.input, ref reg_value, TOOLS_ESCAPE_CODE.TOOL_ESC_READ_MMIO_REGISTER))
            {
                RegisterData.output = reg_value;
                return true;
            }
            return false;
        }
        /// <summary>
        /// This escape call is used for DIVA
        /// </summary>
        /// <param name="escDataStruct"></param>
        /// <param name="escapeData"></param>
        /// <param name="escapeCode"></param>
        /// <returns></returns>
        internal static bool PerformDIVADriverEscape(uint offset, ref uint reg_value, TOOLS_ESCAPE_CODE escapeCode)
        {
            bool status = true;

            // Create CLR-Utility handle
            DivaUtilityCLR DivaUtility = new DivaUtilityCLR();

            // Get DIVA device handle
            SafeFileHandle hDivaDevice = DivaUtility.GetDivaDeviceHandle();

            // Create 'Generic GFX Access DIVA CLR Utility'
            DivaGenericGfxAccessUtilityCLR DivaGfxAccessUtility = new DivaGenericGfxAccessUtilityCLR(hDivaDevice);

            // Create data structure to read MMIO via Escape API
            DIVA_ESC_MMIO_ACCESS_ARGS EscMmioArgs = new DIVA_ESC_MMIO_ACCESS_ARGS();
            EscMmioArgs.ulMinorInterfaceVersion = 1;
            EscMmioArgs.ulMajorEscapeCode = 20; // GFX_ESCAPE_TOOLS_CONTROL
            EscMmioArgs.uiMinorEscapeCode = (uint)escapeCode;
            EscMmioArgs.Offset = offset;
            EscMmioArgs.Value = 0xFFFF;

            // Allocate unmanged memory to hold the managed struct.
            IntPtr UnmanagedMemAddr = Marshal.AllocHGlobal(Marshal.SizeOf(EscMmioArgs));

            // Copy the managed struct to unmanaged memory.
            Marshal.StructureToPtr(EscMmioArgs,
                UnmanagedMemAddr,
                false);

            DIVA_D3DKMT_ESC_ARGS_CLR DivaEscArgs = new DIVA_D3DKMT_ESC_ARGS_CLR();
            DivaEscArgs.PrivateDriverDataSize = (uint)Marshal.SizeOf(EscMmioArgs);
            Marshal.Copy(UnmanagedMemAddr, DivaEscArgs.PrivateDriverData, 0, (int)DivaEscArgs.PrivateDriverDataSize);

            try
            {
                // Read MMIO
                DivaGfxAccessUtility.D3DKMTEscape(DivaEscArgs);

                // Marshal the resultant unmanaged memory contents to managed struct
                Marshal.PtrToStructure(UnmanagedMemAddr,
                    EscMmioArgs);

                Log.Message("INFO: ESCAPE-MMIO-READ Value @ Offset: 0x{0:X} = 0x{1:X}",
                    EscMmioArgs.Offset,
                    EscMmioArgs.Value);

                reg_value = EscMmioArgs.Value;

            }
            catch (Exception Exp)
            {
                Log.Fail("ERROR: Exception in ESCAPE-MMIO-READ: {0}",
                    Exp.Message);
                status = false;
            }
            finally
            {
                // Free the unmanaged memory allocated to hold managed struct
                Marshal.FreeHGlobal(UnmanagedMemAddr);
                UnmanagedMemAddr = IntPtr.Zero;
            }
            return status;
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
                    hdc = Interop.CreateDC(deviceName.DeviceName, null, null, IntPtr.Zero);
                    // hdc = Interop.GetDC(IntPtr.Zero);

                    if (hdc == IntPtr.Zero)
                    {
                       // Log.Verbose(false, "Unable to create device context with CreateDC with {0} -> {1}", deviceName.DeviceName, Interop.GetLastError());
                    }
                    else
                        break; // Currently only DISPLAY1 is used. User can include logic for other display adapters also.
                }

                if (hdc == IntPtr.Zero)
                {
                    bCreateDC = false;
                    Log.Fail(false, "ERROR: Unable to create device context with CreateDC:{0}", Interop.GetLastError());
                    return false;
                }

                openAdapterData.hDc = hdc;
                if (Interop.D3DKMTOpenAdapterFromHdc(ref openAdapterData) != 0)
                {
                    bOpenAdapter = false;
                    Log.Fail(false, "ERROR: Unable to get adapter handle with OpenAdapterFromHDC:{0}", Interop.GetLastError());
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
                    //Log.Verbose(false, "Escape call returned {0}", retval);
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
                Log.Fail(false, "{Exception Caught: {1}", e.Message.ToString());
                return false;
            }
            finally
            {
                if (bCreateDC == true)
                {
                    //Release handles
                    if (!Interop.DeleteDC(hdc))
                        Log.Fail(false, "ERROR: Unable to clear device context: {0}", Interop.GetLastError());
                }
                if (bOpenAdapter == true)
                {
                    D3DKMT_CLOSEADAPTER closeAdapter = new D3DKMT_CLOSEADAPTER();
                    closeAdapter.hAdapter = openAdapterData.hAdapter;

                    if (Interop.D3DKMTCloseAdapter(ref closeAdapter) != 0)
                        Log.Fail(false, "ERROR: Unable to close adapter handle: {0}", Interop.GetLastError());
                }
            }
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

        internal bool ParseGTARegisterRead<I>(I args)
        {
            DriverEscapeData<uint, uint> RegisterData = args as DriverEscapeData<uint, uint>;

            uint tempValue = 0;
            readMMIOReg(RegisterData.input, ref tempValue);
            RegisterData.output = tempValue;

            return true;
        }

        internal bool ParseGTARegisterWrite<I>(I args)
        {
            DriverEscapeData<uint, uint> RegisterData = args as DriverEscapeData<uint, uint>;
            writeMMIOReg(RegisterData.input, RegisterData.output);
            return true;
        }

        internal bool ParseVBTByteRead<I>(I args)
        {
            DriverEscapeData<List<uint>, List<uint>> VBTData = args as DriverEscapeData<List<uint>, List<uint>>;

            VBTData.output.Clear();
            for (UInt32 i = 0; i < 4400; i++)
            {
                VBTData.output.Add(readVBT_BYTE(i));
            }
            return true;
        }

        private bool ParseSBRegisterRead<I>(I args)
        {
            DriverEscapeData<SBRegisterData, uint> SBRegisterData = args as DriverEscapeData<SBRegisterData, uint>;

            SBRegisterData.output = ReadSBRegister(SBRegisterData.input.DSP_SS_PM_REG, SBRegisterData.input.PUNIT_PORT_ID);
            Log.Verbose("DSP_SS_PM_REG: {0}, PUNIT_ID: {1}, output: {2}", SBRegisterData.input.DSP_SS_PM_REG.ToString("X"), SBRegisterData.input.PUNIT_PORT_ID.ToString("X"), SBRegisterData.output.ToString("X"));
            return true;
        }

        private bool GetDriverPortInfo(uint winId, ref PORT_TYPES driverPort)
        {
            TOOL_ESC_EscapeData_QueryDisplayDetailsArgs Tool_Esc_escapeQueryDisplayData = new TOOL_ESC_EscapeData_QueryDisplayDetailsArgs();
            TOOL_ESC_QUERY_DISPLAY_DETAILS_ARGS Tool_Esc_SbInfo = new TOOL_ESC_QUERY_DISPLAY_DETAILS_ARGS();

            Tool_Esc_SbInfo.ulDisplayUID = winId;
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
            Log.Verbose("Fetching PortName by WindowsId: 0x{0}", PortData.input.ToString("X"));
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
            Log.Verbose("Fetching PortName by WindowsId: 0x{0}", PortData.input.ToString("X"));
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
                case PORT_TYPES.INTDPE_PORT:
                case PORT_TYPES.INTDPF_PORT:
                    return DisplayType.DP;
                case PORT_TYPES.INTHDMIB_PORT:
                case PORT_TYPES.INTHDMIC_PORT:
                case PORT_TYPES.INTHDMID_PORT:
                case PORT_TYPES.INTHDMIE_PORT:
                case PORT_TYPES.INTHDMIF_PORT:
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
                case PORT_TYPES.INTDPE_PORT:
                case PORT_TYPES.DVOE_PORT:
                case PORT_TYPES.INTHDMIE_PORT:
                    actualPort = PORT.PORTE;
                    break;
                case PORT_TYPES.INTDPF_PORT:
                case PORT_TYPES.DVOF_PORT:
                case PORT_TYPES.INTHDMIF_PORT:
                    actualPort = PORT.PORTF;
                    break;
                case PORT_TYPES.TPV_PORT:
                    actualPort = PORT.TVPORT;
                    break;
                default:
                    actualPort = PORT.NONE;
                    break;
            }
        }

        public void Parse(string[] args)
        {
            bool loop = false;
            uint range = 0;

            if (args.Length == 4 && args[3].ToLower().Contains("loop"))
            {
                loop = true;
            }
            else if (args.Length == 5 && args[3].ToLower().Contains("range"))
            {
                range = Convert.ToUInt32(args[4]);
            }

            if (args.Length >= 3 && args[0].ToLower().Contains("get"))
            {
                DriverEscapeType escapeType = (DriverEscapeType)Enum.Parse(typeof(DriverEscapeType), args[1].ToLower(), true);

                do
                {
                    switch (escapeType)
                    {
                        case DriverEscapeType.PortName:
                            DriverEscapeData<uint, PORT> portData = new DriverEscapeData<uint, PORT>();
                            portData.input = Convert.ToUInt32(args[2], 16);

                            if (_commands[escapeType](portData))
                                Log.Verbose("PortName for MonitorId:{0} is {1}", args[2], portData.output);
                            else
                                Log.Alert("Fail to get PortName");
                            break;

                        case DriverEscapeType.Register:
                            DriverEscapeData<uint, uint> registerData = new DriverEscapeData<uint, uint>();
                            for (uint count = 0; count <= range; count++)
                            {
                                registerData.input = Convert.ToUInt32(args[2], 16) + (count * 4);

                                if (_commands[escapeType](registerData))
                                    Log.Verbose("RegisterValue for Offset:{0} is {1}", registerData.input.ToString("X"), registerData.output.ToString("X"));
                                else
                                    Log.Alert("Fail to get RegisterValue");

                                if (range > 0)
                                {
                                    using (System.IO.StreamWriter file =
                                                  new System.IO.StreamWriter(@"RegisterDump.txt", true))
                                    {
                                        file.WriteLine(string.Format("{0}:{1}", registerData.input.ToString("X"), registerData.output.ToString("X8")));
                                    }
                                }
                            }
                            break;

                        case DriverEscapeType.GTARegisterRead:
                            DriverEscapeData<uint, uint> gtaRegisterReadData = new DriverEscapeData<uint, uint>();
                            gtaRegisterReadData.input = Convert.ToUInt32(args[2], 16);

                            if (_commands[escapeType](gtaRegisterReadData))
                                Log.Verbose("RegisterValue for Offset:{0} is {1}", args[2], gtaRegisterReadData.output.ToString("X"));
                            else
                                Log.Alert("Fail to get RegisterValue");
                            break;

                        case DriverEscapeType.VBTByteRead:
                            DriverEscapeData<uint, uint> VBTByteReadData = new DriverEscapeData<uint, uint>();
                            VBTByteReadData.input = Convert.ToUInt32(args[2], 16);

                            if (_commands[escapeType](VBTByteReadData))
                                Log.Verbose("VBT Data for Offset:{0} is {1}", args[2], VBTByteReadData.output.ToString("X"));
                            else
                                Log.Alert("Fail to get VBT Data");
                            break;

                        case DriverEscapeType.DIVARegisterEscape:
                            DriverEscapeData<uint, uint> divaRegisterData = new DriverEscapeData<uint, uint>();
                            divaRegisterData.input = Convert.ToUInt32(args[2], 16);

                            if (_commands[escapeType](divaRegisterData))
                                Log.Verbose("DIVA Escape RegisterValue for Offset:{0} is {1}", args[2], divaRegisterData.output.ToString("X"));
                            else
                                Log.Alert("Fail to get DIVA Escape RegisterValue");
                            break;

                        case DriverEscapeType.DIVAMMIORead:
                            DriverEscapeData<uint, uint> divaMMIORead = new DriverEscapeData<uint, uint>();
                            divaMMIORead.input = Convert.ToUInt32(args[2], 16);

                            if (_commands[escapeType](divaMMIORead))
                                Log.Verbose("DIVA Direct MMIO RegisterValue for Offset:{0} is {1}", args[2], divaMMIORead.output.ToString("X"));
                            else
                                Log.Alert("Fail to get DIVA Direct MMIO RegisterValue");
                            break;
                        default:
                            this.HelpText();
                            return;
                    }

                    System.Threading.Thread.Sleep(1000);
                } while (loop);
            }
            else if (args.Length == 4 && args[0].ToLower().Contains("set"))
            {
                DriverEscapeType escapeType = (DriverEscapeType)Enum.Parse(typeof(DriverEscapeType), args[1].ToLower(), true);

                switch (escapeType)
                {
                    case DriverEscapeType.GTARegisterWrite:
                        DriverEscapeData<uint, uint> gtaRegisterWriteData = new DriverEscapeData<uint, uint>();
                        gtaRegisterWriteData.input = Convert.ToUInt32(args[2], 16);
                        gtaRegisterWriteData.output = Convert.ToUInt32(args[3], 16);

                        if (_commands[escapeType](gtaRegisterWriteData))
                            Log.Verbose("GTARegisterWrite, Offset:{0},value:{1} written successfully.", args[2], gtaRegisterWriteData.output.ToString("X"));
                        else
                            Log.Alert("Fail to set RegisterValue");
                        break;

                    case DriverEscapeType.DIVAMMIOWrite:
                        DriverEscapeData<uint, uint> divaMMIOWrite = new DriverEscapeData<uint, uint>();
                        divaMMIOWrite.input = Convert.ToUInt32(args[2], 16);
                        divaMMIOWrite.output = Convert.ToUInt32(args[3], 16);

                        if (_commands[escapeType](divaMMIOWrite))
                            Log.Verbose("DIVAMMIOWrite, Offset:{0},value:{1} written successfully.", args[2], divaMMIOWrite.output.ToString("X"));
                        else
                            Log.Alert("Fail to set RegisterValue");
                        break;
                    default:
                        this.HelpText();
                        return;
                }
            }
            else
                this.HelpText();
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("..\\>Problem with Commandline Parameters. \n Please type : Execute.exe DriverEscape get <Register/PortName/GTARegisterRead/VBTByteRead/DIVARegisterEscape/DIVAMMIORead> <inputvalue> <loop>").Append(Environment.NewLine);
            sb.Append("..\\>\n Execute.exe DriverEscape set <GTARegisterWrite/DIVAMMIOWrite> <inputvalue> <outputvalue>").Append(Environment.NewLine);
            sb.Append("For example : Execute.exe DriverEscape get Register 70080");
            sb.Append("For infinite loop register read : Execute.exe DriverEscape get Register 70080 loop");
            sb.Append("For infinite loop register read : Execute.exe DriverEscape get Register 70080 range 10");
            Log.Message(sb.ToString());
        }
    }
}
