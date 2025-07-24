#include "DisplayPort.h"
#include "SimDrvParser.h"

extern "C"
{
#include "..\GfxValSimulator\GfxValSimLibrary\GfxValSim.h"
}

char LIBRARY_NAME[] = "Displayport.dll";

#import "..\\..\\..\\..\\TestStore\\CommonBin\\IgfxExt.exe" named_guids
using namespace IGFXEXTLib;
ICUIExternal8Ptr m_pCUIExternal = NULL;

#ifndef CUISDK_COMMON_H
#define CUISDK_COMMON_H

#define IGFX_SUCCESS 0x0000
#define IGFX_FAILURE 0x0025

#endif

GUID IGFX_GET_SET_COLLAGE_STATUS_GUID = { 0x61a8470b, 0x918e, 0x48fb, { 0xb6, 0x5b, 0xa6, 0x84, 0x66, 0x78, 0xc2, 0xf1 } };

extern struct DPMSTTopology BranchDetails[MAX_PATH], DisplayDetails[MAX_PATH], CurTopology[MAX_PATH];
GFX_ADAPTER_INFO            GFX_0_ADAPTER_INFO; // Multiadapter WA, Cache default adapter.

/**
 * @brief        Exposed API for initializing DP AUX objects
 * @params       Adapter info
 * @params       Adapter info size
 * @param[in]    pDPInfo : pointer for initializing the DP SST/MST Aux objects
 * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
BOOL DisplayportInit(PGFX_ADAPTER_INFO pAdapterInfo, UINT gfxAdapterInfoSize, PDP_INIT_INFO pDPInfo)
{
    BOOL                     bStatus            = TRUE;
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    do
    {
        stDPDevContext.hGfxValSimHandle = GetGfxValSimHandle();

        /* Check for GfxValSimDriver handler */
        if (stDPDevContext.hGfxValSimHandle == NULL)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Gfx Val Simulation driver not initialized!!!... Exiting...");
            bStatus = FALSE;
            break;
        }
        GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize);

        /* START - Display port Multiadapter WA need to fix later */
        /* Validate whether adapter type is only gfx_0 */
        if (0 == wcscmp(pAdapterInfo->gfxIndex, GFX_0_ADPTER_INDEX))
        {
            /* cache adapter detail for future use */
            memcpy_s(&GFX_0_ADAPTER_INFO, sizeof(GFX_ADAPTER_INFO), pAdapterInfo, sizeof(GFX_ADAPTER_INFO));
        }
        else
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Functionality supports only internal adapter (gfx_0) !!!... Exiting...");
            bStatus = FALSE;
            break;
        }

        /* END - Display port Multiadapter WA need to fix later */

        /* Check for PDP_INIT_INFO pointer for NULL value */
        if (pDPInfo == NULL)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: DP Init Info Object is NULL!!!... Exiting...");
            bStatus = FALSE;
            break;
        }

        devIoControlBuffer.pInBuffer    = pDPInfo;
        devIoControlBuffer.inBufferSize = sizeof(DP_INIT_INFO);
        devIoControlBuffer.pAdapterInfo = pAdapterInfo;

        /* Send DeviceIoCtl for port objects. DP GfxValSim driver doesn't expect/return any argument */
        dwStatus =
        DeviceIoControl(stDPDevContext.hGfxValSimHandle, (DWORD)IOCTL_INIT_DP_TOPOLOGY, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, NULL, &BytesReturned, NULL);

        if (OPERATION_FAILED == dwStatus)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: IoCTL Failed while initialization DP object with error code: 0x%u", GetLastError());
            bStatus = FALSE;
            break;
        }

    } while (FALSE);

    return bStatus;
}

/**
 * @brief        Exposed API to Parse XML Files and send topology/display details to GFX Simulation driver
 * @param[in]    uiPortNum		: Port Number of target
 * @param[in]	eTopologyType	: Topology Type ie SST/MST
 * @param[in]    xmlFile			: File that contains SST/MST data
 * @param[in]	bIsLowPower		: Plug/Unplug status in low power mode
 * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
BOOL ParseNSendTopology(UINT uiPortNum, DP_TOPOLOGY_TYPE eTopologyType, CHAR *pchXmlFile, BOOL bIsLowPower)
{
    BOOL                     bStatus            = TRUE;
    BOOL                     bSSTRetStatus      = FALSE;
    DWORD                    BytesReturned      = 0;
    DWORD                    dwStatus           = 0;
    PBRANCHDISP_DATA_ARRAY   pBranchDispArray   = NULL;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    rapidxml::file<> topologyXMLFile(pchXmlFile);

    do
    {
        stDPDevContext.hGfxValSimHandle = GetGfxValSimHandle();

        /* Check for GfxValSimDriver handler */
        if (stDPDevContext.hGfxValSimHandle == NULL)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Gfx Val Simulation driver not initialized!!!... Exiting...");
            bStatus = FALSE;
            break;
        }

        /* Memory Allocation for MST Topology data */
        pBranchDispArray = (PBRANCHDISP_DATA_ARRAY)malloc(sizeof(BRANCHDISP_DATA_ARRAY));
        if (pBranchDispArray == NULL)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Failed to allocate memory for MST Topology data!!!... Exiting...");
            bStatus = FALSE;
            break;
        }

        memset(pBranchDispArray, 0, sizeof(BRANCHDISP_DATA_ARRAY));
        devIoControlBuffer.pAdapterInfo = &GFX_0_ADAPTER_INFO; /* Get adapter info from cached data */

        /* Initialize DP GFX Simulation driver based on DP Topology type and parse the data from respective XML's */
        if (eTopologyType == eDPSST)
        {
            /* Function call to parse DP SST EDID and DPCD details here */
            bSSTRetStatus = SIMDRVHELPERFUNCS_ParseNSendSSTInfoToSimDrv(pchXmlFile, uiPortNum, bIsLowPower);
            if (bSSTRetStatus == FALSE)
            {
                INFO_LOG("[DisplayPort.DLL]: Error: SST Data Parsing Failed!!!... Exiting...");
                bStatus = FALSE;
                break;
            }
        }
        else if (eTopologyType == eDPMST)
        {
            /* Function call to parse EDID, DPCD and Topology details here */
            if (SIMDRVHELPERFUNCS_ParseNSendMSTInfoToSimDrv(pchXmlFile, uiPortNum, pBranchDispArray, bIsLowPower) == FALSE)
            {
                INFO_LOG("[DisplayPort.DLL]: Error: MST Data Parsing Failed!!!... Exiting...");
                bStatus = FALSE;
                break;
            }

            if (bIsLowPower == TRUE)
            {
                devIoControlBuffer.pInBuffer    = pBranchDispArray;
                devIoControlBuffer.inBufferSize = sizeof(BRANCHDISP_DATA_ARRAY);
                /* Send topology data to Gfx Simulation driver via DeviceIOCLs in low power mode */
                dwStatus = DeviceIoControl(stDPDevContext.hGfxValSimHandle, (DWORD)IOCTL_SET_GFXS3S4_BRANCHDISP_DATA, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL,
                                           NULL, &BytesReturned, NULL);

                if (OPERATION_FAILED == dwStatus)
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: Failed to send topology data to Gfx Sim driver in low power mode with error code: 0x%u", GetLastError());
                    bStatus = FALSE;
                    break;
                }
            }
            else
            {
                devIoControlBuffer.pInBuffer    = pBranchDispArray;
                devIoControlBuffer.inBufferSize = sizeof(BRANCHDISP_DATA_ARRAY);
                /* Send topology data to Gfx Simulation driver via DeviceIOCLs */
                dwStatus = DeviceIoControl(stDPDevContext.hGfxValSimHandle, (DWORD)IOCTL_SET_BRANCHDISP_DATA, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, NULL,
                                           &BytesReturned, NULL);

                if (OPERATION_FAILED == dwStatus)
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: Failed to send topology data to Gfx Sim driver with error code: 0x%u", GetLastError());
                    bStatus = FALSE;
                    break;
                }
            }
        }
        else
        {
            INFO_LOG("[DisplayPort.DLL]: Error: TopologyType is invalid!!!... Exiting...");
            bStatus = FALSE;
            break;
        }

    } while (FALSE);

    /* Freeing pBranchDispArray at the end even if we see failure during IcCTL failure */
    if (pBranchDispArray != NULL)
    {
        free(pBranchDispArray);
    }

    return bStatus;
}

