#ifndef __MSTTOPOLOGY_H__
#define __MSTTOPOLOGY_H__

#include <guiddef.h>
#include "SidebandUtil.h"
#include "SidebandMessageHandlers.h"
#include "DPCDs.h"

#define MAX_PORTS_PER_BRANCH 15u
#define MAX_OUTPUT_PORTS 14u // There must be atleast one Input port?
#define MAX_PHYSICAL_OUT_PORTS 7
#define MAX_VIRTUAL_OUT_PORTS 7
#define MAX_STREAMSINK_PER_DISPLAY 2
#define MAX_POSSIBLE_STREAMS 3 // = MAX_PIPES

#define MAX_RAD_LENGTH 16

// Sideband related
#define SIDEBANDMSG_BUFFER_SIZE 0x1FF // as per DP1.3 Spec

#define LOOKASIDE_INITIAL_COUNT 50
#define MAX_LOOKASIDE_NODE_COUNT 500
#define LOOKASIDE_EXPAND_FACTOR 5

#define INDEX_BUFF_1 0
#define INDEX_BUFF_2 1
#define NAK_REPLY_READY_INDEX 2
#define THREAD_KILL_EVENT_INDEX 3
#define MAX_NON_DOWNPORTS_EVENTS 4 // This number is 4 to account for 1. INDEX_BUFF_1, 2. INDEX_BUFF_2, 3. NAK_REPLY_READY_INDEX and 4. THREAD_KILL_EVENT_INDEX

// DP Link Clock related macros
#define DP_LINKBW_1_62_GBPS 0x6
#define DP_LINKBW_2_16_GBPS 0x8
#define DP_LINKBW_2_43_GBPS 0x9
#define DP_LINKBW_2_7_GBPS 0xa
#define DP_LINKBW_3_24_GBPS 0xc
#define DP_LINKBW_4_32_GBPS 0x10
#define DP_LINKBW_5_4_GBPS 0x14
#define DP_LINKBW_8_1_GBPS 0x1E
#define DP_LINKBW_UNDEFINED ((ULONG)-1)

#define NUM_SLOTS_PER_MTP 64

typedef enum _DWNREQBUFF_SETSTATE
{

    eReturnToFreePool = 0,
    eBuffInUse        = 1

} DWNREQBUFF_SETSTATE;

typedef struct _MST_DWNREQUEST_BUFF_INFO
{

    BOOLEAN                 bIsBuffInUse;
    UCHAR                   ucThisBuffIndex;
    UCHAR                   ucCurrRequestID;
    DP_EVENT                stBuffEvent;
    SBM_CURRENT_HEADER_INFO stHeaderInfo;
    PUCHAR                  puchBuffPtr;
    ULONG                   ulCurrWriteLength;
    ULONG                   ulFinalReplySize;

} MST_DWNREQUEST_BUFF_INFO, *PMST_DWNREQUEST_BUFF_INFO;

typedef struct _MST_DWNREPLY_BUFF_INFO
{
    ULONG  ulTotalReplySize;
    PUCHAR puchBuffPtr;

} MST_DWNREPLY_BUFF_INFO, *PMST_DWNREPLY_BUFF_INFO;

typedef struct _MST_UPREQUEST_BUFF_INFO
{
    UCHAR  ucRequestID;
    ULONG  ulTotalUpReqSize;
    PUCHAR puchUpReqBuffPtr;

} MST_UPREQUEST_BUFF_INFO, *PMST_UPREQUEST_BUFF_INFO;

typedef struct _MST_UPREPLY_BUFF_INFO
{
    SBM_CURRENT_HEADER_INFO stHeaderInfo;
    ULONG                   ulCurrWriteLength;
    ULONG                   ulTotalUpReplySize;
    PUCHAR                  puchBuffPtr;

} MST_UPREPLY_BUFF_INFO, *PMST_UPREPLY_BUFF_INFO;

typedef struct _MST_DOWN_STREAM_PORT_EVENTS
{
    ULONG    ulEventInUseCount;
    UCHAR    ucPortMappingList[MAX_PORTS_PER_BRANCH];
    DP_EVENT stDownReplyEventList[MAX_NON_DOWNPORTS_EVENTS + MAX_PORTS_PER_BRANCH];

} MST_DOWN_STREAM_PORT_EVENTS, *PMST_DOWN_STREAM_PORT_EVENTS;

