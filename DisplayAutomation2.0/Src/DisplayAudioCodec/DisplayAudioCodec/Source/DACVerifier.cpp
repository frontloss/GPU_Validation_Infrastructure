#include "..\Header\DisplayAudioCodec.h"
#include "..\Header\DACVerifier.h"

#pragma warning(disable : 4996)

DACVerifier::DACVerifier()
{
    mPinNodeInUse        = -1;
    mDEInUse             = -1;
    mConverterNodeInUse  = -1;
    mConverterIndexInUse = -1;
    mVendorNodeId        = -1;

    mNumWidgets        = 0;
    mNumPinNodes       = 0;
    mNumConverterNodes = 0;

    mDeviceId   = 0;
    mRevisionId = 0;

    memset(mAudioEndpointName, 0, sizeof(mAudioEndpointName));
}

DACVerifier::~DACVerifier()
{
    delete mGfxMMIO;
}

HRESULT DACVerifier::Initialize(WCHAR *pAudioDevName, PORT_TYPE portType, PGFX_ADAPTER_INFO pAdapterInfo)
{
    mPortType = portType;

    mGfxMMIO = new GFXMMIO(pAdapterInfo);

    CreateAudioDeviceName(pAudioDevName);

    HRESULT hr = GetDmaCounters(); // We don't know pin to converter mapping yet. Get initial value of all DMA counters.
    EXIT_ON_ERROR(hr);

    hr = GetDeviceAndRevisionIds();
    EXIT_ON_ERROR(hr);

    hr = ListNodes();
    EXIT_ON_ERROR(hr);

    hr = FindPipeAndTranscoder();
    EXIT_ON_ERROR(hr);

    hr = FindAssociatedPinNode();
    EXIT_ON_ERROR(hr);

Exit:
    if (S_OK != hr)
    {
        ERROR_LOG("%s Could not initialize codec", ERROR_MESSAGE);
    }

    return hr;
}

HRESULT DACVerifier::VerifyDacProgramming(WAVEFORMATEXTENSIBLE *pFmt)
{
    mWaveFmt = *pFmt;

    GetStreamProperties();

    HRESULT hr = FindAssociatedConverterNode();
    EXIT_ON_ERROR(hr);

    hr = VerifyPowerState();
    EXIT_ON_ERROR(hr);

    hr = VerifyConverterProgramming();
    EXIT_ON_ERROR(hr);

    hr = VerifyPinProgramming();
    EXIT_ON_ERROR(hr);

    hr = VerifyAudioInfoFrame();
    EXIT_ON_ERROR(hr);

    hr = VerifyTranscoderConfig();
    EXIT_ON_ERROR(hr);

Exit:
    if (S_OK != hr)
    {
        ERROR_LOG("%s DAC HW is not programmed correctly", ERROR_MESSAGE);
    }

    return hr;
}

HRESULT DACVerifier::VerifyFinalState(UINT64 NumBytesPlayed)
{
    DWORD   lpibRegOffset    = 0;
    HRESULT hr               = S_OK;
    UINT64  counterIncrement = 0;

    if (PORT_TYPE_HDMI == mPortType)
    {
        hr = VerifyOverAndUnderRunHDMI();
    }
    else if (PORT_TYPE_DP == mPortType)
    {
        hr = VerifyOverAndUnderRunDP();
    }

    EXIT_ON_ERROR(hr);

    // TODO: verify silent stream programming, PCM/non-PCM etc

    switch (mConverterIndexInUse)
    {
    case 0:
        lpibRegOffset = AUD_HDA_LPIB0_REG;
        break;
    case 1:
        lpibRegOffset = AUD_HDA_LPIB1_REG;
        break;
    case 2:
        lpibRegOffset = AUD_HDA_LPIB2_REG;
        break;
    case 3:
        lpibRegOffset = AUD_HDA_LPIB3_REG;
        break;
    default:
        INFO_LOG("mConverterIndexInUse (Value = %d) is not in range of 0-3", mConverterIndexInUse);
        hr = S_FALSE;
        break;
    }

    EXIT_ON_ERROR(hr);

    DWORD finalCounterValue;

    hr = mGfxMMIO->MMIORead(lpibRegOffset, &finalCounterValue);
    EXIT_ON_ERROR(hr);

    if (finalCounterValue >= mDmaCounterValuesInitial[mConverterIndexInUse])
    {
        counterIncrement = finalCounterValue - mDmaCounterValuesInitial[mConverterIndexInUse];
    }
    else
    {
        counterIncrement = (UINT64)finalCounterValue + ((UINT64)1 << 32) - mDmaCounterValuesInitial[mConverterIndexInUse];
    }

    // NumBytesPlayed considers 32 bit container. HW plays 24 bit actually.
    if (24 == mWaveFmt.Samples.wValidBitsPerSample)
    {
        NumBytesPlayed = (NumBytesPlayed * 3) / 4;
    }

    if (counterIncrement < NumBytesPlayed)
    {
        ERROR_LOG("%s Played byte count: %d, Counter increment: %d", VERIFICATION_FAILURE, NumBytesPlayed, counterIncrement);
        return E_FAIL;
    }

Exit:
    if (S_OK != hr)
    {
        ERROR_LOG("%s DAC HW is not programmed correctly", ERROR_MESSAGE);
    }
    else
    {
        INFO_LOG("%s Playback verified successfully. Played byte count: %d, Counter increment: %d Panel: %s Port Type %s", VERIFICATION_SUCCESS, NumBytesPlayed, counterIncrement,
                 mAudioEndpointName, (mPortType ? "DP" : "HDMI"));
    }

    return hr;
}

HRESULT DACVerifier::GetDeviceAndRevisionIds()
{
    DWORD   regVal;
    HRESULT hr = mGfxMMIO->MMIORead(AUD_VID_DID_RO, &regVal);

    EXIT_ON_ERROR(hr);

    mDeviceId = regVal & 0xFFFF;

    hr = mGfxMMIO->MMIORead(AUD_RID_RO, &mRevisionId);

Exit:

    if (S_OK != hr)
    {
        ERROR_LOG("%s Could not read VID and RID", ERROR_MESSAGE);
    }

    return hr;
}

HRESULT DACVerifier::ListNodes()
{
    if (mDeviceId >= ICL_DEVICE_ID)
    {
        mVendorNodeId      = 2;
        mNumConverterNodes = 4;

        mConverterNodeIds[0] = 3;
        mConverterNodeIds[1] = 5;
        mConverterNodeIds[2] = 7;
        mConverterNodeIds[3] = 9;

        mPinNodeIds[0] = 4;
        mPinNodeIds[1] = 6;
        mPinNodeIds[2] = 8;
        mPinNodeIds[3] = 0xA;
        mPinNodeIds[4] = 0xB;
    }

    if ((ICL_DEVICE_ID == mDeviceId) || (RKL_DEVICE_ID == mDeviceId))
    {
        mNumPinNodes = 5;
    }
    else if (mDeviceId >= LKF_DEVICE_ID)
    {
        mNumPinNodes = 9;

        mPinNodeIds[5] = 0xC;
        mPinNodeIds[6] = 0xD;
        mPinNodeIds[7] = 0xE;
        mPinNodeIds[8] = 0xF;
    }

    return S_OK;
}

HRESULT DACVerifier::FindAssociatedPinNode()
{
    HRESULT hr = E_NOTFOUND;
    BYTE    MonitoNameString[32];
    DWORD   ConnectedDEs[MAX_NUM_TRANSCODERS];

    for (DWORD i = 0; i < mNumPinNodes; i++)
    {
        DWORD NumConnectedDevice = GetConnectedAudioDeviceCount(mPinNodeIds[i], ConnectedDEs); // MST may have multiple devices connected to one pin

        if ((PORT_TYPE_DP == mPortType) && NumConnectedDevice)
        {
            // TODO: Try to get PinNode by knowing Trancoder to port mapping. We also need to know DE
            if (S_OK == GetELdFromPin(mPinNodeIds[i], mDEInUse))
            {
                memset(MonitoNameString, 0, sizeof(MonitoNameString));
                memcpy(MonitoNameString, mEld.ucMNSAndSADs, mMonitorNameLen);

                if (0 == _stricmp(mAudioEndpointName, (const char *)MonitoNameString))
                {
                    mPinNodeInUse = mPinNodeIds[i];
                    return S_OK;
                }
            }
        }
        else if ((PORT_TYPE_HDMI == mPortType) && NumConnectedDevice)
        {
            if (S_OK == GetELdFromPin(mPinNodeIds[i], 0))
            {
                memset(MonitoNameString, 0, sizeof(MonitoNameString));
                memcpy(MonitoNameString, mEld.ucMNSAndSADs, mMonitorNameLen);

                if (0 == _stricmp(mAudioEndpointName, (const char *)MonitoNameString))
                {
                    mPinNodeInUse = mPinNodeIds[i];
                    mDEInUse      = 0;
                    return S_OK;
                }
            }
        }
    }

    if (S_OK != hr)
    {
        ERROR_LOG("%s %s Device not found", ERROR_MESSAGE, mAudioEndpointName);
    }

    return hr;
}

