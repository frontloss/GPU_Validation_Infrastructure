
// Imp: IOCTL Files shouldn't include any driver headers execept other IOCTL files and dependant files accessible to the APP world

#ifndef __COMMON_IOCTL_H__
#define __COMMON_IOCTL_H__

#define SIM_IOCTL_DEVTYPE 0x9000

#define SIM_IOCTL_BASEVAL 0x801

#define SIM_IOCTL_SIMINIT 0
#define SIM_IOCTL_SIMINITSIZE 50

#define SIM_IOCTL_COMMON 51
#define SIM_IOCTL_COMMONSIZE 50

#define SIM_IOCTL_DP 101
#define SIM_IOCTL_DPSIZE 50

#define SIM_IOCTL_HDMI 151
#define SIM_IOCTL_HDMISIZE 50

#define SIM_IOCTL_EDP 201
#define SIM_IOCTL_EDPSIZE 50

#pragma warning(disable : 4201)
#pragma warning(disable : 4214)

// This string size macro is defined with different names in SST_MST_Common and DPCoreIOCTLCommonDefs because of compilation issues.
// So beware modifying it. Modify at those other places too if needed
#define NAME_STR_SIZE 40
#define CCHDEVICENAME 32

#define SIMDRVDOS_DEVICE_NAME L"\\DosDevices\\SimDrvDosDev"

#define SIM_FILE_ACCESS (FILE_READ_ACCESS | FILE_WRITE_ACCESS)

#include "DPIOCTL.h"
#include "../../../CommonInclude/ValsimSharedCommonInclude.h"
#include <stdbool.h>

/////////****************************************************************************************************************/////////////
////////*************************************************IOCTLs START***************************************************/////////////
////////****************************************************************************************************************/////////////

///////////////////////////*******Init Test Cases Related IOCTLs  //Lets Reserve 50 Values for this*******************////////////

/////////////////////////*******Common Test Cases Related IOCTLs  //Lets Reserve 50 Values for this*************////////////////

#define IOCTL_INIT_PORT_INFO CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON), METHOD_BUFFERED, SIM_FILE_ACCESS)

// This would have Hotplug and HotUnplug variable in the IOCTL data
#define IOCTL_GENERATE_HPD CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON + 1), METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_SET_EDID_DATA CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON + 2), METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_SET_GFXS3S4_EDID_DATA CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON + 3), METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_GFXS3S4_PLUGUNPLUG_DATA CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON + 4), METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_SIMDRVTOGFX_DISPLAY_DFTHOOKS CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON + 5), METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_SIMDRVTOGFX_TRIGGER_DSB CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON + 6), METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_SIMDRVTOGFX_MMIO_ACCESS CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON + 7), METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_GENERATE_MIPI_DSI_TE CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON + 8), METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_SIMDRVTOGFX_TRIGGER_MIPI_DSI_DCS CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON + 9), METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_SIMDRVTOGFX_TRIGGER_BRIGHTNESS3 CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON + 10), METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_SIMDRVTOGFX_PLATFORM_DETAILS CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON + 11), METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_TRIGGER_SPI CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON + 12), METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_GET_DRIVER_WA_TABLE CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON + 13), METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_GET_DISP_DIAG_DATA CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON + 14), METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_GET_DISP_ADAPTER_CAPS CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON + 15), METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_SET_DONGLE_TYPE CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON + 16), METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_TRIGGER_HPD CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON + 17), METHOD_BUFFERED, SIM_FILE_ACCESS)
#define IOCTL_TRIGGER_DPCD_WRITE CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON + 18), METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_TRIGGER_SCDC_INTERRUPT CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON + 19), METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_SIMDRVTOGFX_WAKE_LOCK_ACCESS CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON + 20), METHOD_BUFFERED, SIM_FILE_ACCESS)

/////////****************************************************************************************************************/////////////
////////*************************************************IOCTLs END***************************************************** /////////////
////////****************************************************************************************************************/////////////

#define MAX_ENCODERS 14

typedef enum _RX_TYPE
{
    RxInvalidType,
    DP, // used for EDP and DP SST/MST. for EDP we use the same topology type enum as we use for DP SST i.e. eDPSST
    HDMI,
    MAX_RX_TYPES

} RX_TYPE,
*PRX_TYPE;

typedef enum _SINK_PLUGGED_STATE
{
    ePluggedStateInvalid = 0,
    eSinkPlugged,
    eSinkUnplugged

} SINK_PLUGGED_STATE,
*PSINK_PLUGGED_STATE;

