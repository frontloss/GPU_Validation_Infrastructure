#include "stdafx.h"
#include "EscapeHandler.h"
#include "SetupAPI.h"
#include <wchar.h>
#include "string.h"
#include "gfxEscape.h"
#include "d3dkmthk.h"
#include <stdlib.h>

#define MAX_ESCAPE_REFERENCE 30 //Allow Max 10 References
#define STATUS_UNSUCCESSFUL              ((NTSTATUS)0xC0000001L)
#define VENDOR_INTEL            L"VEN_8086"
#define VENDOR_INTEL_LOWERCASE  L"ven_8086"

const GUID GUID_DISPLAY_DEVICE_ARRIVAL = { 0x1CA05180, 0xA699, 0x450A, { 0x9A, 0x0C, 0xDE, 0x4F, 0xBE, 0x3D, 0xDD, 0x89 } };
//class EscapeHandler;

static ULONG m_ulReferenceCount;
static EscapeHandler* m_EscapeReference;



EscapeHandler::EscapeHandler()
{
    m_AdapterHandle = NULL;
    Initialize();
}


EscapeHandler::~EscapeHandler()
{
    NTSTATUS Status = STATUS_UNSUCCESSFUL;
    if (NULL != m_DeviceHandle)
    {
        //Destroy the device first
        D3DKMT_DESTROYDEVICE stDestroyDevice = { 0 };

        stDestroyDevice.hDevice = m_DeviceHandle;

        //Call the D3DKMT interface to destroy the device
        Status = m_D3dKmtInterfaces.pfnDestroyDevice(&stDestroyDevice);

        if (0 != Status)
        {
            //Something is messed up:(
        }

        m_DeviceHandle = NULL;
    }

    if (NULL != m_AdapterHandle)
    {
        D3DKMT_CLOSEADAPTER stCloseAdapter = { 0 };

        stCloseAdapter.hAdapter = m_AdapterHandle;

        Status = m_D3dKmtInterfaces.pfnCloseAdapter(&stCloseAdapter);

        if (0 != Status)
        {
            //Something is messed up:(
        }

        m_AdapterHandle = NULL;
    }

    if (NULL != m_Gdi32Handle)
    {
        //Free the loaded GDI32 library
        FreeLibrary(m_Gdi32Handle);

        m_Gdi32Handle = NULL;
    }
}

EscapeHandler* EscapeHandler:: AcquireEscapeHandler()
{
    if (NULL == m_EscapeReference)
    {
        m_EscapeReference = new EscapeHandler();
    }
    if (NULL != m_EscapeReference && m_ulReferenceCount < MAX_ESCAPE_REFERENCE)
    {
        m_ulReferenceCount++;
    }
    return m_EscapeReference;
}

HRESULT EscapeHandler::ReleaseEscapeHandler(EscapeHandler** pEscHandler)
{
    HRESULT hr = E_FAIL;
    if (NULL != m_EscapeReference && NULL != pEscHandler && *pEscHandler == m_EscapeReference)
    {
        m_ulReferenceCount--;
        if (0 == m_ulReferenceCount)
        {
            delete (m_EscapeReference);
            m_EscapeReference = NULL;
        }
        *pEscHandler = NULL;
        hr = S_OK;
    }
    
    return hr;
}
//=============================================================================
// 
// Function: Checksum
// 
// Desc: 
//      Calculates the Check Sum for the data
//                               
// Parameters:
//      uiSize ==> Size of the Data
//      pData  ==> Pointer to the Data
// Returns:
//    CheckSum value      
//-----------------------------------------------------------------------------
UINT EscapeHandler::Checksum(UINT uiSize, PVOID pData)
{
    UINT uiSum = 0, uiCounter = 0;
    UINT *uiElement = (UINT *)pData;

    UINT BMUL = uiSize & ((UINT)(-1) - (sizeof(UINT)-1));

    UINT NUM = BMUL / sizeof(UINT);

    for (uiCounter = 0; uiCounter < NUM; uiCounter++)
    {
        uiSum += *(uiElement++);
    }

    return uiSum;
}

