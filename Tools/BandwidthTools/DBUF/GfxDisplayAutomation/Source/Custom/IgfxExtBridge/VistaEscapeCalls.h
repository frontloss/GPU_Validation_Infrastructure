#ifndef _VISTA_ESC_H
#define _VISTA_ESC_H

#define MAX_PIPES		2
#define MAX_DISPLAYS	(MAX_PORTS * 2)	  // Allows for combo codecs
#define MAX_PLANES		4	// VGA, DisplayA/B & C
#define MAX_CURSOR_PLANES 2
#include "malloc.h"

typedef LONG							NTSTATUS;
#define STATUS_SUCCESS                   ((NTSTATUS)0x00000000L) // ntsubauth
#define STATUS_INVALID_PARAMETER         ((NTSTATUS)0xC000000DL)
#define STATUS_INVALID_PARAMETER_MIX     ((NTSTATUS)0xC0000030L)
#define STATUS_INVALID_PARAMETER_1       ((NTSTATUS)0xC00000EFL)

//For Vista escape calls
typedef UINT D3DKMT_HANDLE;
/*typedef struct _DISPLAY_LIST {
	UINT	nDisplays;
    ULONG   ulDisplayUID[14];      
    ULONG   ulDeviceConfig;         // device configuration (Usefull for dual display)
} DISPLAY_LIST, *PDISPLAY_LIST;*/
/*
typedef enum _D3DKMT_TDRDBGCTRLTYPE
{
    D3DKMT_TDRDBGCTRLTYPE_FORCETDR      = 0, //Simulate a TDR
    D3DKMT_TDRDBGCTRLTYPE_DISABLEBREAK  = 1, //Disable DebugBreak on timeout
    D3DKMT_TDRDBGCTRLTYPE_ENABLEBREAK   = 2, //Enable DebugBreak on timeout
    D3DKMT_TDRDBGCTRLTYPE_UNCONDITIONAL = 3, //Disables all safety conditions (e.g. check for consecutive recoveries)
} D3DKMT_TDRDBGCTRLTYPE;
*/
/*typedef struct _COM_DETECT_DEVICE_ARGS   { 
    ULONG         Cmd;      //Always COM_DETECT_DEVICE
    ULONG         ulFlags;  //Bit0:  Do Redetect
                            //Bit1:  Do Legacy Detection 
    DISPLAY_LIST  DispList; //Refer to SbArgs for define
    
}COM_DETECT_DEVICE_ARGS, *PCOM_DETECT_DEVICE_ARGS;*/

/*typedef enum {
	NULL_PORT_TYPE = -1,
	ANALOG_PORT = 0,
	DVOA_PORT,
	DVOB_PORT,
	DVOC_PORT,
	LVDS_PORT,
	INT_TVOUT_PORT,		// From Alviso onwards
	INT_DVI_PORT,		// NA
	MAX_PORTS
} PORT_TYPES, *PPORT_TYPES;*/

typedef enum _D3DKMT_ESCAPETYPE
{
    D3DKMT_ESCAPE_DRIVERPRIVATE           = 0,
    D3DKMT_ESCAPE_VIDMM                   = 1,
    D3DKMT_ESCAPE_TDRDBGCTRL              = 2,
    D3DKMT_ESCAPE_VIDSCH                  = 3,
    D3DKMT_ESCAPE_DEVICE                  = 4,
    D3DKMT_ESCAPE_DMM                     = 5,
    D3DKMT_ESCAPE_DEBUG_SNAPSHOT          = 6,
    D3DKMT_ESCAPE_SETDRIVERUPDATESTATUS   = 7
} D3DKMT_ESCAPETYPE;

typedef struct _D3DDDI_ESCAPEFLAGS
{
    union
    {
        struct
        {
            UINT    HardwareAccess      : 1;    // 0x00000001
            UINT    Reserved            :31;    // 0xFFFFFFFE
        };
        UINT        Value;
    };
} D3DDDI_ESCAPEFLAGS;

typedef struct _D3DKMT_ESCAPE
{
    D3DKMT_HANDLE       hAdapter;               // in: adapter handle
    D3DKMT_HANDLE       hDevice;                // in: device handle [Optional]
    D3DKMT_ESCAPETYPE   Type;                   // in: escape type.
    D3DDDI_ESCAPEFLAGS  Flags;                  // in: flags
    VOID*               pPrivateDriverData;     // in/out: escape data
    UINT                PrivateDriverDataSize;  // in: size of escape data
    D3DKMT_HANDLE       hContext;               // in: context handle [Optional]
} D3DKMT_ESCAPE;

