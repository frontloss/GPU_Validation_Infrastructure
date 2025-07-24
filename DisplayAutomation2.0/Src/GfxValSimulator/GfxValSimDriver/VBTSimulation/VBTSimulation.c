#include "..\\CommonInclude\\\DisplayDefs.h"
#include "..\\DriverInterfaces\SimDriver.h"
#include "..\\DriverInterfaces\\SIMDRV_GFX_COMMON.h"
#include "..\CommonCore\CommonCore.h"
#include "VBTSimulation.h"
#include "..\CommonInclude\ETWLogging.h"

// Gfx CB for reading PCI config / ROM space
DDU32 VBTSIMULATION_GetOpRegionPHYAddr(PGFX_ADAPTER_CONTEXT pGfxAdapterContext);
DDU32 VBTSIMULATION_GetOPROMSize(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, DDU8* pOpromInfo, unsigned int ulOffset);

// Registry operations
BOOLEAN VBTSIMULATION_CopyTestVBTFromRegistry(GFX_ADAPTER_CONTEXT gfxAdapterContext, DDU8 *pRegistryVBT, DDU32 VbtSize);
BOOLEAN VBTSIMULATION_CopyDefaultVBTFromRegistry(GFX_ADAPTER_CONTEXT gfxAdapterContext, DDU8 *pRegistryVBT);
VOID    VBTSIMULATION_WriteActualVBT(GFX_ADAPTER_CONTEXT gfxAdapterContext, DDU8 *pPCIVBT, DDU32 VbtSize);
BOOLEAN VBTSIMULATION_CopyTestOpromHeaderFromRegistry(GFX_ADAPTER_CONTEXT gfxAdapterContext, DDU8 *pHeaderBase, DDU32 Size);
VOID    VBTSIMULATION_WriteActualOpromHeader(GFX_ADAPTER_CONTEXT gfxAdapterContext, DDU8 *pHeaderBase, DDU32 Size);
VOID    VBTSIMULATION_WriteActualOpromFooter(GFX_ADAPTER_CONTEXT gfxAdapterContext, DDU8 *pFooterBase, DDU32 Size);

#define PCI_IGD_OPREGION_BASE_ADDR 0xFC

// OPROM data, creating static variable to avoid interface breakage
// between GfxValSim driver and Gfx driver(Legacy and Yangra).
// static PEXPANSION_ROM_HEADER pStaticExpansionRomHeader;

#pragma region Internal helper functions

//----------------------------------------------------------------------------
//  Function    :   VBTSIMULATION_GetOpRegionPHYAddr
//  Type        :   Helper function to get PCI Config base address
//  Description :   Reads PCI configuration register data from IGD device.
//  Arguments   :   Pointer to SIMDRVGFX_INTERFACE_DATA
//  Returns     :   Pointer to OpRegion Physical address
//-----------------------------------------------------------------------------
DDU32 VBTSIMULATION_GetOpRegionPHYAddr(PGFX_ADAPTER_CONTEXT pGfxAdapterContext)
{
    BOOLEAN           bRet                     = FALSE;
    GFXCALLBACK_ARGS  stGfxCallbackArgs        = { 0 };
    DDU8 *            pBuff                    = NULL;
    KIRQL             kIrql                    = KeGetCurrentIrql();
    DDU32             OpregionBasePhysicalAddr = 0;
    PPORTINGLAYER_OBJ pstPortingObj            = GetPortingObj();
    // IRQL check.
    if (kIrql >= DISPATCH_LEVEL)
    {
        GFXVALSIM_DBG_MSG("GetOpRegionBaseAddr FAILED Cannot be called at this IRQL!\r\n");
        goto END;
    }

    // Offset 0xFC Opregion Physical base is 0, so this is Discrete Graphics config
    // First read only 4 bytes and verify signature and get the OPROM size
    pBuff = (DDU8 *)pstPortingObj->pfnAllocateMem(sizeof(PCI_COMMON_CONFIG), TRUE);
    if (pBuff == NULL)
    {
        GFXVALSIM_DBG_MSG("Memory allocation failed!!\r\n");
        goto END;
    }

    stGfxCallbackArgs.eGfxCbEvent                     = ReadPCIConfig;
    stGfxCallbackArgs.stSimReadPCIConfigArgs.ulSize   = sizeof(PCI_COMMON_CONFIG);
    stGfxCallbackArgs.stSimReadPCIConfigArgs.ulOffset = 0;
    stGfxCallbackArgs.stSimReadPCIConfigArgs.pBuffer  = pBuff;
    bRet                                              = pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler(pGfxAdapterContext->pvGfxHwDev, &stGfxCallbackArgs);

    if (bRet == TRUE)
    {
        GFXVALSIM_PCI_CONFIG_DATA(stGfxCallbackArgs.stSimReadPCIConfigArgs.ulOffset, stGfxCallbackArgs.stSimReadPCIConfigArgs.ulSize,
                                  stGfxCallbackArgs.stSimReadPCIConfigArgs.pBuffer);
        PCI_COMMON_CONFIG *pPCI  = (PCI_COMMON_CONFIG *)pBuff;
        OpregionBasePhysicalAddr = *((DDU32 *)(&pPCI->DeviceSpecific[PCI_IGD_OPREGION_BASE_ADDR - sizeof(PCI_COMMON_HEADER)]));
    }
    else
    {
        GFXVALSIM_DBG_MSG("ReadPCIConfig failed!!\r\n");
    }

END:
    if (pBuff != NULL)
    {
        pstPortingObj->pfnFreeMem(pBuff);
    }
    GFXVALSIM_FUNC_EXIT((bRet == TRUE) ? 0 : 1);

    return OpregionBasePhysicalAddr;
}

