#ifndef __DPCOREIOCTLCOMMON_H__
#define __DPCOREIOCTLCOMMON_H__

// This value is same as the NODE_NAME_STR_SIZE
#define MAX_STR_SIZE 40

////****************************************************************************************************************/////
///// Below Declaration has same structs with Different Names defined in other files. Please change those if changing
////  below values
////***************************************************************************************************************/////
#define MAX_NUM_BRANCHES 15
#define MAX_NUM_DISPLAYS 30

#define MAX_LINK_COUNT 15
// As every Address for a link requires 4 Bits, therefore total 14 links (MAX_LINK_COUNT - 1, since for 1st link RAD is not required) would require 56 bits.
// Hence total 7 Bytes
#define MAX_BYTES_RAD ((MAX_LINK_COUNT) / 2)

#define DPCD_MAX_DPCD_VALUES 8
#define DPCD_MAX_DPCD_SETS 2
#define DPCD_MAX_TRANSACTIONS 15

typedef enum _DP_TOPOLOGY_TYPE
{
    eInvalidTopology = 0,
    eDPSST,
    eDPMST,
    eDPEDP

} DP_TOPOLOGY_TYPE;

typedef enum _DP_AVAILABLE_LINK_RATE
{
    eLinkRate_162 = 0x6,
    eLinkRate_270 = 0xA,
    eLinkRate_540 = 0x14,
    eLinkRate_810 = 0x1E

} DP_AVAILABLE_LINK_RATE,
*PDP_AVAILABLE_LINK_RATE;

typedef enum _DP_AVAILABLE_LANE_COUNT
{
    eLaneCount_1 = 1,
    eLaneCount_2 = 2,
    eLaneCount_4 = 4,

} DP_AVAILABLE_LANE_COUNT,
*PDP_AVAILABLE_LANE_COUNT;

typedef enum _DP_TRAINING_PATTERN
{
    eTrainingNotInProgress = 0,
    eTrainingPattern1      = 1,
    eTrainingPattern2      = 2,
    eTrainingPattern3      = 3,
    // eD102WithoutScrambling = 4,
    // eSymbolErrMsrCnt = 5,
    // ePRBS7 = 6,
    // eIdlePattern = 7,
    // eScrambling = 8,
    // eHBR2EyeCompliance = 9,
    // eBits80Custom = 10,
    // ePCTPattern = 11,
    eTrainingPattern4 = 7

} DP_TRAINING_PATTERN,
*PDP_TRAINING_PATTERN;

typedef enum _DP_VOLTAGE_SWING_LEVEL
{
    eInvalidVswing = -1,
    eVSWing_e0_4   = 0,
    eVSWing_e0_6   = 1,
    eVSWing_e0_8   = 2,
    eVSWing_e1_2   = 3,
    eMAX_VSWING    = 4,

} DP_VOLTAGE_SWING_LEVEL,
*PDP_VOLTAGE_SWING_LEVEL;

typedef enum _DP_PREEMPHASIS_LEVEL
{
    eInvalidPreEmphasis = -1,
    eNoPreEmp_0db       = 0,
    ePreEmp_e3_5dB      = 1,
    ePreEmp_e6dB        = 2,
    ePreEmp_e9_5dB      = 3,
    eMAX_PREEMPHASIS    = 4,

} DP_PREEMPHASIS_LEVEL,
*PDP_PREEMPHASIS_LEVEL;

#pragma pack(1)

// Packing this structure because it has to be copied to the identical packed structure in DPIOCTL.h that is used in the usermode land
typedef struct _MST_RELATIVEADDRESS
{
    unsigned char ucTotalLinkCount;
    unsigned char ucRemainingLinkCount;
    unsigned char ucRadSize;
    // If ucTotalLinkCount is 1 then Relative ucAddress should have zero value at all the indexes..

    // If the ucTotalLinkCount is Even then index from 0 till (ucTotalLinkCount/2 - 1) (apart from the Upper Nibble of last index) is a Valid Address, .

    // If the ucTotalLinkCount is Odd then index from 0 till (ucTotalLinkCount)/2 - 1) will be a Valid Address

    // Hence for both odd/even ucTotalLinkCount, we can use Index from 0 till (ucTotalLinkCount/2 - 1)

    unsigned char ucAddress[MAX_BYTES_RAD];

} MST_RELATIVEADDRESS, *PMST_RELATIVEADDRESS;