typedef struct _MST_NAK_REPLY_INFO
{
    DP_LIST_ENTRY      DPListEntry;
    BOOLEAN            bIsNak;
    UCHAR              ucSeqNum;
    UCHAR              ucRequestID;
    GUID *             pGuid;
    MST_REASON_FOR_NAK eReason;
    UCHAR              ucNakData;

} MST_NAK_REPLY_INFO, *PMST_NAK_REPLY_INFO;

typedef enum _NODE_TYPE
{
    eBRANCH = 0,
    eDISPLAY,
    eDPSource

} NODE_TYPE,
*PNODE_TYPE;

typedef enum _MST_PEER_DEVICE_TYPE
{
    eINVALIDDEVICETYPE       = 0,
    eSOURCEORSSTBRANCHDEVICE = 1,
    eMSTBRANCHDEVICE         = 2,
    eSSTSINKORSTREAMSINK     = 3,
    eDP2LEGACYCONVERTER      = 4,
    eDP2WIRELESSCONVERTER    = 5

} MST_PEER_DEVICE_TYPE;

// Calculating these values as per 63 time slots, excluding one time slot used for MTP header. Is that correct?
// Using Table 2-61 in DP spec
typedef enum _PBN_AVAILABLE
{
    eRBR_1LANE  = 189,
    eRBR_2LANE  = 378,
    eRBR_4LANE  = 576,
    eHBR_1LANE  = 315,
    eHBR_2LANE  = 630,
    eHBR_4LANE  = 1260,
    eHBR2_1LANE = 630,
    eHBR2_2LANE = 1260,
    eHBR2_4LANE = 2520,

} PBN_AVAILABLE,
*PPBN_AVAILABLE;

// Usually port number should be enough to find out port type, but still
typedef enum _OUT_PORT_TYPE
{
    eVirtualOutPort = 0,
    ePhysicalOutPort

} OUT_PORT_TYPE;

typedef struct _OUTPORT_ENTRY
{
    UCHAR                ucOutPortNumber;
    BOOLEAN              bPortConnectedStatus;         // Something connected to this Port
    BOOLEAN              bConnectedDeviceMsgCapStatus; // Connected device is a branc or a display : MsgCapStatus == TRUE? Branch: Display
    UCHAR                ucConnectedDevicePortNumber;
    MST_PEER_DEVICE_TYPE stConnectedDevicePeerType;
    NODE_TYPE            eConnectedDeviceNodeType;
    PVOID                pvConnectedDeviceNodePointer;
    USHORT               usAllocatedPBN;
    UCHAR                ucStreamID;
    MST_RELATIVEADDRESS  stStreamRAD; // i.e RAD of the virtual channel this Node onwards
    BOOLEAN              bPostUpdateDownStreamTable;

} OUTPORT_ENTRY, *POUTPORT_ENTRY;

typedef struct _INPUTPORT_ENTRY
{
    UCHAR                ucInputPortNumber;
    UCHAR                ucUpStreamPortNumber;
    BOOLEAN              bPortConnectedStatus;
    MST_PEER_DEVICE_TYPE stUpStreamDevicePeerType;
    NODE_TYPE            eUpStreamNodeType;
    PVOID                pvUpStreamNodePointer;
    ULONG                ulTrainedLinkPBN;

} INPUTPORT_ENTRY, *PINPUTPORT_ENTRY;

typedef struct _EDID_I2C_DATA
{
    UCHAR ucLastWriteAddress;
    UCHAR ucLastSegmentPtr;
    UCHAR ucBlockByteOffset;
    UCHAR ucLastReadLength;

} EDID_I2C_DATA, *PEDID_I2C_DATA;

typedef struct _DISPLAY_EDID
{
    UCHAR  ucDisplayName[MAX_NODE_NAME_SIZE];
    ULONG  ulNumEDIDBlocks;
    PUCHAR pucEDIDBlocks[MAX_NUM_EDID_BLOCKS];

} DISPLAY_EDID, *PDISPLAY_EDID;

typedef struct _MST_DISPLAY_EDID_ARRAY
{
    ULONG        ulNumEDIDTypes;
    DISPLAY_EDID stMSTDispEDID[MAX_NUM_DISPLAYS];

} MST_DISPLAY_EDID_ARRAY, *PMST_DISPLAY_EDID_ARRAY;

typedef struct _BRANCHDISP_DPCD
{
    UCHAR  ucDPCDName[MAX_NODE_NAME_SIZE];
    ULONG  ulDPCDBuffSize;
    PUCHAR pucDPCDBuff;

} BRANCHDISP_DPCD, *PBRANCHDISP_DPCD;

