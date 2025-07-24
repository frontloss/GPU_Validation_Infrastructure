#include "DPHandlers.h"
#include "CommonRxHandlers.h"
#include "..\\DPCore\DPCDModel.h"
#include "..\\CommonInclude\\ETWLogging.h"

// This struct has a very specific use, its used to initialize a DPCD modifier list that would modify any DPCD file being configured by the app
// This example would make it more clear: We found an issue where DPCD addresses 0x201 and 0x202 though which a DP Sink indicates the link status (if bits are set in these
// DPCDs, it means link training steps like EQ and CR succeeded) were already set in the raw DPCD file without even the link training and this was
// causing all kinds of Machine checks and hangs when graphics did mode set due to a Yangra specific link training optimization code.
// So the below list would act as a repository of DPCDs that we want to have a certain predefined values such as DPCD 0x201 and 0x201 must have an initial value of 0x0.
// Also use such static declarations and global variables only if there's no other way
// Here it was neccesary because this list is a singleton and would be used across all DP ports/Auxinterfaces the same way
static DPCD_ADDR_VALUE_PAIR staticDPCDAddrValPair[] = { { 0x201, 0x0 }, { 0x202, 0x0 }, { 0x203, 0x0 }, { 0x600, 0x1 } };

// Lets keep PDPAUX_INTERFACE pstDPAuxInterface read only in this file to take decisions based on current configuration
// Lets do any modification

// LETS NOT MANIPULATE PRX_INFO_ARR Member Variables directly in this file but implement functional interfaces
// that are implemented in AuxInterface.c

BOOLEAN DPHANDLERS_CreateDPMSTSubTopology(PDP12_TOPOLOGY pstDP12Topology, PVOID *pstInOutNode, PBRANCHDISP_DATA_ARRAY pstBranchDispDataArr);

void DPHANDLERS_ModifyDPCDBasedonStaticList(PFILE_DATA pstDPCDData);

PDPAUX_INTERFACE DPHANDLERS_DPInterfaceInit(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType)
{
    BOOLEAN           bRet           = FALSE;
    ULONG             ulDataStartReg = 0, ulDataEndReg = 0, ulControlReg = 0;
    PPORTINGLAYER_OBJ pstPortingObj     = GetPortingObj();
    PDPAUX_INTERFACE  pstDPAuxInterface = (PDPAUX_INTERFACE)pstPortingObj->pfnAllocateMem(sizeof(DPAUX_INTERFACE), TRUE);

    do
    {
        if (pstDPAuxInterface == NULL || pstRxInfoArr == NULL)
        {
            break;
        }

        // Get the Aux Register offsets for the Platform under test and the Port specified by the app
        if (FALSE == COMMONMMIOHANDLERS_GetPortAuxRegOffsets(pstRxInfoArr->pstMMIOInterface, ePortType, &ulDataStartReg, &ulDataEndReg, &ulControlReg))
        {
            break;
        }

        // Use the aux register offsets obtained from the call above to Intialize AuxInterface
        if (FALSE == AUXINTERFACE_Init(pstDPAuxInterface, pstRxInfoArr->pstMMIOInterface->stGlobalMMORegData.ucMMIORegisterFile,
                                       pstRxInfoArr->pstMMIOInterface->stGlobalMMORegData.ulMMIOBaseOffset, ePortType, ulDataStartReg, ulDataEndReg, ulControlReg))
        {
            break;
        }

        if (FALSE == COMMONMMIOHANDLERS_RegisterPortAuxHandlers(pstRxInfoArr->pstMMIOInterface, pstDPAuxInterface, ePortType))
        {
            break;
        }

        bRet = TRUE;

    } while (FALSE);

    if (bRet == FALSE && pstDPAuxInterface)
    {
        pstPortingObj->pfnFreeMem(pstDPAuxInterface);
        pstDPAuxInterface = NULL;
    }

    return pstDPAuxInterface;
}

BOOLEAN DPHANDLERS_InitDPTopologyType(PRX_INFO_ARR pstRxInfoArr, PDP_INIT_INFO pstDPInitInfo)
{
    BOOLEAN          bRet              = FALSE;
    PDPAUX_INTERFACE pstDPAuxInterface = NULL;

    GFXVALSIM_FUNC_ENTRY();

    // Implementation Note TBD: Cleanup DPTopology even for a new MST topology XML
    pstDPAuxInterface = COMMRXHANDLERS_GetAuxInterfaceFromPortType(pstRxInfoArr, pstDPInitInfo->uiPortNum);

    if (pstDPAuxInterface)
    {
        bRet = AUXINTERFACE_UpdateTopologyType(pstDPAuxInterface, pstDPInitInfo->eTopologyType);
    }
    GFXVALSIM_FUNC_EXIT(!bRet);

    return bRet;
}

