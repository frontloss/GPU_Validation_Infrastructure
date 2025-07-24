#pragma once

#ifndef __VBTSIMULATION_H__
#define __VBTSIMULATION_H__

#include "..\\DriverInterfaces\\PlatformInfo.h"

#define MIN_VBT_SIZE (1024 * 6)

// PCI Bus
#define PCI_BUS 0
// DEVICE 0 of PCI BUS
#define PCI_CTL_DEVICE 0
// DEVICE 2 of PCI BUS - most for Gfx
#define PCI_GFX_DEVICE 2

// Function of each PCI Device
#define PCI_FUNCTION_0 0

#define PCI_MEM_OPREGION_PHYSICAL_ADDR_REGISTER 0xFC
#define OPREGION_SIGNATURE "IntelGraphicsMem" // Opregion Signature
#define NUM_SIGNATURE_BYTES 16
#define CPD_SIGNATURE "$CPD" // CPD Signature
#define NUM_CPD_BYTES 4
#define TOTAL_OPREGION_SIZE (8 * 1024) // Opregion size
#define OPROM_BYTE_BOUNDARY 512        // OPROM image sizes are indicated in 512 byte boundaries

#define OPROM_INITIAL_READ_SIZE (64 * 1024) // Read 64 Kilobytes to get the entire oprom data required for authentication in single read

#define PCI_IMAGE_LENGTH_OFFSET 0x10
#define PCI_IMAGE_LENGTH_SIZE 1
#define PCI_LAST_IMAGE_INDICATOR_OFFSET 0x15
#define PCI_LAST_IMAGE_INDICATOR_MASK 0x80
#define PCI_CODE_TYPE_OFFSET 0x14

#define MAJOR_VERSION_2 2
#define MINOR_VERISON_0 0

#define KB_TO_BYTE(KB) (KB * 1024)

//------------------------------------------------------------------------------
//
// MailBox (4): Used to get VBT from system BIOS
//
//------------------------------------------------------------------------------
#define MAILBOX4_OFFSET 0x400     // Offset[0x400] : VBT table starts here and ends until VBT size.
#define VBT_MAILBOX_SIZE 6 * 1024 // 6KB space is pre-reserved for VBT End Offset = 0x1BFF

#define DD_MAX_REGISTRY_PATH_LENGTH 256
#define MB2_BCLM_FIELD_SIZE 30

#define SIMDRV_REGKEY_ACTUAL_VBT L"_ActualVBT"
#define SIMDRV_REGKEY_DEFAULT_VBT L"_DefaultVBT"
#define SIMDRV_REGKEY_VBTSIMULATION L"VBTSimulation"
#define SIMDRV_REGKEY_CUSTOM_VBT L"_CustomVBT"
#define SIMDRV_REGKEY_CUSTOM_VBT_SIZE L"_CustomVBTSize"

#define SIMDRV_REGKEY_ACTUAL_OPROM_HEADER L"_ActualOpromHeader"
#define SIMDRV_REGKEY_ACTUAL_OPROM_FOOTER L"_ActualOpromFooter"
#define SIMDRV_REGKEY_CUSTOM_OPROM L"_CustomOprom"
#define SIMDRV_REGKEY_CUSTOM_OPROM_SIZE L"_CustomOpromSize"

#define SIMDRV_REGKEY_ACTUAL_OPREGION L"_ActualOpRegion"

#define SIMDRV_REGKEY_TEST_MMIO_DATA L"_TestMmioData"

#define _SIZE L"_Size"

typedef struct _SIMDRV_OPREGION_VBT_DETAILS
{
    DDU8 *pCodeOpRomBase;
    DDU32 OPRomSize;
    DDU32 OPRomHeaderSize;
    DDU32 OPRomFooterSize;

    DDU8 *pOpregionBaseVirtualAddr;
    DDU32 OpRegionSize;
    DDU8 *pVBTBase;
    DDU32 VbtSize;

    BOOLEAN bUnmapVirtualAddr;

} SIMDRV_OPREGION_VBT_DETAILS, *PSIMDRV_OPREGION_VBT_DETAILS;

