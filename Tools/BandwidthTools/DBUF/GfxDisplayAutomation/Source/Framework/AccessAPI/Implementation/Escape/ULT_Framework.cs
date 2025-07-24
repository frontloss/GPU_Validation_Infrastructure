namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Runtime.InteropServices;
    using System.Collections.Generic;

    public class ULT_Framework : FunctionalBase, ISetMethod
    {
        public ULT_Framework()
        {
        }

        private const int D3DKMT_ESCAPE_DRIVERPRIVATE = 0;

        #region ULT_Framework_Structures

        [StructLayout(LayoutKind.Sequential, Pack = 1)]
        public class ULT_Framework_EscapeData
        {
            public GFX_ESCAPE_HEADER_T header;

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 0x3cdc)]//0x2731)]
            public byte[] dataBytes;
        }

        #endregion

        public bool SetMethod(object argMessage)
        {
            if (argMessage != null)
            {
                ULT_FW_EscapeParams escParams = argMessage as ULT_FW_EscapeParams;

                ULT_Framework_EscapeData ULT_Esc_EscapeData = new ULT_Framework_EscapeData();

                if (PerformDriverEscape(escParams.driverEscapeData, ULT_Esc_EscapeData, GFX_ESCAPE_CODE_T.GFX_ESCAPE_ULT_FW, TOOLS_ESCAPE_CODE.TOOL_ESC_READ_MMIO_REGISTER))
                {
                    //Log.Message("Escape call: {0} passed", escParams.ULT_Escape_Type);
                    return true;
                }
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
        internal static bool PerformDriverEscape(Object escDataStruct, Object escapeData, GFX_ESCAPE_CODE_T majorVersion, TOOLS_ESCAPE_CODE escapeCode)
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
                uint sizeofEscapeData = (uint)Marshal.SizeOf(escapeData);
                escHeader.ulReserved = sizeofEscapeData - sizeofEscHeader;
                escHeader.ulMinorInterfaceVersion = 1; // Calculate the checksum, if not assign it to zero.
                escHeader.uiMajorEscapeCode = (uint)majorVersion;
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
                IntPtr escapeDataPtr = Marshal.AllocHGlobal((int)sizeofEscapeData);

                // 3. Convert escape data (to IntPtr)
                Marshal.StructureToPtr(escapeData, escapeDataPtr, true);
                kmtEscape.pPrivateDriverData = escapeDataPtr;
                kmtEscape.PrivateDriverDataSize = sizeofEscapeData;

                // 4. Perform escape call
                uint retval = (uint)Interop.D3DKMTEscape(ref kmtEscape);
                if (retval != 0)
                {
                    Log.Alert(false, "Escape call returned {0}", retval);
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
    }
}