HRESULT EscapeHandler::PerformEscape(int EscapeCode, void *pInputData, UINT  uiInputSize, BOOL  bNeedHWAccess, BOOL bIsInit)
{
    HRESULT             hr = E_FAIL;
    D3DKMT_ESCAPE       stD3DKMTEscape = { 0 };
    UINT                uiEscapePvtDataSize = 0;
    void                *pEscapePvtData = NULL;
    GFX_ESCAPE_HEADER_T *pGfxEscapeHeader = NULL;
    int retval = 0;
    //BOOL bIsInit = TRUE;

    do
    {
        if (NULL == pInputData)
        {
            //Corrupt input buffer
            break;
        }
        //Either we need the adapter and device handles or the IOCTL function pointer
        if (NULL == m_AdapterHandle)
        {
            //Escape context is not setup properly
            break;
        }

        //Calculate the total Escape size --> Header + InputData
        uiEscapePvtDataSize = uiInputSize + sizeof(GFX_ESCAPE_HEADER_T);

        pEscapePvtData = (void*)malloc(uiEscapePvtDataSize);

        if (NULL == pEscapePvtData)
        {
            //Allocation for EscapePrivateData failed
            break;
        }

        //Zero-out the memory
        ZeroMemory(pEscapePvtData, uiEscapePvtDataSize);

        //Populate the input params for Esacpe call
        stD3DKMTEscape.hAdapter = m_AdapterHandle;
        //Check if it's the init call
        if (bIsInit)
        {
            //Need the Device handle during the initialization.
            //A TDR will make this handle invalid and the escapes will start failing. 
            //So skip populating hDevicefor the other escapes where its not mandatory.
            stD3DKMTEscape.hDevice = m_DeviceHandle;
        }
        stD3DKMTEscape.Type = D3DKMT_ESCAPE_DRIVERPRIVATE;
        stD3DKMTEscape.Flags.HardwareAccess = bNeedHWAccess;
        stD3DKMTEscape.pPrivateDriverData = pEscapePvtData;
        stD3DKMTEscape.PrivateDriverDataSize = uiEscapePvtDataSize;

        //Update the PrivateDriverData

        //Update the Header first
        pGfxEscapeHeader = (GFX_ESCAPE_HEADER_T *)pEscapePvtData;
        pGfxEscapeHeader->ulMajorEscapeCode = GFX_ESCAPE_CUICOM_CONTROL;
        pGfxEscapeHeader->uiMinorEscapeCode = EscapeCode;
        pGfxEscapeHeader->usEscapeVersion = 1;

        //Calculate the checksum value for input data
        //pGfxEscapeHeader->CheckSum = Checksum(uiInputSize, pInputData);

        //Increment the pEscapePvtData pointer and copy the client
        //input data
        pEscapePvtData = (void *)((char *)pEscapePvtData + sizeof(GFX_ESCAPE_HEADER_T));

        //Copy the client input data
        memcpy_s(pEscapePvtData, uiInputSize, pInputData, uiInputSize);

        
        //Call the D3DKMT interface for making Escape Call into the driver
        hr = m_D3dKmtInterfaces.pfnEscape(&stD3DKMTEscape);

        if (S_OK != hr)
        {
            //Escape call failed
            break;
        }

        //Reached here means, Escape call is executed successfully.
        //Copy back the Private data back to Client Input buffer
        //Note: At this point, pEscapePvtData variable is pointing to the client
        //input data, not the header.
        memcpy_s(pInputData, uiInputSize, pEscapePvtData, uiInputSize);

        hr = S_OK;

    } while (FALSE);

    if (NULL != pGfxEscapeHeader)
    {
        //Free up the allocated memory
        free(pGfxEscapeHeader);
        pGfxEscapeHeader = NULL;
    }

    return hr;
}