typedef union _OPROM_HEADER {
    DDU32 Data;
    struct
    {
        DDU16 Signature;      // Offset[0x0]: Header 0x55 0xAA
        DDU8  SizeIn512Bytes; // Offset[0x2]: Oprom size in 512 bytes
        DDU8  Reserved;       // Reserved
    };
} OPROM_HEADER;

typedef struct _EXPANSION_ROM_HEADER
{
    OPROM_HEADER Header;          // Offset[0x0]: Oprom Header
    DDU16        VbiosPostOffset; // Offset[0x4]: Will be 0 in GOP case, else pointer to VBIOS entry point
    DDU8         Resvd[0x12];     // Offset[0x6]: Reserved
    DDU16        PciStructOffset; // Offset[0x18]: Contains pointer to a list of supported device IDs
    DDU16        OpregionBase;    // Offset[0x1A]: Offset to Opregion Base start
} EXPANSION_ROM_HEADER, *PEXPANSION_ROM_HEADER;

typedef union _OPREGION_VER {
    DDU32 Value;
    struct
    {
        DDU32 Reserved : 8;
        DDU32 Revision : 8;
        DDU32 MinorVersion : 8;
        DDU32 MajorVersion : 8;
    };
} OPREGION_VER;

typedef struct _OPREGION_HEADER
{
    DDU8         OpRegionSignature[0x10];   // Offset[0x00]  : Bios needs to put OPREGION_SIGNATURE here
    DDU32        OpregionSize;              // Offset[0x10]  : This is supposed to be 8KB
    OPREGION_VER OpregionVersion;           // Offset[0x14]  : Of type OPREGION_VER
    DDU8         SysBiosBuildVersion[0x20]; // Offset[0x18]  : BIOS version used for debug purpose (Optional)
    DDU8         VideoBiosVersion[0x10];    // Offset[0x38]  : Video BIOS version (if VBIOS is loaded)
    DDU8         GfxDriverversion[0x10];    // Offset[0x48]  : Graphics driver version (Optional)
    DDU32        OpregionSuportedMailbox;   // Offset[0x58]  : This is of type OPREGION_SUPPORTED_MAILBOXES
    DDU32        DriverModel;               // Offset[0x5C]  : Driver Model of type OPREG_DRV_MODEL
    DDU32        PlatformConfiguration;     // Offset[0x60]  : Platform  of type PLATFORM_CONFIG
    DDU8         GopBuildVersion[0x20];     // Offset[0x64]  : GOP build version #
} OPREGION_HEADER;

#pragma pack(1)
//------------------------------------------------------------------------------
//
// OPREGION_MAILBOX3: Used to get VBT
//
//------------------------------------------------------------------------------

#define DD_MB3_BCLM_FIELD_SIZE 20
#define DD_MB2_BCLM_FIELD_SIZE 30

// BCLM Data Word
typedef struct _DD_MB3_BCLM_MAPPING_
{
    union {
        DDU16 BclmData;
        struct
        {
            DDU16 DutyCycle : 8; // Inverter Duty Cycle
            DDU16 Percent : 7;   // Brightness Percent
            DDU16 ValidBit : 1;  // Data Valid bit
        };
    };
} DD_MB3_BCLM_MAPPING;

// MB2 BCL fields
typedef union _DD_MB2_BCL_FIELD {
    DDU32 Brightness;
    struct
    {
        DDU32 BlcValue : 8;
        DDU32 Reserved : 23; // Reserved Bits
        DDU32 ValidBit : 1;  // Validity bit for the field
    };
} DD_MB2_BCL_FIELD;

// MB2 BCM value
typedef union _DD_MB2_BCM_FIELD {
    DDU32 Value;
    struct
    {
        DDU32 DesiredDutyCycle : 16; // Indicates the brightness level for LFP1 and LFP2
        DDU32 BrightnessPercent : 7; // Indicates Brightness Percentage
        DDU32 Reserved : 8;          // Reserved Bits
        DDU32 FieldValidBit : 1;     // Validity bit for the field
    };
} DD_MB2_BCM_FIELD;

// Brightness data
typedef struct _DD_MB3_BRIGHTNESS
{
    union {
        DDU32 Brightness;
        struct
        {
            DDU32 BlcValue : 16; // Backlight Brightness value in % format specified in bits[29:28]
            DDU32 Reseved : 12;  // Bits[27:16] - Reserved
            DDU32 BlcFormat : 2; // Backlight % format for bits[15:0]
            DDU32 Reseved1 : 1;  // Bit[30] - Reserved
            DDU32 ValidBit : 1;  // Data Valid bit
        };
    };
} DD_MB3_BRIGHTNESS;