/**
 * @brief        Exposed API to Read DPCD Value
 * @param[in]    pDpcdData	  : pointer to structure GET_DPCD_ARGS contains port number and RAD
 * @param[in]    pOutputBuffer : buffer containing the register values
 * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
BOOL ReadDPCD(PGET_DPCD_ARGS pDpcdData, ULONG ulOutputBuffer[])
{
    BOOL                     bStatus            = TRUE;
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    do
    {
        stDPDevContext.hGfxValSimHandle = GetGfxValSimHandle();

        /* Check for GfxValSimDriver handler */
        if (stDPDevContext.hGfxValSimHandle == NULL)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Gfx Val Simulation driver not initialized!!!... Exiting...");
            return FALSE;
            break;
        }

        /* Check for pDpcdData pointer for NULL value */
        if (pDpcdData == NULL)
        {
            INFO_LOG("[DisplayPort.DLL]: Error : DPCD Data Object is NULL!!!... Exiting...");
            return FALSE;
            break;
        }

        devIoControlBuffer.pInBuffer     = pDpcdData;
        devIoControlBuffer.inBufferSize  = sizeof(GET_DPCD_ARGS);
        devIoControlBuffer.pOutBuffer    = ulOutputBuffer;
        devIoControlBuffer.outBufferSize = pDpcdData->ulReadLength;
        devIoControlBuffer.pAdapterInfo  = &GFX_0_ADAPTER_INFO; /* Get adapter info from cached data */

        /* Send DPCD read to Gfx Simulation driver via DeviceIOCLs  */
        dwStatus =
        DeviceIoControl(stDPDevContext.hGfxValSimHandle, (DWORD)IOCTL_READ_DPCD, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, NULL, &BytesReturned, NULL);

        if (OPERATION_FAILED == dwStatus)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: IoCTL Failed during Read DPCD call with error code: 0x%u", GetLastError());
            bStatus = FALSE;
            break;
        }

    } while (FALSE);

    return bStatus;
}

