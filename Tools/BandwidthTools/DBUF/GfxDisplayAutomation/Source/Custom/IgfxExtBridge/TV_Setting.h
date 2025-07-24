

/* this ALWAYS GENERATED file contains the definitions for the interfaces */


 /* File created by MIDL compiler version 8.00.0595 */
/* at Mon Jun 15 12:52:13 2015
 */
/* Compiler settings for TV_Setting.idl:
    Oicf, W1, Zp8, env=Win32 (32b run), target_arch=X86 8.00.0595 
    protocol : dce , ms_ext, c_ext, robust
    error checks: allocation ref bounds_check enum stub_data 
    VC __declspec() decoration level: 
         __declspec(uuid()), __declspec(selectany), __declspec(novtable)
         DECLSPEC_UUID(), MIDL_INTERFACE()
*/
/* @@MIDL_FILE_HEADING(  ) */

#pragma warning( disable: 4049 )  /* more than 64k source lines */


/* verify that the <rpcndr.h> version is high enough to compile this file*/
#ifndef __REQUIRED_RPCNDR_H_VERSION__
#define __REQUIRED_RPCNDR_H_VERSION__ 475
#endif

#include "rpc.h"
#include "rpcndr.h"

#ifndef __RPCNDR_H_VERSION__
#error this stub requires an updated version of <rpcndr.h>
#endif // __RPCNDR_H_VERSION__

#ifndef COM_NO_WINDOWS_H
#include "windows.h"
#include "ole2.h"
#endif /*COM_NO_WINDOWS_H*/

#ifndef __TV_Setting_h__
#define __TV_Setting_h__

#if defined(_MSC_VER) && (_MSC_VER >= 1020)
#pragma once
#endif

/* Forward Declarations */ 

#ifndef __ITVSetting_FWD_DEFINED__
#define __ITVSetting_FWD_DEFINED__
typedef interface ITVSetting ITVSetting;

#endif 	/* __ITVSetting_FWD_DEFINED__ */


/* header files for imported files */
#include "oaidl.h"
#include "ocidl.h"
#include "igfxBridgeUDT.h"