// Opregion MAILBOX2 Fields
typedef struct _OPREGION_MAILBOX2
{
    DD_MB2_BCL_FIELD BacklightBrightnessLfp1;                                  // Offset[0x200]: backlight brightness to be set for LFP Panel 1
    DD_MB2_BCL_FIELD BacklightBrightnessLfp2;                                  // Offset[0x204]: backlight brightness to be set for LFP Panel 2
    DDU32            CurrentUserBrighnessLevelLfp1;                            // Offset[0x208]: current brightness level set from driver for LFP 1
    DDU32            CurrentUserBrighnessLevelLfp2;                            // Offset[0x20C]: current brightness level set from driver for LFP 2
    DD_MB2_BCM_FIELD BrightnessLevelDutyCycleMappingLfp1[MB2_BCLM_FIELD_SIZE]; // Offset[0x210]: 0x00 t0 0x64 are valid values. 0x65 to 0xFF are reserved values (LFP1)
    DD_MB2_BCM_FIELD BrightnessLevelDutyCycleMappingLfp2[MB2_BCLM_FIELD_SIZE]; // Offset[0x288]: 0x00 t0 0x64 are valid values. 0x65 to 0xFF are reserved values (LFP2)
} OPREGION_MAILBOX2;

typedef union _TCHE_FLD {
    DDU32 Value;
    struct
    {
        DDU32 ALSEvent : 1;              // Indicate ALS Event  BIT0
        DDU32 BLCEvent : 1;              // Indicate BLC Event  BIT1
        DDU32 PFITEvent : 1;             // Indicate PFIT Event BIT2
        DDU32 PFMBEvent : 1;             // Indicate PFMB Event BIT3
        DDU32 GRSEvent : 1;              // Indicate GRS Event  BIT4
        DDU32 KeyPressEvent : 1;         // Indicate Key press Event BIT5
        DDU32 SltNBConvEvent : 1;        // Indicate Slate to Notebook or Vice versa Conversion Event BIT6
        DDU32 SltDckEvent : 1;           // Indicate Dock state of a Tablet Event BIT7
        DDU32 ISCTEvent : 1;             // Indicate iSCT Event  BIT8
        DDU32 UNIQUENAME(Reserved) : 23; // Reserved BIT9-BIT31
    };
} TCHE_FLD;

typedef struct _LUT_HEADER
{
    DDU8 IsSysBiosPanelIdForFakeEDID : 1;  // Override LUT only for EDIDLess panels
    DDU8 IsSysBiosPanelIdForEDIDPanel : 1; // Override LUT only for EDID panels
    DDU8 IsLUTTablePresent : 1;            // Is LUT present
    DDU8 IsRegistryLUTPreferred : 1;       // Is registry entry if present preferred over this LUT
    DDU8 UNIQUENAME(Reserved) : 4;         // Reserved
} LUT_HEADER;

typedef struct _OPREGION_PNP_ID
{
    DDU16 IdMfgName;     // ID Manufacturer Name
    DDU16 IdProductCode; // ID Product Code
    DDU32 IdSerialNum;   // ID Serial Number
    DDU8  IDMfgWeek;     // Week of Manufacture
    DDU8  IDMfgYear;     // Year of Manufacture
} OPREGION_PNP_ID;

#define MAILBOX3_OFFSET 0x300

