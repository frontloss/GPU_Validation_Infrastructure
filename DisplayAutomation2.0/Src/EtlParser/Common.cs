/**
* @file		Commons.cs
* @brief	Contains common definitions for all handlers
*
* @source   GfxInstrumentationAnalyzer\DisplayAnalysis
*/

namespace EtlParser
{
    public enum ANALYZE_LEVEL
    {
        GOOD_CASE = -1,
        LOG_ALWAYS = 0,
        CRITICAL = 1,
        ERROR = 2,
        WARNING = 3,
        INFO = 4,
        VERBOSE = 5,
    }
    public enum GFX_DBG_LEVEL
    {
        CRITICAL = (0x01),
        NORMAL = (0x02),
        VERBOSE = (0x04)
    }
    public enum DIAG_TYPE
    {
        CATASTROPHE = 0,
        ERROR,
        WARNING,
        INFO,
        VERBOSE
    }
    public enum DD_DIAGNOSTIC_SOURCE
    {
        // Collect data which will help us identify the cause and take preventive measures
        DD_DIAG_CAT_FAIL = 0x0,
        // Underrun, PipeIndex, UnderRunCount, NA, NA.
        DD_DIAG_CAT_PIPE_UNDER_RUN = (0x01 | DD_DIAG_CAT_FAIL),
        // Flip failure, Source ID, Pipe, NumPlanes, ErrorCode.
        DD_DIAG_CAT_FLIP_FAIL = (0x02 | DD_DIAG_CAT_FAIL),
        // EDID Read Failure, Target ID, Port, TBD, TBD.
        DD_DIAG_CAT_EDID_READ_FAIL = (0x03 | DD_DIAG_CAT_FAIL),


        // Error. Something failed and the end used saw the after effect(Flicker\Blank out). 
        // But the system is still stable
        DD_DIAG_ERR = (0x1 << 28),
        // Mode Set Failed, DisplayID, PipeIndex, X Res, Dot Clock.
        DD_DIAG_ERR_MODESET_FAIL = (0x01 | DD_DIAG_ERR),
        // Link Training Failed, DisplayID, Rate, TBD, TBD.
        DD_DIAG_ERR_LINK_TRAINING_FAIL = (0x02 | DD_DIAG_ERR),
        // Insufficient Dbuf in a flip, Pipe, Num Planes, Dbuf needed, Dbuf avilable
        DD_DIAG_ERR_INSUFFICIENT_DBUF = (0x01 | DD_DIAG_ERR),


        // Warning. Something failed. But the user didn't see the effect
        DD_DIAG_WRN = (0x2 << 28),
        // Insufficinet DBuf to enable the planes on a Display, PipeIndex, DBuf Needed, DBuf Available, N Planes.
        DD_DIAG_WRN_INSUFFICIENT_DBUF = (0x01 | DD_DIAG_WRN),


        // Info. Helpful debuf info. Routine data collection. 
        // Will get handly when debugging the CAT, ERR and WRN cases
        DD_DIAG_INF = (0x3 << 28),

        // Diagnostics related to the function execution time
        // Analyzer will use these clues to dig into the performance issues

