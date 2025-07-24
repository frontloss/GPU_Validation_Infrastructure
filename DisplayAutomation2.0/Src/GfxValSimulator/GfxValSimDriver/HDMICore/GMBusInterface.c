#include "GMBUSInterface.h"
#include "..\CommonInclude\ETWLogging.h"

static UINT8(*g_ulEdid);
static UINT8(*g_ulscdcdata);
static UINT8(*g_ulAdapterdata);

UINT8 g_HDMIPortB[] = { 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x30, 0xAE, 0xE4, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x01, 0x04, 0x95, 0x1C, 0x10, 0x78, 0xEA, 0x36,
                        0x25, 0x93, 0x56, 0x55, 0x93, 0x29, 0x1D, 0x50, 0x54, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
                        0x01, 0x01, 0xD2, 0x37, 0x80, 0xA2, 0x70, 0x38, 0x40, 0x40, 0x30, 0x20, 0x55, 0x00, 0x14, 0x9B, 0x10, 0x00, 0x00, 0x19, 0xD2, 0x37, 0x80, 0xA2, 0x70, 0x38,
                        0x40, 0x40, 0x30, 0x20, 0x55, 0x00, 0x14, 0x9B, 0x10, 0x00, 0x00, 0x19, 0x00, 0x00, 0x00, 0x0F, 0x00, 0xD1, 0x09, 0x30, 0xD1, 0x09, 0x28, 0x28, 0x0A, 0x00,
                        0x4C, 0x83, 0x47, 0x31, 0x00, 0x00, 0x00, 0xFE, 0x00, 0x4C, 0x54, 0x4E, 0x31, 0x32, 0x35, 0x48, 0x4C, 0x30, 0x33, 0x34, 0x30, 0x31, 0x00, 0x5A };

UINT8 g_HDMIPortC[] = { 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x30, 0xAE, 0xE4, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x01, 0x04, 0x95, 0x1C, 0x10, 0x78, 0xEA, 0x36,
                        0x25, 0x93, 0x56, 0x55, 0x93, 0x29, 0x1D, 0x50, 0x54, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
                        0x01, 0x01, 0xD2, 0x37, 0x80, 0xA2, 0x70, 0x38, 0x40, 0x40, 0x30, 0x20, 0x55, 0x00, 0x14, 0x9B, 0x10, 0x00, 0x00, 0x19, 0xD2, 0x37, 0x80, 0xA2, 0x70, 0x38,
                        0x40, 0x40, 0x30, 0x20, 0x55, 0x00, 0x14, 0x9B, 0x10, 0x00, 0x00, 0x19, 0x00, 0x00, 0x00, 0x0F, 0x00, 0xD1, 0x09, 0x30, 0xD1, 0x09, 0x28, 0x28, 0x0A, 0x00,
                        0x4C, 0x83, 0x47, 0x31, 0x00, 0x00, 0x00, 0xFE, 0x00, 0x4C, 0x54, 0x4E, 0x31, 0x32, 0x35, 0x48, 0x4C, 0x30, 0x33, 0x34, 0x30, 0x31, 0x00, 0x5A };

UINT8 g_HDMIPortD[] = { 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x30, 0xAE, 0xE4, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x01, 0x04, 0x95, 0x1C, 0x10, 0x78, 0xEA, 0x36,
                        0x25, 0x93, 0x56, 0x55, 0x93, 0x29, 0x1D, 0x50, 0x54, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
                        0x01, 0x01, 0xD2, 0x37, 0x80, 0xA2, 0x70, 0x38, 0x40, 0x40, 0x30, 0x20, 0x55, 0x00, 0x14, 0x9B, 0x10, 0x00, 0x00, 0x19, 0xD2, 0x37, 0x80, 0xA2, 0x70, 0x38,
                        0x40, 0x40, 0x30, 0x20, 0x55, 0x00, 0x14, 0x9B, 0x10, 0x00, 0x00, 0x19, 0x00, 0x00, 0x00, 0x0F, 0x00, 0xD1, 0x09, 0x30, 0xD1, 0x09, 0x28, 0x28, 0x0A, 0x00,
                        0x4C, 0x83, 0x47, 0x31, 0x00, 0x00, 0x00, 0xFE, 0x00, 0x4C, 0x54, 0x4E, 0x31, 0x32, 0x35, 0x48, 0x4C, 0x30, 0x33, 0x34, 0x30, 0x31, 0x00, 0x5A };

#define TYPE2_ADAPTER_STRING 0xA0
#define LSPCON_ADAPTER_STRING 0xA8
#define TYPE1_ADAPTER_STRING_SIZE 16
#define ADAPTER_STRING_SIZE 17

UINT32 g_HDMISegmentPointer = 0;

// As defn in spec "DP-HDMI ADAPTOR "
static DDU8 Type1Adapter[16] = { 0x44, 0x50, 0x2D, 0x48, 0x44, 0x4D, 0x49, 0x20, 0x41, 0x44, 0x41, 0x50, 0x54, 0x4F, 0x52, 0x04 };

// "DP-HDMI ADAPTOR + 0xA0 for DP type 2 dongle
static DDU8 Type2Adapter[0x1D] = { 0x44, 0x50, 0x2D, 0x48, 0x44, 0x4D, 0x49, 0x20, 0x41, 0x44, 0x41, 0x50, 0x54, 0x4F, 0x52, 0x04, TYPE2_ADAPTER_STRING,
                                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xF0 };

// "DP-HDMI ADAPTOR + 0xA0 for DP type 2 Parade PS8469 dongle
static DDU8 Type2Adapter_PS8469[0x1E] = { 0x44, 0x50, 0x2D, 0x48, 0x44, 0x4D, 0x49, 0x20, 0x41, 0x44, 0x41, 0x50, 0x54, 0x4F, 0x52, 0x04, TYPE2_ADAPTER_STRING,
                                          0x00, 0x1C, 0xF8, 0x50, 0x53, 0x38, 0x34, 0x36, 0x39, 0xA2, 0x00, 0x00, 0xF0 };

// DVI adaptor string
static DDU8 DviAdapter[17] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, TYPE2_ADAPTER_STRING };

// LSPCON adaptor string
static DDU8 LsPconAdapter[17] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, LSPCON_ADAPTER_STRING };

// SCDC Port Data  - Currently using below static data - Later plan is to integrate in our Automation 2.0 Plug API for HDMI
// Current - We get Read request for following Index
// Read Index = 0x01 Sink Version = which we have set to 0x1
// Read Index = 0x21 Scrambler_Status = which we have set to 0x1
// SCDC - Write is ignorred as of now ( based on +ve / -Ve test requirement in future - we have to handle - TBD)
// SCDC - Write requirement as on WW 48.4-2017 - none.

