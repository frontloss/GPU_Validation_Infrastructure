using System;
using System.Runtime.InteropServices;
namespace Intel.VPG.Display.Automation
{
    public class ULT_FW_EscapeParams
    {
        public const int MAX_PLANES = 13;

        public ULT_ESCAPE_CODE ULT_Escape_Type { get; set; }
        public object driverEscapeData { get; set; }

        public ULT_FW_EscapeParams(ULT_ESCAPE_CODE EscapeType, object EscapeData)
        {
            ULT_Escape_Type = EscapeType;
            driverEscapeData = EscapeData;
        }
    }

    public enum ULT_ESCAPE_CODE
    {
        ULT_ESC_ENABLE_ULT = 0,     // Enable Disable the ULT mode
        ULT_ESC_ENABLE_DISABLE_FEATURE,     // Eanble Disable particular feature in ULT Mode
        ULT_ESC_GET_SYSTEM_INFO,    // Get System Info. functions
        ULT_ESC_ENUM_DEVICE,        // Enumerate Display Devices
        ULT_DEVICE_CONNECTIVITY,    // Get Set the HPD state of a DispUID
        ULT_ESC_GET_SET_EDID,       // Get Set the EDID of a DispUID
        ULT_CREATE_RESOURCE,        // Allocate the Surface
        ULT_FREE_RESOURCE,          // Freeup the allocated resource
        ULT_SET_SRC_ADDRESS,        // MMIO flip
        ULT_GET_MPO_CAPS,           // Get the MPO capability
        ULT_MPO_GROUP_CAPS,         // Get the MPO Group caps
        ULT_CHECK_MPO,              // Check MPO DDI
        ULT_SET_SRC_ADD_MPO,        // MPO flip
        ULT_ESC_SET_DPCD_INFO,  
        ULT_ESC_GET_SET_SIMULATE_DEVICE,
        // MAX_ULT_FUNCTIONS should be the last value in this enum
        MAX_ULT_FW_FUNCTIONS
    }

    public enum ULT_Return_Codes : uint
    {
        ULT_STATUS_SUCCESS = 0x00000000,
        ULT_STATUS_FAILURE = 0x00000001,
        ULT_STATUS_FW_NOT_ENABLED = 0x00000002,
        ULT_STATUS_FEATURE_NOT_ENABLED = 0x00000004,
        ULT_STATUS_ERROR_SIZE_MISMATCH = 0x00000008,
        ULT_STATUS_ERROR_INVALID_FEATURE = 0x00000010,
        ULT_STATUS_ERROR_INVALID_PARAMETER = 0x00000020,
        ULT_STATUS_ERROR_PARAM_NULL_POINTER = 0x00000040,
        ULT_STATUS_ERROR_FUNC_NULL_POINTER = 0x00000080,
        ULT_STATUS_ERROR_MEMORY_ALLOCATION = 0x00000100,
        ULT_STATUS_ERROR_DEV_SIM_ATTACH_ON_ATTACH = 0x00000200,
        ULT_STATUS_ERROR_DEV_SIM_DETACH_WITHOUT_ATTACH = 0x00000400,
        ULT_STATUS_ERROR_NO_DPCD_DATA = 0x00000800,
    }

    #region ULT_ESC_ENABLE_ULT
    public enum ULT_OP_TYPE
    {
        OP_GET,
        OP_SET,
    }

    public enum ULT_ESC_ENABLE_DISABLE_ULT_FEATURE
    {
        ULT_FEATURE_PRIVATE_FLIP,
        ULT_FEATURE_PRIVATE_MPOFLIP,
        ULT_FEATURE_DEV_SIM
    }
    // ULT_ESC_ENABLE_ULT
    [StructLayout(LayoutKind.Sequential, Pack = 1 /*To allocate 1 byte for char/bool*/)]
    public class ULT_ESC_ENABLE_ULT_ARG
    {
        public ULT_ESCAPE_CODE eULTEscapeCode;
        public uint dwRetErrorCode;
        public uint ulDataSize;
        public uint ulEscapeDataSize;

