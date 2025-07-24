using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    #region data structure for parsing panel brightness control data (Class: PanelBLCInfo)
    public enum NonPnPDriverService
    {
        Undefined,
        Install,
        UnInstall,
        Disable,
        Enable,
        Status,
        VerifyDriverUpdate
    }

    public enum PanelBLCFunctions
    {
        NotifyEvent,
        AuxAccessStatus,
        SetBrighthness,
        GetBrighthness,
        GetBrighthnessCaps,
        PanelBlcPathEnableStatus
    }

    public enum PanelBLCEventName
    {
        IGD_EVENT_UNDEFINED,
        IGD_PANEL_POWER_OFF,
        IGD_PANEL_POWER_ON,
        IGD_DRIVER_UNLOAD,
        IGD_DRIVER_LOADED,
        IGD_SYSTEM_D3_D4,
        IGD_SYSTEM_D0,
        IGD_BACKLIGHT_ON,
        IGD_BACKLIGHT_OFF
    }

    public enum PanelBLCEventType
    {
        IGD_EVENT_UNDEFINED,
        IGD_EVENT_TYPE_SINGLE_EVENT,
        IGD_EVENT_TYPE_PRE_EVENT,
        IGD_EVENT_TYPE_POST_EVENT
    }

    public enum PanelBLCIGDStatus
    {
        IGD_UNDEFINED,
        IGD_SUCCESS,
        IGD_UNSUCCESSFUL,
        IGD_INVALID_PARAMETER,
        IGD_CHANNEL_BUSY,
        IGD_INVALID_REQUEST,
        IGD_NOT_READY
    }

    public class NotifyEvent
    {
        public PanelBLCEventName EventName;
        public PanelBLCEventType EventType;
        public bool Optional;
        public Int64 TimeStamp;
    }

    public class AuxAccessStatus
    {
        public PanelBLCIGDStatus AuxStatus;
    }

    public class SetBrighthness
    {
        public int BrightnessValue;
        public Int64 TimeStamp;
    }

    public class GetBrighthness
    {
        public int BrightnessValue;
        public Int64 TimeStamp;
    }

    public class GetBrighthnessCaps
    {
        public int BrightnessCaps;
        public Int64 TimeStamp;
    }

    public class PanelBlcPathEnableStatus
    {
        public bool Status;
    }

    public class PanelBLCData
    {
        public NotifyEvent PanelNotifyEvent;
        public AuxAccessStatus PanelAuxAccess;
        public SetBrighthness PanelSetBrightness;
        public GetBrighthness PanelGetBrightness;
        public GetBrighthnessCaps PanelBrightnessCaps;
        public PanelBlcPathEnableStatus PathEnableStatus;
    }

    public class PanelDriverInstallUnInstallParam
    {
        public string DriverpackagePath;
        public string RegKeyName;
        public string DriverBinaryName;
        public string INFFileName;
    }

    public class PanelDriverAccessParam
    {
        public string DriverStringPattern;
    }

    public class PanelDeviceDriverParam
    {
        public NonPnPDriverService ServiceType;
        public PanelDriverInstallUnInstallParam InstallParam;
        public PanelDriverAccessParam AccessParam;
    }

    #endregion

    #region data structure for panel brightness control (Class: PanelBrightnessControl)

    public enum PanelGetService
    {
        Undefined,
        GetCurrentBrightness,
    }

    public enum PanelSetService
    {
        Undefined,
        SerBrightness,
    }

    public class SetBrightnessParam
    {
        public PanelSetService ServiceType;
        public ulong Timeout; //In Sec
        public ushort Brightness; //In percent
    }

    public class GetBrightnessParam
    {
        public PanelGetService ServiceType;

    }

    #endregion
}
