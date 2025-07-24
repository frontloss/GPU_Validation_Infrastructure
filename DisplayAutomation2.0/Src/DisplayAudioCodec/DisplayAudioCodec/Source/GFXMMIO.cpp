#include "..\Header\DisplayAudioCodec.h"
#include "..\Header\GFXMMIO.h"
#include <iostream>
#pragma warning(disable : 4996)
#pragma comment(lib, "windowscodecs.lib")
#pragma comment(lib, "dxgi.lib")
#pragma comment(lib, "Setupapi.lib")

#ifdef DEFINE_DEVPROPKEY
#undef DEFINE_DEVPROPKEY
#endif
#ifdef INITGUID
#define DEFINE_DEVPROPKEY(name, l, w1, w2, b1, b2, b3, b4, b5, b6, b7, b8, pid) \
    EXTERN_C const DEVPROPKEY DECLSPEC_SELECTANY name = { { l, w1, w2, { b1, b2, b3, b4, b5, b6, b7, b8 } }, pid }
#else
#define DEFINE_DEVPROPKEY(name, l, w1, w2, b1, b2, b3, b4, b5, b6, b7, b8, pid) EXTERN_C const DEVPROPKEY name
#endif // INITGUID

DEFINE_GUID(GUID_DEVCLASS_DISPLAY, 0x4d36e968L, 0xe325, 0x11ce, 0xbf, 0xc1, 0x08, 0x00, 0x2b, 0xe1, 0x03, 0x18);

DEFINE_DEVPROPKEY(DEVPKEY_Device_LocationInfo, 0xa45c254e, 0xdf1c, 0x4efd, 0x80, 0x20, 0x67, 0xd1, 0x46, 0xa8, 0x50, 0xe0, 15);

GFXMMIO::GFXMMIO(PGFX_ADAPTER_INFO pAdapterInfoObj)
{
    pAdapterInfo = pAdapterInfoObj;
}

GFXMMIO::~GFXMMIO()
{
}

HRESULT GFXMMIO::GetSetAudioVerb(ULONG ulWidgetId, ULONG ulVerbId, ULONG ulPayload, ULONG *pReadVal)
{
    HRESULT          hr                = S_OK;
    DAC_VERB         dacVerb           = { 0 };
    GEN9_ICS_MAILBOX ICSMailboxValue   = { 0 };
    ULONG            ulIRRMailboxValue = 0;

    if (ulVerbId <= 0xF)
    {
        dacVerb.verbShort.WidgetId    = ulWidgetId;
        dacVerb.verbShort.VerbId      = ulVerbId;
        dacVerb.verbShort.PayloadData = ulPayload;
        dacVerb.verbShort.CADValue    = 0x2;
    }
    else
    {
        dacVerb.verbLong.WidgetId    = ulWidgetId;
        dacVerb.verbLong.VerbId      = ulVerbId;
        dacVerb.verbLong.PayloadData = ulPayload;
        dacVerb.verbLong.CADValue    = 0x2;
    }

    return GetSetAudioVerbRaw(dacVerb.raw, pReadVal);
}

