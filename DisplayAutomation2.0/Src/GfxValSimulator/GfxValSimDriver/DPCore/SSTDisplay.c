
#include "SSTDisplay.h"
#include "AuxDefs.h"
#include "..\CommonInclude\ETWLogging.h"

PI2C_SLAVE_INFO SSTDISPLAY_RegisterI2CSlaves(PSST_DISPLAY_INFO pstSSTDisplayInfo, ULONG ulSlaveStartAddress, ULONG ulSlaveEndAddress, ULONG ulSlaveBuffSize,
                                             PFN_I2CSLAVEINITROUTINE pfnI2CSlaveInitRoutine, PFN_I2CSLAVEINITROUTINE pfnI2CSlaveUpdateRoutine,
                                             PFN_I2CSLAVECLEANUPROUTINE pfnI2CSlaveCleanUpRoutine, PFN_I2CSLAVEHANDLER pfnI2CSlaveReadHandler,
                                             PFN_I2CSLAVEHANDLER pfnI2CSlaveWriteHandler,
                                             PVOID               pvCallerPersistedContext, // Caller would persist this data as long as it uses this client
                                             PVOID               pvCallerNonPersistedData, // Caller won't persist this data after this call returns so client needs to copy
                                             ULONG               ulNonPersistedSize);

BOOLEAN SSTDISPLAY_RegisterOffsetsOnExistingHandler(PSST_DISPLAY_INFO pstSSTDisplayInfo, PI2C_SLAVE_INFO pstI2CSlaveInfo, ULONG ulSlaveStartAddress, ULONG ulSlaveEndAddress);

PI2C_SLAVE_INFO SSTDISPLAY_GetI2CSlaveInfoObjFromSlaveAddress(PSST_DISPLAY_INFO pstSSTDisplayInfo, ULONG ulSlaveStartAddress, ULONG ulSlaveEndAddress);

PSST_DISPLAY_INFO SSTDISPLAY_SSTDisplayInit(void)
{
    GFXVALSIM_FUNC_ENTRY();

    BOOLEAN           bRet              = FALSE;
    PSST_DISPLAY_INFO pstSSTDisplayInfo = NULL;
    PI2C_SLAVE_INFO   pstI2CSlaveInfo   = NULL;
    PPORTINGLAYER_OBJ pstPortingObj     = GetPortingObj();

    do
    {
        pstSSTDisplayInfo = pstPortingObj->pfnAllocateMem(sizeof(SST_DISPLAY_INFO), TRUE);

        if (pstSSTDisplayInfo == NULL)
        {
            break;
        }

        if (FALSE == pstPortingObj->pfnInitializeListHead(&pstSSTDisplayInfo->I2CSlaveInfoListHead))
        {
            break;
        }

        pstI2CSlaveInfo = SSTDISPLAY_RegisterI2CSlaves(pstSSTDisplayInfo, I2C_EDID_SLAVE_ADDRESS, I2C_EDID_SLAVE_ADDRESS, AUX_MAX_TXN_LEN, NULL,
                                                       I2CSLAVES_DDCEDIDUpdateRoutine, // Update Routine
                                                       I2CSLAVES_DDCEDIDCleanUpRoutine, I2CSLAVES_DDCEDIDHandler, I2CSLAVES_DDCEDIDHandler,
                                                       NULL, // Caller would persist this data as long as it uses this client
                                                       NULL, // Caller won't persist this data after this call returns so client needs to copy
                                                       0);

        if (pstI2CSlaveInfo)
        {
            bRet = SSTDISPLAY_RegisterOffsetsOnExistingHandler(pstSSTDisplayInfo, pstI2CSlaveInfo, I2C_EDID_SEGPTR_ADDRESS, I2C_EDID_SEGPTR_ADDRESS);
        }

    } while (FALSE);

    if (bRet == FALSE && pstSSTDisplayInfo)
    {
        pstPortingObj->pfnFreeMem(pstSSTDisplayInfo);
        pstSSTDisplayInfo = NULL;
    }

    GFXVALSIM_FUNC_EXIT(!bRet);

    return pstSSTDisplayInfo;
}