HRESULT DACVerifier::FindAssociatedConverterNode()
{
    // TODO: Check if AUD_PIPE_CONN_SEL_CTRL works. If so, we don't need verb

    ConnectionListEntryResponseType     ConnListResponse   = { 0 };
    ConnectionSelectControlResponseType ConnSelectResponse = { 0 };

    HRESULT hr = mGfxMMIO->GetSetAudioVerb(mPinNodeInUse, SET_DEVICE_SELECT, mDEInUse, NULL);
    EXIT_ON_ERROR(hr);

    hr = mGfxMMIO->GetSetAudioVerb(mPinNodeInUse, GET_CONNECTION_LIST_ENTRY_VERB_ID, 0, &ConnListResponse.Raw);
    EXIT_ON_ERROR(hr);

    hr = mGfxMMIO->GetSetAudioVerb(mPinNodeInUse, GET_CONN_SELECT_CONTROL_VERB_ID, 0, &ConnSelectResponse.Raw);
    EXIT_ON_ERROR(hr);

    mConverterIndexInUse = ConnSelectResponse.s.ConnectionIndex;
    mConverterNodeInUse  = ConnListResponse.ListEntry[ConnSelectResponse.s.ConnectionIndex];

Exit:

    if (S_OK != hr)
    {
        ERROR_LOG("%s Verb failed while finding converter node", VERIFICATION_FAILURE);
    }

    return hr;
}

HRESULT DACVerifier::FindPipeAndTranscoder()
{
    HRESULT hr = E_NOTFOUND;
    BYTE    MonitoNameString[32];
    BOOL    Endpointnotified[MAX_NUM_TRANSCODERS] = { 0 };

    AUD_PIN_ELD_CP_VLD_ST AUD_PIN_ELD_CP_VLD;

    // Reading 650C0 MMIO
    hr = mGfxMMIO->MMIORead(AUD_PIN_ELD_CP_VLD_REG, (ULONG *)&AUD_PIN_ELD_CP_VLD.ulValue);

    if (AUD_PIN_ELD_CP_VLD.bAudioOutputEnableA == TRUE)
    {
        Endpointnotified[PIPE_A] = TRUE;
    }

    if (AUD_PIN_ELD_CP_VLD.bAudioOutputEnableB == TRUE)
    {
        Endpointnotified[PIPE_B] = TRUE;
    }

    if (AUD_PIN_ELD_CP_VLD.bAudioOutputEnableC == TRUE)
    {
        Endpointnotified[PIPE_C] = TRUE;
    }

    if (AUD_PIN_ELD_CP_VLD.bAudioOutputEnableD == TRUE)
    {
        Endpointnotified[PIPE_D] = TRUE;
    }

    for (DWORD TxId = 0; TxId < MAX_NUM_TRANSCODERS; TxId++)
    {
        hr = GetELdFromTranscoder(TxId);
        EXIT_ON_ERROR(hr);

        memset(MonitoNameString, 0, sizeof(MonitoNameString));
        memcpy(MonitoNameString, mEld.ucMNSAndSADs, mMonitorNameLen);

        if (0 == _stricmp(mAudioEndpointName, (const char *)MonitoNameString) && (Endpointnotified[TxId] == TRUE))
        {
            mTranscoderId = TxId;
            mPipeId       = mTranscoderId; // Pipe and Transcoders have 1:1 connection
            mDEInUse      = mTranscoderId;
            hr            = S_OK;
            break;
        }
    }

Exit:

    if (S_OK != hr)
    {
        ERROR_LOG("%s Could not find transcoder accociated with device", ERROR_MESSAGE);
    }

    return hr;
}

HRESULT DACVerifier::GetELdFromPin(DWORD PinNodeId, DWORD DE)
{
    DpcEldResponseType EldRes           = { 0 };
    PBYTE              pEldDataRawBytes = (PBYTE)&mEld;

    DWORD MnlOffset         = 3;
    DWORD MonitorNameOffset = (DWORD)((UINT64)&mEld.ucMNSAndSADs - (UINT64)&mEld);

    ULONG rawResponse = 0;

    HRESULT hr = mGfxMMIO->GetSetAudioVerb(PinNodeId, SET_DEVICE_SELECT, DE, NULL);
    EXIT_ON_ERROR(hr);

    hr = mGfxMMIO->GetSetAudioVerb(PinNodeId, GET_ELD_DATA_VERB_ID, MnlOffset, &EldRes.Raw);
    EXIT_ON_ERROR(hr);

    if (!EldRes.s.EldValid)
    {
        hr = E_FAIL;
        EXIT_ON_ERROR(hr);
    }

    mEld.Raw[MnlOffset] = (UCHAR)EldRes.s.EldData;

    for (UCHAR i = 0; i < mEld.ucMNL; ++i)
    {
        hr = mGfxMMIO->GetSetAudioVerb(PinNodeId, GET_ELD_DATA_VERB_ID, (i + MonitorNameOffset), &rawResponse);
        EXIT_ON_ERROR(hr);

        EldRes.Raw = rawResponse;

        if (!EldRes.s.EldValid)
        {
            hr = E_FAIL;
            EXIT_ON_ERROR(hr);
        }

        pEldDataRawBytes[i + MonitorNameOffset] = (UCHAR)EldRes.s.EldData;
    }

Exit:

    if (S_OK != hr)
    {
        ERROR_LOG("%s Verb failed while reading ELD", ERROR_MESSAGE);
    }

    return hr;
}

HRESULT DACVerifier::GetELdFromTranscoder(DWORD TxId)
{
    ULONG       ulDWORDToRead = 0, ulOffset = 0;
    PDWORD      pEELD           = (PDWORD)&mEld;
    AUD_CNTL_ST stAudDIPELDCtrl = { 0 };
    DWORD       eldCtlRegOffset = 0;
    DWORD       hdmiEdidReg     = 0;

    switch (TxId)
    {
    case 0:
        eldCtlRegOffset = AUD_DIP_ELD_CTL_TRANSA_REG;
        hdmiEdidReg     = AUD_HDMIW_HDMIEDID_TRANSA_REG;
        break;
    case 1:
        eldCtlRegOffset = AUD_DIP_ELD_CTL_TRANSB_REG;
        hdmiEdidReg     = AUD_HDMIW_HDMIEDID_TRANSB_REG;
        break;
    case 2:
        eldCtlRegOffset = AUD_DIP_ELD_CTL_TRANSC_REG;
        hdmiEdidReg     = AUD_HDMIW_HDMIEDID_TRANSC_REG;
        break;
    case 3:
        eldCtlRegOffset = AUD_DIP_ELD_CTL_TRANSD_REG;
        hdmiEdidReg     = AUD_HDMIW_HDMIEDID_TRANSD_REG;
        break;
    default:
        break;
    }

    HRESULT hr = mGfxMMIO->MMIORead(eldCtlRegOffset, (ULONG *)&stAudDIPELDCtrl.ulValue);
    EXIT_ON_ERROR(hr);

    stAudDIPELDCtrl.ulEldAccessAddress = 0; // Reset ELD access address
    hr                                 = mGfxMMIO->MMIOWrite(eldCtlRegOffset, stAudDIPELDCtrl.ulValue);
    EXIT_ON_ERROR(hr);

    // Data to write is minimal of ELD size and max possible HW ELD buffer size
    ulOffset = 0;

    while (ulOffset < sizeof(ELDV2) / sizeof(DWORD))
    {
        hr = mGfxMMIO->MMIORead(hdmiEdidReg, &pEELD[ulOffset]);
        EXIT_ON_ERROR(hr);

        ulOffset++;
    }

Exit:

    if (S_OK != hr)
    {
        ERROR_LOG("%s ELD read from trancoder register failed", ERROR_MESSAGE);
    }

    // Reset ELD buffer read address.
    mGfxMMIO->MMIORead(eldCtlRegOffset, (ULONG *)&stAudDIPELDCtrl.ulValue);
    stAudDIPELDCtrl.ulEldAccessAddress = 0; // Reset ELD access address
    mGfxMMIO->MMIOWrite(eldCtlRegOffset, stAudDIPELDCtrl.ulValue);

    return hr;
}