UINT8 g_HDMIPortSCDC[] = { 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x5E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };

// Below function would create new GMBus Object and initializes platform and pch product family.
PGMBUS_INTERFACE GMBusInterface_GetSingletonGMBusObject(IGFX_PLATFORM eIGFXPlatform, PCH_PRODUCT_FAMILY ePCHProductFamily)
{
    PPORTINGLAYER_OBJ pstPortingObj     = GetPortingObj();
    PGMBUS_INTERFACE  pstGMBusInterface = NULL;

    GFXVALSIM_FUNC_ENTRY();

    pstGMBusInterface = (PGMBUS_INTERFACE)pstPortingObj->pfnAllocateMem(sizeof(*pstGMBusInterface), TRUE);
    if (pstGMBusInterface)
    {
        pstGMBusInterface->ulNumRefCount     = 1;
        pstGMBusInterface->eIGFXPlatform     = eIGFXPlatform;
        pstGMBusInterface->ePCHProductFamily = ePCHProductFamily;
    }

    GFXVALSIM_FUNC_EXIT((pstGMBusInterface == NULL) ? 1 : 0);
    return pstGMBusInterface;
}

BOOLEAN GMBusInterface_GetEDIDIndexFromPort(ULONG ulHDMIPort, PULONG pulEDIDIndex)
{
    BOOLEAN bRet = TRUE;
    switch (ulHDMIPort)
    {
    case INTHDMIA_PORT:
    case INTDPA_PORT:
        *pulEDIDIndex = EDID_INDEX_FOR_HDMIA;
        break;
    case INTHDMIB_PORT:
    case INTDPB_PORT:
        *pulEDIDIndex = EDID_INDEX_FOR_HDMIB;
        break;
    case INTHDMIC_PORT:
    case INTDPC_PORT:
        *pulEDIDIndex = EDID_INDEX_FOR_HDMIC;
        break;
    case INTHDMID_PORT:
    case INTDPD_PORT:
        *pulEDIDIndex = EDID_INDEX_FOR_HDMID;
        break;
    case INTHDMIE_PORT:
    case INTDPE_PORT:
        *pulEDIDIndex = EDID_INDEX_FOR_HDMIE;
        break;
    case INTHDMIF_PORT:
    case INTDPF_PORT:
        *pulEDIDIndex = EDID_INDEX_FOR_HDMIF;
        break;
    case INTHDMIG_PORT:
    case INTDPG_PORT:
        *pulEDIDIndex = EDID_INDEX_FOR_HDMIG;
        break;
    case INTHDMIH_PORT:
    case INTDPH_PORT:
        *pulEDIDIndex = EDID_INDEX_FOR_HDMIH;
        break;
    case INTHDMII_PORT:
    case INTDPI_PORT:
        *pulEDIDIndex = EDID_INDEX_FOR_HDMII;
        break;
    default:
        bRet = FALSE;
        break;
    }
    return bRet;
}

/*-----------------------------------------------------------------------*
 *
 *-----------------------------------------------------------------------*/
BOOLEAN GMBusInterface_GetSCDCIndexFromPort(ULONG ulHDMIPort, PULONG pulSCDCIndex)
{
    BOOLEAN bRet = TRUE;
    switch (ulHDMIPort)
    {
    case INTHDMIA_PORT:
    case INTDPA_PORT:
        *pulSCDCIndex = SCDC_INDEX_FOR_HDMIA;
        break;
    case INTHDMIB_PORT:
    case INTDPB_PORT:
        *pulSCDCIndex = SCDC_INDEX_FOR_HDMIB;
        break;
    case INTHDMIC_PORT:
    case INTDPC_PORT:
        *pulSCDCIndex = SCDC_INDEX_FOR_HDMIC;
        break;
    case INTHDMID_PORT:
    case INTDPD_PORT:
        *pulSCDCIndex = SCDC_INDEX_FOR_HDMID;
        break;
    case INTHDMIE_PORT:
    case INTDPE_PORT:
        *pulSCDCIndex = SCDC_INDEX_FOR_HDMIE;
        break;
    case INTHDMIF_PORT:
    case INTDPF_PORT:
        *pulSCDCIndex = SCDC_INDEX_FOR_HDMIF;
        break;
    case INTHDMIG_PORT:
    case INTDPG_PORT:
        *pulSCDCIndex = SCDC_INDEX_FOR_HDMIG;
        break;
    case INTHDMIH_PORT:
    case INTDPH_PORT:
        *pulSCDCIndex = SCDC_INDEX_FOR_HDMIH;
        break;
    case INTHDMII_PORT:
    case INTDPI_PORT:
        *pulSCDCIndex = SCDC_INDEX_FOR_HDMII;
        break;
    default:
        bRet = FALSE;
        break;
    }
    return bRet;
}

/*-----------------------------------------------------------------------*
 *
 *-----------------------------------------------------------------------*/
BOOLEAN GMBusInterface_SetEDIDData(PGMBUS_INTERFACE pstGMBusInterface, ULONG ulEDIDSize, PUCHAR pucEDIDBuff, ULONG ulHDMIPort)
{
    errno_t           eRetError     = 0;
    ULONG             ulEDIDIndex   = EDID_INDEX_INVALID;
    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();
    BOOLEAN           bRet          = GMBusInterface_GetEDIDIndexFromPort(ulHDMIPort, &ulEDIDIndex);

    GFXVALSIM_FUNC_ENTRY();
    if (bRet)
    {
        if (pstGMBusInterface->EdidData[ulEDIDIndex].pucEdidData)
        {
            // Control should not come here..as EDID for each port should get set only once.
            pstPortingObj->pfnFreeMem(pstGMBusInterface->EdidData[ulEDIDIndex].pucEdidData);
            pstGMBusInterface->EdidData[ulEDIDIndex].pucEdidData = NULL;
        }

        pstGMBusInterface->EdidData[ulEDIDIndex].ulEdidDataSize = ulEDIDSize;
        pstGMBusInterface->EdidData[ulEDIDIndex].pucEdidData    = (PUCHAR)pstPortingObj->pfnAllocateMem((ulEDIDSize), TRUE);
        if (pstGMBusInterface->EdidData[ulEDIDIndex].pucEdidData)
        {
            pstGMBusInterface->EdidData[ulEDIDIndex].ulNumEDIDBlocks = (ulEDIDSize / SIZE_EDID_BLOCK);
            pstGMBusInterface->EdidData[ulEDIDIndex].ulHDMIPort      = ulHDMIPort;
            eRetError                                                = memcpy_s(pstGMBusInterface->EdidData[ulEDIDIndex].pucEdidData, ulEDIDSize, pucEDIDBuff, ulEDIDSize);
            if (0 == eRetError)
            {
                bRet = TRUE;
            }
            else
            {
                pstPortingObj->pfnFreeMem(pstGMBusInterface->EdidData[ulEDIDIndex].pucEdidData);
                pstGMBusInterface->EdidData[ulEDIDIndex].pucEdidData = NULL;
            }
        }
    }
    return bRet;
}

