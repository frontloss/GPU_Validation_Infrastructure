
/* Sample app to demonstrate get handle to DisplayPort.dll and sending IOCTLs to the DIVA KMD driver and GfxValSimulation driver */

#include "stdafx.h"
#include <windows.h>
#include <string>
#include "..\Header\Common\DisplayPort.h"

#define PORT_NUM 13

typedef HRESULT(__cdecl *DLLDivaKMDConn)();
typedef HRESULT(__cdecl *GetDPAPIVersion)(PINT pVersion);
typedef HRESULT(__cdecl *PFN_CHECK_HANDLE)();
typedef HRESULT(__cdecl *PFN_INIT_PORT)(PPORT_INFO_ARRAY);
typedef HRESULT(__cdecl *PFN_PARSENSEND_TOPOLOGY)(UINT, DP_TOPOLOGY_TYPE, CONST CHAR *, BOOL);
typedef HRESULT(__cdecl *PFN_SET_HPD)(UINT, BOOL);
typedef HRESULT(__cdecl *PFN_READ_DPCD)(GET_DPCD_ARGS, PVOID);
typedef HRESULT(__cdecl *PFN_GET_RAD)(ULONG, PBRANCHDISP_RAD_ARRAY);
typedef HRESULT(__cdecl *PFN_ADDREMOVE_TOPOLOGY)(ULONG, BOOL, PMST_RELATIVEADDRESS, CHAR *, BOOL);
typedef HRESULT(__cdecl *PFN_INIT_DP)(PDP_INIT_INFO);
typedef HRESULT(__cdecl *PFN_VERIFY_TOPOLOGY)(ULONG);
typedef HRESULT(__cdecl *PFN_SETLP_MODE)(GFXS3S4_ALLPORTS_PLUGUNPLUG_DATA);
typedef HRESULT(__cdecl *PFN_WRITE_DPCD)(PSET_DPCD_ARGS);
typedef HRESULT(__cdecl *PFN_INITIALIZECUISDK)();
typedef HRESULT(__cdecl *PFN_GETCOLLAGEINFO)();
typedef HRESULT(__cdecl *PFN_DISABLECOLLAGEMODE)();
typedef HRESULT(__cdecl *PFN_APPLYCOLLAGE)(PIGFX_SYSTEM_CONFIG_DATA_N_VIEW);
typedef HRESULT(__cdecl *PFN_APPLYSINGLEDISPLAY)();
typedef HRESULT(__cdecl *PFN_GETSUPPORTEDCONFIG)(PIGFX_TEST_CONFIG_EX);

/* Function prototypes */
void VerifyDLLDIVAConnection(HMODULE handle);
void GetDPInterfaceVersion(HMODULE handle);
void InitGfxValSimDriverNPort(HMODULE handle);
void CheckSimulateDPDisplay(HMODULE handle, std::string inputType, std::string inputfile);
void SetHPD(HMODULE handle);
void ReadDPCD(HMODULE handle);
void WriteDPCD(HMODULE handle);
void VerifyMSTTopology(HMODULE handle);
void GetMSTRADInfo(HMODULE handle);
void AddRemoveSubTopology(HMODULE handle);
void SetLowPowerMode(HMODULE handle);
void GetCollage(HMODULE handle);

/*
 * @brief        Sample App which gets DisplayPort DLL handle & calls functions exported by it
 * @param[In]    Zero
 * @return       INT
 */
