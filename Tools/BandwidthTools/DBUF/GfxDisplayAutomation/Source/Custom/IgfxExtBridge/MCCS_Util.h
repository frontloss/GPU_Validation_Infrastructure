

/* this ALWAYS GENERATED file contains the definitions for the interfaces */


 /* File created by MIDL compiler version 8.00.0595 */
/* at Mon Jun 15 12:52:08 2015
 */
/* Compiler settings for MCCS_Util.idl:
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

#ifndef __MCCS_Util_h__
#define __MCCS_Util_h__

#if defined(_MSC_VER) && (_MSC_VER >= 1020)
#pragma once
#endif

/* Forward Declarations */ 

#ifndef __IMCCSUtil_FWD_DEFINED__
#define __IMCCSUtil_FWD_DEFINED__
typedef interface IMCCSUtil IMCCSUtil;

#endif 	/* __IMCCSUtil_FWD_DEFINED__ */


/* header files for imported files */
#include "oaidl.h"
#include "ocidl.h"
#include "igfxBridgeUDT.h"

#ifdef __cplusplus
extern "C"{
#endif 


#ifndef __IMCCSUtil_INTERFACE_DEFINED__
#define __IMCCSUtil_INTERFACE_DEFINED__

/* interface IMCCSUtil */
/* [unique][helpstring][dual][uuid][object] */ 


EXTERN_C const IID IID_IMCCSUtil;

#if defined(__cplusplus) && !defined(CINTERFACE)
    
    MIDL_INTERFACE("0F470F34-D410-4dc8-A3F9-3C36D65D8BCF")
    IMCCSUtil : public IDispatch
    {
    public:
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE Open( 
            /* [in] */ DWORD monitorID,
            /* [out] */ DWORD *pHandle,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE Close( 
            /* [in] */ DWORD dwHandle,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE Max( 
            /* [in] */ DWORD dwHandle,
            /* [in] */ DWORD controlCode,
            /* [in] */ DWORD size,
            /* [out][in] */ DWORD *pVal,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE Min( 
            /* [in] */ DWORD dwHandle,
            /* [in] */ DWORD controlCode,
            /* [in] */ DWORD size,
            /* [out][in] */ DWORD *pVal,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE ResetControl( 
            /* [in] */ DWORD dwHandle,
            /* [in] */ DWORD controlCode,
            /* [in] */ DWORD size,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetCurrent( 
            /* [in] */ DWORD dwHandle,
            /* [in] */ DWORD controlCode,
            /* [in] */ DWORD size,
            /* [out][in] */ DWORD *pVal,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetCurrent( 
            /* [in] */ DWORD dwHandle,
            /* [in] */ DWORD controlCode,
            /* [in] */ DWORD size,
            /* [in] */ DWORD pVal,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetCapability( 
            /* [in] */ DWORD monitorID,
            /* [out] */ BSTR *pCapabilities,
            /* [out][in] */ DWORD *pSize,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE ParseCapabilityCmds( 
            /* [in] */ BSTR *pCapabilities,
            /* [in] */ DWORD *pCmdArray,
            /* [out] */ DWORD *pTotalCmds,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE ParseCapabilityVCP( 
            /* [in] */ BSTR *pCapabilities,
            /* [in] */ DWORD *pVcpArray,
            /* [out] */ DWORD *pTotalCmds,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE Get( 
            /* [out][in] */ IGFX_MCCS_DATA *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE Set( 
            /* [out][in] */ IGFX_MCCS_DATA *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
    };
    
    
#else 	/* C style interface */

    typedef struct IMCCSUtilVtbl
    {
        BEGIN_INTERFACE
        
        HRESULT ( STDMETHODCALLTYPE *QueryInterface )( 
            IMCCSUtil * This,
            /* [in] */ REFIID riid,
            /* [annotation][iid_is][out] */ 
            _COM_Outptr_  void **ppvObject);
        
        ULONG ( STDMETHODCALLTYPE *AddRef )( 
            IMCCSUtil * This);
        
        ULONG ( STDMETHODCALLTYPE *Release )( 
            IMCCSUtil * This);
        
        HRESULT ( STDMETHODCALLTYPE *GetTypeInfoCount )( 
            IMCCSUtil * This,
            /* [out] */ UINT *pctinfo);
        
        HRESULT ( STDMETHODCALLTYPE *GetTypeInfo )( 
            IMCCSUtil * This,
            /* [in] */ UINT iTInfo,
            /* [in] */ LCID lcid,
            /* [out] */ ITypeInfo **ppTInfo);
        
        HRESULT ( STDMETHODCALLTYPE *GetIDsOfNames )( 
            IMCCSUtil * This,
            /* [in] */ REFIID riid,
            /* [size_is][in] */ LPOLESTR *rgszNames,
            /* [range][in] */ UINT cNames,
            /* [in] */ LCID lcid,
            /* [size_is][out] */ DISPID *rgDispId);
        
        /* [local] */ HRESULT ( STDMETHODCALLTYPE *Invoke )( 
            IMCCSUtil * This,
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
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *Open )( 
            IMCCSUtil * This,
            /* [in] */ DWORD monitorID,
            /* [out] */ DWORD *pHandle,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *Close )( 
            IMCCSUtil * This,
            /* [in] */ DWORD dwHandle,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *Max )( 
            IMCCSUtil * This,
            /* [in] */ DWORD dwHandle,
            /* [in] */ DWORD controlCode,
            /* [in] */ DWORD size,
            /* [out][in] */ DWORD *pVal,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *Min )( 
            IMCCSUtil * This,
            /* [in] */ DWORD dwHandle,
            /* [in] */ DWORD controlCode,
            /* [in] */ DWORD size,
            /* [out][in] */ DWORD *pVal,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *ResetControl )( 
            IMCCSUtil * This,
            /* [in] */ DWORD dwHandle,
            /* [in] */ DWORD controlCode,
            /* [in] */ DWORD size,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetCurrent )( 
            IMCCSUtil * This,
            /* [in] */ DWORD dwHandle,
            /* [in] */ DWORD controlCode,
            /* [in] */ DWORD size,
            /* [out][in] */ DWORD *pVal,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetCurrent )( 
            IMCCSUtil * This,
            /* [in] */ DWORD dwHandle,
            /* [in] */ DWORD controlCode,
            /* [in] */ DWORD size,
            /* [in] */ DWORD pVal,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetCapability )( 
            IMCCSUtil * This,
            /* [in] */ DWORD monitorID,
            /* [out] */ BSTR *pCapabilities,
            /* [out][in] */ DWORD *pSize,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *ParseCapabilityCmds )( 
            IMCCSUtil * This,
            /* [in] */ BSTR *pCapabilities,
            /* [in] */ DWORD *pCmdArray,
            /* [out] */ DWORD *pTotalCmds,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *ParseCapabilityVCP )( 
            IMCCSUtil * This,
            /* [in] */ BSTR *pCapabilities,
            /* [in] */ DWORD *pVcpArray,
            /* [out] */ DWORD *pTotalCmds,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *Get )( 
            IMCCSUtil * This,
            /* [out][in] */ IGFX_MCCS_DATA *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *Set )( 
            IMCCSUtil * This,
            /* [out][in] */ IGFX_MCCS_DATA *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        END_INTERFACE
    } IMCCSUtilVtbl;

    interface IMCCSUtil
    {
        CONST_VTBL struct IMCCSUtilVtbl *lpVtbl;
    };

    

#ifdef COBJMACROS


#define IMCCSUtil_QueryInterface(This,riid,ppvObject)	\
    ( (This)->lpVtbl -> QueryInterface(This,riid,ppvObject) ) 

#define IMCCSUtil_AddRef(This)	\
    ( (This)->lpVtbl -> AddRef(This) ) 

#define IMCCSUtil_Release(This)	\
    ( (This)->lpVtbl -> Release(This) ) 


#define IMCCSUtil_GetTypeInfoCount(This,pctinfo)	\
    ( (This)->lpVtbl -> GetTypeInfoCount(This,pctinfo) ) 

#define IMCCSUtil_GetTypeInfo(This,iTInfo,lcid,ppTInfo)	\
    ( (This)->lpVtbl -> GetTypeInfo(This,iTInfo,lcid,ppTInfo) ) 

#define IMCCSUtil_GetIDsOfNames(This,riid,rgszNames,cNames,lcid,rgDispId)	\
    ( (This)->lpVtbl -> GetIDsOfNames(This,riid,rgszNames,cNames,lcid,rgDispId) ) 

#define IMCCSUtil_Invoke(This,dispIdMember,riid,lcid,wFlags,pDispParams,pVarResult,pExcepInfo,puArgErr)	\
    ( (This)->lpVtbl -> Invoke(This,dispIdMember,riid,lcid,wFlags,pDispParams,pVarResult,pExcepInfo,puArgErr) ) 


#define IMCCSUtil_Open(This,monitorID,pHandle,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> Open(This,monitorID,pHandle,pExtraErrorCode,pErrorDescription) ) 

#define IMCCSUtil_Close(This,dwHandle,pErrorDescription)	\
    ( (This)->lpVtbl -> Close(This,dwHandle,pErrorDescription) ) 

#define IMCCSUtil_Max(This,dwHandle,controlCode,size,pVal,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> Max(This,dwHandle,controlCode,size,pVal,pExtraErrorCode,pErrorDescription) ) 

#define IMCCSUtil_Min(This,dwHandle,controlCode,size,pVal,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> Min(This,dwHandle,controlCode,size,pVal,pExtraErrorCode,pErrorDescription) ) 

#define IMCCSUtil_ResetControl(This,dwHandle,controlCode,size,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> ResetControl(This,dwHandle,controlCode,size,pExtraErrorCode,pErrorDescription) ) 

#define IMCCSUtil_GetCurrent(This,dwHandle,controlCode,size,pVal,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetCurrent(This,dwHandle,controlCode,size,pVal,pExtraErrorCode,pErrorDescription) ) 

#define IMCCSUtil_SetCurrent(This,dwHandle,controlCode,size,pVal,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetCurrent(This,dwHandle,controlCode,size,pVal,pExtraErrorCode,pErrorDescription) ) 

#define IMCCSUtil_GetCapability(This,monitorID,pCapabilities,pSize,pErrorDescription)	\
    ( (This)->lpVtbl -> GetCapability(This,monitorID,pCapabilities,pSize,pErrorDescription) ) 

#define IMCCSUtil_ParseCapabilityCmds(This,pCapabilities,pCmdArray,pTotalCmds,pErrorDescription)	\
    ( (This)->lpVtbl -> ParseCapabilityCmds(This,pCapabilities,pCmdArray,pTotalCmds,pErrorDescription) ) 

#define IMCCSUtil_ParseCapabilityVCP(This,pCapabilities,pVcpArray,pTotalCmds,pErrorDescription)	\
    ( (This)->lpVtbl -> ParseCapabilityVCP(This,pCapabilities,pVcpArray,pTotalCmds,pErrorDescription) ) 

#define IMCCSUtil_Get(This,pBuffer,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> Get(This,pBuffer,pExtraErrorCode,pErrorDescription) ) 

#define IMCCSUtil_Set(This,pBuffer,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> Set(This,pBuffer,pExtraErrorCode,pErrorDescription) ) 

#endif /* COBJMACROS */


#endif 	/* C style interface */




#endif 	/* __IMCCSUtil_INTERFACE_DEFINED__ */


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