/**
* @brief        Exposed API to verify whether expected and applied MST topologies are identical or not
* @params       ulPortNum : Port number from where topology should be verified
* @return       UINT. Returns error code depending on the error. Error code could be SUCCESS, FAILURE, TOPOLOGIES_MATCHING,
                DISPLAYS_MISMATCH, BRANCHES_MISMATCH, TOPOLOGIES_MISMATCH or TOPOLOGY_NOT_PRESENT
*/
UINT VerifyMSTTopology(ULONG ulPortNum)
{
    BOOL                     bBranchesMatching = TRUE;
    BOOL                     bDisplaysMatching = TRUE;
    BOOL                     bPortFound        = FALSE;
    UINT                     uiStatus          = GFXSIM_DISPLAY_FAILURE;
    UINT                     uiTotalNoOfNodes  = 0;
    UINT                     uiBranchIteration = 0, uiDisplayIteration = 0, uiNodeindex = 0;
    LONG                     lDisplayindex = 0, lBranchindex = 0;
    ULONG                    ulBranchindex_Verification = 0;
    HRESULT                  hr = NULL, hr_SA = NULL;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    do
    {
        if (m_pCUIExternal)
        {
            DWORD                 dwExtraErrorCode = IGFX_FAILURE;
            IGFX_DP_TOPOLOGY_PORT dpTopologyPort;

            /* Call CUISDK API GetValidDPTopologyPorts to retrieve list of valid DP1.2 ports */
            hr = m_pCUIExternal->GetValidDPTopologyPorts(&dpTopologyPort, &dwExtraErrorCode);

            if (SUCCEEDED(hr) && dwExtraErrorCode == IGFX_SUCCESS)
            {
                /* If DP1.2 ports not detected then break and exit */
                if (dpTopologyPort.numPorts <= 0)
                {
                    uiStatus = GFXSIM_DISPLAY_TOPOLOGY_NOT_PRESENT;
                    INFO_LOG("[Displayport.DLL]: DP1.2/MST ports not detected!!!... Exiting...");
                    break;
                }

                INFO_LOG("[Displayport.DLL]: %d DP1.2/MST ports detected", dpTopologyPort.numPorts);

                /* Check whether user/script passed Port present in the list of topologies or not */
                for (uiNodeindex = 0; uiNodeindex < dpTopologyPort.numPorts; uiNodeindex++)
                {
                    if (ulPortNum == (dpTopologyPort.PortList[uiNodeindex] - 1))
                    {
                        bPortFound = TRUE;
                        break;
                    }
                }

                if (FALSE == bPortFound)
                {
                    /* User/script passed Port not present in the list of topologies */
                    INFO_LOG("[Displayport.DLL]: User/Script passed Port %d not present in the list of topologies", ulPortNum);

                    uiStatus = GFXSIM_DISPLAY_TOPOLOGY_NOT_PRESENT;
                    break;
                }

                SAFEARRAY *              branchDetails  = NULL;
                SAFEARRAY *              displayDetails = NULL;
                IGFX_DP_TOPOLOGY_BRANCH *pBranches      = NULL;
                IGFX_DP_DISPLAY *        pDisplays      = NULL;
                LONG                     lowerBound, upperBound; // Get array bounds

                /************************* Parsing - Extract branch and display details for the script requesting Port  *************************/

                /* Call CUISDK API GetTopologyDetailsForDisplayPort to retrieve branch and displays details */
                hr = m_pCUIExternal->GetTopologyDetailsForDisplayPort(dpTopologyPort.PortList[uiNodeindex], &branchDetails, &displayDetails, &dwExtraErrorCode);

                if (SUCCEEDED(hr) && dwExtraErrorCode == IGFX_SUCCESS)
                {
                    SafeArrayGetLBound(branchDetails, 1, &lowerBound);
                    SafeArrayGetUBound(branchDetails, 1, &upperBound);
                    LONG noOfBranches = upperBound - lowerBound + 1;

                    SafeArrayGetLBound(displayDetails, 1, &lowerBound);
                    SafeArrayGetUBound(displayDetails, 1, &upperBound);
                    LONG noOfDisplays = upperBound - lowerBound + 1;

                    INFO_LOG("[Displayport.DLL]: Below are the details of Branches and Displays connected to Port %s (Id: %d)", GET_PORT_STRING[ulPortNum], ulPortNum);

                    /* Branch details as follows */
                    if (NULL != branchDetails)
                    {
                        hr_SA = ::SafeArrayAccessData(branchDetails, reinterpret_cast<PVOID *>(&pBranches));

                        if (SUCCEEDED(hr_SA))
                        {
                            /* Run through branch list and assign branch, parent and temp ids to structure DPMSTTopology */
                            for (lBranchindex = 0; lBranchindex < noOfBranches; lBranchindex++)
                            {
                                INFO_LOG("[Displayport.DLL]: Branch %d's Parent index: %d", lBranchindex + 1, pBranches[lBranchindex].ulParentBranchIndex);

                                strcpy(CurTopology[lBranchindex].chNode, "Branch");
                                CurTopology[lBranchindex].uiParentId = pBranches[lBranchindex].ulParentBranchIndex;

                                /* WA: Root node's parent id is hard-coded to 0xffffffff in the XML file but where as parent id returned by
                                    CUISDK API is 0xffff. To align parent ids of both XML and CUISDK, we are replacing root node's parent id
                                    returned by CUISDK to 0xffffffff from 0xffff */
                                if (CurTopology[lBranchindex].uiParentId == 0xffff)
                                    CurTopology[lBranchindex].uiParentId = 0xffffffff;

                                uiTotalNoOfNodes++;
                            }

                            hr_SA = ::SafeArrayUnaccessData(branchDetails);
                        }
                    }
                    else
                    {
                        INFO_LOG("[Displayport.DLL]: BranchDetails safe array is NULL");
                    }

                    /* Display details as follows */
                    if (NULL != displayDetails)
                    {
                        hr_SA = ::SafeArrayAccessData(displayDetails, reinterpret_cast<PVOID *>(&pDisplays));
                        if (SUCCEEDED(hr_SA))
                        {
                            /* Run through display list and assign branch, parent and temp ids to structure DPMSTTopology
                                Starting index to noOfBranches since we want to store display details after branch details in same array */
                            for (lBranchindex = noOfBranches; lBranchindex < (noOfDisplays + noOfBranches); lBranchindex++)
                            {
                                INFO_LOG("[Displayport.DLL]: Display %d's Parent index: %d", lBranchindex + 1, pDisplays[lDisplayindex].ulParentBranchIndex);

                                strcpy(CurTopology[lBranchindex].chNode, "Display");
                                CurTopology[lBranchindex].uiParentId = pDisplays[lDisplayindex++].ulParentBranchIndex;

                                uiTotalNoOfNodes++;
                            }

                            hr_SA = ::SafeArrayUnaccessData(displayDetails);
                        }
                    }
                    else
                    {
                        INFO_LOG("[Displayport.DLL]: DisplayDetails not available! ");
                    }
                }
                else
                {
                    /* CUISDK call GetTopologyDetailsForDisplayPort failed to get DP1.2 topology details! */
                    INFO_LOG("[Displayport.DLL]: Get topology details for DisplayPort FAILED -> HRESULT : %d ", hr);
                }

                if (NULL != branchDetails)
                {
                    /* Cleanup resources */
                    SafeArrayDestroy(branchDetails);
                    branchDetails = NULL;
                    pBranches     = NULL;
                }

                if (NULL != displayDetails)
                {
                    /* Cleanup resources */
                    SafeArrayDestroy(displayDetails);
                    displayDetails = NULL;
                    pDisplays      = NULL;
                }
            }
            else
            {
                /* CUISDK call to get valid DP1.2 ports failed! */
                INFO_LOG("[Displayport.DLL]: Get valid DP1.2 topology ports FAILED -> HRESULT : %d ", hr);
            }
        }
        else
        {
            uiStatus = GFXSIM_DISPLAY_FAILURE;

            /* Failed to get handle to CUISDK */
            INFO_LOG("[Displayport.DLL]: Error: CUISDK CUIExternal Failure: Igfxext initialization failed! Exiting.... ");
        }

        /*************************************** Get MST topology from Gfx Simulation driver ***************************************/

        DWORD dwStatus      = 0;
        DWORD BytesReturned = 0;

        PBRANCHDISP_RAD_ARRAY pAppliedTopologyData = (PBRANCHDISP_RAD_ARRAY)malloc(sizeof(BRANCHDISP_RAD_ARRAY));

        if (pAppliedTopologyData == NULL)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Not enough memory to allocate Branch Display Array! Exiting ....");
            break;
        }

        stDPDevContext.hGfxValSimHandle = GetGfxValSimHandle();

        /* Check for GfxValSimDriver handler */
        if (stDPDevContext.hGfxValSimHandle == NULL)
        {
            uiStatus = GFXSIM_DISPLAY_FAILURE;
            break;
        }

        devIoControlBuffer.pInBuffer     = &ulPortNum;
        devIoControlBuffer.inBufferSize  = sizeof(ULONG);
        devIoControlBuffer.pOutBuffer    = pAppliedTopologyData;
        devIoControlBuffer.outBufferSize = sizeof(BRANCHDISP_RAD_ARRAY);
        devIoControlBuffer.pAdapterInfo  = &GFX_0_ADAPTER_INFO; /* Get adapter info from cached data */

        /* Send DeviceIoCtl for getting the RAD information */
        dwStatus =
        DeviceIoControl(stDPDevContext.hGfxValSimHandle, (DWORD)IOCTL_GET_MST_RAD, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, NULL, &BytesReturned, NULL);

        if (OPERATION_FAILED == dwStatus)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Get RAD IOCTL failed with error code: 0x%u", GetLastError());
            uiStatus = GFXSIM_DISPLAY_FAILURE;
            break;
        }

        /*************************** Verification of Expected and Applied topologies are identical or not *****************************/

        /* TODO: Currently we are verifying total number of nodes count, level/parent-id of each corresponding nodes (Branch/Display) in
           Expected/Applied are identical or not. We need to find solution to compare even whether Display manufacture/model are same or not */

        /* Fail if total number of nodes (Branches + Displays) in expected and applied topologies are different */
        if (uiTotalNoOfNodes != (pAppliedTopologyData->ulNumBranches + pAppliedTopologyData->ulNumDisplays))
        {
            uiStatus = GFXSIM_DISPLAY_FAILURE;
            INFO_LOG("[Displayport.DLL]: Expected and Applied topologies are different.");
            break;
        }

        /* Compare whether each branch in expected and applied topologies which are at same level in the topology tree. We need to fail
           if corresponding branch nodes are not at same level eventhough if both topologies contains same number of branch nodes.
           for (uiBranchindex = 0; uiBranchindex < stDPDevContext.numberOfBranches; uiBranchindex++) */
        for (uiBranchIteration = 0; uiBranchIteration < pAppliedTopologyData->ulNumBranches; uiBranchIteration++)
        {
            for (ulBranchindex_Verification = 0; ulBranchindex_Verification < pAppliedTopologyData->ulNumBranches; ulBranchindex_Verification++)
            {
                if (CurTopology[ulBranchindex_Verification].bVisited == TRUE)
                {
                    continue;
                }

                if (pAppliedTopologyData->stBranchRADInfo[uiBranchIteration].ulParentBranchIndex == CurTopology[ulBranchindex_Verification].uiParentId)
                {
                    CurTopology[ulBranchindex_Verification].bVisited = TRUE;
                    /* Do nothing. Just continue with next branch in the topology */
                    break;
                }
            }
        }

        for (ulBranchindex_Verification = 0; ulBranchindex_Verification < pAppliedTopologyData->ulNumBranches; ulBranchindex_Verification++)
        {
            if (CurTopology[ulBranchindex_Verification].bVisited == FALSE)
            {
                /* We should not hit here. If we hit, means Parent ids of branch nodes are different for
                   branches at same level in both expected and applied topologies */
                uiStatus = GFXSIM_DISPLAY_BRANCHES_MISMATCH;

                /* Set the flag bBranchesMatching to FALSE indicating number of branches and their
                   corresponding are mis-matching */
                bBranchesMatching = FALSE;

                break;
            }
        }

        /* No point in continuing with Displays comparision if Branches comparision failed! */
        if (bBranchesMatching == FALSE)
        {
            break;
        }

        /* Compare whether each display in expected and applied topologies which are at same level in the topology tree. We need to fail
           if corresponding display nodes are not at same level eventhough if both topologies contains same number of display nodes.
           for (int uiDisplayIndex = 0; uiDisplayIndex < stDPDevContext.numberOfDisplays; uiDisplayIndex++) */
        for (uiDisplayIteration = 0; uiDisplayIteration < pAppliedTopologyData->ulNumDisplays; uiDisplayIteration++)
        {
            for (ULONG ulDisplayIndex = 0; ulDisplayIndex < pAppliedTopologyData->ulNumDisplays; ulDisplayIndex++)
            {
                if (CurTopology[uiBranchIteration + ulDisplayIndex].bVisited == TRUE)
                {
                    continue;
                }

                if (pAppliedTopologyData->stDisplayRADInfo[uiDisplayIteration].ulParentBranchIndex == (CurTopology[uiBranchIteration + ulDisplayIndex].uiParentId))
                {
                    CurTopology[uiBranchIteration + ulDisplayIndex].bVisited = TRUE;
                    /* Do nothing. Just continue with next display in the topology */
                    break;
                }
            }
        }

        for (ULONG ulDisplayIndex = 0; ulDisplayIndex < pAppliedTopologyData->ulNumDisplays; ulDisplayIndex++)
        {
            if (CurTopology[ulDisplayIndex].bVisited == FALSE)
            {
                /* We should not hit here. If we hit, means Parent ids of display nodes are different for displays at same level in both
                   expected and applied topologies */
                uiStatus = GFXSIM_DISPLAY_DISPLAYS_MISMATCH;

                /* Set the flag bBranchesMatching to FALSE indicating number of displays and their
                   corresponding are mis-matching */
                bDisplaysMatching = FALSE;

                break;
            }
        }

        /* Return TRUE if topologies are matching */
        if (bBranchesMatching && bDisplaysMatching)
        {
            uiStatus = GFXSIM_DISPLAY_TOPOLOGIES_MATCHING;
        }
    } while (FALSE);

    return uiStatus;
}