int main(int argc, char *argv[])
{
    TRACE_LOG(DEBUG_LOGS, "\n**********************************************************************************\n");
    TRACE_LOG(DEBUG_LOGS, "Sample App which gets DisplayPort utility handle & calls functions exported by it.");
    TRACE_LOG(DEBUG_LOGS, "\n**********************************************************************************\n");

    std::string input1 = argv[1];
    std::string input2 = argv[2];

    /* Load DisplayPort.dll library */
    HMODULE handle = LoadLibraryA("C:\\Automation\\bin\\DisplayPort.dll");

    if (NULL != handle)
    {
        TRACE_LOG(DEBUG_LOGS, "DLL DisplayPort.dll loaded Successfully.\n");

        /* Verify DLL to DIVA KMD connection status */
        VerifyDLLDIVAConnection(handle);

        /* Get DisplayPort DLL interface version */
        GetDPInterfaceVersion(handle);

        /* Get GfxValSim Handle and Initialize Port */
        InitGfxValSimDriverNPort(handle);

        /* Initialize DP Aux objects, parse and send SST/MST data to Sim driver */
        CheckSimulateDPDisplay(handle, input1, input2);

        /* Hotplug DP Panel*/
        SetHPD(handle);

        /* Read DPCD value from the Gfx Val Sim driver */
        ReadDPCD(handle);

        /* Verify Topology detected after plugging is same or not */
        VerifyMSTTopology(handle);

        /* Get all RAD Inofmration from Gfx Val Sim driver */
        GetMSTRADInfo(handle);

        /* Add/Remove Sub-Topology from original topology */
        AddRemoveSubTopology(handle);

        /* Add/Remove Sub-Topology from original topology in low power mode */
        SetLowPowerMode(handle);

        GetCollage(handle);

        /* Free the DLL library */
        FreeLibrary(handle);
    }
    else
    {
        /* DLL load failed */
        TRACE_LOG(DEBUG_LOGS, "DLL DisplayPort.dll load failed!\n");
    }
    return 0;
}

/*
 * @brief        VerifyDLLDIVAConnection function gets handle to DisplayPort.DLL and calls few functions
 *               exported by it to verify connection b/w DLL and DIVA KMD
 * @param[In]    Handle of DIVA KMD driver
 * @return       VOID
 */
void VerifyDLLDIVAConnection(HMODULE handle)
{
    /* Get the address of function DLLDivaKMDConnection */
    DLLDivaKMDConn VerifyDLLDivaKMDConnStatus = (DLLDivaKMDConn)GetProcAddress(handle, "Get_DLLToDivaKMDConnectionStatus");

    /* Verify DLL to DIVA KMD connection status */
    VerifyDLLDivaKMDConnStatus();
}

/*
 * @brief        GetDPInterfaceVersion function gets DisplayPort DLL's Interface version
 * @param[In]    Handle to DIVA KMD driver
 * @return       VOID
 */
void GetDPInterfaceVersion(HMODULE handle)
{
    INT Version = 0x0;

    /* Get the address of function DLLDivaKMDConnection */
    GetDPAPIVersion GetDisplayPortAPIVersion = (GetDPAPIVersion)GetProcAddress(handle, "Get_DisplayPortInterfaceVersion");

    /* Get DisplayPort DLL interface version */
    GetDisplayPortAPIVersion(&Version);

    TRACE_LOG(DEBUG_LOGS, "DisplayPort API Version: %d\n", Version);
}

/*
 * @brief        InitGfxValSimDriverNPort function gets GfxValSimDriver initialization
 * @param[In]    Handle to GfxValSimDriver
 * @return       VOID
 */
void InitGfxValSimDriverNPort(HMODULE handle)
{
    BOOL bStatus = FALSE;

    PORT_INFO_ARRAY stPortInfo;
    stPortInfo.ulNumPorts               = 1;
    stPortInfo.stPortInfoArr->ulPortNum = PORT_NUM;
    stPortInfo.stPortInfoArr->eRxTypes  = eDP;

    PFN_CHECK_HANDLE pInitValSim = (PFN_CHECK_HANDLE)GetProcAddress(handle, "InitGfxValSimulator");
    bStatus                      = (pInitValSim)();
    if (bStatus != TRUE)
    {
        TRACE_LOG(DEBUG_LOGS, "\n GetHandle Call Failed!!!!! \n");
    }

    PFN_INIT_PORT pInitport = (PFN_INIT_PORT)GetProcAddress(handle, "InitPort");
    bStatus                 = ((pInitport)(&stPortInfo));
    if (bStatus != TRUE)
    {
        TRACE_LOG(DEBUG_LOGS, "\n Initialization of Port and DP Object Call Failed!!!!! \n");
    }
}

/*
 * @brief        CheckSimulateDPDisplay function Initializes DP Object, parse SST/MST data and sends
 *				to GFX Val Sim driver
 * @param[In]    Handle to GfxValSimDriver, InputType - SST/MST, InputFile - XML File
 * @return       VOID
 */