BOOLEAN DPHANDLERS_SetDPCDModelData(PRX_INFO_ARR pstRxInfoArr, PDP_DPCD_MODEL_DATA pstDpDPCDModelData)
{
    GFXVALSIM_FUNC_ENTRY();

    BOOLEAN          bRet              = FALSE;
    PDPAUX_INTERFACE pstDPAuxInterface = NULL;

    do
    {
        pstDPAuxInterface = COMMRXHANDLERS_GetAuxInterfaceFromPortType(pstRxInfoArr, pstDpDPCDModelData->uiPortNum);

        if (pstDPAuxInterface == NULL)
        {
            break;
        }

        bRet = DPCDMODEL_LoadDPCDModelData(pstDPAuxInterface, pstDpDPCDModelData->eTopologyType, (PDPCD_MODEL_DATA) & (pstDpDPCDModelData->stDPCDModelData));

    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(!bRet);

    return bRet;
}

BOOLEAN DPHANDLERS_SetDPCDModelDataForS3S4Cycle(PVOID pstRxInfoArr, PDP_DPCD_MODEL_DATA pstDpDPCDModelData)
{
    GFXVALSIM_FUNC_ENTRY();

    BOOLEAN                  bRet                    = FALSE;
    PDP12_TOPOLOGY           pstDP12Topology         = NULL;
    PDPCD_MODEL_DATA         pstDestDPCDModelData    = NULL;
    PRX_S3S4_PLUGUNPLUG_DATA pstRxS3S4PlugUnPlugData = COMMRXHANDLERS_GetRxS3S4PlugUnPlugDataPtr(pstRxInfoArr, pstDpDPCDModelData->uiPortNum, DP);
    PDPAUX_INTERFACE         pstDPAuxInterface       = COMMRXHANDLERS_GetAuxInterfaceFromPortType(pstRxInfoArr, pstDpDPCDModelData->uiPortNum);
    PPORTINGLAYER_OBJ        pstPortingObj           = GetPortingObj();

    do
    {
        if (pstDPAuxInterface == NULL)
        {
            break;
        }

        if (pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.eTopologyType == eDPMST)
        {
            pstDP12Topology = pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pvNewDP12Topology;

            if (pstDP12Topology == NULL)
            {
                // Someone Tried to Set MST EDID data without Initializing the topology object. THIS SHOULD NEVER HAPPEN!
                break;
            }

            pstDestDPCDModelData = &(pstDP12Topology->stDPCDConfigData.stDPCDModelData);
            memcpy_s(pstDestDPCDModelData, sizeof(DPCD_MODEL_DATA), &(pstDpDPCDModelData->stDPCDModelData), sizeof(DPCD_MODEL_DATA));
            pstDP12Topology->stDPCDConfigData.ucDPCDTransactionIndex = 0;
            bRet                                                     = TRUE;
        }
        else
        {
            pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pstNewSSTDPCDConfigData = (PDPCD_CONFIG_DATA)pstPortingObj->pfnAllocateMem(sizeof(DPCD_CONFIG_DATA), TRUE);
            pstDestDPCDModelData                                              = &(pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pstNewSSTDPCDConfigData->stDPCDModelData);
            memcpy_s(pstDestDPCDModelData, sizeof(DPCD_MODEL_DATA), &(pstDpDPCDModelData->stDPCDModelData), sizeof(DPCD_MODEL_DATA));
            pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pstNewSSTDPCDConfigData->ucDPCDTransactionIndex = 0;
            bRet                                                                                      = TRUE;
        }

    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(!bRet);

    return bRet;
}

BOOLEAN DPHANDLERS_SetEDIDData(PRX_INFO_ARR pstRxInfoArr, PFILE_DATA pstEdidData)
{
    BOOLEAN           bRet              = FALSE;
    DP_TOPOLOGY_TYPE  eTopologyType     = eInvalidTopology;
    PDP12_TOPOLOGY    pstDP12Topology   = NULL;
    PSST_DISPLAY_INFO pstSSTDisplayInfo = NULL;
    PDPAUX_INTERFACE  pstDPAuxInterface = NULL;

    do
    {

        pstDPAuxInterface = COMMRXHANDLERS_GetAuxInterfaceFromPortType(pstRxInfoArr, pstEdidData->uiPortNum);

        if (pstDPAuxInterface == NULL)
        {
            break;
        }

        eTopologyType = AUXINTERFACE_GetTopologyType(pstDPAuxInterface);

        if (eTopologyType == eDPMST)
        {
            pstDP12Topology = AUXINTERFACE_GetMSTTopologPtr(pstDPAuxInterface);

            if (pstDP12Topology == NULL)
            {
                // Someone Tried to Set MST EDID data without Initializing the topology object. THIS SHOULD NEVER HAPPEN!
                break;
            }

            bRet = DP12TOPOLOGY_SetEDIDData(pstDP12Topology, pstEdidData->ucNodeName, pstEdidData->uiDataSize, (PUCHAR)(((PUCHAR)pstEdidData) + sizeof(FILE_DATA)));
        }
        else if (eTopologyType == eDPSST)
        {
            pstSSTDisplayInfo = AUXINTERFACE_GetSSTDisplayInfoPtr(pstDPAuxInterface);

            if (pstSSTDisplayInfo == NULL)
            {
                break;
            }

            bRet = SSTDISPLAY_SetEDIDData(pstSSTDisplayInfo, pstEdidData->uiDataSize, (PUCHAR)(((PUCHAR)pstEdidData) + sizeof(FILE_DATA)));
        }

    } while (FALSE);

    return bRet;
}

// This function is kept temporarily to fill model data for PASSing link training in first two transactions itself. As of now, this is called from DPHANDLERS_SetDPCDData()
// Once we enable the mechanism to send user data from python in next phase, we will remove this function. Then plug from userspace should always send model data.
VOID DPHANDLERS_FillDPCDStaticUltData(PDP_DPCD_MODEL_DATA pstDpDPCDModelData, unsigned int uiPortNum, DP_TOPOLOGY_TYPE eTopologyType)
{
    /*****default transactions for 'PASSing LT immediately' case******/
    UCHAR transactionCount        = 2;
    UCHAR ucNumInputDpcdSets      = 0;
    UCHAR ucInputDpcdSetLength    = 0;
    UCHAR ucNumResponseDpcdSets   = 1;
    UCHAR ucResponseDpcdSetLength = 3;
    // 1st transaction for CR pass, and 2nd transcation for CHEQ pass
    ULONG inputStartingOffsets[20]    = { 0x102, 0x102 };     // dummy. Won't be used
    UCHAR inputValues[2][1]           = { { 0x0 }, { 0x0 } }; // dummy. Won't be used
    ULONG responseStartingOffsets[20] = { 0x202, 0x202 };
    UCHAR responseValues[2][3]        = { { 0x11, 0x11, 0x80 }, { 0x77, 0x77, 0x8D } };
    ULONG ulTriggerOffsetForTrans     = 0x103;

    pstDpDPCDModelData->uiPortNum     = uiPortNum;
    pstDpDPCDModelData->eTopologyType = eTopologyType;
    PDPCD_MODEL_DATA pDPCDModelData   = &(pstDpDPCDModelData->stDPCDModelData);

    pDPCDModelData->ulTriggerOffset    = ulTriggerOffsetForTrans;
    pDPCDModelData->ucTransactionCount = transactionCount;
    for (ULONG trans_index = 0; trans_index < pDPCDModelData->ucTransactionCount; trans_index++)
    {
        PDPCD_TRANSACTION pDPCDTrans                    = &(pDPCDModelData->stDPCDTransactions[trans_index]);
        pDPCDTrans->ucNumInputDpcdSets                  = ucNumInputDpcdSets;
        pDPCDTrans->stInputDpcdSets[0].ulStartingOffset = inputStartingOffsets[trans_index];
        pDPCDTrans->stInputDpcdSets[0].ucLength         = ucInputDpcdSetLength;
        for (int i = 0; i < ucInputDpcdSetLength; i++)
            pDPCDTrans->stInputDpcdSets[0].ucValues[i] = inputValues[trans_index][i];

        pDPCDTrans->ucNumResponseDpcdSets                  = ucNumResponseDpcdSets;
        pDPCDTrans->stResponseDpcdSets[0].ulStartingOffset = responseStartingOffsets[trans_index];
        pDPCDTrans->stResponseDpcdSets[0].ucLength         = ucResponseDpcdSetLength;
        for (int i = 0; i < ucResponseDpcdSetLength; i++)
            pDPCDTrans->stResponseDpcdSets[0].ucValues[i] = responseValues[trans_index][i];
    }
    GFXVALSIM_DBG_MSG("Filled DPCD model static ULT data succesfully\n");
}

BOOLEAN DPHANDLERS_SetDPCDData(PRX_INFO_ARR pstRxInfoArr, PFILE_DATA pstDPCDData)
{
    GFXVALSIM_FUNC_ENTRY();

    BOOLEAN          bRet              = FALSE;
    DP_TOPOLOGY_TYPE eTopologyType     = eInvalidTopology;
    PDP12_TOPOLOGY   pstDP12Topology   = NULL;
    PDPCD_MODEL_DATA pstDPCDModelData  = NULL;
    PDPAUX_INTERFACE pstDPAuxInterface = COMMRXHANDLERS_GetAuxInterfaceFromPortType(pstRxInfoArr, pstDPCDData->uiPortNum);
    do
    {
        if (pstDPAuxInterface == NULL)
        {
            break;
        }

        //
        DPHANDLERS_ModifyDPCDBasedonStaticList(pstDPCDData);

        eTopologyType = AUXINTERFACE_GetTopologyType(pstDPAuxInterface);

        if (eTopologyType == eDPMST)
        {
            pstDP12Topology = AUXINTERFACE_GetMSTTopologPtr(pstDPAuxInterface);

            if (pstDP12Topology == NULL)
            {
                // Someone Tried to Set MST EDID data without Initializing the topology object. THIS SHOULD NEVER HAPPEN!
                break;
            }

            //(PUCHAR)(pstDPCDData + sizeof(FILE_DATA)) because Raw DPCD data follows after the EDID_DPCD_DATA members
            // as per our agreement with the APP world for this IOCTL with the app world
            bRet = DP12TOPOLOGY_SetDPCDData(pstDP12Topology, pstDPCDData->ucNodeName, pstDPCDData->uiDataSize, (PUCHAR)(((PUCHAR)pstDPCDData) + sizeof(FILE_DATA)));
        }
        else
        {
            // We'd copy the DPCD for Display (directly connected to Source) directly in the AuxInterface object
            // Because AuxInterface would directly respond to Native Aux rather than going to sink
            // And Aux access to the Sink directly connected to source (Be it a Branch in MST mode or a Display in SST mode)
            // should always be Native Aux.
            if (NULL == AUXINTERFACE_SetDwnStrmDPCDMap(pstDPAuxInterface, (PUCHAR)(((PUCHAR)pstDPCDData) + sizeof(FILE_DATA)), pstDPCDData->uiDataSize))
            {
                break;
            }
        }

        /* Registring DPCD clients once the DPCD buffer is sent by app world and filled in Val-Sim DPCD buffer*/
        if (FALSE == AUXINTERFACE_InitialDPCDClientsRegister(pstDPAuxInterface, eTopologyType))
        {
            break;
        }

        bRet = TRUE;

        /*********************************temp code*****************************************/
        // temporary code to fill DPCD model data to PASS link training in first two transactions itself.
        // Although Plug lib in python is sending this data always, some userspace consumers (like DP MST testcases) are not sending the DPCD model data.
        // TODO: Remove this code portion once all userspace consumers start sending DPCD model data properly.
        if (eTopologyType == eDPMST)
            pstDPCDModelData = &(pstDPAuxInterface->pstDP12Topology->stDPCDConfigData.stDPCDModelData);
        else
            pstDPCDModelData = &(pstDPAuxInterface->pstSSTDisplayInfo->stDPCDConfigData.stDPCDModelData);

        // DPCD model data should have been set before setting DPCD data (through IOCTLs)
        // TransactionCount == 0 indicates that, no data has been sent from userspace for DPCD model data
        if (pstDPCDModelData->ucTransactionCount == 0)
        {
            PDP_DPCD_MODEL_DATA pstDpDPCDModelData;
            PPORTINGLAYER_OBJ   pstPortingObj = GetPortingObj();
            pstDpDPCDModelData                = (PDP_DPCD_MODEL_DATA)pstPortingObj->pfnAllocateMem(sizeof(DP_DPCD_MODEL_DATA), TRUE);
            if (pstDpDPCDModelData != NULL)
            {
                DPHANDLERS_FillDPCDStaticUltData(pstDpDPCDModelData, pstDPCDData->uiPortNum, eTopologyType);

                DPHANDLERS_SetDPCDModelData(pstRxInfoArr, pstDpDPCDModelData);
                pstPortingObj->pfnFreeMem(pstDpDPCDModelData);
            }
        }
        /***************************************************************************************/

    } while (FALSE);
    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}

// So the app world parses the Topology descripton from the XML and packs the branch and display information in a structure using the
// discussed algo and sends it to driver. Here, in this function, we use that info to finally build the topopology
BOOLEAN DPHANDLERS_SetDPMSTTopology(PRX_INFO_ARR pstRxInfoArr, PBRANCHDISP_DATA_ARRAY pstBranchDispDataArr)
{
    BOOLEAN bRet = FALSE;

    PDP12_TOPOLOGY pstDP12Topology  = NULL;
    PBRANCH_NODE   pstNewBranchNode = NULL;

    PBRANCHDISP_DPCD pstBranchDispDCPD = NULL;

    PUCHAR pucSharedDPCDBuff;

    NODE_ADD_ERRROR_CODES eNodeAdditionResult = eGENERIC_ERROR;

    PDPAUX_INTERFACE pstDPAuxInterface = COMMRXHANDLERS_GetAuxInterfaceFromPortType(pstRxInfoArr, pstBranchDispDataArr->uiPortNum);

    do
    {
        if (pstDPAuxInterface == NULL || eDPMST != AUXINTERFACE_GetTopologyType(pstDPAuxInterface) || pstBranchDispDataArr->uiNumBranches == 0)
        {
            break;
        }

        pstDP12Topology = AUXINTERFACE_GetMSTTopologPtr(pstDPAuxInterface);

        if (pstDP12Topology == NULL)
        {
            // Someone Tried to Set MST EDID data without Initializing the topology object. THIS SHOULD NEVER HAPPEN!
            break;
        }

        // Lets take First Branch Data: As per our Agreement with the app world, this should be the Branch connected to source with Parent Index 0xFFFFFFFF
        if (pstBranchDispDataArr->stBranchData[0].uiParentBranchIndex != PARENT_INDEX_BRANCH_CONNECTED_TO_SRC)
        {
            break;
        }

        // This is the branch connected to the source
        // Passing Null for what DPCD we want for this Branch. We'd link this branch's DPCD directly to the AUX_INTERFACE object that handles native Aux's
        pstNewBranchNode = DP12TOPOLOGY_CreateBranchNode(
        pstDP12Topology, eMSTBRANCHDEVICE, pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.ucTotalInputPorts,
        pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.ucTotalPhysicalPorts, pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.ucTotalVirtualPorts,
        pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.uiMaxLinkRate, pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.uiMaxLaneCount,
        pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.uiBranchReplyDelay, pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.usTotalAvailablePBN,
        pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.uiLinkAddressDelay, pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.uiRemoteI2ReadDelay,
        pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.uiRemoteI2WriteDelay, pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.uiRemoteDPCDReadDelay,
        pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.uiRemoteDPCDWriteDelay, pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.uiEPRDelay,
        pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.uiAllocatePayloadDelay, pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.uiClearPayLoadDelay, NULL);

        if (pstNewBranchNode == NULL)
        {
            break;
        }

        pstBranchDispDCPD = DP12TOPOLOGY_GetNodeDPCD(pstDP12Topology, pstBranchDispDataArr->stBranchData[0].ucDPCDName);

        if (pstBranchDispDCPD == NULL || pstBranchDispDCPD->ulDPCDBuffSize == 0)
        {
            break;
        }

        // We'd copy the DPCD for First branch (directly connected to Source) directly in the AuxInterface object
        // Because AuxInterface would directly respond to Native Aux rather than going to sink
        // And Aux access to the Sink directly connected to source (Be it a Branch in MST mode or a Display in SST mode)
        // should always be Native Aux.
        pucSharedDPCDBuff = AUXINTERFACE_SetDwnStrmDPCDMap(pstDPAuxInterface, pstBranchDispDCPD->pucDPCDBuff, pstBranchDispDCPD->ulDPCDBuffSize);

        if (NULL == pucSharedDPCDBuff)
        {
            break;
        }

        //!!!Branch directly connected to Source will share the DPCD that's stored in AuxInterface
        eNodeAdditionResult = DP12TOPOLOGY_AddFirstBranch(pstDP12Topology, pstNewBranchNode, pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.ucThisBranchInputPort,
                                                          pucSharedDPCDBuff, pstBranchDispDCPD->ucDPCDName, pstBranchDispDCPD->ulDPCDBuffSize);

        if (eNODE_ADD_SUCCESS != eNodeAdditionResult)
        {
            break;
        }

        bRet = DPHANDLERS_CreateDPMSTSubTopology(pstDP12Topology, &pstNewBranchNode, pstBranchDispDataArr);

    } while (FALSE);

    return bRet;
}

// While creating a fresh topology from scratch pstInOutBranchNode would contain address of the BranchConnectedSource
BOOLEAN DPHANDLERS_CreateDPMSTSubTopology(PDP12_TOPOLOGY pstDP12Topology, PVOID *pstInOutNode, PBRANCHDISP_DATA_ARRAY pstBranchDispDataArr)
{

    BOOLEAN               bRet                   = FALSE;
    PBRANCH_NODE          pstNewBranchNode       = NULL;
    PBRANCH_NODE          pstParentBranchNode    = NULL;
    PBRANCH_NODE *        pstTempBranchNodeArray = NULL;
    PDISPLAY_NODE         pstDisplayNode         = NULL;
    ULONG                 ulCount                = 0;
    ULONG                 ulCurrentBranchCount   = 0;
    NODE_ADD_ERRROR_CODES eNodeAdditionResult    = eNODE_ADD_SUCCESS;
    PPORTINGLAYER_OBJ     pstPortingObj          = GetPortingObj();

    do
    {
        if (pstBranchDispDataArr->uiNumBranches == 0 && pstBranchDispDataArr->uiNumDisplays == 0)
        {
            break;
        }

        pstTempBranchNodeArray = pstPortingObj->pfnAllocateMem(pstBranchDispDataArr->uiNumBranches * sizeof(PBRANCH_NODE), TRUE);

        if (pstTempBranchNodeArray == NULL)
        {
            break;
        }

        if (*pstInOutNode)
        {
            pstTempBranchNodeArray[ulCount] = *pstInOutNode;
            ulCurrentBranchCount++;
            ulCount++;
        }

        for (; ulCount < pstBranchDispDataArr->uiNumBranches; ulCount++)
        {
            pstNewBranchNode = DP12TOPOLOGY_CreateBranchNode(
            pstDP12Topology, eMSTBRANCHDEVICE, pstBranchDispDataArr->stBranchData[ulCount].stBranchNodeDesc.ucTotalInputPorts,
            pstBranchDispDataArr->stBranchData[ulCount].stBranchNodeDesc.ucTotalPhysicalPorts, pstBranchDispDataArr->stBranchData[ulCount].stBranchNodeDesc.ucTotalVirtualPorts,
            pstBranchDispDataArr->stBranchData[ulCount].stBranchNodeDesc.uiMaxLinkRate, pstBranchDispDataArr->stBranchData[ulCount].stBranchNodeDesc.uiMaxLaneCount,
            pstBranchDispDataArr->stBranchData[ulCount].stBranchNodeDesc.uiBranchReplyDelay, pstBranchDispDataArr->stBranchData[ulCount].stBranchNodeDesc.usTotalAvailablePBN,
            pstBranchDispDataArr->stBranchData[ulCount].stBranchNodeDesc.uiLinkAddressDelay, pstBranchDispDataArr->stBranchData[ulCount].stBranchNodeDesc.uiRemoteI2ReadDelay,
            pstBranchDispDataArr->stBranchData[ulCount].stBranchNodeDesc.uiRemoteI2WriteDelay, pstBranchDispDataArr->stBranchData[ulCount].stBranchNodeDesc.uiRemoteDPCDReadDelay,
            pstBranchDispDataArr->stBranchData[ulCount].stBranchNodeDesc.uiRemoteDPCDWriteDelay, pstBranchDispDataArr->stBranchData[ulCount].stBranchNodeDesc.uiEPRDelay,
            pstBranchDispDataArr->stBranchData[ulCount].stBranchNodeDesc.uiAllocatePayloadDelay, pstBranchDispDataArr->stBranchData[ulCount].stBranchNodeDesc.uiClearPayLoadDelay,
            pstBranchDispDataArr->stBranchData[ulCount].ucDPCDName);

            if (pstNewBranchNode == NULL)
            {
                break;
            }

            if (pstBranchDispDataArr->stBranchData[ulCount].uiParentBranchIndex == PARENT_INDEX_SUB_TOPOLOGY)
            {
                pstTempBranchNodeArray[ulCount] = pstNewBranchNode;
                ulCurrentBranchCount++;
                *pstInOutNode = pstNewBranchNode;
                continue;
            }

            // Parent Branch Index should always be less than the total number of branches we have till now
            if (pstBranchDispDataArr->stBranchData[ulCount].uiParentBranchIndex >= ulCurrentBranchCount)
            {
                break;
            }

            pstParentBranchNode = pstTempBranchNodeArray[pstBranchDispDataArr->stBranchData[ulCount].uiParentBranchIndex];

            if (pstParentBranchNode == NULL)
            {
                break;
            }

            eNodeAdditionResult =
            DP12TOPOLOGY_AddBranch(pstDP12Topology, pstParentBranchNode, pstNewBranchNode, pstBranchDispDataArr->stBranchData[ulCount].stBranchNodeDesc.ucUpStrmBranchOutPort,
                                   pstBranchDispDataArr->stBranchData[ulCount].stBranchNodeDesc.ucThisBranchInputPort, FALSE);

            if (eNODE_ADD_SUCCESS != eNodeAdditionResult)
            {
                break;
            }

            // Add this new branch to our temp branch node array
            pstTempBranchNodeArray[ulCount] = pstNewBranchNode;
            ulCurrentBranchCount++;
        }

        if (eNODE_ADD_SUCCESS != eNodeAdditionResult)
        {
            break;
        }

        for (ulCount = 0; ulCount < pstBranchDispDataArr->uiNumDisplays; ulCount++)
        {

            pstDisplayNode = DP12TOPOLOGY_CreateDisplayNode(
            pstDP12Topology, eSSTSINKORSTREAMSINK, pstBranchDispDataArr->stDisplayData[ulCount].stDisplayNodeDesc.ucTotalInputPorts,
            pstBranchDispDataArr->stDisplayData[ulCount].stDisplayNodeDesc.usTotalAvailablePBN, pstBranchDispDataArr->stDisplayData[ulCount].stDisplayNodeDesc.uiMaxLinkRate,
            pstBranchDispDataArr->stDisplayData[ulCount].stDisplayNodeDesc.uiMaxLaneCount, pstBranchDispDataArr->stDisplayData[ulCount].stDisplayNodeDesc.uiRemoteI2ReadDelay,
            pstBranchDispDataArr->stDisplayData[ulCount].stDisplayNodeDesc.uiRemoteI2WriteDelay,
            pstBranchDispDataArr->stDisplayData[ulCount].stDisplayNodeDesc.uiRemoteDPCDReadDelay,
            pstBranchDispDataArr->stDisplayData[ulCount].stDisplayNodeDesc.uiRemoteDPCDWriteDelay, pstBranchDispDataArr->stDisplayData[ulCount].ucDPCDName,
            pstBranchDispDataArr->stDisplayData[ulCount].ucDisplayName);

            if (pstDisplayNode == NULL)
            {
                break;
            }

            if (pstBranchDispDataArr->stDisplayData[ulCount].uiParentBranchIndex == PARENT_INDEX_SUB_TOPOLOGY)
            {
                *pstInOutNode = pstDisplayNode;
                break;
            }

            // Parent Branch Index should always be less than the total number of branches we have till now
            if (pstBranchDispDataArr->stDisplayData[ulCount].uiParentBranchIndex >= ulCurrentBranchCount)
            {
                break;
            }

            pstParentBranchNode = pstTempBranchNodeArray[pstBranchDispDataArr->stDisplayData[ulCount].uiParentBranchIndex];

            if (pstParentBranchNode == NULL)
            {
                break;
            }

            eNodeAdditionResult =
            DP12TOPOLOGY_AddDisplay(pstDP12Topology, pstParentBranchNode, pstDisplayNode, pstBranchDispDataArr->stDisplayData[ulCount].stDisplayNodeDesc.ucUpStrmBranchOutPort,
                                    pstBranchDispDataArr->stDisplayData[ulCount].stDisplayNodeDesc.ucThisDisplayInputPort);

            if (eNODE_ADD_SUCCESS != eNodeAdditionResult)
            {
                break;
            }
        }

        if (eNODE_ADD_SUCCESS != eNodeAdditionResult)
        {
            break;
        }

        bRet = TRUE;

    } while (FALSE);

    if (pstTempBranchNodeArray)
    {
        pstPortingObj->pfnFreeMem(pstTempBranchNodeArray);
    }

    return bRet;
}

BOOLEAN DPHANDLERS_ReadDPCD(PRX_INFO_ARR pstRxInfoArr, PGET_DPCD_ARGS pstReadDPCDArgs, PUCHAR pucReadBuff)
{
    GFXVALSIM_FUNC_ENTRY();
    PDPAUX_INTERFACE pstDPAuxInterface = COMMRXHANDLERS_GetAuxInterfaceFromPortType(pstRxInfoArr, pstReadDPCDArgs->ulPortNum);
    PDP12_TOPOLOGY   pstDP12Topology   = NULL;
    DP_TOPOLOGY_TYPE eTopologyType     = eInvalidTopology;
    BOOLEAN          bRet              = FALSE;

    do
    {
        if (pstDPAuxInterface == NULL)
        {
            break;
        }

        if (pstReadDPCDArgs->bNative)
        {
            bRet = AUXINTERFACE_ReadDPCDAppWorld(pstDPAuxInterface, pucReadBuff, pstReadDPCDArgs->ulDPCDAddress, pstReadDPCDArgs->ulReadLength);
        }
        else if (pstReadDPCDArgs->stRAD.ucTotalLinkCount > 0)
        {
            // MST case
            eTopologyType = AUXINTERFACE_GetTopologyType(pstDPAuxInterface);

            if (eTopologyType == eDPMST)
            {
                pstDP12Topology = AUXINTERFACE_GetMSTTopologPtr(pstDPAuxInterface);

                if (pstDP12Topology == NULL)
                {
                    // Someone Tried to Set MST EDID data without Initializing the topology object. THIS SHOULD NEVER HAPPEN!
                    break;
                }

                // Call Rad based DPCD accessing function here
                bRet = DP12TOPOLOGY_ReadRemoteDPCDAppWorld(pstDP12Topology, &pstReadDPCDArgs->stRAD, pucReadBuff, pstReadDPCDArgs->ulDPCDAddress, pstReadDPCDArgs->ulReadLength);
            }
        }

        bRet = TRUE;

    } while (FALSE);
    GFXVALSIM_FUNC_EXIT(!bRet);

    return bRet;
}

BOOLEAN DPHANDLERS_WriteDPCD(PRX_INFO_ARR pstRxInfoArr, PSET_DPCD_ARGS pstSetDPCDArgs)
{
    GFXVALSIM_FUNC_ENTRY();

    PDP12_TOPOLOGY   pstDP12Topology   = NULL;
    PUCHAR           pucWriteBuff      = (PUCHAR)(pstSetDPCDArgs + 1);
    DP_TOPOLOGY_TYPE eTopologyType     = eInvalidTopology;
    BOOLEAN          bRet              = FALSE;
    PDPAUX_INTERFACE pstDPAuxInterface = COMMRXHANDLERS_GetAuxInterfaceFromPortType(pstRxInfoArr, pstSetDPCDArgs->ulPortNum);

    do
    {
        if (pstDPAuxInterface == NULL)
        {
            break;
        }

        if (pstSetDPCDArgs->bNative)
        {
            bRet = AUXINTERFACE_WriteDPCDAppWorld(pstDPAuxInterface, pucWriteBuff, pstSetDPCDArgs->ulDPCDAddress, pstSetDPCDArgs->ulWriteLength);
        }
        else if (pstSetDPCDArgs->stRAD.ucTotalLinkCount > 0)
        {
            // MST case
            eTopologyType = AUXINTERFACE_GetTopologyType(pstDPAuxInterface);

            if (eTopologyType == eDPMST)
            {
                pstDP12Topology = AUXINTERFACE_GetMSTTopologPtr(pstDPAuxInterface);

                if (pstDP12Topology == NULL)
                {
                    // Someone Tried to Set MST EDID data without Initializing the topology object. THIS SHOULD NEVER HAPPEN!
                    break;
                }

                // Call Rad based DPCD accessing function here
                bRet = DP12TOPOLOGY_WriteRemoteDPCDAppWorld(pstDP12Topology, &pstSetDPCDArgs->stRAD, pucWriteBuff, pstSetDPCDArgs->ulDPCDAddress, pstSetDPCDArgs->ulWriteLength);
            }
        }

        bRet = TRUE;

    } while (FALSE);
    GFXVALSIM_FUNC_EXIT(!bRet);

    return bRet;
}

BOOLEAN DPHANDLERS_GetMSTTopologyRADArray(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortNum, PBRANCHDISP_RAD_ARRAY pstBranchDispRADArray)
{
    BOOLEAN          bRet              = FALSE;
    PDP12_TOPOLOGY   pstDP12Topology   = NULL;
    PDPAUX_INTERFACE pstDPAuxInterface = COMMRXHANDLERS_GetAuxInterfaceFromPortType(pstRxInfoArr, ePortNum);

    do
    {
        if (pstDPAuxInterface == NULL)
        {
            break;
        }

        if (eDPMST != AUXINTERFACE_GetTopologyType(pstDPAuxInterface))
        {
            break;
        }

        pstDP12Topology = AUXINTERFACE_GetMSTTopologPtr(pstDPAuxInterface);

        if (pstDP12Topology == NULL)
        {
            break;
        }

        memset(pstBranchDispRADArray, 0, sizeof(BRANCHDISP_RAD_ARRAY));

        bRet = DP12TOPOLOGY_GetMSTTopologyRADArray(pstDP12Topology, pstBranchDispRADArray);

    } while (FALSE);

    return bRet;
}

BOOLEAN DPHANDLERS_ExtractCurrentTopologyInArrayFormat(PRX_INFO_ARR pstRxInfoArr, PBRANCHDISP_DATA_ARRAY pstBranchDispDataArray, PORT_TYPE ePortNum)
{
    BOOLEAN          bRet              = FALSE;
    PDP12_TOPOLOGY   pstDP12Topology   = NULL;
    PDPAUX_INTERFACE pstDPAuxInterface = COMMRXHANDLERS_GetAuxInterfaceFromPortType(pstRxInfoArr, ePortNum);

    do
    {
        if (pstDPAuxInterface == NULL)
        {
            break;
        }

        if (eDPMST != AUXINTERFACE_GetTopologyType(pstDPAuxInterface))
        {
            break;
        }

        pstDP12Topology = AUXINTERFACE_GetMSTTopologPtr(pstDPAuxInterface);

        if (pstDP12Topology == NULL)
        {
            break;
        }

        memset(pstBranchDispDataArray, 0, sizeof(BRANCHDISP_DATA_ARRAY));

        // updating the PORT Number
        pstBranchDispDataArray->uiPortNum = ePortNum;
        GFXVALSIM_DBG_MSG("DPHANDLERS_ExtractCurrentTopologyInArrayFormat %d", ePortNum);
        bRet = DP12TOPOLOGY_ExtractCurrentTopologyInArrayFormat(pstDP12Topology, pstBranchDispDataArray);

    } while (FALSE);

    return bRet;
}

BOOLEAN DPHANDLERS_ExecuteConnectionStatusNotify(PRX_INFO_ARR pstRxInfoArr, PVOID pGfxAdapterContext, PDP_SUBTOPOLOGY_ARGS pstCSNArgs)
{
    BOOLEAN          bRet                = FALSE;
    PDP12_TOPOLOGY   pstDP12Topology     = NULL;
    UP_REQUEST_ARGS  stUpRequestArgs     = { 0 };
    PBRANCH_NODE     pstNewNodeToBeAdded = NULL;
    PDPAUX_INTERFACE pstDPAuxInterface   = COMMRXHANDLERS_GetAuxInterfaceFromPortType(pstRxInfoArr, pstCSNArgs->ulPortNum);

    do
    {
        GFXVALSIM_DBG_MSG("Total link count %u", pstCSNArgs->stNodeRAD.ucTotalLinkCount);
        GFXVALSIM_DBG_MSG("Remaining link count %u", pstCSNArgs->stNodeRAD.ucRemainingLinkCount);
        GFXVALSIM_DBG_MSG("Node Rad address %u", pstCSNArgs->stNodeRAD.ucAddress);
        GFXVALSIM_DBG_MSG("Node Rad Size %u", pstCSNArgs->stNodeRAD.ucRadSize);
        GFXVALSIM_DBG_MSG("Port No %lu", pstCSNArgs->ulPortNum);
        GFXVALSIM_DBG_MSG("Attach Detach Status %d", pstCSNArgs->bAttachOrDetach);

        if (pstCSNArgs->stNodeRAD.ucTotalLinkCount == 0)
        {
            break;
        }

        if (pstCSNArgs->bAttachOrDetach && pstCSNArgs->stSubTopology.uiNumBranches == 0 && pstCSNArgs->stSubTopology.uiNumDisplays == 0)
        {
            GFXVALSIM_DBG_MSG("SubTopology has 0 branches and 0 displays for Attach True");
            break;
        }

        if (!memcmp(&pstCSNArgs->stNodeRAD.ucAddress, &stUpRequestArgs.stRAD.ucAddress, MAX_BYTES_RAD))
        {
            // CSN Shouldn't come for Zero RAD, i.e for branch connected to source
            GFXVALSIM_DBG_MSG("Subtopology Address mismatch");
            break;
        }

        // CSN can't come for SST topology
        if (eDPMST != AUXINTERFACE_GetTopologyType(pstDPAuxInterface))
        {
            break;
        }

        pstDP12Topology = AUXINTERFACE_GetMSTTopologPtr(pstDPAuxInterface);

        if (pstDP12Topology == NULL)
        {
            // Someone Tried to Set MST EDID data without Initializing the topology object. THIS SHOULD NEVER HAPPEN!
            break;
        }

        if (pstCSNArgs->bAttachOrDetach)
        {
            DPHANDLERS_CreateDPMSTSubTopology(pstDP12Topology, &pstNewNodeToBeAdded, &pstCSNArgs->stSubTopology);

            if (pstCSNArgs->stSubTopology.uiNumBranches)
            {
                stUpRequestArgs.stCSNArgs.ucNewNodeInputPort = pstCSNArgs->stSubTopology.stBranchData[0].stBranchNodeDesc.ucThisBranchInputPort;
                GFXVALSIM_DBG_MSG("Branch SubTopology Case %u", stUpRequestArgs.stCSNArgs.ucNewNodeInputPort);
            }
            else
            {
                stUpRequestArgs.stCSNArgs.ucNewNodeInputPort = pstCSNArgs->stSubTopology.stDisplayData[0].stDisplayNodeDesc.ucThisDisplayInputPort;
                GFXVALSIM_DBG_MSG("Display SubTopology Case %u", stUpRequestArgs.stCSNArgs.ucNewNodeInputPort);
            }
        }

        stUpRequestArgs.eUpRequestID                 = eMST_CONNECTION_STATUS_NOTIFY;
        stUpRequestArgs.stRAD                        = pstCSNArgs->stNodeRAD;
        stUpRequestArgs.pstGfxAdapterInfo            = pGfxAdapterContext;
        stUpRequestArgs.ulPortNum                    = pstCSNArgs->ulPortNum;
        stUpRequestArgs.stCSNArgs.bAttachOrDetatch   = pstCSNArgs->bAttachOrDetach;
        stUpRequestArgs.stCSNArgs.pvNewNodeToBeAdded = pstNewNodeToBeAdded;

        GFXVALSIM_DBG_MSG("SubTopology Port No %lu", stUpRequestArgs.ulPortNum);
        GFXVALSIM_DBG_MSG("SubTopology Attach Status %d", stUpRequestArgs.stCSNArgs.bAttachOrDetatch);

        bRet = DP12TOPOLOGY_UpRequestHandler(pstDP12Topology, &stUpRequestArgs);

    } while (FALSE);

    return bRet;
}

BOOLEAN DPHANDLERS_AuxDataReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    do
    {
        bRet = AUXINTERFACE_DataRegReadHandler(pstMMIOHandlerInfo->pvCallerPersistedData, ulMMIOOffset, pulReadData);

    } while (FALSE);

    return bRet;
}

BOOLEAN DPHANDLERS_AuxDataWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    do
    {
        bRet = AUXINTERFACE_DataRegWriteHandler(pstMMIOHandlerInfo->pvCallerPersistedData, ulMMIOOffset, ulWriteData);

    } while (FALSE);

    return bRet;
}