typedef struct _MST_BRANCHDISP_DPCD_ARRAY
{
    ULONG           ulNumDPCDTypes;
    BRANCHDISP_DPCD stMSTBranchDispDPCD[MAX_NUM_DISPLAYS];

} MST_BRANCHDISP_DPCD_ARRAY, *PMST_BRANCHDISP_DPCD_ARRAY;

typedef struct _PAYLOADTABLE_ENTRY
{
    UCHAR ucStreamID;  // StreamId =  ucChildEncoderIndex + 1 as  ucChildEncoderIndex will start from 0 to (MAX_MULTISTREAMS_SUPPORTED - 1)
    UCHAR ucStartSlot; // Ranges from 1 - 63
    UCHAR ucNumOfSlots;
    // USHORT usPBNAllocated; //in PBN
    // MST_RELATIVEADDRESS stFullRADFromSrc; //This is basically used only by first Branch meaningfully through ClearPayload table

} PAYLOADTABLE_ENTRY, *PPAYLOADTABLE_ENTRY;

typedef struct _PAYLOADTABLE_STATE
{
    ULONG              ulNumStreamsSlotsAllocated;
    UCHAR              ucTotalNumSlotsInUse;
    UCHAR              ucReserved1;
    UCHAR              ucReserved2;
    UCHAR              ucReserved3;
    PAYLOADTABLE_ENTRY stPTEntryArray[MAX_OUTPUT_PORTS];

} PAYLOADTABLE_STATE, *PPAYLOADTABLE_STATE;