/**
 * @brief		Routine that calls to add or delete display/topology
 * @param[in]    ulPortNum : Port number
 * @param[in]	pRADData  : RAD Information
 * @return		BOOL. TRUE if PASS, FALSE if FAIL
 */
BOOL GetMSTTopologyRAD(ULONG ulPortNum, PBRANCHDISP_RAD_ARRAY pRADData)
{
    BOOL                     bStatus            = TRUE;
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    do
    {
        stDPDevContext.hGfxValSimHandle = GetGfxValSimHandle();

        /* Check for GfxValSimDriver handler */
        if (stDPDevContext.hGfxValSimHandle == NULL)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Gfx Val Simulation driver not initialized!!!... Exiting...");
            bStatus = FALSE;
            break;
        }

        /* Check for pRADData pointer for NULL value */
        if (pRADData == NULL)
        {
            INFO_LOG("[DisplayPort.DLL]: Error:RAD Data Object is NULL!!!... Exiting...");
            return FALSE;
            break;
        }

        devIoControlBuffer.pInBuffer     = &ulPortNum;
        devIoControlBuffer.inBufferSize  = sizeof(ULONG);
        devIoControlBuffer.pOutBuffer    = pRADData;
        devIoControlBuffer.outBufferSize = sizeof(BRANCHDISP_RAD_ARRAY);
        devIoControlBuffer.pAdapterInfo  = &GFX_0_ADAPTER_INFO; /* Get adapter info from cached data */

        /* Send RAD information via DeviceIOCLs */
        dwStatus =
        DeviceIoControl(stDPDevContext.hGfxValSimHandle, (DWORD)IOCTL_GET_MST_RAD, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, NULL, &BytesReturned, NULL);

        if (OPERATION_FAILED == dwStatus)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: IoCTL Failed during Get MST Topology RAD with error code: 0x%u", GetLastError());
            bStatus = FALSE;
            break;
        }

    } while (FALSE);

    return bStatus;
}