/*-----------------------------------------------------------------------*
 *
 *-----------------------------------------------------------------------*/
BOOLEAN GMBusInterface_SetSCDCData(PGMBUS_INTERFACE pstGMBusInterface, ULONG ulSCDCSize, PUCHAR pucSCDCBuff, ULONG ulHDMIPort)
{
    errno_t           eRetError     = 0;
    ULONG             ulSCDCIndex   = SCDC_INDEX_INVALID;
    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();
    BOOLEAN           bRet          = GMBusInterface_GetSCDCIndexFromPort(ulHDMIPort, &ulSCDCIndex);
    if (bRet)
    {
        if (pstGMBusInterface->ScdcData[ulSCDCIndex].pucScdcData)
        {
            // Control should not come here..as EDID for each port should get set only once.
            pstPortingObj->pfnFreeMem(pstGMBusInterface->ScdcData[ulSCDCIndex].pucScdcData);
            pstGMBusInterface->ScdcData[ulSCDCIndex].pucScdcData = NULL;
        }

        pstGMBusInterface->ScdcData[ulSCDCIndex].ulScdcDataSize = ulSCDCSize;
        pstGMBusInterface->ScdcData[ulSCDCIndex].pucScdcData    = (PUCHAR)pstPortingObj->pfnAllocateMem((ulSCDCSize), TRUE);
        if (pstGMBusInterface->ScdcData[ulSCDCIndex].pucScdcData)
        {
            pstGMBusInterface->ScdcData[ulSCDCIndex].ulHDMIPort = ulHDMIPort;
            eRetError                                           = memcpy_s(pstGMBusInterface->ScdcData[ulSCDCIndex].pucScdcData, ulSCDCSize, pucSCDCBuff, ulSCDCSize);
            if (0 == eRetError)
            {
                bRet = TRUE;
            }
            else
            {
                pstPortingObj->pfnFreeMem(pstGMBusInterface->ScdcData[ulSCDCIndex].pucScdcData);
                pstGMBusInterface->ScdcData[ulSCDCIndex].pucScdcData = NULL;
            }
        }
    }
    return bRet;
}

BOOLEAN GMBusInterface_SetDongleType(PGMBUS_INTERFACE pstGMBusInterface, ULONG ulHDMIPort, DONGLE_TYPE eDongleType)
{
    GFXVALSIM_FUNC_ENTRY();
    ULONG   ulEDIDIndex = EDID_INDEX_INVALID;
    BOOLEAN bRet        = GMBusInterface_GetEDIDIndexFromPort(ulHDMIPort, &ulEDIDIndex);

    if (bRet)
    {
        pstGMBusInterface->DongleType[ulEDIDIndex] = eDongleType;
        bRet                                       = TRUE;
    }
    GFXVALSIM_FUNC_EXIT(bRet != TRUE);
    return bRet;
}