typedef struct _BRANCH_NODE_DESC
{
    unsigned char  ucUpStrmBranchOutPort;
    unsigned char  ucThisBranchInputPort;
    unsigned char  ucTotalInputPorts;
    unsigned char  ucTotalPhysicalPorts;
    unsigned char  ucTotalVirtualPorts;
    unsigned char  ucReserved;
    unsigned short usTotalAvailablePBN;
    unsigned int   uiMaxLinkRate;
    unsigned int   uiMaxLaneCount;
    unsigned int   uiBranchReplyDelay;
    unsigned int   uiLinkAddressDelay;
    unsigned int   uiRemoteI2ReadDelay;
    unsigned int   uiRemoteI2WriteDelay;
    unsigned int   uiRemoteDPCDReadDelay;
    unsigned int   uiRemoteDPCDWriteDelay;
    unsigned int   uiEPRDelay;
    unsigned int   uiAllocatePayloadDelay;
    unsigned int   uiClearPayLoadDelay;

} BRANCH_NODE_DESC, *PBRANCH_NODE_DESC;

typedef struct _DISPLAY_NODE_DESC
{
    unsigned char  ucUpStrmBranchOutPort;
    unsigned char  ucThisDisplayInputPort;
    unsigned char  ucTotalInputPorts;
    unsigned char  ucReserved;
    unsigned short usTotalAvailablePBN;
    unsigned int   uiMaxLinkRate;
    unsigned int   uiMaxLaneCount;
    unsigned int   uiRemoteI2ReadDelay;
    unsigned int   uiRemoteI2WriteDelay;
    unsigned int   uiRemoteDPCDReadDelay;
    unsigned int   uiRemoteDPCDWriteDelay;

} DISPLAY_NODE_DESC, *PDISPLAY_NODE_DESC;

typedef struct _BRANCH_DATA
{
    unsigned int     uiThisIndex;
    unsigned int     uiParentBranchIndex;
    unsigned char    ucDPCDName[MAX_STR_SIZE];
    BRANCH_NODE_DESC stBranchNodeDesc;

} BRANCH_DATA, *PBRANCH_DATA;

typedef struct _DISPLAY_DATA
{
    unsigned int      uiThisIndex;
    unsigned int      uiParentBranchIndex;
    unsigned char     ucDPCDName[MAX_STR_SIZE];
    unsigned char     ucDisplayName[MAX_STR_SIZE];
    DISPLAY_NODE_DESC stDisplayNodeDesc;

} DISPLAY_DATA, *PDISPLAY_DATA;

typedef struct _BRANCHDISP_DATA_ARRAY
{
    unsigned int uiPortNum;
    unsigned int uiNumBranches;
    BRANCH_DATA  stBranchData[MAX_NUM_BRANCHES];
    unsigned int uiNumDisplays;
    DISPLAY_DATA stDisplayData[MAX_NUM_DISPLAYS];

} BRANCHDISP_DATA_ARRAY, *PBRANCHDISP_DATA_ARRAY;

typedef struct _NODE_RAD_INFO
{
    unsigned long       ulThisNodeIndex;
    unsigned long       ulParentBranchIndex;
    MST_RELATIVEADDRESS stNodeRAD;

} NODE_RAD_INFO, *PNODE_RAD_INFO;

typedef struct _BRANCHDISP_RAD_ARRAY
{
    unsigned long ulNumBranches;
    NODE_RAD_INFO stBranchRADInfo[MAX_NUM_BRANCHES];
    unsigned long ulNumDisplays;
    NODE_RAD_INFO stDisplayRADInfo[MAX_NUM_DISPLAYS];

} BRANCHDISP_RAD_ARRAY, *PBRANCHDISP_RAD_ARRAY;

// this represents DPCDs from startingOffset till startingOffset+length, and respective values in values
typedef struct _DPCD_VALUE_LIST
{
    ULONG ulStartingOffset;
    UCHAR ucLength;
    UCHAR ucValues[DPCD_MAX_DPCD_VALUES];
} DPCD_VALUE_LIST, *PDPCD_VALUE_LIST;

typedef struct _DPCD_TRANSACTION
{
    UCHAR           ucNumInputDpcdSets;
    DPCD_VALUE_LIST stInputDpcdSets[DPCD_MAX_DPCD_SETS];
    UCHAR           ucNumResponseDpcdSets;
    DPCD_VALUE_LIST stResponseDpcdSets[DPCD_MAX_DPCD_SETS];
} DPCD_TRANSACTION, *PDPCD_TRANSACTION;

typedef struct _DPCD_MODEL_DATA
{
    UCHAR            ucTransactionCount;
    DPCD_TRANSACTION stDPCDTransactions[DPCD_MAX_TRANSACTIONS];
    // whenever write to ulTriggerOffset comes, we consider it an DPCD transaction and do necessary actions
    ULONG ulTriggerOffset;
    // during any failure case like write values didn't match expected input, we will give response in DPCD as given in stDefaultResponseDpcdSet
    // (some status registers can be passed here)
    DPCD_VALUE_LIST stDefaultResponseDpcdSet;
} DPCD_MODEL_DATA, *PDPCD_MODEL_DATA;

#pragma pack()

#endif // !__DPCOREIOCTLCOMMON_H__
