#include "CommonMMIO.h"
#include "..\\CommonCore\\PortingLayer.h"
#include "..\\DriverInterfaces\\CommonRxHandlers.h"
#include "Gen9MMIO.h"
#include "Gen10MMIO.h"
#include "Gen11MMIO.h"
#include "Gen11P5MMIO.h"
#include "Gen12\\Gen12CommonMMIO.h"
#include "Gen12\\TGLLPMMIO.h"
#include "Gen12\\RKLMMIO.h"
#include "Gen12\\LKFRMMIO.h"
#include "Gen12\\DG1MMIO.h"
#include "Gen12\\ADLSMMIO.h"
#include "Gen13\\DG2MMIO.h"
#include "Gen13\\ADLPMMIO.h"
#include "Gen14\\MTLMMIO.h"
#include "Gen15\\LNLMMIO.h"
#include "..\\DriverInterfaces\\HDMIHandlers.h"
#include "..\\CommonInclude\\ETWLogging.h"

ULONG COMMONMMIOHANDLERS_GetGenMMIOOffset(PMMIO_INTERFACE pstMMIOInterface, GEN_OFFSET_INDEX eMMIOOffset);

BOOLEAN COMMONMMIOHANDLERS_RegisterMMIOHandlers(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bForceRegister, ULONG ulMMIOStartOffset, ULONG ulMMIOEndOffset,
                                                ULONG ulMMIOInitialState, PVOID pvCallerPersistedData, PVOID pvCallerNonPersistedData, ULONG ulCallerNonPersistedSize,
                                                BOOLEAN bReadHandlerlessRegistration, REGRW_EXEC_SITE eRegReadExecSite, PFN_MMIO_READ_HANDLER pfnMMIOReadHandler,
                                                PFN_MMIO_WRITE_HANDLER pfnMMIOWriteHandler, PFN_MMIO_HANDLER_INITROUTINE pfnMMIOInitRoutine,
                                                PFN_MMIO_HANDLER_UPDATEROUTINE pfnMMIOUpdateRoutine, PFN_MMIO_HANDLER_CLEANUPROUTINE pfnMMIOCleanUpRoutine)
{
    PPORTINGLAYER_OBJ  pstPortingObj      = GetPortingObj();
    BOOLEAN            bRet               = TRUE;
    PMMIO_HANDLER_INFO pstMMIOHandlerInfo = NULL;
    // PDP_LIST_ENTRY pListEntry = NULL;
    ULONG                      ulCount              = 0;
    ULONG                      ulNumCurrentHandlers = 0;
    BOOLEAN                    bAlreadyRegistered   = FALSE;
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData  = &pstMMIOInterface->stGlobalMMORegData;

    do
    {

        ulNumCurrentHandlers = pstMMIOInterface->stMMIOHandlerArr.ulNumRegisteredHandlers;
        pstMMIOHandlerInfo   = pstMMIOInterface->stMMIOHandlerArr.stMMIOHandlerList;

        if (ulNumCurrentHandlers >= MAX_MMMIO_OFFSETS_HANDLED)
        {
            break;
        }

        for (ulCount = 0; ulCount < ulNumCurrentHandlers; ulCount++)
        {
            if (ulMMIOStartOffset >= pstMMIOHandlerInfo[ulCount].ulMMIOStartOffset && ulMMIOEndOffset <= pstMMIOHandlerInfo[ulCount].ulMMIOEndOffset)
            {
                bAlreadyRegistered = TRUE;
                break;
            }
        }

        if (bAlreadyRegistered)
        {
            // The guy registering this MMIO handler wants us to force register the new handler so free up the old
            // Registeration's Info Struct
            if (bForceRegister)
            {
                if (pstMMIOHandlerInfo[ulCount].pfnMMIOCleanUpRoutine)
                {
                    pstMMIOHandlerInfo[ulCount].pfnMMIOCleanUpRoutine(&pstMMIOHandlerInfo[ulCount]);
                }

                pstMMIOInterface->stMMIOHandlerArr.ulNumRegisteredHandlers--;
                pstMMIOHandlerInfo = &pstMMIOHandlerInfo[ulCount];
            }
            else
            {
                break; // break from for loop
            }
        }
        else
        {
            pstMMIOHandlerInfo = &pstMMIOHandlerInfo[ulNumCurrentHandlers];
        }

        if (pstMMIOHandlerInfo == NULL)
        {
            // Registration Failed
            bRet = FALSE;
            break;
        }

        pstMMIOHandlerInfo->ePortType = ePortType;

        if (!pstPortingObj->pfnInitializeDPLock(&pstMMIOHandlerInfo->pMMIOSpinLock))
        {
            bRet = FALSE;
            break;
        }

        pstMMIOHandlerInfo->stGlobalMMORegData    = pstMMIOInterface->stGlobalMMORegData;
        pstMMIOHandlerInfo->ulMMIOStartOffset     = ulMMIOStartOffset;
        pstMMIOHandlerInfo->ulMMIOEndOffset       = ulMMIOEndOffset;
        pstMMIOHandlerInfo->ulMMIOData            = ulMMIOInitialState;
        pstMMIOHandlerInfo->pvCallerPersistedData = pvCallerPersistedData;

        if (bReadHandlerlessRegistration)
        {
            pstMMIOHandlerInfo->bReadHandlerlessRegistration = TRUE;
            pstMMIOHandlerInfo->eRegReadExecSite             = eRegReadExecSite;
        }
        else
        {
            pstMMIOHandlerInfo->pfnMMIOReadHandler = pfnMMIOReadHandler;
        }

        pstMMIOHandlerInfo->pfnMMIOWriteHandler = pfnMMIOWriteHandler;

        for (ulCount = ulMMIOStartOffset; ulCount <= ulMMIOEndOffset; ulCount = ulCount + sizeof(DWORD32))
        {
            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulCount - pstGlobalMMORegData->ulMMIOBaseOffset]) = ulMMIOInitialState;
        }

        if (pfnMMIOInitRoutine)
        {
            pfnMMIOInitRoutine(pstMMIOHandlerInfo, pvCallerNonPersistedData, ulCallerNonPersistedSize);
        }

        pstMMIOHandlerInfo->pfnMMIOUpdateRoutine  = pfnMMIOUpdateRoutine;
        pstMMIOHandlerInfo->pfnMMIOCleanUpRoutine = pfnMMIOCleanUpRoutine;
        pstMMIOInterface->stMMIOHandlerArr.ulNumRegisteredHandlers++;

    } while (FALSE);

    return bRet;
}

