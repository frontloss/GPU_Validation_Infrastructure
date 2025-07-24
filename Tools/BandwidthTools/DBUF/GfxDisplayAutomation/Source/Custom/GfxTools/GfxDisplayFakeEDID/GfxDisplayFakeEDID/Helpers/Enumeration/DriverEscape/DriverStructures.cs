namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Runtime.InteropServices;

    [StructLayout(LayoutKind.Sequential)]
    internal class SB_QUERY_DISPLAY_DETAILS_ARGS
    {
        public uint Command;    //Always
        public QUERY_DISPLAY_DETAILS_ARGS SbInfo;
    };
    [StructLayout(LayoutKind.Sequential)]//, Pack = 1 /*To allocate 1 byte for char/bool*/)]
    internal class QUERY_DISPLAY_DETAILS_ARGS
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
    internal class EscapeData_QueryDisplayDetailsArgs
    {
        public GFX_ESCAPE_HEADER header;
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 28)]
        public byte[] dataBytes;
    }

    #region Tool_ESC_GetPortNameStructures

    [StructLayout(LayoutKind.Sequential)]
    public struct GFX_ESCAPE_HEADER_T
    {
        public uint ulReserved;
        public uint ulMinorInterfaceVersion;
        public uint uiMajorEscapeCode;
        public uint uiMinorEscapeCode;
    }

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


    [StructLayout(LayoutKind.Sequential)]
    internal class EscapeData_RegisterOperation
    {
        public GFX_ESCAPE_HEADER header;
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 12 /*Size of escape data structure*/)]
        public byte[] dataBytes;
    }
    [StructLayout(LayoutKind.Sequential)]
    internal class MMIOArgs
    {
        public uint cmd;
        public uint offset;
        public uint value;
    }
    [StructLayout(LayoutKind.Sequential)]
    internal struct D3DKMT_ESCAPE
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
    internal struct D3DKMT_CLOSEADAPTER
    {
        public UInt32 hAdapter;
    }
    [StructLayout(LayoutKind.Sequential)]
    internal struct GFX_ESCAPE_HEADER
    {
        public uint Size;
        public uint CheckSum;
        public uint EscapeCode;
        public uint Reserved;
    }
    [StructLayout(LayoutKind.Sequential)]
    internal struct D3DKMT_OPENADAPTERFROMHDC
    {
        public IntPtr hDc;
        public UInt32 hAdapter;
        public LUID AdapterLuid;
        public UInt32 VidPnSourceId;
    }
}