//----------------------------------------------------------------------------
//  Function    :   VBTSIMULATION_GetOPROMSize
//  Type        :   Helper function to get PCI ROM size
//  Description :   Reads PCI configuration register data from DGfx device.
//  Arguments   :   Pointer to SIMDRVGFX_INTERFACE_DATA
//  Returns     :   Size of ROM
//-----------------------------------------------------------------------------
DDU32 VBTSIMULATION_GetOPROMSize(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, DDU8* pOpromInfo, unsigned int ulOffset)
{
    BOOLEAN           bRet              = FALSE;
    GFXCALLBACK_ARGS  stGfxCallbackArgs = { 0 };
    OPROM_HEADER      OpromHeader;
   
    DDU32             OpROMSize     = 0;
    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();
    // Offset 0xFC Opregion Physical base is 0, so this is Discrete Graphics config
    // For oprom reads, proceed only if the offset is 0
    // This is done to work around a limitation with OS interface which only accepts offset 0 and ignores non-zero offset reads
    if (ulOffset == 0)
    // Get the image size from PCI structure
    {
        stGfxCallbackArgs.eGfxCbEvent                     = ReadOPROM;
        stGfxCallbackArgs.stSimReadPCIConfigArgs.ulSize   = OPROM_INITIAL_READ_SIZE;
        stGfxCallbackArgs.stSimReadPCIConfigArgs.ulOffset = ulOffset;
        stGfxCallbackArgs.stSimReadPCIConfigArgs.pBuffer  = pOpromInfo;

        // Call Gfx Interface to read PCI ROM config space
        bRet = pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler(pGfxAdapterContext->pvGfxHwDev, &stGfxCallbackArgs);

        if (bRet == FALSE)
        {
            GFXVALSIM_DBG_MSG("VBTSIMULATION_GetOPROMSize: Failed to read OPROM memory!\r\n");
            return 0;
        }
    }

    // Check for invalid OPROM signature
    if (((OPROM_HEADER *)(pOpromInfo + ulOffset))->Signature != 0xAA55)
    {
        bRet = FALSE;
        GFXVALSIM_DBG_MSG("VBTSIMULATION_GetOPROMSize: Invalid OPRegion signature!\r\n");
        return 0;
    }

    // Read the image length from PCI Data structure offset 0x10
    // Copy the image size to Oprom Header
    memcpy_s(&OpromHeader.SizeIn512Bytes, PCI_IMAGE_LENGTH_SIZE,
             &(pOpromInfo + ulOffset)[((EXPANSION_ROM_HEADER *)(pOpromInfo + ulOffset))->PciStructOffset + PCI_IMAGE_LENGTH_OFFSET],
             PCI_IMAGE_LENGTH_SIZE);

    if (OpromHeader.SizeIn512Bytes == 0x0)
    {
        bRet = FALSE;
        GFXVALSIM_DBG_MSG("VBTSIMULATION_GetOPROMSize: OPRegion size is 0x0!\r\n");
        return 0;
    }

    OpROMSize = OpromHeader.SizeIn512Bytes * OPROM_BYTE_BOUNDARY;

    return OpROMSize;
}