typedef struct _BRANCH_NODE
{
    // Make sure eNodeType always remains the first member or it will break the code
    NODE_TYPE            eNodeType;
    DPCD_REV             eDPCDRev;
    GUID                 uidBranchGUID;
    BOOLEAN              bIsBranchConnectedToSrc;
    UCHAR                ucTotalInputPorts;
    UCHAR                ucAvailableInputPorts;
    INPUTPORT_ENTRY      stInportList[MAX_PORTS_PER_BRANCH];
    MST_RELATIVEADDRESS  stBranchRAD;
    MST_PEER_DEVICE_TYPE ePeerDeviceType;
    USHORT               usTotalAvailablePBN;
    USHORT               usCurrentAvailablePBN;
    UCHAR                ucFECPathInfo;
    UCHAR                ucTotalPhysicalPorts;
    UCHAR                ucAvailablePhysicalPorts;
    UCHAR                ucTotalVirtualPorts;
    UCHAR                ucAvailableVirtualPorts;
    OUTPORT_ENTRY        stOutPortList[MAX_PORTS_PER_BRANCH];

    // This state structure should be branch's per input port incase different inputs are being driven through different sources
    // in which case stream ID management would become quite complicated (e.g. two sources don't know what stream ID the other is
    // source is using and end up using the same stream ID and the branch can't manage this)
    PAYLOADTABLE_STATE stBranchPayloadTableState;

    USHORT usDwnStreamPBNPerMTPSlot;

    BOOLEAN bAllocPayloadSentForClearPayload; // Used only by Branch Connected to Source to Manage ClearPayload Message

    // The below variable will keep a count of how many Allocate Payload are sent with PBN Zero as a part
    // of ClearPayload SBM handling. Branch Connected to Source will increment it for every clearpayload
    // table sent. And for every reply of the sent Allocate Payload table, this variable is decremented again
    // When this value comes to zero, it means all the allocate payload messages are handled by downstream
    // So the branch connected to source then finally sends the ACK reply for clearpayload message
    // This variable need not be incremented or decremented because access is guaranteed to be serialized
    // especially the decrementing case  by virtue of the threaded design of DownReplyMessageHandler thread
    ULONG ulNumAllocPayloadSentForClearPayload;

    // We need a look aside list of nak infos because the nak condition would be realized in one thread and
    // processed in another thread so if we use the same nak info struct it might get clobbered if client sends
    // back to back requests with Naks
    DP_LOOKASIDE_LIST_HEAD NakInfoLookAsideListHead;
    DP_LIST_HEAD           NakInfoProcessingListHead;

    // Notes on stServiceIRQVectorSpinLock
    // This lock has mainly been added for the Branch directly connected to source (BDCS)
    // The reason is the CSN test case path directly updates the UpRequest Buffer of the BDCS by passing
    // all other down stream branches and as a part of sending the UpRequest, the test case also modifies the UpRequestReady bit of the
    // IRQ vector DPCD of the BDCS. In any test case if the detection is going on in parallel while CSN is invoked, the BDCS IRQ Vector
    // might end up in a BAD state because detection path also modifies the IRQ vector. So we need to modify it within spin lock, i.e.
    // 1.Acquire Spin Lock
    // 2.Read-Modify-Write IRQ Vector of BDCS
    // 3. Release Spin Lock.
    // For ease of implementation and to maintain uniformity in code, this lock is currently acquired for all down stream branches
    // while modifying their IRQ vector DPCD
    DP_LOCK stServiceIRQVectorSpinLock;

    // If the Current Branch Node does a NACK
    PDP_EVENT pstThisNodeNAKReplyEvent;

    // Need two NodeACKReply Event for the current node to tell the Down Reply handling thread for the current node
    // which down request buffer has the valid data
    PDP_EVENT pstThisNodeACKReplyEvent[2];
    ULONG     ulCurrDwnReqBuffIndex; // Thisvariable will hold the buff Index of one of the two down req buffers being used.Need this variable as to pass the processed request from
    MST_DWNREQUEST_BUFF_INFO stDownRequestBuffInfo[2]; // DPCD 1000H - 11FFH For Msg with sequence No. 0
    HANDLE                   hDownRequestHandlerThreadHandle;
    DWORD                    dwDownRequestHandlerThreadID;
    DP_EVENT                 stDownRequestHandlerThreadKillEvent;

    MST_DWNREPLY_BUFF_INFO      stDownReplyBuffInfo; // DPCD 1400H - 15FFH
    PDP_EVENT                   pstDownReplyReadyEvent;
    DP_EVENT                    stUpReadDownReplyEvent;
    HANDLE                      hDownReplyHandlerThreadHandle;
    DWORD                       dwDownReplyHandlerThreadID;
    PDP_EVENT                   pstDownReplyHandlerThreadKillEvent;
    MST_DOWN_STREAM_PORT_EVENTS stDownStreamPortEvents;

    DP_LIST_HEAD            stUpRequestListHead;
    MST_UPREQUEST_BUFF_INFO stUpRequestBuffInfo; // DPCD 1600H - 17FFH
    DP_EVENT                stUpRequestEvent;
    HANDLE                  hUpRequestHandlerThreadHandle;
    DWORD                   dwUpRequestHandlerThreadID;
    DP_EVENT                stUpRequestHandlerThreadKillEvent;

    MST_UPREPLY_BUFF_INFO stUpReplyInfo; // DPCD 1200H - 13FFH

    PMST_DWNREQUEST_BUFF_INFO (*pfnGetAvailableDownReqBuff)(void *pstBranchNode);
    void (*pfnSetDownReqBuffState)(void *pstBranchNode, ULONG ulThisBuffIndex, DWNREQBUFF_SETSTATE eSetState);
    BOOLEAN (*pfnCheckSeqNumValidity)(void *pstBranchNode, UCHAR ucSeqNum);

    BRANCHDISP_DPCD stBranchDPCDMap;

} BRANCH_NODE, *PBRANCH_NODE;

typedef struct _DISPLAY_NODE
{
    // Make sure eNodeType always remains the first member or it will break the code
    NODE_TYPE            eNodeType;
    DPCD_REV             eDPCDRev;
    GUID                 uidDisplayGUID;
    MST_RELATIVEADDRESS  stDisplayRAD;
    UCHAR                ucTotalInputPorts;
    INPUTPORT_ENTRY      stInportList[MAX_STREAMSINK_PER_DISPLAY]; // Lets use only Port Zero for now
    MST_PEER_DEVICE_TYPE ePeerDeviceType;
    USHORT               usTotalAvailablePBN;
    USHORT               usCurrentAvailablePBN;
    EDID_I2C_DATA        stDisplayEDIDI2CData;
    UCHAR                ucFECPathInfo;

    // Node Mutex Lock is needed
    PDISPLAY_EDID   pstDisplayEDID;
    BRANCHDISP_DPCD stDisplayDPCDMap;

    // Add Edid fetching Fn Pointer here?

} DISPLAY_NODE, *PDISPLAY_NODE;