BOOLEAN DPHANDLERS_AuxControlReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    do
    {
        bRet = AUXINTERFACE_ControlRegReadHandler(pstMMIOHandlerInfo->pvCallerPersistedData, ulMMIOOffset, pulReadData);

    } while (FALSE);

    return bRet;
}

BOOLEAN DPHANDLERS_AuxControlWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    do
    {
        bRet = AUXINTERFACE_ControlRegWriteHandler(pstMMIOHandlerInfo->pvCallerPersistedData, ulMMIOOffset, ulWriteData);

    } while (FALSE);

    return bRet;
}

BOOLEAN DPHANDLERS_ConfigureDPGfxS3S4PlugUnplugData(PRX_INFO_ARR pstRxInfoArr, PGFXS3S4_PORT_PLUGUNPLUG_DATA pstGfxS3S4PortPlugUnplugData)
{
    BOOLEAN                  bRet                    = TRUE;
    PRX_S3S4_PLUGUNPLUG_DATA pstRxS3S4PlugUnPlugData = COMMRXHANDLERS_GetRxS3S4PlugUnPlugDataPtr(pstRxInfoArr, pstGfxS3S4PortPlugUnplugData->ulPortNum, DP);

    pstRxS3S4PlugUnPlugData->eRxS3S4PlugRequest                   = pstGfxS3S4PortPlugUnplugData->eSinkPlugReq;
    pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.bPlugUnplugAtSource = pstGfxS3S4PortPlugUnplugData->stS3S4DPPlugUnplugData.bPlugOrUnPlugAtSource;
    pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.eTopologyType       = pstGfxS3S4PortPlugUnplugData->stS3S4DPPlugUnplugData.eTopologyAfterResume;

    if (pstGfxS3S4PortPlugUnplugData->stS3S4DPPlugUnplugData.bPlugOrUnPlugAtSource && pstGfxS3S4PortPlugUnplugData->stS3S4DPPlugUnplugData.eTopologyAfterResume == eDPMST)
    {

        pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pvNewDP12Topology = DP12TOPOLOGY_TopologyObjectInit();

        if (pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pvNewDP12Topology == NULL)
        {
            bRet = FALSE;
        }
    }

    return bRet;
}