//----------------------------------------------------------------------------
//  Function    :   VBTSIMULATION_GetROMDataFromPCIROM
//  Type        :   Helper function to Read ROM from  PCI ROM
//  Description :   Reads PCI ROM data from Dgfx device.
//  Arguments   :   SimDrv Interface
//  Returns     :   Pointer to OPRegion
//-----------------------------------------------------------------------------
VOID VBTSIMULATION_GetROMDataFromPCIROM(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PSIMDRV_OPREGION_VBT_DETAILS pOpRegionVbtDetails)
{
    BOOLEAN               bRet                = FALSE;
    GFXCALLBACK_ARGS      stGfxCallbackArgs   = { 0 };
    EXPANSION_ROM_HEADER *pExpansionRomHeader = NULL;
    OPREGION_HEADER *     pOpregionHeader     = NULL;
    DDU8                  CodeType            = 0;
    DDU32                 ulOPRomSize         = 0;
    DDU32                 pageCount           = 0;
    DDU32                 Offset              = 0;
    BOOLEAN               IsSignaturePresent  = FALSE;
    BOOLEAN               LastImageIndicator  = FALSE;
    DDU8 *                pSignatureRomBase   = NULL;
    DDU8                 *pOpromInfo = NULL;
    PPORTINGLAYER_OBJ     pstPortingObj       = GetPortingObj();
    pOpRegionVbtDetails->OPRomHeaderSize      = 0;
    pOpromInfo = (DDU8 *)pstPortingObj->pfnAllocateMem(OPROM_INITIAL_READ_SIZE, TRUE);
    if (pOpromInfo == NULL)
    {
        GFXVALSIM_DBG_MSG("VBTSIMULATION_GetOPROMSize: Memory allocation failed!!\r\n");
        return;
    }
    do
    {
        if (NULL == pGfxAdapterContext)
            break;

        // if (pGfxAdapterContext->pvExpansionRomHeader != NULL)
        //    break;

        ulOPRomSize = VBTSIMULATION_GetOPROMSize(pGfxAdapterContext, pOpromInfo, Offset);
        if (!ulOPRomSize)
            break;

        /* Allocate memory always 1 page aligned */
        pageCount = ((ulOPRomSize) / PAGE_SIZE);
        if ((ulOPRomSize) % PAGE_SIZE) /* If total oprom size is not page aligned allocate extra memory to make it 1 Page aligned */
        {
            pageCount++;
        }

        // Once Signature is validated, try reading full OPROM into driver's memory
        // Currently this is just ~8KB data which is OPROM header + Opregion size, so allocating memory here for the full size
        pExpansionRomHeader = (EXPANSION_ROM_HEADER *)pstPortingObj->pfnAllocateMem((pageCount * PAGE_SIZE), TRUE);
        if (pExpansionRomHeader == NULL)
        {
            GFXVALSIM_DBG_MSG("VBTSIMULATION_GetROMDataFromPCIROM: Memory allocation failed!\r\n");
            break;
        }

        // Call Gfx Interface to read PCI ROM config space
        memcpy_s((DDU8 *)pExpansionRomHeader, (pageCount * PAGE_SIZE), (pOpromInfo + Offset), ulOPRomSize);

        // Opregion address will be stored at offset 0x1A per Intel OPROM design
        pOpregionHeader = (OPREGION_HEADER *)((DDU8 *)pExpansionRomHeader + pExpansionRomHeader->OpregionBase);

        if (pOpregionHeader == NULL)
        {
            GFXVALSIM_DBG_MSG("VBTSIMULATION_GetROMDataFromPCIROM: pOpregionHeader is NULL!\r\n");
            break;
        }

        // CodeType = (DDU8 *)pExpansionRomHeader[pExpansionRomHeader->PciStructOffset + PCI_CODE_TYPE_OFFSET];
        // Verify the OPREGION signature
        // This should match the string "IntelGraphicsMem"
        if (0 != (memcmp(pOpregionHeader->OpRegionSignature, OPREGION_SIGNATURE, NUM_SIGNATURE_BYTES)))
        {
            // OPREGION signature did not match
            // Check if this is the last image
            if ((*((DDU8 *)pExpansionRomHeader + PCI_LAST_IMAGE_INDICATOR_OFFSET) & PCI_LAST_IMAGE_INDICATOR_MASK) == PCI_LAST_IMAGE_INDICATOR_MASK)
            {
                // Set the LastImageIndicator flag to TRUE
                // If last image, then config data binary is not found
                // break
                LastImageIndicator = TRUE;
                GFXVALSIM_DBG_MSG("VBTSIMULATION_GetROMDataFromPCIROM: LastImageIndicator is TRUE !\r\n");
                pstPortingObj->pfnFreeMem(pExpansionRomHeader);
                break;
            }

            // Try to match $CPD signature
            // If matched, proceed with Oprom signature authentication
            if ((0 == memcmp(pOpregionHeader->OpRegionSignature, CPD_SIGNATURE, NUM_CPD_BYTES))) // && (CodeType == 0xF0))
            {
                // Oprom Signature validated
                // Reaching here means that the current image does not contain config data binary
                IsSignaturePresent = TRUE;

                pSignatureRomBase                    = (DDU8 *)pExpansionRomHeader;
                pOpRegionVbtDetails->OPRomHeaderSize = ulOPRomSize;

                Offset = Offset + ulOPRomSize;
                continue;
            }
            else
            {
                pstPortingObj->pfnFreeMem(pExpansionRomHeader);
                // Invalid Oprom
                GFXVALSIM_DBG_MSG("VBTSIMULATION_GetROMDataFromPCIROM: Invalid Oprom. Neither signature nor IntelGraphicsmem matched. !\r\n");
                break;
            }
        }

        if (IsSignaturePresent == TRUE)
        {
            /* Allocate memory always 1 page aligned */
            pageCount = ((ulOPRomSize + Offset) / PAGE_SIZE);
            if ((ulOPRomSize + Offset) % PAGE_SIZE) /* If total oprom size is not page aligned allocate extra memory to make it 1 Page aligned */
            {
                pageCount++;
            }

            // Once Signature is validated, try reading full OPROM with signature and data
            // So, totally it would be 64KB ie., 2KB(Signature Oprom) + 62KB(Code Oprom)
            DDU8 *ptempBuffer = (DDU8 *)pstPortingObj->pfnAllocateMem((pageCount * PAGE_SIZE), TRUE);
            if (ptempBuffer == NULL)
            {
                GFXVALSIM_DBG_MSG("VBTSIMULATION_GetROMDataFromPCIROM: Memory allocation failed!\r\n");
                break;
            }
            memcpy(ptempBuffer, pSignatureRomBase, Offset);                 // check this
            memcpy(ptempBuffer + Offset, pExpansionRomHeader, ulOPRomSize); // revisit
            pstPortingObj->pfnFreeMem(pSignatureRomBase);
            pstPortingObj->pfnFreeMem(pExpansionRomHeader);
            pGfxAdapterContext->pvExpansionRomHeader = ptempBuffer;
        }
        else
        {
            pGfxAdapterContext->pvExpansionRomHeader = pExpansionRomHeader;
        }

        pGfxAdapterContext->OPRomTotalSize  = Offset + ulOPRomSize;
        pOpRegionVbtDetails->pCodeOpRomBase = ((DDU8 *)pGfxAdapterContext->pvExpansionRomHeader + Offset);
        pOpRegionVbtDetails->OPRomSize      = ulOPRomSize;

        break;

    } while (FALSE == LastImageIndicator);

    if (pOpromInfo != NULL)
    {
        pstPortingObj->pfnFreeMem(pOpromInfo);
    }
}

//----------------------------------------------------------------------------
//  Function    :   VBTSIMULATION_IsDefaultVBTPresent
//  Type        :   Helper function
//  Description :   Check if Default VBT is already present in registry
//  Returns     :   Boolean
//-----------------------------------------------------------------------------
BOOLEAN VBTSIMULATION_IsDefaultVBTPresent(GFX_ADAPTER_CONTEXT gfxAdapterContext, PSIMDRV_OPREGION_VBT_DETAILS pOpRegionVbtDetails)
{
    BOOLEAN IsDefaultVbtPresent = FALSE;

    do
    {
        if (VBTSIMULATION_CopyDefaultVBTFromRegistry(gfxAdapterContext, pOpRegionVbtDetails->pVBTBase) == FALSE)
        {
            // VBTSIMULATION_WriteDefaultVBT(&gfxAdapterContext, pOpRegionVbtDetails->pVBTBase, pOpRegionVbtDetails->VbtSize);
            GFXVALSIM_DBG_MSG("Failed to copy Default VBT from registry!");
            break;
        }

        IsDefaultVbtPresent = TRUE;
    } while (FALSE);

    return IsDefaultVbtPresent;
}

