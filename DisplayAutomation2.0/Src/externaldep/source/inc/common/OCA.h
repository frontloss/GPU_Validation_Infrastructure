//=============================================================================
//  OCA.h
//
//  Copyright(c) Intel Corporation (2013)
//
//  INTEL MAKES NO WARRANTY OF ANY KIND REGARDING THE CODE.  THIS CODE IS
//  LICENSED ON AN "AS IS" BASIS AND INTEL WILL NOT PROVIDE ANY SUPPORT,
//  ASSISTANCE, INSTALLATION, TRAINING OR OTHER SERVICES.  INTEL DOES NOT
//  PROVIDE ANY UPDATES, ENHANCEMENTS OR EXTENSIONS.  INTEL SPECIFICALLY
//  DISCLAIMS ANY WARRANTY OF MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR ANY
//  PARTICULAR PURPOSE, OR ANY OTHER WARRANTY.  Intel disclaims all liability,
//  including liability for infringement of any proprietary rights, relating to
//  use of the code. No license, express or implied, by estoppel or otherwise,
//  to any intellectual property rights is granted herein.
//
//
//  File Description:
//  This file contains prototypes of DDIs implemented for supporting TDR in LH
//  driver
//
//=============================================================================
#ifndef _OCA_H_
#define _OCA_H_

#ifdef _COMMON_PPA
#include "OMPTool.h"
#endif

// Set packing alignment to a single byte
#pragma pack(push, 1)

//**********************************************************************//
// General defines and enums
//**********************************************************************//
#define DRIVER_VERSION_STRING_SIZE 512

// TDR/OCA Operation Types
typedef enum _TDR_OPERATION_REC
{
    TDR_OPERATION_RESET                       = 1, // Reset hardware
    TDR_OPERATION_RESET_PRE_GDRST             = 2, // Used to inform SB prior of GDRST
    TDR_OPERATION_RESET_POST_GDRST            = 3, // Used to inform SB post GDRST.
    TDR_OPERATION_RESTART                     = 4, // Restart hardware
    TDR_OPERATION_COLLECT_INFO_SAFE_REGISTERS = 5, // Dump registers into OCA report that will not cause hard hang
    TDR_OPERATION_COLLECT_INFO_REGISTERS      = 6, // Dump registers into OCA report
    TDR_OPERATION_COLLECT_INFO_STATE          = 7, // Dump state info into OCA report
    TDR_OPERATION_CHECK_KCR_STATUS            = 8  // Check KCR Status
} TDR_OPERATION;

//**********************************************************************//
// OCA Blob Header Definitions and Structures ...
//
//     Header size is currently determined by the OCA_BLOB_HDR
//     structure. Individual component divisions appear after this.
//**********************************************************************//

// Initial OCA header version
#define INITIAL_DRIVER_OCA_HEADER 0x115

// These definitions are used by the WinDbg KMOCA.DLL extension
#define OCA_HEADER_ID_0x115 0x115 // Valid from 15.12.75 through 15.17, inclusive
#define OCA_HEADER_ID_0x116 0x116 // Valid beginning with 15.21
#define OCA_HEADER_ID_0x117 0x117 // Valid beginning with 15.22 (HSW / Gen7_5)
#define OCA_HEADER_ID_0x141 0x141 // Valid beginning with 15.28 (Win8)
#define OCA_HEADER_ID_0x142 0x142 // Valid beginning with 15.44.4407 (KmOCA tool enhancement)

// Updated whenever the OCA header changes and requires a corresponding
// change in the WinDbg DLL we supply to Microsoft.  This definition
// is used by the driver.
#define CURRENT_DRIVER_OCA_HEADER OCA_HEADER_ID_0x142

//------------------------------------------------------
// Component's analysis results given in OCA blob header