ENUM_EDID_PORT_INDEX GMBusInterface_GetEDIDIndex(PGMBUS_INTERFACE pstGMBusInterface, ULONG ulGPIOPin)
{
    ENUM_EDID_PORT_INDEX result = EDID_INDEX_INVALID;

    if (pstGMBusInterface->eIGFXPlatform == eIGFX_JASPERLAKE)
    {
        // For EHL, default pinpair mapping B:2, C:4, D:1(from vbt)
        // For JSL, default pinpair mapping B:2, C:3, D:1(from vbt)
        // From prepare display, we always configuring EHL/JSL, pinpair mapping is B:2, C:4, D:5
        // To be in sync, we are using below pinpair values. Also, to support default pinpair of JSL PortC, we are handling GPIOPin: 0x3
        switch (ulGPIOPin)
        {
        case 0x2:
            result = EDID_INDEX_FOR_HDMIB;
            break;
        case 0x3: // temp workaround for JSP PCH where the default pin pair mapping would be PinpairIndex3
        case 0x9:
            result = EDID_INDEX_FOR_HDMIC;
            break;
        case 0xA:
            result = EDID_INDEX_FOR_HDMID;
            break;
        default:
            break;
        }
    }
    else if (pstGMBusInterface->eIGFXPlatform == eIGFX_SKYLAKE || pstGMBusInterface->eIGFXPlatform == eIGFX_KABYLAKE)
    {
        if (pstGMBusInterface->ePCHProductFamily == PCH_TGL_H || pstGMBusInterface->ePCHProductFamily == PCH_TGL_LP)
        {
            switch (ulGPIOPin)
            {
            case 0x1:
                result = EDID_INDEX_FOR_HDMIA;
                break;
            case 0x2:
                result = EDID_INDEX_FOR_HDMIB;
                break;
            case 0x9:
                result = EDID_INDEX_FOR_HDMIC;
                break;
            case 0xA:
                result = EDID_INDEX_FOR_HDMID;
                break;
            default:
                break;
            }
        }
        else
        {
            switch (ulGPIOPin)
            {
            case 0x5:
                result = EDID_INDEX_FOR_HDMIB;
                break;
            case 0x4:
                result = EDID_INDEX_FOR_HDMIC;
                break;
            case 0x6:
                result = EDID_INDEX_FOR_HDMID;
                break;
            default:
                break;
            }
        }
    }
    else if (pstGMBusInterface->eIGFXPlatform == eIGFX_CANNONLAKE)
    {
        switch (ulGPIOPin)
        {
        case 0x1:
            result = EDID_INDEX_FOR_HDMIB;
            break;
        case 0x2:
            result = EDID_INDEX_FOR_HDMIC;
            break;
        case 0x3:
            result = EDID_INDEX_FOR_HDMID;
            break;
        case 0x4:
            result = EDID_INDEX_FOR_HDMIF;
            break;
        default:
            break;
        }
    }

    else if (pstGMBusInterface->eIGFXPlatform == eIGFX_COFFEELAKE)
    {
        if (pstGMBusInterface->ePCHProductFamily == PCH_TGL_H || pstGMBusInterface->ePCHProductFamily == PCH_TGL_LP)
        {
            switch (ulGPIOPin)
            {
            case 0x1:
                result = EDID_INDEX_FOR_HDMIA;
                break;
            case 0x2:
                result = EDID_INDEX_FOR_HDMIB;
                break;
            case 0x9:
                result = EDID_INDEX_FOR_HDMIC;
                break;
            case 0xA:
                result = EDID_INDEX_FOR_HDMID;
                break;
            default:
                break;
            }
        }
        else
        {
            switch (ulGPIOPin)
            {
            case 0x1:
                result = EDID_INDEX_FOR_HDMIB;
                break;
            case 0x2:
                result = EDID_INDEX_FOR_HDMIC;
                break;
            case 0x3:
                result = EDID_INDEX_FOR_HDMIF;
                break;
            case 0x4:
                result = EDID_INDEX_FOR_HDMID;
                break;
            default:
                break;
            }
        }
    }

    // BSPEC: https://gfxspecs.intel.com/Predator/Home/Index/31299
    else if ((pstGMBusInterface->eIGFXPlatform == eIGFX_ICELAKE_LP) || (pstGMBusInterface->eIGFXPlatform == eIGFX_ROCKETLAKE))
    {
        if (pstGMBusInterface->ePCHProductFamily == PCH_CMP_H)
        {
            switch (ulGPIOPin)
            {
            case 0x1:
                result = EDID_INDEX_FOR_HDMIB;
                break;
            case 0x2:
                result = EDID_INDEX_FOR_HDMIC;
                break;
            case 0x4:
                result = EDID_INDEX_FOR_HDMID;
                break;
            default:
                break;
            }
        }
        else
        {
            switch (ulGPIOPin)
            {
            case 0x1:
                result = EDID_INDEX_FOR_HDMIA;
                break;
            case 0x2:
                result = EDID_INDEX_FOR_HDMIB;
                break;
            case 0x9:
                result = EDID_INDEX_FOR_HDMIC;
                break;
            case 0xA:
                result = EDID_INDEX_FOR_HDMID;
                break;
            case 0xB:
                result = EDID_INDEX_FOR_HDMIE;
                break;
            case 0xC:
                result = EDID_INDEX_FOR_HDMIF;
                break;
            default:
                break;
            }
        }
    }
    else if (pstGMBusInterface->eIGFXPlatform == eIGFX_GEMINILAKE)
    {
        // Reference from: https://gfxspecs.intel.com/Predator/Home/Index/4256?dstFilter=GLK&mode=Filter
        switch (ulGPIOPin)
        {
        case 0x1:
            result = EDID_INDEX_FOR_HDMIB;
            break;
        case 0x2:
            result = EDID_INDEX_FOR_HDMIC;
            break;
        case 0x3:
            // PortD
            result = EDID_INDEX_FOR_HDMID;
            break;
        default:
            break;
        }
    }
    else if ((pstGMBusInterface->eIGFXPlatform == eIGFX_ICELAKE) || (pstGMBusInterface->eIGFXPlatform == eIGFX_LAKEFIELD) ||
             (pstGMBusInterface->eIGFXPlatform == eIGFX_TIGERLAKE_LP) || (pstGMBusInterface->eIGFXPlatform == eIGFX_TIGERLAKE_HP) ||
             (pstGMBusInterface->eIGFXPlatform == eIGFX_RYEFIELD) ||
             (pstGMBusInterface->eIGFXPlatform == eIGFX_LAKEFIELD_R)) // To revisit pin-pair mapping once driver code is ready
    {
        // Reference from: https://gfxspecs.intel.com/Predator/Home/Index/8411
        // GMBUS0[4:0] -->	pinpair select for ICP+
        // VBT Index 1 -->  PinPair1 register which is used for DDI A
        // VBT Index 2 -->  PinPair2 register which is used for DDI B
        // VBT Index 3 -->  PinPair3 register which is used for DDI C
        // VBT Index 4 -->  PinPair9 register which is used for TypeC Port 1
        // VBT Index 5 -->  PinPair10 register which is used for TypeC Port 2
        // VBT Index 6 -->  PinPair11 register which is used for TypeC Port 3
        // VBT Index 7 -->  PinPair12 register which is used for TypeC Port 4
        // VBT Index 8 -->  PinPair13 register which is used for TypeC Port 5
        // VBT Index 9 -->  PinPair14 register which is used for TypeC Port 6
        switch (ulGPIOPin)
        {
        case 0x1:
            result = EDID_INDEX_FOR_HDMIA;
            break;
        case 0x2:
            result = EDID_INDEX_FOR_HDMIB;
            break;
        case 0x3:
            result = EDID_INDEX_FOR_HDMIC;
            break;
        case 0x9:
            result = EDID_INDEX_FOR_HDMID;
            break;
        case 0xA:
            result = EDID_INDEX_FOR_HDMIE;
            break;
        case 0xB:
            result = EDID_INDEX_FOR_HDMIF;
            break;
        case 0xC:
            result = EDID_INDEX_FOR_HDMIG;
            break;
        case 0xD:
            result = EDID_INDEX_FOR_HDMIH;
            break;
        case 0xE:
            result = EDID_INDEX_FOR_HDMII;
            break;
        default:
            break;
        }
    }
    else if (pstGMBusInterface->eIGFXPlatform == eIGFX_DG100)
    {
        // Reference from: https://gfxspecs.intel.com/Predator/Home/Index/33857
        // GMBUS0[4:0] -->	pinpair select for DG100
        // VBT Index 1 -->  PinPair1 register which is used for DDI A
        // VBT Index 2 -->  PinPair2 register which is used for DDI B
        // VBT Index 3 -->  PinPair3 register which is used for DDI C
        // VBT Index 4 -->  PinPair4 register which is used for DDI D
        switch (ulGPIOPin)
        {
        case 0x1:
            result = EDID_INDEX_FOR_HDMIA;
            break;
        case 0x2:
            result = EDID_INDEX_FOR_HDMIB;
            break;
        case 0x3:
            result = EDID_INDEX_FOR_HDMIC;
            break;
        case 0x4:
            result = EDID_INDEX_FOR_HDMID;
            break;
        default:
            break;
        }
    }
    else if (pstGMBusInterface->eIGFXPlatform == eIGFX_DG2)
    {
        // Reference from: https://gfxspecs.intel.com/Predator/Home/Index/33857
        // GMBUS0[4:0] -->	pinpair select for DG100
        // VBT Index 1 -->  PinPair1 register which is used for DDI A
        // VBT Index 2 -->  PinPair2 register which is used for DDI B
        // VBT Index 3 -->  PinPair3 register which is used for DDI C
        // VBT Index 4 -->  PinPair4 register which is used for DDI D
        // VBT Index 9 -->  PinPair4 register which is used for DDI F
        switch (ulGPIOPin)
        {
        case 0x1:
            result = EDID_INDEX_FOR_HDMIA;
            break;
        case 0x2:
            result = EDID_INDEX_FOR_HDMIB;
            break;
        case 0x3:
            result = EDID_INDEX_FOR_HDMIC;
            break;
        case 0x4:
            result = EDID_INDEX_FOR_HDMID;
            break;
        case 0x9:
            result = EDID_INDEX_FOR_HDMIF;
            break;
        default:
            break;
        }
    }
    // BSPEC: https://gfxspecs.intel.com/Predator/Home/Index/49306
    else if (pstGMBusInterface->eIGFXPlatform == eIGFX_ALDERLAKE_S)
    {
        switch (ulGPIOPin)
        {
        case 0x1:
            result = EDID_INDEX_FOR_HDMIA;
            break;
        case 0x9:
            result = EDID_INDEX_FOR_HDMIB;
            break;
        case 0xA:
            result = EDID_INDEX_FOR_HDMIC;
            break;
        case 0xB:
            result = EDID_INDEX_FOR_HDMID;
            break;
        case 0xC:
            result = EDID_INDEX_FOR_HDMIE;
            break;
        default:
            break;
        }
    }
    // BSPEC: https://gfxspecs.intel.com/Predator/Home/Index/49306
    else if (pstGMBusInterface->eIGFXPlatform == eIGFX_ALDERLAKE_P || pstGMBusInterface->eIGFXPlatform == eIGFX_ALDERLAKE_N ||
             pstGMBusInterface->eIGFXPlatform == eIGFX_METEORLAKE || pstGMBusInterface->eIGFXPlatform == eIGFX_ARROWLAKE || pstGMBusInterface->eIGFXPlatform == eIGFX_ELG ||
             pstGMBusInterface->eIGFXPlatform == eIGFX_LUNARLAKE || pstGMBusInterface->eIGFXPlatform == eIGFX_PTL || pstGMBusInterface->eIGFXPlatform == eIGFX_NVL ||
             pstGMBusInterface->eIGFXPlatform == eIGFX_NVL_AX || pstGMBusInterface->eIGFXPlatform == IGFX_NVL_XE3G || pstGMBusInterface->eIGFXPlatform == eIGFX_CLS)
    {
        switch (ulGPIOPin)
        {
        case 0x1:
            result = EDID_INDEX_FOR_HDMIA;
            break;
        case 0x2:
            result = EDID_INDEX_FOR_HDMIB;
            break;
        case 0x9:
            result = EDID_INDEX_FOR_HDMIF;
            break;
        case 0xA:
            result = EDID_INDEX_FOR_HDMIG;
            break;
        case 0xB:
            result = EDID_INDEX_FOR_HDMIH;
            break;
        case 0xC:
            result = EDID_INDEX_FOR_HDMII;
            break;
        default:
            break;
        }
    }

    return result;
}