/**
 * @brief			Routine that calls to add/delete node/branch from the Topology
 * @params[In]   	Attach/Detach details of Branch/Display passed by the user
 * @params[In]   	RAD details passed by the user
 * @params[In]   	subTopology details needed for attaching branch/display
 * @params[In]   	bIsLowPower : To indicate the system to be in low power state
 * @return			BOOL. TRUE if PASS, FALSE if FAIL
 */
BOOL AddRemoveSubTopology(ULONG ulPortNum, BOOL bAttachDetach, PMST_RELATIVEADDRESS pstRAD, CHAR *pchSubTopologyXmlFile, BOOL bIsLowPower)
{
    BOOL                     bStatus            = TRUE;
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    UINT                     uiParentIndex      = PARENT_INDEX_SUB_TOPOLOGY;
    PDP_SUBTOPOLOGY_ARGS     pCsnData           = NULL;
    PBRANCHDISP_DATA_ARRAY   pBranchDispArray   = NULL;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    rapidxml::xml_document<> *doc         = new rapidxml::xml_document<>();
    rapidxml::xml_node<> *    pchRootNode = NULL;

    do
    {
        INFO_LOG("AddRemoveSubTopology called for Port %lu with Attach Status as %d and Low Power %d", ulPortNum, bAttachDetach, bIsLowPower);

        stDPDevContext.hGfxValSimHandle = GetGfxValSimHandle();

        /* Check for GfxValSimDriver handler */
        if (stDPDevContext.hGfxValSimHandle == NULL)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Gfx Val Simulation driver not initialized!!!... Exiting...");
            bStatus = FALSE;
            break;
        }

        /* Memory Allocation for Adding/deleting Node/display from DP Topology*/
        pCsnData = (PDP_SUBTOPOLOGY_ARGS)malloc(sizeof(DP_SUBTOPOLOGY_ARGS));
        if (pCsnData == NULL)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Failed to allocate Memory for Sub-Topology Data!!!... Exiting...");
            bStatus = FALSE;
            break;
        }
        memset(pCsnData, 0, sizeof(DP_SUBTOPOLOGY_ARGS));

        /* Memory Allocation for Node/display details from DP Topology*/
        pBranchDispArray = (PBRANCHDISP_DATA_ARRAY)malloc(sizeof(BRANCHDISP_DATA_ARRAY));
        if (pBranchDispArray == NULL)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Failed to allocate Memory for Topology Data!!!... Exiting...");
            bStatus = FALSE;
            break;
        }
        memset(pBranchDispArray, 0, sizeof(BRANCHDISP_DATA_ARRAY));

        /* Populating sub topology details */
        pCsnData->ulPortNum       = ulPortNum;
        pCsnData->bAttachOrDetach = bAttachDetach;
        memcpy(&pCsnData->stNodeRAD, pstRAD, sizeof(MST_RELATIVEADDRESS));

        if (bAttachDetach == TRUE)
        {
            rapidxml::file<> subTopologyXMLFile(pchSubTopologyXmlFile);

            /* Parse Branch/Display Data from DPMST XML and get details*/
            doc->parse<0>(subTopologyXMLFile.data());

            pchRootNode = doc->first_node();
            pchRootNode = pchRootNode->first_node();

            /* Function call to parse topology data, fail if data is not present*/
            if (FALSE == SIMDRVPARSER_RecursiveParseTopologyDataFromXML(pchRootNode, pBranchDispArray, uiParentIndex))
            {
                INFO_LOG("[DisplayPort.DLL]: Error: The Topology Data in the XML is in invalid format!!!... Exiting...");
                bStatus = FALSE;
                break;
            }

            /* Fill the subTopology parsed and send it to IoCTL for generating SPI */
            memcpy(&(pCsnData->stSubTopology), pBranchDispArray, sizeof(BRANCHDISP_DATA_ARRAY));
        }

        if (bIsLowPower == TRUE)
        {
            devIoControlBuffer.pInBuffer    = pCsnData;
            devIoControlBuffer.inBufferSize = sizeof(DP_SUBTOPOLOGY_ARGS);
            devIoControlBuffer.pAdapterInfo = &GFX_0_ADAPTER_INFO; /* Get adapter info from cached data */

            /* Send DeviceIoCtl for doing partial topology update in low power mode */
            dwStatus = DeviceIoControl(stDPDevContext.hGfxValSimHandle, (DWORD)IOCTL_GFXS3S4_ADDREMOVESUBTOPOLOGY, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL,
                                       NULL, &BytesReturned, NULL);
        }
        else
        {
            INFO_LOG("CSN data Attach Status is %d", pCsnData->bAttachOrDetach);
            devIoControlBuffer.pInBuffer    = pCsnData;
            devIoControlBuffer.inBufferSize = sizeof(DP_SUBTOPOLOGY_ARGS);
            devIoControlBuffer.pAdapterInfo = &GFX_0_ADAPTER_INFO; /* Get adapter info from cached data */
            /* Send DeviceIoCtl for adding/removing sub topology details */
            dwStatus =
            DeviceIoControl(stDPDevContext.hGfxValSimHandle, (DWORD)IOCTL_GENERATE_CSN, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, NULL, &BytesReturned, NULL);
        }

        if (OPERATION_FAILED == dwStatus)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Failed to attach/detach Display/Branch with error code: 0x%u", GetLastError());
            bStatus = FALSE;
            break;
        }

    } while (FALSE);

    /* free the topology data array */
    if (pBranchDispArray != NULL)
    {
        free(pBranchDispArray);
    }

    /* free the sub-topology data array */
    if (pCsnData != NULL)
    {
        free(pCsnData);
    }

    doc->clear();
    delete doc;

    return bStatus;
}