// Implementation Note: Add Sideband Message Handler Function Pointers to the topology object
typedef struct _DP12_TOPOLOGY
{
    ULONG                     ulTotalNumBranches;
    ULONG                     ulTotalNumDisplays;
    BOOLEAN                   bIsTopologyCleanedUp;
    PBRANCH_NODE              pstBranchConnectedToSrc;
    MST_DISPLAY_EDID_ARRAY    stMSTEDIDArray;
    MST_BRANCHDISP_DPCD_ARRAY stMSTDPCDArray;
    DPCD_CONFIG_DATA          stDPCDConfigData;

} DP12_TOPOLOGY, *PDP12_TOPOLOGY;

typedef enum _NODE_ADD_ERRROR_CODES
{
    eNODE_ADD_SUCCESS = 0,
    eINVALID_INPUT_PORT,
    eINVALID_OUTPUT_PORT,
    ePORT_ALREADY_IN_USE,
    eNO_FREE_PORT_AVAILABLE,
    eGENERIC_ERROR

} NODE_ADD_ERRROR_CODES;

typedef struct _UP_REQUEST_ARGS
{
    MST_REQ_ID_TYPE     eUpRequestID;
    MST_RELATIVEADDRESS stRAD;
    PVOID               pstGfxAdapterInfo;
    ULONG               ulPortNum;

    union {
        struct
        {
            BOOLEAN bAttachOrDetatch; // Applicable only to CSN
            PVOID   pvNewNodeToBeAdded;
            UCHAR   ucNewNodeInputPort;

        } stCSNArgs;

        struct
        {
            ULONG ulAvailabePBN; // Applicable only to RSN

        } stRSNArgs;
    };

} UP_REQUEST_ARGS, *PUP_REQUEST_ARGS;

// This structure is used to return three things
// Exact node (branch or display) for a given RAD
// Parent Branch of the node for a given RAD
// Port number of Parent Branch to which Node with the Given RAD is attached
typedef struct _RAD_NODE_INFO
{
    PVOID        pvRADNode;
    PBRANCH_NODE pstBranchNode;
    UCHAR        ucPortNum;

} RAD_NODE_INFO, *PRAD_NODE_INFO;

typedef enum _PORT_CONNECTED_STATUS
{

    eNotConnected = 0,
    eConnected    = 1,
    eAmbiguous    = 2

} PORT_CONNECTED_STATUS;

// These gets called from  other source files so putting the declaration in the header
// Topology creation related
PDP12_TOPOLOGY DP12TOPOLOGY_TopologyObjectInit();

BOOLEAN DP12TOPOLOGY_SetEDIDData(PDP12_TOPOLOGY pstDP12Topology, PUCHAR pucDisplayName, ULONG ulEDIDSize, PUCHAR pucEDIDBuff);
BOOLEAN DP12TOPOLOGY_SetDPCDData(PDP12_TOPOLOGY pstDP12Topology, PUCHAR pucDPCDName, ULONG ulNodeSize, PUCHAR pucDPCDBuff);

PDISPLAY_EDID    DP12TOPOLOGY_GetDisplayEDID(PDP12_TOPOLOGY pstDP12Topology, PUCHAR pucDisplayName);
PBRANCHDISP_DPCD DP12TOPOLOGY_GetNodeDPCD(PDP12_TOPOLOGY pstDP12Topology, PUCHAR pucDPCDName);

PBRANCH_NODE DP12TOPOLOGY_CreateBranchNode(PDP12_TOPOLOGY pstDP12Topology, MST_PEER_DEVICE_TYPE ePeerDeviceType, UCHAR ucTotalInputPorts, UCHAR ucTotalPhysicalPorts,
                                           UCHAR ucTotalVirtualPorts, ULONG ulMaxLinkRate, ULONG ulMaxLaneCount, ULONG ulBranchReplyDelay, USHORT usTotalAvailablePBN,
                                           ULONG ulLinkAddressDelay, ULONG ulRemoteI2ReadDelay, ULONG ulRemoteI2WriteDelay, ULONG ulRemoteDPCDReadDelay,
                                           ULONG ulRemoteDPCDWriteDelay, ULONG ulEPRDelay, ULONG ulAllocatePayloadDelay, ULONG ulClearPayLoadDelay, PUCHAR pucDPCDName);