        // Polled MMIO Read, Register, Mask, Value, TBD.
        DD_DIAG_INF_POLLED_READ = (0x001 | DD_DIAG_INF),
        // Delay introduced by stalling CPU, Delay time in us, TBD, TBD, TBD.
        DD_DIAG_INF_DELAY_STALL_CPU = (0x003 | DD_DIAG_INF),
        // Delay introduced by delaying thread, Delay time in us, TBD, TBD, TBD.
        DD_DIAG_INF_DELAY_EXECUTION_THREAD = (0x004 | DD_DIAG_INF),
        // DDI Entry, DDI, TBD, TBD, TBD.
        DD_DIAG_INF_DDI_ENTRY = (0x005 | DD_DIAG_INF),
        // DDI Exit, DDI, Status, TBD, TBD.
        DD_DIAG_INF_DDI_EXIT = (0x006 | DD_DIAG_INF),
        // DPC Entry, TBD, TBD, TBD, TBD.
        DD_DIAG_INF_DPC_ENTRY = (0x007 | DD_DIAG_INF),
        // DPC Exit, TBD, Status, TBD, TBD.
        DD_DIAG_INF_INSERT_DPC = (0x008 | DD_DIAG_INF),
        // Work Item Entry, TBD, TBD, TBD, TBD.
        DD_DIAG_INF_INSERT_WI = (0x009 | DD_DIAG_INF),
        // Work Item Exit, TBD, Status, TBD, TBD.
        DD_DIAG_INF_DPC_EXIT = (0x00A | DD_DIAG_INF),
        // Lock Entry, TBD, TBD, TBD, TBD.
        DD_DIAG_INF_WI_ENTRY = (0x00B | DD_DIAG_INF),
        // Lock Exit, TBD, Status, TBD, TBD.
        DD_DIAG_INF_WI_EXIT = (0x00C | DD_DIAG_INF),
        // Queue Work Item, TBD, TBD, TBD, TBD.
        DD_DIAG_INF_LOCK_ENTRY = (0x00D | DD_DIAG_INF),
        // Queue Work Item, TBD, TBD, TBD, TBD.
        DD_DIAG_INF_LOCK_EXIT = (0x00E | DD_DIAG_INF),