DWORD DACVerifier::GetConnectedAudioDeviceCount(DWORD PinNodeId, DWORD DE[MAX_NUM_TRANSCODERS])
{
    DWORD                     NumConnectedevice    = 0;
    DWORD                     devListEntryResponse = 0;
    DpcGetDeviceListEntryType xResponse            = { 0 };

    HRESULT hr = mGfxMMIO->GetSetAudioVerb(PinNodeId, GET_DEVICE_LIST_ENTRY, 0, &devListEntryResponse);

    if (S_OK != hr)
    {
        ERROR_LOG("%s GET_DEVICE_LIST_ENTRY verb failed", ERROR_MESSAGE);
        return NumConnectedevice;
    }

    for (DWORD i = 0; i < 4; i++)
    {
        xResponse.Raw = GET_NIBBLE(devListEntryResponse, i);

        if (xResponse.s.PresenceDetect && xResponse.s.EldValid)
        {
            DE[NumConnectedevice] = i;
            NumConnectedevice++;
        }
    }

    return NumConnectedevice;
}

void DACVerifier::CreateAudioDeviceName(WCHAR *pAudioDevName)
{
    mMonitorNameLen = (DWORD)wcslen(pAudioDevName);
    mMonitorNameLen = min(mMonitorNameLen, 31);

    sprintf(mAudioEndpointName, "%ws", pAudioDevName);

    // Make it a c sting by terminating with null character.
    mAudioEndpointName[mMonitorNameLen] = 0;
}

HRESULT DACVerifier::VerifyTC(DWORD Offset)
{
    AUD_CONFIG audCfg;
    HRESULT    hr = mGfxMMIO->MMIORead(Offset, (ULONG *)&audCfg.ulValue);
    EXIT_ON_ERROR(hr);

    // UpperNValue
    INFO_LOG("AUD_CONFIG: UpperNValue 0x%x ", audCfg.UpperNValue);
    // LowerNValue
    INFO_LOG("AUD_CONFIG: LowerNValue 0x%x ", audCfg.LowerNValue);

    // N value Index
    if (audCfg.NValueIndex == 0x0)
    {
        INFO_LOG("AUD_CONFIG_TRANS: HDMI");
    }
    else
    {
        INFO_LOG("AUD_CONFIG_TRANS: DP");
    }

    // Pixel Clock HDMI
    switch (audCfg.PixelClockHDMI)
    {
    case 0:
        INFO_LOG("AUD_CONFIG_TRANS_HDMI_Pixel: 25.2 / 1.001 MHz");
        break;
    case 1:
        INFO_LOG("AUD_CONFIG_TRANS_HDMI_Pixel: 25.2 MHz");
        break;
    case 2:
        INFO_LOG("AUD_CONFIG_TRANS_HDMI_Pixel: 27 MHz");
        break;
    case 3:
        INFO_LOG("AUD_CONFIG_TRANS_HDMI_Pixel: 27 * 1.001 MHz");
        break;
    case 4:
        INFO_LOG("AUD_CONFIG_TRANS_HDMI_Pixel: 54 MHz");
        break;
    case 5:
        INFO_LOG("AUD_CONFIG_TRANS_HDMI_Pixel: 54 * 1.001 MHz");
        break;
    case 6:
        INFO_LOG("AUD_CONFIG_TRANS_HDMI_Pixel: 74.25 / 1.001 MHz MHz");
        break;
    case 7:
        INFO_LOG("AUD_CONFIG_TRANS_HDMI_Pixel: 74.25 MHz");
        break;
    case 8:
        INFO_LOG("AUD_CONFIG_TRANS_HDMI_Pixel: 148.5 / 1.001 MHz");
        break;
    case 9:
        INFO_LOG("AUD_CONFIG_TRANS_HDMI_Pixel: 148.5 MHz");
        break;
    case 10:
        INFO_LOG("AUD_CONFIG_TRANS_HDMI_Pixel: 297 / 1.001 MHz");
        break;
    case 11:
        INFO_LOG("AUD_CONFIG_TRANS_HDMI_Pixel: 297 MHz");
        break;
    case 12:
        INFO_LOG("AUD_CONFIG_TRANS_HDMI_Pixel: 594 / 1.001 MHz");
        break;
    case 13:
        INFO_LOG("AUD_CONFIG_TRANS_HDMI_Pixel: 594 MHz");
        break;
    default:
        break;
    }

Exit:

    if (S_OK != hr)
    {
        ERROR_LOG("%s Failed to read AUD_CONFIG register", ERROR_MESSAGE);
    }

    return hr;
}

// AUD_CONFIG2 . 65004h/65104h/65204h/65304h

HRESULT DACVerifier::VerifyTC2(DWORD Offset)
{
    AUD_CONFIG2 audCfg2;

    HRESULT hr = mGfxMMIO->MMIORead(Offset, (ULONG *)&audCfg2.ulValue);
    EXIT_ON_ERROR(hr);

    // Upper bits for MCTS value
    INFO_LOG("AUD_CONFIG_TRANS: AudTCACfg2.UpperBitsMCTSValue 0x%x ", audCfg2.UpperBitsMCTSValue);
    // Upper bits for N value
    INFO_LOG("AUD_CONFIG_TRANS: AudTCACfg2.UpperBitsNValue 0x%x ", audCfg2.UpperBitsNValue);
    // DPSpecVersion
    INFO_LOG("AUD_CONFIG_TRANS: AudTCACfg2.DPSpecVersion 0x%x ", audCfg2.DPSpecVersion);

    // N value Index
    if (audCfg2.DisableHBlankOverFlowFix == 0x0)
    {
        INFO_LOG("Hblank overflow fix enabled");
    }
    else
    {
        INFO_LOG("Hblank overflow fix not enabled");
    }

Exit:

    if (S_OK != hr)
    {
        ERROR_LOG("%s Failed to read AUD_CONFIG2 register", ERROR_MESSAGE);
    }

    return hr;
}

HRESULT DACVerifier::VerifyMCTS(DWORD Offset)
{
    AUD_M_CTS AudMCTS;

    HRESULT hr = mGfxMMIO->MMIORead(Offset, (ULONG *)&AudMCTS.ulValue);
    EXIT_ON_ERROR(hr);

    // Audio M or CTS values
    INFO_LOG("AUD_M_CTS: AudMCTS.Audio M or CTS values 0x%x ", AudMCTS.AudioCTSValues);

Exit:
    if (S_OK != hr)
    {
        ERROR_LOG("%s Failed to Read AudioMCTS registers", ERROR_MESSAGE);
    }

    return hr;
}

// Audio MCTS Enable

HRESULT DACVerifier::VerifyMCTSEnable(DWORD Offset)
{
    AUD_M_CTS_ENABLE AudMCTSEnable;

    HRESULT hr = mGfxMMIO->MMIORead(Offset, (ULONG *)&AudMCTSEnable.ulValue);
    EXIT_ON_ERROR(hr);

    // CTS Programming
    INFO_LOG("AUD_M_CTS_Enable: AudMCTSEnable.AudioCTSvalues 0x%x ", AudMCTSEnable.CTSProgramming);
    // Enable CTS or M prog
    INFO_LOG("AUD_M_CTS_Enable: AudMCTSEnable.Audio M or CTS values 0x%x ", AudMCTSEnable.EnableCTSORM);

    // CTS M value Index

    if (AudMCTSEnable.CTSMValueIndex == 0x0)
    {
        INFO_LOG("CTS value index Enabled");
    }
    else
    {
        INFO_LOG("M Value index is Enabled ");
    }

Exit:
    if (S_OK != hr)
    {
        ERROR_LOG("%s Failed to Read AudioMCTSEnable registers", ERROR_MESSAGE);
    }

    return hr;
}