//----------------------------------------------------------------------------
//  Function    :   VBTSIMULATION_CopyDefaultVBTFromRegistry
//  Type        :   Helper function
//  Description :   Read Default VBT from registry and assign the output to the pRegistryVBT. The caller should free the memory allocated here.
//  Arguments   :   Integer pointer for VBT location
//  Returns     :   Boolean
//-----------------------------------------------------------------------------
BOOLEAN VBTSIMULATION_CopyDefaultVBTFromRegistry(GFX_ADAPTER_CONTEXT gfxAdapterContext, DDU8 *pRegistryVBT)
{
    NTSTATUS NtStatus;
    BOOLEAN  ret     = FALSE;
    DDU32    VbtSize = 0;
    WCHAR    RegistryKey[MAX_PATH_STRING_LEN];

    wcscpy(RegistryKey, gfxAdapterContext.PCIBusDeviceId);
    wcscat_s(RegistryKey, MAX_PATH_STRING_LEN, SIMDRV_REGKEY_DEFAULT_VBT);
    wcscat_s(RegistryKey, MAX_PATH_STRING_LEN, _SIZE);

    NtStatus = COMMONCORE_GetRegistryInfo(RegistryKey, REG_DWORD, &VbtSize, sizeof(DDU32));
    ret      = NT_SUCCESS(NtStatus) ? TRUE : FALSE;

    if (ret == FALSE || VbtSize == 0)
    {
        GFXVALSIM_DBG_MSG("FAIL: Read default VBT size from registry !!\r\n");
        return FALSE;
    }

    wcscpy(RegistryKey, gfxAdapterContext.PCIBusDeviceId);
    wcscat_s(RegistryKey, MAX_PATH_STRING_LEN, SIMDRV_REGKEY_DEFAULT_VBT);

    NtStatus = COMMONCORE_GetRegistryInfo(RegistryKey, REG_BINARY, pRegistryVBT, VbtSize);

    ret = NT_SUCCESS(NtStatus) ? TRUE : FALSE;
    if (ret == FALSE)
    {
        GFXVALSIM_DBG_MSG("FAIL: Read default VBT from registry !!\r\n");
        return FALSE;
    }

    return ret;
}

//----------------------------------------------------------------------------
//  Function    :   VBTSIMULATION_CopyTestVBTFromRegistry
//  Type        :   Helper function
//  Description :   Read Custom VBT from registry and assign the output to the pRegistryVBT. The caller should free the memory allocated here.
//  Arguments   :   Integer pointer for VBT location
//  Returns     :   Boolean
//-----------------------------------------------------------------------------
BOOLEAN VBTSIMULATION_CopyTestVBTFromRegistry(GFX_ADAPTER_CONTEXT gfxAdapterContext, DDU8 *pRegistryVBT, DDU32 NumberOfBytes)
{
    NTSTATUS NtStatus;
    BOOLEAN  ret     = FALSE;
    DDU32    VbtSize = 0;
    WCHAR    RegistryKey[MAX_PATH_STRING_LEN];

    wcscpy(RegistryKey, gfxAdapterContext.PCIBusDeviceId);
    wcscat_s(RegistryKey, MAX_PATH_STRING_LEN, SIMDRV_REGKEY_CUSTOM_VBT_SIZE);

    NtStatus = COMMONCORE_GetRegistryInfo(RegistryKey, REG_DWORD, &VbtSize, sizeof(DDU32));
    ret      = NT_SUCCESS(NtStatus) ? TRUE : FALSE;

    if (ret == FALSE)
    {
        GFXVALSIM_DBG_MSG("Failed to read VBT size from registry !!\r\n");
        return FALSE;
    }
    else if (VbtSize != NumberOfBytes)
    {
        GFXVALSIM_DBG_MSG("Mismatch in vbt size between Opregion and  Registry!!\r\n");
        return FALSE;
    }

    wcscpy(RegistryKey, gfxAdapterContext.PCIBusDeviceId);
    wcscat_s(RegistryKey, MAX_PATH_STRING_LEN, SIMDRV_REGKEY_CUSTOM_VBT);
    NtStatus = COMMONCORE_GetRegistryInfo(RegistryKey, REG_BINARY, pRegistryVBT, VbtSize);

    ret = NT_SUCCESS(NtStatus) ? TRUE : FALSE;
    if (ret == FALSE)
    {
        GFXVALSIM_DBG_MSG("Failed to read VBT from registry !!\r\n");
        return FALSE;
    }

    return TRUE;
}

//----------------------------------------------------------------------------
//  Function    :   VBTSIMULATION_CopyTestOpromHeaderFromRegistry
//  Type        :   Helper function
//  Description :   Read Custom Oprom Header(Signature Oprom and Opregion Header) from registry and assign it. The caller should free the memory allocated here.
//  Arguments   :   Integer pointer for Oprom Header location
//  Returns     :   Boolean
//-----------------------------------------------------------------------------
BOOLEAN VBTSIMULATION_CopyTestOpromHeaderFromRegistry(GFX_ADAPTER_CONTEXT gfxAdapterContext, DDU8 *pHeaderBase, DDU32 Size)
{
    NTSTATUS NtStatus;
    BOOLEAN  ret        = FALSE;
    DDU32    HeaderSize = 0;
    WCHAR    RegistryKey[MAX_PATH_STRING_LEN];

    wcscpy(RegistryKey, gfxAdapterContext.PCIBusDeviceId);
    wcscat_s(RegistryKey, MAX_PATH_STRING_LEN, SIMDRV_REGKEY_CUSTOM_OPROM_SIZE);

    NtStatus = COMMONCORE_GetRegistryInfo(RegistryKey, REG_DWORD, &HeaderSize, sizeof(DDU32));
    ret      = NT_SUCCESS(NtStatus) ? TRUE : FALSE;

    if (ret == FALSE)
    {
        GFXVALSIM_DBG_MSG("Failed to read Oprom size from registry !!\r\n");
        return FALSE;
    }
    else if (HeaderSize != Size)
    {
        GFXVALSIM_DBG_MSG("Mismatch in size between Oprom and  Registry!!\r\n");
        return FALSE;
    }

    wcscpy(RegistryKey, gfxAdapterContext.PCIBusDeviceId);
    wcscat_s(RegistryKey, MAX_PATH_STRING_LEN, SIMDRV_REGKEY_CUSTOM_OPROM);
    NtStatus = COMMONCORE_GetRegistryInfo(RegistryKey, REG_BINARY, pHeaderBase, Size);

    ret = NT_SUCCESS(NtStatus) ? TRUE : FALSE;
    if (ret == FALSE)
    {
        GFXVALSIM_DBG_MSG("Failed to read Oprom from registry !!\r\n");
        return FALSE;
    }

    return TRUE;
}

