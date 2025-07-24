
// Imp: IOCTL Files shouldn't include any driver headers execept other IOCTL files and dependant files accessible to the APP world

#ifndef __DP_IOCTL_H__
#define __DP_IOCTL_H__
#include "DPCoreIOCTLCommonDefs.h"

/////////****************************************************************************************************************/////////////
////////*************************************************IOCTLs START***************************************************/////////////
////////****************************************************************************************************************/////////////

// Simulation Init Related IOCTLs  //Lets Reserve 50 values for this

#define IOCTL_INIT_DP_TOPOLOGY CTL_CODE(SIM_IOCTL_DEVTYPE, SIM_IOCTL_BASEVAL + SIM_IOCTL_DP, METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_SET_DPCD_DATA CTL_CODE(SIM_IOCTL_DEVTYPE, SIM_IOCTL_BASEVAL + SIM_IOCTL_DP + 3, METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_SET_BRANCHDISP_DATA CTL_CODE(SIM_IOCTL_DEVTYPE, SIM_IOCTL_BASEVAL + SIM_IOCTL_DP + 4, METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_READ_DPCD CTL_CODE(SIM_IOCTL_DEVTYPE, SIM_IOCTL_BASEVAL + SIM_IOCTL_DP + 5, METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_WRITE_DPCD CTL_CODE(SIM_IOCTL_DEVTYPE, SIM_IOCTL_BASEVAL + SIM_IOCTL_DP + 6, METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_GET_MST_RAD CTL_CODE(SIM_IOCTL_DEVTYPE, SIM_IOCTL_BASEVAL + SIM_IOCTL_DP + 7, METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_GENERATE_CSN CTL_CODE(SIM_IOCTL_DEVTYPE, SIM_IOCTL_BASEVAL + SIM_IOCTL_DP + 8, METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_GENERATE_SPI CTL_CODE(SIM_IOCTL_DEVTYPE, SIM_IOCTL_BASEVAL + SIM_IOCTL_DP + 9, METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_SET_GFXS3S4_DPCD_DATA CTL_CODE(SIM_IOCTL_DEVTYPE, SIM_IOCTL_BASEVAL + SIM_IOCTL_DP + 10, METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_SET_GFXS3S4_BRANCHDISP_DATA CTL_CODE(SIM_IOCTL_DEVTYPE, SIM_IOCTL_BASEVAL + SIM_IOCTL_DP + 11, METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_GFXS3S4_ADDREMOVESUBTOPOLOGY CTL_CODE(SIM_IOCTL_DEVTYPE, SIM_IOCTL_BASEVAL + SIM_IOCTL_DP + 12, METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_SET_DPCD_MODEL_DATA CTL_CODE(SIM_IOCTL_DEVTYPE, SIM_IOCTL_BASEVAL + SIM_IOCTL_DP + 13, METHOD_BUFFERED, SIM_FILE_ACCESS)

#define IOCTL_SET_GFXS3S4_DPCD_MODEL_DATA CTL_CODE(SIM_IOCTL_DEVTYPE, SIM_IOCTL_BASEVAL + SIM_IOCTL_DP + 14, METHOD_BUFFERED, SIM_FILE_ACCESS)

/////////****************************************************************************************************************/////////////
////////*************************************************IOCTLs END***************************************************** /////////////
////////****************************************************************************************************************/////////////

//\/\/\/\//////////////////////////////////////////////////////////////\/\
//\/\//\/////////Define App-Driver Common structures below///////////\/\/\
//\/\/\/\/////////////////////////////////////////////////////////////\/\/

#define PARENT_INDEX_BRANCH_CONNECTED_TO_SRC 0xFFFFFFFF

#define PARENT_INDEX_SUB_TOPOLOGY 0xBBBBBBBB

#define MAX_DP_PORTS 6

// Packing  to 1 as the branch and display data would go as a raw buffer to driver

#pragma pack(1)

typedef struct _DP_INIT_INFO
{
    unsigned int     uiPortNum;
    DP_TOPOLOGY_TYPE eTopologyType;

} DP_INIT_INFO, *PDP_INIT_INFO;

typedef struct _DP_DPCD_MODEL_DATA
{
    unsigned int     uiPortNum;
    DP_TOPOLOGY_TYPE eTopologyType;
    DPCD_MODEL_DATA  stDPCDModelData;

} DP_DPCD_MODEL_DATA, *PDP_DPCD_MODEL_DATA;

typedef struct _GET_DPCD_ARGS
{
    unsigned long       ulPortNum;
    BOOLEAN             bNative;
    MST_RELATIVEADDRESS stRAD;
    ULONG               ulDPCDAddress;
    ULONG               ulReadLength;

} GET_DPCD_ARGS, *PGET_DPCD_ARGS;

typedef struct _SET_DPCD_ARGS
{
    unsigned long       ulPortNum;
    BOOLEAN             bNative;
    MST_RELATIVEADDRESS stRAD;
    ULONG               ulDPCDAddress;
    ULONG               ulWriteLength;
    // Write Buffer goes here

} SET_DPCD_ARGS, *PSET_DPCD_ARGS;

typedef struct _DP_SUBTOPOLOGY_ARGS
{
    unsigned long         ulPortNum;
    BOOLEAN               bAttachOrDetach; // TRUE - Attach, FALSE - Detach
    MST_RELATIVEADDRESS   stNodeRAD;
    BRANCHDISP_DATA_ARRAY stSubTopology;

} DP_SUBTOPOLOGY_ARGS, *PDP_SUBTOPOLOGY_ARGS;

typedef struct _PORT_SPI_ARGS
{
    unsigned long ulPortNum;

} PORT_SPI_ARGS, *PPORT_SPI_ARGS;

typedef struct _S3S4_DP_PLUGUNPLUG_DATA
{
    BOOLEAN          bPlugOrUnPlugAtSource; // Whether the App wants to plug or unplug at source or at non-source-connected node in the MST daisy chain (Valid only for DP MST)
    DP_TOPOLOGY_TYPE eTopologyAfterResume;

} S3S4_DP_PLUGUNPLUG_DATA, *PS3S4_DP_PLUGUNPLUG_DATA;

typedef struct _DPCD_ARGS
{
    unsigned long ulPortNum;
    UINT16        uOffset;
    UINT8         uValue;
} DPCD_ARGS, *PDPCD_ARGS;
#pragma pack()

#endif