PDISPLAY_NODE DP12TOPOLOGY_CreateDisplayNode(PDP12_TOPOLOGY pstDP12Topology, MST_PEER_DEVICE_TYPE ePeerDeviceType, UCHAR ucTotalInputPorts,
                                             USHORT usTotalAvailablePBN, // Ideally for display, usTotalAvailablePBN shouldn't be given separately through APP
                                             ULONG  ulMaxLinkRate,       // But should solely be called based on MAX LINK RATE and MAX LANE COUNT
                                             ULONG ulMaxLaneCount, ULONG ulRemoteI2ReadDelay, ULONG ulRemoteI2WriteDelay, ULONG ulRemoteDPCDReadDelay, ULONG ulRemoteDPCDWriteDelay,
                                             PUCHAR pucDPCDName, PUCHAR pucDisplayName);

NODE_ADD_ERRROR_CODES DP12TOPOLOGY_AddFirstBranch(PDP12_TOPOLOGY pstDP12Topology, PBRANCH_NODE pstNewBranchNode, UCHAR ucNewBranchInputPort, PUCHAR pucSharedDPCDBuff,
                                                  PUCHAR pucDPCDName, ULONG ulDPCDSize);
NODE_ADD_ERRROR_CODES DP12TOPOLOGY_AddBranch(PDP12_TOPOLOGY pstDP12Topology, PBRANCH_NODE pstTargetBranchNode, PBRANCH_NODE pstNewBranchNode, UCHAR ucTargetBranchOutPort,
                                             UCHAR ucNewBranchInputPort, BOOLEAN bSubTopologyAddition);
NODE_ADD_ERRROR_CODES DP12TOPOLOGY_AddDisplay(PDP12_TOPOLOGY pstDP12Topology, PBRANCH_NODE pstTargetBranchNode, PDISPLAY_NODE pstDisplayNode, UCHAR ucTargetBranchOutPort,
                                              UCHAR ucNewDisplayInputPor);

BOOLEAN DP12TOPOLOGY_UpRequestHandler(PDP12_TOPOLOGY pstDP12Topology, PUP_REQUEST_ARGS punUpRequestArgs);

// This is a interface called from the APP world and has nothing to do with the RemoteDPCDRead sideband message
BOOLEAN DP12TOPOLOGY_ReadRemoteDPCDAppWorld(PDP12_TOPOLOGY pstDP12Topology, PMST_RELATIVEADDRESS pstRAD, PUCHAR pucReadBuff, ULONG ulDPCDAddress, ULONG ulLength);

// This is a interface called from the APP world and has nothing to do with the RemoteDPCDWrite sideband message
BOOLEAN DP12TOPOLOGY_WriteRemoteDPCDAppWorld(PDP12_TOPOLOGY pstDP12Topology, PMST_RELATIVEADDRESS pstRAD, PUCHAR pucWriteBuff, ULONG ulDPCDAddress, ULONG ulLength);

BOOLEAN DP12TOPOLOGY_GetMSTTopologyRADArray(PDP12_TOPOLOGY pstDP12Topology, PBRANCHDISP_RAD_ARRAY pstBranchDispRADArray);
BOOLEAN DP12TOPOLOGY_ExtractCurrentTopologyInArrayFormat(PDP12_TOPOLOGY pstDP12Topology, PBRANCHDISP_DATA_ARRAY pstBranchDispDataArray);

RAD_NODE_INFO DP12TOPOLOGY_GetNodeForAGivenRAD(PDP12_TOPOLOGY pstDP12Topology, PMST_RELATIVEADDRESS pstInputRAD);
BOOLEAN       DP12TOPOLOGY_GetNodePortAttachStatus(PVOID pvNode, NODE_TYPE eNodeType, UCHAR ucPortNum);

BOOLEAN DP12TOPOLOGY_UpdateVCPayloadTable(PBRANCH_NODE pstBranchNode, PUCHAR pucBuffToWrite, ULONG ulAddress, ULONG ulLen);

BOOLEAN DP12TOPOLOGY_AddOrDeleteSubTopology(PDP12_TOPOLOGY pstDP12Topology, BOOLEAN bAttachOrDetach,
                                            BOOLEAN bForceAttach, // If we want to force attach the new node even though the branch's outport for a given RAD has already something
                                                                  // attached on it Detach Parameters:
                                            PVOID pvNodeToBeDeleted,
                                            // Attach Parameters:
                                            PBRANCH_NODE pstTargetBranchNode, PVOID pvNewNodeToBeAdded, UCHAR ucTargetBranchOutPort, UCHAR ucNewBranchInputPort);

BOOLEAN DP12TOPOLOGY_Cleanup(PDP12_TOPOLOGY pstDP12Topology);

#endif