HRESULT DACVerifier::VerifyConfigBE()
{
    AUD_CONFIG_BE AudConfigBE;

    HRESULT hr = mGfxMMIO->MMIORead(AUD_CONFIG_BE_REG, (ULONG *)&AudConfigBE.ulValue);
    EXIT_ON_ERROR(hr);

    INFO_LOG("AudConfigBE register value: 0x%x", AudConfigBE.ulValue);

    switch (mPipeId)
    {
    case 0:
        INFO_LOG("AudConfigBE register DelaySampleCountLatchPipeA: 0x%x ", AudConfigBE.DelaySampleCountLatchPipeA);
        INFO_LOG("AudConfigBE register DPMixerMainStreamPpriorityEnablePipeA: 0x%x", AudConfigBE.DPMixerMainStreamPpriorityEnablePipeA);
        INFO_LOG("AudConfigBE register HBlankEarlyEnablePipeA: 0x%x", AudConfigBE.HBlankEarlyEnablePipeA);
        INFO_LOG("AudConfigBE register HBlankStartCountPipeA: 0x%x", AudConfigBE.HBlankStartCountPipeA);
        INFO_LOG("AudConfigBE register NumberofSamplesPerLinePipeA: 0x%x", AudConfigBE.NumberofSamplesPerLinePipeA);
        break;
    case 1:
        INFO_LOG("AudConfigBE register DelaySampleCountLatchPipeB: 0x%x ", AudConfigBE.DelaySampleCountLatchPipeB);
        INFO_LOG("AudConfigBE register DPMixerMainstreamPriorityEnablePipeB: 0x%x", AudConfigBE.DPMixerMainstreamPriorityEnablePipeB);
        INFO_LOG("AudConfigBE register HBlankEarlyEnablePipeB: 0x%x", AudConfigBE.HBlankEarlyEnablePipeB);
        INFO_LOG("AudConfigBE register HBlankStartCountPipeB: 0x%x", AudConfigBE.HBlankStartCountPipeB);
        INFO_LOG("AudConfigBE register NumberofSamplesPerLinePipeB: 0x%x", AudConfigBE.NumberofSamplesPerLinePipeB);
        break;
    case 2:
        INFO_LOG("AudConfigBE register DelaySampleCountLatchPipeC: 0x%x ", AudConfigBE.DelaySampleCountLatchPipeC);
        INFO_LOG("AudConfigBE register DPMixerMainstreamPriorityEnablePipeC: 0x%x", AudConfigBE.DPMixerMainstreamPriorityEnablePipeC);
        INFO_LOG("AudConfigBE register HBlankEarlyEnablePipeC: 0x%x", AudConfigBE.HBlankEarlyEnablePipeC);
        INFO_LOG("AudConfigBE register HBlankStartCountPipeC: 0x%x", AudConfigBE.HBlankStartCountPipeC);
        INFO_LOG("AudConfigBE register NumberofSamplesPerLinePipeC: 0x%x", AudConfigBE.NumberofSamplesPerLinePipeC);
    case 3:
        INFO_LOG("AudConfigBE register DelaySampleCountLatchPipeD: 0x%x ", AudConfigBE.DelaysampleCountLatchPipeD);
        INFO_LOG("AudConfigBE register DPMixerMainstreamPriorityEnablePipeD: 0x%x", AudConfigBE.DPMixerMainstreamPriorityEnablePipeD);
        INFO_LOG("AudConfigBE register HBlankEarlyEnablePipeD: 0x%x", AudConfigBE.HBlankEnablePipeD);
        INFO_LOG("AudConfigBE register HBlankStartCountPipeD: 0x%x", AudConfigBE.HBlankStartCountPipeD);
        INFO_LOG("AudConfigBE register NumberofSamplesPerLinePipeD: 0x%x", AudConfigBE.NumberofSamplesPerLinePipeD);
        break;
    default:
        break;
    }

Exit:

    if (S_OK != hr)
    {
        ERROR_LOG("%s Failed to Read AUD_CONFIG_BE registers", ERROR_MESSAGE);
    }

    // TODO : Yet to complete the function , need to logic from Bit 24 to 31..
    // CTS M value Index
    // TODO.

    return hr;
}

HRESULT DACVerifier::VerifyTranscoderConfig()
{
    HRESULT hr                  = S_OK;
    DWORD   cfgRegOffset        = 0;
    DWORD   cfg2RegOffset       = 0;
    DWORD   mCtsRegOffset       = 0;
    DWORD   mCtsEnableRegOffset = 0;

    switch (mTranscoderId)
    {
    case 0:
        cfgRegOffset        = AUD_CONFIG_TRANSA;
        cfg2RegOffset       = AUD_CONFIG_2_TRANSA;
        mCtsRegOffset       = Audio_M_CTS_TCA;
        mCtsEnableRegOffset = AUD_TCA_M_CTS_ENABLE;
        break;
    case 1:
        cfgRegOffset        = AUD_CONFIG_TRANSB;
        cfg2RegOffset       = AUD_CONFIG_2_TRANSB;
        mCtsRegOffset       = Audio_M_CTS_TCB;
        mCtsEnableRegOffset = AUD_TCB_M_CTS_ENABLE;
        break;
    case 2:
        cfgRegOffset        = AUD_CONFIG_TRANSC;
        cfg2RegOffset       = AUD_CONFIG_2_TRANSC;
        mCtsRegOffset       = Audio_M_CTS_TCC;
        mCtsEnableRegOffset = AUD_TCC_M_CTS_ENABLE;
        break;
    case 3:
        cfgRegOffset        = AUD_CONFIG_TRANSD;
        cfg2RegOffset       = AUD_CONFIG_2_TRANSD;
        mCtsRegOffset       = Audio_M_CTS_TCD;
        mCtsEnableRegOffset = AUD_TCD_M_CTS_ENABLE;
        break;
    default:
        break;
    }

    hr = VerifyTC(cfgRegOffset);
    EXIT_ON_ERROR(hr);

    hr = VerifyTC2(cfg2RegOffset);
    EXIT_ON_ERROR(hr);

    hr = VerifyMCTS(mCtsRegOffset);
    EXIT_ON_ERROR(hr);

    hr = VerifyMCTSEnable(mCtsEnableRegOffset);
    EXIT_ON_ERROR(hr);

    hr = VerifyConfigBE();
    EXIT_ON_ERROR(hr);

Exit:
    return hr;
}