void CheckSimulateDPDisplay(HMODULE handle, std::string inputType, std::string inputfile)
{
    BOOL bStatus = FALSE;

    std::string XMLPath            = inputfile;
    CHAR *      sstMSTXMLFile      = const_cast<char *>(XMLPath.c_str());
    CHAR *      subTopologyXMLFile = "C:\\Automation\\DisplayAutomation2.0\\bin\\XMLFiles\\SubTopology.xml";

    DP_INIT_INFO stDPInitInfo;

    stDPInitInfo.uiPortNum = PORT_NUM;
    if (inputType == "SST")
    {
        stDPInitInfo.eTopologyType = eDPSST;
    }
    else
    {
        stDPInitInfo.eTopologyType = eDPMST;
    }

    PFN_INIT_DP pInitDP = (PFN_INIT_DP)GetProcAddress(handle, "DisplayportInit");
    bStatus             = ((pInitDP)(&stDPInitInfo));
    if (bStatus != TRUE)
    {
        TRACE_LOG(DEBUG_LOGS, "\n Initialization of DP Object Call Failed!!!!! \n");
    }

    PFN_PARSENSEND_TOPOLOGY pParseNSendTopology = (PFN_PARSENSEND_TOPOLOGY)GetProcAddress(handle, "ParseNSendTopology");
    bStatus                                     = ((pParseNSendTopology)(stDPInitInfo.uiPortNum, stDPInitInfo.eTopologyType, sstMSTXMLFile, FALSE));
    if (bStatus != TRUE)
    {
        TRACE_LOG(DEBUG_LOGS, "\n Parsing Topology Call Failed!!!!! \n");
    }
}

/*
 * @brief        SetHPD function issues hotplug/unplug command to Gfx Val Sim driver
 * @param[In]    Handle to GfxValSimDriver
 * @return       VOID
 */
void SetHPD(HMODULE handle)
{
    BOOL bStatus = FALSE;

    DP_INIT_INFO stDPInitInfo;
    stDPInitInfo.uiPortNum = PORT_NUM;

    PFN_SET_HPD pSetHPD = (PFN_SET_HPD)GetProcAddress(handle, "SetHPD");
    bStatus             = ((pSetHPD)(stDPInitInfo.uiPortNum, TRUE));
    if (bStatus != TRUE)
    {
        TRACE_LOG(DEBUG_LOGS, "\n SetHPD Call Failed!!!!! \n");
    }
}

/*
 * @brief        GetMSTRADInfo function used to get all RAD Information from the Gfx Val Sim driver
 * @param[In]    Handle to GfxValSimDriver
 * @return       VOID
 */
void GetMSTRADInfo(HMODULE handle)
{
    BOOL                 bStatus = FALSE;
    GET_DPCD_ARGS        stDpcdInfo;
    BRANCHDISP_RAD_ARRAY stRADdata = {
        0,
    };

    stDpcdInfo.ulPortNum = PORT_NUM;

    PFN_GET_RAD pGetRADInfo = (PFN_GET_RAD)GetProcAddress(handle, "GetMSTTopologyRAD");
    bStatus                 = ((pGetRADInfo)(stDpcdInfo.ulPortNum, &stRADdata));
    if (bStatus != TRUE)
    {
        TRACE_LOG(DEBUG_LOGS, "\n GetMSTTopologyRAD Call Failed!!!!! \n");
    }
}

/*
 * @brief        ReadDPCD function used to read DPCD value from the Gfx Val Sim driver
 * @param[In]    Handle to GfxValSimDriver
 * @return       VOID
 */
void ReadDPCD(HMODULE handle)
{
    BOOL  bStatus      = FALSE;
    VOID *outputBuffer = NULL;

    GET_DPCD_ARGS stDpcdInfo;
    stDpcdInfo.ulPortNum     = PORT_NUM;
    stDpcdInfo.bNative       = TRUE;
    stDpcdInfo.ulReadLength  = 1;
    stDpcdInfo.ulDPCDAddress = 0x600;

    outputBuffer = malloc(stDpcdInfo.ulReadLength);

    PFN_READ_DPCD pReadDPCD = (PFN_READ_DPCD)GetProcAddress(handle, "ReadDPCD");
    bStatus                 = ((pReadDPCD)(stDpcdInfo, outputBuffer));
    if (bStatus != TRUE)
    {
        TRACE_LOG(DEBUG_LOGS, "\n ReadDPCD Call Failed!!!!! \n");
    }

    free(outputBuffer);
}