        [MarshalAs(UnmanagedType.I1)]
        public bool bEnableULT;// Enable the ULT mode in Gfx Driver
        public uint ulBufferSize;// Size of the Buffer
        public byte Buffer; // Security cookie. WIP

        public uint ucMajVer;       // Max Version Number
        public uint ucMinVer;       // Min Version Number
    }

    // ULT_ESC_ENABLE_ULT_Feature
    [StructLayout(LayoutKind.Sequential, Pack = 1 /*To allocate 1 byte for char/bool*/)]
    public class ULT_ESC_ENABLE_DISABLE_FEATURE_ARGS
    {
        public ULT_ESCAPE_CODE eULTEscapeCode;
        public uint dwRetErrorCode;
        public uint ulDataSize;
        public uint ulEscapeDataSize;

        [MarshalAs(UnmanagedType.I1)]
        public bool bEnableFeature;// Enable the ULT mode in Gfx Driver
        public ULT_ESC_ENABLE_DISABLE_ULT_FEATURE eFeatureEnable; // App needs to set these flags in Disable ULT Call
    }

    #endregion

    #region ULT_CREATE_RESOURCE

    //Rource management
    public enum ULT_PIXELFORMAT
    {
        SB_UNINITIALIZED = 0,   // use default pixel format in this case for setmode (e.g. XP might always set this)
        // SB_8BPP_INDEXED for 8bpp, SB_B5G6R5X0 for 16bpp, SB_B8G8R8X8 for 32bpp
        //Keep in the order of increasing BPP
        //Update min, max below if any other format is added                
        SB_8BPP_INDEXED,        // for 8bpp
        //Keep in the order of increasing BPP
        //Update min, max below if any other format is added                
        SB_B5G6R5X0,            // for 16bpp   
        //Keep in the order of increasing BPP
        //Update min, max below if any other format is added                
        SB_B8G8R8X8,            // for 32bpp (default)
        SB_B8G8R8A8,
        SB_R8G8B8X8,
        SB_R8G8B8A8,
        SB_R10G10B10X2,         // for 32bpp 10bpc
        SB_R10G10B10A2,         // for 32bpp 10bpc
        SB_B10G10R10X2,         // for 32bpp 10bpc
        SB_B10G10R10A2,         // for 32bpp 10bpc

        SB_R10G10B10A2_XR_BIAS, // for 32bpp 10bpc, XR BIAS format (used by Win7)
        //Keep in the order of increasing BPP
        //Update min, max below if any other format is added                
        SB_R16G16B16X16F,       // for 64bpp, 16bit floating
        //Keep in the order of increasing BPP
        //Update min, max below if any other format is added                
        //Adding formats used ONLY for MPO, adding at the last to reduce impact
        //Macros below will be updated for them only where it is really required
        SB_MAX_PIXELFORMAT, // Last one - just for internal bitmask usage          
        SB_NV12YUV420,
        SB_YUV422,
    }
    public enum ULT_TILE_FORMATS
    {
        ULT_TILE_FORMAT_W = 1,
        ULT_TILE_FORMAT_X = 2,
        ULT_TILE_FORMAT_Y = 4,
        ULT_TILE_FORMAT_Yf = 8,
        ULT_TILE_FORMAT_Ys = 16
    }
    // ULT_CREATE_RESOURCE
    [StructLayout(LayoutKind.Sequential, Pack = 1 /*To allocate 1 byte for char/bool*/)]
    public class ULT_CREATE_RES_ARGS
    {
        public ULT_ESCAPE_CODE eULTEscapeCode;
        public uint dwRetErrorCode;
        public uint ulDataSize;
        public uint ulEscapeDataSize;

        public ULT_PIXELFORMAT Format; // Surface format
        [MarshalAs(UnmanagedType.I1)]
        public bool AuxSurf;
        public ULT_TILE_FORMATS TileFormat;
        public uint ulBaseWidth;  // Surface Width
        public uint ulBaseHeight; // Surface Height