typedef struct _OCA_ANALYSIS_ST
{
    // Kernel Mode Render component
    union {
        struct
        {
            ULONG KMR_Bad_Gfx_Addr : 1;     // Bad graphics address detected
            ULONG KMR_Bad_Phys_Addr : 1;    // Bad physical page in GTT
            ULONG KMR_Generic_Bad_Addr : 1; // A bad address was detected

            ULONG KMR_Parser_Error : 1;              // Instruction parser detected
                                                     // an error
            ULONG KMR_Render_Ring_Problem : 1;       // There is a problem in the
                                                     // Render engine ring
            ULONG KMR_Video_Ring_Problem : 1;        // There is a problem in the
                                                     // Video engine ring
            ULONG KMR_Blitter_Ring_Problem : 1;      // There is a problem in the
                                                     // Blitter engine ring
            ULONG KMR_VE_Ring_Problem : 1;           // There is a problem in the
                                                     // Video Enhancement engine ring
            ULONG KMR_VE2_Ring_Problem : 1;          // There is a problem in the
                                                     // Video Enhancement engine ring
            ULONG KMR_Ring_Disabled : 1;             // Ring buffer is disabled
            ULONG KMR_Ring_Hang : 1;                 // Ring is hung.  Head != Tail
            ULONG KMR_Ring_Head_Error : 1;           // Failure analysis has detected
                                                     // an error in ring head addressing
            ULONG KMR_Ring_Wrap : 1;                 // Ring wrap condition detected
                                                     // at error location
            ULONG KMR_GPU_Is_Active : 1;             // This indicates the GPU was still
                                                     // processing data when the OS
                                                     // triggered the TDR.
            ULONG KMR_Batch_Buffer_Hang : 1;         // Hang occurred in batch buffer
            ULONG KMR_Bad_Batch_Contents : 1;        // Batch contents appear to be
                                                     // corrupted.
            ULONG KMR_No_Batch_Overrun : 1;          // Batch buffer end was detected
                                                     // but the overrun pattern was
                                                     // missing.
            ULONG KMR_Aux_Batch_Buffer_Hang : 1;     // Hung in a batch buffer not
                                                     // directly associated with the
                                                     // current DMA buffer
            ULONG KMR_Exec_Invalid_Batch_Buffer : 1; // GPU fetching commands from
                                                     // an invalid batch buffer or
                                                     // address range.
            ULONG KMR_No_General_State : 1;          // No General State Base
                                                     // found
            ULONG KMR_No_Dynamic_State : 1;          // No Dynamic State Base
                                                     // found
            ULONG KMR_No_Binding_Table : 1;          // No Binding Table State
                                                     // found
            ULONG KMR_No_Surface_State : 1;          // No Surface State Base
                                                     // found
            ULONG KMR_No_Vertex_Buffer : 1;          // No vertex buffer found
            ULONG KMR_Inconsistent_Fence_Tags : 1;   // Access to the FENCE_TAGS structure
                                                     // thru CPU and GPU produces different
                                                     // data.
            ULONG KMR_Induced_TDR : 1;               // TDR was artificially induced--i.e.
            ULONG KMD_L3_Parity_Error : 1;           // L3 parity error.
            ULONG KMR_PF_Encountered : 1;            // Legacy context encountered page fault.
            ULONG KMR_Reserved : 4;                  // (Reserved)
        };

        ULONG KMR_AnalysisResults; // KMR ULONG equivalent
    };

    // Miniport/SoftBIOS component
    union {
        struct
        {
            ULONG MPSB_VSyncTimeout : 1;            // VSync timeout detected. Acts as master bit for all sub-reasons mentioned bellow.
            ULONG MPSB_VBIEnablingError : 1;        // VBI(s) not enabled
            ULONG MPSB_VBIGenError : 1;             // VBI(s) didn't get generated.
            ULONG MPSB_VBIRepError : 1;             // Missed reporting VBI(s)
            ULONG MPSB_VBIWrongSrcAddrReported : 1; // Wrong source address reported in VBI(s)
            ULONG MPSB_VBIWrongTgtIdReported : 1;   // Wrong target id reported in VBI(s)
            ULONG MPSB_Reserved : 26;               // (Reserved)
        };

        ULONG MPSB_AnalysisResults; // MPSB ULONG equivalent
    };

    // GMM component
    union {
        struct
        {
            ULONG GMM_Page_Table_Error : 1; // A page table error occurred
            ULONG GMM_Reserved : 31;        // (Reserved)
        };

        ULONG GMM_AnalysisResults; // GMM ULONG equivalent
    };

    // GRM component
    union {
        struct
        {
            ULONG GRM_LastBWChkFailed : 1; // Last BW Check failed
            ULONG GRM_Reserved : 31;       // Reserved
        };

        ULONG GRM_AnalysisResults; // GRM ULONG equivalent
    };

    // PC component
    union {
        struct
        {
            ULONG OCA_Gsv_RS2_Set_State_Hang : 1;    // HW hang after RS2 Enable
            ULONG OCA_Gsv_Pstate_Switching_Hang : 1; // HW hang after RS2 Enable
            ULONG PC_Reserved : 30;                  // Reserved
        };

        ULONG PC_AnalysisResults; // PC ULONG equivalent
    };

} OCA_ANALYSIS;