HRESULT GFXMMIO::GetSetAudioVerbRaw(ULONG verb, ULONG *pReadVal)
{
    HRESULT                hr                 = S_OK;
    DAC_VERB               dacVerb            = { 0 };
    GEN9_ICS_MAILBOX       ICSMailboxValue    = { 0 };
    AUD_CHICKENBIT_REG_SKL chknReg            = { 0 };
    ULONG                  ulIRRMailboxValue  = 0;
    ULONG                  LinkWakeRetryCount = 0;

    dacVerb.raw = verb;

    if (S_OK != MMIORead(AUD_CHICKEN_BIT_REG, (DWORD *)&chknReg.ulValue))
    {
        hr = E_FAIL;
        ERROR_LOG("Could not read from AUD_CHICKEN_BIT_REG");
        goto exit;
    }

    // Force link wake
    while (chknReg.iDispLinkSleepState && LinkWakeRetryCount < 3)
    {
        chknReg.CodecWakeOverwriteToDacfeunit = 1;
        MMIOWrite(AUD_CHICKEN_BIT_REG, chknReg.ulValue);
        Sleep(1);
        chknReg.CodecWakeOverwriteToDacfeunit = 0;
        MMIOWrite(AUD_CHICKEN_BIT_REG, chknReg.ulValue);
        Sleep(10);
        MMIORead(AUD_CHICKEN_BIT_REG, (DWORD *)&chknReg.ulValue);
        LinkWakeRetryCount++;
    }

    if ((LinkWakeRetryCount >= 3) && chknReg.iDispLinkSleepState)
    {
        ERROR_LOG("Could not wake the link");
        hr = ERROR_DEVICE_NOT_AVAILABLE;
        goto exit;
    }

    if (S_OK != MMIORead(AUD_ICS_REG, &ICSMailboxValue.ulValue))
    {
        hr = E_FAIL;
        ERROR_LOG("Could not read from AUD_ICS_REG");
        goto exit;
    }

    // Step1: Clearing IRV
    ICSMailboxValue.bImmediateResultValid = 1;

    if (S_OK != MMIOWrite(AUD_ICS_REG, ICSMailboxValue.ulValue))
    {
        hr = E_FAIL;
        ERROR_LOG("Could not write to AUD_ICS_REG");
        goto exit;
    }

    // 2.Now write the value to ICW once ICB = 0
    Sleep(1);

    hr = MMIORead(AUD_ICS_REG, &ICSMailboxValue.ulValue);

    if (S_OK != hr || ICSMailboxValue.bImmediateCommandBusy != 0)
    {
        ERROR_LOG("bImmediateCommandBusy is not Zero");
        goto exit;
    }

    // Write ICW
    if (S_OK != MMIOWrite(AUD_ICW_REG, dacVerb.ulValue))
    {
        hr = E_FAIL;
        ERROR_LOG("Could not write to AUD_ICW_REG");
        goto exit;
    }

    // Set ICB = 1 to start the transaction.
    if (S_OK != MMIORead(AUD_ICS_REG, &ICSMailboxValue.ulValue))
    {
        hr = E_FAIL;
        ERROR_LOG("Could not read from AUD_ICS_REG");
        goto exit;
    }

    ICSMailboxValue.bImmediateCommandBusy = 0x01;

    if (S_OK != MMIOWrite(AUD_ICS_REG, ICSMailboxValue.ulValue))
    {
        hr = E_FAIL;
        ERROR_LOG("Could not write to AUD_ICS_REG");
        goto exit;
    }

    Sleep(1);

    hr = MMIORead(AUD_ICS_REG, &ICSMailboxValue.ulValue);

    if ((S_OK != hr) || (0 != ICSMailboxValue.bImmediateCommandBusy) || (NULL == ICSMailboxValue.bImmediateResultValid))
    {
        ERROR_LOG("bImmediateCommandBusy is not Zero");
        goto exit;
    }

    if (pReadVal)
    {
        if (S_OK != MMIORead(AUD_IRR_REG, &ulIRRMailboxValue))
        {
            hr = E_FAIL;
            ERROR_LOG("Could not write to AUD_IRR_REG");
            goto exit;
        }

        *pReadVal = ulIRRMailboxValue;
    }

    if (S_OK != MMIORead(AUD_ICS_REG, &ICSMailboxValue.ulValue))
    {
        hr = E_FAIL;
        ERROR_LOG("Could not read from AUD_ICS_REG");
        goto exit;
    }

    // Clearing IRV
    ICSMailboxValue.bImmediateResultValid = 0x01;

    if (S_OK != MMIOWrite(AUD_ICS_REG, ICSMailboxValue.ulValue))
    {
        hr = E_FAIL;
        ERROR_LOG("Could not write to AUD_ICS_REG");
        goto exit;
    }

exit:

    return hr;
}

HRESULT GFXMMIO::SetMMIOPIOMode(BOOLEAN bSet)
{
    HRESULT                hr                        = S_OK;
    AUD_CHICKENBIT_REG_SKL stAudioChickenBitRegister = { 0 };
    ULONG                  val;
    hr                                              = MMIORead(AUD_CHICKEN_BIT_REG, &val);
    stAudioChickenBitRegister.ulValue               = static_cast<UINT32>(val);
    stAudioChickenBitRegister.EnableMmioProgramming = bSet;
    hr                                              = MMIOWrite(AUD_CHICKEN_BIT_REG, stAudioChickenBitRegister.ulValue);

    return hr;
}

HRESULT GFXMMIO::MMIOWrite(ULONG offset, ULONG regValue)
{
    BOOL bStatus = FALSE;

    bStatus = ValSimWriteMMIO(pAdapterInfo, sizeof(GFX_ADAPTER_INFO), offset, regValue);

    if (bStatus == TRUE)
    {
        return S_OK;
    }
    else
    {
        return E_FAIL;
    }
}

HRESULT GFXMMIO::MMIORead(ULONG offset, ULONG *pRegValue)
{
    BOOL bStatus = FALSE;

    bStatus = ValSimReadMMIO(pAdapterInfo, sizeof(GFX_ADAPTER_INFO), offset, pRegValue);

    if (bStatus == TRUE)
    {
        return S_OK;
    }
    else
    {
        return E_FAIL;
    }
}