BOOLEAN GMBusInterface_GetEDIDDataBlock(PGMBUS_INTERFACE pstGMBusInterface, ULONG ulGPIOPin)
{
    BOOLEAN           bRet        = FALSE;
    GMBUS1_REG_STRUCT stGMBUS1Reg = { 0 };

    stGMBUS1Reg.ulValue             = GMBusInterface_ReadGMBUSDWORDRegister(pstGMBusInterface, GMBUS1);
    ENUM_EDID_PORT_INDEX edid_index = GMBusInterface_GetEDIDIndex(pstGMBusInterface, ulGPIOPin);

    if (edid_index >= EDID_INDEX_FOR_HDMIA && edid_index < EDID_INDEX_INVALID)
    {
        if (NULL == pstGMBusInterface->EdidData[edid_index].pucEdidData)
        {
            bRet = FALSE;
        }
        else
        {
            g_ulEdid = (pstGMBusInterface->EdidData[edid_index].pucEdidData + stGMBUS1Reg.ulSlaveRegisterIndex + (g_HDMISegmentPointer * 256));
            bRet     = TRUE;
        }
    }
    else
    {
        GFXVALSIM_DBG_MSG("platform: %d, pch: %d, stGMBUS1Reg.ulValue: %d, ulGPIOPin: %d, edid_index: %d", pstGMBusInterface->eIGFXPlatform, pstGMBusInterface->ePCHProductFamily,
                          stGMBUS1Reg.ulValue, ulGPIOPin, edid_index);
    }

    g_HDMISegmentPointer = 0; // Resetting HDMI Segment Pointer index to 0 as the edid data is copied to edid pointer.

    return bRet;
}

BOOLEAN GMBusInterface_GetDongleTypeData(PGMBUS_INTERFACE pstGMBusInterface, ULONG ulGPIOPin)
{
    BOOLEAN bRet = TRUE;

    ENUM_EDID_PORT_INDEX edid_index = GMBusInterface_GetEDIDIndex(pstGMBusInterface, ulGPIOPin);

    if (edid_index >= EDID_INDEX_FOR_HDMIA && edid_index < EDID_INDEX_INVALID)
    {
        switch (pstGMBusInterface->DongleType[edid_index])
        {
        case DONGLE_TYPE_DEFAULT:
        case DONGLE_TYPE_2_ADAPTER:
            g_ulAdapterdata = Type2Adapter;
            break;
        case DONGLE_TYPE_2_ADAPTER_PS8469:
            g_ulAdapterdata = Type2Adapter_PS8469;
            break;

        case DONGLE_TYPE_1_ADAPTER:
            g_ulAdapterdata = Type1Adapter;
            break;
        case DONGLE_TYPE_DVI:
            g_ulAdapterdata = DviAdapter;
            break;
        case DONGLE_TYPE_LSPCON:
            g_ulAdapterdata = LsPconAdapter;
            break;
        default:
            GFXVALSIM_DBG_MSG("Invalid DongleType %d, ulGPIOPin: %d, edid_index: %d", pstGMBusInterface->DongleType[edid_index], ulGPIOPin, edid_index);
            bRet = FALSE;
            break;
        }
    }
    else
    {
        bRet = FALSE;
        GFXVALSIM_DBG_MSG("platform: %d, pch: %d, ulGPIOPin: %d, edid_index: %d", pstGMBusInterface->eIGFXPlatform, pstGMBusInterface->ePCHProductFamily, ulGPIOPin, edid_index);
    }

    return bRet;
}