HRESULT DACVerifier::VerifyConverterProgramming()
{
    DWORD cnvRegOffset        = 0;
    DWORD streamDescRegOffset = 0;
    DWORD miscCtrRegOffset    = 0;
    DWORD StreamId            = 0;
    DWORD samplingRateBase, samplingRateMultiplier, samplingRateDivisor;

    AUD_DIG_CNVT      cvtCfg  = { 0 };
    AUD_PIPE_CONV_CFG pcvtCfg = { 0 };
    AUD_STR_DESC      strDesc = { 0 };
    AUD_MISC_CTRL     miscCtl = { 0 };
    AUD_PIPE_CONV_CFG pipeCfg = { 0 };
    BOOL              digEn   = FALSE;

    HRESULT hr = mGfxMMIO->MMIORead(AUD_PIPE_CONV_CFG_RO_REG, (DWORD *)&pcvtCfg.ulValue);
    EXIT_ON_ERROR(hr);

    switch (mConverterIndexInUse)
    {
    case 0:
        StreamId            = pcvtCfg.Convertor1StreamID;
        streamDescRegOffset = AUD_C1_STR_DESC_RO_REG;
        cnvRegOffset        = AUD_C1_DIG_CNVT_RO_REG;
        miscCtrRegOffset    = AUD_C1_MISC_CTRL;
        break;
    case 1:
        StreamId            = pcvtCfg.Convertor2StreamID;
        streamDescRegOffset = AUD_C2_STR_DESC_RO_REG;
        cnvRegOffset        = AUD_C2_DIG_CNVT_RO_REG;
        miscCtrRegOffset    = AUD_C2_MISC_CTRL;
        break;
    case 2:
        StreamId            = pcvtCfg.Convertor3StreamID;
        streamDescRegOffset = AUD_C3_STR_DESC_RO_REG;
        cnvRegOffset        = AUD_C3_DIG_CNVT_RO_REG;
        miscCtrRegOffset    = AUD_C3_MISC_CTRL;
        break;
    case 3:
        StreamId            = pcvtCfg.Convertor4StreamID;
        streamDescRegOffset = AUD_C4_STR_DESC_RO_REG;
        cnvRegOffset        = AUD_C4_DIG_CNVT_RO_REG;
        miscCtrRegOffset    = AUD_C4_MISC_CTRL;
        break;
    default:
        break;
    }

    if ((mDeviceId == TGL_DEVICE_ID) || (mDeviceId == RKL_DEVICE_ID) || (mDeviceId == ADL_DEVICE_ID) || (mDeviceId == DG1_DEVICE_ID))
    {
        switch (mPipeId)
        {
        case 0:
            miscCtrRegOffset = AUD_C1_MISC_CTRL;
            break;
        case 1:
            miscCtrRegOffset = AUD_C2_MISC_CTRL;
            break;
        case 2:
            miscCtrRegOffset = AUD_C3_MISC_CTRL;
            break;
        case 3:
            miscCtrRegOffset = AUD_C4_MISC_CTRL;
            break;
        default:
            break;
        }
    }

    hr = mGfxMMIO->MMIORead(cnvRegOffset, (DWORD *)&cvtCfg.ulValue);
    EXIT_ON_ERROR(hr);

    hr = mGfxMMIO->MMIORead(streamDescRegOffset, (DWORD *)&strDesc.ulValue);
    EXIT_ON_ERROR(hr);

    hr = mGfxMMIO->MMIORead(miscCtrRegOffset, (DWORD *)&miscCtl.ulValue);
    EXIT_ON_ERROR(hr);

    hr = mGfxMMIO->MMIORead(AUD_PIPE_CONV_CFG_RO, (DWORD *)&pipeCfg.ulValue);
    EXIT_ON_ERROR(hr);

    if ((0 == cvtCfg.StreamId) || (15 == cvtCfg.StreamId))
    {
        ERROR_LOG("%s Incorrect stream id (%d), converterIndex: %d, Pipe: %d", VERIFICATION_FAILURE, cvtCfg.StreamId, mConverterIndexInUse, mPipeId);
        return ERROR_INVALID_STATE;
    }

    if ((mDeviceId == ICL_DEVICE_ID) || (mDeviceId == JSL_DEVICE_ID) || (mDeviceId == EHL_DEVICE_ID))
    {
        // TODO: Need to skip silent stream verification for disconnected ports.
        // Need to have new sequence for Gen 11, currently disabling the silent stream check for ICL/JSL/EHL
        INFO_LOG("Skipping Silent stream (sample fabrication) verification, converterIndex: %d, Pipe: %d", mConverterIndexInUse, mPipeId);
    }
    else
    {
        if (0 == miscCtl.SampleFabricationEN)
        {
            INFO_LOG("%s Silent stream (sample fabrication) disabled, converterIndex: %d, Pipe: %d", VERIFICATION_FAILURE, mConverterIndexInUse, mPipeId);
            return ERROR_INVALID_STATE;
        }
    }

    switch (mConverterIndexInUse)
    {
    case 0:
        digEn = pipeCfg.ConverterADigen;
        break;
    case 1:
        digEn = pipeCfg.ConverterBDigen;
        break;
    case 2:
        digEn = pipeCfg.ConverterCDigen;
        break;
    case 3:
        digEn = pipeCfg.ConverterDDigen;
        break;
    default:
        break;
    }

    if (FALSE == digEn)
    {
        ERROR_LOG("%s DigEn disabled, converter: %d", VERIFICATION_FAILURE, mConverterNodeInUse);
        return ERROR_INVALID_STATE;
    }

    if (0 != cvtCfg.ChannelIndex)
    {
        ERROR_LOG("%s Incorrect channel index (%d), converter: %d", VERIFICATION_FAILURE, cvtCfg.ChannelIndex, mConverterNodeInUse);
        return ERROR_INVALID_STATE;
    }

    if (CONVERTER_STREAM_TYPE_PCM == mStreamType)
    {
        if (cvtCfg.NonPCM)
        {
            ERROR_LOG("%s Non-PCM format, converter: %d", VERIFICATION_FAILURE, mConverterNodeInUse);
            return ERROR_INVALID_STATE;
        }
    }
    else if (!cvtCfg.NonPCM)
    {
        ERROR_LOG("%s PCM format programmed, converter: %d", VERIFICATION_FAILURE, mConverterNodeInUse);
        return ERROR_INVALID_STATE;
    }

    hr = GetSampligRateBaseMultDivFactors(samplingRateBase, samplingRateMultiplier, samplingRateDivisor);
    EXIT_ON_ERROR(hr);

    if (samplingRateBase != strDesc.BaseSamplingRate)
    {
        ERROR_LOG("%s Incorrect sampling rate base %d, converter: %d", VERIFICATION_FAILURE, strDesc.BaseSamplingRate, mConverterNodeInUse);
        return ERROR_INVALID_STATE;
    }

    if (samplingRateMultiplier != strDesc.SamplingRateMultiplier)
    {
        ERROR_LOG("%s Incorrect sampling rate multiplier %d, converter: %d", VERIFICATION_FAILURE, strDesc.SamplingRateMultiplier, mConverterNodeInUse);
        return ERROR_INVALID_STATE;
    }

    if (samplingRateDivisor != strDesc.SamplingRateDivisor)
    {
        ERROR_LOG("%s Incorrect sampling rate divisor %d, converter: %d", VERIFICATION_FAILURE, strDesc.SamplingRateDivisor, mConverterNodeInUse);
        return ERROR_INVALID_STATE;
    }

    if (((16 == mWaveFmt.Samples.wValidBitsPerSample) && (BITS_PER_SAMPLE_16 != strDesc.BitsPerSample)) ||
        ((24 == mWaveFmt.Samples.wValidBitsPerSample) && (BITS_PER_SAMPLE_24 != strDesc.BitsPerSample)))
    {
        ERROR_LOG("%s Incorrect bits per sample enum (%d), converter: %d", VERIFICATION_FAILURE, strDesc.BitsPerSample, mConverterNodeInUse);
    }

    if ((1 + strDesc.ChannelCount) != mWaveFmt.Format.nChannels)
    {
        ERROR_LOG("%s Incorrect #channels: %d, converter: %d", VERIFICATION_FAILURE, (1 + strDesc.ChannelCount), mConverterNodeInUse);
        return ERROR_INVALID_STATE;
    }

Exit:
    if (S_OK != hr)
    {
        ERROR_LOG("%s Could not read AUD_Cx_DIG_CNVT_RO register", ERROR_MESSAGE);
    }

    return hr;
}