C_ASSERT(sizeof(OCA_ANALYSIS) == (5 * sizeof(ULONG))); // Validate OCA_ANALYSIS size.
                                                       // Checks that error bits do
                                                       // not overflow ULONG

//***********************************************************************************************//
// OCA blob header
//
//      This is the first block of data written to the OCA blob.  To be compatible with
//      the previous WinDbg extension given to Microsoft, members of OCA_BLOB_HDR_STATIC
//      should not be altered.
//      Changes to OCA_BLOB_HDR_xxxxx requires increment to HeaderID. That way, the Intel
//      WinDbg extension will know it is dealing with a fundamentally new header.
//
// **IMPORTANT** To add a new field to blob header:
//
//  ** Changing the blob header requires increment to HeaderID **
//  1. Make a copy of latest OCA_BLOB_HDR_xxxxx and name the new header struct with a new
//     HeaderID (e.g. OCA_BLOB_HDR_0x150)
//  2. Add the new field to the newly created header struct at the end of struct.
//     OCA_BLOB_HDR_STATIC should always be the first field of the struct.
//  3. Change OCA_BLOB_HDR typedef to the latest version of the header, driver will always use
//     this(the latest version)
//  4. Make sure the KmOCA source code accessing blob header casts to the correct header
//     version based on HeaderID.
//  Above steps are essential in keeping the KmOCA backward compatible!
//
//***********************************************************************************************//

#define OCA_HDR_GUID_SIZE 36        // Size of Intel GUID string
#define OCA_BUCKET_STRING_SIZE 64   // Size of "bucket string"
#define OCA_NUMBER_OF_RINGS_0x116 3 // Number of ring info structures
#define OCA_NUMBER_OF_RINGS_0x141 6 // Number of ring info structures for 0x141 Header
// New fields should be added to OCA_BLOB_HDR rather than OCA_BLOB_HDR_STATIC
typedef struct _OCA_BLOB_HDR_STATIC_ST
{
    char IntelEnumGuid[OCA_HDR_GUID_SIZE];     // ASCII character GUID identifier
    WORD HeaderID;                             // Will start at 0x115
    WORD DriverBuild;                          // Driver build number
    char BucketString[OCA_BUCKET_STRING_SIZE]; // Bucket string for Microsoft
                                               //-----------------DO NOT CHANGE ANYTHING in OCA_BLOB_HDR_STATIC above this comment --------------------------
    ULONG     BugCheck;                        // OS supplied bugcheck number
    ULONG     PCIDeviceID;                     // Gfx device PCI ID
    ULONG     PCIDeviceRevision;               // Gfx device revision ID (stepping)
    ULONG     VideoBIOSVersion;                // Video BIOS version
    ULONG     OCAHeaderSize;                   // Size of OCA header
    ULONG     OCABufferSize;                   // Size of OS provided OCA buffer
    ULONG     OCAReportSize;                   // Size used for report
    ULONGLONG StolenMemorySize;                // Size of stolen memory
    ULONGLONG TotalMemoryPages;                // Total memory pages
    ULONG     TotalGfxAddrRange;               // Maximum graphics address
} OCA_BLOB_HDR_STATIC;