BOOLEAN DPHANDLERS_HandleGfxPowerNotification(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType, PRX_S3S4_PLUGUNPLUG_DATA pstRxS3S4PlugUnPlugData, DEVICE_POWER_STATE eGfxPowerState,
                                              POWER_ACTION eActionType, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN           bRet              = FALSE;
    PDP12_TOPOLOGY    pstDP12Topology   = 0;
    PDPAUX_INTERFACE  pstDPAuxInterface = COMMRXHANDLERS_GetAuxInterfaceFromPortType(pstRxInfoArr, ePortType);
    PPORTINGLAYER_OBJ pstPortingObj     = GetPortingObj();

    if (eGfxPowerState != PowerDeviceD0)
    {
        if (pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.bPlugUnplugAtSource)
        {
            if (pstRxS3S4PlugUnPlugData->eRxS3S4PlugRequest == ePlugSink || pstRxS3S4PlugUnPlugData->eRxS3S4PlugRequest == eUnPlugOldPlugNew)
            {
                pstDPAuxInterface->bSinkPluggedState = TRUE;
                // Turn off Live State here First:
                bRet = COMMONMMIOHANDLERS_SetLiveStateForPort(pstRxInfoArr->pstMMIOInterface, ePortType, FALSE, PortConnectorInfo);

                if (bRet)
                {
                    bRet = AUXINTERFACE_GfxS3S4UpdateTopology(
                    pstDPAuxInterface, pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.eTopologyType, pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pvNewDP12Topology,
                    pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pucBranch0DPCDBuff, pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.ulBranch0DPCDSize,
                    pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pucNewSSTEDIDBuff, pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.ulNewSSTEDIDSize,
                    pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pucNewSSTDPCDBuff, pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.ulNewSSTDPCDSize,
                    pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pstNewSSTDPCDConfigData);

                    // turn on live state here again if it was turned on:
                    bRet = COMMONMMIOHANDLERS_SetLiveStateForPort(pstRxInfoArr->pstMMIOInterface, ePortType, TRUE, PortConnectorInfo);
                }
            }
            else if (pstRxS3S4PlugUnPlugData->eRxS3S4PlugRequest == eUnplugSink)
            {
                pstDPAuxInterface->bSinkPluggedState = FALSE;
                bRet                                 = COMMONMMIOHANDLERS_SetLiveStateForPort(pstRxInfoArr->pstMMIOInterface, ePortType, FALSE, PortConnectorInfo);
            }
        }
        else
        {
            if (eDPMST == AUXINTERFACE_GetTopologyType(pstDPAuxInterface))
            {
                pstDP12Topology = AUXINTERFACE_GetMSTTopologPtr(pstDPAuxInterface);

                if (pstDP12Topology)
                {
                    if (pstRxS3S4PlugUnPlugData->eRxS3S4PlugRequest == ePlugSink || pstRxS3S4PlugUnPlugData->eRxS3S4PlugRequest == eUnPlugOldPlugNew ||
                        pstRxS3S4PlugUnPlugData->eRxS3S4PlugRequest == eUnplugSink)
                    {

                        bRet = DP12TOPOLOGY_AddOrDeleteSubTopology(
                        pstDP12Topology, (pstRxS3S4PlugUnPlugData->eRxS3S4PlugRequest == eUnplugSink ? FALSE : TRUE),
                        (pstRxS3S4PlugUnPlugData->eRxS3S4PlugRequest == eUnPlugOldPlugNew ?
                         TRUE :
                         FALSE), // If we want to force attach the new node even though the branch's outport for a given RAD has already something attached on it
                        // Detach Parameters:
                        pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.stRADInfo.pvRADNode,
                        // Attach Parameters:
                        pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.stRADInfo.pstBranchNode, pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pvNewSubTopologyNode,
                        pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.stRADInfo.ucPortNum, pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.ulNewNodeInputPort);
                    }
                }
            }
        }

        // Since we have finally processed the S3/S4 data so cleanup and reset the cache
        if (pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pucNewSSTEDIDBuff)
        {
            pstPortingObj->pfnFreeMem(pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pucNewSSTEDIDBuff);
        }

        if (pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pucNewSSTDPCDBuff)
        {
            pstPortingObj->pfnFreeMem(pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pucNewSSTDPCDBuff);
        }

        if (pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pstNewSSTDPCDConfigData)
        {
            pstPortingObj->pfnFreeMem(pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pstNewSSTDPCDConfigData);
        }

        memset(pstRxS3S4PlugUnPlugData, 0, sizeof(RX_S3S4_PLUGUNPLUG_DATA));
    }

    return bRet;
}