        // Flip Related diagnostics
        // Check MPO Passed, N Pipes, N Planes, TBD, TBD.
        DD_DIAG_INF_CHECK_MPO_PASSED = (0x10001 | DD_DIAG_INF),
        // Check MPO Failed, N Pipes, N Planes, Failing Plane, Reason_TBD.
        DD_DIAG_INF_CHECK_MPO_FAILED = (0x10002 | DD_DIAG_INF),
        // Insufficient Dbuf in a CheckMPO, Pipe, Num Planes, Dbuf needed, Dbuf avilable
        DD_DIAG_INF_INSUFFICIENT_DBUF = (0x10003 | DD_DIAG_INF),
    }
    public enum DD_DIAG_SOURCE_DDI
    {
        DDI_START_DEVICE = 100000,
        DDI_STOP_DEVICE,
        DDI_REMOVE_DEVICE,
        DDI_DISPATCH_IO_REQUEST,
        DDI_INTERRUPT_ROUTINE,
        DDI_DPC_ROUTINE,
        DDI_QUERY_CHILD_RELATIONS,
        DDI_QUERY_CHILD_STATUS,
        DDI_QUERY_DEVICE_DESCRIPTOR,
        DDI_SET_POWER_STATE,
        DDI_NOTIFY_ACPI_EVENT,
        DDI_RESET_DEVICE,
        DDI_UNLOAD,
        DDI_QUERY_INTERFACE,
        DDI_CONTROL_ETW_LOGGING,
        DDI_QUERYADAPTERINFO,
        DDI_CREATEDEVICE,
        DDI_CREATEALLOCATION,
        DDI_DESTROYALLOCATION,
        DDI_DESCRIBEALLOCATION,
        DDI_GETSTANDARDALLOCATIONDRIVERDATA,
        DDI_ACQUIRESWIZZLINGRANGE,
        DDI_RELEASESWIZZLINGRANGE,
        DDI_PATCH,
        DDI_SUBMITCOMMAND,
        DDI_PREEMPTCOMMAND,
        DDI_BUILDPAGINGBUFFER,
        DDI_SETPALETTE,
        DDI_SETPOINTERPOSITION,
        DDI_SETPOINTERSHAPE,
        DDI_RESETFROMTIMEOUT,
        DDI_RESTARTFROMTIMEOUT,
        DDI_ESCAPE,
        DDI_COLLECTDBGINFO,
        DDI_QUERYCURRENTFENCE,
        DDI_ISSUPPORTEDVIDPN,
        DDI_RECOMMENDFUNCTIONALVIDPN,
        DDI_ENUMVIDPNCOFUNCMODALITY,
        DDI_SETVIDPNSOURCEADDRESS,
        DDI_SETVIDPNSOURCEVISIBILITY,
        DDI_COMMITVIDPN,
        DDI_UPDATEACTIVEVIDPNPRESENTPATH,
        DDI_RECOMMENDMONITORMODES,
        DDI_RECOMMENDVIDPNTOPOLOGY,
        DDI_GETSCANLINE,
        DDI_STOPCAPTURE,
        DDI_CONTROLINTERRUPT,
        DDI_CREATEOVERLAY,
        DDI_DESTROYDEVICE,
        DDI_OPENALLOCATIONINFO,
        DDI_CLOSEALLOCATION,
        DDI_RENDER,
        DDI_PRESENT,
        DDI_UPDATEOVERLAY,
        DDI_FLIPOVERLAY,
        DDI_DESTROYOVERLAY,
        DDI_CREATECONTEXT,
        DDI_DESTROYCONTEXT,
        DDI_LINK_DEVICE,
        DDI_SETDISPLAYPRIVATEDRIVERFORMAT,
        DDI_RENDERKM,
        DDI_QUERYVIDPNHWCAPABILITY,
        DDISETPOWERCOMPONENTFSTATE,
        DDI_QUERYDEPENDENTENGINEGROUP,
        DDI_QUERYENGINESTATUS,
        DDI_RESETENGINE,
        DDI_STOP_DEVICE_AND_RELEASE_POST_DISPLAY_OWNERSHIP,
        DDI_SYSTEM_DISPLAY_ENABLE,
        DDI_SYSTEM_DISPLAY_WRITE,
        DDI_CANCELCOMMAND,
        DDI_GET_CHILD_CONTAINER_ID,
        DDIPOWERRUNTIMECONTROLREQUEST,
        DDI_SETVIDPNSOURCEADDRESSWITHMULTIPLANEOVERLAY,
        DDI_NOTIFY_SURPRISE_REMOVAL,
        DDI_GETNODEMETADATA,
        DDISETPOWERPSTATE,
        DDI_CONTROLINTERRUPT2,
        DDI_CHECKMULTIPLANEOVERLAYSUPPORT,
        DDI_CALIBRATEGPUCLOCK,
        DDI_FORMATHISTORYBUFFER,
        DDI_RENDERGDI,
        DDI_SUBMITCOMMANDVIRTUAL,
        DDI_SETROOTPAGETABLE,
        DDI_GETROOTPAGETABLESIZE,
        DDI_MAPCPUHOSTAPERTURE,
        DDI_UNMAPCPUHOSTAPERTURE,
        DDI_CHECKMULTIPLANEOVERLAYSUPPORT2,
        DDI_CREATEPROCESS,
        DDI_DESTROYPROCESS,
        DDI_SETVIDPNSOURCEADDRESSWITHMULTIPLANEOVERLAY2,
        DDI_POWERRUNTIMESETDEVICEHANDLE,
        DDI_SETSTABLEPOWERSTATE,
        DDI_SETVIDEOPROTECTEDREGION,
        DDI_CHECKMULTIPLANEOVERLAYSUPPORT3,
        DDI_SETVIDPNSOURCEADDRESSWITHMULTIPLANEOVERLAY3,
        DDI_POSTMULTIPLANEOVERLAYPRESENT,
        DDI_VALIDATEUPDATEALLOCATIONPROPERTY,
        DDI_CONTROLMODEBEHAVIOR,
        DDI_UPDATEMONITORLINKINFO,
        DDI_CREATEHWCONTEXT,
        DDI_DESTROYHWCONTEXT,
        DDI_CREATEHWQUEUE,
        DDI_DESTROYHWQUEUE,
        DDI_SUBMITCOMMANDTOHWQUEUE,
        DDI_SWITCHTOHWCONTEXTLIST,
        DDI_RESETHWENGINE,
        DDI_CREATEPERIODICFRAMENOTIFICATION,
        DDI_DESTROYPERIODICFRAMENOTIFICATION,
        DDI_SETTIMINGSFROMVIDPN,
        DDI_SETTARGETGAMMA,
        DDI_SETTARGETCONTENTTYPE,
        DDI_SETTARGETANALOGCOPYPROTECTION,
        DDI_SETTARGETADJUSTEDCOLORIMETRY,
        DDI_DISPLAYDETECTCONTROL,
        DDI_QUERYCONNECTIONCHANGE,
        DDI_EXCHANGEPRESTARTINFO,
        DDI_GETMULTIPLANEOVERLAYCAPS,
        DDI_GETPOSTCOMPOSITIONCAPS,
        DDI_OPM_GET_CERTIFICATESIZE,
        DDI_OPM_GET_CERTIFICATE,
        DDI_OPM_CREATEPROTECTEDOUTPUT,
        DDI_OPM_CREATEPROTECTEDOUTPUTFORNONLOCALDISPLAY,
        DDI_OPM_GET_RANDOMNUMBER,
        DDI_OPM_SET_SIGNINGKEYANDSEQUENCENUMBERS,
        DDI_OPM_GET_INFO,
        DDI_OPM_GET_COPPCOMPATIBLEINFO,
        DDI_OPM_CONFIGURE_PROTECTEDOUTPUT,
        DDI_OPM_DESTROY_PROTECTEDOUTPUT,
        DDI_I2C_TRANSMITDATATODISPLAY,
        DDI_I2C_RECEIVEDATAFROMDISPLAY,
        DDI_BLC_GETPOSSIBLEBRIGHTNESS,
        DDI_BLC_SET_BRIGHTNESS,
        DDI_BLC_GET_BRIGHTNESS,
        DDI_BLC_GET_BRIGHTNESS_CAPS,
        DDI_BLC_SET_BRIGHTNESS_STATE,
        DDI_BLC_GET_BACKLIGHT_REDUCTION,
        DDI_BLC_SET_BACKLIGHT_OPTIMIZATION,
        DDI_BLC_GET_NITRANGES,
        DDI_BLC_GET_BRIGHTNESS_CAPS3,
        DDI_BLC_GET_BRIGHTNESS3,
        DDI_BLC_SET_BRIGHTNESS3,
        DDI_BLC_SET_BACKLIGHT_OPTIMIZATION3,