/*
 * @brief        VerifyMSTTopology function used to check if Topology plugged is the expected one or not
 * @param[In]    Handle to GfxValSimDriver
 * @return       VOID
 */
void VerifyMSTTopology(HMODULE handle)
{
    BOOL         bStatus = FALSE;
    DP_INIT_INFO stDPInitInfo;

    stDPInitInfo.uiPortNum = PORT_NUM;

    PFN_VERIFY_TOPOLOGY pVerifyTopology = (PFN_VERIFY_TOPOLOGY)GetProcAddress(handle, "VerifyMSTTopology");
    bStatus                             = ((pVerifyTopology)(stDPInitInfo.uiPortNum));
    if (bStatus != TRUE)
    {
        TRACE_LOG(DEBUG_LOGS, "\n VerifyMSTTopology Call Failed!!!!! \n");
    }
}

/*
 * @brief        AddRemoveSubTopology function used to add/remove sub-topology from original topology
 * @param[In]    Handle to GfxValSimDriver
 * @return       VOID
 */
void AddRemoveSubTopology(HMODULE handle)
{
    BOOL                 bStatus = FALSE;
    GET_DPCD_ARGS        stDpcdInfo;
    BRANCHDISP_RAD_ARRAY stRADdata = {
        0,
    };

    stDpcdInfo.ulPortNum = PORT_NUM;

    PFN_ADDREMOVE_TOPOLOGY pAddRemoveTopology = (PFN_ADDREMOVE_TOPOLOGY)GetProcAddress(handle, "AddRemoveSubTopology");
    bStatus                                   = ((pAddRemoveTopology)(stDpcdInfo.ulPortNum, FALSE, &(stRADdata.stDisplayRADInfo[5].stNodeRAD), NULL, FALSE));
    if (bStatus != TRUE)
    {
        TRACE_LOG(DEBUG_LOGS, "\n SetCSN Call Failed for detaching display/branch!!!!! \n");
    }
}

/*
 * @brief        SetLowPowerMode function used to add/remove sub-topology from original topology in low power mode
 * @param[In]    Handle to GfxValSimDriver
 * @return       VOID
 */
void SetLowPowerMode(HMODULE handle)
{
    BOOL                             bStatus = FALSE;
    GFXS3S4_ALLPORTS_PLUGUNPLUG_DATA stPowerInfo;

    stPowerInfo.ulNumPorts                                                               = 1;
    stPowerInfo.stS3S4PortPlugUnplugData[0].ulPortNum                                    = PORT_NUM;
    stPowerInfo.stS3S4PortPlugUnplugData[0].eSinkPlugReq                                 = ePlugSink;
    stPowerInfo.stS3S4PortPlugUnplugData[0].stS3S4DPPlugUnplugData.bPlugOrUnPlugAtSource = TRUE;
    stPowerInfo.stS3S4PortPlugUnplugData[0].stS3S4DPPlugUnplugData.eTopologyAfterResume  = eDPMST;

    PFN_SETLP_MODE pSetLPMode = (PFN_SETLP_MODE)GetProcAddress(handle, "SetLowPowerState");
    bStatus                   = ((pSetLPMode)(stPowerInfo));
    if (bStatus != TRUE)
    {
        TRACE_LOG(DEBUG_LOGS, "\n SetLowPowerState Call Failed \n");
    }
}

/*
 * @brief        WriteDPCD function used to write DPCD value
 * @param[In]    Handle to GfxValSimDriver
 * @return       VOID
 */