//----------------------------------------------------------------------------
//  Function    :   VBTSIMULATION_WriteDefaultVBT
//  Type        :   Helper Function
//  Description :   Write Default VBT read from Opregion to Registry
//  Returns     :   VOID
//-----------------------------------------------------------------------------
VOID VBTSIMULATION_WriteDefaultVBT(GFX_ADAPTER_CONTEXT gfxAdapterContext, DDU8 *pVBTBase, DDU32 VbtSize)
{
    do
    {
        if (NULL == pVBTBase)
        {
            GFXVALSIM_DBG_MSG("Invalid memory passed: pVBTBase to copy to default VBT registry");
            break;
        }
        wcscat_s(gfxAdapterContext.PCIBusDeviceId, MAX_PATH_STRING_LEN, SIMDRV_REGKEY_DEFAULT_VBT);
        COMMONCORE_SetRegistryInfo(gfxAdapterContext.PCIBusDeviceId, REG_BINARY, pVBTBase, VbtSize);
        wcscat_s(gfxAdapterContext.PCIBusDeviceId, MAX_PATH_STRING_LEN, _SIZE);
        COMMONCORE_SetRegistryInfo(gfxAdapterContext.PCIBusDeviceId, REG_DWORD, &VbtSize, sizeof(DDU32));

    } while (FALSE);
}

//----------------------------------------------------------------------------
//  Function    :   WriteActualVBT
//  Type        :   Helper Function
//  Description :   Write VBT read from PCI config space to Registry
//  Returns     :   VOID
//-----------------------------------------------------------------------------
VOID VBTSIMULATION_WriteActualVBT(GFX_ADAPTER_CONTEXT gfxAdapterContext, DDU8 *pVBTBase, DDU32 VbtSize)
{
    do
    {
        if (NULL == pVBTBase)
            break;
        wcscat_s(gfxAdapterContext.PCIBusDeviceId, MAX_PATH_STRING_LEN, SIMDRV_REGKEY_ACTUAL_VBT);
        COMMONCORE_SetRegistryInfo(gfxAdapterContext.PCIBusDeviceId, REG_BINARY, pVBTBase, VbtSize);
        wcscat_s(gfxAdapterContext.PCIBusDeviceId, MAX_PATH_STRING_LEN, _SIZE);
        COMMONCORE_SetRegistryInfo(gfxAdapterContext.PCIBusDeviceId, REG_DWORD, &VbtSize, sizeof(DDU32));

    } while (FALSE);
}

//----------------------------------------------------------------------------
//  Function    :   WriteActualOpromHeader
//  Type        :   Helper Function
//  Description :   Write Oprom Signature and Opregion Header from PCI config space to Registry
//  Returns     :   VOID
//-----------------------------------------------------------------------------
VOID VBTSIMULATION_WriteActualOpromHeader(GFX_ADAPTER_CONTEXT gfxAdapterContext, DDU8 *pHeaderBase, DDU32 Size)
{
    do
    {
        if (NULL == pHeaderBase)
            break;
        wcscat_s(gfxAdapterContext.PCIBusDeviceId, MAX_PATH_STRING_LEN, SIMDRV_REGKEY_ACTUAL_OPROM_HEADER);
        COMMONCORE_SetRegistryInfo(gfxAdapterContext.PCIBusDeviceId, REG_BINARY, pHeaderBase, Size);
        wcscat_s(gfxAdapterContext.PCIBusDeviceId, MAX_PATH_STRING_LEN, _SIZE);
        COMMONCORE_SetRegistryInfo(gfxAdapterContext.PCIBusDeviceId, REG_DWORD, &Size, sizeof(DDU32));

    } while (FALSE);
}
//----------------------------------------------------------------------------
//  Function    :   WriteActualOpromHeader
//  Type        :   Helper Function
//  Description :   Write Oprom Signature and Opregion Header from PCI config space to Registry
//  Returns     :   VOID
//-----------------------------------------------------------------------------
VOID VBTSIMULATION_WriteActualOpromFooter(GFX_ADAPTER_CONTEXT gfxAdapterContext, DDU8 *pFooterBase, DDU32 Size)
{
    do
    {
        if (NULL == pFooterBase)
            break;
        wcscat_s(gfxAdapterContext.PCIBusDeviceId, MAX_PATH_STRING_LEN, SIMDRV_REGKEY_ACTUAL_OPROM_FOOTER);
        COMMONCORE_SetRegistryInfo(gfxAdapterContext.PCIBusDeviceId, REG_BINARY, pFooterBase, Size);
        wcscat_s(gfxAdapterContext.PCIBusDeviceId, MAX_PATH_STRING_LEN, _SIZE);
        COMMONCORE_SetRegistryInfo(gfxAdapterContext.PCIBusDeviceId, REG_DWORD, &Size, sizeof(DDU32));

    } while (FALSE);
}
#pragma endregion

#pragma region APIs