/**
 * @brief		Routine that calls to set target to low power state
 * @param[in]	pPowerData : pointer to structure GFXS3S4_ALLPORTS_PLUGUNPLUG_DATA contains number of ports, port number, plug/unplug status
 * @return		BOOL. TRUE if PASS, FALSE if FAIL
 */
BOOL SetLowPowerState(PGFXS3S4_ALLPORTS_PLUGUNPLUG_DATA pPowerData)
{
    BOOL                     bStatus            = TRUE;
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    do
    {
        stDPDevContext.hGfxValSimHandle = GetGfxValSimHandle();

        /* Check for GfxValSimDriver handler */
        if (stDPDevContext.hGfxValSimHandle == NULL)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Gfx Val Simulation driver not initialized!!!... Exiting...");
            bStatus = FALSE;
            break;
        }

        /* Check for pPowerData pointer for NULL value */
        if (pPowerData == NULL)
        {
            INFO_LOG("[DisplayPort.DLL]: Error : pPowerData Object is NULL!!!... Exiting...");
            return FALSE;
            break;
        }

        devIoControlBuffer.pInBuffer    = pPowerData;
        devIoControlBuffer.inBufferSize = sizeof(GFXS3S4_ALLPORTS_PLUGUNPLUG_DATA);
        devIoControlBuffer.pAdapterInfo = &GFX_0_ADAPTER_INFO; /* Get adapter info from cached data */

        /* Send DeviceIoCtl to plug/unplug display in low power mode */
        dwStatus = DeviceIoControl(stDPDevContext.hGfxValSimHandle, (DWORD)IOCTL_GFXS3S4_PLUGUNPLUG_DATA, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, NULL,
                                   &BytesReturned, NULL);

        if (OPERATION_FAILED == dwStatus)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: IoCTL Failed during Set to S3/S4 with error code: 0x%u", GetLastError());
            bStatus = FALSE;
            break;
        }

    } while (FALSE);

    return bStatus;
}

/**
 * @brief        Exposed API to Write DPCD Value
 * @param[in]    pDpcdWriteData	: pointer to structure SET_DPCD_ARGS contains port number and RAD
 * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
BOOL WriteDPCD(PSET_DPCD_ARGS pDpcdWriteData)
{
    BOOL                     bStatus            = TRUE;
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    do
    {
        stDPDevContext.hGfxValSimHandle = GetGfxValSimHandle();

        /* Check for GfxValSimDriver handler */
        if (stDPDevContext.hGfxValSimHandle == NULL)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Gfx Val Simulation driver not initialized!!!... Exiting...");
            return FALSE;
            break;
        }

        /* Check for pDpcdData pointer for NULL value */
        if (pDpcdWriteData == NULL)
        {
            INFO_LOG("[DisplayPort.DLL]: Error : DPCD Write Data Object is NULL!!!... Exiting...");
            return FALSE;
            break;
        }

        devIoControlBuffer.pInBuffer    = pDpcdWriteData;
        devIoControlBuffer.inBufferSize = (sizeof(SET_DPCD_ARGS) + pDpcdWriteData->ulWriteLength);
        devIoControlBuffer.pAdapterInfo = &GFX_0_ADAPTER_INFO; /* Get adapter info from cached data */

        /* Send DPCD read to Gfx Simulation driver via DeviceIOCLs  */
        dwStatus =
        DeviceIoControl(stDPDevContext.hGfxValSimHandle, (DWORD)IOCTL_WRITE_DPCD, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, NULL, &BytesReturned, NULL);

        if (OPERATION_FAILED == dwStatus)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: IoCTL Failed during Write DPCD call with error code: 0x%u ", GetLastError());
            bStatus = FALSE;
            break;
        }

    } while (FALSE);

    return bStatus;
}

/**
 * @brief		API to Initaizlize CUI SDK
 * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
BOOL InitializeCUISDK()
{
    HRESULT hr      = CoInitialize(NULL);
    BOOL    bStatus = FALSE;
    if (SUCCEEDED(hr))
    {
        CLSID clsid;
        hr = CLSIDFromProgID(L"Igfxext.CUIExternal", &clsid);
        if (SUCCEEDED(hr))
        {
            hr = CoCreateInstance(clsid, NULL, CLSCTX_SERVER, IID_ICUIExternal8, (void **)&m_pCUIExternal);
            if (FAILED(hr))
            {
                INFO_LOG("CoCreateInstance() Failed");
                bStatus = FALSE;
            }
        }
    }
    else
    {
        bStatus = FALSE;
    }
    return TRUE;
}

/**
 * @breief       API to Uninitialize CUI SDK
 */
