

#include "../HeaderFiles/DisplayStateBuffer.h"
#include "../HeaderFiles/CommonDetails.h"

CDLL_EXPORT BOOLEAN VerifyDSB(PGVSTUB_DSB_BUFFER_ARGS pDSBBufferArgs)
{
    BOOLEAN                  status = FALSE;
    GVSTUB_FEATURE_INFO_ARGS ValStubFeatureInfo;
    DFT_MMIO_ACCESS          MmioAccessArgs = { 0 };
    PGVSTUB_DSB_BUFFER_ARGS  pGVStubDSBArgs = &(ValStubFeatureInfo.stDisplayFeatureArgs.stDSBBufferArgs);
    do
    {
        if (NULL == pDSBBufferArgs)
            break;

        InitDIVA();
        if (NULL == hDivaAccess)
            break;

        memset(pGVStubDSBArgs, 0, sizeof(GVSTUB_DSB_BUFFER_ARGS));
        CopyMemory(pGVStubDSBArgs, pDSBBufferArgs, sizeof(GVSTUB_DSB_BUFFER_ARGS));

        PGVSTUB_META_DATA pDisplayFeatureMetaData = &(ValStubFeatureInfo.stDisplayFeatureArgs.stDisplayFeatureMetaData);
        pDisplayFeatureMetaData->ulSize           = sizeof(GVSTUB_META_DATA) + sizeof(GVSTUB_DSB_BUFFER_ARGS);
        pDisplayFeatureMetaData->ulVersion        = GVSTUB_DISPLAY_FEATURE_ACCESS_VERSION;
        pDisplayFeatureMetaData->ulServiceType    = GVSTUB_TRIGGER_DSB;
        pDisplayFeatureMetaData->ulStatus         = GVSTUB_DISPLAY_FEATURE_STATUS_FAILURE;

        PGVSTUB_META_DATA pValStubMetaData = &(ValStubFeatureInfo.stFeatureMetaData);
        pValStubMetaData->ulSize           = sizeof(GVSTUB_META_DATA) + pDisplayFeatureMetaData->ulSize;
        pValStubMetaData->ulVersion        = GVSTUB_FEATURE_INFO_VERSION;
        pValStubMetaData->ulServiceType    = GVSTUB_FEATURE_DISPLAY;
        pValStubMetaData->ulStatus         = GVSTUB_FEATURE_FAILURE;

        // Make an IOCTL call
        DWORD bytesReturned = 0;
        if (DeviceIoControl(hDivaAccess,                               // Device handle
                            (DWORD)DIVA_IOCTL_GfxValStubCommunication, // IOCTL code
                            &(ValStubFeatureInfo),                     // Input buffer
                            pValStubMetaData->ulSize,                  // Input buffer size
                            &(ValStubFeatureInfo),                     // Output buffer
                            pValStubMetaData->ulSize,                  // Output buffer size
                            &bytesReturned,                            // Variable to receive size of data stored in output buffer
                            NULL                                       // Ignored
                            ) == FALSE)
        {
            TRACE_LOG(DEBUG_LOGS, "Ioctl call failed for Trigger DSB execution");
            break;
        }

        if ((GVSTUB_DISPLAY_FEATURE_STATUS_SUCCESS != pDisplayFeatureMetaData->ulStatus) || (GVSTUB_FEATURE_SUCCESS != pValStubMetaData->ulStatus))
        {
            TRACE_LOG(DEBUG_LOGS, "Trigger DSB through DFT failed from Gfx Driver");
            break;
        }
        /* Verify MMIO against DSB programmed value*/
        MmioAccessArgs.accessType = DFT_MMIO_READ;
        MmioAccessArgs.offset     = pDSBBufferArgs->pOffsetDataPair[pDSBBufferArgs->DataCount - 1].Offset;
        MmioAccessArgs.value      = 0;
        if (TRUE == DftMMIOAccess(&MmioAccessArgs))
        {
            if (MmioAccessArgs.value == pDSBBufferArgs->pOffsetDataPair[pDSBBufferArgs->DataCount - 1].Data)
                status = TRUE;
            else
                status = FALSE;
            TRACE_LOG(DEBUG_LOGS, "MMIO write through DSB with offset {%lu} expected value %lu actual value %lu", MmioAccessArgs.offset,
                      pDSBBufferArgs->pOffsetDataPair[pDSBBufferArgs->DataCount - 1].Data, MmioAccessArgs.value);
        }
        else
            status = FALSE;
    } while (FALSE);

    return status;
}