BOOLEAN COMMONMMIOHANDLERS_UpdateMMIOInitialStateMMIOHandlers(PMMIO_INTERFACE pstMMIOInterface, ULONG ulMMIOOffset, ULONG ulMMIOInitialState)
{
    PMMIO_HANDLER_INFO         pstMMIOHandlerInfo   = NULL;
    ULONG                      ulCount              = 0;
    ULONG                      ulNumCurrentHandlers = 0;
    BOOLEAN                    bAlreadyRegistered   = FALSE;
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData  = &pstMMIOInterface->stGlobalMMORegData;
    GFXVALSIM_FUNC_ENTRY();

    do
    {
        ulNumCurrentHandlers = pstMMIOInterface->stMMIOHandlerArr.ulNumRegisteredHandlers;
        pstMMIOHandlerInfo   = pstMMIOInterface->stMMIOHandlerArr.stMMIOHandlerList;

        for (ulCount = 0; ulCount < ulNumCurrentHandlers; ulCount++)
        {
            if (ulMMIOOffset >= pstMMIOHandlerInfo[ulCount].ulMMIOStartOffset && ulMMIOOffset <= pstMMIOHandlerInfo[ulCount].ulMMIOEndOffset)
            {
                bAlreadyRegistered = TRUE;
                break;
            }
        }

        if (FALSE == bAlreadyRegistered)
        {
            GFXVALSIM_DBG_MSG("MMIO %d not matched. Registering.", ulMMIOOffset);
            if (FALSE == COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, ulMMIOOffset, ulMMIOOffset, ulMMIOInitialState, NULL, NULL, 0, TRUE, eReadCombine,
                                                                 NULL, NULL, NULL, NULL, NULL))
            {
                GFXVALSIM_DBG_MSG("Registration of MMIO %d failed.", ulMMIOOffset);
            }
            break;
        }

        for (ULONG ulOffset = pstMMIOHandlerInfo[ulCount].ulMMIOStartOffset; ulOffset <= pstMMIOHandlerInfo[ulCount].ulMMIOEndOffset; ulOffset = ulOffset + sizeof(DWORD32))
        {
            if (ulOffset == ulMMIOOffset)
            {
                GFXVALSIM_DBG_MSG("Test MMIO matched %d. val: %d", ulMMIOOffset, ulMMIOInitialState);
                *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = ulMMIOInitialState;
            }
        }

    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(0);
    return TRUE;
}