        //Out parameters
        public UInt64 pGmmBlock; //To be used in the Sesource address calls
        public UInt64 pUserVirtualAddress; //For the app to access the ubuffer using CPU
        public UInt64 u64SurfaceSize;
        public uint ulPitch;
    }

    #endregion

    #region ULT_FREE_RESOURCE

    // ULT_FREE_RESOURCE
    [StructLayout(LayoutKind.Sequential, Pack = 1 /*To allocate 1 byte for char/bool*/)]
    public class ULT_FREE_RES_ARGS
    {
        public ULT_ESCAPE_CODE eULTEscapeCode;
        public uint dwRetErrorCode;
        public uint ulDataSize;
        public uint ulEscapeDataSize;
        public UInt64 pGmmBlock;
    }

    #endregion

    #region ULT_SET_SRC_ADDRESS

    public enum ULT_SETVIDPNSOURCEADDRESS_FLAGS
    {
        ModeChange = 1,
        FlipImmediate = 2,
        FlipOnNextVSync = 4,
        FlipStereo = 8,
        FlipStereoTemporaryMono = 16,
        FlipStereoPreferRight = 32,
        SharedPrimaryTransition = 64
    }
    // ULT_SET_SRC_ADDRESS
    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public class ULT_ESC_SET_SRC_ADD_ARGS
    {
        public ULT_ESCAPE_CODE eULTEscapeCode;
        public uint dwRetErrorCode;
        public uint ulDataSize;
        public uint ulEscapeDataSize;

        public ULT_SETVIDPNSOURCEADDRESS_FLAGS Flags;//IN ULT_SETVIDPNSOURCEADDRESS_FLAGS Flags;
        public uint ulSrcID;    // The Vidpn source ID
        public UInt64 pGmmBlock;  // The Surface allocated in create resource call
        public uint ulDuration; // the Duarion parameter for entering 48 Hz
    }
    #endregion

    #region MPO_Group_Caps

    //MPO
    [StructLayout(LayoutKind.Sequential)]
    public struct ULT_MPO_CAPS
    {
        public uint uiMaxPlanes;
        public uint uiNumCapabilityGroups;
    }

    // ULT_GET_MPO_CAPS
    [StructLayout(LayoutKind.Sequential)]
    public class ULT_ESC_MPO_CAPS_ARGS
    {
        //In Params
        public ULT_ESCAPE_CODE eULTEscapeCode;
        public uint dwRetErrorCode;
        public uint ulDataSize;
        public uint ulEscapeDataSize;

        public uint ulVidpnSourceID;

        //Out Params
        public ULT_MPO_CAPS stMPOCaps;
    }

    [StructLayout(LayoutKind.Sequential)]
    public class ULT_MPO_GROUP_CAPS_ARGS
    {
        //Need not Escape code inside this as UMD_GENERAL_ESCAPE_BUFFER of which this structure //would be part will have it.
        //In Params
        public ULT_ESCAPE_CODE eULTEscapeCode;
        public uint dwRetErrorCode;
        public uint ulDataSize;
        public uint ulEscapeDataSize;

        public uint ulVidpnSourceID;
        public uint uiGroupIndex;

        //Out Params
        public ULT_MPO_GROUP_CAPS stMPOGroupCaps;
    }
    [StructLayout(LayoutKind.Sequential)]
    public struct ULT_MPO_GROUP_CAPS
    {
        public uint uiMaxPlanes;
        public uint uiMaxStretchFactorNum;
        public uint uiMaxStretchFactorDenm;
        public uint uiMaxShrinkFactorNum;
        public uint uiMaxShrinkFactorDenm;
        public uint uiOverlayFtrCaps;
        public uint uiStereoCaps;
    }
    #endregion

    #region Check_MPO

    //Uncomment this part of code
    // ULT_CHECK_MPO
    //  typedef SB_MPO_CHECKMPOSUPPORT_ARGS ULT_CHECK_MPO_ARG, *PULT_CHECK_MPO_ARG;