// Ring information structure
typedef struct _OCA_BLOB_RING_INFO_ST
{
    ULONG WorkloadType; // Type of workload active
                        // at time of error:
                        // 0 = Unknown
                        // 1 = Media
                        // 2 = DX 9
                        // 3 = DX 10
                        // 4 = OpenGL
    ULONG     TailPtr;  // Contents of ring tail register
    ULONG     HeadPtr;  // Contents of ring head register
    ULONGLONG ACTHD;    // Active head contents for this ring
    ULONGLONG BB_ADDR;  // Batch buffer address register
    ULONG     RingSize; // Size of ring in bytes
} OCA_BLOB_RING_INFO;

//----------------------------- 0x115 HEADER -----------------------------------------------------------------
// ID 0x115 - Main Blob Header structure
typedef struct _OCA_BLOB_HDR_0x115_ST
{
    OCA_BLOB_HDR_STATIC OcaBlobHdrStatic; // Static portion of OCA header
    ULONG               Workload_Type;    // Type of workload active
                                          // at time of error:
                                          // 0 = Unknown
                                          // 1 = Media
                                          // 2 = DX 9
                                          // 3 = DX 10
                                          // 4 = OpenGL
    OCA_ANALYSIS AnalysisResults;         // Component analysis results ...
                                          // Each component is allocated
                                          // a ULONG in which to store
                                          // error flags.
    ULONG ACTHD_Before;                   // Active head pointer at
                                          // start of OCA processing.
    ULONG ACTHD_After;                    // Active head pointer at
                                          // end of OCA processing.
    ULONG BB_ADDR_register;               // Batch buffer address reg
    ULONG PRB0_HEAD_register;             // Primary ring buffer head pointer
    ULONG BCS_HEAD_register;              // Blitter ring buffer head pointer
    ULONG Prim_ring_size;                 // Size of primary ring in bytes
} OCA_BLOB_HDR_0x115;

//----------------------------- 0x116 HEADER -----------------------------------------------------------------
// ID 0x116 - Main Blob Header structure
typedef struct _OCA_BLOB_HDR_0x116_ST
{
    OCA_BLOB_HDR_STATIC OcaBlobHdrStatic;                   // Static portion of OCA header
    ULONG               NumGPUs;                            // Number of GPUs
    OCA_ANALYSIS        AnalysisResults;                    // Component analysis results ...
                                                            // Each component is allocated
                                                            // a ULONG in which to store
                                                            // error flags
    OCA_BLOB_RING_INFO RingInfo[OCA_NUMBER_OF_RINGS_0x116]; // Array of ring info structures
} OCA_BLOB_HDR_0x116;

//----------------------------- 0x117 HEADER -----------------------------------------------------------------
// ID 0x117 - Main Blob Header structure
typedef struct _OCA_BLOB_HDR_0x117_ST
{
    OCA_BLOB_HDR_STATIC OcaBlobHdrStatic; // Static portion of OCA header
    ULONG               NumGPUs;          // Number of GPUs
    OCA_ANALYSIS        AnalysisResults;  // Component analysis results ...
                                          // Each component is allocated
                                          // a ULONG in which to store
                                          // error flags.
    ULONG NumOCARings;                    // Number of OCA_BLOB_RING_INFO
                                          // structs to follow in the header
    OCA_BLOB_RING_INFO RingInfo[1];       // Placeholder for OCA_BLOB_RING_INFO
                                          // structs.
} OCA_BLOB_HDR_0x117;