typedef enum _DD_SPI_EVENTS
{
    DD_SPI_NONE,
    DD_SPI_CONNECTION_EVENT,
    DD_SPI_LINK_LOSS_EVENT, // DP link retraining event, handled by OSL
    DD_SPI_ATR_EVENT,
    DD_SPI_PARTIAL_DETECTION_EVENT, // MST CSN
    DD_SPI_CP_EVENT,
    DD_SPI_CRC_ERROR_EVENT,       // To CRC error in PSR
    DD_SPI_RESOURCE_CHANGE_EVENT, // set by TBT tunnel BW manager
    DD_SPI_PSR_CAPS_CHANGE_EVENT, // Set when PSR caps change from PSR to PSR2 or vice versa
    DD_SPI_MAX_EVENTS
} DD_SPI_EVENTS,
* PDD_SPI_EVENTS;

#pragma pack(1)

typedef union _PORT_CONNECTOR_INFO {
    unsigned char Value;
    struct
    {
        unsigned char IsTypeC : 1;
        unsigned char IsTbt : 1;
    };

} PORT_CONNECTOR_INFO;

typedef struct _DONGLE_TYPE_INFO
{
    unsigned int uiPortNum;
    unsigned int uiDongleType;

} DONGLE_TYPE_INFO, *PDONGLE_TYPE_INFO;

typedef struct _PORT_INFO
{
    unsigned int       ulPortNum;
    RX_TYPE            eRxTypes;
    SINK_PLUGGED_STATE eInitialPlugState; // This Flag's main use is in eDP simulation. This flag allows
                                          // eDP to to saved in the persistence database without generating an HPD
} PORT_INFO, *PPORT_INFO;

typedef struct _PORT_HPD_ARGS
{
    unsigned long       ulPortNum;
    BOOLEAN             bAttachorDettach;
    PORT_CONNECTOR_INFO uPortConnectorInfo;

} PORT_HPD_ARGS, *PPORT_HPD_ARGS;

typedef struct _FILE_DATA
{
    unsigned int  uiPortNum;
    unsigned int  uiDataSize;
    unsigned char ucNodeName[NAME_STR_SIZE];

} FILE_DATA, *PFILE_DATA;

typedef enum _PLUG_REQUEST
{
    ePlugRequestInvalid = 0,
    ePlugSink,
    eUnplugSink,
    eUnPlugOldPlugNew

} PLUG_REQUEST,
*PPLUG_REQUEST;

typedef struct _GFXS3S4_PORT_PLUGUNPLUG_DATA
{
    unsigned long           ulPortNum;
    PLUG_REQUEST            eSinkPlugReq; // Plug Or Unlug
    PORT_CONNECTOR_INFO     uConnectorInfoAfterResume;
    unsigned int            uiDongleType;
    S3S4_DP_PLUGUNPLUG_DATA stS3S4DPPlugUnplugData;

} GFXS3S4_PORT_PLUGUNPLUG_DATA, *PGFXS3S4_PORT_PLUGUNPLUG_DATA;

typedef struct _GFXS3S4_ALLPORTS_PLUGUNPLUG_DATA
{
    unsigned long                ulNumPorts;
    GFXS3S4_PORT_PLUGUNPLUG_DATA stS3S4PortPlugUnplugData[MAX_ENCODERS];

} GFXS3S4_ALLPORTS_PLUGUNPLUG_DATA, *PGFXS3S4_ALLPORTS_PLUGUNPLUG_DATA;

typedef struct _DISP_ADAPTER_CAPS
{
    WCHAR busDeviceID[MAX_DEVICE_ID_LEN];
    LUID  adapterLuid;
    GUID  adapterGuid;
    bool  displayLessAdapter;
    bool  displayOnlyDriver;
    bool  isGfxReady;
    ULONG devicePowerState;
    ULONG powerAction;
} DISP_ADAPTER_CAPS;

typedef struct _DISP_ADAPTER_CAPS_DETAILS
{
    ULONG             numAdapterCaps;
    DISP_ADAPTER_CAPS displayAdapterCaps[MAX_GFX_ADAPTER];
} DISP_ADAPTER_CAPS_DETAILS;

typedef struct _SCDC_ARGS
{
    unsigned long ulPortNum;
    DD_SPI_EVENTS eSpiEventType;
} SCDC_ARGS, * PSCDC_ARGS;

/** Structure definition forDevice Io Control Buffer */
typedef struct _DEVICE_IO_CONTROL_BUFFER
{
    PVOID             pInBuffer;     // Device Io Control Input Buffer
    ULONG             inBufferSize;  // Device Io Control Input Buffer Size
    PVOID             pOutBuffer;    // Device Io Control Output Buffer
    ULONG             outBufferSize; // Device Io Control Output Buffer Size
    PGFX_ADAPTER_INFO pAdapterInfo;  // Gfx Adapter Info
} DEVICE_IO_CONTROL_BUFFER, *PDEVICE_IO_CONTROL_BUFFER;

#pragma pack()

#endif