HRESULT DACVerifier::VerifyPinProgramming()
{
    AmplifierGainMutePayload   gainMutePayload   = { 0 };
    AmplifierGainMuteResponse  gainMuteRespLeft  = { 0 };
    AmplifierGainMuteResponse  gainMuteRespRight = { 0 };
    PinWidgetControlParamsType pinCtrl           = { 0 };

    gainMutePayload.s.GetOutputInput = 1;
    gainMutePayload.s.GetLeftRight   = 0;

    HRESULT hr = mGfxMMIO->GetSetAudioVerb(mPinNodeInUse, SET_DEVICE_SELECT, mDEInUse, NULL);
    EXIT_ON_ERROR(hr);

    hr = mGfxMMIO->GetSetAudioVerb(mPinNodeInUse, GET_AMPLIFIER_GAIN_MUTE, gainMutePayload.Raw, &gainMuteRespRight.Raw);
    EXIT_ON_ERROR(hr);

    gainMutePayload.s.GetLeftRight = 1;
    hr                             = mGfxMMIO->GetSetAudioVerb(mPinNodeInUse, GET_AMPLIFIER_GAIN_MUTE, gainMutePayload.Raw, &gainMuteRespLeft.Raw);
    EXIT_ON_ERROR(hr);

    hr = mGfxMMIO->GetSetAudioVerb(mPinNodeInUse, GET_PIN_WIDGET_CONTROL_VERB_ID, 0, &pinCtrl.Raw);
    EXIT_ON_ERROR(hr);

    if (gainMuteRespLeft.s.AmplifierMute)
    {
        ERROR_LOG("%s Left amplifier muted, pin: %d, DE: %d", VERIFICATION_FAILURE, mPinNodeInUse, mDEInUse);
        return ERROR_INVALID_STATE;
    }

    if (gainMuteRespRight.s.AmplifierMute)
    {
        ERROR_LOG("%s Right amplifier muted, pin: %d, DE: %d", VERIFICATION_FAILURE, mPinNodeInUse, mDEInUse);
        return ERROR_INVALID_STATE;
    }

    // TODO: We are getting this disabled. Check with Intel DAC
    /*if (!pinCtrl.digital.InEnable)
    {
        INFO_LOG("%s Input muted, pin: %d, DE: %d", VERIFICATION_FAILURE, mPinNodeInUse, mDEInUse);
        return ERROR_INVALID_STATE;
    }*/

    if (!pinCtrl.digital.OutEnable)
    {
        ERROR_LOG("%s Output muted, pin: %d, DE: %d", VERIFICATION_FAILURE, mPinNodeInUse, mDEInUse);
        return ERROR_INVALID_STATE;
    }

    if ((CONVERTER_STREAM_TYPE_NONPCM_HBR == mStreamType) && (3 != pinCtrl.digital.EPT))
    {
        ERROR_LOG("%s Incorrect EPT: %d for HBR non PCM stream, pin: %d, DE: %d", VERIFICATION_FAILURE, pinCtrl.digital.EPT, mPinNodeInUse, mDEInUse);
        return ERROR_INVALID_STATE;
    }

    if ((CONVERTER_STREAM_TYPE_NONPCM_HBR != mStreamType) && (0 != pinCtrl.digital.EPT))
    {
        ERROR_LOG("%s Incorrect EPT: %d for non HBR stream, pin: %d, DE: %d", VERIFICATION_FAILURE, pinCtrl.digital.EPT, mPinNodeInUse, mDEInUse);
        return ERROR_INVALID_STATE;
    }

    hr = VerifyAspChannelMapping();

Exit:
    if (S_OK != hr)
    {
        ERROR_LOG("%s Verb failed during verifying pin: %d programming", VERIFICATION_FAILURE, mPinNodeInUse);
    }

    return hr;
}

HRESULT DACVerifier::VerifyAspChannelMapping()
{
    DWORD                    mappedChannelIndex[MAX_NUM_CHANNEL] = { 0 };
    ASPChannelMappingResp    channelMapResp                      = { 0 };
    ASPChannelMappingPayload payload                             = { 0 };

    for (UCHAR i = 0; i < MAX_NUM_CHANNEL; ++i)
    {
        mappedChannelIndex[i] = 0xF;
    }

    // Map OS settings to h/w ASP slots
    switch (mChannelMask)
    {
    case KSAUDIO_SPEAKER_STEREO:
        mappedChannelIndex[0] = 0; // LL LL LR RR RR
        mappedChannelIndex[1] = 1;
        break;

    case KSAUDIO_SPEAKER_QUAD:
        mappedChannelIndex[0] = 0x0;
        mappedChannelIndex[1] = 0x1;
        mappedChannelIndex[4] = 0x2;
        mappedChannelIndex[5] = 0x3;
        break;

    case KSAUDIO_SPEAKER_SURROUND:
        mappedChannelIndex[0] = 0x0; // LcC CcC CcC CcC CcR
        mappedChannelIndex[1] = 0x1;
        mappedChannelIndex[3] = 0x2;
        mappedChannelIndex[4] = 0x3;
        break;

    case KSAUDIO_SPEAKER_3POINT1:
        mappedChannelIndex[0] = 0x0; // LcC CcC CcC CcC CcR
        mappedChannelIndex[1] = 0x1;
        mappedChannelIndex[2] = 0x3;
        mappedChannelIndex[3] = 0x2;
        break;

    case KSAUDIO_SPEAKER_5POINT1:
    case KSAUDIO_SPEAKER_5POINT1_SURROUND:
        mappedChannelIndex[0] = 0x0;
        mappedChannelIndex[1] = 0x1;
        mappedChannelIndex[2] = 0x3;
        mappedChannelIndex[3] = 0x2;
        mappedChannelIndex[4] = 0x4;
        mappedChannelIndex[5] = 0x5;
        break;

    case KSAUDIO_SPEAKER_7POINT1:
        mappedChannelIndex[0] = 0x0;
        mappedChannelIndex[1] = 0x1;
        mappedChannelIndex[2] = 0x3;
        mappedChannelIndex[3] = 0x2;
        mappedChannelIndex[4] = 0x4;
        mappedChannelIndex[5] = 0x5;
        mappedChannelIndex[6] = 0x6;
        mappedChannelIndex[7] = 0x7;
        break;

    case KSAUDIO_SPEAKER_7POINT1_SURROUND:
        mappedChannelIndex[0] = 0x0;
        mappedChannelIndex[1] = 0x1;
        mappedChannelIndex[2] = 0x3;
        mappedChannelIndex[3] = 0x2;
        mappedChannelIndex[4] = 0x6;
        mappedChannelIndex[5] = 0x7;
        mappedChannelIndex[6] = 0x4;
        mappedChannelIndex[7] = 0x5;
        break;

    default:
        break;
    }

    HRESULT hr = mGfxMMIO->GetSetAudioVerb(mPinNodeInUse, SET_DEVICE_SELECT, mDEInUse, NULL);
    EXIT_ON_ERROR(hr);

    for (UCHAR i = 0; i < MAX_NUM_CHANNEL; ++i)
    {
        payload.s.ASPSlotNumber = i;
        hr                      = mGfxMMIO->GetSetAudioVerb(mPinNodeInUse, GET_ASP_CHANNEL_MAPPING_VERB_ID, payload.Raw, &channelMapResp.Raw);
        EXIT_ON_ERROR(hr);

        if (mappedChannelIndex[i] != channelMapResp.s.ChannelNumber)
        {
            ERROR_LOG("%s Incorrect Channel mapping. Expected %d, Programmed: %d, pin: %d, DE: %d", VERIFICATION_FAILURE, mappedChannelIndex[i], channelMapResp.s.ChannelNumber,
                      mPinNodeInUse, mDEInUse);

            return ERROR_INVALID_STATE;
        }
    }

Exit:
    if (S_OK != hr)
    {
        ERROR_LOG("%s Could not read AUD_OUT_CHAN_MAP register", VERIFICATION_FAILURE);
    }

    return hr;
}

HRESULT DACVerifier::VerifyPowerState()
{
    AUD_PWRST_RO           pWrState;
    DWORD                  converterPowerState  = 3;
    PowerStateResponseType pwrStateVerbResponse = { 0 };
    HRESULT                hr                   = mGfxMMIO->MMIORead(AUD_PWRST_REG, (DWORD *)&pWrState.ulValue);
    EXIT_ON_ERROR(hr);

    if (0 != pWrState.FuncGrpDevPwrStCurr)
    {
        ERROR_LOG("%s AFG is not in D0 state", VERIFICATION_FAILURE);
        return ERROR_INVALID_STATE;
    }

    switch (mConverterIndexInUse)
    {
    case 0:
        converterPowerState = pWrState.Convertor1WidgetPwrStCurr;
        break;
    case 1:
        converterPowerState = pWrState.Convertor2WidgetPwrStCurr;
        break;
    case 2:
        converterPowerState = pWrState.Converter3WidgetPwrStCurr;
        break;
    case 3:
        converterPowerState = pWrState.Converter4WidgetPwrStCurr;
        break;
    default:
        break;
    }

    if (0 != converterPowerState)
    {
        ERROR_LOG("%s Converter node %d is not in D0 state", VERIFICATION_FAILURE, mConverterNodeInUse);
        return ERROR_INVALID_STATE;
    }

    hr = mGfxMMIO->GetSetAudioVerb(mPinNodeInUse, GET_POWER_STATE_VERB_ID, 0, &pwrStateVerbResponse.Raw);
    EXIT_ON_ERROR(hr);

    if (0 != pwrStateVerbResponse.s.PSSet)
    {
        ERROR_LOG("%s Pin node %d is not in D0 state", VERIFICATION_FAILURE, mPinNodeInUse);
        return ERROR_INVALID_STATE;
    }

Exit:
    if (S_OK != hr)
    {
        ERROR_LOG("%s Could not get power state of widgets", VERIFICATION_FAILURE);
    }

    return hr;
}