void WriteDPCD(HMODULE handle)
{
    BOOL                 bStatus     = TRUE;
    UCHAR *              inputBuffer = NULL;
    BRANCHDISP_RAD_ARRAY stRADdata   = {
        0,
    };

    inputBuffer                   = (PUCHAR)malloc(sizeof(SET_DPCD_ARGS) + sizeof(UCHAR));
    PSET_DPCD_ARGS pDpcdWriteInfo = (PSET_DPCD_ARGS)inputBuffer;

    do
    {
        if (inputBuffer == NULL)
        {
            TRACE_LOG(DEBUG_LOGS, "\n Memory Allocation failed for input buffer data required for write DPCD.... \n");
            bStatus = FALSE;
            break;
        }

        if (pDpcdWriteInfo == NULL)
        {
            TRACE_LOG(DEBUG_LOGS, "\n Memory Allocation failed for WriteDPCD data structure.... \n");
            bStatus = FALSE;
            break;
        }

        pDpcdWriteInfo->ulPortNum              = PORT_NUM;
        pDpcdWriteInfo->bNative                = FALSE;
        pDpcdWriteInfo->ulWriteLength          = 1;
        pDpcdWriteInfo->ulDPCDAddress          = 0x00;
        *(inputBuffer + sizeof(SET_DPCD_ARGS)) = 0xFF;

        pDpcdWriteInfo->stRAD = stRADdata.stBranchRADInfo[1].stNodeRAD;

        PFN_WRITE_DPCD pWriteDPCD = (PFN_WRITE_DPCD)GetProcAddress(handle, "ReadDPCD");
        bStatus                   = ((pWriteDPCD)(pDpcdWriteInfo));
        if (bStatus != TRUE)
        {
            TRACE_LOG(DEBUG_LOGS, "\n WriteDPCD Call Failed!!!!! \n");
            bStatus = FALSE;
            break;
        }

    } while (FALSE);

    free(inputBuffer);
}

/*
 * @brief        GetCollage function will enable/disable collage
 * @param[In]    GfxValSimDriver
 * @return       VOID
 */