PI2C_SLAVE_INFO SSTDISPLAY_RegisterI2CSlaves(PSST_DISPLAY_INFO pstSSTDisplayInfo, ULONG ulSlaveStartAddress, ULONG ulSlaveEndAddress, ULONG ulSlaveBuffSize,
                                             PFN_I2CSLAVEINITROUTINE    pfnI2CSlaveInitRoutine,
                                             PFN_I2CSLAVEINITROUTINE    pfnI2CSlaveUpdateRoutine, // Used for updating data anytime after registering
                                             PFN_I2CSLAVECLEANUPROUTINE pfnI2CSlaveCleanUpRoutine, PFN_I2CSLAVEHANDLER pfnI2CSlaveReadHandler,
                                             PFN_I2CSLAVEHANDLER pfnI2CSlaveWriteHandler,
                                             PVOID               pvCallerPersistedContext, // Caller would persist this data as long as it uses this client
                                             PVOID               pvCallerNonPersistedData, // Caller won't persist this data after this call returns so client needs to copy
                                             ULONG               ulNonPersistedSize)
{
    GFXVALSIM_FUNC_ENTRY();

    PPORTINGLAYER_OBJ pstPortingObj  = GetPortingObj();
    BOOLEAN           bRet           = TRUE;
    BOOLEAN           bHandlerExists = FALSE;

    PI2C_SLAVE_INFO pstI2CSlaveInfo = NULL;
    PDP_LIST_ENTRY  pDPListEntry    = NULL;

    do
    {

        // The link list implementation can be changed to Array List from Link list to fasten up the code
        if ((pfnI2CSlaveReadHandler == NULL) && (pfnI2CSlaveWriteHandler == NULL))
        {
            bRet = FALSE;
            break;
        }

        pDPListEntry = pstPortingObj->pfnInterLockedTraverseList(&pstSSTDisplayInfo->I2CSlaveInfoListHead, pDPListEntry);

        while (pDPListEntry)
        {
            // Lets check if a client isn't alread registered, in which case print error and exit
            pstI2CSlaveInfo = (PI2C_SLAVE_INFO)pDPListEntry;
            ULONG ulCount   = 0;
            for (ulCount = 0; ulCount < pstI2CSlaveInfo->stSlaveOffsetsArray.ulNumOffsetRanges; ulCount++)
            {
                if (ulSlaveStartAddress >= pstI2CSlaveInfo->stSlaveOffsetsArray.stI2CSlaveOffsets[ulCount].ulSlaveStartAddress &&
                    ulSlaveEndAddress <= pstI2CSlaveInfo->stSlaveOffsetsArray.stI2CSlaveOffsets[ulCount].ulSlaveEndAddress)
                {
                    // printf("I2C Client Already registered for the given DPCD range /r/n");
                    bHandlerExists = TRUE;
                    break; // break from while loop
                }
            }

            if (bHandlerExists)
            {
                break;
            }

            pDPListEntry = pstPortingObj->pfnInterLockedTraverseList(&pstSSTDisplayInfo->I2CSlaveInfoListHead, pDPListEntry);
        }

        if (pDPListEntry)
        {
            // Someone Trying to re-register a client. Break with False
            pstI2CSlaveInfo = NULL;
            bRet            = FALSE;
            break;
        }

        pstI2CSlaveInfo = (PI2C_SLAVE_INFO)pstPortingObj->pfnAllocateMem(sizeof(I2C_SLAVE_INFO), TRUE);

        if (!pstI2CSlaveInfo)
        {
            // Registration Failed
            bRet = FALSE;
            break;
        }

        pstI2CSlaveInfo->stSlaveOffsetsArray.stI2CSlaveOffsets[pstI2CSlaveInfo->stSlaveOffsetsArray.ulNumOffsetRanges].ulSlaveStartAddress = ulSlaveStartAddress;
        pstI2CSlaveInfo->stSlaveOffsetsArray.stI2CSlaveOffsets[pstI2CSlaveInfo->stSlaveOffsetsArray.ulNumOffsetRanges].ulSlaveEndAddress   = ulSlaveEndAddress;
        pstI2CSlaveInfo->stSlaveOffsetsArray.ulNumOffsetRanges++;

        pstI2CSlaveInfo->ulSlaveTransBuffSize = ulSlaveBuffSize;

        pstI2CSlaveInfo->pfnI2CSlaveReadHandler  = pfnI2CSlaveReadHandler;
        pstI2CSlaveInfo->pfnI2CSlaveWriteHandler = pfnI2CSlaveWriteHandler;

        pstI2CSlaveInfo->pfnI2CSlaveCleanUpRoutine = pfnI2CSlaveCleanUpRoutine;
        pstI2CSlaveInfo->pfnI2CSlaveUpdateRoutine  = pfnI2CSlaveUpdateRoutine;

        if (ulSlaveBuffSize)
        {
            pstI2CSlaveInfo->pucSlaveIntermediateDataBuff = pstPortingObj->pfnAllocateMem(ulSlaveBuffSize, TRUE);

            if (pstI2CSlaveInfo->pucSlaveIntermediateDataBuff == NULL)
            {
                bRet = FALSE;
                break;
            }
        }

        if (pfnI2CSlaveInitRoutine)
        {
            pfnI2CSlaveInitRoutine(pstI2CSlaveInfo, pvCallerNonPersistedData, ulNonPersistedSize);
        }

        // Insert in the slave list
        pstPortingObj->pfnInterlockedInsertTailList(&pstSSTDisplayInfo->I2CSlaveInfoListHead, &pstI2CSlaveInfo->DPListEntry);

    } while (FALSE);

    if (bRet == FALSE && pstI2CSlaveInfo)
    {
        pstPortingObj->pfnFreeMem(pstI2CSlaveInfo);
        pstI2CSlaveInfo = NULL;
    }

    GFXVALSIM_FUNC_EXIT(!bRet);
    return pstI2CSlaveInfo;
}