HRESULT DACVerifier::VerifyAudioInfoFrame()
{
    ULONG       ulOffset        = 0;
    DWORD       infoFrame[4]    = { 0 };
    AUD_CNTL_ST stAudDIPELDCtrl = { 0 };
    DWORD       dipCtlRegOffset = 0;
    DWORD       infoFrameReg    = 0;
    PBYTE       pInfoFrameRead  = NULL;

    switch (mTranscoderId)
    {
    case 0:
        dipCtlRegOffset = AUD_DIP_ELD_CTL_TRANSA_REG;
        infoFrameReg    = AUD_TCA_INFOFR_REG;
        break;
    case 1:
        dipCtlRegOffset = AUD_DIP_ELD_CTL_TRANSB_REG;
        infoFrameReg    = AUD_TCB_INFOFR_REG;
        break;
    case 2:
        dipCtlRegOffset = AUD_DIP_ELD_CTL_TRANSC_REG;
        infoFrameReg    = AUD_TCC_INFOFR_REG;
        break;
    case 3:
        dipCtlRegOffset = AUD_DIP_ELD_CTL_TRANSD_REG;
        infoFrameReg    = AUD_TCD_INFOFR_REG;
        break;
    default:
        break;
    }

    HRESULT hr = mGfxMMIO->MMIORead(dipCtlRegOffset, (ULONG *)&stAudDIPELDCtrl.ulValue);
    EXIT_ON_ERROR(hr);

    if (3 != stAudDIPELDCtrl.ulDipTransmissionFreq)
    {
        ERROR_LOG("%s Incorrect AIF Tx Freq: %d, pin: %d, DE: %d", VERIFICATION_FAILURE, stAudDIPELDCtrl.ulDipTransmissionFreq, mPinNodeInUse, mDEInUse);
        // TODO: Remove the comment once the OS fix is received from MSFT. HSD: 16015684285
        // return ERROR_INVALID_STATE;
    }

    if (!(stAudDIPELDCtrl.ulDipTypeEnableStatus & 0x1))
    {
        ERROR_LOG("%s DIP disabled, pin: %d, DE: %d", VERIFICATION_FAILURE, mPinNodeInUse, mDEInUse);
        return ERROR_INVALID_STATE;
    }

    stAudDIPELDCtrl.ulDipRamAcessAddress = 0; // Reset DIP read address.
    stAudDIPELDCtrl.ulDipBufferIndex     = 0; // Read Audio DIP
    hr                                   = mGfxMMIO->MMIOWrite(dipCtlRegOffset, stAudDIPELDCtrl.ulValue);
    EXIT_ON_ERROR(hr);

    // Data to write is minimal of ELD size and max possible HW ELD buffer size
    ulOffset = 0;

    while (ulOffset < ceil(AIF_PACKET_SIZE / sizeof(DWORD)))
    {
        hr = mGfxMMIO->MMIORead(infoFrameReg, &infoFrame[ulOffset]);
        EXIT_ON_ERROR(hr);

        ulOffset++;
    }

    CreateAudioInfoFrame();

    pInfoFrameRead = (PBYTE)infoFrame;

    if (mPortType == mEld.ucConnectionType)
    {
        if (0 != memcmp(mAifPacket, pInfoFrameRead, mInfoFrameSize))
        {
            ERROR_LOG("%s Incorrect InfoFrame, pin: %d, DE: %d", VERIFICATION_FAILURE, mPinNodeInUse, mDEInUse);
            return ERROR_INVALID_STATE;
        }
    }

Exit:

    if (S_OK != hr)
    {
        ERROR_LOG("%s ELD read from trancoder register failed", ERROR_MESSAGE);
    }

    return hr;
}

HRESULT DACVerifier::VerifyOverAndUnderRunHDMI()
{
    BOOL                 bOverRun       = FALSE;
    BOOL                 bUnderRun      = FALSE;
    AUD_HDMI_FIFO_STATUS hdmiFifoStatus = { 0 };

    HRESULT hr = mGfxMMIO->MMIORead(AUD_HDMI_FIFO_STATUS_RO, (DWORD *)&hdmiFifoStatus.ulValue);
    EXIT_ON_ERROR(hr);

    switch (mConverterIndexInUse)
    {
    case 0:
        bOverRun  = hdmiFifoStatus.Conv1Overrun;
        bUnderRun = hdmiFifoStatus.Conv1Underrun;
        break;
    case 1:
        bOverRun  = hdmiFifoStatus.Conv2Overrun;
        bUnderRun = hdmiFifoStatus.Conv2Underrun;
        break;
    case 2:
        bOverRun  = hdmiFifoStatus.Conv3Overrun;
        bUnderRun = hdmiFifoStatus.Conv3Underrun;
        break;
    case 3:
        bOverRun  = hdmiFifoStatus.Conv4Overrun;
        bUnderRun = hdmiFifoStatus.Conv4Underrun;
        break;
    default:
        break;
    }

    if (bOverRun)
    {
        ERROR_LOG("%s FIFO Overrun, converter: %d", VERIFICATION_FAILURE, mConverterNodeInUse);
        return ERROR_INVALID_STATE;
    }

Exit:
    if (S_OK != hr)
    {
        ERROR_LOG("%s Could not red AUD_HDMI_FIFO_STATUS_RO register", ERROR_MESSAGE);
    }

    return hr;
}

HRESULT DACVerifier::VerifyOverAndUnderRunDP()
{
    BOOL              bOverRun     = FALSE;
    AUD_DP_DIP_STATUS dpFifoStatus = { 0 };

    HRESULT hr = mGfxMMIO->MMIORead(AUD_DP_DIP_STATUS_REG, (DWORD *)&dpFifoStatus.ulValue);
    EXIT_ON_ERROR(hr);

    // TODO: Check other bits too.
    switch (mPipeId)
    {
    case 0:
        bOverRun = dpFifoStatus.AudfaDpFifoOverrun;
        break;
    case 1:
        bOverRun = dpFifoStatus.AudfbDpFifoOverrun;
        break;
    case 2:
        bOverRun = dpFifoStatus.AudfcDpFifoOverrun;
        break;
    case 3:
        bOverRun = dpFifoStatus.AudfdDpFifoOverrun;
        break;
    default:
        break;
    }

    if (bOverRun)
    {
        ERROR_LOG("%s DP FIFO Overrun, pipe: %d", VERIFICATION_FAILURE, mPipeId);
        return ERROR_INVALID_STATE;
    }

Exit:
    if (S_OK != hr)
    {
        ERROR_LOG("%s Could not red AUD_HDMI_FIFO_STATUS_RO register", ERROR_MESSAGE);
    }

    return hr;
}

HRESULT DACVerifier::GetDmaCounters()
{
    HRESULT hr = mGfxMMIO->MMIORead(AUD_HDA_LPIB0_REG, &mDmaCounterValuesInitial[0]);
    EXIT_ON_ERROR(hr);

    hr = mGfxMMIO->MMIORead(AUD_HDA_LPIB1_REG, &mDmaCounterValuesInitial[1]);
    EXIT_ON_ERROR(hr);

    hr = mGfxMMIO->MMIORead(AUD_HDA_LPIB2_REG, &mDmaCounterValuesInitial[2]);
    EXIT_ON_ERROR(hr);

    hr = mGfxMMIO->MMIORead(AUD_HDA_LPIB3_REG, &mDmaCounterValuesInitial[3]);
    EXIT_ON_ERROR(hr);

Exit:
    if (S_OK != hr)
    {
        ERROR_LOG("%s Could not read DMA counter registers", ERROR_MESSAGE);
    }

    return hr;
}

HRESULT DACVerifier::GetSampligRateBaseMultDivFactors(DWORD &base, DWORD &mult, DWORD &div)
{
    HRESULT hr = S_OK;

    switch (mWaveFmt.Format.nSamplesPerSec)
    {
    case 32000:
        base = 0;
        mult = 2;
        div  = 3;
        break;
    case 44100:
        base = 1;
        mult = 1;
        div  = 1;
        break;
    case 48000:
        base = 0;
        mult = 1;
        div  = 1;
        break;
    case 88200:
        base = 1;
        mult = 2;
        div  = 1;
        break;
    case 96000:
        base = 0;
        mult = 2;
        div  = 1;
        break;
    case 176400:
        base = 1;
        mult = 4;
        div  = 1;
        break;
    case 192000:
        base = 0;
        mult = 4;
        div  = 1;
        break;
    default:
        hr = ERROR_INVALID_DATA;
    }

    if (S_OK != hr)
    {
        ERROR_LOG("%s Unsupporetd sampling rate: %d", ERROR_MESSAGE, mWaveFmt.Format.nSamplesPerSec);
    }

    mult -= 1; // Multiplier and divisior values in register is (actual -1)
    div -= 1;

    return hr;
}