    //All the aspects of the Plane that SoftBIOS has to validate for support - includes OS given info and internal context info for that plane.
    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO
    {
        public uint uiLayerIndex; // top mostplane is layer 0, 0 based index
        //Do we need Surface Block?
        [MarshalAs(UnmanagedType.I1)]
        public bool bEnabled;
        public ULT_MPO_PLANE_ATTRIBUTES stPlaneAttributes;
        //The below are those information which OS doesn't directly give as part of checkMPO call but we need to find out internally before calling SoftBIOS.
        public ULT_SURFACE_MEM_OFFSET_INFO stSurfaceMemInfo;
        public ULT_PIXELFORMAT eSBPixelFormat;
        [MarshalAs(UnmanagedType.I1)]
        public bool bIsAsyncMMIOFlip;  //Not be used currently for MPO as it is always Synchronous flips..
    }
    public enum ULT_SURFACE_MEMORY_TYPE
    {
        SURFACE_MEMORY_INVALID = 0,
        SURFACE_MEMORY_LINEAR = 1,                      // Surface uses linear momory
        SURFACE_MEMORY_TILED = 2,                       // Surface uses tiled memory
        SURFACE_MEMORY_X_TILED = SURFACE_MEMORY_TILED,
        SURFACE_MEMORY_Y_LEGACY_TILED = 4,              // Surface uses Legacy Y tiled memory (Gen9+)
        SURFACE_MEMORY_Y_F_TILED = 8,                   // Surface uses Y F tiled memory 
    }
    // Struct representing surface memory offset data
    // Used by SB_SETDISPLAYSTART_ARGS
    [StructLayout(LayoutKind.Sequential)]
    public class ULT_SURFACE_MEM_OFFSET_INFO//Uncomment data inside
    {
        // Indicates surface memory type
        // Note: Based on this param SB will read & program
        // linear/tiled offset values
        // Indicates surface memory type
        public ULT_SURFACE_MEMORY_TYPE eSurfaceMemType;

        //union
        //{
        //    // Gen4 linear offset
        //    public uint ulLinearOffset;

        //    // Gen4 tiled offset
        //    struct
        //    {
        public uint ulTiledXOffset;
        public uint ulTiledYOffset;
        public uint ulTiledUVXOffset; // NV12 case
        public uint ulTiledUVYOffset; // NV12 case
        //    };
        //};

        public uint ulUVDistance;  // For NV12 surface, as of now nv12 cant come in normal flip path
        public uint ulAuxDistance; // Control surface Aux Offset. Will be 0 for non unified allocations, MP is abstracted from it
    }
    public enum SB_PIXELFORMAT
    {
        SB_UNINITIALIZED = 0,   // use default pixel format in this case for setmode (e.g. XP might always set this)
        // SB_8BPP_INDEXED for 8bpp, SB_B5G6R5X0 for 16bpp, SB_B8G8R8X8 for 32bpp
        //Keep in the order of increasing BPP
        //Update min, max below if any other format is added                
        SB_8BPP_INDEXED,        // for 8bpp
        //Keep in the order of increasing BPP
        //Update min, max below if any other format is added                
        SB_B5G6R5X0,            // for 16bpp   
        //Keep in the order of increasing BPP
        //Update min, max below if any other format is added                
        SB_B8G8R8X8,            // for 32bpp (default)
        SB_B8G8R8A8,
        SB_R8G8B8X8,
        SB_R8G8B8A8,
        SB_R10G10B10X2,         // for 32bpp 10bpc
        SB_R10G10B10A2,         // for 32bpp 10bpc
        SB_B10G10R10X2,         // for 32bpp 10bpc
        SB_B10G10R10A2,         // for 32bpp 10bpc

        SB_R10G10B10A2_XR_BIAS, // for 32bpp 10bpc, XR BIAS format (used by Win7)
        //Keep in the order of increasing BPP
        //Update min, max below if any other format is added                
        SB_R16G16B16X16F,       // for 64bpp, 16bit floating
        //Keep in the order of increasing BPP
        //Update min, max below if any other format is added                
        //Adding formats used ONLY for MPO, adding at the last to reduce impact
        //Macros below will be updated for them only where it is really required
        SB_MAX_PIXELFORMAT, // Last one - just for internal bitmask usage          
        SB_NV12YUV420,
        SB_YUV422,
    }

