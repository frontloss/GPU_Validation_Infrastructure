

/* this ALWAYS GENERATED file contains the definitions for the interfaces */


 /* File created by MIDL compiler version 8.00.0595 */
/* at Mon Jun 15 12:52:09 2015
 */
/* Compiler settings for Power_Util.idl:
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

#ifndef __Power_Util_h__
#define __Power_Util_h__

#if defined(_MSC_VER) && (_MSC_VER >= 1020)
#pragma once
#endif

/* Forward Declarations */ 

#ifndef __IPowerUtil_FWD_DEFINED__
#define __IPowerUtil_FWD_DEFINED__
typedef interface IPowerUtil IPowerUtil;

#endif 	/* __IPowerUtil_FWD_DEFINED__ */


/* header files for imported files */
#include "oaidl.h"
#include "ocidl.h"
#include "igfxBridgeUDT.h"

#ifdef __cplusplus
extern "C"{
#endif 


#ifndef __IPowerUtil_INTERFACE_DEFINED__
#define __IPowerUtil_INTERFACE_DEFINED__

/* interface IPowerUtil */
/* [unique][helpstring][dual][uuid][object] */ 


EXTERN_C const IID IID_IPowerUtil;

#if defined(__cplusplus) && !defined(CINTERFACE)
    
    MIDL_INTERFACE("A8B30857-69FB-44ba-B6CB-DE06D9152CF5")
    IPowerUtil : public IDispatch
    {
    public:
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE PowerApiOpen( 
            DWORD *punHandle,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE PowerApiClose( 
            DWORD punHandle,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetPowerConsCaps( 
            DWORD handle,
            DWORD *pCaps,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetPowerPolicy_DFGT( 
            DWORD handle,
            DWORD PolicyID,
            DWORD AcDc,
            IGFX_DFGT_POLICY_1_0 *Policy,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetPowerPolicy_DFGT( 
            DWORD handle,
            DWORD PolicyID,
            DWORD AcDc,
            IGFX_DFGT_POLICY_1_0 *Policy,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetPowerPolicy_DPST( 
            DWORD handle,
            DWORD PolicyID,
            IGFX_DPST_POLICY_1_0 *Policy,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetPowerPolicy_DPST( 
            DWORD handle,
            DWORD PolicyID,
            IGFX_DPST_POLICY_1_0 *Policy,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetInverterParams( 
            DWORD PolicyID,
            IGFX_POWER_PARAMS_0 *powerPolicy,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetInverterParams( 
            DWORD PolicyID,
            IGFX_POWER_PARAMS_0 *powerPolicy,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetPowerPolicyAll( 
            DWORD handle,
            DWORD PolicyID,
            DWORD *Policy,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetPowerPolicyAll( 
            DWORD handle,
            DWORD PolicyID,
            DWORD *Policy,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetPowerInfo( 
            /* [out][in] */ IGFX_POWER_CONSERVATION_DATA *pData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetPowerInfo( 
            /* [out][in] */ IGFX_POWER_CONSERVATION_DATA *pData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetPowerPolicy_ADB( 
            DWORD handle,
            DWORD PolicyID,
            IGFX_ADB_POLICY_1_0 *Policy,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetPowerPolicy_ADB( 
            DWORD handle,
            DWORD PolicyID,
            IGFX_ADB_POLICY_1_0 *Policy,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription) = 0;
        
    };
    
    
#else 	/* C style interface */

    typedef struct IPowerUtilVtbl
    {
        BEGIN_INTERFACE
        
        HRESULT ( STDMETHODCALLTYPE *QueryInterface )( 
            IPowerUtil * This,
            /* [in] */ REFIID riid,
            /* [annotation][iid_is][out] */ 
            _COM_Outptr_  void **ppvObject);
        
        ULONG ( STDMETHODCALLTYPE *AddRef )( 
            IPowerUtil * This);
        
        ULONG ( STDMETHODCALLTYPE *Release )( 
            IPowerUtil * This);
        
        HRESULT ( STDMETHODCALLTYPE *GetTypeInfoCount )( 
            IPowerUtil * This,
            /* [out] */ UINT *pctinfo);
        
        HRESULT ( STDMETHODCALLTYPE *GetTypeInfo )( 
            IPowerUtil * This,
            /* [in] */ UINT iTInfo,
            /* [in] */ LCID lcid,
            /* [out] */ ITypeInfo **ppTInfo);
        
        HRESULT ( STDMETHODCALLTYPE *GetIDsOfNames )( 
            IPowerUtil * This,
            /* [in] */ REFIID riid,
            /* [size_is][in] */ LPOLESTR *rgszNames,
            /* [range][in] */ UINT cNames,
            /* [in] */ LCID lcid,
            /* [size_is][out] */ DISPID *rgDispId);
        
        /* [local] */ HRESULT ( STDMETHODCALLTYPE *Invoke )( 
            IPowerUtil * This,
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
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *PowerApiOpen )( 
            IPowerUtil * This,
            DWORD *punHandle,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *PowerApiClose )( 
            IPowerUtil * This,
            DWORD punHandle,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetPowerConsCaps )( 
            IPowerUtil * This,
            DWORD handle,
            DWORD *pCaps,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetPowerPolicy_DFGT )( 
            IPowerUtil * This,
            DWORD handle,
            DWORD PolicyID,
            DWORD AcDc,
            IGFX_DFGT_POLICY_1_0 *Policy,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetPowerPolicy_DFGT )( 
            IPowerUtil * This,
            DWORD handle,
            DWORD PolicyID,
            DWORD AcDc,
            IGFX_DFGT_POLICY_1_0 *Policy,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetPowerPolicy_DPST )( 
            IPowerUtil * This,
            DWORD handle,
            DWORD PolicyID,
            IGFX_DPST_POLICY_1_0 *Policy,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetPowerPolicy_DPST )( 
            IPowerUtil * This,
            DWORD handle,
            DWORD PolicyID,
            IGFX_DPST_POLICY_1_0 *Policy,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetInverterParams )( 
            IPowerUtil * This,
            DWORD PolicyID,
            IGFX_POWER_PARAMS_0 *powerPolicy,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetInverterParams )( 
            IPowerUtil * This,
            DWORD PolicyID,
            IGFX_POWER_PARAMS_0 *powerPolicy,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetPowerPolicyAll )( 
            IPowerUtil * This,
            DWORD handle,
            DWORD PolicyID,
            DWORD *Policy,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetPowerPolicyAll )( 
            IPowerUtil * This,
            DWORD handle,
            DWORD PolicyID,
            DWORD *Policy,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetPowerInfo )( 
            IPowerUtil * This,
            /* [out][in] */ IGFX_POWER_CONSERVATION_DATA *pData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetPowerInfo )( 
            IPowerUtil * This,
            /* [out][in] */ IGFX_POWER_CONSERVATION_DATA *pData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetPowerPolicy_ADB )( 
            IPowerUtil * This,
            DWORD handle,
            DWORD PolicyID,
            IGFX_ADB_POLICY_1_0 *Policy,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetPowerPolicy_ADB )( 
            IPowerUtil * This,
            DWORD handle,
            DWORD PolicyID,
            IGFX_ADB_POLICY_1_0 *Policy,
            IGFX_ERROR_CODES *pExtraErrorCode,
            BSTR *pErrorDescription);
        
        END_INTERFACE
    } IPowerUtilVtbl;

    interface IPowerUtil
    {
        CONST_VTBL struct IPowerUtilVtbl *lpVtbl;
    };

    

#ifdef COBJMACROS


#define IPowerUtil_QueryInterface(This,riid,ppvObject)	\
    ( (This)->lpVtbl -> QueryInterface(This,riid,ppvObject) ) 

#define IPowerUtil_AddRef(This)	\
    ( (This)->lpVtbl -> AddRef(This) ) 

#define IPowerUtil_Release(This)	\
    ( (This)->lpVtbl -> Release(This) ) 


#define IPowerUtil_GetTypeInfoCount(This,pctinfo)	\
    ( (This)->lpVtbl -> GetTypeInfoCount(This,pctinfo) ) 

#define IPowerUtil_GetTypeInfo(This,iTInfo,lcid,ppTInfo)	\
    ( (This)->lpVtbl -> GetTypeInfo(This,iTInfo,lcid,ppTInfo) ) 

#define IPowerUtil_GetIDsOfNames(This,riid,rgszNames,cNames,lcid,rgDispId)	\
    ( (This)->lpVtbl -> GetIDsOfNames(This,riid,rgszNames,cNames,lcid,rgDispId) ) 

#define IPowerUtil_Invoke(This,dispIdMember,riid,lcid,wFlags,pDispParams,pVarResult,pExcepInfo,puArgErr)	\
    ( (This)->lpVtbl -> Invoke(This,dispIdMember,riid,lcid,wFlags,pDispParams,pVarResult,pExcepInfo,puArgErr) ) 


#define IPowerUtil_PowerApiOpen(This,punHandle,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> PowerApiOpen(This,punHandle,pExtraErrorCode,pErrorDescription) ) 

#define IPowerUtil_PowerApiClose(This,punHandle,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> PowerApiClose(This,punHandle,pExtraErrorCode,pErrorDescription) ) 

#define IPowerUtil_GetPowerConsCaps(This,handle,pCaps,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetPowerConsCaps(This,handle,pCaps,pExtraErrorCode,pErrorDescription) ) 

#define IPowerUtil_GetPowerPolicy_DFGT(This,handle,PolicyID,AcDc,Policy,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetPowerPolicy_DFGT(This,handle,PolicyID,AcDc,Policy,pExtraErrorCode,pErrorDescription) ) 

#define IPowerUtil_SetPowerPolicy_DFGT(This,handle,PolicyID,AcDc,Policy,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetPowerPolicy_DFGT(This,handle,PolicyID,AcDc,Policy,pExtraErrorCode,pErrorDescription) ) 

#define IPowerUtil_GetPowerPolicy_DPST(This,handle,PolicyID,Policy,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetPowerPolicy_DPST(This,handle,PolicyID,Policy,pExtraErrorCode,pErrorDescription) ) 

#define IPowerUtil_SetPowerPolicy_DPST(This,handle,PolicyID,Policy,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetPowerPolicy_DPST(This,handle,PolicyID,Policy,pExtraErrorCode,pErrorDescription) ) 

#define IPowerUtil_GetInverterParams(This,PolicyID,powerPolicy,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetInverterParams(This,PolicyID,powerPolicy,pExtraErrorCode,pErrorDescription) ) 

#define IPowerUtil_SetInverterParams(This,PolicyID,powerPolicy,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetInverterParams(This,PolicyID,powerPolicy,pExtraErrorCode,pErrorDescription) ) 

#define IPowerUtil_SetPowerPolicyAll(This,handle,PolicyID,Policy,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetPowerPolicyAll(This,handle,PolicyID,Policy,pExtraErrorCode,pErrorDescription) ) 

#define IPowerUtil_GetPowerPolicyAll(This,handle,PolicyID,Policy,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetPowerPolicyAll(This,handle,PolicyID,Policy,pExtraErrorCode,pErrorDescription) ) 

#define IPowerUtil_GetPowerInfo(This,pData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetPowerInfo(This,pData,pExtraErrorCode,pErrorDescription) ) 

#define IPowerUtil_SetPowerInfo(This,pData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetPowerInfo(This,pData,pExtraErrorCode,pErrorDescription) ) 

#define IPowerUtil_GetPowerPolicy_ADB(This,handle,PolicyID,Policy,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetPowerPolicy_ADB(This,handle,PolicyID,Policy,pExtraErrorCode,pErrorDescription) ) 

#define IPowerUtil_SetPowerPolicy_ADB(This,handle,PolicyID,Policy,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetPowerPolicy_ADB(This,handle,PolicyID,Policy,pExtraErrorCode,pErrorDescription) ) 

#endif /* COBJMACROS */


#endif 	/* C style interface */




#endif 	/* __IPowerUtil_INTERFACE_DEFINED__ */


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