BOOLEAN COMMONMMIOHANDLERS_InitMMIOInterfaceForPlatform(PMMIO_INTERFACE pstMMIOInterface, PLATFORM_INFO stPlatformInfo)
{
    BOOLEAN           bRet          = TRUE;
    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();

    do
    {
        if (pstMMIOInterface == NULL)
        {
            bRet = FALSE;
            break;
        }

        // This sort of work around can be removed if we could parse VBT in the simulation driver
        if (pstMMIOInterface->bInterfaceInitialized == TRUE)
        {
            break;
        }

        pstMMIOInterface->eIGFXPlatform     = stPlatformInfo.eProductFamily;
        pstMMIOInterface->ePCHProductFamily = stPlatformInfo.ePCHProductFamily;
        pstMMIOInterface->stGfxGmdId.Value  = stPlatformInfo.sDisplayBlockID;

        // Allocate 1MB Data for register file
        pstMMIOInterface->stGlobalMMORegData.ucMMIORegisterFile = pstPortingObj->pfnAllocateMem(GFX_MMIO_FILE_SIZE, TRUE);

        if (pstMMIOInterface->stGlobalMMORegData.ucMMIORegisterFile == NULL)
        {
            bRet = FALSE;
            break;
        }

        pstMMIOInterface->stGlobalMMORegData.ulMMIOBaseOffset = GFX_MMIO_BASE_OFFSET;

        pstMMIOInterface->pulGenMMIOOffsetArray = pstPortingObj->pfnAllocateMem(sizeof(ULONG) * MAX_GEN_MMIO_OFFSETS_STORED, TRUE);

        if (pstMMIOInterface->pulGenMMIOOffsetArray == NULL)
        {
            bRet = FALSE;
            break;
        }

        switch (stPlatformInfo.eProductFamily)
        {
        case eIGFX_SKYLAKE:
        case eIGFX_KABYLAKE:
        case eIGFX_COFFEELAKE:
            bRet = GEN9MMIOHANDLERS_GenSpecificMMIOInitialization(pstMMIOInterface);
            break;

        case eIGFX_CANNONLAKE:
        case eIGFX_CNX_G:
            bRet = GEN10MMIOHANDLERS_GenSpecificMMIOInitialization(pstMMIOInterface);
            break;

        case eIGFX_GEMINILAKE:
            bRet = GEN10LPMMIOHANDLERS_GenSpecificMMIOInitialization(pstMMIOInterface);
            break;

        case eIGFX_ICELAKE_LP:
            bRet = GEN11MMIOHANDLERS_GenSpecificMMIOInitialization(pstMMIOInterface);
            break;

        // Seperating due to DDI-D muxing changes
        case eIGFX_JASPERLAKE:
            bRet = GEN11JSL_MMIOHANDLERS_GenSpecificMMIOInitialization(pstMMIOInterface);
            break;

        case eIGFX_ICELAKE:
        case eIGFX_LAKEFIELD:
        case eIGFX_RYEFIELD:
            bRet = GEN11P5MMIOHANDLERS_GenSpecificMMIOInitialization(pstMMIOInterface);
            break;

        case eIGFX_TIGERLAKE_LP:
        case eIGFX_TIGERLAKE_HP:
            bRet = TGLLP_MMIOHANDLERS_GenSpecificMMIOInitialization(pstMMIOInterface);
            break;
        case eIGFX_ROCKETLAKE:
            bRet = RKL_MMIOHANDLERS_GenSpecificMMIOInitialization(pstMMIOInterface);
            break;
        case eIGFX_LAKEFIELD_R:
            bRet = LKFR_MMIOHANDLERS_GenSpecificMMIOInitialization(pstMMIOInterface);
            break;
        case eIGFX_DG100:
            bRet = DG1_MMIOHANDLERS_GenSpecificMMIOInitialization(pstMMIOInterface);
            break;
        case eIGFX_DG2:
            bRet = DG2_MMIOHANDLERS_GenSpecificMMIOInitialization(pstMMIOInterface);
            break;
        case eIGFX_ALDERLAKE_S:
            bRet = ADLS_MMIOHANDLERS_GenSpecificMMIOInitialization(pstMMIOInterface);
            break;
        case eIGFX_ALDERLAKE_P:
        case eIGFX_ALDERLAKE_N:
            bRet = ADLP_MMIOHANDLERS_GenSpecificMMIOInitialization(pstMMIOInterface);
            break;
        case eIGFX_METEORLAKE:
        case eIGFX_ARROWLAKE:
        case eIGFX_ELG:
            bRet = MTL_MMIOHANDLERS_GenSpecificMMIOInitialization(pstMMIOInterface);
            break;
        case eIGFX_LUNARLAKE:
        case eIGFX_PTL:
        case eIGFX_NVL:
        case IGFX_NVL_XE3G:
        case eIGFX_NVL_AX:
        case eIGFX_CLS:
            bRet = LNL_MMIOHANDLERS_GenSpecificMMIOInitialization(pstMMIOInterface);
            break;
        default:
            bRet = FALSE;
            break;
        }

        if (bRet)
        {
            pstMMIOInterface->bInterfaceInitialized = TRUE;
        }

    } while (FALSE);

    return bRet;
}

