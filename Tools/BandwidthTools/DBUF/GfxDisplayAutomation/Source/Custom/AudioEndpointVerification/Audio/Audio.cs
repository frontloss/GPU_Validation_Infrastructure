namespace AudioEndpointVerification
{
    using System;
    using System.Runtime.InteropServices;
    public enum Platform
    {
        IVBM,
        HSWM,
        HSWDT,
        HSWU,
        VLV,
        BDW,
        CHV,
        BXT,
        SKL,
        CNL
    }
    public enum AudioInputSource
    {
        Single,
        Multiple
    }
    public enum EDataFlow
    {
        eRender = 0,
        eCapture = 1,
        eAll = 2,
        EDataFlow_enum_count = 3
    }
    [Flags]
    public enum EDeviceState : uint
    {
        DEVICE_STATE_ACTIVE = 0x00000001,
        DEVICE_STATE_UNPLUGGED = 0x00000002,
        DEVICE_STATE_NOTPRESENT = 0x00000004,
        DEVICE_STATEMASK_ALL = 0x00000007
    }
    [Flags]
    public enum CLSCTX : uint
    {
        INPROC_SERVER = 0x1,
        INPROC_HANDLER = 0x2,
        LOCAL_SERVER = 0x4,
        INPROC_SERVER16 = 0x8,
        REMOTE_SERVER = 0x10,
        INPROC_HANDLER16 = 0x20,
        RESERVED1 = 0x40,
        RESERVED2 = 0x80,
        RESERVED3 = 0x100,
        RESERVED4 = 0x200,
        NO_CODE_DOWNLOAD = 0x400,
        RESERVED5 = 0x800,
        NO_CUSTOM_MARSHAL = 0x1000,
        ENABLE_CODE_DOWNLOAD = 0x2000,
        NO_FAILURE_LOG = 0x4000,
        DISABLE_AAA = 0x8000,
        ENABLE_AAA = 0x10000,
        FROM_DEFAULT_CONTEXT = 0x20000,
        INPROC = INPROC_SERVER | INPROC_HANDLER,
        SERVER = INPROC_SERVER | LOCAL_SERVER | REMOTE_SERVER,
        ALL = SERVER | INPROC_HANDLER
    }
    public enum EStgmAccess
    {
        STGM_READ = 0x00000000,
        STGM_WRITE = 0x00000001,
        STGM_READWRITE = 0x00000002
    }
    public enum ERole
    {
        eConsole = 0,
        eMultimedia = 1,
        eCommunications = 2,
        ERole_enum_count = 3
    }
    [Flags]
    public enum EEndpointHardwareSupport
    {
        Volume = 0x00000001,
        Mute = 0x00000002,
        Meter = 0x00000004
    }
    public enum AudioSessionState
    {
        AudioSessionStateInactive = 0,
        AudioSessionStateActive = 1,
        AudioSessionStateExpired = 2
    }
    public enum AudioSessionDisconnectReason
    {
        DisconnectReasonDeviceRemoval = 0,
        DisconnectReasonServerShutdown = (DisconnectReasonDeviceRemoval + 1),
        DisconnectReasonFormatChanged = (DisconnectReasonServerShutdown + 1),
        DisconnectReasonSessionLogoff = (DisconnectReasonFormatChanged + 1),
        DisconnectReasonSessionDisconnected = (DisconnectReasonSessionLogoff + 1),
        DisconnectReasonExclusiveModeOverride = (DisconnectReasonSessionDisconnected + 1)
    }
    public struct PropertyKey
    {
        public Guid fmtid;
        public int pid;
    };

    internal struct Blob
    {
        public int Length;
        public IntPtr Data;
        private void FixCS0649()
        {
            Length = 0;
            Data = IntPtr.Zero;
        }
    }

    [StructLayout(LayoutKind.Explicit)]
    public struct PropVariant
    {
        [FieldOffset(0)]
        short vt;
        [FieldOffset(2)]
        short wReserved1;
        [FieldOffset(4)]
        short wReserved2;
        [FieldOffset(6)]
        short wReserved3;
        [FieldOffset(8)]
        sbyte cVal;
        [FieldOffset(8)]
        byte bVal;
        [FieldOffset(8)]
        short iVal;
        [FieldOffset(8)]
        ushort uiVal;
        [FieldOffset(8)]
        int lVal;
        [FieldOffset(8)]
        uint ulVal;
        [FieldOffset(8)]
        long hVal;
        [FieldOffset(8)]
        ulong uhVal;
        [FieldOffset(8)]
        float fltVal;
        [FieldOffset(8)]
        double dblVal;
        [FieldOffset(8)]
        Blob blobVal;
        [FieldOffset(8)]
        DateTime date;
        [FieldOffset(8)]
        bool boolVal;
        [FieldOffset(8)]
        int scode;
        [FieldOffset(8)]
        System.Runtime.InteropServices.ComTypes.FILETIME filetime;
        [FieldOffset(8)]
        IntPtr everything_else;

        //I'm sure there is a more efficient way to do this but this works ..for now..
        internal byte[] GetBlob()
        {
            byte[] Result = new byte[blobVal.Length];
            for (int i = 0; i < blobVal.Length; i++)
            {
                Result[i] = Marshal.ReadByte((IntPtr)((long)(blobVal.Data) + i));
            }
            return Result;
        }

        public object Value
        {
            get
            {
                VarEnum ve = (VarEnum)vt;
                switch (ve)
                {
                    case VarEnum.VT_I1:
                        return bVal;
                    case VarEnum.VT_I2:
                        return iVal;
                    case VarEnum.VT_I4:
                        return lVal;
                    case VarEnum.VT_I8:
                        return hVal;
                    case VarEnum.VT_INT:
                        return iVal;
                    case VarEnum.VT_UI4:
                        return ulVal;
                    case VarEnum.VT_LPWSTR:
                        return Marshal.PtrToStringUni(everything_else);
                    case VarEnum.VT_BLOB:
                        return GetBlob();
                }
                return "FIXME Type = " + ve.ToString();
            }
        }

    }
}
