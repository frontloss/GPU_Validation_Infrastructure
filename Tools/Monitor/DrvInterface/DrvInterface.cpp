// DrvInterface.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"
#include <cstdlib>
#include "EscapeHandler.h"
#include "..\Code\inc\shared\DisplayArgs.h"
#include "DrvInterface.h" 



EscapeHandler *hEscape = NULL;
ULONG DeviceId[2] = { 0,0 };
extern "C" {
    //TRADITIONALDLL_API double GetDistance(Location, Location);
    //TRADITIONALDLL_API void InitLocation(Location*);

    DllExport HRESULT NTAPI QueryWbStatus(WB_CAPS *pWbCaps)
    {
        // return S_OK;
        //__debugbreak();
        DD_WRITEBACK_QUERY_ARGS WbQuery = { 0 };
        if ((NULL == pWbCaps))
        {
            return E_INVALIDARG;
        }
        if (SUCCEEDED(hEscape->PerformEscape(105, &WbQuery, sizeof(WbQuery), FALSE, FALSE)))
        {

            pWbCaps->IsSupported = WbQuery.IsWbFeatureEnabled;
            pWbCaps->IsEnabled = WbQuery.WbPluggedIn[0];
            pWbCaps->HResolution = WbQuery.CurrentResolution[0].Cx;
            pWbCaps->VResolution = WbQuery.CurrentResolution[0].Cy;
            pWbCaps->PixelFormat = 1;

            //for (int devicenum = 0; devicenum < 2; devicenum++)
            {
                if (TRUE == WbQuery.WbPluggedIn[0])
                {
                    DeviceId[0] = WbQuery.DeviceId[0];
                }
                else
                {
                    DD_WRITEBACK_HPD WdHpd = { 0 };
                    WdHpd.HotPlug = true;
                    hEscape->PerformEscape(106, &WdHpd, sizeof(WdHpd), FALSE, FALSE);
                    DeviceId[0] = WdHpd.DeviceId;
                    pWbCaps->HResolution = WdHpd.Resolution.Cx;
                    pWbCaps->VResolution = WdHpd.Resolution.Cy;
                }
            }
        }
        else
        {
            pWbCaps->IsSupported = true;
            pWbCaps->IsEnabled = true;
            pWbCaps->HResolution = 1920;
            pWbCaps->VResolution = 1080;
            pWbCaps->PixelFormat = 1;
        }
        return S_OK;
    }

    DllExport HRESULT NTAPI CaptureFrame(WB_CAPTURE *pWbCapture, int *pBuffer)
    {
        HRESULT hr;
        DD_WRITEBACK_CAPTURE_BUFFER_ARGS WdCapture = { 0 };
        void *p = NULL;
        int index = 0;
        int *pPixelData;
        
        if ((NULL == pWbCapture))// ||(NULL == pBuffer))
        {
            return E_INVALIDARG;
        }

        //__debugbreak();
        WdCapture.DeviceId = DeviceId[0];
        if (0 == pWbCapture->BufferSize)
        {
            hr = hEscape->PerformEscape(107, &WdCapture, sizeof(WdCapture), FALSE, FALSE);
            
            pWbCapture->BufferSize = WdCapture.BufferSize;
            return hr;
        }
        WdCapture.BufferSize = pWbCapture->BufferSize;

        
        p = malloc(sizeof(DD_WRITEBACK_CAPTURE_BUFFER_ARGS) + pWbCapture->BufferSize);
        DD_WRITEBACK_CAPTURE_BUFFER_ARGS *pEscArg = (DD_WRITEBACK_CAPTURE_BUFFER_ARGS*)p;
        pEscArg->BufferSize = WdCapture.BufferSize;
        pEscArg->DeviceId = DeviceId[0];

        
        hr = hEscape->PerformEscape(107, pEscArg, (sizeof(DD_WRITEBACK_CAPTURE_BUFFER_ARGS) + pWbCapture->BufferSize), FALSE, FALSE);
        if (SUCCEEDED(hr))
        {


           // int Data = rand();
           /* for (index = 0; index < pWbCapture->BufferSize; index++)
            {
                pPixelData = (int *)(pBuffer + index);
                //*pPixelData = Data;
                //*pPixelData = 12;
            }*/
            pWbCapture->HResolution = pEscArg->Resolution.Cx;
            pWbCapture->VResolution = pEscArg->Resolution.Cy;
            pWbCapture->PixelFormat = pEscArg->PixelFormat;
            memcpy_s(pBuffer, pWbCapture->BufferSize, pEscArg->WdBuffer, pEscArg->BufferSize);
        }
        return hr;
    }
}