    //All aspects of the Path which needs to be validated - this would contain information from multiple planes in a path and corresponding Pipe\DisplayUID.
    [StructLayout(LayoutKind.Sequential)]
    public struct SB_MPO_CHECKMPOSUPPORT_PATH_INFO
    {
        public uint uiPlaneCount;
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 13)]
        public ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[] stMPOPlaneInfo; // sjm: max planes per pipe ? 
        //public char Reserved;// ucPipeIndex;
        //public uint Reserved1; //ulDisplayUID; //Only Pipe index should be sufficient but let's fill this also for implementation ease in SoftBIOS.
    }

    //Parent structure containing information on all paths which is being asked for MPO support. This should be the structure going to SoftBIOS for validation.
    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public class SB_MPO_CHECKMPOSUPPORT_ARGS
    {
        //In Params
        public ULT_ESCAPE_CODE eULTEscapeCode;
        public uint dwRetErrorCode;
        public uint ulDataSize;
        public uint ulEscapeDataSize;

        public uint dwSourceID;//new field added.

        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 3)]
        public SB_MPO_CHECKMPOSUPPORT_PATH_INFO[] stCheckMPOPathInfo;      //_simi: replaced MAX_PATH with MAX_PIPES
        public uint ulNumPaths;
        public uint ulConfig;//Ideally SoftBIOS doesn't need this info, but providing it for basic level verification before going deeper and for any future needs.

        //Out Params
        [MarshalAs(UnmanagedType.I1)]
        public bool bSupported;
        public uint ulFailureReason; //We can define macros and store internally, if OS requests  this info we can give back later.
        public CHECKMPOSUPPORT_RETURN_INFO stMPOCheckSuppReturnInfo;
    }

    [StructLayout(LayoutKind.Sequential)]
    public class CHECKMPOSUPPORT_RETURN_INFO
    {
        public uint uiValue;
    }
    #endregion

    #region SET_SRC_ADD_MPO

    // ULT_SET_SRC_ADD_MPO
    [StructLayout(LayoutKind.Sequential)]
    public class ULT_SET_SRC_ADD_MPO_ARG
    {
        //In params
        public ULT_ESCAPE_CODE eULTEscapeCode;
        public uint dwRetErrorCode;
        public uint ulDataSize;
        public uint ulEscapeDataSize;

        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 13)]
        public MPO_FLIP_PLANE_INFO[] stDxgkMPOPlaneArgs;
        public uint ulNumPlanes;
        public ULT_SETVIDPNSOURCEADDRESS_FLAGS ulFlags;
        public uint dwSourceID;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct MPO_FLIP_PLANE_INFO
    {
        public uint uiLayerIndex;
        [MarshalAs(UnmanagedType.I1)]
        public bool bEnabled;
        [MarshalAs(UnmanagedType.I1)]
        public bool bAffected;

        public uint uiAllocationSegment;
        public uint AllocationAddress;
        public UInt64 hAllocation;
        public ULT_MPO_PLANE_ATTRIBUTES stPlaneAttributes;
    }

    public enum ULT_MPO_FLIP_FLAGS
    {
        DEFAULT = 0,
        VerticalFlip = 1,
        HorizontalFlip = 2,
    }

    //Matches Kernel Flip Attribute..
    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public class ULT_MPO_PLANE_ATTRIBUTES
    {
        public uint uiMPOFlags; //(ULT_MPO_FLIP_FLAGS use this for future use.)
        public ULT_M_RECT MPOSrcRect;
        public ULT_M_RECT MPODstRect;
        public ULT_M_RECT MPOClipRect;
        public ULT_MPO_ROTATION eMPORotation;
        public ULT_MPO_PLANE_ORIENTATION eHWOrientation;
        public ULT_MPO_BLEND_VAL eMPOBlend;
        //Commenting the filters part as of now since it is not in latest Spec but it might come //back, so it can be commented out for now.
        //UINT	uiMPONumFilters;
        //MPO_FILTER_VAL	stFilterVal[MAX_FILTERS];
        public ULT_MPO_VIDEO_FRAME_FORMAT eMPOVideoFormat;
        public uint uiMPOYCbCrFlags;

        //Not in Dx9 Spec
        public ULT_MPO_STEREO_FORMAT eMPOStereoFormat;
        [MarshalAs(UnmanagedType.I1)]
        public bool bMPOLeftViewFrame0; //? Do we want to keep bool
        [MarshalAs(UnmanagedType.I1)]
        public bool bMPOBaseViewFrame0; //? Do we want to keep bool
        public ULT_MPO_STEREO_FLIP_MODE eMPOStereoFlipMode;
        public ULT_MPO_STRETCH_QUALITY eStretchQuality;
        //Currently Driver may not use this info.
        public uint uiDirtyRectCount;
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 8)]
        public ULT_M_RECT[] DIRTYRECTS; //Making it an array as sending as //pointer is not possible.
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct ULT_M_RECT
    {
        public uint left;
        public uint top;
        public uint right;
        public uint bottom;
    }


    public enum ULT_MPO_ROTATION
    {
        MPO_ROTATION_IDENTITY = 1,
        MPO_ROTATION_90 = 2,
        MPO_ROTATION_180 = 3,
        MPO_ROTATION_270 = 4

    }

    // As per OS rotation Values, starting from 0
    public enum ULT_MPO_PLANE_ORIENTATION
    {
        MPO_ORIENTATION_DEFAULT = 0,                        // Default value
        MPO_ORIENTATION_0 = MPO_ORIENTATION_DEFAULT,            // 0 degree
        MPO_ORIENTATION_90 = 1,                             // 90 degree, supported Gen9 onwards
        MPO_ORIENTATION_180 = 2,                            // 180 degree
        MPO_ORIENTATION_270 = 3,                            // 270 degree, supported Gen9 onwards
    }

    //Use the below definition..
    public enum ULT_MPO_BLEND_VAL
    {
        None = 0,
        AlphaBlend = 1
    }
    //Not in Dx9 spec
    //Matches Kernel flip attribute.
    public enum ULT_MPO_VIDEO_FRAME_FORMAT
    {
        MPO_VIDEO_FRAME_FORMAT_PROGRESSIVE = 0x0,
        MPO_VIDEO_FRAME_FORMAT_INTERLACED_TOP_FIELD_FIRST = 0x1,
        MPO_VIDEO_FRAME_FORMAT_INTERLACED_BOTTOM_FIELD_FIRST = 0x2
    }
    //Not in Dx9 Spec
    //Matches Kernel flip attribute.
    public enum ULT_MPO_STEREO_FORMAT
    {
        MPO_FORMAT_MONO = 0,
        MPO_FORMAT_HOR = 1,
        MPO_FORMAT_VER = 2,
        MPO_FORMAT_SEPARATE = 3,
        MPO_FORMAT_ROW_INTERLEAVED = 5, //??????? 4 is missing ?????
        MPO_FORMAT_COLUMN_INTERLEAVED = 6,
        MPO_FORMAT_CHECKBOARD = 7
    }

    //Not in Dx9 Spec
    //Matches Kernel flip attribute.
    public enum ULT_MPO_STEREO_FLIP_MODE
    {
        MPO_FLIP_NONE = 0,
        MPO_FLIP_FRAME0 = 1,
        MPO_FLIP_FRAME1 = 2
    }

    public enum ULT_MPO_STRETCH_QUALITY
    {
        MPO_STRETCH_QUALITY_BILINEAR = 0x1, //Bilinear
        MPO_STRETCH_QUALITY_HIGH = 0x2 //Maximum
    }
    #endregion

    #region Device_Simulation

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct ULT_DEVICE_INFO
    {
        public uint OpType;         //Whether Get or Set
        [MarshalAs(UnmanagedType.I1)]
        public bool bAttach;      //HPD state of the Display

        public uint ulDisplayUID;  

        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 768)]
        public byte[] bDisplayEdid; // Applicable for attach or query for connected device. For detach, this field will be irrelevant.

        [MarshalAs(UnmanagedType.I1)]
        public bool bSimConnectionInLowPower; //If set, the action of attach or detach is deferred till low power mode.
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public class ULT_ESC_GET_SET_DEVICE_CONNECTIVITY_ARGS
    {
        //In params
        public ULT_ESCAPE_CODE eULTEscapeCode;
        public uint dwRetErrorCode;
        public uint ulDataSize;
        public uint ulEscapeDataSize;

        public uint ulNumDevices; //Number of Devices for simulation.

        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 20)]
        public ULT_DEVICE_INFO[] stDeviceInfo; // Device information of each device to be simulated. MAX_DDI is set to 5 today.
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public class ULT_ESC_DPCD_INFO
    {
        //In params
        public ULT_ESCAPE_CODE eULTEscapeCode;
        public uint dwRetErrorCode;
        public uint ulDataSize;
        public uint ulEscapeDataSize;

        public uint ulDisplayUID;
        public uint ulDPCDAddress;
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 512)]
        public byte[] bDPCDData;
        public uint ulSize;
    }

    /* ----- ULT Escape - "ULT_ESC_ENUM_DEVICE" ----- */
    public enum ULT_DISPLAY_TYPE
    {
        ULT_NULL_DISPLAY_TYPE = 0,
        ULT_CRT_TYPE,
        ULT_RESERVED_TYPE,
        ULT_DFP_TYPE,
        ULT_LFP_TYPE,
        ULT_MAX_DISPLAY_TYPES
    }
    public enum ULT_PORT_TYPE
    {
        ULT_NULL_PORT_TYPE = -1,
        ULT_ANALOG_PORT = 0,
        ULT_DVOA_PORT,
        ULT_DVOB_PORT,
        ULT_DVOC_PORT,
        ULT_DVOD_PORT,
        ULT_LVDS_PORT,
        ULT_RESERVED_PORT,
        ULT_INTHDMIB_PORT,
        ULT_INTHDMIC_PORT,
        ULT_INTHDMID_PORT,
        ULT_INT_DVI_PORT,
        ULT_INTDPA_PORT,
        ULT_INTDPB_PORT,
        ULT_INTDPC_PORT,
        ULT_INTDPD_PORT,
        //INTDPE_PORT, 
        ULT_TPV_PORT,
        ULT_INTMIPIA_PORT,
        ULT_INTMIPIC_PORT,
        ULT_MAX_PORTS
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct ULT_DISPLAY_DETAILS_ARGS
    {
        public uint ulDisplayUID;
        public ULT_DISPLAY_TYPE eDisplayType;
        [MarshalAs(UnmanagedType.I1)]
        public bool bExternalEncoderDriven;
        [MarshalAs(UnmanagedType.I1)]
        public bool bTPVDrivenEncoder;
        public ULT_PORT_TYPE ePortType;
        [MarshalAs(UnmanagedType.I1)]
        public bool bInternalPortraitPanel;
        public uint ulConnectorType;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public class ULT_ESC_ENUM_DEVICE_ARGS
    {
        //In params
        public ULT_ESCAPE_CODE eULTEscapeCode;
        public uint dwRetErrorCode;
        public uint ulDataSize;
        public uint ulEscapeDataSize;

        public uint ulNumDisplays;
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 36)]
        public ULT_DISPLAY_DETAILS_ARGS[] stDisplayDetailsArgs;//[MAX_DISPLAYS];
    }


    /* ----- ULT Escape - "ULT_ESC_GET_DEVICE_CONNECTIVITY" -----*/
    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public class ULT_ESC_GET_DEVICE_CONNECTIVITY_ARGS
    {
        //In params
        public ULT_ESCAPE_CODE eULTEscapeCode;
        public uint dwRetErrorCode;
        public uint ulDataSize;
        public uint ulEscapeDataSize;

        public uint ulDisplayUID;        //Display UID
        [MarshalAs(UnmanagedType.I1)]
        public bool bAttached;           //HPD state of the Display
    }

    #endregion
}