HRESULT EscapeHandler::PerformEscape(GFX_ESCAPE_HEADER_T *pInputDataHeader, UINT  uiInputSize, BOOL  bNeedHWAccess,BOOL bIsInit)
{
    HRESULT             hr = E_FAIL;
    D3DKMT_ESCAPE       stD3DKMTEscape = { 0 };
    UINT                uiEscapePvtDataSize = uiInputSize;
    void                *pEscapePvtData = NULL;
    GFX_ESCAPE_HEADER_T *pGfxEscapeHeader = NULL;
    int retval = 0;
    //BOOL bIsInit = TRUE;
    PBYTE pInputData = (PBYTE)pInputDataHeader;
    UINT  uiInputDataSize = 0;
    do
    {
        //Make sure we have valid input data and we have data beyond the Header
        if (NULL == pInputDataHeader || uiInputSize <= sizeof(GFX_ESCAPE_HEADER_T))
        {
            //Corrupt input buffer
            break;
        }
        //Either we need the adapter and device handles or the IOCTL function pointer
        if (NULL == m_AdapterHandle)
        {
            //Escape context is not setup properly
            break;
        }
        pInputData += sizeof(GFX_ESCAPE_HEADER_T);
        uiInputDataSize = uiInputSize - sizeof(GFX_ESCAPE_HEADER_T);
        pEscapePvtData = pInputDataHeader;

        //Populate the input params for Esacpe call
        stD3DKMTEscape.hAdapter = m_AdapterHandle;
        //Check if it's the init call
        if (bIsInit)
        {
            //Need the Device handle during the initialization.
            //A TDR will make this handle invalid and the escapes will start failing. 
            //So skip populating hDevicefor the other escapes where its not mandatory.
            stD3DKMTEscape.hDevice = m_DeviceHandle;
        }
        stD3DKMTEscape.Type = D3DKMT_ESCAPE_DRIVERPRIVATE;
        stD3DKMTEscape.Flags.HardwareAccess = bNeedHWAccess;
        stD3DKMTEscape.pPrivateDriverData = pEscapePvtData;
        stD3DKMTEscape.PrivateDriverDataSize = uiEscapePvtDataSize;

        //Update the PrivateDriverData

        //Update the Header first
        pGfxEscapeHeader = (GFX_ESCAPE_HEADER_T *)pEscapePvtData;
        pGfxEscapeHeader->EscapeCode = GFX_ESCAPE_HDCP_SRVC;
        pGfxEscapeHeader->Size = uiInputDataSize;

        //Calculate the checksum value for input data
        pGfxEscapeHeader->CheckSum = Checksum(uiInputDataSize, pInputData);

        //Call the D3DKMT interface for making Escape Call into the driver
        hr = m_D3dKmtInterfaces.pfnEscape(&stD3DKMTEscape);

        if (S_OK != hr)
        {
            //Escape call failed
            break;
        }

        hr = S_OK;

    } while (FALSE);

    return hr;
}
#if 0
HRESULT EscapeHandler::Initialize()
{
    HRESULT hr = E_FAIL;
    NTSTATUS                Status = -1;  //Actual NTSTATUS def is not available. 
    HDEVINFO                            deviceInfo;

    
    do
    {
        SP_DEVICE_INTERFACE_DATA            deviceInfoData;
        SP_DEVINFO_DATA                     devInfoData;
        PSP_DEVICE_INTERFACE_DETAIL_DATA    deviceDetailData = NULL;
        CONST GUID*                         Interface = &GUID_DISPLAY_DEVICE_ARRIVAL;
        D3DKMT_CREATEDEVICE     stCreateDeviceData = { 0 };

        m_Gdi32Handle = LoadLibraryEx(L"gdi32.dll", NULL, 0);

        if (NULL == m_Gdi32Handle)
        {
            //Not able to load gdi32 dll itself... bail out
            break;
        }

        //Get the different D3DKMT interfaces that are required
        m_D3dKmtInterfaces.pfnOpenAdapterFromGDIDisplayName = (PFND3DKMT_OPENADAPTERFROMGDIDISPLAYNAME)GetProcAddress(m_Gdi32Handle, "D3DKMTOpenAdapterFromGdiDisplayName");
        m_D3dKmtInterfaces.pfnEscape = (PFND3DKMT_ESCAPE)GetProcAddress(m_Gdi32Handle, "D3DKMTEscape");
        m_D3dKmtInterfaces.pfnCreateDevice = (PFND3DKMT_CREATEDEVICE)GetProcAddress(m_Gdi32Handle, "D3DKMTCreateDevice");
        m_D3dKmtInterfaces.pfnDestroyDevice = (PFND3DKMT_DESTROYDEVICE)GetProcAddress(m_Gdi32Handle, "D3DKMTDestroyDevice");
        m_D3dKmtInterfaces.pfnCloseAdapter = (PFND3DKMT_CLOSEADAPTER)GetProcAddress(m_Gdi32Handle, "D3DKMTCloseAdapter");

        //Should be able to get all the interfaces. If not bail out
        if ((NULL == m_D3dKmtInterfaces.pfnOpenAdapterFromGDIDisplayName) ||
            (NULL == m_D3dKmtInterfaces.pfnEscape) ||
            (NULL == m_D3dKmtInterfaces.pfnCreateDevice) ||
            (NULL == m_D3dKmtInterfaces.pfnDestroyDevice) ||
            (NULL == m_D3dKmtInterfaces.pfnCloseAdapter))
        {
            break;
        }

        deviceInfo = SetupDiGetClassDevs((LPGUID)Interface,
            NULL,
            NULL,
            (DIGCF_PRESENT | DIGCF_DEVICEINTERFACE));

        if (deviceInfo != INVALID_HANDLE_VALUE)
        {
            deviceInfoData.cbSize = sizeof(SP_DEVICE_INTERFACE_DATA);
            devInfoData.cbSize = sizeof(devInfoData);

            for (int index = 0;
                SetupDiEnumDeviceInterfaces(deviceInfo,
                0,
                (LPGUID)Interface,
                index,
                &deviceInfoData);
            index++)
            {
                ULONG  requiredLength;

                SetupDiGetDeviceInterfaceDetail(deviceInfo,
                    &deviceInfoData,
                    NULL,
                    0,
                    &requiredLength,
                    NULL);

                if (GetLastError() != ERROR_INSUFFICIENT_BUFFER)
                {
                    continue;
                }

                deviceDetailData = (PSP_DEVICE_INTERFACE_DETAIL_DATA)new char[requiredLength];

                deviceDetailData->cbSize = sizeof(SP_DEVICE_INTERFACE_DETAIL_DATA);

                if (!SetupDiGetDeviceInterfaceDetail(deviceInfo,
                    &deviceInfoData,
                    deviceDetailData,
                    requiredLength,
                    &requiredLength,
                    &devInfoData))
                {
                    continue;
                }

                if (strstr(deviceDetailData->DevicePath,
                    "ven_8086") || strstr(deviceDetailData->DevicePath,
                    "VEN_8086"))
                {
                    HMODULE                             hGDI32 = NULL;
                    PFND3DKMT_ESCAPE                    pfnKTEscape = NULL;
                    PFND3DKMT_CLOSEADAPTER              pfnKTCloseAdapter = NULL;
                    PFND3DKMT_OPENADAPTERFROMDEVICENAME pfnKTOpenAdapterFromDeviceName = NULL;

                    hGDI32 = ::LoadLibraryEx("GDI32.dll",
                        NULL,
                        LOAD_LIBRARY_SEARCH_SYSTEM32);

                    if (NULL == hGDI32)
                    {
                        break;
                    }

                    pfnKTEscape = (PFND3DKMT_ESCAPE)GetProcAddress(
                        hGDI32,
                        "D3DKMTEscape");

                    pfnKTCloseAdapter = (PFND3DKMT_CLOSEADAPTER)GetProcAddress(
                        hGDI32,
                        "D3DKMTCloseAdapter");

                    pfnKTOpenAdapterFromDeviceName = (PFND3DKMT_OPENADAPTERFROMDEVICENAME)GetProcAddress(
                        hGDI32,
                        "D3DKMTOpenAdapterFromDeviceName");

                    if ((NULL != pfnKTEscape) &&
                        (NULL != pfnKTCloseAdapter) &&
                        (NULL != pfnKTOpenAdapterFromDeviceName))
                    {
                        WCHAR                           DeviceName[256];
                        CHAR                            *pDeviceName = deviceDetailData->DevicePath;
                        D3DKMT_OPENADAPTERFROMDEVICENAME OpenAdapter = {};
                        //Converts a character string to a wide character string
                        //(required by the D3DKMT_OPENADAPTERFROMGDIDISPLAYNAME structure)
                        //and stores the result in the DeviceName of the structure.
                        mbsrtowcs_s(NULL, DeviceName,
                            (const char**)&pDeviceName, strlen(pDeviceName), NULL);/**/
                        //OpenAdapter.pDeviceName = deviceDetailData->DevicePath;
                        OpenAdapter.pDeviceName = DeviceName;
                        if (0x80000000 & (pfnKTOpenAdapterFromDeviceName(&OpenAdapter)))
                        {
                            //Failed
                        }
                        else
                        {
                            m_AdapterHandle = OpenAdapter.hAdapter;
                            break;
                        }
                    }
                }
            }
        }
        if (NULL != deviceDetailData)
        {
            delete deviceDetailData;
            deviceDetailData = NULL;
        }
        stCreateDeviceData.hAdapter = m_AdapterHandle;
        stCreateDeviceData.Flags.LegacyMode = TRUE;

        //Create the device
        Status = m_D3dKmtInterfaces.pfnCreateDevice(&stCreateDeviceData);

        if (0 != Status)
        {
            //DDELogEvent("DDE Escape ERROR: Failed to Create Device \n");
            break;
        }

        //Save the Device handle
        m_DeviceHandle = stCreateDeviceData.hDevice;

        //Reached here means, setup is succesful
        hr = S_OK;
    }while (FALSE);

    //Not checking for hr status as the calling routine will do the 
    //appropriate clean up if this fails

    return hr;
}
#else
HRESULT EscapeHandler::Initialize()
{
    HRESULT                               hr = S_OK;
    NTSTATUS                              ntStatus = NO_ERROR;
    WCHAR                                 DeviceName[32] = { 0 };
    D3DKMT_CREATEDEVICE                   stCreateDeviceData = { 0 };
    D3DKMT_OPENADAPTERFROMGDIDISPLAYNAME  stOpenAdapterFromGDIDisplayName = { 0 };

    do
    {
        //Load the gdi32 dll and get the handle
        m_Gdi32Handle = LoadLibraryEx(L"gdi32.dll", NULL, 0);
        if (NULL == m_Gdi32Handle)
        {
            hr = E_FAIL;
            break;
        }
        //Get the different D3DKMT interfaces that are required
        m_D3dKmtInterfaces.pfnOpenAdapterFromGDIDisplayName = (PFND3DKMT_OPENADAPTERFROMGDIDISPLAYNAME)GetProcAddress(m_Gdi32Handle, "D3DKMTOpenAdapterFromGdiDisplayName");
        m_D3dKmtInterfaces.pfnOpenAdapterFromDeviceName = (PFND3DKMT_OPENADAPTERFROMDEVICENAME)GetProcAddress(m_Gdi32Handle, "D3DKMTOpenAdapterFromDeviceName");
        m_D3dKmtInterfaces.pfnEscape = (PFND3DKMT_ESCAPE)GetProcAddress(m_Gdi32Handle, "D3DKMTEscape");
        m_D3dKmtInterfaces.pfnCreateDevice = (PFND3DKMT_CREATEDEVICE)GetProcAddress(m_Gdi32Handle, "D3DKMTCreateDevice");
        m_D3dKmtInterfaces.pfnDestroyDevice = (PFND3DKMT_DESTROYDEVICE)GetProcAddress(m_Gdi32Handle, "D3DKMTDestroyDevice");
        m_D3dKmtInterfaces.pfnCloseAdapter = (PFND3DKMT_CLOSEADAPTER)GetProcAddress(m_Gdi32Handle, "D3DKMTCloseAdapter");

        //Should be able to get all the interfaces. If not bail out
        if ((NULL == m_D3dKmtInterfaces.pfnOpenAdapterFromGDIDisplayName) ||
            (NULL == m_D3dKmtInterfaces.pfnOpenAdapterFromDeviceName) ||
            (NULL == m_D3dKmtInterfaces.pfnEscape) ||
            (NULL == m_D3dKmtInterfaces.pfnCreateDevice) ||
            (NULL == m_D3dKmtInterfaces.pfnDestroyDevice) ||
            (NULL == m_D3dKmtInterfaces.pfnCloseAdapter))
        {
            hr = E_FAIL;
            break;
        }

        {
            //_LOG_DBG << "Starting in Session 0 " << endl;
            // Note in session 0 the service is not tied to a desktop thus EnumDisplayDevices used above will fail
            // In Windows Vista, Windows Server 2008, and later versions of Windows, the operating system isolates 
            // services in Session 0 and runs applications in other sessions, so services are protected from 
            // attacks that originate in application code.
            // https://msdn.microsoft.com/en-us/library/windows/hardware/dn653293%28v=vs.85%29.aspx
            // Need to use a lower level api (setup api) to communicate with driver
            // https://msdn.microsoft.com/en-us/library/windows/hardware/ff550855%28v=vs.85%29.aspx
            // Will link to setupapi.lib
            // Many of the API calls are demonstrated in the WDK samples
            // https://code.msdn.microsoft.com/windowshardware/Windows-8-Driver-Samples-5e1aa62e
            HDEVINFO                            deviceInfo;
            SP_DEVICE_INTERFACE_DATA            deviceInfoData;
            SP_DEVINFO_DATA                     devInfoData;
            PSP_DEVICE_INTERFACE_DETAIL_DATA    deviceDetailData = NULL;
            INT                                uiDeviceCount = -1;
            // WDDM register instances of this device interface class to notify the operating system and applications of the presence of display adapters.
            // https://msdn.microsoft.com/en-us/library/windows/hardware/ff546042%28v=vs.85%29.aspx
            const GUID DisplayDeviceArrivalInterface = { 0x1CA05180, 0xA699, 0x450A, { 0x9A, 0x0C, 0xDE, 0x4F, 0xBE, 0x3D, 0xDD, 0x89 } };

            // Get handle to device Info structure for all devices having DisplayDeviceArrival Interface  
            deviceInfo = SetupDiGetClassDevs((LPGUID)&DisplayDeviceArrivalInterface,
                NULL,
                NULL,
                (DIGCF_PRESENT | DIGCF_DEVICEINTERFACE));
            // check if null
            if (deviceInfo != INVALID_HANDLE_VALUE)
            {
                // If not NULL enumerate all devices 
                deviceInfoData.cbSize = sizeof(SP_DEVICE_INTERFACE_DATA);
                devInfoData.cbSize = sizeof(devInfoData);
                //  Determine how many devices are present.
                while (SetupDiEnumDeviceInterfaces(deviceInfo,
                    NULL,
                    (LPGUID)&DisplayDeviceArrivalInterface,
                    ++uiDeviceCount,
                    &deviceInfoData)
                    );

                //_LOG_DBG << "Enumerated Device Count:" << uiDeviceCount << endl;

                for (UINT index = 0; index < uiDeviceCount; index++)
                {
                    BOOL    bSetupEnumResult = FALSE;
                    ULONG   requiredLength = 0;
                    ULONG   allocatedLength = 0;
                    ULONG   StoredrequiredLength = 0;

                    bSetupEnumResult = SetupDiEnumDeviceInterfaces(deviceInfo,
                        NULL,
                        (LPGUID)&DisplayDeviceArrivalInterface,
                        index,
                        &deviceInfoData);
                    if (bSetupEnumResult == FALSE)
                    {
                        // in theory that should not happen since count is done prior
                        //_LOG_DBG << "SetupDiEnumDeviceInterfaces Failed" << endl;
                        hr = E_FAIL;
                        break;
                    }
                    // For each device get the interface details
                    // First call to get required length 
                    SetupDiGetDeviceInterfaceDetail(deviceInfo,
                        &deviceInfoData,
                        NULL,
                        0,
                        &requiredLength,
                        NULL);

                    if (GetLastError() != ERROR_INSUFFICIENT_BUFFER)
                    {
                        // if error different than buffer size not enough skip
                        //_LOG_DBG << "SetupDiGetDeviceInterfaceDetail Failed" << GetLastError() << endl;
                        continue;
                    }
                    // if allocation  performed in the previous iteration 
                    if (NULL != deviceDetailData)
                    {
                        if (requiredLength > allocatedLength)
                        {
                            //_LOG_DBG << "Allocation of buffer required" << endl;
                            delete[] deviceDetailData;
                            deviceDetailData = NULL;
                        }
                    }
                    if (deviceDetailData == NULL)
                    {
                        deviceDetailData = (PSP_DEVICE_INTERFACE_DETAIL_DATA) malloc (requiredLength);

                        if (deviceDetailData == NULL)
                        {
                            //_LOG_DBG << "Cannot Allocate Memory" << endl;
                            hr = E_OUTOFMEMORY;
                            break;
                        }
                    }
                    allocatedLength = requiredLength;
                    deviceDetailData->cbSize = sizeof(SP_DEVICE_INTERFACE_DETAIL_DATA);
                    // Call again but actually this time to get the interface details
                    // returns TRUE if success
                    if (!SetupDiGetDeviceInterfaceDetail(deviceInfo,
                        &deviceInfoData,
                        deviceDetailData,
                        requiredLength,
                        &requiredLength,
                        &devInfoData))
                    {
                        //_LOG_DBG << "SetupDiGetDeviceInterfaceDetail Failed" << GetLastError() << endl;
                        continue;
                    }
                    // Compare to check if Intel display driver
                    if (wcsstr(deviceDetailData->DevicePath, VENDOR_INTEL) ||
                        wcsstr(deviceDetailData->DevicePath, VENDOR_INTEL_LOWERCASE)
                        )
                    {
                        //_LOG_DBG << "Intel Device Detected:" << deviceDetailData->DevicePath << endl;
                        D3DKMT_OPENADAPTERFROMDEVICENAME OpenAdapter = {};
                        OpenAdapter.pDeviceName = deviceDetailData->DevicePath;
                        // Get handle for Adapter
                        ntStatus = m_D3dKmtInterfaces.pfnOpenAdapterFromDeviceName(&OpenAdapter);
                        if (ntStatus != NO_ERROR)
                        {
                            //Failed
                            //_LOG_DBG << "OpenAdapter failed:" << deviceDetailData->DevicePath << endl;
                        }
                        else
                        {
                            m_AdapterHandle = OpenAdapter.hAdapter;
                            //_LOG_DBG << "OpenAdapter success:" << endl;
                        }
                        break;
                    }
                }
                if (NULL != deviceDetailData)
                {
                    free(deviceDetailData);
                    deviceDetailData = NULL;
                }
            }
        }

        if (NULL == m_AdapterHandle)
        {
            //Failed to get the adapter handle
            //_LOG << "Failure to get handle to adapter" << endl;
            hr = E_FAIL;
            break;
        }
        //Fill up the stCreateDeviceData parameters
        stCreateDeviceData.hAdapter = m_AdapterHandle;
        stCreateDeviceData.Flags.LegacyMode = TRUE;

        /*//Create the device
        ntStatus = m_D3dKmtInterfaces.pfnCreateDevice(&stCreateDeviceData);
        if (NO_ERROR != ntStatus)
        {
            //_LOG << "pfnCreateDevice failed" << ntStatus << std::endl;
            hr = E_FAIL;
            break;
        }
        //Save the Device handle
        m_DeviceHandle = stCreateDeviceData.hDevice;*/

        //Reached here means, setup is succesful
        hr = S_OK;
    } while (FALSE);

    //Not checking for hr status as the calling routine will do the 
    //appropriate clean up if this fails
    return hr;
}
#endif