void DACVerifier::GetStreamProperties()
{
    mStreamType = CONVERTER_STREAM_TYPE_PCM;

    if (IsEqualGUID(mWaveFmt.SubFormat, KSDATAFORMAT_SUBTYPE_PCM))
    {
        mStreamType  = CONVERTER_STREAM_TYPE_PCM;
        mChannelMask = mWaveFmt.dwChannelMask;
    }
    else if (IsEqualGUID(mWaveFmt.SubFormat, KSDATAFORMAT_SUBTYPE_IEC61937_DOLBY_DIGITAL) || IsEqualGUID(mWaveFmt.SubFormat, KSDATAFORMAT_SUBTYPE_IEC61937_DTS) ||
             IsEqualGUID(mWaveFmt.SubFormat, KSDATAFORMAT_SUBTYPE_IEC61937_WMA_PRO) || IsEqualGUID(mWaveFmt.SubFormat, KSDATAFORMAT_SUBTYPE_IEC61937_DOLBY_DIGITAL_PLUS))
    {
        mStreamType  = CONVERTER_STREAM_TYPE_NONPCM;
        mChannelMask = mWaveFmt.dwChannelMask;
    }
    else if (IsEqualGUID(mWaveFmt.SubFormat, KSDATAFORMAT_SUBTYPE_IEC61937_DTS_HD))
    {
        switch (mWaveFmt.Format.nChannels)
        {
        case 8:
            mStreamType  = CONVERTER_STREAM_TYPE_NONPCM_HBR;
            mChannelMask = KSAUDIO_SPEAKER_HBR;
            break;

        case 2:
            mStreamType  = CONVERTER_STREAM_TYPE_NONPCM;
            mChannelMask = mWaveFmt.dwChannelMask;
            break;

        default:
            break;
        }
    }
    else if ((IsEqualGUID(mWaveFmt.SubFormat, KSDATAFORMAT_SUBTYPE_IEC61937_DOLBY_MLP)) || (IsEqualGUID(mWaveFmt.SubFormat, KSDATAFORMAT_SUBTYPE_IEC61937_DOLBY_MAT20)) ||
             (IsEqualGUID(mWaveFmt.SubFormat, KSDATAFORMAT_SUBTYPE_IEC61937_DOLBY_MAT21)))
    {
        mStreamType  = CONVERTER_STREAM_TYPE_NONPCM_HBR;
        mChannelMask = KSAUDIO_SPEAKER_HBR;
    }
}

void DACVerifier::CreateAudioInfoFrame()
{
    DWORD             headerSize = 0;
    AifPacketDataType aifData    = { 0 };

    memset(mAifPacket, 0, sizeof(mAifPacket));

    if (PORT_TYPE_HDMI == mPortType)
    {
        AifPacketHdmiHeaderType HdmiHeader; /**< HDMI header template. */
        headerSize = sizeof(HdmiHeader);

        HdmiHeader.s.InfoFrameType    = AIF_INFOFRAME_TYPE;
        HdmiHeader.s.InfoFrameVersion = 1;
        HdmiHeader.s.Reserved1        = 0;
        HdmiHeader.s.InfoFrameLength  = 0xa;
        HdmiHeader.s.Checksum         = 0;

        memcpy(mAifPacket, &HdmiHeader, sizeof(HdmiHeader));
        mInfoFrameSize = sizeof(HdmiHeader) + AIF_DATA_SIZE;
    }
    else if (PORT_TYPE_DP == mPortType)
    {
        AifPacketDpHeaderType DpHeader; /**< DP header template. */
        headerSize = sizeof(DpHeader);

        DpHeader.s.PacketType       = AIF_INFOFRAME_TYPE;
        DpHeader.s.DataByteCountLSB = 0x1b;
        DpHeader.s.DataByteCountMSB = 0;
        DpHeader.s.DpVersion        = 0x11;

        memcpy(mAifPacket, &DpHeader, sizeof(DpHeader));
        mInfoFrameSize = sizeof(DpHeader) + AIF_DATA_SIZE;
    }

    BuildAudioInfoFrame(aifData);

    memcpy(&mAifPacket[headerSize], &aifData, sizeof(aifData));
}

void DACVerifier::BuildAudioInfoFrame(AifPacketDataType &aifData)
{
    UCHAR channelAlloc = 0;

    aifData.s.CodingType         = 0x0; // HDMI 1.3 says this should be 0
    aifData.s.SamplingFrequency  = 0x0; // HDMI 1.3 says this should be 0
    aifData.s.SampleSize         = 0x0; // HDMI 1.3 says this should be 0
    aifData.s.LevelShiftInfo     = 0x0; // HDMI 1.3 says this should be 0
    aifData.s.DownMixInhibitFlag = 0x0; // No downmix as per HDMI 1.3

    aifData.s.ChannelCount      = (UCHAR)(mWaveFmt.Format.nChannels - 1); // ChannelCount is 0 based
    aifData.s.ChannelAllocation = 0x0;                                    // HDMI 1.3 says this is not valid for compresses nonPcm streams

    switch (mStreamType)
    {
    case CONVERTER_STREAM_TYPE_NONPCM_HBR:
        aifData.s.ChannelCount = 0; // For HBR we do not know exact number of channels so we set refer to Stream Header
        break;

    case CONVERTER_STREAM_TYPE_NONPCM:
        aifData.s.ChannelCount = 0; // For NonPcm we do not know exact number of channels so we set refer to Stream Header
        break;

    case CONVERTER_STREAM_TYPE_PCM:
        MapChannelMaskToChannelAllocation(mChannelMask, channelAlloc);
        aifData.s.ChannelAllocation = channelAlloc;
        break;

    default:
        break;
    }

    if (PORT_TYPE_HDMI == mPortType) // HDMI Interface, checksum is required in the header
    {
        AifPacketHdmiHeaderType *pHeader = (AifPacketHdmiHeaderType *)mAifPacket;
        pHeader->s.Checksum              = CalculateAifChecksum(&aifData);
    }
}

UCHAR DACVerifier::CalculateAifChecksum(const AifPacketDataType *_pAifData)
{
    // Header part
    UCHAR byte_sum = 0;
    for (UCHAR i = 0; i < (AIF_HDMI_HEADER_SIZE - 1); ++i) // skip checksum field
    {
        byte_sum += mAifPacket[i];
    }

    // Data part
    for (UCHAR i = 0; i < AIF_DATA_SIZE; ++i)
    {
        byte_sum += _pAifData->Raw[i];
    }

    return (UCHAR)(0 - byte_sum);
}

void DACVerifier::MapChannelMaskToChannelAllocation(ULONG channelMask, UCHAR &channelAllocation)
{
    // Calculating
    switch (channelMask)
    {
    case KSAUDIO_SPEAKER_STEREO:
        channelAllocation = 0x00;
        break;

        // Chrontel: For any 4 channel configuration set _ChannelAllocation to 0x03
    case KSAUDIO_SPEAKER_QUAD:
        channelAllocation = 0x08;
        break;

    case KSAUDIO_SPEAKER_SURROUND:
        channelAllocation = 0x06;
        break;

    case KSAUDIO_SPEAKER_3POINT1:
        channelAllocation = 0x03;
        break;

    case KSAUDIO_SPEAKER_5POINT1:
    case KSAUDIO_SPEAKER_5POINT1_SURROUND:
        channelAllocation = 0x0B;
        break;

    case KSAUDIO_SPEAKER_7POINT1:
        channelAllocation = 0x1F;
        break;

        // Chrontel: For 7.1 surround channels 5,6 are swapped with 7,8. Set allocation to 0x1F
    case KSAUDIO_SPEAKER_7POINT1_SURROUND:
        channelAllocation = 0x13;
        break;

    default:
        channelAllocation = 0x00;
    }
}
