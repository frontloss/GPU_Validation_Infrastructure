

/* this ALWAYS GENERATED file contains the definitions for the interfaces */


 /* File created by MIDL compiler version 8.00.0595 */
/* at Mon Jun 15 12:52:00 2015
 */
/* Compiler settings for D3D_Setting.idl:
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

#ifndef __D3D_Setting_h__
#define __D3D_Setting_h__

#if defined(_MSC_VER) && (_MSC_VER >= 1020)
#pragma once
#endif

/* Forward Declarations */ 

#ifndef __ID3DSetting_FWD_DEFINED__
#define __ID3DSetting_FWD_DEFINED__
typedef interface ID3DSetting ID3DSetting;

#endif 	/* __ID3DSetting_FWD_DEFINED__ */


/* header files for imported files */
#include "oaidl.h"
#include "ocidl.h"
#include "igfxBridgeUDT.h"

#ifdef __cplusplus
extern "C"{
#endif 


#ifndef __ID3DSetting_INTERFACE_DEFINED__
#define __ID3DSetting_INTERFACE_DEFINED__

/* interface ID3DSetting */
/* [unique][helpstring][dual][uuid][object] */ 


EXTERN_C const IID IID_ID3DSetting;

#if defined(__cplusplus) && !defined(CINTERFACE)
    
    MIDL_INTERFACE("dec5b974-c1c0-4f46-8b74-ff8fa387bd23")
    ID3DSetting : public IDispatch
    {
    public:
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetD3DInfo( 
            /* [out][in] */ IGFX_D3D_INFO *pD3D,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetD3DInfo( 
            /* [out][in] */ IGFX_D3D_INFO *pD3D,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetD3DInfoEx( 
            /* [out][in] */ IGFX_D3D_INFO_EX *pD3D,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetD3DInfoEx( 
            /* [out][in] */ IGFX_D3D_INFO_EX *pD3D,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
    };
    
    
#else 	/* C style interface */

    typedef struct ID3DSettingVtbl
    {
        BEGIN_INTERFACE
        
        HRESULT ( STDMETHODCALLTYPE *QueryInterface )( 
            ID3DSetting * This,
            /* [in] */ REFIID riid,
            /* [annotation][iid_is][out] */ 
            _COM_Outptr_  void **ppvObject);
        
        ULONG ( STDMETHODCALLTYPE *AddRef )( 
            ID3DSetting * This);
        
        ULONG ( STDMETHODCALLTYPE *Release )( 
            ID3DSetting * This);
        
        HRESULT ( STDMETHODCALLTYPE *GetTypeInfoCount )( 
            ID3DSetting * This,
            /* [out] */ UINT *pctinfo);
        
        HRESULT ( STDMETHODCALLTYPE *GetTypeInfo )( 
            ID3DSetting * This,
            /* [in] */ UINT iTInfo,
            /* [in] */ LCID lcid,
            /* [out] */ ITypeInfo **ppTInfo);
        
        HRESULT ( STDMETHODCALLTYPE *GetIDsOfNames )( 
            ID3DSetting * This,
            /* [in] */ REFIID riid,
            /* [size_is][in] */ LPOLESTR *rgszNames,
            /* [range][in] */ UINT cNames,
            /* [in] */ LCID lcid,
            /* [size_is][out] */ DISPID *rgDispId);
        
        /* [local] */ HRESULT ( STDMETHODCALLTYPE *Invoke )( 
            ID3DSetting * This,
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
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetD3DInfo )( 
            ID3DSetting * This,
            /* [out][in] */ IGFX_D3D_INFO *pD3D,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetD3DInfo )( 
            ID3DSetting * This,
            /* [out][in] */ IGFX_D3D_INFO *pD3D,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetD3DInfoEx )( 
            ID3DSetting * This,
            /* [out][in] */ IGFX_D3D_INFO_EX *pD3D,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetD3DInfoEx )( 
            ID3DSetting * This,
            /* [out][in] */ IGFX_D3D_INFO_EX *pD3D,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        END_INTERFACE
    } ID3DSettingVtbl;

    interface ID3DSetting
    {
        CONST_VTBL struct ID3DSettingVtbl *lpVtbl;
    };

    

#ifdef COBJMACROS


#define ID3DSetting_QueryInterface(This,riid,ppvObject)	\
    ( (This)->lpVtbl -> QueryInterface(This,riid,ppvObject) ) 

#define ID3DSetting_AddRef(This)	\
    ( (This)->lpVtbl -> AddRef(This) ) 

#define ID3DSetting_Release(This)	\
    ( (This)->lpVtbl -> Release(This) ) 


#define ID3DSetting_GetTypeInfoCount(This,pctinfo)	\
    ( (This)->lpVtbl -> GetTypeInfoCount(This,pctinfo) ) 

#define ID3DSetting_GetTypeInfo(This,iTInfo,lcid,ppTInfo)	\
    ( (This)->lpVtbl -> GetTypeInfo(This,iTInfo,lcid,ppTInfo) ) 

#define ID3DSetting_GetIDsOfNames(This,riid,rgszNames,cNames,lcid,rgDispId)	\
    ( (This)->lpVtbl -> GetIDsOfNames(This,riid,rgszNames,cNames,lcid,rgDispId) ) 

#define ID3DSetting_Invoke(This,dispIdMember,riid,lcid,wFlags,pDispParams,pVarResult,pExcepInfo,puArgErr)	\
    ( (This)->lpVtbl -> Invoke(This,dispIdMember,riid,lcid,wFlags,pDispParams,pVarResult,pExcepInfo,puArgErr) ) 


#define ID3DSetting_GetD3DInfo(This,pD3D,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetD3DInfo(This,pD3D,pExtraErrorCode,pErrorDescription) ) 

#define ID3DSetting_SetD3DInfo(This,pD3D,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetD3DInfo(This,pD3D,pExtraErrorCode,pErrorDescription) ) 

#define ID3DSetting_GetD3DInfoEx(This,pD3D,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetD3DInfoEx(This,pD3D,pExtraErrorCode,pErrorDescription) ) 

#define ID3DSetting_SetD3DInfoEx(This,pD3D,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetD3DInfoEx(This,pD3D,pExtraErrorCode,pErrorDescription) ) 

#endif /* COBJMACROS */


#endif 	/* C style interface */




#endif 	/* __ID3DSetting_INTERFACE_DEFINED__ */


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