//----------------------------- 0x141 HEADER -----------------------------------------------------------------
// ID 0x141 - Main Blob Header structure
typedef struct _OCA_BLOB_HDR_0x141_ST
{
    OCA_BLOB_HDR_STATIC OcaBlobHdrStatic;                   // Static portion of OCA header
    ULONG               NumGPUs;                            // Number of GPUs
    OCA_ANALYSIS        AnalysisResults;                    // Component analysis results ...
                                                            // Each component is allocated
                                                            // a ULONG in which to store
                                                            // error flags.
    ULONG NumOCARings;                                      // Number of OCA_BLOB_RING_INFO
                                                            // structs to follow in the header
    ULONG              NodeOrdinal;                         // Node Ordinal for the engine being reset
    OCA_BLOB_RING_INFO RingInfo[OCA_NUMBER_OF_RINGS_0x141]; // Placeholder for OCA_BLOB_RING_INFO
} OCA_BLOB_HDR_0x141;
//----------------------------- 0x142 HEADER -----------------------------------------------------------------
// ID 0x142 - Main Blob Header structure
typedef struct _OCA_BLOB_HDR_0x142_ST
{
    OCA_BLOB_HDR_STATIC OcaBlobHdrStatic; // Static portion of OCA header
    // New fields added in 0x142
    ULONG          RenderCore;
    ULONG          DisplayCore;
    ULONG          PlatformName;
    unsigned short usRevId;        // Revision ID of the Gfx
    unsigned short usDeviceID_PCH; // Device ID of PCH
    unsigned short usRevId_PCH;    // Revision ID of PCH
    //
    ULONG        NumGPUs;         // Number of GPUs
    OCA_ANALYSIS AnalysisResults; // Component analysis results ...
    // Each component is allocated
    // a ULONG in which to store
    // error flags.
    ULONG NumOCARings; // Number of OCA_BLOB_RING_INFO
    // structs to follow in the header
    ULONG              NodeOrdinal;                         // Node Ordinal for the engine being reset
    OCA_BLOB_RING_INFO RingInfo[OCA_NUMBER_OF_RINGS_0x141]; // Placeholder for OCA_BLOB_RING_INFO
} OCA_BLOB_HDR_0x142;

//----------------------------- Current BLOB Header ----------------------------------------------------------
typedef OCA_BLOB_HDR_0x142 OCA_BLOB_HDR;

//***********************************************************************************************//
// OCA Division Definitions and Structures ...
//
//     OCA data divisions are written to the "blob" immediately after the header.  There can be
//     any number of divisions in the report. The final division is the TRAILER division.
//     Divisions are containers of OCA data "sections".
//
// **IMPORTANT** To add a new field to division header:
//
//  ** Changing the division header requires increment to HeaderID **
//  1. Make a copy of OCA_DIVISION_HDR_BASE (or the latest vesion of OCA_DIVISION_HDR) and name
//     the new header struct with a new HeaderID (e.g. OCA_DIVISION_HDR_0x145)
//  2. Add the new field to the newly created header struct.
//  3. Change OCA_DIVISION_HDR typedef to the latest version of the header, driver will always use
//     this(the latest version)
//  4. Make sure the KmOCA source code accessing division header casts to the correct header
//     version based on header ID.
//  Above steps are essential in keeping the KmOCA backward compatible!
//
//***********************************************************************************************//

#define OCA_DIVISION_NAME_SIZE 8

#define OCA_TRAILER_TAG 0xbeeffeed;