BOOLEAN COMMONMMIOHANDLERS_RegisterPlatormBasedGeneralMMIOHandHandlers(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet = TRUE;

    if (pstMMIOInterface->bGeneralMMIOInitalized == FALSE)
    {
        switch (pstMMIOInterface->eIGFXPlatform)
        {
        case eIGFX_SKYLAKE:
        case eIGFX_KABYLAKE:
        case eIGFX_COFFEELAKE:
            if (pstMMIOInterface->ePCHProductFamily == PCH_TGL_H || pstMMIOInterface->ePCHProductFamily == PCH_TGL_LP)
            {
                bRet = RKL_MMIOHANDLERS_RegisterGeneralMMIOHandlers(pstMMIOInterface);
            }
            else
            {
                bRet = GEN9MMIOHANDLERS_RegisterGeneralMMIOHandHandlers(pstMMIOInterface);
            }
            break;

        case eIGFX_CANNONLAKE:
        case eIGFX_CNX_G:
            bRet = GEN10MMIOHANDLERS_RegisterGeneralMMIOHandHandlers(pstMMIOInterface);
            break;

        case eIGFX_GEMINILAKE:
            bRet = GEN10LPMMIOHANDLERS_RegisterGeneralMMIOHandHandlers(pstMMIOInterface);
            break;

        case eIGFX_ICELAKE_LP:
            bRet = GEN11MMIOHANDLERS_RegisterGeneralMMIOHandHandlers(pstMMIOInterface);
            break;

        case eIGFX_JASPERLAKE:
            bRet = GEN11JSL_MMIOHANDLERS_RegisterGeneralMMIOHandHandlers(pstMMIOInterface);
            break;

        case eIGFX_ICELAKE:
        case eIGFX_LAKEFIELD:
        case eIGFX_RYEFIELD:
            bRet = GEN11P5MMIOHANDLERS_RegisterGeneralMMIOHandHandlers(pstMMIOInterface);
            break;
        case eIGFX_TIGERLAKE_LP:
        case eIGFX_TIGERLAKE_HP:
            bRet = TGLLP_MMIOHANDLERS_RegisterGeneralMMIOHandlers(pstMMIOInterface);
            break;
        case eIGFX_ROCKETLAKE:
            if (pstMMIOInterface->ePCHProductFamily == PCH_CMP_H)
            {
                bRet = GEN9MMIOHANDLERS_RegisterGeneralMMIOHandHandlers(pstMMIOInterface);
            }
            else
            {
                bRet = RKL_MMIOHANDLERS_RegisterGeneralMMIOHandlers(pstMMIOInterface);
            }
            break;
        case eIGFX_DG100:
            bRet = DG1_MMIOHANDLERS_RegisterGeneralMMIOHandlers(pstMMIOInterface);
            break;
        case eIGFX_LAKEFIELD_R:
            bRet = LKFR_MMIOHANDLERS_RegisterGeneralMMIOHandlers(pstMMIOInterface);
            break;
        case eIGFX_ALDERLAKE_S:
            bRet = ADLS_MMIOHANDLERS_RegisterGeneralMMIOHandlers(pstMMIOInterface);
            break;
        case eIGFX_DG2:
            bRet = DG2_MMIOHANDLERS_RegisterGeneralMMIOHandlers(pstMMIOInterface);
            break;
        case eIGFX_ALDERLAKE_P:
        case eIGFX_ALDERLAKE_N:
            bRet = ADLP_MMIOHANDLERS_RegisterGeneralMMIOHandlers(pstMMIOInterface);
            break;
        case eIGFX_METEORLAKE:
        case eIGFX_ARROWLAKE:
        case eIGFX_ELG:
            bRet = MTL_MMIOHANDLERS_RegisterGeneralMMIOHandlers(pstMMIOInterface);
            break;
        case eIGFX_LUNARLAKE:
        case eIGFX_PTL:
        case eIGFX_NVL:
        case IGFX_NVL_XE3G:
        case eIGFX_NVL_AX:
        case eIGFX_CLS:
            bRet = MTL_MMIOHANDLERS_RegisterGeneralMMIOHandlers(pstMMIOInterface);
            bRet &= LNL_MMIOHANDLERS_RegisterGeneralMMIOHandlers(pstMMIOInterface);
            break;
        default:
            bRet = FALSE;
            break;
        }

        if (bRet)
        {
            pstMMIOInterface->bGeneralMMIOInitalized = TRUE;
        }
    }

    return bRet;
}

BOOLEAN COMMONMMIOHANDLERS_GetPortAuxRegOffsets(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, PULONG pulDataStartReg, PULONG pulDataEndReg, PULONG pulControlReg)
{
    BOOLEAN bRet = FALSE;

    do
    {
        if (pstMMIOInterface == NULL || pulDataStartReg == NULL || pulDataEndReg == NULL)
        {
            break;
        }

        switch (ePortType)
        {
        case INTDPA_PORT:

            *pulDataStartReg = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_DATA_A_START);
            *pulDataEndReg   = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_DATA_A_END);
            *pulControlReg   = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_CTL_A);
            break;

        case INTDPB_PORT:

            *pulDataStartReg = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_DATA_B_START);
            *pulDataEndReg   = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_DATA_B_END);
            *pulControlReg   = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_CTL_B);
            break;

        case INTDPC_PORT:

            *pulDataStartReg = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_DATA_C_START);
            *pulDataEndReg   = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_DATA_C_END);
            *pulControlReg   = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_CTL_C);
            break;

        case INTDPD_PORT:

            *pulDataStartReg = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_DATA_D_START);
            *pulDataEndReg   = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_DATA_D_END);
            *pulControlReg   = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_CTL_D);
            break;

        case INTDPE_PORT:

            *pulDataStartReg = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_DATA_E_START);
            *pulDataEndReg   = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_DATA_E_END);
            *pulControlReg   = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_CTL_E);
            break;

        case INTDPF_PORT:

            *pulDataStartReg = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_DATA_F_START);
            *pulDataEndReg   = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_DATA_F_END);
            *pulControlReg   = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_CTL_F);
            break;

        case INTDPG_PORT:

            *pulDataStartReg = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_DATA_G_START);
            *pulDataEndReg   = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_DATA_G_END);
            *pulControlReg   = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_CTL_G);
            break;

        case INTDPH_PORT:

            *pulDataStartReg = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_DATA_H_START);
            *pulDataEndReg   = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_DATA_H_END);
            *pulControlReg   = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_CTL_H);
            break;

        case INTDPI_PORT:

            *pulDataStartReg = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_DATA_I_START);
            *pulDataEndReg   = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_DATA_I_END);
            *pulControlReg   = COMMONMMIOHANDLERS_GetGenMMIOOffset(pstMMIOInterface, eINDEX_DDI_AUX_CTL_I);
            break;
        }
        if (*pulDataStartReg != OFFSET_INVALID && *pulDataEndReg != OFFSET_INVALID && *pulControlReg != OFFSET_INVALID)
        {
            bRet = TRUE;
        }

    } while (FALSE);

    return bRet;
}