BOOLEAN SSTDISPLAY_RegisterOffsetsOnExistingHandler(PSST_DISPLAY_INFO pstSSTDisplayInfo, PI2C_SLAVE_INFO pstI2CSlaveInfo, ULONG ulSlaveStartAddress, ULONG ulSlaveEndAddress)
{
    GFXVALSIM_FUNC_ENTRY();

    BOOLEAN           bRet                = FALSE;
    BOOLEAN           bHandlerExists      = FALSE;
    PDP_LIST_ENTRY    pDPListEntry        = NULL;
    PI2C_SLAVE_INFO   pstTempI2CSlaveInfo = NULL;
    PPORTINGLAYER_OBJ pstPortingObj       = GetPortingObj();

    do
    {
        if (pstI2CSlaveInfo->stSlaveOffsetsArray.ulNumOffsetRanges >= MAX_OFFSETRANGE_PER_SLAVEINFO)
        {
            break;
        }

        if ((pstSSTDisplayInfo == NULL) && (pstI2CSlaveInfo == NULL))
        {
            bRet = FALSE;
            break;
        }

        pDPListEntry = pstPortingObj->pfnInterLockedTraverseList(&pstSSTDisplayInfo->I2CSlaveInfoListHead, pDPListEntry);

        while (pDPListEntry)
        {
            // Lets check if a client isn't alread registered, in which case print error and exit
            pstTempI2CSlaveInfo = (PI2C_SLAVE_INFO)pDPListEntry;
            ULONG ulCount       = 0;
            for (ulCount = 0; ulCount < pstTempI2CSlaveInfo->stSlaveOffsetsArray.ulNumOffsetRanges; ulCount++)
            {
                if (ulSlaveStartAddress >= pstTempI2CSlaveInfo->stSlaveOffsetsArray.stI2CSlaveOffsets[ulCount].ulSlaveStartAddress &&
                    ulSlaveEndAddress <= pstTempI2CSlaveInfo->stSlaveOffsetsArray.stI2CSlaveOffsets[ulCount].ulSlaveEndAddress)
                {
                    // printf("I2C Client Already registered for the given DPCD range /r/n");
                    bHandlerExists = TRUE;
                    break; // break from while loop
                }
            }

            if (bHandlerExists)
            {
                break;
            }

            pDPListEntry = pstPortingObj->pfnInterLockedTraverseList(&pstSSTDisplayInfo->I2CSlaveInfoListHead, pDPListEntry);
        }

        if (pDPListEntry)
        {
            // Someone Trying to re-register a client. Break with False
            bRet = FALSE;
            break;
        }

        pstI2CSlaveInfo->stSlaveOffsetsArray.stI2CSlaveOffsets[pstI2CSlaveInfo->stSlaveOffsetsArray.ulNumOffsetRanges].ulSlaveStartAddress = ulSlaveStartAddress;
        pstI2CSlaveInfo->stSlaveOffsetsArray.stI2CSlaveOffsets[pstI2CSlaveInfo->stSlaveOffsetsArray.ulNumOffsetRanges].ulSlaveEndAddress   = ulSlaveEndAddress;
        pstI2CSlaveInfo->stSlaveOffsetsArray.ulNumOffsetRanges++;

        bRet = TRUE;

    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}

PI2C_SLAVE_INFO SSTDISPLAY_GetI2CSlaveInfoObjFromSlaveAddress(PSST_DISPLAY_INFO pstSSTDisplayInfo, ULONG ulSlaveStartAddress, ULONG ulSlaveEndAddress)
{
    BOOLEAN           bHandlerFound   = FALSE;
    PDP_LIST_ENTRY    pDPListEntry    = NULL;
    PI2C_SLAVE_INFO   pstI2CSlaveInfo = NULL;
    PPORTINGLAYER_OBJ pstPortingObj   = GetPortingObj();

    pDPListEntry = pstPortingObj->pfnInterLockedTraverseList(&pstSSTDisplayInfo->I2CSlaveInfoListHead, pDPListEntry);

    while (pDPListEntry)
    {
        // Lets check if a client isn't alread registered, in which case print error and exit
        pstI2CSlaveInfo = (PI2C_SLAVE_INFO)pDPListEntry;
        ULONG ulCount   = 0;
        for (ulCount = 0; ulCount < pstI2CSlaveInfo->stSlaveOffsetsArray.ulNumOffsetRanges; ulCount++)
        {
            if (ulSlaveStartAddress >= pstI2CSlaveInfo->stSlaveOffsetsArray.stI2CSlaveOffsets[ulCount].ulSlaveStartAddress &&
                ulSlaveEndAddress <= pstI2CSlaveInfo->stSlaveOffsetsArray.stI2CSlaveOffsets[ulCount].ulSlaveEndAddress)
            {
                bHandlerFound = TRUE;
                break; // break from while loop
            }
        }

        if (bHandlerFound)
        {
            break;
        }

        pDPListEntry = pstPortingObj->pfnInterLockedTraverseList(&pstSSTDisplayInfo->I2CSlaveInfoListHead, pDPListEntry);
    }

    return (PI2C_SLAVE_INFO)pDPListEntry;
}

BOOLEAN SSTDISPLAY_SetEDIDData(PSST_DISPLAY_INFO pstSSTDisplayInfo, ULONG ulEDIDSize, PUCHAR pucEDIDBuff)
{
    BOOLEAN         bRet            = FALSE;
    PI2C_SLAVE_INFO pstI2CSlaveInfo = NULL;

    do
    {
        if (pstSSTDisplayInfo == NULL || ulEDIDSize == 0 || pucEDIDBuff == NULL)
        {
            break;
        }

        pstI2CSlaveInfo = SSTDISPLAY_GetI2CSlaveInfoObjFromSlaveAddress(pstSSTDisplayInfo, I2C_EDID_SLAVE_ADDRESS, I2C_EDID_SLAVE_ADDRESS);

        if (pstI2CSlaveInfo == NULL)
        {
            break;
        }

        if (pstI2CSlaveInfo->pfnI2CSlaveUpdateRoutine == NULL)
        {
            break;
        }

        pstI2CSlaveInfo->pfnI2CSlaveUpdateRoutine(pstI2CSlaveInfo, pucEDIDBuff, ulEDIDSize);

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN SSTDISPLAY_Cleanup(PSST_DISPLAY_INFO pstSSTDisplayInfo)
{
    BOOLEAN           bRet            = FALSE;
    PDP_LIST_ENTRY    pDPTempEntry    = NULL;
    PI2C_SLAVE_INFO   pstI2CSlaveInfo = NULL;
    PPORTINGLAYER_OBJ pstPortingObj   = GetPortingObj();

    // Take out any registered I2C Slave Handlers for an I2C Address
    pDPTempEntry = pstPortingObj->pfnInterlockedRemoveHeadList(&pstSSTDisplayInfo->I2CSlaveInfoListHead);

    while (pDPTempEntry)
    {
        pstI2CSlaveInfo = (PI2C_SLAVE_INFO)pDPTempEntry;

        if (pstI2CSlaveInfo)
        {
            // If a registered I2C slave handler has a clean up routine registered, call it to do the I2C slave handler
            // specific cleanup.
            if (pstI2CSlaveInfo->pfnI2CSlaveCleanUpRoutine)
            {
                pstI2CSlaveInfo->pfnI2CSlaveCleanUpRoutine(pstI2CSlaveInfo);
            }

            pstPortingObj->pfnFreeMem(pstI2CSlaveInfo);
        }

        pDPTempEntry = pstPortingObj->pfnInterlockedRemoveHeadList(&pstSSTDisplayInfo->I2CSlaveInfoListHead);
    }

    bRet = TRUE;

    return bRet;
}
