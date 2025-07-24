/*------------------------------------------------------------------------------------------------*
 *
 * @file     DisplayPort.cpp
 * @brief    This file contains Implementation of DisplayPort APIs - IsCollageEnabled, GetCollageInfo,
 *           ApplyCollage, GetSupportedConfig, CollageGetSupportedModes, VerifyMstTopology
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#include "SdkSharedHeader.h"
#include "CuiSdk.h"
extern "C"
{
#include "GfxValSim.h"
}

extern ICUIExternal8 *pCUIExternal;
struct DPMSTTopology  currentTopology[MAX_PATH];
GFX_ADAPTER_INFO      gfxAdapterInfo; // Multiadapter WA, Cache default adapter.

/**---------------------------------------------------------------------------------------------------------*
 * @brief           IsCollageEnabled (Exposed API)
 * Description      This function has implementation to check if Collage is Enabled or Disabled
 * @param[InOut]    pCollageStatus (Pointer to _IGFX_COLLAGE_STATUS structure)
 * @return BOOLEAN  Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN IsCollageEnabled(_Inout_ IGFX_COLLAGE_STATUS *pCollageStatus)
{
    DWORD errorCode = 0;

    do
    {
        NULL_PTR_CHECK(pCUIExternal);
        NULL_PTR_CHECK(pCollageStatus);

        VERIFY_STATUS(pCUIExternal->GetDeviceData(IGFX_GET_SET_COLLAGE_STATUS_GUID, sizeof(IGFX_COLLAGE_STATUS), (BYTE *)pCollageStatus, &errorCode));
        VERIFY_STATUS(errorCode);
    } while (FALSE);

    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           GetCollageInfo (Exposed API)
 * Description      This function has implementation to check if Collage is supported or not in the platform
 * @param[Out]      pCollageStatus (Pointer to _IGFX_COLLAGE_STATUS structure)
 * @return BOOLEAN  Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN GetCollageInfo(_Out_ IGFX_COLLAGE_STATUS *pCollageStatus)
{
    DWORD errorCode = 0;

    do
    {
        NULL_PTR_CHECK(pCUIExternal);
        NULL_PTR_CHECK(pCollageStatus);

        VERIFY_STATUS(pCUIExternal->GetDeviceData(IGFX_GET_SET_COLLAGE_STATUS_GUID, sizeof(IGFX_COLLAGE_STATUS), (BYTE *)pCollageStatus, &errorCode));
        VERIFY_STATUS(errorCode);
    } while (FALSE);

    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           ApplyCollage (Exposed API)
 * Description      This function has implementation to set the Collage Mode for the selected Displays
 * @param[In]       pSystemConfigData (Pointer to _IGFX_SYSTEM_CONFIG_DATA_N_VIEW structure)
 * @return BOOLEAN  Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN ApplyCollage(_In_ IGFX_SYSTEM_CONFIG_DATA_N_VIEW *pSystemConfigData)
{
    DWORD errorCode = 0;

    do
    {
        NULL_PTR_CHECK(pCUIExternal);
        NULL_PTR_CHECK(pSystemConfigData);

        VERIFY_STATUS(pCUIExternal->SetDeviceData(IGFX_GET_SET_N_VIEW_CONFIG_GUID, pSystemConfigData->size, (BYTE *)pSystemConfigData, &errorCode));
        VERIFY_STATUS(errorCode);
    } while (FALSE);

    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           GetSupportedConfig (Exposed API)
 * Description      This function has implementation to get all the supported Config
 *                 For Example: SD,DD CLone, Tri Clone, Tri ED, Dual Hor Collage, etc
 * @param[In]       pTestConfigEx (Pointer to _IGFX_TEST_CONFIG_EX structure)
 * @return BOOLEAN  Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN GetSupportedConfig(_In_ IGFX_TEST_CONFIG_EX *pTestConfigEx)
{
    DWORD errorCode = 0;

    do
    {
        NULL_PTR_CHECK(pCUIExternal);
        NULL_PTR_CHECK(pTestConfigEx);

        VERIFY_STATUS(pCUIExternal->GetDeviceData(IGFX_SUPPORTED_CONFIGURATIONS_EX, sizeof(IGFX_TEST_CONFIG_EX), (BYTE *)pTestConfigEx, &errorCode));
        VERIFY_STATUS(errorCode);
    } while (FALSE);
    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           CollageGetSupportedModes (Exposed API)
 * Description      This function has implementation to get all the supported modes for the applied collage config
 * @param[In]       size (DWORD containing the size to be allocated)
 * @param[InOut]    pVideoModeList (Pointer to _IGFX_VIDEO_MODE_LIST_EX structure)
 * @return BOOLEAN  Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN CollageGetSupportedModes(_In_ DWORD size, _Inout_ IGFX_VIDEO_MODE_LIST_EX *pVideoModeList)
{
    DWORD errorCode = 0;

    NULL_PTR_CHECK(pCUIExternal);
    NULL_PTR_CHECK(pVideoModeList);

    if (pVideoModeList->vmlNumModes == 0)
    {
        pVideoModeList->flags = IGFX_VIDEO_MODE_LIST_SIZE_ONLY;

        VERIFY_STATUS(pCUIExternal->GetDeviceData(IGFX_GET_VIDEO_MODE_LIST_GUID, size, (BYTE *)&pVideoModeList, &errorCode));
        VERIFY_STATUS(errorCode);
    }
    else
    {
        pVideoModeList->flags = 0;

        VERIFY_STATUS(pCUIExternal->GetDeviceData(IGFX_GET_VIDEO_MODE_LIST_GUID, size, (BYTE *)&pVideoModeList, &errorCode));
        VERIFY_STATUS(errorCode);
    }

    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           VerifyMstTopology (Exposed API)
 * Description      This function has implementation to verify whether expected and applied MST topologies are identical or not
 * @param[In]       portNum (Port number from where topology should be verified)
 * @return BOOLEAN  Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN VerifyMstTopology(_In_ ULONG portNum)
{
    BOOLEAN branchesMatching        = TRUE;
    BOOLEAN displaysMatching        = TRUE;
    BOOLEAN portFound               = FALSE;
    BOOLEAN status                  = FALSE;
    HRESULT hr                      = NULL;
    UINT    totalNoOfNodes          = 0;
    UINT    branchIteration         = 0;
    UINT    displayIteration        = 0;
    UINT    nodeIndex               = 0;
    LONG    displayIndex            = 0;
    LONG    branchIndex             = 0;
    ULONG   branchIndexVerification = 0;
    LONG    lowerBound              = 0L;
    LONG    upperBound              = 0L;
    DWORD   errorCode               = 0;
    DWORD   bytesReturned           = 0;

    SAFEARRAY *              pBranchDetails       = NULL;
    SAFEARRAY *              pDisplayDetails      = NULL;
    IGFX_DP_TOPOLOGY_BRANCH *pBranches            = NULL;
    IGFX_DP_DISPLAY *        pDisplays            = NULL;
    DPDeviceContext          dpDeviceContext      = { 0 };
    IGFX_DP_TOPOLOGY_PORT    dpTopologyPort       = { 0 };
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer   = { 0 };
    BRANCHDISP_RAD_ARRAY *   pAppliedTopologyData = (BRANCHDISP_RAD_ARRAY *)malloc(sizeof(BRANCHDISP_RAD_ARRAY));

    do
    {
        NULL_PTR_CHECK(pCUIExternal);

        /* Call CUISDK API GetValidDPTopologyPorts to retrieve list of valid DP1.2 ports */
        VERIFY_STATUS(pCUIExternal->GetValidDPTopologyPorts(&dpTopologyPort, &errorCode));
        VERIFY_STATUS(errorCode);

        /* If DP1.2 ports not detected then break and exit */
        if (dpTopologyPort.numPorts <= 0)
        {
            status = FALSE;
            ERROR_LOG("DP1.2/MST ports not detected!!!... Exiting.");
            break;
        }

        INFO_LOG("%d DP1.2/MST ports detected", dpTopologyPort.numPorts);

        /* Check whether user/script passed Port present in the list of topologies or not */
        for (nodeIndex = 0; nodeIndex < dpTopologyPort.numPorts; nodeIndex++)
        {
            if (portNum == (dpTopologyPort.PortList[nodeIndex] - 1))
            {
                portFound = TRUE;
                break;
            }
        }

        if (FALSE == portFound)
        {
            /* User/script passed Port not present in the list of topologies */
            ERROR_LOG("User/Script passed Port %d not present in the list of topologies", portNum);

            status = FALSE;
            break;
        }

        /************************* Parsing - Extract branch and display details for the script requesting Port  *************************/

        /* Call CUISDK API GetTopologyDetailsForDisplayPort to retrieve branch and displays details */
        VERIFY_STATUS(pCUIExternal->GetTopologyDetailsForDisplayPort(dpTopologyPort.PortList[nodeIndex], &pBranchDetails, &pDisplayDetails, &errorCode));
        VERIFY_STATUS(errorCode);

        SafeArrayGetLBound(pBranchDetails, 1, &lowerBound);
        SafeArrayGetUBound(pBranchDetails, 1, &upperBound);
        LONG noOfBranches = upperBound - lowerBound + 1;

        SafeArrayGetLBound(pDisplayDetails, 1, &lowerBound);
        SafeArrayGetUBound(pDisplayDetails, 1, &upperBound);
        LONG noOfDisplays = upperBound - lowerBound + 1;

        /* Branch details as follows */
        if (NULL == pBranchDetails)
        {
            ERROR_LOG("NULL Pointer, Exiting !!!");
            status = FALSE;
        }
        else
        {
            hr = ::SafeArrayAccessData(pBranchDetails, reinterpret_cast<PVOID *>(&pBranches));

            if (S_OK == hr)
            {
                /* Run through branch list and assign branch, parent and temp ids to structure DPMSTTopology */
                for (branchIndex = 0; branchIndex < noOfBranches; branchIndex++)
                {
                    INFO_LOG("Branch %d's Parent index: %d", branchIndex + 1, pBranches[branchIndex].ulParentBranchIndex);

                    strcpy_s(currentTopology[branchIndex].node, sizeof("Branch"), "Branch");
                    currentTopology[branchIndex].parentId = pBranches[branchIndex].ulParentBranchIndex;

                    /* WA: Root node's parent id is hard-coded to 0xffffffff in the XML file but where as parent id returned by
                        CUISDK API is 0xffff. To align parent ids of both XML and CUISDK, we are replacing root node's parent id
                        returned by CUISDK to 0xffffffff from 0xffff */
                    if (currentTopology[branchIndex].parentId == 0xffff)
                        currentTopology[branchIndex].parentId = 0xffffffff;

                    totalNoOfNodes++;
                }

                hr = ::SafeArrayUnaccessData(pBranchDetails);
                if (S_OK != hr)
                {
                    ERROR_LOG("Invalidation of pointer pBranchDetails failed");
                }
            }
            else
            {
                ERROR_LOG("Failed to retrieve pointer pBranchDetails!! Exiting.");
            }
        }

        if (NULL == pDisplayDetails)
        {
            ERROR_LOG("NULL Pointer, Exiting !!!");
            status = FALSE;
        }
        else
        {
            hr = ::SafeArrayAccessData(pDisplayDetails, reinterpret_cast<PVOID *>(&pDisplays));

            if (S_OK == hr)
            {
                /* Run through display list and assign branch, parent and temp ids to structure DPMSTTopology
                    Starting index to noOfBranches since we want to store display details after branch details in same array */
                for (branchIndex = noOfBranches; branchIndex < (noOfDisplays + noOfBranches); branchIndex++)
                {
                    INFO_LOG("Display %d's Parent index: %d", branchIndex + 1, pDisplays[displayIndex].ulParentBranchIndex);

                    strcpy_s(currentTopology[branchIndex].node, sizeof("Display"), "Display");
                    currentTopology[branchIndex].parentId = pDisplays[displayIndex++].ulParentBranchIndex;

                    totalNoOfNodes++;
                }

                hr = ::SafeArrayUnaccessData(pDisplayDetails);
                if (S_OK != hr)
                {
                    ERROR_LOG("Invalidation of pointer pDisplayDetails failed");
                }
            }
            else
            {
                ERROR_LOG("Failed to retrieve pointer pDisplayDetails!! Exiting.");
            }
        }

        if (NULL != pBranchDetails)
        {
            /* Cleanup resources */
            SafeArrayDestroy(pBranchDetails);
            pBranchDetails = NULL;
            pBranches      = NULL;
        }

        if (NULL != pDisplayDetails)
        {
            /* Cleanup resources */
            SafeArrayDestroy(pDisplayDetails);
            pDisplayDetails = NULL;
            pDisplays       = NULL;
        }

        if (FALSE == status)
            break;

        NULL_PTR_CHECK(pAppliedTopologyData);

        dpDeviceContext.gfxValSimHandle = GetGfxValSimHandle();

        /* Check for GfxValSimDriver handler */
        NULL_PTR_CHECK(dpDeviceContext.gfxValSimHandle);

        devIoControlBuffer.pInBuffer     = &portNum;
        devIoControlBuffer.inBufferSize  = sizeof(ULONG);
        devIoControlBuffer.pOutBuffer    = pAppliedTopologyData;
        devIoControlBuffer.outBufferSize = sizeof(BRANCHDISP_RAD_ARRAY);
        devIoControlBuffer.pAdapterInfo  = &gfxAdapterInfo; /* Get adapter info from cached data */

        /* Send DeviceIoCtl for getting the RAD information */
        errorCode =
        DeviceIoControl(dpDeviceContext.gfxValSimHandle, (DWORD)IOCTL_GET_MST_RAD, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, NULL, &bytesReturned, NULL);

        if (FALSE == errorCode)
        {
            ERROR_LOG("Error: Get RAD IOCTL failed");
            status = FALSE;
            break;
        }

        /*************************** Verification of Expected and Applied topologies are identical or not *****************************/

        /* TODO: Currently we are verifying total number of nodes count, level/parent-id of each corresponding nodes (Branch/Display) in
           Expected/Applied are identical or not. We need to find solution to compare even whether Display manufacture/model are same or not */

        /* Fail if total number of nodes (Branches + Displays) in expected and applied topologies are different */
        if (totalNoOfNodes != (pAppliedTopologyData->ulNumBranches + pAppliedTopologyData->ulNumDisplays))
        {
            status = FALSE;
            ERROR_LOG("Expected and Applied topologies are different.");
            break;
        }

        /* Compare whether each branch in expected and applied topologies which are at same level in the topology tree. We need to fail
           if corresponding branch nodes are not at same level eventhough if both topologies contains same number of branch nodes.
           for (uiBranchindex = 0; uiBranchindex < stDPDevContext.numberOfBranches; uiBranchindex++) */
        for (branchIteration = 0; branchIteration < pAppliedTopologyData->ulNumBranches; branchIteration++)
        {
            for (branchIndexVerification = 0; branchIndexVerification < pAppliedTopologyData->ulNumBranches; branchIndexVerification++)
            {
                if (currentTopology[branchIndexVerification].isVisited == TRUE)
                {
                    continue;
                }

                if (pAppliedTopologyData->stBranchRADInfo[branchIteration].ulParentBranchIndex == currentTopology[branchIndexVerification].parentId)
                {
                    currentTopology[branchIndexVerification].isVisited = TRUE;
                    /* Do nothing. Just continue with next branch in the topology */
                    break;
                }
            }
        }

        for (branchIndexVerification = 0; branchIndexVerification < pAppliedTopologyData->ulNumBranches; branchIndexVerification++)
        {
            if (FALSE == currentTopology[branchIndexVerification].isVisited)
            {
                /* We should not hit here. If we hit, means Parent ids of branch nodes are different for
                   branches at same level in both expected and applied topologies */
                status = FALSE;
                /* Set the flag bBranchesMatching to FALSE indicating number of branches and their
                   corresponding are mis-matching */
                branchesMatching = FALSE;
                ERROR_LOG("Mismatch occured in branch count");
                break;
            }
        }

        /* No point in continuing with Displays comparision if Branches comparision failed! */
        if (FALSE == branchesMatching)
        {
            ERROR_LOG("Failed to compare branches");
            break;
        }

        /* Compare whether each display in expected and applied topologies which are at same level in the topology tree. We need to fail
           if corresponding display nodes are not at same level eventhough if both topologies contains same number of display nodes.
           for (int displayIndex = 0; displayIndex < dpDeviceContext.numberOfDisplays; displayIndex++) */
        for (displayIteration = 0; displayIteration < pAppliedTopologyData->ulNumDisplays; displayIteration++)
        {
            for (ULONG displayIndex = 0; displayIndex < pAppliedTopologyData->ulNumDisplays; displayIndex++)
            {
                if (currentTopology[branchIteration + displayIndex].isVisited == TRUE)
                {
                    continue;
                }

                if (pAppliedTopologyData->stDisplayRADInfo[displayIteration].ulParentBranchIndex == (currentTopology[branchIteration + displayIndex].parentId))
                {
                    currentTopology[branchIteration + displayIndex].isVisited = TRUE;
                    /* Do nothing. Just continue with next display in the topology */
                    break;
                }
            }
        }

        for (ULONG displayIndex = 0; displayIndex < pAppliedTopologyData->ulNumDisplays; displayIndex++)
        {
            if (FALSE == currentTopology[displayIndex].isVisited)
            {
                /* We should not hit here. If we hit, means Parent ids of display nodes are different for displays at same level in both
                   expected and applied topologies */
                status = FALSE;

                /* Set the flag bBranchesMatching to FALSE indicating number of displays and their
                   corresponding are mis-matching */
                displaysMatching = FALSE;
                ERROR_LOG("Mismatch occured in display count");
                break;
            }
        }

        /* Return TRUE if topologies are matching */
        if (branchesMatching && displaysMatching)
        {
            status = TRUE;
        }
    } while (FALSE);

    free(pAppliedTopologyData);
    return status;
}