BOOLEAN COMMONMMIOHANDLERS_RegisterPortAuxHandlers(PMMIO_INTERFACE pstMMIOInterface, PVOID pvCallerPersistedData, PORT_TYPE ePortType)
{
    BOOLEAN bRet           = FALSE;
    ULONG   ulDataStartReg = 0;
    ULONG   ulDataEndReg   = 0;
    ULONG   ulControlReg   = 0;

    // The Init And Cleanup Routines for Aux MMIO Handlers are NULL because the Init and Cleanup of the underlying
    // handler Object AuxInterface is handled through IOCTL interfaces because some memembers like Topology etc
    // are changed via usermode depending on the test cases

    do
    {
        if (pstMMIOInterface == NULL || pvCallerPersistedData == NULL)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_GetPortAuxRegOffsets(pstMMIOInterface, ePortType, &ulDataStartReg, &ulDataEndReg, &ulControlReg);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, ePortType,
                                                       TRUE, // Force Register
                                                       ulDataStartReg, ulDataEndReg, 0, pvCallerPersistedData, NULL, 0, FALSE, eNoExecHw, DPHANDLERS_AuxDataReadHandler,
                                                       DPHANDLERS_AuxDataWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, ePortType,
                                                       TRUE, // Force Register
                                                       ulControlReg, ulControlReg, 0, pvCallerPersistedData, NULL, 0, FALSE, eNoExecHw, DPHANDLERS_AuxControlReadHandler,
                                                       DPHANDLERS_AuxControlWriteHandler, NULL, NULL, NULL);

    } while (FALSE);

    return bRet;
}

ULONG COMMONMMIOHANDLERS_GetGenMMIOOffset(PMMIO_INTERFACE pstMMIOInterface, GEN_OFFSET_INDEX eOffsetIndex)
{
    ULONG ulMMIOOffset = OFFSET_INVALID;

    if (eOffsetIndex < MAX_GEN_MMIO_OFFSETS_STORED && pstMMIOInterface->pulGenMMIOOffsetArray)
    {
        // Below array gets intialized in platform specific MMIO files different for each platform
        ulMMIOOffset = pstMMIOInterface->pulGenMMIOOffsetArray[eOffsetIndex];
    }

    return ulMMIOOffset;
}

BOOLEAN COMMONMMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD,
                                                              PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN bRet = FALSE;
    GFXVALSIM_FUNC_ENTRY();

    switch (pstMMIOInterface->eIGFXPlatform)
    {
    case eIGFX_SKYLAKE:
    case eIGFX_KABYLAKE:
    case eIGFX_COFFEELAKE:
        if (pstMMIOInterface->ePCHProductFamily == PCH_TGL_H || pstMMIOInterface->ePCHProductFamily == PCH_TGL_LP)
        {
            bRet = RKL_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(pstMMIOInterface, ePortType, bAttach, bIsHPD, PortConnectorInfo);
        }
        else
        {
            bRet = GEN9MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(pstMMIOInterface, ePortType, bAttach, bIsHPD);
        }
        break;

    case eIGFX_CANNONLAKE:
        bRet = GEN10MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(pstMMIOInterface, ePortType, bAttach, bIsHPD);
        break;

    case eIGFX_GEMINILAKE:
        bRet = GEN10LPMMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(pstMMIOInterface, ePortType, bAttach, bIsHPD);
        break;

    case eIGFX_CNX_G:
        break;

    case eIGFX_ICELAKE_LP:
        bRet = GEN11MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(pstMMIOInterface, ePortType, bAttach, bIsHPD, PortConnectorInfo);
        break;

    case eIGFX_JASPERLAKE:
        bRet = GEN11JSL_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(pstMMIOInterface, ePortType, bAttach, bIsHPD, PortConnectorInfo);
        break;

    case eIGFX_ICELAKE:
    case eIGFX_LAKEFIELD:
    case eIGFX_RYEFIELD:
        bRet = GEN11P5MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(pstMMIOInterface, ePortType, bAttach, bIsHPD, PortConnectorInfo);
        break;

    case eIGFX_TIGERLAKE_LP:
    case eIGFX_TIGERLAKE_HP:
        bRet = TGLLP_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(pstMMIOInterface, ePortType, bAttach, bIsHPD, PortConnectorInfo);
        break;

    case eIGFX_ROCKETLAKE:
        if (pstMMIOInterface->ePCHProductFamily == PCH_CMP_H)
        {
            bRet = GEN9MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(pstMMIOInterface, ePortType, bAttach, bIsHPD);
        }
        else
        {
            bRet = RKL_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(pstMMIOInterface, ePortType, bAttach, bIsHPD, PortConnectorInfo);
        }
        break;

    case eIGFX_DG100:
        bRet = DG1_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(pstMMIOInterface, ePortType, bAttach, bIsHPD, PortConnectorInfo);
        break;

    case eIGFX_LAKEFIELD_R:
        bRet = LKFR_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(pstMMIOInterface, ePortType, bAttach, bIsHPD, PortConnectorInfo);
        break;

    case eIGFX_ALDERLAKE_S:
        bRet = ADLS_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(pstMMIOInterface, ePortType, bAttach, bIsHPD, PortConnectorInfo);
        break;
    case eIGFX_DG2:
        bRet = DG2_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(pstMMIOInterface, ePortType, bAttach, bIsHPD, PortConnectorInfo);
        break;
    case eIGFX_ALDERLAKE_P:
    case eIGFX_ALDERLAKE_N:
        bRet = ADLP_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(pstMMIOInterface, ePortType, bAttach, bIsHPD, PortConnectorInfo);
        break;
    case eIGFX_METEORLAKE:
    case eIGFX_ARROWLAKE:
    case eIGFX_ELG:
    case eIGFX_LUNARLAKE:
        bRet = MTL_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(pstMMIOInterface, ePortType, bAttach, bIsHPD, PortConnectorInfo);
        break;
    case eIGFX_PTL:
        bRet = PTL_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(pstMMIOInterface, ePortType, bAttach, bIsHPD, PortConnectorInfo);
        break;
    case IGFX_NVL_XE3G:
    case eIGFX_NVL_AX:
    case eIGFX_CLS:
    case eIGFX_NVL:
        bRet = PTL_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(pstMMIOInterface, ePortType, bAttach, bIsHPD, PortConnectorInfo);
        bRet &= NVL_MMIOHANDLERS_SetupIOMRegistersForHPDorSPI(pstMMIOInterface, ePortType, bAttach, bIsHPD, PortConnectorInfo);
        break;
    default:
        bRet = FALSE;
        break;
    }
    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}