// OCA Division Header 0x115/116/117/141
// Any new division header struct should have these two fields at beginning
typedef struct _OCA_DIVISION_HDR_BASE_ST
{
    char  DivisionName[OCA_DIVISION_NAME_SIZE]; // ASCII division name
    ULONG DivisionSize;                         // Division size
} OCA_DIVISION_HDR_BASE;
// OCA Division Header 0x142
typedef struct _OCA_DIVISION_HDR_0x142_ST
{
    char  DivisionName[OCA_DIVISION_NAME_SIZE]; // ASCII division name
    ULONG DivisionSize;                         // Division size
    //==================================================================
    ULONG DivisionState; // Will be set to invalid if certain dumps fail.
} OCA_DIVISION_HDR_0x142;
// Current division header (used by driver)
typedef OCA_DIVISION_HDR_0x142 OCA_DIVISION_HDR;

// Last division in the OCA report is the TRAILER
typedef struct _OCA_TRAILER_DIV_0x141_ST
{
    OCA_DIVISION_HDR_BASE DivisionHeader;
    ULONG                 TrailerTag;
} OCA_TRAILER_DIV_0x141;
// Trailer 0x142 (needed because added field in DivisionHeader has shifter TrailerTag
typedef struct _OCA_TRAILER_DIV_0x142_ST
{
    OCA_DIVISION_HDR_0x142 DivisionHeader;
    ULONG                  TrailerTag;
} OCA_TRAILER_DIV_0x142;
// Current trailer div (used by driver)
typedef OCA_TRAILER_DIV_0x142 OCA_TRAILER_DIV;

//***********************************************************************************************//
// OCA Section Definitions and Structures ...
//
//     The next level of data organization under the OCA data division
//     is the data "section".  Sections are completely contained within
//     their parent "divisions".
//
// Different section header types are organized into a hierarchy, think of it as inheritance:
//
// - OCA_SECTION_HDR_BASE
//      - OCA_COM_SECTION_HDR_BASE
//          - OCA_LABELED_SECTION_HDR_0x141
//          - OCA_COM_SECTION_HDR_0x142
//              - OCA_LABELED_SECTION_HDR_0x142
//      - OCA_REG_SECTION_HDR
//
// All section header types have first two fields being Size and Type, and OCA_PARSER would
// traverse the sections using OCA_SECTION_HDR_BASE.
//
// **IMPORTANT** To add a new field to section header:
//
//  ** Changing the section header requires increment to HeaderID **
//  1. Make a copy of OCA_SECTION_HDR_BASE (or the latest vesion of OCA_SECTION_HDR) and name
//     the new header struct with a new HeaderID (e.g. OCA_SECTION_HDR_0x145)
//  2. Add the new field to the newly created header struct.
//  3. Change the OCA_xxx_SECTION_HDR typedef to the latest version of the header, driver will
//     always use this(the latest version)
//  4. Make sure the KmOCA source code accessing section header casts to the correct header
//     version based on header ID.
//  Note that there're different types of Section headers: COM/LABELED/REG
//  Above steps are essential in keeping the KmOCA backward compatible!
//
//***********************************************************************************************//

// Conditions triggering Register List contents to be dumped
// into the OCA/TDR report.
typedef enum _TDR_REG_ACTIONS_REC
{
    TDR_READ_SKIP          = 0, // Skip reading this register
    TDR_READ_UNCONDITIONAL = 1, // Always read and dump register contents
    TDR_READ_NOT_EQUAL     = 2, // Read and dump if contents != Value
    TDR_READ_BIT_SET       = 3, // Read and dump if contents contain
                                // a bit set that's also set in Value
    TDR_READ_BIT_CLEAR = 4      // Read and dump if contents contain
                                // a bit clear that's set in Value.
} TDR_REG_ACTIONS;

