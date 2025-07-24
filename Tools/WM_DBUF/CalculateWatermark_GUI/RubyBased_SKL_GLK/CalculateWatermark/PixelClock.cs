using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using IgfxExtBridge_DotNet;
using Intel.Display.Automation.Common;
using Intel.Display.Automation.TestsCommon;
using Intel.Display.Automation.Logging;
using System.Runtime.InteropServices;

namespace CalculateWatermark
{
    class PixelClock
    {

        internal struct DISPLAYCONFIG_PATH_SOURCE_INFO
        {
            public LUID adapterId;
            public UInt32 id;
            public UInt32 modeInfoIdx;
            public UInt32 statusFlags;
        }

        public struct LUID
        {
            public uint LowPart;
            public int HighPart;
        }
        
        internal struct DISPLAYCONFIG_PATH_INFO
        {
            public DISPLAYCONFIG_PATH_SOURCE_INFO sourceInfo;
            public DISPLAYCONFIG_PATH_TARGET_INFO targetInfo;
            public UInt32 flags;
        }

      

    internal struct DISPLAYCONFIG_PATH_TARGET_INFO
    {
        public LUID adapterId;
        public UInt32 id;
        public UInt32 modeInfoIdx;
        public DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY outputTechnology;
        public DISPLAYCONFIG_ROTATION rotation;
        public DISPLAYCONFIG_SCALING scaling;
        public DISPLAYCONFIG_RATIONAL refreshRate;
        public DISPLAYCONFIG_SCANLINE_ORDERING scanlineOrdering;
        public bool targetAvailable;
        public UInt32 statusFlags;
    }

    internal struct DISPLAYCONFIG_RATIONAL
    {
        public UInt32 Numerator;
        public UInt32 Denominator;
    }
    internal enum DISPLAYCONFIG_SCALING : uint
    {
        DISPLAYCONFIG_SCALING_IDENTITY = 1,
        DISPLAYCONFIG_SCALING_CENTERED = 2,
        DISPLAYCONFIG_SCALING_STRETCHED = 3,
        DISPLAYCONFIG_SCALING_ASPECTRATIO_CENTEREDMAX = 4,
        DISPLAYCONFIG_SCALING_CUSTOM = 5,
        DISPLAYCONFIG_SCALING_PREFERRED = 128,
        DISPLAYCONFIG_SCALING_FORCE_UINT32 = 0xFFFFFFFF
    }


    internal enum DISPLAYCONFIG_SCANLINE_ORDERING : uint
    {
        DISPLAYCONFIG_SCANLINE_ORDERING_PROGRESSIVE = 1,
        DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED = 2,
        DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED_UPPERFIELDFIRST = DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED,
        DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED_LOWERFIELDFIRST = 3,
        DISPLAYCONFIG_SCANLINE_ORDERING_FORCE_UINT32 = 0xFFFFFFFF
    }

    internal enum DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY : uint
    {
        DISPLAYCONFIG_OUTPUT_TECHNOLOGY_HD15 = 0,
        DISPLAYCONFIG_OUTPUT_TECHNOLOGY_SVIDEO = 1,
        DISPLAYCONFIG_OUTPUT_TECHNOLOGY_COMPOSITE_VIDEO = 2,
        DISPLAYCONFIG_OUTPUT_TECHNOLOGY_COMPONENT_VIDEO = 3,
        DISPLAYCONFIG_OUTPUT_TECHNOLOGY_DVI = 4,
        DISPLAYCONFIG_OUTPUT_TECHNOLOGY_HDMI = 5,
        DISPLAYCONFIG_OUTPUT_TECHNOLOGY_LVDS = 6,
        DISPLAYCONFIG_OUTPUT_TECHNOLOGY_D_JPN = 8,
        DISPLAYCONFIG_OUTPUT_TECHNOLOGY_SDI = 9,
        DISPLAYCONFIG_OUTPUT_TECHNOLOGY_DISPLAYPORT_EXTERNAL = 10,
        DISPLAYCONFIG_OUTPUT_TECHNOLOGY_DISPLAYPORT_EMBEDDED = 11,
        DISPLAYCONFIG_OUTPUT_TECHNOLOGY_UDI_EXTERNAL = 12,
        DISPLAYCONFIG_OUTPUT_TECHNOLOGY_UDI_EMBEDDED = 13,
        DISPLAYCONFIG_OUTPUT_TECHNOLOGY_SDTVDONGLE = 14,
        DISPLAYCONFIG_OUTPUT_TECHNOLOGY_INTERNAL = 0x80000000,
        DISPLAYCONFIG_OUTPUT_TECHNOLOGY_FORCE_UINT32 = 0xFFFFFFFF
    }