BOOL UninitializeCUISDK()
{
    BOOL bStatus = FALSE;
    // Initialize CUISDK 2 times and uninitialize only once to properly cleanup the CUI COM objects.
    // If we don't initialize CUISDK 2 times, then control doesn't get transferred from DisplayPort.DLL
    // to the Python libraries resulting in Software hang. This is WA (WorkAround) only. Proper fix
    // needs to be figure-out. As per blogs on Python, this issue shouldn’t observe with latest Python
    // binaries but we needs to be verified.
    if (TRUE == InitializeCUISDK())
    {
        m_pCUIExternal->Release();
        m_pCUIExternal = NULL;
        CoUninitialize();
        bStatus = TRUE;
    }

    return bStatus;
}

/**
 * @brief        Exposed API to check if Collage is Enabled or Disabled
 * @param[in]    None
 * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
BOOL IsCollageEnabled()
{
    BOOL                bStatus       = FALSE;
    IGFX_COLLAGE_STATUS stCollageInfo = {
        0,
    };
    HRESULT hr;
    DWORD   dwExtraErrorCode = NULL;
    DWORD   dwSize;

    do
    {
        // Verify CUISDK handle available or not
        if (m_pCUIExternal)
        {

            dwSize = sizeof(IGFX_COLLAGE_STATUS);

            stCollageInfo.versionHeader.dwVersion = m_dwVersion;

            // Call the below GUID to get the collage  information
            hr = m_pCUIExternal->GetDeviceData(&IGFX_GET_SET_COLLAGE_STATUS_GUID, dwSize, (BYTE *)&stCollageInfo, &dwExtraErrorCode);
            if (SUCCEEDED(hr) && dwExtraErrorCode == IGFX_SUCCESS)
            {
                INFO_LOG("[DisplayPort.DLL]: Collage Information is retrieved successfully...");
                // Verify collage mode is enabled or not
                if (stCollageInfo.bIsCollageModeEnabled == 1)
                {
                    bStatus = TRUE;
                    INFO_LOG("[DisplayPort.DLL]: Collage mode is enabled...");
                    break;
                }
                else
                {
                    INFO_LOG("[DisplayPort.DLL]: Collage mode is not enabled...");
                    break;
                }
            }
            else
            {
                INFO_LOG("[DisplayPort.DLL]: Failed to get the Collage Information...");
                break;
            }
        }
        else
        {
            INFO_LOG("[DisplayPort.DLL]: Error : CUISDK initialization FAILED!!!... Exiting...");
            break;
        }

    } while (FALSE);

    return bStatus;
}

/**
 * @brief        Exposed API to check if Collage is supported or not in the platform
 * @param[in]    None
 * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
BOOL GetCollageInfo()
{
    BOOL                bStatus       = FALSE;
    IGFX_COLLAGE_STATUS stCollageInfo = {
        0,
    };
    HRESULT hr;
    DWORD   dwExtraErrorCode = NULL;
    DWORD   dwSize;

    do
    {
        // Verify CUISDK handle available or not
        if (m_pCUIExternal)
        {
            dwSize = sizeof(IGFX_COLLAGE_STATUS);

            stCollageInfo.versionHeader.dwVersion = m_dwVersion;

            // Call the below GUID to get the collage  information
            hr = m_pCUIExternal->GetDeviceData(&IGFX_GET_SET_COLLAGE_STATUS_GUID, dwSize, (BYTE *)&stCollageInfo, &dwExtraErrorCode);

            if (SUCCEEDED(hr) && dwExtraErrorCode == IGFX_SUCCESS)
            {
                // Verify collage mode is supported or not
                if (stCollageInfo.bIsCollageModeSupported == 0)
                {
                    INFO_LOG("[DisplayPort.DLL]: Error : Collage mode is NOT supported by the platform!!!... Exiting...");
                    break;
                }
                else
                {
                    bStatus = TRUE;
                    INFO_LOG("[DisplayPort.DLL]: Collage mode is supported by the platform....");

                    // Verify collage mode is enabled or not
                    if (stCollageInfo.bIsCollageModeEnabled == 1)
                    {
                        INFO_LOG("[DisplayPort.DLL]: Collage mode is enabled...");
                    }
                    else
                    {
                        INFO_LOG("[DisplayPort.DLL]: Collage mode is not enabled...");
                    }
                    break;
                }
            }
            else
            {
                INFO_LOG("[DisplayPort.DLL]: Failed to get the Collage Information...");
                break;
            }
        }
        else
        {
            INFO_LOG("[DisplayPort.DLL]: Error : CUISDK initialization FAILED!!!... Exiting...");
            break;
        }

    } while (FALSE);

    return bStatus;
}

/**
 * @brief        Exposed API to set the Collage Mode for the selected Displays
 * @param[in]    pstGetSystemConfigExData: Pointer to structure IGFX_SYSTEM_CONFIG_DATA_N_VIEW
 * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
BOOL ApplyCollage(PIGFX_SYSTEM_CONFIG_DATA_N_VIEW pstGetSystemConfigExData)
{
    BOOL    bStatus = FALSE;
    HRESULT hr;
    DWORD   dwError = 0;
    do
    {
        if (m_pCUIExternal)
        {
            UINT uiSize = pstGetSystemConfigExData->uiSize;
            // Call the below GUID to set the collage
            hr = m_pCUIExternal->SetDeviceData((GUID *)&IGFX_GET_SET_N_VIEW_CONFIG_GUID, uiSize, (BYTE *)pstGetSystemConfigExData, &dwError);
            if (SUCCEEDED(hr) && dwError == 0)
            {
                INFO_LOG("[DisplayPort.DLL]: Collage Mode Applied Successfully...");
                bStatus = TRUE;
                break;
            }
            else
            {
                INFO_LOG("[DisplayPort.DLL]: Failed to Apply Collage Mode...");
                break;
            }
        }
        else
        {
            INFO_LOG("[DisplayPort.DLL]: Error : CUISDK initialization FAILED!!!... Exiting...");
            break;
        }
    } while (FALSE);

    return bStatus;
}

/**
 * @brief        Exposed API to get all the supported Config For Ex, SD,DD CLone, Tri Clone, Tri ED, Dual Hor Collage, etc
 * @param[in]    pstConfigEx: Pointer to structure IGFX_TEST_CONFIG_EX
 * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
BOOL GetSupportedConfig(PIGFX_TEST_CONFIG_EX pstConfigEx)
{
    BOOL    bStatus = FALSE;
    HRESULT hr;
    DWORD   dwError = 0;
    do
    {
        if (m_pCUIExternal)
        {
            pstConfigEx->versionHeader.dwVersion = 1;
            // Call the below GUID to get all the supported configs
            // TODO: currently while debugging found that TRI Collage is not listed as a config when one DP port is connected with 3 displays.
            hr = m_pCUIExternal->GetDeviceData((GUID *)&IGFX_SUPPORTED_CONFIGURATIONS_EX, sizeof(IGFX_TEST_CONFIG_EX), (BYTE *)pstConfigEx, &dwError);
            if (SUCCEEDED(hr) && dwError == 0)
            {
                INFO_LOG("[DisplayPort.DLL]: All Suported Configuration retrieved Successfully...");
                bStatus = TRUE;
                break;
            }
            else
            {
                INFO_LOG("[DisplayPort.DLL]: All Suported Configuration retrieval failed...");
                break;
            }
        }
        else
        {
            INFO_LOG("[DisplayPort.DLL]: Error : CUISDK initialization FAILED!!!... Exiting...");
            break;
        }
    } while (FALSE);

    return bStatus;
}

/**
 * @brief        Exposed API to get all the supported modes for the applied collage config
 * @param[in]    pstGetSystemConfigExData: Pointer to structure IGFX_SYSTEM_CONFIG_DATA_N_VIEW
 * @param[in]    uiDisplayIndex: display index
 * @param[out]   pstVideoModesListEx2: Pointer to structure IGFX_VIDEO_MODE_LIST_EX
 * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
BOOL Collage_GetSupportedModes(PIGFX_SYSTEM_CONFIG_DATA_N_VIEW pstGetSystemConfigExData, UINT uiDisplayIndex, PIGFX_VIDEO_MODE_LIST_EX pstVideoModesListEx2)
{
    BOOL    bStatus = FALSE;
    HRESULT hr;
    DWORD   dwError  = 0;
    BOOL    bModeset = TRUE;

    do
    {
        if (m_pCUIExternal)
        {
            IGFX_VIDEO_MODE_LIST_EX VideoModesListEx2 = { 0 };

            ZeroMemory(&VideoModesListEx2, sizeof(VideoModesListEx2));
            VideoModesListEx2.versionHeader.dwVersion = 1;
            // this will be config applied ie Dual/Tri Hor/Ver Collage
            VideoModesListEx2.dwOpMode = pstGetSystemConfigExData->dwOpMode;
            // Number of displays in the collage mode
            VideoModesListEx2.uiNDisplays = pstGetSystemConfigExData->uiNDisplays;
            // Fill the  display UID for each displays
            for (UINT uiNumOfDisplays = 0; uiNumOfDisplays < pstGetSystemConfigExData->uiNDisplays; uiNumOfDisplays++)
            {
                VideoModesListEx2.DispCfg[uiNumOfDisplays].dwDisplayUID = pstGetSystemConfigExData->DispCfg[uiNumOfDisplays].dwDisplayUID;
            }
            VideoModesListEx2.dwDeviceID = pstGetSystemConfigExData->DispCfg[uiDisplayIndex].dwDisplayUID;
            VideoModesListEx2.dwFlags    = IGFX_VIDEO_MODE_LIST_SIZE_ONLY;
            // Get the number of modes supported ie VideoModesListEx2.vmlNumMode
            hr = m_pCUIExternal->GetDeviceData((GUID *)&IGFX_GET_VIDEO_MODE_LIST_GUID, sizeof(VideoModesListEx2), (BYTE *)&VideoModesListEx2, &dwError);
            if (SUCCEEDED(hr) && dwError == 0)
            {
                // allocate memory based on the number of modes supported
                DWORD                    dwSize             = sizeof(IGFX_VIDEO_MODE_LIST_EX) + (sizeof(IGFX_DISPLAY_RESOLUTION_EX) * (VideoModesListEx2.vmlNumModes - 1));
                IGFX_VIDEO_MODE_LIST_EX *VideoModesListEx23 = (IGFX_VIDEO_MODE_LIST_EX *)malloc(dwSize);
                memcpy(VideoModesListEx23, &VideoModesListEx2, sizeof(IGFX_VIDEO_MODE_LIST_EX));
                VideoModesListEx23->versionHeader.dwVersion = 1;
                VideoModesListEx23->dwFlags                 = 0;
                hr                                          = m_pCUIExternal->GetDeviceData((GUID *)&IGFX_GET_VIDEO_MODE_LIST_GUID, dwSize, (BYTE *)VideoModesListEx23, &dwError);
                if (SUCCEEDED(hr) && dwError == 0)
                {
                    INFO_LOG("[DisplayPort.DLL]: Get the supported modes for collage is successful...");
                    // Copy the mode information
                    memcpy((PVOID)pstVideoModesListEx2, (PVOID)VideoModesListEx23, dwSize);
                    bStatus = TRUE;
                    if (VideoModesListEx23 != NULL)

                    {
                        free(VideoModesListEx23);
                        VideoModesListEx23 = NULL;
                    }
                    break;
                }
                else
                {
                    INFO_LOG("[DisplayPort.DLL]: Failed to Get the supported modes for collage...");
                    if (VideoModesListEx23 != NULL)
                    {
                        free(VideoModesListEx23);
                        VideoModesListEx23 = NULL;
                    }
                    break;
                }
            }
            else
            {
                INFO_LOG("[DisplayPort.DLL]: Failed to Get the Size of supported modes for collage...");
                break;
            }
        }

    } while (FALSE);

    return bStatus;
}
