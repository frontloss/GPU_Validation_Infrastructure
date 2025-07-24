#include "I2CSlaves.h"
#include "SST_MST_Common.h"
#include "..\CommonInclude\ETWLogging.h"

BOOLEAN I2CSLAVES_DDCEDIDHandler(PI2C_SLAVE_INFO pstI2CSlaveInfo)
{
    BOOLEAN                 bRet         = FALSE;
    PEDID_HOUSEKEEPING_DATA pstEDIDData  = (PEDID_HOUSEKEEPING_DATA)pstI2CSlaveInfo->pvI2CSlavePvtData;
    PUCHAR                  pucEDIDBlock = NULL;

    GFXVALSIM_FUNC_ENTRY();

    do
    {
        if (pstEDIDData == NULL)
        {
            break;
        }

        GFXVALSIM_DBG_MSG("EDID handler pstI2CSlaveInfo: eCurrAccessType=%d, ulCurrTransLen=%lu, ulCurrTransAddr=%lu\r\n", pstI2CSlaveInfo->eCurrAccessType,
                          pstI2CSlaveInfo->ulCurrTransLen, pstI2CSlaveInfo->ulCurrTransAddr);
        GFXVALSIM_DBG_MSG("EDID handler pstEDIDData: ulLastWriteOffset=%lu, ulLastSegPtrVal=%lu, ulBlockByteOffset=%lu\r\n", pstEDIDData->ulLastWriteOffset,
                          pstEDIDData->ulLastSegPtrVal, pstEDIDData->ulBlockByteOffset);
        if (pstI2CSlaveInfo->eCurrAccessType == eWrite)
        {
            if (pstI2CSlaveInfo->ulCurrTransLen != 1)
            {
                // For EDID read addresses, write size should always be one:
                // 1Byte Block offset for 0x50 Edid I2C slave address and 0x30 for Segment pointer offset

                GFXVALSIM_DBG_MSG("Expected transaction length as 1 for Write transcations. Actual length = %lu", pstI2CSlaveInfo->ulCurrTransLen);
                break;
            }

            if (pstI2CSlaveInfo->ulCurrTransAddr == I2C_EDID_SEGPTR_ADDRESS)
            {
                pstEDIDData->ulLastSegPtrVal = *pstI2CSlaveInfo->pucSlaveIntermediateDataBuff;
                GFXVALSIM_DBG_MSG("Segment Pointer value updated to %lu", pstEDIDData->ulLastSegPtrVal);
            }
            else if (pstI2CSlaveInfo->ulCurrTransAddr == I2C_EDID_SLAVE_ADDRESS)
            {
                // After Writing Segment pointer at 0x30, the next write should be Slave Address Write with byte offset between 0 to 0xFF
                // into a 256byte EDID block. This should be followed by a read at 0x50.
                // If we get another Write at 0x50 again instead of the above expected read then we should reset the segment pointer.
                // This is my understanding
                if (pstEDIDData->ulLastWriteOffset == I2C_EDID_SLAVE_ADDRESS)
                {
                    pstEDIDData->ulLastSegPtrVal = I2C_EDID_DEFAULT_SEGPTR;
                    GFXVALSIM_DBG_MSG("Updated to default Segment Pointer value");
                }

                pstEDIDData->ulBlockByteOffset = *pstI2CSlaveInfo->pucSlaveIntermediateDataBuff;
                pstI2CSlaveInfo->bIsIndexWrite = TRUE;
                GFXVALSIM_DBG_MSG("Updated ulBlockByteOffset to %lu and set bIsIndexWrite", pstEDIDData->ulBlockByteOffset);
            }

            pstEDIDData->ulLastWriteOffset = pstI2CSlaveInfo->ulCurrTransAddr;
            GFXVALSIM_DBG_MSG("Updated ulLastWriteOffset to %lu and set bIsIndexWrite", pstEDIDData->ulLastWriteOffset);
        }
        else
        {

            // We have stored EDID in such a way that each block has 256 bytes data corresponding to a seg ptr value
            // So the byte offset from where to start reading and read length should not go beyond the block
            if ((pstEDIDData->ulBlockByteOffset + pstI2CSlaveInfo->ulCurrentSlaveOffset + pstI2CSlaveInfo->ulCurrTransLen) > 2 * SIZE_EDID_BLOCK)
            {
                GFXVALSIM_DBG_MSG("ERROR: Calculated offset exceeding 256 bytes of data. Exiting without filling data");
                break;
            }

            pucEDIDBlock = pstEDIDData->pucEDIDBlocks[pstEDIDData->ulLastSegPtrVal];

            memcpy_s(pstI2CSlaveInfo->pucSlaveIntermediateDataBuff, pstI2CSlaveInfo->ulCurrTransLen,
                     (pucEDIDBlock + pstEDIDData->ulBlockByteOffset + pstI2CSlaveInfo->ulCurrentSlaveOffset), pstI2CSlaveInfo->ulCurrTransLen);
        }

        bRet = TRUE;

    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}

BOOLEAN I2CSLAVES_DDCEDIDUpdateRoutine(PI2C_SLAVE_INFO pstI2CSlaveInfo, PUCHAR pucEDIDBuff, ULONG ulEdidSize)
{
    BOOLEAN                 bRet                 = TRUE;
    PUCHAR *                ppucTemp256ByteBlock = NULL;
    PEDID_HOUSEKEEPING_DATA pstEDIDData          = NULL;
    PPORTINGLAYER_OBJ       pstPortingObj        = GetPortingObj();

    GFXVALSIM_FUNC_ENTRY();
    do
    {
        if (!(pstI2CSlaveInfo && pucEDIDBuff && ulEdidSize))
        {
            bRet = FALSE;
            break;
        }

        // Expect EDID size to be an integral multiple of SIZE_EDID_BLOCK
        if (ulEdidSize % SIZE_EDID_BLOCK)
        {
            bRet = FALSE;
            break;
        }

        pstEDIDData = (PEDID_HOUSEKEEPING_DATA)pstI2CSlaveInfo->pvI2CSlavePvtData;

        // Check if EDID was already initialized and free the blocks if that was the case
        if (pstEDIDData)
        {
            while (pstEDIDData->ulNumEdidBlocks)
            {
                if (pstEDIDData->pucEDIDBlocks[pstEDIDData->ulNumEdidBlocks])
                {
                    pstPortingObj->pfnFreeMem(pstEDIDData->pucEDIDBlocks[pstEDIDData->ulNumEdidBlocks]);
                }

                pstEDIDData->ulNumEdidBlocks--;
            }

            memset(pstEDIDData, 0, sizeof(EDID_HOUSEKEEPING_DATA));
        }
        else
        {
            pstEDIDData = pstPortingObj->pfnAllocateMem(sizeof(EDID_HOUSEKEEPING_DATA), TRUE);
        }

        // We have decided to keep EDID in blocks of 256 bytes to simply the logic of sending EDID simple when Gfx asks for it
        // via I2C-Aux or Remote I2C sideband Message

        while (ulEdidSize / (2 * SIZE_EDID_BLOCK))
        {
            ppucTemp256ByteBlock  = &pstEDIDData->pucEDIDBlocks[pstEDIDData->ulNumEdidBlocks];
            *ppucTemp256ByteBlock = pstPortingObj->pfnAllocateMem((2 * SIZE_EDID_BLOCK), TRUE);

            if (*ppucTemp256ByteBlock == NULL)
            {
                bRet = FALSE;
                break;
            }

            memcpy_s(*ppucTemp256ByteBlock, 2 * SIZE_EDID_BLOCK, pucEDIDBuff, 2 * SIZE_EDID_BLOCK);
            pucEDIDBuff = pucEDIDBuff + 2 * SIZE_EDID_BLOCK;
            ulEdidSize  = ulEdidSize - 2 * SIZE_EDID_BLOCK;
            pstEDIDData->ulNumEdidBlocks++;
        }

        // Now copy the last 128 bytes block if left or if EDID has only 128bytes
        if (ulEdidSize / SIZE_EDID_BLOCK)
        {
            ppucTemp256ByteBlock  = &pstEDIDData->pucEDIDBlocks[pstEDIDData->ulNumEdidBlocks];
            *ppucTemp256ByteBlock = pstPortingObj->pfnAllocateMem((2 * SIZE_EDID_BLOCK), TRUE);
            memcpy_s(*ppucTemp256ByteBlock, SIZE_EDID_BLOCK, pucEDIDBuff, SIZE_EDID_BLOCK);
            pstEDIDData->ulNumEdidBlocks++;
        }

        pstI2CSlaveInfo->pvI2CSlavePvtData = (PVOID)pstEDIDData;

    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}

BOOLEAN I2CSLAVES_DDCEDIDCleanUpRoutine(PI2C_SLAVE_INFO pstI2CSlaveInfo)
{
    BOOLEAN                 bRet          = TRUE;
    ULONG                   ulCount       = 0;
    PEDID_HOUSEKEEPING_DATA pstEDIDData   = (PEDID_HOUSEKEEPING_DATA)pstI2CSlaveInfo->pvI2CSlavePvtData;
    PPORTINGLAYER_OBJ       pstPortingObj = GetPortingObj();

    GFXVALSIM_FUNC_ENTRY();

    do
    {
        if (pstI2CSlaveInfo == NULL)
        {
            break;
        }

        if (pstI2CSlaveInfo->pucSlaveIntermediateDataBuff)
        {
            pstPortingObj->pfnFreeMem(pstI2CSlaveInfo->pucSlaveIntermediateDataBuff);
        }

        if (pstEDIDData)
        {
            for (ulCount = 0; ulCount < pstEDIDData->ulNumEdidBlocks; ulCount++)
            {
                if (pstEDIDData->pucEDIDBlocks[ulCount])
                {
                    pstPortingObj->pfnFreeMem(pstEDIDData->pucEDIDBlocks[ulCount]);
                }
            }

            pstPortingObj->pfnFreeMem(pstEDIDData);
            pstI2CSlaveInfo->pvI2CSlavePvtData = NULL;
        }

    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}