BOOLEAN COMMONMMIOHANDLERS_SetupInterruptRegistersForTE(PMMIO_INTERFACE pstMMIOInterface, MIPI_DSI_PORT_TYPE ePortType)
{
    BOOLEAN bRet = FALSE;
    GFXVALSIM_FUNC_ENTRY();

    switch (pstMMIOInterface->eIGFXPlatform)
    {

    case eIGFX_LAKEFIELD:
        bRet = GEN11P5MMIOHANDLERS_SetupInterruptRegistersForTE(pstMMIOInterface, ePortType);
        break;

    default:
        bRet = FALSE;
        break;
    }
    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}

// This function would just set/reset the ISR/Live State register without caring for CTL, IMR or IER registers
// This is especially needed for plugging/Unplugging while S3/S4/Persistence
BOOLEAN COMMONMMIOHANDLERS_SetLiveStateForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN bRet = FALSE;

    switch (pstMMIOInterface->eIGFXPlatform)
    {
    case eIGFX_SKYLAKE:
    case eIGFX_KABYLAKE:
    case eIGFX_COFFEELAKE:
        if (pstMMIOInterface->ePCHProductFamily == PCH_TGL_H || pstMMIOInterface->ePCHProductFamily == PCH_TGL_LP)
        {
            bRet = RKL_MMIOHANDLERS_SetLiveStateForPort(pstMMIOInterface, ePortType, bAttach, PortConnectorInfo);
        }
        else
        {
            bRet = GEN9MMIOHANDLERS_SetLiveStateForPort(pstMMIOInterface, ePortType, bAttach);
        }
        break;

    case eIGFX_CANNONLAKE:
        bRet = GEN10MMIOHANDLERS_SetLiveStateForPort(pstMMIOInterface, ePortType, bAttach);
        break;

    case eIGFX_GEMINILAKE:
        bRet = GEN10LPMMIOHANDLERS_SetLiveStateForPort(pstMMIOInterface, ePortType, bAttach);
        break;

    case eIGFX_CNX_G:
        break;

    case eIGFX_ICELAKE_LP:
        bRet = GEN11MMIOHANDLERS_SetLiveStateForPort(pstMMIOInterface, ePortType, bAttach, PortConnectorInfo);
        break;

    case eIGFX_JASPERLAKE:
        bRet = GEN11JSL_MMIOHANDLERS_SetLiveStateForPort(pstMMIOInterface, ePortType, bAttach, PortConnectorInfo);
        break;

    case eIGFX_ICELAKE:
    case eIGFX_LAKEFIELD:
    case eIGFX_RYEFIELD:
        bRet = GEN11P5MMIOHANDLERS_SetLiveStateForPort(pstMMIOInterface, ePortType, bAttach, PortConnectorInfo);
        break;

    case eIGFX_TIGERLAKE_LP:
    case eIGFX_TIGERLAKE_HP:
        bRet = TGLLP_MMIOHANDLERS_SetLiveStateForPort(pstMMIOInterface, ePortType, bAttach, PortConnectorInfo);
        break;

    case eIGFX_ROCKETLAKE:
        if (pstMMIOInterface->ePCHProductFamily == PCH_CMP_H)
        {
            bRet = GEN9MMIOHANDLERS_SetLiveStateForPort(pstMMIOInterface, ePortType, bAttach);
        }
        else
        {
            bRet = RKL_MMIOHANDLERS_SetLiveStateForPort(pstMMIOInterface, ePortType, bAttach, PortConnectorInfo);
        }
        break;

    case eIGFX_DG100:
        bRet = DG1_MMIOHANDLERS_SetLiveStateForPort(pstMMIOInterface, ePortType, bAttach, PortConnectorInfo);
        break;

    case eIGFX_LAKEFIELD_R:
        bRet = LKFR_MMIOHANDLERS_SetLiveStateForPort(pstMMIOInterface, ePortType, bAttach, PortConnectorInfo);
        break;

    case eIGFX_ALDERLAKE_S:
        bRet = ADLS_MMIOHANDLERS_SetLiveStateForPort(pstMMIOInterface, ePortType, bAttach, PortConnectorInfo);
        break;
    case eIGFX_DG2:
        bRet = DG2_MMIOHANDLERS_SetLiveStateForPort(pstMMIOInterface, ePortType, bAttach, PortConnectorInfo);
        break;
    case eIGFX_ALDERLAKE_P:
    case eIGFX_ALDERLAKE_N:
        bRet = ADLP_MMIOHANDLERS_SetLiveStateForPort(pstMMIOInterface, ePortType, bAttach, PortConnectorInfo);
        break;
    case eIGFX_METEORLAKE:
    case eIGFX_ARROWLAKE:
    case eIGFX_ELG:
    case eIGFX_LUNARLAKE:
        bRet = MTL_MMIOHANDLERS_SetLiveStateForPort(pstMMIOInterface, ePortType, bAttach, PortConnectorInfo);
        break;
    case eIGFX_PTL:
    case eIGFX_NVL:
    case IGFX_NVL_XE3G:
    case eIGFX_NVL_AX:
    case eIGFX_CLS:
        bRet = PTL_MMIOHANDLERS_SetLiveStateForPort(pstMMIOInterface, ePortType, bAttach, PortConnectorInfo);
        break;
    default:
        bRet = FALSE;
        break;
    }

    return bRet;
}