    internal enum DISPLAYCONFIG_ROTATION : uint
    {
        DISPLAYCONFIG_ROTATION_IDENTITY = 1,
        DISPLAYCONFIG_ROTATION_ROTATE90 = 2,
        DISPLAYCONFIG_ROTATION_ROTATE180 = 3,
        DISPLAYCONFIG_ROTATION_ROTATE270 = 4,
        DISPLAYCONFIG_ROTATION_FORCE_UINT32 = 0xFFFFFFFF
    }

        internal struct DISPLAYCONFIG_MODE_INFO
        {
            public DISPLAYCONFIG_MODE_INFO_TYPE infoType;
            public UInt32 id;
            public LUID adapterId;
            public ModeUnion mode;
        }

        [StructLayout(LayoutKind.Explicit)]
        internal struct ModeUnion
        {
            [FieldOffset(0)]
            public DISPLAYCONFIG_TARGET_MODE targetMode;
            [FieldOffset(0)]
            public DISPLAYCONFIG_SOURCE_MODE sourceMode;
        }

        internal struct DISPLAYCONFIG_SOURCE_MODE
        {
            public UInt32 width;
            public UInt32 height;
            public DISPLAYCONFIG_PIXELFORMAT pixelFormat;
            public POINTL position;
        }

        internal struct POINTL
        {
            public int px;
            public int py;
        }

        internal enum DISPLAYCONFIG_PIXELFORMAT : uint
        {
            DISPLAYCONFIG_PIXELFORMAT_8BPP = 1,
            DISPLAYCONFIG_PIXELFORMAT_16BPP = 2,
            DISPLAYCONFIG_PIXELFORMAT_24BPP = 3,
            DISPLAYCONFIG_PIXELFORMAT_32BPP = 4,
            DISPLAYCONFIG_PIXELFORMAT_FORCE_UINT32 = 0xffffffff
        }

        internal struct DISPLAYCONFIG_TARGET_MODE
        {
            public DISPLAYCONFIG_VIDEO_SIGNAL_INFO targetVideoSignalInfo;
        }

        internal struct DISPLAYCONFIG_VIDEO_SIGNAL_INFO
        {
            public UInt64 pixelRate;
            public DISPLAYCONFIG_RATIONAL hSyncFreq;
            public DISPLAYCONFIG_RATIONAL vSyncFreq;
            public DISPLAYCONFIG_2DREGION activeSize;
            public DISPLAYCONFIG_2DREGION totalSize;
            public UInt32 videoStandard;
            public DISPLAYCONFIG_SCANLINE_ORDERING scanLineOrdering;
        }

        internal struct DISPLAYCONFIG_2DREGION
        {
            public UInt32 cx;
            public UInt32 cy;
        }
        internal enum DISPLAYCONFIG_MODE_INFO_TYPE : uint
        {
            DISPLAYCONFIG_MODE_INFO_TYPE_SOURCE = 1,
            DISPLAYCONFIG_MODE_INFO_TYPE_TARGET = 2,
            DISPLAYCONFIG_MODE_INFO_TYPE_FORCE_UINT32 = 0xFFFFFFFF
        }