BOOLEAN GMBusInterface_GetSCDCDataBlock(PGMBUS_INTERFACE pstGMBusInterface, ULONG ulGPIOPin)
{
    BOOLEAN           bRet        = TRUE;
    GMBUS1_REG_STRUCT stGMBUS1Reg = { 0 };
    stGMBUS1Reg.ulValue           = GMBusInterface_ReadGMBUSDWORDRegister(pstGMBusInterface, GMBUS1);

    if (((pstGMBusInterface->eIGFXPlatform == eIGFX_GEMINILAKE) || (pstGMBusInterface->eIGFXPlatform == eIGFX_ICELAKE) || (pstGMBusInterface->eIGFXPlatform == eIGFX_ICELAKE_LP) ||
         (pstGMBusInterface->eIGFXPlatform == eIGFX_JASPERLAKE) || (pstGMBusInterface->eIGFXPlatform == eIGFX_LAKEFIELD) ||
         (pstGMBusInterface->eIGFXPlatform == eIGFX_TIGERLAKE_LP) || (pstGMBusInterface->eIGFXPlatform == eIGFX_ROCKETLAKE) ||
         (pstGMBusInterface->eIGFXPlatform == eIGFX_TIGERLAKE_HP) || (pstGMBusInterface->eIGFXPlatform == eIGFX_RYEFIELD) ||
         (pstGMBusInterface->eIGFXPlatform == eIGFX_CANNONLAKE) || (pstGMBusInterface->eIGFXPlatform == eIGFX_LAKEFIELD_R) || (pstGMBusInterface->eIGFXPlatform == eIGFX_DG100) ||
         (pstGMBusInterface->eIGFXPlatform == eIGFX_DG2) || (pstGMBusInterface->eIGFXPlatform == eIGFX_ALDERLAKE_S) || (pstGMBusInterface->eIGFXPlatform == eIGFX_ALDERLAKE_P) ||
         (pstGMBusInterface->eIGFXPlatform == eIGFX_ALDERLAKE_N) || (pstGMBusInterface->eIGFXPlatform == eIGFX_METEORLAKE) ||
         (pstGMBusInterface->eIGFXPlatform == eIGFX_ARROWLAKE) || (pstGMBusInterface->eIGFXPlatform == eIGFX_ELG) || (pstGMBusInterface->eIGFXPlatform == eIGFX_LUNARLAKE) ||
         (pstGMBusInterface->eIGFXPlatform == eIGFX_PTL) || (pstGMBusInterface->eIGFXPlatform == eIGFX_NVL) || (pstGMBusInterface->eIGFXPlatform == eIGFX_NVL_AX) ||
         (pstGMBusInterface->eIGFXPlatform == IGFX_NVL_XE3G) || (pstGMBusInterface->eIGFXPlatform == eIGFX_CLS)) &&
        (ulGPIOPin))
    {
        g_ulscdcdata = &g_HDMIPortSCDC[stGMBUS1Reg.ulSlaveRegisterIndex];
    }
    return bRet; // Valid later when we add - SCDC data from App.
}