BOOLEAN COMMONMMIOHANDLERS_InvokeUpdateRoutineForOffset(PMMIO_INTERFACE pstMMIOInterface, ULONG ulMMIOOffset, PVOID pvUpdateData)
{
    BOOLEAN            bRet                 = FALSE;
    PMMIO_HANDLER_INFO pstMMIOHandlerInfo   = NULL;
    ULONG              ulNumCurrentHandlers = 0;
    ULONG              ulCount              = 0;
    BOOLEAN            bFound               = FALSE;

    pstMMIOHandlerInfo   = pstMMIOInterface->stMMIOHandlerArr.stMMIOHandlerList;
    ulNumCurrentHandlers = pstMMIOInterface->stMMIOHandlerArr.ulNumRegisteredHandlers;

    for (ulCount = 0; ulCount < ulNumCurrentHandlers; ulCount++)
    {
        if (ulMMIOOffset >= pstMMIOHandlerInfo[ulCount].ulMMIOStartOffset && ulMMIOOffset <= pstMMIOHandlerInfo[ulCount].ulMMIOEndOffset)
        {
            bFound = TRUE;
            break;
        }
    }

    if (bFound)
    {
        pstMMIOHandlerInfo[ulCount].pfnMMIOUpdateRoutine(&pstMMIOHandlerInfo[ulCount], pvUpdateData);
        bRet = TRUE;
    }

    return bRet;
}

BOOLEAN COMMONMMIOHANDLERS_RegisterGMBUSHandlers(PMMIO_INTERFACE pstMMIOInterface, PVOID pvCallerPersistedData, PORT_TYPE ePortType)
{
    BOOLEAN bRet            = FALSE;
    ULONG   ulGMBusStartReg = GMBUS0;
    ULONG   ulGMBusEndReg   = GMBUS5;

    do
    {
        if (pvCallerPersistedData == NULL)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, ePortType,
                                                       TRUE, // FALSE,
                                                       ulGMBusStartReg, ulGMBusEndReg, 0, pvCallerPersistedData, NULL, 0, FALSE, eNoExecHw, HDMIHANDLERS_GMBUSReadHandler,
                                                       HDMIHANDLERS_GMBUSWriteHandler, NULL, NULL, NULL);

    } while (FALSE);

    return bRet;
}

BOOLEAN COMMONMMIOHANDLERS_CleanUp(PMMIO_INTERFACE pstMMIOInterface)
{
    ULONG              ulCount            = 0;
    PMMIO_HANDLER_INFO pstMMIOHandlerInfo = NULL;
    PPORTINGLAYER_OBJ  pstPortingObj      = GetPortingObj();

    // Call Cleanup routines of registered Handlers
    for (ulCount = 0; ulCount < pstMMIOInterface->stMMIOHandlerArr.ulNumRegisteredHandlers; ulCount++)
    {
        pstMMIOHandlerInfo = &pstMMIOInterface->stMMIOHandlerArr.stMMIOHandlerList[ulCount];

        if (pstMMIOHandlerInfo->pfnMMIOCleanUpRoutine)
        {
            pstMMIOHandlerInfo->pfnMMIOCleanUpRoutine(pstMMIOHandlerInfo);
        }
    }

    pstMMIOInterface->stMMIOHandlerArr.ulNumRegisteredHandlers = 0;

    if (pstMMIOInterface->stGlobalMMORegData.ucMMIORegisterFile)
    {
        pstPortingObj->pfnFreeMem(pstMMIOInterface->stGlobalMMORegData.ucMMIORegisterFile);
        pstMMIOInterface->stGlobalMMORegData.ulMMIOBaseOffset   = 0;
        pstMMIOInterface->stGlobalMMORegData.ucMMIORegisterFile = NULL;
    }

    // Cleanup the offset List
    if (pstMMIOInterface->pulGenMMIOOffsetArray)
    {
        pstPortingObj->pfnFreeMem(pstMMIOInterface->pulGenMMIOOffsetArray);
        pstMMIOInterface->pulGenMMIOOffsetArray = NULL;
    }

    return TRUE;
}