#ifdef __cplusplus
extern "C"{
#endif 


#ifndef __ITVSetting_INTERFACE_DEFINED__
#define __ITVSetting_INTERFACE_DEFINED__

/* interface ITVSetting */
/* [unique][helpstring][dual][uuid][object] */ 


EXTERN_C const IID IID_ITVSetting;

#if defined(__cplusplus) && !defined(CINTERFACE)
    
    MIDL_INTERFACE("82C03218-085D-4301-9718-9CEC0EA4721B")
    ITVSetting : public IDispatch
    {
    public:
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetAvailableConnectors( 
            /* [in] */ DWORD monitorID,
            /* [out] */ DWORD *pAvailableConnectors,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetConnectorSelection( 
            /* [in] */ DWORD monitorID,
            /* [out] */ DWORD *pAvailableConnectors,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetConnectorAttachedStatus( 
            /* [in] */ DWORD monitorID,
            /* [out] */ DWORD *pAvailableConnectors,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetConnectorSelection( 
            /* [in] */ DWORD monitorID,
            /* [in] */ DWORD availableConnector,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetTvParameters( 
            /* [in] */ DWORD monitorID,
            /* [out] */ IGFX_TV_PARAMETER_DATA *pTVParamaterData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetTvParameters( 
            /* [in] */ DWORD monitorID,
            /* [in] */ IGFX_TV_PARAMETER_DATA *pTVParamaterData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE TVTypeStdGet( 
            /* [out] */ IGFX_TV_FORMAT_EX *pTVFormat,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE TVTypeStdSet( 
            /* [in] */ IGFX_TV_FORMAT_EX *pTVFormat,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE ConnectorStatus( 
            /* [out] */ IGFX_CONNECTOR_STATUS *pConnectorStatus,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetPersistenceStatus( 
            /* [out] */ DWORD *pPersistanceStatus,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetPersistenceDisable( 
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetPersistenceEnable( 
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
    };
    
    
#else 	/* C style interface */

    typedef struct ITVSettingVtbl
    {
        BEGIN_INTERFACE
        
        HRESULT ( STDMETHODCALLTYPE *QueryInterface )( 
            ITVSetting * This,
            /* [in] */ REFIID riid,
            /* [annotation][iid_is][out] */ 
            _COM_Outptr_  void **ppvObject);
        
        ULONG ( STDMETHODCALLTYPE *AddRef )( 
            ITVSetting * This);
        
        ULONG ( STDMETHODCALLTYPE *Release )( 
            ITVSetting * This);
        
        HRESULT ( STDMETHODCALLTYPE *GetTypeInfoCount )( 
            ITVSetting * This,
            /* [out] */ UINT *pctinfo);
        
        HRESULT ( STDMETHODCALLTYPE *GetTypeInfo )( 
            ITVSetting * This,
            /* [in] */ UINT iTInfo,
            /* [in] */ LCID lcid,
            /* [out] */ ITypeInfo **ppTInfo);
        
        HRESULT ( STDMETHODCALLTYPE *GetIDsOfNames )( 
            ITVSetting * This,
            /* [in] */ REFIID riid,
            /* [size_is][in] */ LPOLESTR *rgszNames,
            /* [range][in] */ UINT cNames,
            /* [in] */ LCID lcid,
            /* [size_is][out] */ DISPID *rgDispId);
        
        /* [local] */ HRESULT ( STDMETHODCALLTYPE *Invoke )( 
            ITVSetting * This,
            /* [annotation][in] */ 
            _In_  DISPID dispIdMember,
            /* [annotation][in] */ 
            _In_  REFIID riid,
            /* [annotation][in] */ 
            _In_  LCID lcid,
            /* [annotation][in] */ 
            _In_  WORD wFlags,
            /* [annotation][out][in] */ 
            _In_  DISPPARAMS *pDispParams,
            /* [annotation][out] */ 
            _Out_opt_  VARIANT *pVarResult,
            /* [annotation][out] */ 
            _Out_opt_  EXCEPINFO *pExcepInfo,
            /* [annotation][out] */ 
            _Out_opt_  UINT *puArgErr);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetAvailableConnectors )( 
            ITVSetting * This,
            /* [in] */ DWORD monitorID,
            /* [out] */ DWORD *pAvailableConnectors,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetConnectorSelection )( 
            ITVSetting * This,
            /* [in] */ DWORD monitorID,
            /* [out] */ DWORD *pAvailableConnectors,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetConnectorAttachedStatus )( 
            ITVSetting * This,
            /* [in] */ DWORD monitorID,
            /* [out] */ DWORD *pAvailableConnectors,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetConnectorSelection )( 
            ITVSetting * This,
            /* [in] */ DWORD monitorID,
            /* [in] */ DWORD availableConnector,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetTvParameters )( 
            ITVSetting * This,
            /* [in] */ DWORD monitorID,
            /* [out] */ IGFX_TV_PARAMETER_DATA *pTVParamaterData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetTvParameters )( 
            ITVSetting * This,
            /* [in] */ DWORD monitorID,
            /* [in] */ IGFX_TV_PARAMETER_DATA *pTVParamaterData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *TVTypeStdGet )( 
            ITVSetting * This,
            /* [out] */ IGFX_TV_FORMAT_EX *pTVFormat,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *TVTypeStdSet )( 
            ITVSetting * This,
            /* [in] */ IGFX_TV_FORMAT_EX *pTVFormat,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *ConnectorStatus )( 
            ITVSetting * This,
            /* [out] */ IGFX_CONNECTOR_STATUS *pConnectorStatus,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetPersistenceStatus )( 
            ITVSetting * This,
            /* [out] */ DWORD *pPersistanceStatus,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetPersistenceDisable )( 
            ITVSetting * This,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetPersistenceEnable )( 
            ITVSetting * This,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        END_INTERFACE
    } ITVSettingVtbl;

    interface ITVSetting
    {
        CONST_VTBL struct ITVSettingVtbl *lpVtbl;
    };

    

#ifdef COBJMACROS


#define ITVSetting_QueryInterface(This,riid,ppvObject)	\
    ( (This)->lpVtbl -> QueryInterface(This,riid,ppvObject) ) 

#define ITVSetting_AddRef(This)	\
    ( (This)->lpVtbl -> AddRef(This) ) 

#define ITVSetting_Release(This)	\
    ( (This)->lpVtbl -> Release(This) ) 


#define ITVSetting_GetTypeInfoCount(This,pctinfo)	\
    ( (This)->lpVtbl -> GetTypeInfoCount(This,pctinfo) ) 

#define ITVSetting_GetTypeInfo(This,iTInfo,lcid,ppTInfo)	\
    ( (This)->lpVtbl -> GetTypeInfo(This,iTInfo,lcid,ppTInfo) ) 

#define ITVSetting_GetIDsOfNames(This,riid,rgszNames,cNames,lcid,rgDispId)	\
    ( (This)->lpVtbl -> GetIDsOfNames(This,riid,rgszNames,cNames,lcid,rgDispId) ) 

#define ITVSetting_Invoke(This,dispIdMember,riid,lcid,wFlags,pDispParams,pVarResult,pExcepInfo,puArgErr)	\
    ( (This)->lpVtbl -> Invoke(This,dispIdMember,riid,lcid,wFlags,pDispParams,pVarResult,pExcepInfo,puArgErr) ) 


#define ITVSetting_GetAvailableConnectors(This,monitorID,pAvailableConnectors,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetAvailableConnectors(This,monitorID,pAvailableConnectors,pExtraErrorCode,pErrorDescription) ) 

#define ITVSetting_GetConnectorSelection(This,monitorID,pAvailableConnectors,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetConnectorSelection(This,monitorID,pAvailableConnectors,pExtraErrorCode,pErrorDescription) ) 

#define ITVSetting_GetConnectorAttachedStatus(This,monitorID,pAvailableConnectors,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetConnectorAttachedStatus(This,monitorID,pAvailableConnectors,pExtraErrorCode,pErrorDescription) ) 

#define ITVSetting_SetConnectorSelection(This,monitorID,availableConnector,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetConnectorSelection(This,monitorID,availableConnector,pExtraErrorCode,pErrorDescription) ) 

#define ITVSetting_GetTvParameters(This,monitorID,pTVParamaterData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetTvParameters(This,monitorID,pTVParamaterData,pExtraErrorCode,pErrorDescription) ) 

#define ITVSetting_SetTvParameters(This,monitorID,pTVParamaterData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetTvParameters(This,monitorID,pTVParamaterData,pExtraErrorCode,pErrorDescription) ) 

#define ITVSetting_TVTypeStdGet(This,pTVFormat,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> TVTypeStdGet(This,pTVFormat,pExtraErrorCode,pErrorDescription) ) 

#define ITVSetting_TVTypeStdSet(This,pTVFormat,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> TVTypeStdSet(This,pTVFormat,pExtraErrorCode,pErrorDescription) ) 

#define ITVSetting_ConnectorStatus(This,pConnectorStatus,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> ConnectorStatus(This,pConnectorStatus,pExtraErrorCode,pErrorDescription) ) 

#define ITVSetting_GetPersistenceStatus(This,pPersistanceStatus,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetPersistenceStatus(This,pPersistanceStatus,pExtraErrorCode,pErrorDescription) ) 

#define ITVSetting_SetPersistenceDisable(This,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetPersistenceDisable(This,pExtraErrorCode,pErrorDescription) ) 

#define ITVSetting_SetPersistenceEnable(This,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetPersistenceEnable(This,pExtraErrorCode,pErrorDescription) ) 

#endif /* COBJMACROS */


#endif 	/* C style interface */




#endif 	/* __ITVSetting_INTERFACE_DEFINED__ */


/* Additional Prototypes for ALL interfaces */

unsigned long             __RPC_USER  BSTR_UserSize(     unsigned long *, unsigned long            , BSTR * ); 
unsigned char * __RPC_USER  BSTR_UserMarshal(  unsigned long *, unsigned char *, BSTR * ); 
unsigned char * __RPC_USER  BSTR_UserUnmarshal(unsigned long *, unsigned char *, BSTR * ); 
void                      __RPC_USER  BSTR_UserFree(     unsigned long *, BSTR * ); 

/* end of Additional Prototypes */

#ifdef __cplusplus
}
#endif

#endif