BOOLEAN GMBusInterface_GMBUSStateMachineHandler(PGMBUS_INTERFACE pstGMBusInterface, GMBUS_STATE eNewState)
{
    GMBUS_STATE eCurrentState      = GMBusInterface_GetGMBUSCurrentState(pstGMBusInterface);
    BOOLEAN     bRet               = TRUE;
    errno_t     eRetError          = 0;
    int         iCurrentByteToRead = 0;
    int         iByteSizeToRead    = 4; // GMBUS3 Register will Hold 4 Bytes data - Default
    int         iCurrentScdcIndex  = 0;
    GFXVALSIM_FUNC_ENTRY();
    GFXVALSIM_GMBUS_STATE(eCurrentState, eNewState);
    GMBUS1_REG_STRUCT stGMBUS1Reg = { 0 };

    switch (eNewState)
    {
    case GMBUS_START:
    {
        if ((GMBUS_ACQUIRE == eCurrentState) || (GMBUS_DEFAULT == eCurrentState) || (GMBUS_STOP == eCurrentState) || (GMBUS_RELEASE == eCurrentState) ||
            ((GMBUS_RESET == eCurrentState)))
        {
            // Set GMBUS2[BIT10] = 0; ACK
            // Set GMBUS2[BIT15] = 1; // InUse
            // Set GMBUS2[BIT14] = 0 - Not in wait phase
            // The WAIT state is exited by generating a STOP or by starting another GMBUS cycle.

            // ULONG ulGMBUS2Data = GMBusInterface_ReadGMBUSDWORDRegister(GMBUS2);
            GMBUS2_RW_REG_STRUCT stGMBUS2Reg = { 0 };
            // ulGMBUS2Data = (ulGMBUS2Data & ~(BIT10));
            stGMBUS2Reg.bInUse = 1;

            GMBusInterface_WriteGMBUSDWORDRegister(pstGMBusInterface, GMBUS2, stGMBUS2Reg.ulValue);
            GMBusInterface_SetGMBUSCurrentState(pstGMBusInterface, GMBUS_START);
            // eGMBUSCurrentState = GMBUS_START;
        }
        else
        {
            bRet = FALSE;
        }
        break;
    }
    case GMBUS_READY:
    {
        if (GMBUS_START == eCurrentState)
        {
            // Set GMBUS2[BIT11] = 1 - H/W Ready
            // Set GMBUS2[BIT15] = 1; // InUse
            // Set GMBUS2[BIT14] = 0 - Not in Wait Phase
            // Set GMBUS3 = 0//

            // ULONG ulGMBUS2Data = GMBusInterface_ReadGMBUSDWORDRegister(GMBUS2);
            GMBUS0_REG_STRUCT    stGMBUS0Reg = { 0 };
            GMBUS2_RW_REG_STRUCT stGMBUS2Reg = { 0 };
            GMBUS3_REG_STRUCT    stGMBUS3Reg = { 0 };

            stGMBUS1Reg.ulValue = GMBusInterface_ReadGMBUSDWORDRegister(pstGMBusInterface, GMBUS1);
            stGMBUS0Reg.ulValue = GMBusInterface_ReadGMBUSDWORDRegister(pstGMBusInterface, GMBUS0);

            switch (stGMBUS1Reg.ulSlaveAddress)
            {
            case 0xA1:
                bRet = GMBusInterface_GetEDIDDataBlock(pstGMBusInterface, stGMBUS0Reg.ulPinPairSelect); // Read from EDID block
                break;
            case 0xA8:
                // GMBusInterface_SetSCDCDataBlock(pstGMBusInterface, stGMBUS0Reg.ulPinPairSelect);
                iCurrentScdcIndex = stGMBUS1Reg.ulSlaveRegisterIndex;
                if (0x31 == iCurrentScdcIndex)
                {
                    g_HDMIPortSCDC[0x10] = g_HDMIPortSCDC[0x10] | 0x20;
                }
                else if (0x10 == iCurrentScdcIndex)
                {
                    g_HDMIPortSCDC[iCurrentScdcIndex] = g_HDMIPortSCDC[iCurrentScdcIndex] & 0xDF;
                }
                break;
            case 0xA9:
                // bRet = GMBusInterface_GetSCDCDataBlock(pstGMBusInterface, stGMBUS0Reg.ulPinPairSelect);  //Read from SCDC data block
                break;
            case 0x81:
                bRet = GMBusInterface_GetDongleTypeData(pstGMBusInterface, stGMBUS0Reg.ulPinPairSelect);
                break;
            case 0x60:
                stGMBUS3Reg.ulValue  = GMBusInterface_ReadGMBUSDWORDRegister(pstGMBusInterface, GMBUS3);
                g_HDMISegmentPointer = stGMBUS3Reg.ulDataByte0;
                GFXVALSIM_DBG_MSG("Setting hdmisegment pointer to : %d", g_HDMISegmentPointer);

                bRet = TRUE;
                break;
            default:
                break;
            }

            stGMBUS2Reg.bHWReady     = 1;
            stGMBUS2Reg.bInUse       = 1;
            stGMBUS2Reg.bInWaitPhase = 1;
            GMBusInterface_WriteGMBUSDWORDRegister(pstGMBusInterface, GMBUS2, stGMBUS2Reg.ulValue);
            GMBusInterface_SetGMBUSCurrentState(pstGMBusInterface, GMBUS_READY);
            // eGMBUSCurrentState = GMBUS_READY;
        }
        else
        {
            bRet = FALSE;
        }
        break;
    }
    case GMBUS_READ:
    {
        if ((GMBUS_READY == eCurrentState) || (GMBUS_READ == eCurrentState))
        {
            // State - Data Phase
            // Adjust GMBUS2[8:0] - Current byte Count(transferred)
            // Set GMBUS2[BIT14] = 1 - indicates in wait phase
            // Wait phase is entered at the end of the current transaction when that transaction is selected not to terminate with a STOP.

            GMBUS3_REG_STRUCT    stGMBUS3Reg = { 0 };
            GMBUS2_RW_REG_STRUCT stGMBUS2Reg = { 0 };
            stGMBUS2Reg.ulValue              = GMBusInterface_ReadGMBUSDWORDRegister(pstGMBusInterface, GMBUS2);
            stGMBUS1Reg.ulValue              = GMBusInterface_ReadGMBUSDWORDRegister(pstGMBusInterface, GMBUS1);

            iCurrentByteToRead = stGMBUS1Reg.ulTotalBytes - stGMBUS2Reg.ulCurrentByteCount;
            if (iCurrentByteToRead < 4) // GMBUS3 Register will Hold 4 Bytes data Default,  only when we have read request coming for less than 4 byte data we need this.
            {
                iByteSizeToRead = iCurrentByteToRead;
            }

            if (stGMBUS1Reg.ulSlaveAddress == 0xA1) // EDID
            {
                eRetError = memcpy_s(&stGMBUS3Reg.ulValue, iByteSizeToRead * sizeof(UINT8), &(g_ulEdid[stGMBUS2Reg.ulCurrentByteCount]), iByteSizeToRead * sizeof(UINT8));
            }
            else if (stGMBUS1Reg.ulSlaveAddress == 0x81) // Type2Adapter
            {
                eRetError = memcpy_s(&stGMBUS3Reg.ulValue, iByteSizeToRead * sizeof(UINT8), &(g_ulAdapterdata[stGMBUS1Reg.ulSlaveRegisterIndex + stGMBUS2Reg.ulCurrentByteCount]),
                                     iByteSizeToRead * sizeof(UINT8));
            }
            else if (stGMBUS1Reg.ulSlaveAddress == 0xA9) // SCDC
            {
                eRetError = memcpy_s(&stGMBUS3Reg.ulValue, iByteSizeToRead * sizeof(UINT8), &(g_HDMIPortSCDC[stGMBUS1Reg.ulSlaveRegisterIndex + stGMBUS2Reg.ulCurrentByteCount]),
                                     iByteSizeToRead * sizeof(UINT8));
            }

            if (0 == eRetError)
            {

                stGMBUS2Reg.ulCurrentByteCount = (stGMBUS2Reg.ulCurrentByteCount + iByteSizeToRead);
                stGMBUS2Reg.bInWaitPhase       = 1;

                GMBusInterface_WriteGMBUSDWORDRegister(pstGMBusInterface, GMBUS2, stGMBUS2Reg.ulValue);
                GMBusInterface_WriteGMBUSDWORDRegister(pstGMBusInterface, GMBUS3, stGMBUS3Reg.ulValue);

                GMBusInterface_SetGMBUSCurrentState(pstGMBusInterface, GMBUS_READ);
                // eGMBUSCurrentState = GMBUS_READ;
            }
            else
            {
                GFXVALSIM_DBG_MSG("case: GMBUS_READ -> eRetError: %d", eRetError);
                bRet = FALSE;
            }
        }
        else
        {
            bRet = FALSE;
        }
        break;
    }
    case GMBUS_STOP:
    {
        // Set GMBUS2[BIT11] = 1 - H/W Ready
        // Set GMBUS2[BIT9]  = 0 - GMBus is Idle
        // Set GMBUS2[BIT14] = 0 - Not in wait phase
        // The WAIT state is exited by generating a STOP or by starting another GMBUS cycle.
        // ULONG ulGMBUS2Data = GMBusInterface_ReadGMBUSDWORDRegister(GMBUS2);
        GMBUS2_RW_REG_STRUCT stGMBUS2Reg = { 0 };
        stGMBUS2Reg.bHWReady             = 1;
        // ulGMBUS2Data = (ulGMBUS2Data & ~(BIT9));
        // ulGMBUS2Data = (ulGMBUS2Data | ~(BIT14));
        GMBusInterface_WriteGMBUSDWORDRegister(pstGMBusInterface, GMBUS2, stGMBUS2Reg.ulValue);
        GMBusInterface_SetGMBUSCurrentState(pstGMBusInterface, GMBUS_STOP);
        // eGMBUSCurrentState = GMBUS_STOP;
        break;
    }
    case GMBUS_RESET:
    {
        // Set GMBUS2[BIT9]  = 0 - GMBus is Idle
        // Set GMBUS2[BIT14] = 0 - Not in wait phase
        // The WAIT state is exited by generating a STOP or by starting another GMBUS cycle.
        GMBusInterface_WriteGMBUSDWORDRegister(pstGMBusInterface, GMBUS0, 0);
        GMBusInterface_WriteGMBUSDWORDRegister(pstGMBusInterface, GMBUS1, 0);
        GMBusInterface_WriteGMBUSDWORDRegister(pstGMBusInterface, GMBUS2, 0);
        GMBusInterface_WriteGMBUSDWORDRegister(pstGMBusInterface, GMBUS3, 0);
        GMBusInterface_WriteGMBUSDWORDRegister(pstGMBusInterface, GMBUS4, 0);
        GMBusInterface_WriteGMBUSDWORDRegister(pstGMBusInterface, GMBUS5, 0);

        GMBusInterface_SetGMBUSCurrentState(pstGMBusInterface, GMBUS_RESET);
        // eGMBUSCurrentState = GMBUS_RESET;
        break;
    }
    case GMBUS_RELEASE:
    {
        GMBusInterface_SetGMBUSCurrentState(pstGMBusInterface, GMBUS_RELEASE);
        // eGMBUSCurrentState = GMBUS_RELEASE;
        break;
    }
    default:
        break;
    }
    BOOLEAN bRetComplement = bRet ? FALSE : TRUE;
    GFXVALSIM_FUNC_EXIT(bRetComplement);
    return bRet;
}