        internal enum DISPLAYCONFIG_TOPOLOGY_ID : uint
        {
            DISPLAYCONFIG_TOPOLOGY_INTERNAL = 0x00000001,
            DISPLAYCONFIG_TOPOLOGY_CLONE = 0x00000002,
            DISPLAYCONFIG_TOPOLOGY_EXTEND = 0x00000004,
            DISPLAYCONFIG_TOPOLOGY_EXTERNAL = 0x00000008,
            DISPLAYCONFIG_TOPOLOGY_NULL = 0x00000000,
            DISPLAYCONFIG_TOPOLOGY_FORCE_UINT32 = 0xFFFFFFFF
        }

        [DllImport("user32.dll", SetLastError = true)]
        internal static extern int QueryDisplayConfig(UInt32 Flags, ref UInt32 pNumPathArrayElements, [Out] DISPLAYCONFIG_PATH_INFO[] pPathInfoArray, ref UInt32 pNumModeInfoArrayElements, [Out] DISPLAYCONFIG_MODE_INFO[] pModeInfoArray, DISPLAYCONFIG_TOPOLOGY_ID pCurrentTopologyId);

        internal enum QDCFlags
        {
            QDC_ALL_PATHS = 0x00000001,
            QDC_ONLY_ACTIVE_PATHS = 0x00000002,
            QDC_DATABASE_CURRENT = 0x00000004
        }

        [DllImport("user32.dll", SetLastError = true)]
        internal static extern int GetDisplayConfigBufferSizes(UInt32 Flags, ref UInt32 pNumPathArrayElements, ref UInt32 pNumModeInfoArrayElements);

        internal enum QDC_SDC_StatusCode
        {
            SUCCESS = 0,
            ERROR_INVALID_PARAMETER = 87,
            ERROR_NOT_SUPPORTED = 51,
            ERROR_ACCESS_DENIED = 5,
            ERROR_GEN_FAILURE = 31,
            ERROR_INSUFFICIENT_BUFFER = 122
        }

        public double GetCurrentMode(uint argWinMonitorID)
        {

            double pixelClock = 0;
            int returnVal;
            UInt32 numPathArrayElements = 0, numModeInfoArrayElements = 0;
            returnVal = GetDisplayConfigBufferSizes((uint)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, ref numModeInfoArrayElements);
            DISPLAYCONFIG_PATH_INFO[] pathInfo = new DISPLAYCONFIG_PATH_INFO[numPathArrayElements];
            DISPLAYCONFIG_MODE_INFO[] modeInfo = new DISPLAYCONFIG_MODE_INFO[numModeInfoArrayElements];
            DISPLAYCONFIG_TOPOLOGY_ID topologyId = DISPLAYCONFIG_TOPOLOGY_ID.DISPLAYCONFIG_TOPOLOGY_NULL;
            returnVal = QueryDisplayConfig((UInt32)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, pathInfo,
            ref numModeInfoArrayElements, modeInfo, topologyId);
            //SimpleLogger.Info(string.Format("Return value of QDC call : {0}", returnVal));
            //SimpleLogger.Info(string.Format("Return value of QDC call : {0}", returnVal));
            if (returnVal != (int)QDC_SDC_StatusCode.SUCCESS)
            {
              //  SimpleLogger.Info("Failed to fetch mode!");
                return 0;
            }
          
            for (int eachModeInfo = 0; eachModeInfo < modeInfo.Length; eachModeInfo++)
            {
                double tempPixelClock = Convert.ToDouble(modeInfo[eachModeInfo].mode.targetMode.targetVideoSignalInfo.pixelRate / 1000);
                //System.Windows.Forms.MessageBox.Show(string.Format("Pixel clock for 0x{0} is {1}", modeInfo[eachModeInfo].id.ToString("X"), tempPixelClock));  
                
                if ((modeInfo[eachModeInfo].id & 0xFFFFF) == argWinMonitorID)
                {
                    pixelClock = Convert.ToDouble(modeInfo[eachModeInfo].mode.targetMode.targetVideoSignalInfo.pixelRate / 1000);
                }
            }

            return pixelClock;
        }
    }
}