// This function is to support eDP Simulation in Gfx Driver Disable/Enable scenario
// This will be called only in Gfx Driver Disable/Enable scenario
// Live State needs to be set in this case
// hence verify is eDP being simulated
// if so call function to set live  state
BOOLEAN COMMONMMIOHANDLERS_VerifyeDPSimulation(PVOID pvRxInfoArr, PVOID pvMMIOInterface)
{
    BOOLEAN             bRet             = TRUE;
    PRX_INFO_ARR        pstRxInfoArr     = NULL;
    PMMIO_INTERFACE     pstMMIOInterface = NULL;
    ULONG               ulCount          = 0;
    PORT_CONNECTOR_INFO ConnectorInfo    = {
        0,
    };

    do
    {
        if (pvRxInfoArr == NULL || pvMMIOInterface == NULL)
        {
            bRet = FALSE;
            break;
        }

        pstRxInfoArr     = pvRxInfoArr;
        pstMMIOInterface = pvMMIOInterface;

        // verify is eDP being simulated
        for (ulCount = 0; ulCount < pstRxInfoArr->ulNumEnumeratedPorts; ulCount++)
        {
            if ((pstRxInfoArr->stRxInfoObj[ulCount].ePortNum == INTDPA_PORT) && (pstRxInfoArr->stRxInfoObj[ulCount].pstDPAuxInterface != NULL))
            {
                // Connector Info will be ZERO as it won't be TC/TBT
                bRet = COMMONMMIOHANDLERS_SetLiveStateForPort(pvMMIOInterface, INTDPA_PORT, TRUE, ConnectorInfo);
                break;
            }
        }

    } while (FALSE);

    return bRet;
}

BOOLEAN COMMONMMIOHANDLERS_SetupScdcInterrupt(PMMIO_INTERFACE pstMMIOInterface, PSCDC_ARGS pstScdcArgs)
{
    BOOLEAN bRet = FALSE;
    GFXVALSIM_FUNC_ENTRY();

    switch (pstMMIOInterface->eIGFXPlatform)
    {
    case eIGFX_TIGERLAKE_LP:
    case eIGFX_TIGERLAKE_HP:
        bRet = TGLLP_MMIOHANDLERS_ScdcInterruptGeneration(pstMMIOInterface, pstScdcArgs);
        break;

    case eIGFX_ROCKETLAKE:
        if (pstMMIOInterface->ePCHProductFamily == PCH_CMP_H)
        {
            // Todo: Add support for CometLake PCH
            // bRet = GEN9MMIOHANDLERS_ScdcInterruptGeneration(pstMMIOInterface, pstScdcArgs);
            bRet = TRUE;
        }
        else
        {
            bRet = RKL_MMIOHANDLERS_ScdcInterruptGeneration(pstMMIOInterface, pstScdcArgs);
        }
        break;

    case eIGFX_DG100:
        bRet = DG1_MMIOHANDLERS_ScdcInterruptGeneration(pstMMIOInterface, pstScdcArgs);
        break;

    case eIGFX_ALDERLAKE_S:
        bRet = ADLS_MMIOHANDLERS_ScdcInterruptGeneration(pstMMIOInterface, pstScdcArgs);
        break;

    case eIGFX_ALDERLAKE_P:
    case eIGFX_ALDERLAKE_N:
        bRet = ADLP_MMIOHANDLERS_ScdcInterruptGeneration(pstMMIOInterface, pstScdcArgs);
        break;

    case eIGFX_DG2:
        bRet = DG2_MMIOHANDLERS_ScdcInterruptGeneration(pstMMIOInterface, pstScdcArgs);
        break;

    case eIGFX_METEORLAKE:
    case eIGFX_ARROWLAKE:
    case eIGFX_ELG:
    case eIGFX_LUNARLAKE:
    case eIGFX_PTL:
    case eIGFX_NVL:
    case IGFX_NVL_XE3G:
    case eIGFX_NVL_AX:
    case eIGFX_CLS:
        bRet = MTL_MMIOHANDLERS_ScdcInterruptGeneration(pstMMIOInterface, pstScdcArgs);
        break;

    default:
        bRet = FALSE;
        break;
    }
    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}
// This function helps enable 2nd eDP over Type-C port
BOOLEAN COMMONMMIOHANDLERS_SetEdpTypeCMappingInfo(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortNum)
{
    BOOLEAN bRet = FALSE;
    GFXVALSIM_FUNC_ENTRY();

    switch (pstMMIOInterface->eIGFXPlatform)
    {
    case eIGFX_SKYLAKE:
    case eIGFX_KABYLAKE:
    case eIGFX_COFFEELAKE:
    case eIGFX_CANNONLAKE:
    case eIGFX_GEMINILAKE:
    case eIGFX_CNX_G:
    case eIGFX_ICELAKE_LP:
    case eIGFX_JASPERLAKE:
    case eIGFX_ICELAKE:
    case eIGFX_LAKEFIELD:
    case eIGFX_RYEFIELD:
    case eIGFX_TIGERLAKE_LP:
    case eIGFX_TIGERLAKE_HP:
    case eIGFX_ROCKETLAKE:
    case eIGFX_DG100:
    case eIGFX_LAKEFIELD_R:
    case eIGFX_ALDERLAKE_S:
    case eIGFX_DG2:
    case eIGFX_ALDERLAKE_P:
    case eIGFX_ALDERLAKE_N:
    case eIGFX_METEORLAKE:
    case eIGFX_ARROWLAKE:
    case eIGFX_ELG:
    case eIGFX_LUNARLAKE:
    case eIGFX_CLS:
        bRet = TRUE;
        break;
    case eIGFX_PTL:
        if (TRUE == GFX_IS_WCL_CONFIG(pstMMIOInterface->stGfxGmdId))
        {
            bRet = TRUE;
            break;
        }

    case eIGFX_NVL:
    case IGFX_NVL_XE3G:
    case eIGFX_NVL_AX:
        bRet = PTL_SetEdpOnTypeC(pstMMIOInterface, ePortNum);
        break;
    default:
        bRet = FALSE;
        break;
    }
    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}