//----------------------------------------------------------------------------
//  Function    :   VBTSIMULATION_GetOpregionDetails
//  Type        :   API
//  Description :   Write VBT data from PCI config space to Registry. Caller has to unmap pOpregionBaseVirtualAddr if it is not NULL
//  Returns     :   VOID
//-----------------------------------------------------------------------------
BOOLEAN VBTSIMULATION_GetOpregionDetails(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PLATFORM_INFO stPlatformInfo, PSIMDRV_OPREGION_VBT_DETAILS pOpRegionVbtDetails)
{
    PEXPANSION_ROM_HEADER pRomData             = NULL;
    DDU8 *                pIoMappedVirtualAddr = NULL;
    OPREGION_HEADER *     pOpRegionHeader      = NULL;
    DDU32                 OpRegionSize         = 0;
    DDU8 *                pVBTBase             = NULL;
    DDU32                 VbtSize              = 0;
    BOOLEAN               bReadFromSpi         = FALSE;
    BOOLEAN               bUnmapVirtualAddr    = FALSE;

    if (TRUE == pGfxAdapterContext->isDisplayLessAdapter)
        return FALSE;

    if (((stPlatformInfo.eProductFamily == eIGFX_DG100 || stPlatformInfo.eProductFamily == eIGFX_DG2) && pGfxAdapterContext->bIsPreSi == FALSE) ||
        (stPlatformInfo.eProductFamily == eIGFX_ELG) || (stPlatformInfo.eProductFamily ==eIGFX_CLS))
    {
        bReadFromSpi = TRUE;
    }

    if (bReadFromSpi)
    {
        OPREGION_MAILBOX3 *pOpregionMailBox3;
        VBTSIMULATION_GetROMDataFromPCIROM(pGfxAdapterContext, pOpRegionVbtDetails);
        pRomData = (PEXPANSION_ROM_HEADER)pOpRegionVbtDetails->pCodeOpRomBase;
        // pRomData = pGfxAdapterContext->pvExpansionRomHeader;
        if (pRomData == NULL)
        {
            GFXVALSIM_DBG_MSG("VBTSIMULATION_DumpVBTFromPCI: Failed to read ROM data!\r\n");
            return FALSE;
        }

        // Opregion address will be stored at offset 0x1A per Intel OPROM design
        DDU8 *pOpregionBase = ((DDU8 *)pRomData + pRomData->OpregionBase);
        pOpregionMailBox3   = (OPREGION_MAILBOX3 *)(pOpregionBase + MAILBOX3_OFFSET);
        GFXVALSIM_DBG_MSG("Oprom: OpregionMailBox3->RVDSField :%uld, pOpregionMailBox3->RVDAField :%ulld.", pOpregionMailBox3->RVDSField, pOpregionMailBox3->RVDAField);
        if (pOpregionMailBox3->RVDSField != 0 && pOpregionMailBox3->RVDAField != 0)
        {
            pVBTBase = pOpregionBase + pOpregionMailBox3->RVDAField;
            VbtSize  = pOpregionMailBox3->RVDSField;
        }
        else
        {
            pVBTBase = pOpregionBase + MAILBOX4_OFFSET; // VBT data starts from MailBox4 Offset.
            VbtSize  = MIN_VBT_SIZE;
        }

        // ACPI opregion spec https://gfxspecs.intel.com/Predator/Home/Index/53441
        pIoMappedVirtualAddr = pOpregionBase;
        OpRegionSize         = KB_TO_BYTE(((OPREGION_HEADER *)pOpregionBase)->OpregionSize); // Size in header will be in KB
        GFXVALSIM_DBG_MSG("Oprom: OpRegionSize :%uld", OpRegionSize);

        // pOpRegionVbtDetails->OPRomHeaderSize += (DDU32)(((DDU8 *)pOpRegionVbtDetails->pCodeOpRomBase - pVBTBase)* sizeof(pVBTBase));
        pOpRegionVbtDetails->OPRomHeaderSize += (DDU32)(pVBTBase - pOpRegionVbtDetails->pCodeOpRomBase);
        pOpRegionVbtDetails->OPRomFooterSize = (pGfxAdapterContext->OPRomTotalSize - pOpRegionVbtDetails->OPRomHeaderSize - VbtSize);
    }
    else
    {
        bUnmapVirtualAddr = TRUE;
        // Offset 0xFC in iGfx case contains Physical address of Opregion memory
        // This cannot be 0 in iGfx case. Only in dGPU case(Non-MBD), this will be 0
        OPREGION_MAILBOX3 *pOpregionMailBox3;
        PHYSICAL_ADDRESS   PhysicalAddress = { 0 };
        PhysicalAddress.LowPart            = VBTSIMULATION_GetOpRegionPHYAddr(pGfxAdapterContext);
        pIoMappedVirtualAddr               = (DDU8 *)MmMapIoSpace(PhysicalAddress, TOTAL_OPREGION_SIZE, MmNonCached); // pIoMappedVirtualAddress contains the OpRegion Base address.

        if (pIoMappedVirtualAddr == NULL)
        {
            GFXVALSIM_DBG_MSG("VBTSIMULATION_DumpVBTFromPCI: Unable to map memory!\r\n");
            return FALSE;
        }

        pOpregionMailBox3 = (OPREGION_MAILBOX3 *)(pIoMappedVirtualAddr + MAILBOX3_OFFSET); // MailBox3 is present at 0x300 from OpRegion Base
        GFXVALSIM_DBG_MSG("OpregionMailBox3->RVDSField :%uld, pOpregionMailBox3->RVDAField :%ulld.", pOpregionMailBox3->RVDSField, pOpregionMailBox3->RVDAField);

        // VBT data is present in extended offset because its size > 6KB. So get the VBT Base from RVDS and RVDA fields.
        if (pOpregionMailBox3->RVDSField != 0 && pOpregionMailBox3->RVDAField != 0)
        {
            GFXVALSIM_DBG_MSG("rvds and rvda not 0!\r\n");
            DDU32 VbtBaseRelativeAddr = 0;
            pOpRegionHeader           = (OPREGION_HEADER *)pIoMappedVirtualAddr;

            if ((MAJOR_VERSION_2 == pOpRegionHeader->OpregionVersion.MajorVersion) &&
                (MINOR_VERISON_0 == pOpRegionHeader->OpregionVersion.MinorVersion)) // For Opregion version 2.0, VBT Physical address is present in RVDA field.
            {
                GFXVALSIM_DBG_MSG("opregion 2.0\r\n");
                PhysicalAddress.QuadPart =
                pOpregionMailBox3->RVDAField; // VBT Base Physical address would be present at RVDA Field. So, Remap the physical address to get virtual address.
                OpRegionSize        = pOpregionMailBox3->RVDSField; // store the vbt size for remapping.
                VbtBaseRelativeAddr = 0;                            // As we are getting directly physical address of VBT. The Relative address of VBT from OpRegion is Zero.
                VbtSize             = pOpregionMailBox3->RVDSField; // RVDSField contains the size of extended VBT.
            }
            else // For Opregion Version > 2.0, the VBT Base Relative address from OpRegion Base present at RVDA Field.
            {
                GFXVALSIM_DBG_MSG("opregion >2.0\r\n");
                OpRegionSize = TOTAL_OPREGION_SIZE + pOpregionMailBox3->RVDSField; // The New/Total Opregion size is extended with default Opregion size + VBT size.
                VbtBaseRelativeAddr =
                (DDU32)
                pOpregionMailBox3->RVDAField; // The relative address of VBT Base from OpRegion Base is present at RVDA field. The Opregion Base Physical address would remain same.
                VbtSize = pOpregionMailBox3->RVDSField; // RVDSField contains the size of extended VBT.
            }

            // unmap the 8KB OpRegion and remap along with total Opregion or extended VBT.
            MmUnmapIoSpace(pIoMappedVirtualAddr, TOTAL_OPREGION_SIZE);

            pIoMappedVirtualAddr = (DDU8 *)MmMapIoSpace(PhysicalAddress, OpRegionSize, MmNonCached);
            if (pIoMappedVirtualAddr == NULL)
            {
                GFXVALSIM_DBG_MSG("VBTSIMULATION_DumpVBTFromPCI: Unable to map memory for extended vbt!\r\n");
                return FALSE;
            }

            pVBTBase = pIoMappedVirtualAddr + VbtBaseRelativeAddr; // Add the VBT Base Relative address to Mapped Virtual address to get the VBT Base Virtual address.
        }
        else
        {
            GFXVALSIM_DBG_MSG("rvds and rvda is 0!\r\n");
            OpRegionSize = TOTAL_OPREGION_SIZE;
            pVBTBase     = pIoMappedVirtualAddr + MAILBOX4_OFFSET;
            VbtSize      = MIN_VBT_SIZE;
        }
    }

    // No Error. Copy the above assigned data and return True.
    pOpRegionVbtDetails->pOpregionBaseVirtualAddr = pIoMappedVirtualAddr;
    pOpRegionVbtDetails->OpRegionSize             = OpRegionSize;
    pOpRegionVbtDetails->pVBTBase                 = pVBTBase;
    pOpRegionVbtDetails->VbtSize                  = VbtSize;
    pOpRegionVbtDetails->bUnmapVirtualAddr        = bUnmapVirtualAddr;

    GFXVALSIM_VBT_MSG(pGfxAdapterContext->OPRomTotalSize, pOpRegionVbtDetails->OPRomHeaderSize, pOpRegionVbtDetails->OPRomFooterSize, pOpRegionVbtDetails->VbtSize,
                      pOpRegionVbtDetails->pVBTBase, pGfxAdapterContext->pvExpansionRomHeader);
    return TRUE;
}