// Format of information in a data section.
typedef enum _OCA_SECTION_TYPE_REC
{
    OCA_SECT_REG_LIST = 1,               // Section contains Register List
                                         // output.  Data in this section is
                                         // formatted as a string of
                                         // OCA_REG_LIST_OUT structures.
    OCA_SECT_REG_RANGE = 2,              // Section contains Register Range
                                         // output.  Data is formatted as an
                                         // array of DWORDs.
    OCA_SECT_DRV_STRUCT = 3,             // Section contains driver structure(s).
                                         // Data are formatted according to the
                                         // driver's structure name given in
                                         // 'SectionName'.
    OCA_SECT_GPU_CMDS = 4,               // Section contains GPU commands which
                                         // can be interpreted by AUBLIST.
    OCA_SECT_UNDEF_BINARY = 5,           // Section contains undefined binary data
                                         // and is formatted as an array of
                                         // DWORDs.
    OCA_SECT_TEXT_ERROR_MSG = 6,         // A text error message is stored
                                         // in this section.
    OCA_SECT_LABELED_DRV_STRUCT = 7,     // Section contains driver structure(s).
                                         // Data are formatted according to the
                                         // driver's structure name given in
                                         // the 'StructName' character field
                                         // placed in the first portion of the
                                         // section data area..
    OCA_SECT_TEXT_ERROR_LABELED_MSG = 8, // A text error message is stored
                                         // in this labeled section.
    OCA_SECT_GENERIC_GFX = 9,            // Section contains binary graphics data

    OCA_BUF_DBG_MSGS = 10, // Section contains Text debug msg strings
} OCA_SECTION_TYPE;

// State of the Header for tracking in tool
typedef enum _OCA_DATA_STATE_REC
{
    OCA_DIVISION_INVALID = 0, // TODO: Name should be changed as it is used by sections also
    OCA_DIVISION_VALID   = 1
} OCA_DATA_STATE;

//------------------------------------------------------
// Base section header, all section headers must have the fields of this struct at beginning
typedef struct _OCA_SECTION_HDR_BASE_ST
{
    ULONG            Size; // Section size (including header)
    OCA_SECTION_TYPE Type; // Section type
} OCA_SECTION_HDR_BASE;

// OCA section header within the register division
typedef struct _OCA_REG_SECTION_HDR_ST
{
    ULONG            Size; // Section size (including header)
    OCA_SECTION_TYPE Type; // Section type
                           // 1 = Register list
                           // 2 = Register range
    //==================================================================
    union {
        struct
        {                      // --- OCA_SECT_REG_LIST ---
            ULONG NumListRegs; // Num registers in list
        } OcaSectionRegList;

        struct
        {                       // --- OCA_SECT_REG_RANGE ---
            ULONG StartOffset;  // Start register offset
            ULONG NumRangeRegs; // Number of registers in range
        } OcaSectionRegRange;
    };
} OCA_REG_SECTION_HDR;

//------------------------------------------------------
// OCA section header within component divisions

#define OCA_SECTION_NAME_SIZE 32

#define OCA_SECTION_NAME_MMDMM_TDR_DBG_GENERAL_INFO "MMDMM_TDR_DBG_GENERAL_INFO"
#define OCA_SECTION_NAME_MMDMM_TDR_DBG_CV_HISTORY_DATA "MMDMM_TDR_DBG_CV_HISTORY_DATA"
#define OCA_SECTION_NAME_MMDMM_TDR_DBG_SSA_HISTORY_DATA "MMDMM_TDR_DBG_SSA_HISTORY_DATA"
#define OCA_SECTION_NAME_MMDMM_TDR_DBG_SSV_HISTORY_DATA "MMDMM_TDR_DBG_SSV_HISTORY_DATA"
#define OCA_SECTION_NAME_MMDMM_VBI_CTRL_HISTORY_DATA "MMDMM_VBI_CTRL_HISTORY_DATA"
#define OCA_SECTION_NAME_MMDMM_TDR_DBG_VBI_HISTORY_DATA "MMDMM_TDR_DBG_VBI_HISTORY_DATA"
#define OCA_SECTION_NAME_MMDMM_TDR_DBG_MPO_HISTORY_DATA "MMDMM_TDR_DBG_MPO_HISTORY_DATA"
#define OCA_SECTION_NAME_MMDMM_VBI_PROBLEM_TRACKER "MMDMM_VBI_PROBLEM_TRACKER"
#define OCA_SECTION_NAME_DMA_TYPE "DMA Type"