/*-----------------------------------------------------------------------*
 *
 *-----------------------------------------------------------------------*/
BOOLEAN GMBusInterface_GMBUS0WriteHandler(PGMBUS_INTERFACE pstGMBusInterface, ULONG ulOffset, ULONG ulData)
{
    BOOLEAN           bRet        = FALSE;
    GMBUS0_REG_STRUCT stGMBUS0Reg = { 0 };
    stGMBUS0Reg.ulValue           = ulData;
    if (0 != stGMBUS0Reg.ulPinPairSelect)
    {
        // State - Started
        // PinPair is not disabled
        GMBusInterface_WriteGMBUSDWORDRegister(pstGMBusInterface, ulOffset, stGMBUS0Reg.ulValue);
        bRet = GMBusInterface_GMBUSStateMachineHandler(pstGMBusInterface, GMBUS_START);
    }
    else
    {
        // State - reset to Available
        // PinPair is disable - reset
        // Set GMBUS2[BIT9] = 0 - GMBus is Idle - WaitForIdle
        GMBusInterface_WriteGMBUSDWORDRegister(pstGMBusInterface, ulOffset, stGMBUS0Reg.ulValue);
        bRet = GMBusInterface_GMBUSStateMachineHandler(pstGMBusInterface, GMBUS_RESET);
    }
    return bRet;
}

/*-----------------------------------------------------------------------*
 *
 *-----------------------------------------------------------------------*/
BOOLEAN GMBusInterface_GMBUS1WriteHandler(PGMBUS_INTERFACE pstGMBusInterface, ULONG ulOffset, ULONG ulData)
{
    // BIT0 = 0 - indicates read from slave
    // BIT[7:1] - Slave address
    // BIT[27:25] - Bus cycle select
    BOOLEAN           bRet        = TRUE;
    GMBUS1_REG_STRUCT stGMBUS1Reg = { 0 };
    stGMBUS1Reg.ulValue           = ulData;

    if ((stGMBUS1Reg.bSWReady) && (stGMBUS1Reg.ulSlaveAddress) && (stGMBUS1Reg.ulBusCycleSelect))
    {
        // State - ReadyToTransfer
        // Set GMBUS2[BIT11] - H/W Ready
        BOOLEAN ulValueBIT27Complement = ((stGMBUS1Reg.ulValue) & BIT27) ? FALSE : TRUE;
        if (((stGMBUS1Reg.ulValue) & BIT25) && ulValueBIT27Complement)
        {
            // Cycle will end in WAIT, and STOP will be issued later.
            // Set GMBUS2[BIT11] - H/W Ready

            GMBusInterface_WriteGMBUSDWORDRegister(pstGMBusInterface, ulOffset, stGMBUS1Reg.ulValue);
            bRet = GMBusInterface_GMBUSStateMachineHandler(pstGMBusInterface, GMBUS_READY);
        }
        else if (((ulData)&BIT25) && ((ulData)&BIT27))
        {
            // TBD: In driver code, this bus cycle is used for CRT legacy where cycle does not go to WAIT phase
            // Check total bytes to transfer, and issue a STOP once transaction is complete
        }
        BOOLEAN ulValueBIT25Complement = ((stGMBUS1Reg.ulValue) & BIT25) ? FALSE : TRUE;
        if (ulValueBIT25Complement && (((stGMBUS1Reg.ulValue) & BIT27)))
        {
            // GMBUS_CYCLE_STOP_IFWAIT_ENDBYTE - indicates STOP is issued
            // Set GMBUS2[BIT11] - H/W Ready
            GMBusInterface_WriteGMBUSDWORDRegister(pstGMBusInterface, ulOffset, stGMBUS1Reg.ulValue);
            bRet = GMBusInterface_GMBUSStateMachineHandler(pstGMBusInterface, GMBUS_STOP);
        }
    }
    else
    {
        // No GMBUS cycle is generated..reset path
        GMBusInterface_WriteGMBUSDWORDRegister(pstGMBusInterface, ulOffset, stGMBUS1Reg.ulValue);
    }
    return bRet;
}

/*-----------------------------------------------------------------------*
 *
 *-----------------------------------------------------------------------*/
BOOLEAN GMBusInterface_GMBUS2WriteHandler(PGMBUS_INTERFACE pstGMBusInterface, ULONG ulOffset, ULONG ulData)
{
    // if (((pAccess->ulData) & BIT15) & ulReadValue) //BIT15: Writing ONE to already set BIT15.. resets
    BOOLEAN              bRet        = FALSE;
    GMBUS2_RW_REG_STRUCT stGMBUS2Reg = { 0 };
    stGMBUS2Reg.ulValue              = GMBusInterface_ReadGMBUSDWORDRegister(pstGMBusInterface, GMBUS2);

    if ((stGMBUS2Reg.bInUse) && (ulData & BIT15))
    {
        stGMBUS2Reg.ulValue = ulData;
        stGMBUS2Reg.bInUse  = 0;
        bRet                = GMBusInterface_GMBUSStateMachineHandler(pstGMBusInterface, GMBUS_RELEASE);
    }
    GMBusInterface_WriteGMBUSDWORDRegister(pstGMBusInterface, ulOffset, stGMBUS2Reg.ulValue);
    return bRet;
}