typedef enum _KMTQUERYADAPTERINFOTYPE
{
     KMTQAITYPE_UMDRIVERPRIVATE         =  0,
     KMTQAITYPE_UMDRIVERNAME            =  1,
     KMTQAITYPE_UMOPENGLINFO            =  2,
     KMTQAITYPE_GETSEGMENTSIZE          =  3,
     KMTQAITYPE_ADAPTERGUID             =  4,
     KMTQAITYPE_FLIPQUEUEINFO           =  5,
     KMTQAITYPE_ADAPTERADDRESS          =  6,
     KMTQAITYPE_SETWORKINGSETINFO       =  7,
     KMTQAITYPE_ADAPTERREGISTRYINFO     =  8,
     KMTQAITYPE_CURRENTDISPLAYMODE      =  9,
     KMTQAITYPE_MODELIST                = 10,
     KMTQAITYPE_CHECKDRIVERUPDATESTATUS = 11,
} KMTQUERYADAPTERINFOTYPE;


typedef enum 
{
    // DO NOT ADD NEGATIVE ENUMERATORTS
    GFX_ESCAPE_CODE_DEBUG_CONTROL = 0L, // DO NOT CHANGE 
    GFX_ESCAPE_CUICOM_CONTROL,
    GFX_ESCAPE_GMM_CONTROL,
    GFX_ESCAPE_CAMARILLO_CONTROL,
    GFX_ESCAPE_ROTATION_CONTROL,
    GFX_ESCAPE_ENCRYPTION_CONTROL,

    // NOTE: WHEN YOU ADD NEW ENUMERATOR, PLEASE UPDATE 
    //       InitializeEscapeCodeTable in miniport\LHDM\Display\AdapterEscape.c
 
    GFX_MAX_ESCAPE_CODES // MUST BE LAST 
} GFX_ESCAPE_CODE_T;

typedef struct GFX_ESCAPE_HEADER
{
    unsigned long       Size;       // Size of operation specific data arguments
    unsigned long       CheckSum;   // ulong based sum of data arguments
    GFX_ESCAPE_CODE_T   EscapeCode; // code defined for each independent
                                    // component
    unsigned long       ulReserved; // ensure sizeof struct divisible by 8
                                    // to prevent padding on 64-bit builds
} GFX_ESCAPE_HEADER_T;

typedef UINT  D3DDDI_VIDEO_PRESENT_SOURCE_ID;
typedef struct _D3DKMT_OPENADAPTERFROMHDC
{
    HDC                             hDc;            // in:  DC that maps to a single display
    D3DKMT_HANDLE                   hAdapter;       // out: adapter handle
    LUID                            AdapterLuid;    // out: adapter LUID
    D3DDDI_VIDEO_PRESENT_SOURCE_ID  VidPnSourceId;  // out: VidPN source ID for that particular display
} D3DKMT_OPENADAPTERFROMHDC;

typedef struct _D3DKMT_ADAPTERADDRESS
{
    UINT   BusNumber;              // Bus number on which the physical device is located.
    UINT   DeviceNumber;           // Index of the physical device on the bus.
    UINT   FunctionNumber;         // Function number of the adapter on the physical device.
} D3DKMT_ADAPTERADDRESS;

typedef struct _D3DKMT_QUERYADAPTERINFO
{
    D3DKMT_HANDLE           hAdapter;
    KMTQUERYADAPTERINFOTYPE Type;
    VOID*                   pPrivateDriverData;
    UINT                    PrivateDriverDataSize;
} D3DKMT_QUERYADAPTERINFO;

typedef struct _D3DKMT_INVALIDATEACTIVEVIDPN
{
    D3DKMT_HANDLE                   hAdapter;               // in: Adapter handle
    VOID*                           pPrivateDriverData;     // in: Private driver data
    UINT                            PrivateDriverDataSize;  // in: Size of private driver data
} D3DKMT_INVALIDATEACTIVEVIDPN;
typedef struct _D3DKMT_CLOSEADAPTER
{
    D3DKMT_HANDLE   hAdapter;   // in: adapter handle
} D3DKMT_CLOSEADAPTER;

typedef NTSTATUS (APIENTRY *PFND3DKMT_ESCAPE)(D3DKMT_ESCAPE*);
typedef NTSTATUS (APIENTRY *PFND3DKMT_OPENADAPTERFROMHDC)(D3DKMT_OPENADAPTERFROMHDC*);
typedef NTSTATUS (APIENTRY *PFND3DKMT_CLOSEADAPTER)(D3DKMT_CLOSEADAPTER*);
typedef NTSTATUS (APIENTRY *PFND3DKMT_INVALIDATEACTIVEVIDPN)(D3DKMT_INVALIDATEACTIVEVIDPN*);


#endif //End of _VISTA_ESC_H