VOID VBTSIMULATION_DumpVBTToETW()
{
    PSIMDEV_EXTENTSION pSimDrvExtension    = GetSimDrvExtension();
    PSIMDRVGFX_CONTEXT pstSimDrvGfxContext = (PSIMDRVGFX_CONTEXT)pSimDrvExtension->pvSimDrvToGfxContext;
    do
    {
        if (NULL == pstSimDrvGfxContext)
            break;
        for (INT adapterIndex = 0; adapterIndex < pstSimDrvGfxContext->gfxAdapterCount; adapterIndex++)
        {
            GFX_ADAPTER_CONTEXT gfxAdapterContext = pstSimDrvGfxContext->GfxAdapterContext[adapterIndex];
            if (gfxAdapterContext.bIsGfxReady && gfxAdapterContext.pVbtsize != 0 && gfxAdapterContext.pVbtbase != NULL)
            {
                LOG_SYSTEM_DETAILS(gfxAdapterContext.pstRxInfoArr->pstMMIOInterface->eIGFXPlatform, gfxAdapterContext.pstRxInfoArr->pstMMIOInterface->ePCHProductFamily,
                                   gfxAdapterContext.pVbtsize, gfxAdapterContext.pVbtbase);
            }
            else
            {
                GFXVALSIM_DBG_MSG("Invalid adapter context received at index {%d}. IsGfxReady:%d, VbtSize:%lu", adapterIndex, gfxAdapterContext.bIsGfxReady,
                                  gfxAdapterContext.pVbtsize);
            }
        }
    } while (FALSE);
}

//----------------------------------------------------------------------------
//  Function    :   VBTSIMULATION_DumpVBTFromPCI
//  Type        :   API
//  Description :   Write VBT data from PCI config space to Registry
//  Returns     :   VOID
//-----------------------------------------------------------------------------
VOID VBTSIMULATION_DumpVBTFromPCI(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PSIMDRV_OPREGION_VBT_DETAILS pOpRegionVbtDetails)
{
    VBTSIMULATION_WriteActualVBT(*pGfxAdapterContext, pOpRegionVbtDetails->pVBTBase, pOpRegionVbtDetails->VbtSize); // This might go to else loop below.

    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();

    if (pOpRegionVbtDetails->pVBTBase != NULL)
    {
        pGfxAdapterContext->pVbtbase = pstPortingObj->pfnAllocateMem(pOpRegionVbtDetails->VbtSize, TRUE);
        if (pGfxAdapterContext->pVbtbase != NULL)
        {
            memcpy_s(pGfxAdapterContext->pVbtbase, pOpRegionVbtDetails->VbtSize, pOpRegionVbtDetails->pVBTBase, pOpRegionVbtDetails->VbtSize);
            pGfxAdapterContext->pVbtsize = pOpRegionVbtDetails->VbtSize;
        }
    }
    if (pGfxAdapterContext->pvExpansionRomHeader != NULL)
    {
        VBTSIMULATION_WriteActualOpromHeader(*pGfxAdapterContext, pGfxAdapterContext->pvExpansionRomHeader, pOpRegionVbtDetails->OPRomHeaderSize);
        VBTSIMULATION_WriteActualOpromFooter(*pGfxAdapterContext,
                                             ((DDU8 *)pGfxAdapterContext->pvExpansionRomHeader + pOpRegionVbtDetails->OPRomHeaderSize + pOpRegionVbtDetails->VbtSize),
                                             pOpRegionVbtDetails->OPRomFooterSize);
    }
}