BOOLEAN DPHANDLERS_SetEDIDDataForS3S4Cycle(PRX_INFO_ARR pstRxInfoArr, PFILE_DATA pstEdidData)
{
    BOOLEAN                  bRet                    = FALSE;
    PDP12_TOPOLOGY           pstDP12Topology         = NULL;
    PUCHAR                   pucIncomingEDIDBuff     = NULL;
    PRX_S3S4_PLUGUNPLUG_DATA pstRxS3S4PlugUnPlugData = COMMRXHANDLERS_GetRxS3S4PlugUnPlugDataPtr(pstRxInfoArr, pstEdidData->uiPortNum, DP);
    PDPAUX_INTERFACE         pstDPAuxInterface       = COMMRXHANDLERS_GetAuxInterfaceFromPortType(pstRxInfoArr, pstEdidData->uiPortNum);
    PPORTINGLAYER_OBJ        pstPortingObj           = GetPortingObj();

    do
    {
        if (pstRxS3S4PlugUnPlugData == NULL || NULL == pstDPAuxInterface)
        {
            break;
        }

        if (pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.eTopologyType == eDPMST)
        {
            pstDP12Topology = pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pvNewDP12Topology;
            bRet            = DP12TOPOLOGY_SetEDIDData(pstDP12Topology, pstEdidData->ucNodeName, pstEdidData->uiDataSize, (PUCHAR)(((PUCHAR)pstEdidData) + sizeof(FILE_DATA)));
        }
        else
        {
            pucIncomingEDIDBuff                                         = (PUCHAR)(((PUCHAR)pstEdidData) + sizeof(FILE_DATA));
            pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pucNewSSTEDIDBuff = pstPortingObj->pfnAllocateMem(pstEdidData->uiDataSize, TRUE);
            memcpy_s(pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pucNewSSTEDIDBuff, pstEdidData->uiDataSize, pucIncomingEDIDBuff, pstEdidData->uiDataSize);
            pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.ulNewSSTEDIDSize = pstEdidData->uiDataSize;
            bRet                                                       = TRUE;
        }

    } while (FALSE);

    return bRet;
}