        // special case for Work Item and DPC
        WORK_ITEM = 0x1000,
        DPC,
        ORPHAN_THREADS,
    }
    public class ParserConfig
    {
        public bool CommonEvents;   // bit 0
        public bool DbgMsg;
        public bool Diag;
        public bool Dpcd;
        public bool Flip;
        public bool Function;
        public bool Interrupt;
        public bool Mmio;
        public bool Vbi;
        public bool Dpst;
        public bool I2c;
        public bool Psr;
        public bool Detection;

        public ParserConfig(ulong config)
        {
            this.CommonEvents = (config & 0x1) == 0x1;
            this.DbgMsg = (config & 0x2) == 0x2;
            this.Diag = (config & 0x4) == 0x4;
            this.Dpcd = (config & 0x8) == 0x8;
            this.Flip = (config & 0x10) == 0x10;
            this.Function = (config & 0x20) == 0x20;
            this.Interrupt = (config & 0x40) == 0x40;
            this.Mmio = (config & 0x80) == 0x80;
            this.Vbi = (config & 0x100) == 0x100;
            this.Dpst = (config & 0x200) == 0x200;
            this.I2c = (config & 0x400) == 0x400;
            this.Psr = (config & 0x800) == 0x800;
            this.Detection = (config & 0x1000) == 0x1000;

        }
    }
    class Common
    {
    }
}