//----------------------------------------------------------------------------
//  Function    :   VBTSIMULATION_DumpOpRegionFromPCI
//  Type        :   API
//  Description :   Write OpRegion data from PCI config space to Registry
//  Returns     :   VOID
//-----------------------------------------------------------------------------
VOID VBTSIMULATION_DumpOpRegionFromPCI(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PSIMDRV_OPREGION_VBT_DETAILS pOpRegionVbtDetails)
{
    WCHAR RegistryName[MAX_PATH_STRING_LEN];

    do
    {
        if (NULL == pOpRegionVbtDetails->pOpregionBaseVirtualAddr)
        {
            GFXVALSIM_DBG_MSG("pOpRegionVbtDetails->pOpregionBaseVirtualAddr is NULL");
            break;
        }

        wcscpy_s(RegistryName, MAX_PATH_STRING_LEN, pGfxAdapterContext->PCIBusDeviceId);
        wcscat_s(RegistryName, MAX_PATH_STRING_LEN, SIMDRV_REGKEY_ACTUAL_OPREGION);
        COMMONCORE_SetRegistryInfo(RegistryName, REG_BINARY, pOpRegionVbtDetails->pOpregionBaseVirtualAddr, pOpRegionVbtDetails->OpRegionSize);
        wcscat_s(RegistryName, MAX_PATH_STRING_LEN, _SIZE);
        COMMONCORE_SetRegistryInfo(RegistryName, REG_DWORD, &pOpRegionVbtDetails->OpRegionSize, sizeof(DDU32));

    } while (FALSE);
}

//----------------------------------------------------------------------------
//  Function    :   VBTSIMULATION_ConfigureTestVBT
//  Type        :   API
//  Description :   VBT simulation interface to dump VBT from PCI config and
//                  configure new VBT from registry if required
//  Returns     :   VOID
//-----------------------------------------------------------------------------
VOID VBTSIMULATION_ConfigureTestVBT(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PSIMDRV_OPREGION_VBT_DETAILS pOpRegionVbtDetails, BOOLEAN vbt_simulation_enabled)
{

    if (vbt_simulation_enabled)
    {
        GFXVALSIM_DBG_MSG("VBTSIMULATION enabled!\r\n");

        if (pGfxAdapterContext->pvExpansionRomHeader != NULL) // For DG Platforms(except Mother Board Down Solution) this path would be taken
        {
            // OpromHeaderSize = pOpRegionVbtDetails->OPRomHeaderSize; // 2048 + 0x3c + 8 * 1024; // pGfxAdapterContext->OPRomTotalSize - OpRegionVbtDetails.VbtSize;
            if (VBTSIMULATION_CopyTestOpromHeaderFromRegistry(*pGfxAdapterContext, pGfxAdapterContext->pvExpansionRomHeader, pGfxAdapterContext->OPRomTotalSize) == FALSE)
            {
                GFXVALSIM_DBG_MSG("VBTSIMULATION_ConfigureTestVBT: Failed to read OpromHeader from registry!\r\n");
            }
        }
        else
        {
            if (VBTSIMULATION_CopyTestVBTFromRegistry(*pGfxAdapterContext, pOpRegionVbtDetails->pVBTBase, pOpRegionVbtDetails->VbtSize) == FALSE)
            {
                GFXVALSIM_DBG_MSG("VBTSIMULATION_ConfigureTestVBT: Failed to read VBT from registry!\r\n");
            }
        }
    }
    else
    {
        GFXVALSIM_DBG_MSG("VBTSIMULATION not enabled!\r\n");
    }
    return;
}

//----------------------------------------------------------------------------
//  Function    :   VBTSimulation_DeleteDefaultVBT
//  Type        :   API
//  Description :   Free allocated memory
//  Returns     :   VOID
//-----------------------------------------------------------------------------
BOOLEAN VBTSimulation_DeleteDefaultVBT(GFX_ADAPTER_CONTEXT gfxAdapterContext)
{
    NTSTATUS NtStatus;
    GFXVALSIM_FUNC_ENTRY();

    wcscat_s(gfxAdapterContext.PCIBusDeviceId, MAX_PATH_STRING_LEN, SIMDRV_REGKEY_DEFAULT_VBT);
    NtStatus = COMMONCORE_DeleteRegistryInfo(gfxAdapterContext.PCIBusDeviceId);

    if (NT_SUCCESS(NtStatus) == FALSE)
    {
        GFXVALSIM_DBG_MSG("Failed to delete default VBT registry");
        GFXVALSIM_FUNC_EXIT(FALSE);
        return FALSE;
    }

    wcscat_s(gfxAdapterContext.PCIBusDeviceId, MAX_PATH_STRING_LEN, _SIZE);
    NtStatus = COMMONCORE_DeleteRegistryInfo(gfxAdapterContext.PCIBusDeviceId);

    if (NT_SUCCESS(NtStatus) == FALSE)
    {
        GFXVALSIM_DBG_MSG("Failed to delete default VBT size registry");
        GFXVALSIM_FUNC_EXIT(FALSE);
        return FALSE;
    }

    GFXVALSIM_FUNC_EXIT(TRUE);
    return TRUE;
}

//----------------------------------------------------------------------------
//  Function    :   VBTSIMULATION_Cleanup
//  Type        :   API
//  Description :   Free allocated memory
//  Returns     :   VOID
//-----------------------------------------------------------------------------
VOID VBTSIMULATION_Cleanup(PGFX_ADAPTER_CONTEXT pGfxAdapterContext)
{
    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();
    do
    {
        if (NULL == pGfxAdapterContext)
            break;
        if (pGfxAdapterContext->pVbtbase != NULL)
        {
            pstPortingObj->pfnFreeMem(pGfxAdapterContext->pVbtbase);
            pGfxAdapterContext->pVbtbase = NULL;
        }
        if (pGfxAdapterContext->pvExpansionRomHeader != NULL)
        {
            pstPortingObj->pfnFreeMem(pGfxAdapterContext->pvExpansionRomHeader);
            pGfxAdapterContext->pvExpansionRomHeader = NULL;
        }
    } while (FALSE);
}

#pragma endregion