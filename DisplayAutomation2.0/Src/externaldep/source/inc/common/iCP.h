/*+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
**
** Copyright (c) Intel Corporation (1998).
**
** INTEL MAKES NO WARRANTY OF ANY KIND REGARDING THE CODE.  THIS CODE IS LICENSED
** ON AN "AS IS" BASIS AND INTEL WILL NOT PROVIDE ANY SUPPORT, ASSISTANCE,
** INSTALLATION, TRAINING OR OTHER SERVICES.  INTEL DOES NOT PROVIDE ANY UPDATES,
** ENHANCEMENTS OR EXTENSIONS.  INTEL SPECIFICALLY DISCLAIMS ANY WARRANTY OF
** MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR ANY PARTICULAR PURPOSE, OR ANY
** OTHER WARRANTY.  Intel disclaims all liability, including liability for
** infringement of any proprietary rights, relating to use of the code. No license,
** express or implied, by estoppel or otherwise, to any intellectual property
** rights is granted herein.
**
**
** File Name: iCP.h
**
** Abstract:  Content Protection definitions and abstraction layer
**
** Authors:   Javier Martinez
**
** Notes:
**
** Items In File:
**
**+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

#ifndef __ICP_H__
#define __ICP_H__

// GUID for CP Parameters
#define CP_GUID "{7846871A-FF56-4669-A3E0-55571D9107C5}"

// Constants
#define CP_NO_PROTECTION_LEVEL_AVAILABLE 0
#define CP_HDCP_KEY_SELECTION_VECTOR_SIZE 5
#define CP_MAX_SIGNALS 2 // Maximum number of content protection signals supported in a TV format
#define CP_SIGNAL_A 0x00000001
#define CP_SIGNAL_B 0x00000002
#define CP_SIGNAL_A_INDEX 0
#define CP_SIGNAL_B_INDEX 1
#define CP_FLAG_SET 0x1

#define MAX_HDCP1_DEVICES 127
#define KSV_SIZE 5

// Error values
#define CP_STATUS_REVOKED_HDCP_DEVICE_ATTACHED 0xC00000FA

// HDCP level check
#define IS_HDCP_LEVEL_ON(x) ((x == CP_PROTECTION_LEVEL_HDCP_ON) || (x == CP_PROTECTION_LEVEL_HDCP_ON_TYPE1))
// HDCP type check for all types
#define IS_HDCP_TYPE(x) ((x & CP_PROTECTION_TYPE_COPP_COMPATIBLE_HDCP) || (x & CP_PROTECTION_TYPE_HDCP) || (x & CP_PROTECTION_TYPE_HDCP_TYPE_ENFORCEMENT))
// HDCP type check for OPM HDCP types
#define IS_OPM_HDCP_TYPE(x) ((x & CP_PROTECTION_TYPE_HDCP) || (x & CP_PROTECTION_TYPE_HDCP_TYPE_ENFORCEMENT))
// HDCP STREAM
#define IS_HDCP_STREAM_TYPE(x) ((x == CONTENT_STREAM_TYPE0) || (x == CONTENT_STREAM_TYPE1))

/////////////////////////////////////////////////////////
//
// Enums
//

// TV protection signaling standards
typedef enum _CP_TVPROTECTIONSTANDARD_T
{
    CP_PROTECTION_STANDARD_UNKNOWN             = 0x80000000,
    CP_PROTECTION_STANDARD_NONE                = 0x00000000,
    CP_PROTECTION_STANDARD_IEC61880_525I       = 0x00000001,
    CP_PROTECTION_STANDARD_IEC61880_2_525I     = 0x00000002,
    CP_PROTECTION_STANDARD_IEC62375_625P       = 0x00000004,
    CP_PROTECTION_STANDARD_EIA608B_525         = 0x00000008,
    CP_PROTECTION_STANDARD_EN300294_625I       = 0x00000010,
    CP_PROTECTION_STANDARD_CEA805A_TypeA_525P  = 0x00000020,
    CP_PROTECTION_STANDARD_CEA805A_TypeA_750P  = 0x00000040,
    CP_PROTECTION_STANDARD_CEA805A_TypeA_1125I = 0x00000080,
    CP_PROTECTION_STANDARD_CEA805A_TypeB_525P  = 0x00000100,
    CP_PROTECTION_STANDARD_CEA805A_TypeB_750P  = 0x00000200,
    CP_PROTECTION_STANDARD_CEA805A_TypeB_1125I = 0x00000400,
    CP_PROTECTION_STANDARD_ARIBTRB15_525I      = 0x00000800,
    CP_PROTECTION_STANDARD_ARIBTRB15_525P      = 0x00001000,
    CP_PROTECTION_STANDARD_ARIBTRB15_750P      = 0x00002000,
    CP_PROTECTION_STANDARD_ARIBTRB15_1125I     = 0x00004000,
} CP_TVPROTECTION_STANDARD_T;
#define CP_SIGNAL_A_MASK                                                                                                                                                         \
    CP_PROTECTION_STANDARD_EIA608B_525 | CP_PROTECTION_STANDARD_IEC62375_625P | CP_PROTECTION_STANDARD_EIA608B_525 | CP_PROTECTION_STANDARD_EN300294_625I |                      \
    CP_PROTECTION_STANDARD_CEA805A_TypeA_525P | CP_PROTECTION_STANDARD_CEA805A_TypeA_750P | CP_PROTECTION_STANDARD_CEA805A_TypeA_1125I |                                         \
    CP_PROTECTION_STANDARD_CEA805A_TypeB_525P | CP_PROTECTION_STANDARD_CEA805A_TypeB_750P | CP_PROTECTION_STANDARD_CEA805A_TypeB_1125I | CP_PROTECTION_STANDARD_ARIBTRB15_525I | \
    CP_PROTECTION_STANDARD_ARIBTRB15_525P | CP_PROTECTION_STANDARD_ARIBTRB15_750P | CP_PROTECTION_STANDARD_ARIBTRB15_1125I
#define CP_SIGNAL_B_MASK CP_PROTECTION_STANDARD_IEC61880_525I // NTSC

// TV image aspect ratio
typedef enum _CP_IMAGE_ASPECT_RATIO
{
    CP_ASPECT_RATIO_FF_4_BY_3             = 0,
    CP_ASPECT_RATIO_14_BY_9_CENTER        = 1,
    CP_ASPECT_RATIO_14_BY_9_TOP           = 2,
    CP_ASPECT_RATIO_16_BY_9_CENTER        = 3,
    CP_ASPECT_RATIO_16_BY_9_TOP           = 4,
    CP_ASPECT_RATIO_GT_16_BY_9_CENTER     = 5,
    CP_ASPECT_RATIO_FF_4_BY_3_PROT_CENTER = 6,
    CP_ASPECT_RATIO_FF_16_BY_9_ANAMORPHIC = 7,
} CP_IMAGE_ASPECT_RATIO;

// Connector type
typedef enum _CP_CONNECTOR_TYPE_T
{
    CP_CONNECTOR_TYPE_UNINITIALIZED            = -2,
    CP_CONNECTOR_TYPE_OTHER                    = -1,
    CP_CONNECTOR_TYPE_VGA                      = 0,
    CP_CONNECTOR_TYPE_SVIDEO                   = 1,
    CP_CONNECTOR_TYPE_COMPOSITE_VIDEO          = 2,
    CP_CONNECTOR_TYPE_COMPONENT_VIDEO          = 3,
    CP_CONNECTOR_TYPE_DVI                      = 4,
    CP_CONNECTOR_TYPE_HDMI                     = 5,
    CP_CONNECTOR_TYPE_LVDS                     = 6,
    CP_CONNECTOR_TYPE_D_JPN                    = 8,
    CP_CONNECTOR_TYPE_DP_EXTERNAL              = 10,
    CP_CONNECTOR_TYPE_DP_EMBEDDED              = 11,
    CP_CONNECTOR_TYPE_MIRACAST                 = 15,
    CP_COPP_COMPATIBLE_CONNECTOR_TYPE_INTERNAL = 0x80000000,
} CP_CONNECTOR_TYPE_T;

// Protection type
typedef enum _CP_PROTECTION_TYPE_T
{
    CP_PROTECTION_TYPE_UNKNOWN               = 0x80000000,
    CP_PROTECTION_TYPE_NONE                  = 0x00000000,
    CP_PROTECTION_TYPE_COPP_COMPATIBLE_HDCP  = 0x00000001,
    CP_PROTECTION_TYPE_ACP                   = 0x00000002,
    CP_PROTECTION_TYPE_CGMSA                 = 0x00000004,
    CP_PROTECTION_TYPE_HDCP                  = 0x00000008,
    CP_PROTECTION_TYPE_HDCP_TYPE_ENFORCEMENT = 0x00000020,
    CP_PROTECTION_TYPE_MASK                  = 0x8000003F,
} CP_PROTECTION_TYPE_T;

// Protection level (ACP)
typedef enum _CP_PROTECTION_LEVEL_ACP
{
    CP_PROTECTION_LEVEL_ACP_OFF         = 0,
    CP_PROTECTION_LEVEL_ACP_LOW         = 1,
    CP_PROTECTION_LEVEL_ACP_MEDIUM      = 3,
    CP_PROTECTION_LEVEL_ACP_HIGH        = 2,
    CP_PROTECTION_LEVEL_ACP_FORCE_ULONG = 0x7fffffff,
} CP_PROTECTION_LEVEL_ACP;

// Protection level (CGMSA)
typedef enum _CP_PROTECTION_LEVEL_CGMSA
{
    CP_PROTECTION_LEVEL_CGMSA_OFF                             = 0,
    CP_PROTECTION_LEVEL_CGMSA_COPY_FREELY                     = 1,
    CP_PROTECTION_LEVEL_CGMSA_COPY_NO_MORE                    = 2,
    CP_PROTECTION_LEVEL_CGMSA_COPY_ONE_GENERATION             = 3,
    CP_PROTECTION_LEVEL_CGMSA_COPY_NEVER                      = 4,
    CP_PROTECTION_LEVEL_CGMSA_REDISTRIBUTION_CONTROL_REQUIRED = 0x08,
} CP_PROTECTION_LEVEL_CGMSA;

// Protection level (HDCP)
typedef enum _CP_PROTECTION_LEVEL_HDCP
{
    CP_PROTECTION_LEVEL_HDCP_OFF      = 0,
    CP_PROTECTION_LEVEL_HDCP_ON       = 1,
    CP_PROTECTION_LEVEL_HDCP_ON_TYPE1 = 2,
} CP_PROTECTION_LEVEL_HDCP;

// HDCP authentication step
typedef enum _HDCP_AUTHENTICATION_STEP_T
{
    HDCP_AUTHENTICATION_STEP_NONE = 0,
    HDCP_AUTHENTICATION_STEP_1    = 1,
    HDCP_AUTHENTICATION_STEP_2    = 2,
} HDCP_AUTHENTICATION_STEP_T;

// CP Operations
typedef enum _CP_OPERATION_T
{
    CP_OP_GET = 0,
    CP_OP_SET = 1,
} CP_OPERATION_T;

typedef enum _CONTENT_STREAM_TYPE
{
    CONTENT_STREAM_TYPEOFF   = 0,
    CONTENT_STREAM_TYPE0     = 1, // may be transmitted by the HDCP repeater to all HDCP devices
    CONTENT_STREAM_TYPE1     = 2, // must not be transmitted by the HDCP repeater to HDCP 1.x-compliant devices and HDCP 2.0-compliant repeaters
    MAX_CONTENT_STREAM_TYPES = 3
} CONTENT_STREAM_TYPE,
*PCONTENT_STREAM_TYPE;

typedef enum _CONTENT_STREAM_TYPE_WIDI
{
    CONTENT_STREAM_TYPE0_WIDI     = 0, // may be transmitted by the HDCP repeater to all HDCP devices
    CONTENT_STREAM_TYPE1_WIDI     = 1, // must not be transmitted by the HDCP repeater to HDCP 1.x-compliant devices and HDCP 2.0-compliant repeaters
    MAX_CONTENT_STREAM_TYPES_WIDI = 2
} CONTENT_STREAM_TYPE_WIDI,
*PCONTENT_STREAM_TYPE_WIDI;

/////////////////////////////////////////////////////////
//
// Structures
//

#pragma pack(1)

// CP Signaling Parameters
typedef struct _CP_SIGNALING_PARAMETERS_T
{
    ULONG                 ulAvailableTVProtectionStandards; // Available TV standards (get)
    ULONG                 ulActiveTVProtectionStandard;     // Active TV standards (get)
    CP_IMAGE_ASPECT_RATIO AspectRatio;                      // Aspect ratio requested -MANDATORY- (set)
    ULONG                 ActiveCPSignals : CP_MAX_SIGNALS; // Active signals requested -MANDATORY- (set)
} CP_SIGNALING_PARAMETERS_T;

// KSV
typedef struct _KSV_T
{
    UCHAR abKSV[CP_HDCP_KEY_SELECTION_VECTOR_SIZE];
} KSV_T, *PKSV_T;

// HDCP
typedef struct _HDCP_DATA_T
{
    ULONG   dwKSVListLength;                        // Length of the revoked KSV list (set)
    KSV_T   AKSV;                                   // KSV of attached device
    KSV_T   BKSV;                                   // KSV of attached device
    PKSV_T  pKSVList;                               // List of revoked KSVs (set)
    UCHAR   BKSV_RPT[MAX_HDCP1_DEVICES * KSV_SIZE]; // list of downstream Bksv
    USHORT  usDeviceCount;                          // Downstream Device Count
    USHORT  usDepth;                                // Downstream Depth
    BOOLEAN bPerformSecondStep;                     // True when the second authentication step is requested (get)
    BOOLEAN bPerformAsync;
    BOOLEAN bIsRepeater;          // True when a repeater is attached to the connector (get and set)
    ULONG   dwMajorVer;           // Major version of HDCP repeater or device
    ULONG   dwMinorVer;           // Minor version of HDCP repeater or device
    BOOLEAN bHasHDCP1_x;          // If TRUE, the topology includes downstream devices that are HDCP 1.x compliant
    BOOLEAN bHasHDCP2_0_Repeater; // if TRUE, the topology includes a downstream HDCP 2.0 compliant repeater
    BOOLEAN bIsiHDCP2_2;
} HDCP_DATA_T, *PHDCP_DATA_T;

// Content Stream Type Mask
typedef enum _HDCP_STREAM_INFO_MASK
{
    CP_HDCP_STREAM_INFO_NONE      = 0,
    CP_HDCP_STREAM_INFO_TYPE      = 1,
    CP_HDCP_STREAM_INFO_TYPE_MASK = 1
} HDCP_STREAM_INFO_MASK;

// HDCP Paramters GUID {AD385541-FAB2-4b0c-AAC3-F1722AF8FD4B}
#define GUID_INTEL_HDCP "{AD385541-FAB2-4b0c-AAC3-F1722AF8FD4B}"
// DEFINE_GUID(GUID_INTEL_HDCP, 0xAD385541, 0xFAB2, 0x4b0c, 0xAA, 0xC3, 0xF1, 0x72, 0x2A, 0xF8, 0xFD, 0x4B);

#ifndef IN
#define IN
#endif

#ifndef OUT
#define OUT
#endif

#ifndef INOUT
#define INOUT
#endif

//#if !defined __QWORD__
//#define __QWORD__
typedef struct SQWORD
{
    union {
        ULONGLONG QuadPart;
        struct
        {
            ULONG LowPart;
            ULONG HighPart;
        } u;
        struct
        {
            UCHAR Byte[8];
        };
    };
} SQWORD;

typedef SQWORD *PSQWORD, *LPSQWORD;

//#endif

#ifndef HQWORD

// A quadword size member
//
typedef struct _HQWORD
{
    union {
        struct
        {
            unsigned __int64 MajorPart : 40; // lower 40 bits
            unsigned __int64 unused1 : 24;
        };
        struct
        {
            unsigned MajorPart_Low : 32; // lower 32 bits
            unsigned MajorPart_High : 8; // lower  bits
            unsigned unused2 : 24;
        };
        struct SQWORD;
    };
} HQWORD, *PHQWORD;

#endif // HWORD

//
// 56 bit member
// or 84 bit member
typedef struct _HDCP_ENCRYPTED_KEY_ST
{
    union {
        struct
        {
            unsigned MajorPart_Low : 32;
            unsigned MajorPart_Med : 32;
            unsigned MajorPart_High : 20;
            unsigned unused1 : 12;
        } uh;
    };
} HDCP_ENCRYPTED_KEY, *PHDCP_ENCRYPTED_KEY;

// HDCP Commands
// The value placed in dwCommand depends on the action being performed.
//
typedef enum _VP_HDCP_COMMANDS
{
    VP_HDCP_CMD_ACTIVATE = 0x01,           // Activates the Link, hLinkContext is filled in with connection context
                                           // The fields after numLinks are required for any other commands
    VP_HDCP_CMD_GET_LINK_STATUS    = 0x02, // Read of the Downstream Status
    VP_HDCP_CMD_READ_STATUS        = 0x04, // Get the Status Word (Requires Cn, Cksv, An, Bksv)
    VP_HDCP_CMD_READ_Z             = 0x08, // Get the Z value (Requires Cn, Cksv)
    VP_HDCP_CMD_VALIDATE_LINK      = 0x10, // Gets M & V (Requires Cn, Cksv)
    VP_HDCP_CMD_RENEGOTIATE        = 0x20, // None of the fields after dwMode need to be filled
    VP_HDCP_CMD_DISABLE_ENCRYPTION = 0x40, // Disables the encryption whenever requested by the app
} VP_HDCP_COMMANDS,
*PVP_HDCP_COMMANDS;

typedef struct _HDCP_BSTATUS
{
    unsigned DeviceCount : 7;         // [6:0] Total Number of Receiver Devices (excluding repeaters) attached
    unsigned bMaxDevicesExceeded : 1; // [7] Topology Error. Greater than 127 devices attached
    unsigned bRepeaterDepth : 3;      // [10:8] Repeater depth
    unsigned bMaxCascadeExceeded : 1; // [11] Topology Error. Greater than 7 levels of Repeater attached
    unsigned bReserved : 20;          // [31:12] Reserved for future expansion
} HDCP_BSTATUS;

typedef enum _VP_AUDIO_ENCRYPT_COMMANDS
{
    VP_AUDIO_CHECK_ENCRYPT_STATUS    = 0x01, // Check if interrupt was from the audio driver & return requested level if it was
    VP_AUDIO_ENCRYPT_CMD_ACKNOWLEDGE = 0x02, // Let the audio driver know the request was serviced
} VP_AUDIO_ENCRYPT_COMMANDS,
*PVP_AUDIO_ENCRYPT_COMMANDS;

typedef struct _HDCP_AUDIO_ENCRYPT
{
    VP_AUDIO_ENCRYPT_COMMANDS dwCommand;
    BOOLEAN                   bAudioEncryption; // Whether to disable or enable encryption
} HDCP_AUDIO_ENCRYPT;

// Flags used for indicating active member elements
//
typedef enum _VP_HDCP_FLAGS
{
    VP_HDCP_FLAGS_LINK    = 0x000000, // NumLinks
    VP_HDCP_FLAGS_CMODE   = 0x000001, // Enumerator/Mode
    VP_HDCP_FLAGS_AN      = 0x000010, // Aksv = Downstream Session ID
    VP_HDCP_FLAGS_AKSV    = 0x000020, // Aksv = Downstream/Xmtr KSV
    VP_HDCP_FLAGS_BKSV    = 0x000040, // Bksv = Downstream/Rcvr KSV
    VP_HDCP_FLAGS_BSTATUS = 0x000080, // Link/Repeater Status
    VP_HDCP_FLAGS_CN      = 0x000100, // Cn = Upstream Session ID
    VP_HDCP_FLAGS_CKSV    = 0x000200, // Cksv = Upstream ClientApp KSV
    VP_HDCP_FLAGS_DKSV    = 0x000400, // Dksv = Upstream/Xmtr KSV
    VP_HDCP_FLAGS_KP      = 0x001000, // Signature
    VP_HDCP_FLAGS_S       = 0x002000, // Status
    VP_HDCP_FLAGS_CS      = 0x004000, // Connection State
    VP_HDCP_FLAGS_ZP      = 0x010000, // Z-prime
    VP_HDCP_FLAGS_V       = 0x020000, // V
    VP_HDCP_FLAGS_MP      = 0x040000, // M-prime
    VP_HDCP_FLAGS_NUMKSVS = 0x080000, // numKSV's
    VP_HDCP_FLAGS_KSVLIST = 0x100000, // KSVlist
} VP_HDCP_FLAGS;

// Indicates Current Mode of Operation
//
typedef enum _VP_HDCP_MODE
{
    VP_HDCP_MODE_NULL         = 0x0,
    VP_HDCP_MODE_ATTACHED     = 0x01, // Set when Monitor is Attached (Hot-Plug)
    VP_HDCP_MODE_ACTIVATED    = 0x02, // Link has start authentication process
    VP_HDCP_MODE_ENCRYPTING   = 0x04, // Link is send encrypted DVI
    VP_HDCP_MODE_INTEGRITY_OK = 0x08, // Ri == Ri'
} VP_HDCP_MODE;

// HDCP VIDEOPARAMETERS
//
typedef struct _HDCP_PARAMETERS
{
    IN GUID guidHDCP;              // {AD385541-FAB2-4b0c-AAC3-F1722AF8FD4B}
    IN ULONG dwSize;               // Offset to the end of VIDEOPARAMETERS_HDCP
                                   // ----------------------------------------------------------
                                   // DO NOT CHANGE ABOVE THIS LINE
                                   //
    IN VP_HDCP_COMMANDS dwCommand; // VP_HDCP_CMD_SET, VP_HDCP_CMD_GET
    INOUT VP_HDCP_FLAGS dwFlags;   // Which Fields are active/changed
    OUT VP_HDCP_MODE dwMode;       //
                                   // ----------------------------------------------------------
    INOUT ULONG hLinkContext;      // Cookie filled in by the Server during QueryInterface, must be used in this and subsequent client calls
    OUT ULONG numLinks;            // Used to enumerate the number of Links in a Virtual Channel
    IN ULONG dwCMode;              // Link enumerator

    // - CMD_Get fields -
    OUT SQWORD hwAn;            // Downstream Session Key, returned for VP_CMD_ReadStatus
    OUT HQWORD hwAksv;          // Transmitter Downstream (not necessary, don't reveal)
    OUT HQWORD hwBksv;          // Receiver Key-Selection Vector, returned for VP_CMD_ReadStatus, VP_CMD_GetLinkStatus
    OUT HDCP_BSTATUS flBStatus; // Downstream Session Key, returned for VP_CMD_GetLinkStatus
    OUT SHORT wRepeater;        // 1 if receiver is a repeater, 0 otherwise

    // - CMD_Set fields -
    IN SQWORD qwCn;   // Upstream Session Key, *MUST* be set before getting Status, VP_CMD_GetStatus, VP_CMD_ReadZ, VP_CMD_ReadM & VP_CMD_ReadM
    IN HQWORD hwCksv; // Client Key-Selection Vector, returned for Status, returned for VP_CMD_GetStatus

    // - CMD_ReadStatus fields -
    OUT HQWORD hwDksv; // Transmitter Upstream Key Selection Vector,
                       // for VP_CMD_ReadStatus, VP_CMD_ReadZ, VP_CMD_ReadM & VP_CMD_ReadM
    OUT SQWORD qwKp;   // Kp (Signature of S & Cs), returned for VP_CMD_ReadStatus
    OUT ULONG dwS;     // S Status Word, returned for VP_CMD_ReadStatus
    OUT HQWORD hwCs;   // Cs Connection State, returned for VP_CMD_ReadStatus

    // - CMD_GetZ fields -
    OUT SQWORD qwZp; // Z' (Encrypted Z), returned for VP_CMD_ReadZ

    // - CMD_ValidateLink  fields -
    OUT UCHAR V[20];                          // V (Receiver's signature of KSVlist, Bstatus, M0), returned for VP_CMD_ValidateLink
    OUT SQWORD qwMp;                          // M' (Encrypted M0), returned for VP_CMD_ValidateLink
    OUT ULONG numKSVs;                        // Number of items in the KSV list, returned for VP_CMD_ValidateLink
    OUT SQWORD qwKSVlist[ANYSIZE_ARRAY];      // Repeater KSV, returned for VP_CMD_ValidateLink
    OUT HDCP_AUDIO_ENCRYPT stAudioEncryption; // Structure to store the audio driver status
                                              // Variable Size ! Don't make any assumptions
} HDCP_PARAMETERS, *PHDCP_PARAMETERS, FAR *LPHDCP_PARAMETERS;

// CP Parameters
typedef struct _CP_PARAMETERS_T
{
    GUID                guid;                     // Content protection GUID (get and set)
    CP_OPERATION_T      op;                       // Operation type (get and set)
    ULONG               dwProtectTypeMask;        // Protection type mask (get and set)
    ULONG               Level;                    // Protection level (get and set)
    CP_CONNECTOR_TYPE_T ConnectorType;            // Connector type (get)
    HDCP_DATA_T         HDCPData;                 // HDCP specific data (get and set)
    ULONG               dwHDCPStreamInfoMask;     // HDCP stream information type mask (get and set)
    ULONG               HDCPStreamType;           // Receives the content stream type from application code.  If application code
                                                  // does not set this, assume CONTENT_STREAM_TYPE0 (Type 0 content).
    CP_SIGNALING_PARAMETERS_T SignalingData;      // CGMS-A signaling information (get and set)
    ULONG                     RedistCtrlFlag : 1; // CGMS-A redistribution control flag (get and set)
} CP_PARAMETERS_T;

#pragma pack()

#endif //__ICP_H__