void GetCollage(HMODULE handle)
{
    BOOL                           bStatus;
    IGFX_TEST_CONFIG_EX            stConfigEx;
    IGFX_SYSTEM_CONFIG_DATA_N_VIEW m_GetSystemConfigExData;
    UINT                           uiNumDisplays, uiSize;

    PFN_INITIALIZECUISDK pInitSDK = (PFN_INITIALIZECUISDK)GetProcAddress(handle, "InitializeCUISDK");
    bStatus                       = (pInitSDK)();
    if (bStatus != TRUE)
    {
        TRACE_LOG(DEBUG_LOGS, "\n GetHandle Call Failed!!!!! \n");
    }

    PFN_GETCOLLAGEINFO pInitport = (PFN_GETCOLLAGEINFO)GetProcAddress(handle, "GetCollageInfo");
    bStatus                      = ((pInitport)());
    if (bStatus != TRUE)
    {
        TRACE_LOG(DEBUG_LOGS, "\n Initialization of Port and DP Object Call Failed!!!!! \n");
    }

    PFN_GETSUPPORTEDCONFIG pGetSupporteConfig = (PFN_GETSUPPORTEDCONFIG)GetProcAddress(handle, "GetSupportedConfig");
    bStatus                                   = ((pGetSupporteConfig)(&stConfigEx));
    if (bStatus != TRUE)
    {
        TRACE_LOG(DEBUG_LOGS, "\n Initialization of Port and DP Object Call Failed!!!!! \n");
    }

    uiNumDisplays                            = 2;
    BOOL bHorizontal                         = TRUE;
    BOOL found                               = FALSE;
    UINT IGFX_SYSTEM_CONFIG_DATA_N_VIEW_SIZE = sizeof(DWORD) + sizeof(DWORD) + sizeof(UINT) + sizeof(UINT) + sizeof(IGFX_DISPLAY_CONFIG_DATA_EX);
    uiSize                                   = IGFX_SYSTEM_CONFIG_DATA_N_VIEW_SIZE + (sizeof(IGFX_DISPLAY_CONFIG_DATA_EX) * (uiNumDisplays - 1));

    for (UINT index = 0; index < stConfigEx.dwNumTotalCfg; index++)
    {
        m_GetSystemConfigExData.DispCfg[0].dwDisplayUID = stConfigEx.ConfigList[index].dwPriDevUID;

        /* Dual Hor Collage */
        if (bHorizontal && uiNumDisplays == stConfigEx.ConfigList[index].dwNDisplays &&
            stConfigEx.ConfigList[index].dwOperatingMode == IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DUAL_HORZCOLLAGE)
        {
            m_GetSystemConfigExData.DispCfg[1].dwDisplayUID = stConfigEx.ConfigList[index].dwSecDevUID;
            m_GetSystemConfigExData.dwOpMode                = IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DUAL_HORZCOLLAGE;
            found                                           = TRUE;
        }
        /* Tri Hor Collage */
        else if (bHorizontal && uiNumDisplays == 3 && stConfigEx.ConfigList[index].dwNDisplays == 3)
        {
            /* UID of eDP is 4096
             eDP will excluded for Collage */
            if (stConfigEx.ConfigList[index].dwPriDevUID != 4096 && stConfigEx.ConfigList[index].dwSecDevUID != 4096 && stConfigEx.ConfigList[index].dwThirdDevUID != 4096)
            {
                m_GetSystemConfigExData.DispCfg[1].dwDisplayUID = stConfigEx.ConfigList[index].dwSecDevUID;
                m_GetSystemConfigExData.DispCfg[2].dwDisplayUID = stConfigEx.ConfigList[index].dwThirdDevUID;
                m_GetSystemConfigExData.dwOpMode                = IGFX_DISPLAY_DEVICE_CONFIG_FLAG_TRI_HORZCOLLAGE;
                found                                           = TRUE;
            }
        }
        /* Dual Ver Collage */
        else if (bHorizontal == FALSE && uiNumDisplays == stConfigEx.ConfigList[index].dwNDisplays &&
                 stConfigEx.ConfigList[index].dwOperatingMode == IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DUAL_VERTCOLLAGE)
        {
            m_GetSystemConfigExData.DispCfg[1].dwDisplayUID = stConfigEx.ConfigList[index].dwSecDevUID;
            m_GetSystemConfigExData.dwOpMode                = IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DUAL_VERTCOLLAGE;
            found                                           = TRUE;
        }
        /* Tri Ver Collage */
        else if (bHorizontal == FALSE && uiNumDisplays == 3 && stConfigEx.ConfigList[index].dwNDisplays == 3)
        {
            /* UID of eDP is 4096
            eDP will excluded for Collage */
            if (stConfigEx.ConfigList[index].dwPriDevUID != 4096 && stConfigEx.ConfigList[index].dwSecDevUID != 4096 && stConfigEx.ConfigList[index].dwThirdDevUID != 4096)
            {
                m_GetSystemConfigExData.DispCfg[1].dwDisplayUID = stConfigEx.ConfigList[index].dwSecDevUID;
                m_GetSystemConfigExData.DispCfg[2].dwDisplayUID = stConfigEx.ConfigList[index].dwThirdDevUID;
                m_GetSystemConfigExData.dwOpMode                = IGFX_DISPLAY_DEVICE_CONFIG_FLAG_TRI_VERTCOLLAGE;
                found                                           = TRUE;
            }
        }
        if (found)
        {
            found                               = FALSE;
            m_GetSystemConfigExData.uiSize      = uiSize;
            m_GetSystemConfigExData.dwFlags     = 0;
            m_GetSystemConfigExData.uiNDisplays = uiNumDisplays;
            PFN_APPLYCOLLAGE pApplyCollage      = (PFN_APPLYCOLLAGE)GetProcAddress(handle, "ApplyCollage");
            bStatus                             = ((pApplyCollage)(&m_GetSystemConfigExData));
            if (bStatus != TRUE)
            {
                TRACE_LOG(DEBUG_LOGS, "\n Initialization of Port and DP Object Call Failed!!!!! \n");
            }
        }
    } // End of For loop

    PFN_DISABLECOLLAGEMODE pInitport2 = (PFN_DISABLECOLLAGEMODE)GetProcAddress(handle, "IsCollageEnabled");
    bStatus                           = ((pInitport2)());
    if (bStatus != TRUE)
    {
        TRACE_LOG(DEBUG_LOGS, "\n Initialization of Port and DP Object Call Failed!!!!! \n");
    }
}