BOOLEAN DPHANDLERS_SetDPCDDataForS3S4Cycle(PRX_INFO_ARR pstRxInfoArr, PFILE_DATA pstDPCDData)
{
    GFXVALSIM_FUNC_ENTRY();

    BOOLEAN                  bRet                    = FALSE;
    PDP12_TOPOLOGY           pstDP12Topology         = NULL;
    PUCHAR                   pucIncomingDPCDBuff     = NULL;
    PDPCD_CONFIG_DATA        pstDPCDConfigData       = NULL;
    PRX_S3S4_PLUGUNPLUG_DATA pstRxS3S4PlugUnPlugData = COMMRXHANDLERS_GetRxS3S4PlugUnPlugDataPtr(pstRxInfoArr, pstDPCDData->uiPortNum, DP);
    PDPAUX_INTERFACE         pstDPAuxInterface       = COMMRXHANDLERS_GetAuxInterfaceFromPortType(pstRxInfoArr, pstDPCDData->uiPortNum);
    PPORTINGLAYER_OBJ        pstPortingObj           = GetPortingObj();

    do
    {
        if (pstDPAuxInterface == NULL)
        {
            break;
        }

        DPHANDLERS_ModifyDPCDBasedonStaticList(pstDPCDData);

        if (pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.eTopologyType == eDPMST)
        {
            pstDP12Topology = pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pvNewDP12Topology;

            if (pstDP12Topology == NULL)
            {
                // Someone Tried to Set MST EDID data without Initializing the topology object. THIS SHOULD NEVER HAPPEN!
                break;
            }

            //(PUCHAR)(pstDPCDData + sizeof(FILE_DATA)) because Raw DPCD data follows after the EDID_DPCD_DATA members
            // as per our agreement with the APP world for this IOCTL with the app world
            bRet = DP12TOPOLOGY_SetDPCDData(pstDP12Topology, pstDPCDData->ucNodeName, pstDPCDData->uiDataSize, (PUCHAR)(((PUCHAR)pstDPCDData) + sizeof(FILE_DATA)));
        }
        else
        {
            pucIncomingDPCDBuff                                         = (PUCHAR)(((PUCHAR)pstDPCDData) + sizeof(FILE_DATA));
            pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pucNewSSTDPCDBuff = pstPortingObj->pfnAllocateMem(pstDPCDData->uiDataSize, TRUE);
            memcpy_s(pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pucNewSSTDPCDBuff, pstDPCDData->uiDataSize, pucIncomingDPCDBuff, pstDPCDData->uiDataSize);
            pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.ulNewSSTDPCDSize = pstDPCDData->uiDataSize;
            bRet                                                       = TRUE;
        }

        /*********************************temp code*****************************************/
        // temporary code to fill DPCD model data to PASS link training in first two transactions itself.
        // Although Plug lib in python is sending this data always, some userspace consumers (like DP MST testcases) are not sending the DPCD model data.
        // TODO: Remove this code portion once all userspace consumers start sending DPCD  model data properly.
        if (pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.eTopologyType == eDPMST)
        {
            pstDP12Topology = pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pvNewDP12Topology;

            if (pstDP12Topology == NULL)
            {
                // Someone Tried to Set MST EDID data without Initializing the topology object. THIS SHOULD NEVER HAPPEN!
                break;
            }
            pstDPCDConfigData = &(pstDP12Topology->stDPCDConfigData);
        }
        else
        {
            pstDPCDConfigData = pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pstNewSSTDPCDConfigData;
        }

        // DPCD model data should have been set before setting DPCD data (through IOCTLs)
        // TransactionCount == 0 indicates that, no data has been sent from userspace for DPCD model data
        if (pstDPCDConfigData == NULL || pstDPCDConfigData->stDPCDModelData.ucTransactionCount == 0)
        {
            PDP_DPCD_MODEL_DATA pstDpDPCDModelData;
            pstDpDPCDModelData = (PDP_DPCD_MODEL_DATA)pstPortingObj->pfnAllocateMem(sizeof(DP_DPCD_MODEL_DATA), TRUE);
            DPHANDLERS_FillDPCDStaticUltData(pstDpDPCDModelData, pstDPCDData->uiPortNum, pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.eTopologyType);

            DPHANDLERS_SetDPCDModelDataForS3S4Cycle(pstRxInfoArr, pstDpDPCDModelData);
            pstPortingObj->pfnFreeMem(pstDpDPCDModelData);
        }
        /***************************************************************************************/

    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(!bRet);

    return bRet;
}

// So the app world parses the Topology descripton from the XML and packs the branch and display information in a structure using the
// discussed algo and sends it to driver. Here, in this function, we use that info to finally build the topopology
BOOLEAN DPHANDLERS_SetDPMSTTopologyForS3S4Cycle(PRX_INFO_ARR pstRxInfoArr, PBRANCHDISP_DATA_ARRAY pstBranchDispDataArr)
{
    BOOLEAN bRet = FALSE;

    PDP12_TOPOLOGY pstDP12Topology  = NULL;
    PBRANCH_NODE   pstNewBranchNode = NULL;

    PBRANCHDISP_DPCD pstBranchDispDCPD = NULL;

    PUCHAR pucSharedDPCDBuff;

    NODE_ADD_ERRROR_CODES eNodeAdditionResult = eGENERIC_ERROR;

    PRX_S3S4_PLUGUNPLUG_DATA pstRxS3S4PlugUnPlugData = COMMRXHANDLERS_GetRxS3S4PlugUnPlugDataPtr(pstRxInfoArr, pstBranchDispDataArr->uiPortNum, DP);
    PDPAUX_INTERFACE         pstDPAuxInterface       = COMMRXHANDLERS_GetAuxInterfaceFromPortType(pstRxInfoArr, pstBranchDispDataArr->uiPortNum);

    do
    {
        if (pstDPAuxInterface == NULL || eDPMST != pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.eTopologyType || pstBranchDispDataArr->uiNumBranches == 0)
        {
            break;
        }

        pstDP12Topology = pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pvNewDP12Topology;

        if (pstDP12Topology == NULL)
        {
            // Someone Tried to Set MST EDID data without Initializing the topology object. THIS SHOULD NEVER HAPPEN!
            break;
        }

        // Lets take First Branch Data: As per our Agreement with the app world, this should be the Branch connected to source with Parent Index 0xFFFFFFFF
        if (pstBranchDispDataArr->stBranchData[0].uiParentBranchIndex != PARENT_INDEX_BRANCH_CONNECTED_TO_SRC)
        {
            break;
        }

        // This is the branch connected to the source
        // Passing Null for what DPCD we want for this Branch. We'd link this branch's DPCD directly to the AUX_INTERFACE object that handles native Aux's
        pstNewBranchNode = DP12TOPOLOGY_CreateBranchNode(
        pstDP12Topology, eMSTBRANCHDEVICE, pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.ucTotalInputPorts,
        pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.ucTotalPhysicalPorts, pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.ucTotalVirtualPorts,
        pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.uiMaxLinkRate, pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.uiMaxLaneCount,
        pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.uiBranchReplyDelay, pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.usTotalAvailablePBN,
        pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.uiLinkAddressDelay, pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.uiRemoteI2ReadDelay,
        pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.uiRemoteI2WriteDelay, pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.uiRemoteDPCDReadDelay,
        pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.uiRemoteDPCDWriteDelay, pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.uiEPRDelay,
        pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.uiAllocatePayloadDelay, pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.uiClearPayLoadDelay, NULL);

        if (pstNewBranchNode == NULL)
        {
            break;
        }

        pstBranchDispDCPD = DP12TOPOLOGY_GetNodeDPCD(pstDP12Topology, pstBranchDispDataArr->stBranchData[0].ucDPCDName);

        if (pstBranchDispDCPD == NULL || pstBranchDispDCPD->ulDPCDBuffSize == 0)
        {
            break;
        }

        pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pucBranch0DPCDBuff = pstBranchDispDCPD->pucDPCDBuff;
        pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.ulBranch0DPCDSize  = pstBranchDispDCPD->ulDPCDBuffSize;

        //   pucSharedDPCDBuff = AUXINTERFACE_GetDwnStrmDPCDMap(pstDPAuxInterface);
        pucSharedDPCDBuff = AUXINTERFACE_SetDwnStrmDPCDMap(pstDPAuxInterface, pstBranchDispDCPD->pucDPCDBuff, pstBranchDispDCPD->ulDPCDBuffSize);

        if (NULL == pucSharedDPCDBuff)
        {
            break;
        }

        //!!!Branch directly connected to Source will share the DPCD that's stored in AuxInterface
        eNodeAdditionResult = DP12TOPOLOGY_AddFirstBranch(pstDP12Topology, pstNewBranchNode, pstBranchDispDataArr->stBranchData[0].stBranchNodeDesc.ucThisBranchInputPort,
                                                          pucSharedDPCDBuff, pstBranchDispDCPD->ucDPCDName, pstBranchDispDCPD->ulDPCDBuffSize);

        if (eNODE_ADD_SUCCESS != eNodeAdditionResult)
        {
            break;
        }

        bRet = DPHANDLERS_CreateDPMSTSubTopology(pstDP12Topology, &pstNewBranchNode, pstBranchDispDataArr);

    } while (FALSE);

    return bRet;
}

BOOLEAN DPHANDLERS_AddOrRemoveSubtopologyForS3S4Cycle(PRX_INFO_ARR pstRxInfoArr, PDP_SUBTOPOLOGY_ARGS pstSubTopologyArgs)
{
    BOOLEAN                  bRet                    = FALSE;
    PDP12_TOPOLOGY           pstDP12Topology         = NULL;
    RAD_NODE_INFO            stNodeRADInfo           = { 0 };
    PBRANCH_NODE             pstNewNodeToBeAdded     = NULL;
    PRX_S3S4_PLUGUNPLUG_DATA pstRxS3S4PlugUnPlugData = COMMRXHANDLERS_GetRxS3S4PlugUnPlugDataPtr(pstRxInfoArr, pstSubTopologyArgs->ulPortNum, DP);
    PDPAUX_INTERFACE         pstDPAuxInterface       = COMMRXHANDLERS_GetAuxInterfaceFromPortType(pstRxInfoArr, pstSubTopologyArgs->ulPortNum);

    do
    {
        if (pstSubTopologyArgs->stNodeRAD.ucTotalLinkCount == 0)
        {
            break;
        }

        if ((pstRxS3S4PlugUnPlugData->eRxS3S4PlugRequest == ePlugSink || pstRxS3S4PlugUnPlugData->eRxS3S4PlugRequest == eUnPlugOldPlugNew) &&
            pstSubTopologyArgs->stSubTopology.uiNumBranches == 0 && pstSubTopologyArgs->stSubTopology.uiNumDisplays == 0)
        {
            break;
        }

        if (pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.eTopologyType != eDPMST && pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.bPlugUnplugAtSource != FALSE)
        {
            break;
        }

        if (pstSubTopologyArgs->stNodeRAD.ucTotalLinkCount > 0)
        {
            if (pstDPAuxInterface)
            {
                if (eDPMST == AUXINTERFACE_GetTopologyType(pstDPAuxInterface))
                {
                    pstDP12Topology = AUXINTERFACE_GetMSTTopologPtr(pstDPAuxInterface);

                    if (pstDP12Topology)
                    {
                        stNodeRADInfo                                       = DP12TOPOLOGY_GetNodeForAGivenRAD(pstDP12Topology, &pstSubTopologyArgs->stNodeRAD);
                        pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.stRADInfo = stNodeRADInfo;
                    }
                }
            }
        }

        if (pstRxS3S4PlugUnPlugData->eRxS3S4PlugRequest == ePlugSink || pstRxS3S4PlugUnPlugData->eRxS3S4PlugRequest == eUnPlugOldPlugNew)
        {
            DPHANDLERS_CreateDPMSTSubTopology(pstDP12Topology, &pstNewNodeToBeAdded, &pstSubTopologyArgs->stSubTopology);

            if (pstSubTopologyArgs->stSubTopology.uiNumBranches)
            {
                pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.ulNewNodeInputPort = pstSubTopologyArgs->stSubTopology.stBranchData[0].stBranchNodeDesc.ucThisBranchInputPort;
            }
            else
            {
                pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.ulNewNodeInputPort = pstSubTopologyArgs->stSubTopology.stDisplayData[0].stDisplayNodeDesc.ucThisDisplayInputPort;
            }
        }

        pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pvNewSubTopologyNode = pstNewNodeToBeAdded;

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

// THis function doesn't modify the dynamic DPCDs beyond the pstDPCDData->uiDataSize range which are
// implemented using BACKUP_DPCD_BUFF_ARR arrBackupDPCDBuff member of AuxInterface
void DPHANDLERS_ModifyDPCDBasedonStaticList(PFILE_DATA pstDPCDData)
{
    ULONG  ulCount     = 0;
    PUCHAR pucDPCDBuff = (PUCHAR)(((PUCHAR)pstDPCDData) + sizeof(FILE_DATA));
    ULONG  ulListSize  = sizeof(staticDPCDAddrValPair) / sizeof(DPCD_ADDR_VALUE_PAIR);

    for (ulCount = 0; ulCount < ulListSize; ulCount++)
    {
        if (staticDPCDAddrValPair[ulCount].ulDPCDAddr < pstDPCDData->uiDataSize)
        {
            *(pucDPCDBuff + staticDPCDAddrValPair[ulCount].ulDPCDAddr) = staticDPCDAddrValPair[ulCount].ucDPCDVal;
        }
    }
}

BOOLEAN DPHANDLERS_CleanUp(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType)
{

    PDPAUX_INTERFACE pstDPAuxInterface = COMMRXHANDLERS_GetAuxInterfaceFromPortType(pstRxInfoArr, ePortType);

    if (pstDPAuxInterface)
    {
        AUXINTERFACE_CleanUp(pstDPAuxInterface);

        COMMRXHANDLERS_FreeAuxInterfaceForPort(pstRxInfoArr, ePortType);
    }

    return TRUE;
}

BOOLEAN DPHANDLERS_SetPanelDpcd(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType, UINT16 Offset, UINT8 Value)
{
    GFXVALSIM_FUNC_ENTRY();
    BOOLEAN          bRet              = FALSE;
    DP_TOPOLOGY_TYPE eTopologyType     = eInvalidTopology;
    PDPAUX_INTERFACE pstDPAuxInterface = COMMRXHANDLERS_GetAuxInterfaceFromPortType(pstRxInfoArr, ePortType);

    do
    {
        if (NULL == pstDPAuxInterface)
        {
            break;
        }
        eTopologyType = AUXINTERFACE_GetTopologyType(pstDPAuxInterface);
        if (eTopologyType == eDPSST)
        {
            // Update the Panel Dpcd buffer
            if (pstDPAuxInterface->pucDownStreamDPCDBuff)
            {
                *(&pstDPAuxInterface->pucDownStreamDPCDBuff[Offset]) = Value;
                LOG_VALSIM_DPCD(Offset, pstDPAuxInterface->pucDownStreamDPCDBuff[Offset], SUCCESS);
                bRet = TRUE;
            }
            else
            {
                LOG_VALSIM_DPCD(Offset, pstDPAuxInterface->pucDownStreamDPCDBuff[Offset], INVALID_OFFSET);
            }
        }
        else
        {
            LOG_VALSIM_DPCD(Offset, pstDPAuxInterface->pucDownStreamDPCDBuff[Offset], INVALID_TOPOLOGY);
        }
    } while (FALSE);
    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}