typedef struct _OCA_COM_SECTION_HDR_BASE_ST // inherit OCA_SECTION_HDR_BASE
{
    ULONG            Size; // Section size (including header)
    OCA_SECTION_TYPE Type; // Section type
                           // 3 = Driver structure
                           // 4 = GPU commands (AUBLIST)
                           // 5 = Undefined binary data
                           // 6 = Text error message
                           // 7 = Driver structure (struct
                           //     name in section data area
    //==================================================================
    char SectionName[OCA_SECTION_NAME_SIZE]; // ASCII section name
} OCA_COM_SECTION_HDR_BASE;
typedef struct _OCA_COM_SECTION_HDR_0x142_ST // inherit OCA_COM_SECTION_HDR_BASE
{
    ULONG            Size;                               // Section size (including header)
    OCA_SECTION_TYPE Type;                               // Section type (same as OCA_COM_SECTION_0x141)
    char             SectionName[OCA_SECTION_NAME_SIZE]; // ASCII section name
    //==================================================================
    ULONG SectionState; // Notify if the section is valid or not
} OCA_COM_SECTION_HDR_0x142;
// Current component section header (used by driver)
typedef OCA_COM_SECTION_HDR_0x142 OCA_COM_SECTION_HDR;
//------------------------------------------------------
// OCA specialized 'labeled section' header

#define OCA_STRUCT_NAME_SIZE 32

// Labelled section 0x115/116/117/141
typedef struct _OCA_LABELED_SECTION_HDR_0x141_ST
{
    OCA_COM_SECTION_HDR_BASE SectionHdr;                       // Component section header
    char                     StructName[OCA_STRUCT_NAME_SIZE]; // ASCII structure name
} OCA_LABELED_SECTION_HDR_0x141;
// Labelled section 0x142, added SectionState in SectionHdr
typedef struct _OCA_LABELED_SECTION_HDR_0x142_ST
{
    OCA_COM_SECTION_HDR_0x142 SectionHdr;                       // Component section header
    char                      StructName[OCA_STRUCT_NAME_SIZE]; // ASCII structure name
} OCA_LABELED_SECTION_HDR_0x142;
// Current labelled section (used by driver)
typedef OCA_LABELED_SECTION_HDR_0x142 OCA_LABELED_SECTION_HDR;

//------------------------------------------------------
// Read action structure for registers lists.  A register's contents
// will be included in the OCA/TDR report if the "Value" matches what
// is required by "Action" (one of TDR_REG_ACTIONS operations).
typedef struct _OCA_REG_LIST_ST
{
    ULONG Offset : 22; // Register offset
    ULONG Action : 10; // Action to perform on register
    ULONG Value;       // Use depends on "Action"
} OCA_REG_LIST;

//------------------------------------------------------
// Definition for register ranges.  All register in the range are read
// and their contents output to the OCA report.
typedef struct _OCA_REG_RANGE_ST
{
    ULONG StartOffset : 22; // Start register offset
    ULONG NumRegs : 10;     // Number of registers to read
} OCA_REG_RANGE;

//------------------------------------------------------
// Format of individual register output in the OCA report
typedef struct _OCA_REG_LIST_OUT_ST
{
    ULONG Offset;   // Register offset (address)
    ULONG Contents; // Register contents
} OCA_REG_LIST_OUT;

//------------------------------------------------------
// Format of individual entry in generic graphics memory section.
#define NUM_GFX_DWORDS 4
typedef struct _GENERIC_GFX_MEM_ST
{
    ULONG Address;              // Memory address
    DWORD Data[NUM_GFX_DWORDS]; // Four DWords at this address.
} GENERIC_GFX_MEM;

#define OCA_OPCODE_MI_NOOP_WRITE_ENABLE_CMP_MASK (0xffc00000)

// Reset packing alignment to project default
#pragma pack(pop)

#endif //_OCA_H_