typedef struct _OPREGION_MAILBOX3
{
    DDU32               ARDYField;                         // Offset[0x300]: Driver readiness for ASLE interrupts, Of type ARDY_DRIVER_READINESS
    DDU32               ASLCField;                         // Offset[0x304]: ASLE interrupt commmand, Of type DRIVER_READINESS
    TCHE_FLD            TCHEField;                         // Offset[0x308]: Technology enabled status Indictor, Of type TCHE_FLD
    DDU32               ALSIField;                         // Offset[0x30C]: Current ALS Illuminance Reading, Of type ALS_FIELD
    DD_MB3_BRIGHTNESS   BCLPReadField;                     // Offset[0x310]: Backlight brightness, Of type BLC_FIELD
    DDU32               PFITField;                         // Offset[0x314]: Panel Fitting, Of type PFIT_FIELD
    DD_MB3_BRIGHTNESS   BCLPWriteField;                    // Offset[0x318]: Current User Brightness Level, Of type BLC_FIELD
    DD_MB3_BCLM_MAPPING BCLMField[DD_MB3_BCLM_FIELD_SIZE]; // Offset[0x31C]: Backlight Brightness Level Duty Cycle Mapping Table, Of type BCLM_MAPPING
    DDU32               CPFMField;                         // Offset[0x344]: Current Panel Fitting Mode, Of type PFIT_FIELD
    DDU32               EPFMField;                         // Offset[0x348]: Enabled Panel Fitting Modes, Of type PFIT_FIELD
    LUT_HEADER          LUTHeader;                         // Offset[0x34C]: Obsolete; Panel LUT header, Of type LUT_HEADER
    OPREGION_PNP_ID     PanelPnpId;                        // Offset[0x34D]: Obsolete; Panel LUT header, Of type LUT_HEADER
    DDU8                PLUTField[63];                     // Offset[0x35D]: Obsolete; Panel LUT from BIOS
    DDU32               PFMBField;                         // Offset[0x396]: PWM Frequency and Minimum Brightness, Of type PFMB_FIELD
    DDU32               CCDVField;                         // Offset[0x39A]: Color Correction Default Values, Of type CCDV_FIELD
    DDU32               PCFTField;                         // Offset[0x39E]: Obsolete; Power Conservation Features , Of type PCFT_FIELD
    DDU32               SROTField;                         // Offset[0x3A2]: Supported Rotation Angles, Of type GRS_FIELD
    DDU32               IUERField;                         // Offset[0x3A6]: Intel UltraBook Event Register , Of type IUER_FIELD
    DDU64               IFFSAddressField;                  // Offset[0x3AA]: Address of DSS Buffer for iFFS feature
    DDU32               IFFSSizeField;                     // Offset[0x3B2]: Size of DSS Buffer allocated
    DDU32               ISCTField;                         // Offset[0x3B6]: State Indicator holds the values of States based on feature, Of type ISCT_FIELD
    DDU64               RVDAField;                         // Offset[0x3BA]: Physical Address of Raw VBT Data (Incase VBT size > 6KB and wont hold in MailBox 4)
    DDU32               RVDSField;                         // Offset[0x3C2]: Size of Raw VBT Data allocated
    DDU8                Reserved[56];                      // Reserved
} OPREGION_MAILBOX3;
#pragma pack()

// Helper Functions
BOOLEAN VBTSIMULATION_IsDefaultVBTPresent(GFX_ADAPTER_CONTEXT gfxAdapterContext, PSIMDRV_OPREGION_VBT_DETAILS pOpRegionVbtDetails);
BOOLEAN VBTSimulation_DeleteDefaultVBT(GFX_ADAPTER_CONTEXT gfxAdapterContext);

// Function to Dump VBT to registry
VOID VBTSIMULATION_DumpVBTFromPCI(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PSIMDRV_OPREGION_VBT_DETAILS pOpRegionVbtDetails);

// Function to Dump OpRegion to registry
VOID VBTSIMULATION_DumpOpRegionFromPCI(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PSIMDRV_OPREGION_VBT_DETAILS pOpRegionVbtDetails);

VOID VBTSIMULATION_DumpVBTToETW();
// Function to Dump VBT to configure custom VBT from registry
VOID VBTSIMULATION_ConfigureTestVBT(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PSIMDRV_OPREGION_VBT_DETAILS pOpRegionVbtDetails, BOOLEAN bVBTSimulationFlag);
VOID VBTSIMULATION_WriteDefaultVBT(GFX_ADAPTER_CONTEXT gfxAdapterContext, DDU8* pVBTBase, DDU32 VbtSize);

BOOLEAN VBTSIMULATION_GetOpregionDetails(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PLATFORM_INFO stPlatformInfo, PSIMDRV_OPREGION_VBT_DETAILS pOpRegionVbtDetails);

VOID VBTSIMULATION_Cleanup(PGFX_ADAPTER_CONTEXT pGfxAdapterContext);
#endif