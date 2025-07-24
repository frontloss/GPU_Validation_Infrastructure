

/* this ALWAYS GENERATED file contains the proxy stub code */


 /* File created by MIDL compiler version 8.00.0595 */
/* at Mon Jun 15 12:52:02 2015
 */
/* Compiler settings for Display_Util.idl:
    Oicf, W1, Zp8, env=Win32 (32b run), target_arch=X86 8.00.0595 
    protocol : dce , ms_ext, c_ext, robust
    error checks: allocation ref bounds_check enum stub_data 
    VC __declspec() decoration level: 
         __declspec(uuid()), __declspec(selectany), __declspec(novtable)
         DECLSPEC_UUID(), MIDL_INTERFACE()
*/
/* @@MIDL_FILE_HEADING(  ) */

#if !defined(_M_IA64) && !defined(_M_AMD64) && !defined(_ARM_)


#pragma warning( disable: 4049 )  /* more than 64k source lines */
#if _MSC_VER >= 1200
#pragma warning(push)
#endif

#pragma warning( disable: 4211 )  /* redefine extern to static */
#pragma warning( disable: 4232 )  /* dllimport identity*/
#pragma warning( disable: 4024 )  /* array to pointer mapping*/
#pragma warning( disable: 4152 )  /* function/data pointer conversion in expression */
#pragma warning( disable: 4100 ) /* unreferenced arguments in x86 call */

#pragma optimize("", off ) 

#define USE_STUBLESS_PROXY


/* verify that the <rpcproxy.h> version is high enough to compile this file*/
#ifndef __REDQ_RPCPROXY_H_VERSION__
#define __REQUIRED_RPCPROXY_H_VERSION__ 475
#endif


#include "rpcproxy.h"
#ifndef __RPCPROXY_H_VERSION__
#error this stub requires an updated version of <rpcproxy.h>
#endif /* __RPCPROXY_H_VERSION__ */


#include "Display_Util.h"

#define TYPE_FORMAT_STRING_SIZE   1575                              
#define PROC_FORMAT_STRING_SIZE   6817                              
#define EXPR_FORMAT_STRING_SIZE   1                                 
#define TRANSMIT_AS_TABLE_SIZE    0            
#define WIRE_MARSHAL_TABLE_SIZE   1            

typedef struct _Display_Util_MIDL_TYPE_FORMAT_STRING
    {
    short          Pad;
    unsigned char  Format[ TYPE_FORMAT_STRING_SIZE ];
    } Display_Util_MIDL_TYPE_FORMAT_STRING;

typedef struct _Display_Util_MIDL_PROC_FORMAT_STRING
    {
    short          Pad;
    unsigned char  Format[ PROC_FORMAT_STRING_SIZE ];
    } Display_Util_MIDL_PROC_FORMAT_STRING;

typedef struct _Display_Util_MIDL_EXPR_FORMAT_STRING
    {
    long          Pad;
    unsigned char  Format[ EXPR_FORMAT_STRING_SIZE ];
    } Display_Util_MIDL_EXPR_FORMAT_STRING;


static const RPC_SYNTAX_IDENTIFIER  _RpcTransferSyntax = 
{{0x8A885D04,0x1CEB,0x11C9,{0x9F,0xE8,0x08,0x00,0x2B,0x10,0x48,0x60}},{2,0}};


extern const Display_Util_MIDL_TYPE_FORMAT_STRING Display_Util__MIDL_TypeFormatString;
extern const Display_Util_MIDL_PROC_FORMAT_STRING Display_Util__MIDL_ProcFormatString;
extern const Display_Util_MIDL_EXPR_FORMAT_STRING Display_Util__MIDL_ExprFormatString;


extern const MIDL_STUB_DESC Object_StubDesc;


extern const MIDL_SERVER_INFO IDisplayUtil_ServerInfo;
extern const MIDL_STUBLESS_PROXY_INFO IDisplayUtil_ProxyInfo;

/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_GetDisplayInformation_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ DWORD *pDisplayInfo,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription)
{
CLIENT_CALL_RETURN _RetVal;

_RetVal = NdrClientCall2(
                  ( PMIDL_STUB_DESC  )&Object_StubDesc,
                  (PFORMAT_STRING) &Display_Util__MIDL_ProcFormatString.Format[6132],
                  ( unsigned char * )&This);
return ( HRESULT  )_RetVal.Simple;

}

/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_GetIndividualRefreshRate_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ REFRESHRATE *rr,
    /* [out][in] */ REFRESHRATE refreshrate[ 20 ],
    /* [in] */ DWORD index,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription)
{
CLIENT_CALL_RETURN _RetVal;

_RetVal = NdrClientCall2(
                  ( PMIDL_STUB_DESC  )&Object_StubDesc,
                  (PFORMAT_STRING) &Display_Util__MIDL_ProcFormatString.Format[6180],
                  ( unsigned char * )&This);
return ( HRESULT  )_RetVal.Simple;

}

/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_GetBusInfo_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_BUS_INFO *pBusInfo,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription)
{
CLIENT_CALL_RETURN _RetVal;

_RetVal = NdrClientCall2(
                  ( PMIDL_STUB_DESC  )&Object_StubDesc,
                  (PFORMAT_STRING) &Display_Util__MIDL_ProcFormatString.Format[6240],
                  ( unsigned char * )&This);
return ( HRESULT  )_RetVal.Simple;

}

/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_SetBusInfo_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_BUS_INFO *pBusInfo,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription)
{
CLIENT_CALL_RETURN _RetVal;

_RetVal = NdrClientCall2(
                  ( PMIDL_STUB_DESC  )&Object_StubDesc,
                  (PFORMAT_STRING) &Display_Util__MIDL_ProcFormatString.Format[6288],
                  ( unsigned char * )&This);
return ( HRESULT  )_RetVal.Simple;

}

/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_GetAviInfoFrameEx_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_AVI_INFOFRAME_EX *pAVIFrameInfoEx,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription)
{
CLIENT_CALL_RETURN _RetVal;

_RetVal = NdrClientCall2(
                  ( PMIDL_STUB_DESC  )&Object_StubDesc,
                  (PFORMAT_STRING) &Display_Util__MIDL_ProcFormatString.Format[6336],
                  ( unsigned char * )&This);
return ( HRESULT  )_RetVal.Simple;

}

/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_SetAviInfoFrameEx_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_AVI_INFOFRAME_EX *pAVIFrameInfoEx,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription)
{
CLIENT_CALL_RETURN _RetVal;

_RetVal = NdrClientCall2(
                  ( PMIDL_STUB_DESC  )&Object_StubDesc,
                  (PFORMAT_STRING) &Display_Util__MIDL_ProcFormatString.Format[6384],
                  ( unsigned char * )&This);
return ( HRESULT  )_RetVal.Simple;

}

/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_GetBezel_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_BEZEL_CONFIG *pBezelConfig,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription)
{
CLIENT_CALL_RETURN _RetVal;

_RetVal = NdrClientCall2(
                  ( PMIDL_STUB_DESC  )&Object_StubDesc,
                  (PFORMAT_STRING) &Display_Util__MIDL_ProcFormatString.Format[6432],
                  ( unsigned char * )&This);
return ( HRESULT  )_RetVal.Simple;

}

/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_SetBezel_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_BEZEL_CONFIG *pBezelConfig,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription)
{
CLIENT_CALL_RETURN _RetVal;

_RetVal = NdrClientCall2(
                  ( PMIDL_STUB_DESC  )&Object_StubDesc,
                  (PFORMAT_STRING) &Display_Util__MIDL_ProcFormatString.Format[6480],
                  ( unsigned char * )&This);
return ( HRESULT  )_RetVal.Simple;

}

/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_GetCollageStatus_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_COLLAGE_STATUS *pCollageStatus,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription)
{
CLIENT_CALL_RETURN _RetVal;

_RetVal = NdrClientCall2(
                  ( PMIDL_STUB_DESC  )&Object_StubDesc,
                  (PFORMAT_STRING) &Display_Util__MIDL_ProcFormatString.Format[6528],
                  ( unsigned char * )&This);
return ( HRESULT  )_RetVal.Simple;

}

/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_SetCollageStatus_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_COLLAGE_STATUS *pCollageStatus,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription)
{
CLIENT_CALL_RETURN _RetVal;

_RetVal = NdrClientCall2(
                  ( PMIDL_STUB_DESC  )&Object_StubDesc,
                  (PFORMAT_STRING) &Display_Util__MIDL_ProcFormatString.Format[6576],
                  ( unsigned char * )&This);
return ( HRESULT  )_RetVal.Simple;

}

/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_SetAudioTopology_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription)
{
CLIENT_CALL_RETURN _RetVal;

_RetVal = NdrClientCall2(
                  ( PMIDL_STUB_DESC  )&Object_StubDesc,
                  (PFORMAT_STRING) &Display_Util__MIDL_ProcFormatString.Format[6624],
                  ( unsigned char * )&This);
return ( HRESULT  )_RetVal.Simple;

}

/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_GetAudioTopology_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription)
{
CLIENT_CALL_RETURN _RetVal;

_RetVal = NdrClientCall2(
                  ( PMIDL_STUB_DESC  )&Object_StubDesc,
                  (PFORMAT_STRING) &Display_Util__MIDL_ProcFormatString.Format[6672],
                  ( unsigned char * )&This);
return ( HRESULT  )_RetVal.Simple;

}

/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_EnableAudioWTVideo_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription)
{
CLIENT_CALL_RETURN _RetVal;

_RetVal = NdrClientCall2(
                  ( PMIDL_STUB_DESC  )&Object_StubDesc,
                  (PFORMAT_STRING) &Display_Util__MIDL_ProcFormatString.Format[6720],
                  ( unsigned char * )&This);
return ( HRESULT  )_RetVal.Simple;

}

/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_DisableAudioWTVideo_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription)
{
CLIENT_CALL_RETURN _RetVal;

_RetVal = NdrClientCall2(
                  ( PMIDL_STUB_DESC  )&Object_StubDesc,
                  (PFORMAT_STRING) &Display_Util__MIDL_ProcFormatString.Format[6768],
                  ( unsigned char * )&This);
return ( HRESULT  )_RetVal.Simple;

}


extern const USER_MARSHAL_ROUTINE_QUADRUPLE UserMarshalRoutines[ WIRE_MARSHAL_TABLE_SIZE ];

#if !defined(__RPC_WIN32__)
#error  Invalid build platform for this stub.
#endif

#if !(TARGET_IS_NT50_OR_LATER)
#error You need Windows 2000 or later to run this stub because it uses these features:
#error   /robust command line switch.
#error However, your C/C++ compilation flags indicate you intend to run this app on earlier systems.
#error This app will fail with the RPC_X_WRONG_STUB_VERSION error.
#endif


static const Display_Util_MIDL_PROC_FORMAT_STRING Display_Util__MIDL_ProcFormatString =
    {
        0,
        {

	/* Procedure GetDeviceStatus */

			0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/*  2 */	NdrFcLong( 0x0 ),	/* 0 */
/*  6 */	NdrFcShort( 0x7 ),	/* 7 */
/*  8 */	NdrFcShort( 0x20 ),	/* x86 Stack size/offset = 32 */
/* 10 */	NdrFcShort( 0x24 ),	/* 36 */
/* 12 */	NdrFcShort( 0x5c ),	/* 92 */
/* 14 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x7,		/* 7 */
/* 16 */	0x8,		/* 8 */
			0x7,		/* Ext Flags:  new corr desc, clt corr check, srv corr check, */
/* 18 */	NdrFcShort( 0x1 ),	/* 1 */
/* 20 */	NdrFcShort( 0x1 ),	/* 1 */
/* 22 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter displayName */

/* 24 */	NdrFcShort( 0x8b ),	/* Flags:  must size, must free, in, by val, */
/* 26 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 28 */	NdrFcShort( 0x1c ),	/* Type Offset=28 */

	/* Parameter index */

/* 30 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 32 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 34 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pMonitorID */

/* 36 */	NdrFcShort( 0x2150 ),	/* Flags:  out, base type, simple ref, srv alloc size=8 */
/* 38 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 40 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pDevType */

/* 42 */	NdrFcShort( 0x158 ),	/* Flags:  in, out, base type, simple ref, */
/* 44 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 46 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pDevStatus */

/* 48 */	NdrFcShort( 0x2150 ),	/* Flags:  out, base type, simple ref, srv alloc size=8 */
/* 50 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 52 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pErrorDescription */

/* 54 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 56 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 58 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 60 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 62 */	NdrFcShort( 0x1c ),	/* x86 Stack size/offset = 28 */
/* 64 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure EnumActiveDisplay */

/* 66 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 68 */	NdrFcLong( 0x0 ),	/* 0 */
/* 72 */	NdrFcShort( 0x8 ),	/* 8 */
/* 74 */	NdrFcShort( 0x1c ),	/* x86 Stack size/offset = 28 */
/* 76 */	NdrFcShort( 0x8 ),	/* 8 */
/* 78 */	NdrFcShort( 0x40 ),	/* 64 */
/* 80 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x6,		/* 6 */
/* 82 */	0x8,		/* 8 */
			0x7,		/* Ext Flags:  new corr desc, clt corr check, srv corr check, */
/* 84 */	NdrFcShort( 0x1 ),	/* 1 */
/* 86 */	NdrFcShort( 0x1 ),	/* 1 */
/* 88 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter displayName */

/* 90 */	NdrFcShort( 0x8b ),	/* Flags:  must size, must free, in, by val, */
/* 92 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 94 */	NdrFcShort( 0x1c ),	/* Type Offset=28 */

	/* Parameter id */

/* 96 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 98 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 100 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pMonitorID */

/* 102 */	NdrFcShort( 0x2150 ),	/* Flags:  out, base type, simple ref, srv alloc size=8 */
/* 104 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 106 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pDevType */

/* 108 */	NdrFcShort( 0x2150 ),	/* Flags:  out, base type, simple ref, srv alloc size=8 */
/* 110 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 112 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pErrorDescription */

/* 114 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 116 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 118 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 120 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 122 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 124 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetMonitorID */

/* 126 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 128 */	NdrFcLong( 0x0 ),	/* 0 */
/* 132 */	NdrFcShort( 0x9 ),	/* 9 */
/* 134 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 136 */	NdrFcShort( 0x8 ),	/* 8 */
/* 138 */	NdrFcShort( 0x24 ),	/* 36 */
/* 140 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x5,		/* 5 */
/* 142 */	0x8,		/* 8 */
			0x7,		/* Ext Flags:  new corr desc, clt corr check, srv corr check, */
/* 144 */	NdrFcShort( 0x1 ),	/* 1 */
/* 146 */	NdrFcShort( 0x1 ),	/* 1 */
/* 148 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter deviceName */

/* 150 */	NdrFcShort( 0x8b ),	/* Flags:  must size, must free, in, by val, */
/* 152 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 154 */	NdrFcShort( 0x1c ),	/* Type Offset=28 */

	/* Parameter index */

/* 156 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 158 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 160 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pMonitorID */

/* 162 */	NdrFcShort( 0x2150 ),	/* Flags:  out, base type, simple ref, srv alloc size=8 */
/* 164 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 166 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pErrorDescription */

/* 168 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 170 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 172 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 174 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 176 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 178 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SingleDisplaySwitch */

/* 180 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 182 */	NdrFcLong( 0x0 ),	/* 0 */
/* 186 */	NdrFcShort( 0xa ),	/* 10 */
/* 188 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 190 */	NdrFcShort( 0x8 ),	/* 8 */
/* 192 */	NdrFcShort( 0x22 ),	/* 34 */
/* 194 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 196 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 198 */	NdrFcShort( 0x1 ),	/* 1 */
/* 200 */	NdrFcShort( 0x0 ),	/* 0 */
/* 202 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter monitorID */

/* 204 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 206 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 208 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 210 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 212 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 214 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 216 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 218 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 220 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 222 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 224 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 226 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure DualDisplayClone */

/* 228 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 230 */	NdrFcLong( 0x0 ),	/* 0 */
/* 234 */	NdrFcShort( 0xb ),	/* 11 */
/* 236 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 238 */	NdrFcShort( 0x10 ),	/* 16 */
/* 240 */	NdrFcShort( 0x22 ),	/* 34 */
/* 242 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x5,		/* 5 */
/* 244 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 246 */	NdrFcShort( 0x1 ),	/* 1 */
/* 248 */	NdrFcShort( 0x0 ),	/* 0 */
/* 250 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter primaryMonitorID */

/* 252 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 254 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 256 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter secondaryMonitorID */

/* 258 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 260 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 262 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 264 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 266 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 268 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 270 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 272 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 274 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 276 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 278 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 280 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure DualDisplayTwin */

/* 282 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 284 */	NdrFcLong( 0x0 ),	/* 0 */
/* 288 */	NdrFcShort( 0xc ),	/* 12 */
/* 290 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 292 */	NdrFcShort( 0x10 ),	/* 16 */
/* 294 */	NdrFcShort( 0x22 ),	/* 34 */
/* 296 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x5,		/* 5 */
/* 298 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 300 */	NdrFcShort( 0x1 ),	/* 1 */
/* 302 */	NdrFcShort( 0x0 ),	/* 0 */
/* 304 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter primaryMonitorID */

/* 306 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 308 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 310 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter secondaryMonitorID */

/* 312 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 314 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 316 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 318 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 320 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 322 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 324 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 326 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 328 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 330 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 332 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 334 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure ExtendedDesktop */

/* 336 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 338 */	NdrFcLong( 0x0 ),	/* 0 */
/* 342 */	NdrFcShort( 0xd ),	/* 13 */
/* 344 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 346 */	NdrFcShort( 0x10 ),	/* 16 */
/* 348 */	NdrFcShort( 0x22 ),	/* 34 */
/* 350 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x5,		/* 5 */
/* 352 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 354 */	NdrFcShort( 0x1 ),	/* 1 */
/* 356 */	NdrFcShort( 0x0 ),	/* 0 */
/* 358 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter primaryMonitorID */

/* 360 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 362 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 364 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter secondaryMonitorID */

/* 366 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 368 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 370 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 372 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 374 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 376 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 378 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 380 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 382 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 384 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 386 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 388 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure EnableRotation */

/* 390 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 392 */	NdrFcLong( 0x0 ),	/* 0 */
/* 396 */	NdrFcShort( 0xe ),	/* 14 */
/* 398 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 400 */	NdrFcShort( 0x10 ),	/* 16 */
/* 402 */	NdrFcShort( 0x22 ),	/* 34 */
/* 404 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x5,		/* 5 */
/* 406 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 408 */	NdrFcShort( 0x1 ),	/* 1 */
/* 410 */	NdrFcShort( 0x0 ),	/* 0 */
/* 412 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter monitorID */

/* 414 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 416 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 418 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter rotationAngle */

/* 420 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 422 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 424 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 426 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 428 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 430 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 432 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 434 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 436 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 438 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 440 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 442 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure DisableRotation */

/* 444 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 446 */	NdrFcLong( 0x0 ),	/* 0 */
/* 450 */	NdrFcShort( 0xf ),	/* 15 */
/* 452 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 454 */	NdrFcShort( 0x8 ),	/* 8 */
/* 456 */	NdrFcShort( 0x22 ),	/* 34 */
/* 458 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 460 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 462 */	NdrFcShort( 0x1 ),	/* 1 */
/* 464 */	NdrFcShort( 0x0 ),	/* 0 */
/* 466 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter monitorID */

/* 468 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 470 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 472 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 474 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 476 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 478 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 480 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 482 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 484 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 486 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 488 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 490 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure IsRotationEnabled */

/* 492 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 494 */	NdrFcLong( 0x0 ),	/* 0 */
/* 498 */	NdrFcShort( 0x10 ),	/* 16 */
/* 500 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 502 */	NdrFcShort( 0x8 ),	/* 8 */
/* 504 */	NdrFcShort( 0x3e ),	/* 62 */
/* 506 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x5,		/* 5 */
/* 508 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 510 */	NdrFcShort( 0x1 ),	/* 1 */
/* 512 */	NdrFcShort( 0x0 ),	/* 0 */
/* 514 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter monitorID */

/* 516 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 518 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 520 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pRotationFlag */

/* 522 */	NdrFcShort( 0x2150 ),	/* Flags:  out, base type, simple ref, srv alloc size=8 */
/* 524 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 526 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 528 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 530 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 532 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 534 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 536 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 538 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 540 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 542 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 544 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetRotationAngle */

/* 546 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 548 */	NdrFcLong( 0x0 ),	/* 0 */
/* 552 */	NdrFcShort( 0x11 ),	/* 17 */
/* 554 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 556 */	NdrFcShort( 0x8 ),	/* 8 */
/* 558 */	NdrFcShort( 0x3e ),	/* 62 */
/* 560 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x5,		/* 5 */
/* 562 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 564 */	NdrFcShort( 0x1 ),	/* 1 */
/* 566 */	NdrFcShort( 0x0 ),	/* 0 */
/* 568 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter monitorID */

/* 570 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 572 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 574 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pRotationAngle */

/* 576 */	NdrFcShort( 0x2150 ),	/* Flags:  out, base type, simple ref, srv alloc size=8 */
/* 578 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 580 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 582 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 584 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 586 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 588 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 590 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 592 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 594 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 596 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 598 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure Rotate */

/* 600 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 602 */	NdrFcLong( 0x0 ),	/* 0 */
/* 606 */	NdrFcShort( 0x12 ),	/* 18 */
/* 608 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 610 */	NdrFcShort( 0x10 ),	/* 16 */
/* 612 */	NdrFcShort( 0x22 ),	/* 34 */
/* 614 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x5,		/* 5 */
/* 616 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 618 */	NdrFcShort( 0x1 ),	/* 1 */
/* 620 */	NdrFcShort( 0x0 ),	/* 0 */
/* 622 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter monitorID */

/* 624 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 626 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 628 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter rotationAngle */

/* 630 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 632 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 634 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 636 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 638 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 640 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 642 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 644 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 646 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 648 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 650 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 652 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetFullScreen */

/* 654 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 656 */	NdrFcLong( 0x0 ),	/* 0 */
/* 660 */	NdrFcShort( 0x13 ),	/* 19 */
/* 662 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 664 */	NdrFcShort( 0x8 ),	/* 8 */
/* 666 */	NdrFcShort( 0x22 ),	/* 34 */
/* 668 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 670 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 672 */	NdrFcShort( 0x1 ),	/* 1 */
/* 674 */	NdrFcShort( 0x0 ),	/* 0 */
/* 676 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter monitorID */

/* 678 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 680 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 682 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 684 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 686 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 688 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 690 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 692 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 694 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 696 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 698 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 700 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetScreenCentered */

/* 702 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 704 */	NdrFcLong( 0x0 ),	/* 0 */
/* 708 */	NdrFcShort( 0x14 ),	/* 20 */
/* 710 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 712 */	NdrFcShort( 0x8 ),	/* 8 */
/* 714 */	NdrFcShort( 0x22 ),	/* 34 */
/* 716 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 718 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 720 */	NdrFcShort( 0x1 ),	/* 1 */
/* 722 */	NdrFcShort( 0x0 ),	/* 0 */
/* 724 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter monitorID */

/* 726 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 728 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 730 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 732 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 734 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 736 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 738 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 740 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 742 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 744 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 746 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 748 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure EnablePortraitPolicy */

/* 750 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 752 */	NdrFcLong( 0x0 ),	/* 0 */
/* 756 */	NdrFcShort( 0x15 ),	/* 21 */
/* 758 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 760 */	NdrFcShort( 0x10 ),	/* 16 */
/* 762 */	NdrFcShort( 0x22 ),	/* 34 */
/* 764 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x5,		/* 5 */
/* 766 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 768 */	NdrFcShort( 0x1 ),	/* 1 */
/* 770 */	NdrFcShort( 0x0 ),	/* 0 */
/* 772 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter monitorID */

/* 774 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 776 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 778 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter rotationAngle */

/* 780 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 782 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 784 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 786 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 788 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 790 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 792 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 794 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 796 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 798 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 800 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 802 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure DisablePortraitPolicy */

/* 804 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 806 */	NdrFcLong( 0x0 ),	/* 0 */
/* 810 */	NdrFcShort( 0x16 ),	/* 22 */
/* 812 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 814 */	NdrFcShort( 0x8 ),	/* 8 */
/* 816 */	NdrFcShort( 0x22 ),	/* 34 */
/* 818 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 820 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 822 */	NdrFcShort( 0x1 ),	/* 1 */
/* 824 */	NdrFcShort( 0x0 ),	/* 0 */
/* 826 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter monitorID */

/* 828 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 830 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 832 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 834 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 836 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 838 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 840 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 842 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 844 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 846 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 848 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 850 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure EnableLandscapePolicy */

/* 852 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 854 */	NdrFcLong( 0x0 ),	/* 0 */
/* 858 */	NdrFcShort( 0x17 ),	/* 23 */
/* 860 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 862 */	NdrFcShort( 0x10 ),	/* 16 */
/* 864 */	NdrFcShort( 0x22 ),	/* 34 */
/* 866 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x5,		/* 5 */
/* 868 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 870 */	NdrFcShort( 0x1 ),	/* 1 */
/* 872 */	NdrFcShort( 0x0 ),	/* 0 */
/* 874 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter monitorID */

/* 876 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 878 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 880 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter rotationAngle */

/* 882 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 884 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 886 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 888 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 890 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 892 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 894 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 896 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 898 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 900 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 902 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 904 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure DisableLandscapePolicy */

/* 906 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 908 */	NdrFcLong( 0x0 ),	/* 0 */
/* 912 */	NdrFcShort( 0x18 ),	/* 24 */
/* 914 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 916 */	NdrFcShort( 0x8 ),	/* 8 */
/* 918 */	NdrFcShort( 0x22 ),	/* 34 */
/* 920 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 922 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 924 */	NdrFcShort( 0x1 ),	/* 1 */
/* 926 */	NdrFcShort( 0x0 ),	/* 0 */
/* 928 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter monitorID */

/* 930 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 932 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 934 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 936 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 938 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 940 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 942 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 944 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 946 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 948 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 950 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 952 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetSupportedEvents */

/* 954 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 956 */	NdrFcLong( 0x0 ),	/* 0 */
/* 960 */	NdrFcShort( 0x19 ),	/* 25 */
/* 962 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 964 */	NdrFcShort( 0x24 ),	/* 36 */
/* 966 */	NdrFcShort( 0x8 ),	/* 8 */
/* 968 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 970 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 972 */	NdrFcShort( 0x1 ),	/* 1 */
/* 974 */	NdrFcShort( 0x0 ),	/* 0 */
/* 976 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter monitorID */

/* 978 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 980 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 982 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter r_ulSupEvents */

/* 984 */	NdrFcShort( 0x148 ),	/* Flags:  in, base type, simple ref, */
/* 986 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 988 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pErrorDescription */

/* 990 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 992 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 994 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 996 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 998 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 1000 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure RegisterEvent */

/* 1002 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 1004 */	NdrFcLong( 0x0 ),	/* 0 */
/* 1008 */	NdrFcShort( 0x1a ),	/* 26 */
/* 1010 */	NdrFcShort( 0x20 ),	/* x86 Stack size/offset = 32 */
/* 1012 */	NdrFcShort( 0x10 ),	/* 16 */
/* 1014 */	NdrFcShort( 0x3e ),	/* 62 */
/* 1016 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x7,		/* 7 */
/* 1018 */	0x8,		/* 8 */
			0x7,		/* Ext Flags:  new corr desc, clt corr check, srv corr check, */
/* 1020 */	NdrFcShort( 0x1 ),	/* 1 */
/* 1022 */	NdrFcShort( 0x1 ),	/* 1 */
/* 1024 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter eventName */

/* 1026 */	NdrFcShort( 0x8b ),	/* Flags:  must size, must free, in, by val, */
/* 1028 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 1030 */	NdrFcShort( 0x1c ),	/* Type Offset=28 */

	/* Parameter monitorID */

/* 1032 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 1034 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 1036 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter eventMask */

/* 1038 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 1040 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 1042 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pRegID */

/* 1044 */	NdrFcShort( 0x2150 ),	/* Flags:  out, base type, simple ref, srv alloc size=8 */
/* 1046 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 1048 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 1050 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 1052 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 1054 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 1056 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 1058 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 1060 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 1062 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 1064 */	NdrFcShort( 0x1c ),	/* x86 Stack size/offset = 28 */
/* 1066 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure UnRegisterEvent */

/* 1068 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 1070 */	NdrFcLong( 0x0 ),	/* 0 */
/* 1074 */	NdrFcShort( 0x1b ),	/* 27 */
/* 1076 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 1078 */	NdrFcShort( 0x8 ),	/* 8 */
/* 1080 */	NdrFcShort( 0x22 ),	/* 34 */
/* 1082 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 1084 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 1086 */	NdrFcShort( 0x1 ),	/* 1 */
/* 1088 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1090 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter regID */

/* 1092 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 1094 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 1096 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 1098 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 1100 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 1102 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 1104 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 1106 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 1108 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 1110 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 1112 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 1114 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetAspectScalingCapabilities */

/* 1116 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 1118 */	NdrFcLong( 0x0 ),	/* 0 */
/* 1122 */	NdrFcShort( 0x1c ),	/* 28 */
/* 1124 */	NdrFcShort( 0x20 ),	/* x86 Stack size/offset = 32 */
/* 1126 */	NdrFcShort( 0x10 ),	/* 16 */
/* 1128 */	NdrFcShort( 0x5a ),	/* 90 */
/* 1130 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x7,		/* 7 */
/* 1132 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 1134 */	NdrFcShort( 0x1 ),	/* 1 */
/* 1136 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1138 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter monitorID */

/* 1140 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 1142 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 1144 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter dwOperatingMode */

/* 1146 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 1148 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 1150 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pAspectScalingCaps */

/* 1152 */	NdrFcShort( 0x2150 ),	/* Flags:  out, base type, simple ref, srv alloc size=8 */
/* 1154 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 1156 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pCurrentAspectScalingPreference */

/* 1158 */	NdrFcShort( 0x2150 ),	/* Flags:  out, base type, simple ref, srv alloc size=8 */
/* 1160 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 1162 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 1164 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 1166 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 1168 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 1170 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 1172 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 1174 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 1176 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 1178 */	NdrFcShort( 0x1c ),	/* x86 Stack size/offset = 28 */
/* 1180 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetAspectPreference */

/* 1182 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 1184 */	NdrFcLong( 0x0 ),	/* 0 */
/* 1188 */	NdrFcShort( 0x1d ),	/* 29 */
/* 1190 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 1192 */	NdrFcShort( 0x10 ),	/* 16 */
/* 1194 */	NdrFcShort( 0x22 ),	/* 34 */
/* 1196 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x5,		/* 5 */
/* 1198 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 1200 */	NdrFcShort( 0x1 ),	/* 1 */
/* 1202 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1204 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter monitorID */

/* 1206 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 1208 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 1210 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter aspectScalingCaps */

/* 1212 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 1214 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 1216 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 1218 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 1220 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 1222 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 1224 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 1226 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 1228 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 1230 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 1232 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 1234 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetGammaRamp */

/* 1236 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 1238 */	NdrFcLong( 0x0 ),	/* 0 */
/* 1242 */	NdrFcShort( 0x1e ),	/* 30 */
/* 1244 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 1246 */	NdrFcShort( 0x65c ),	/* 1628 */
/* 1248 */	NdrFcShort( 0x22 ),	/* 34 */
/* 1250 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x5,		/* 5 */
/* 1252 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 1254 */	NdrFcShort( 0x1 ),	/* 1 */
/* 1256 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1258 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter monitorID */

/* 1260 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 1262 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 1264 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pGammaramp */

/* 1266 */	NdrFcShort( 0x10a ),	/* Flags:  must free, in, simple ref, */
/* 1268 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 1270 */	NdrFcShort( 0x4e ),	/* Type Offset=78 */

	/* Parameter pExtraErrorCode */

/* 1272 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 1274 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 1276 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 1278 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 1280 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 1282 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 1284 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 1286 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 1288 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetGammaRamp */

/* 1290 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 1292 */	NdrFcLong( 0x0 ),	/* 0 */
/* 1296 */	NdrFcShort( 0x1f ),	/* 31 */
/* 1298 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 1300 */	NdrFcShort( 0x8 ),	/* 8 */
/* 1302 */	NdrFcShort( 0x676 ),	/* 1654 */
/* 1304 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x5,		/* 5 */
/* 1306 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 1308 */	NdrFcShort( 0x1 ),	/* 1 */
/* 1310 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1312 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter uidMonitor */

/* 1314 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 1316 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 1318 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pGammaramp */

/* 1320 */	NdrFcShort( 0x112 ),	/* Flags:  must free, out, simple ref, */
/* 1322 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 1324 */	NdrFcShort( 0x4e ),	/* Type Offset=78 */

	/* Parameter pExtraErrorCode */

/* 1326 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 1328 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 1330 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 1332 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 1334 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 1336 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 1338 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 1340 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 1342 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure PopulateSetValidGamma */

/* 1344 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 1346 */	NdrFcLong( 0x0 ),	/* 0 */
/* 1350 */	NdrFcShort( 0x20 ),	/* 32 */
/* 1352 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 1354 */	NdrFcShort( 0x10 ),	/* 16 */
/* 1356 */	NdrFcShort( 0x22 ),	/* 34 */
/* 1358 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x5,		/* 5 */
/* 1360 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 1362 */	NdrFcShort( 0x1 ),	/* 1 */
/* 1364 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1366 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter monitorID */

/* 1368 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 1370 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 1372 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter gam */

/* 1374 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 1376 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 1378 */	0xa,		/* FC_FLOAT */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 1380 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 1382 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 1384 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 1386 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 1388 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 1390 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 1392 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 1394 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 1396 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure PopulateSetInvalidGamma */

/* 1398 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 1400 */	NdrFcLong( 0x0 ),	/* 0 */
/* 1404 */	NdrFcShort( 0x21 ),	/* 33 */
/* 1406 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 1408 */	NdrFcShort( 0x10 ),	/* 16 */
/* 1410 */	NdrFcShort( 0x22 ),	/* 34 */
/* 1412 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x5,		/* 5 */
/* 1414 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 1416 */	NdrFcShort( 0x1 ),	/* 1 */
/* 1418 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1420 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter monitorID */

/* 1422 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 1424 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 1426 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter rule */

/* 1428 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 1430 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 1432 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 1434 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 1436 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 1438 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 1440 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 1442 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 1444 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 1446 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 1448 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 1450 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetCloneRefreshRate */

/* 1452 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 1454 */	NdrFcLong( 0x0 ),	/* 0 */
/* 1458 */	NdrFcShort( 0x22 ),	/* 34 */
/* 1460 */	NdrFcShort( 0x1c ),	/* x86 Stack size/offset = 28 */
/* 1462 */	NdrFcShort( 0x38 ),	/* 56 */
/* 1464 */	NdrFcShort( 0x342 ),	/* 834 */
/* 1466 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x6,		/* 6 */
/* 1468 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 1470 */	NdrFcShort( 0x1 ),	/* 1 */
/* 1472 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1474 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pDispCfg */

/* 1476 */	NdrFcShort( 0x10a ),	/* Flags:  must free, in, simple ref, */
/* 1478 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 1480 */	NdrFcShort( 0x64 ),	/* Type Offset=100 */

	/* Parameter pPrimaryRR */

/* 1482 */	NdrFcShort( 0x12 ),	/* Flags:  must free, out, */
/* 1484 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 1486 */	NdrFcShort( 0x76 ),	/* Type Offset=118 */

	/* Parameter pSecondaryRR */

/* 1488 */	NdrFcShort( 0x12 ),	/* Flags:  must free, out, */
/* 1490 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 1492 */	NdrFcShort( 0x76 ),	/* Type Offset=118 */

	/* Parameter pExtraErrorCode */

/* 1494 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 1496 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 1498 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 1500 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 1502 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 1504 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 1506 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 1508 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 1510 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetCloneView */

/* 1512 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 1514 */	NdrFcLong( 0x0 ),	/* 0 */
/* 1518 */	NdrFcShort( 0x23 ),	/* 35 */
/* 1520 */	NdrFcShort( 0x1c ),	/* x86 Stack size/offset = 28 */
/* 1522 */	NdrFcShort( 0x88 ),	/* 136 */
/* 1524 */	NdrFcShort( 0x22 ),	/* 34 */
/* 1526 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x6,		/* 6 */
/* 1528 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 1530 */	NdrFcShort( 0x1 ),	/* 1 */
/* 1532 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1534 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pDispCfg */

/* 1536 */	NdrFcShort( 0x10a ),	/* Flags:  must free, in, simple ref, */
/* 1538 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 1540 */	NdrFcShort( 0x64 ),	/* Type Offset=100 */

	/* Parameter pPrimaryRR */

/* 1542 */	NdrFcShort( 0x10a ),	/* Flags:  must free, in, simple ref, */
/* 1544 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 1546 */	NdrFcShort( 0x6e ),	/* Type Offset=110 */

	/* Parameter pSecondaryRR */

/* 1548 */	NdrFcShort( 0x10a ),	/* Flags:  must free, in, simple ref, */
/* 1550 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 1552 */	NdrFcShort( 0x6e ),	/* Type Offset=110 */

	/* Parameter pExtraErrorCode */

/* 1554 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 1556 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 1558 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 1560 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 1562 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 1564 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 1566 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 1568 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 1570 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetDVMTData */

/* 1572 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 1574 */	NdrFcLong( 0x0 ),	/* 0 */
/* 1578 */	NdrFcShort( 0x24 ),	/* 36 */
/* 1580 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 1582 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1584 */	NdrFcShort( 0x56 ),	/* 86 */
/* 1586 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 1588 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 1590 */	NdrFcShort( 0x1 ),	/* 1 */
/* 1592 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1594 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBuffer */

/* 1596 */	NdrFcShort( 0x4112 ),	/* Flags:  must free, out, simple ref, srv alloc size=16 */
/* 1598 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 1600 */	NdrFcShort( 0x88 ),	/* Type Offset=136 */

	/* Parameter pExtraErrorCode */

/* 1602 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 1604 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 1606 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 1608 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 1610 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 1612 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 1614 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 1616 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 1618 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetEDIDData */

/* 1620 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 1622 */	NdrFcLong( 0x0 ),	/* 0 */
/* 1626 */	NdrFcShort( 0x25 ),	/* 37 */
/* 1628 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 1630 */	NdrFcShort( 0x140 ),	/* 320 */
/* 1632 */	NdrFcShort( 0x162 ),	/* 354 */
/* 1634 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 1636 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 1638 */	NdrFcShort( 0x1 ),	/* 1 */
/* 1640 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1642 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBuffer */

/* 1644 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 1646 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 1648 */	NdrFcShort( 0x9c ),	/* Type Offset=156 */

	/* Parameter pExtraErrorCode */

/* 1650 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 1652 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 1654 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 1656 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 1658 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 1660 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 1662 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 1664 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 1666 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure IsOverlayOn */

/* 1668 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 1670 */	NdrFcLong( 0x0 ),	/* 0 */
/* 1674 */	NdrFcShort( 0x26 ),	/* 38 */
/* 1676 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 1678 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1680 */	NdrFcShort( 0x4a ),	/* 74 */
/* 1682 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 1684 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 1686 */	NdrFcShort( 0x1 ),	/* 1 */
/* 1688 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1690 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBuffer */

/* 1692 */	NdrFcShort( 0x2112 ),	/* Flags:  must free, out, simple ref, srv alloc size=8 */
/* 1694 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 1696 */	NdrFcShort( 0xac ),	/* Type Offset=172 */

	/* Parameter pExtraErrorCode */

/* 1698 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 1700 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 1702 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 1704 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 1706 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 1708 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 1710 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 1712 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 1714 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetOverScanData */

/* 1716 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 1718 */	NdrFcLong( 0x0 ),	/* 0 */
/* 1722 */	NdrFcShort( 0x27 ),	/* 39 */
/* 1724 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 1726 */	NdrFcShort( 0xc4 ),	/* 196 */
/* 1728 */	NdrFcShort( 0xe6 ),	/* 230 */
/* 1730 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 1732 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 1734 */	NdrFcShort( 0x1 ),	/* 1 */
/* 1736 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1738 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pData */

/* 1740 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 1742 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 1744 */	NdrFcShort( 0xb6 ),	/* Type Offset=182 */

	/* Parameter pExtraErrorCode */

/* 1746 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 1748 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 1750 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 1752 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 1754 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 1756 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 1758 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 1760 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 1762 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetOverScanData */

/* 1764 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 1766 */	NdrFcLong( 0x0 ),	/* 0 */
/* 1770 */	NdrFcShort( 0x28 ),	/* 40 */
/* 1772 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 1774 */	NdrFcShort( 0xc4 ),	/* 196 */
/* 1776 */	NdrFcShort( 0x22 ),	/* 34 */
/* 1778 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 1780 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 1782 */	NdrFcShort( 0x1 ),	/* 1 */
/* 1784 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1786 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pData */

/* 1788 */	NdrFcShort( 0x10a ),	/* Flags:  must free, in, simple ref, */
/* 1790 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 1792 */	NdrFcShort( 0xb6 ),	/* Type Offset=182 */

	/* Parameter pExtraErrorCode */

/* 1794 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 1796 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 1798 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 1800 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 1802 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 1804 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 1806 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 1808 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 1810 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure IsDownScalingSupported */

/* 1812 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 1814 */	NdrFcLong( 0x0 ),	/* 0 */
/* 1818 */	NdrFcShort( 0x29 ),	/* 41 */
/* 1820 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 1822 */	NdrFcShort( 0x88 ),	/* 136 */
/* 1824 */	NdrFcShort( 0x22 ),	/* 34 */
/* 1826 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 1828 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 1830 */	NdrFcShort( 0x1 ),	/* 1 */
/* 1832 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1834 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBuffer */

/* 1836 */	NdrFcShort( 0x10a ),	/* Flags:  must free, in, simple ref, */
/* 1838 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 1840 */	NdrFcShort( 0xd6 ),	/* Type Offset=214 */

	/* Parameter pExtraErrorCode */

/* 1842 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 1844 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 1846 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 1848 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 1850 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 1852 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 1854 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 1856 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 1858 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure IsDownScalingEnabled */

/* 1860 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 1862 */	NdrFcLong( 0x0 ),	/* 0 */
/* 1866 */	NdrFcShort( 0x2a ),	/* 42 */
/* 1868 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 1870 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1872 */	NdrFcShort( 0x3e ),	/* 62 */
/* 1874 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 1876 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 1878 */	NdrFcShort( 0x1 ),	/* 1 */
/* 1880 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1882 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pbIsEnabled */

/* 1884 */	NdrFcShort( 0x2150 ),	/* Flags:  out, base type, simple ref, srv alloc size=8 */
/* 1886 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 1888 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 1890 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 1892 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 1894 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 1896 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 1898 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 1900 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 1902 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 1904 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 1906 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure EnableDownScaling */

/* 1908 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 1910 */	NdrFcLong( 0x0 ),	/* 0 */
/* 1914 */	NdrFcShort( 0x2b ),	/* 43 */
/* 1916 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 1918 */	NdrFcShort( 0x88 ),	/* 136 */
/* 1920 */	NdrFcShort( 0xaa ),	/* 170 */
/* 1922 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 1924 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 1926 */	NdrFcShort( 0x1 ),	/* 1 */
/* 1928 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1930 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBuffer */

/* 1932 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 1934 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 1936 */	NdrFcShort( 0xd6 ),	/* Type Offset=214 */

	/* Parameter pExtraErrorCode */

/* 1938 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 1940 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 1942 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 1944 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 1946 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 1948 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 1950 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 1952 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 1954 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure DisableDownScaling */

/* 1956 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 1958 */	NdrFcLong( 0x0 ),	/* 0 */
/* 1962 */	NdrFcShort( 0x2c ),	/* 44 */
/* 1964 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 1966 */	NdrFcShort( 0x88 ),	/* 136 */
/* 1968 */	NdrFcShort( 0xaa ),	/* 170 */
/* 1970 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 1972 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 1974 */	NdrFcShort( 0x1 ),	/* 1 */
/* 1976 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1978 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBuffer */

/* 1980 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 1982 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 1984 */	NdrFcShort( 0xd6 ),	/* Type Offset=214 */

	/* Parameter pExtraErrorCode */

/* 1986 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 1988 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 1990 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 1992 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 1994 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 1996 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 1998 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 2000 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 2002 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetConfiguration */

/* 2004 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 2006 */	NdrFcLong( 0x0 ),	/* 0 */
/* 2010 */	NdrFcShort( 0x2d ),	/* 45 */
/* 2012 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 2014 */	NdrFcShort( 0x78 ),	/* 120 */
/* 2016 */	NdrFcShort( 0x9a ),	/* 154 */
/* 2018 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 2020 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 2022 */	NdrFcShort( 0x1 ),	/* 1 */
/* 2024 */	NdrFcShort( 0x0 ),	/* 0 */
/* 2026 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBuffer */

/* 2028 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 2030 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 2032 */	NdrFcShort( 0xf4 ),	/* Type Offset=244 */

	/* Parameter pExtraErrorCode */

/* 2034 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 2036 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 2038 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 2040 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 2042 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 2044 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 2046 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 2048 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 2050 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetConfiguration */

/* 2052 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 2054 */	NdrFcLong( 0x0 ),	/* 0 */
/* 2058 */	NdrFcShort( 0x2e ),	/* 46 */
/* 2060 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 2062 */	NdrFcShort( 0x78 ),	/* 120 */
/* 2064 */	NdrFcShort( 0x22 ),	/* 34 */
/* 2066 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 2068 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 2070 */	NdrFcShort( 0x1 ),	/* 1 */
/* 2072 */	NdrFcShort( 0x0 ),	/* 0 */
/* 2074 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBuffer */

/* 2076 */	NdrFcShort( 0x10a ),	/* Flags:  must free, in, simple ref, */
/* 2078 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 2080 */	NdrFcShort( 0xf4 ),	/* Type Offset=244 */

	/* Parameter pExtraErrorCode */

/* 2082 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 2084 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 2086 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 2088 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 2090 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 2092 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 2094 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 2096 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 2098 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure Overlay_Set */

/* 2100 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 2102 */	NdrFcLong( 0x0 ),	/* 0 */
/* 2106 */	NdrFcShort( 0x2f ),	/* 47 */
/* 2108 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 2110 */	NdrFcShort( 0xdc ),	/* 220 */
/* 2112 */	NdrFcShort( 0xfe ),	/* 254 */
/* 2114 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 2116 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 2118 */	NdrFcShort( 0x1 ),	/* 1 */
/* 2120 */	NdrFcShort( 0x0 ),	/* 0 */
/* 2122 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBuffer */

/* 2124 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 2126 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 2128 */	NdrFcShort( 0x110 ),	/* Type Offset=272 */

	/* Parameter pExtraErrorCode */

/* 2130 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 2132 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 2134 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 2136 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 2138 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 2140 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 2142 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 2144 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 2146 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure Overlay_Get */

/* 2148 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 2150 */	NdrFcLong( 0x0 ),	/* 0 */
/* 2154 */	NdrFcShort( 0x30 ),	/* 48 */
/* 2156 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 2158 */	NdrFcShort( 0xdc ),	/* 220 */
/* 2160 */	NdrFcShort( 0xfe ),	/* 254 */
/* 2162 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 2164 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 2166 */	NdrFcShort( 0x1 ),	/* 1 */
/* 2168 */	NdrFcShort( 0x0 ),	/* 0 */
/* 2170 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBuffer */

/* 2172 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 2174 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 2176 */	NdrFcShort( 0x110 ),	/* Type Offset=272 */

	/* Parameter pExtraErrorCode */

/* 2178 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 2180 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 2182 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 2184 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 2186 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 2188 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 2190 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 2192 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 2194 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure CVT_Get */

/* 2196 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 2198 */	NdrFcLong( 0x0 ),	/* 0 */
/* 2202 */	NdrFcShort( 0x31 ),	/* 49 */
/* 2204 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 2206 */	NdrFcShort( 0x2c ),	/* 44 */
/* 2208 */	NdrFcShort( 0x4e ),	/* 78 */
/* 2210 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 2212 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 2214 */	NdrFcShort( 0x1 ),	/* 1 */
/* 2216 */	NdrFcShort( 0x0 ),	/* 0 */
/* 2218 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBuffer */

/* 2220 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 2222 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 2224 */	NdrFcShort( 0xec ),	/* Type Offset=236 */

	/* Parameter pExtraErrorCode */

/* 2226 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 2228 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 2230 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 2232 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 2234 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 2236 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 2238 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 2240 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 2242 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SDVO_Set */

/* 2244 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 2246 */	NdrFcLong( 0x0 ),	/* 0 */
/* 2250 */	NdrFcShort( 0x32 ),	/* 50 */
/* 2252 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 2254 */	NdrFcShort( 0x0 ),	/* 0 */
/* 2256 */	NdrFcShort( 0x22 ),	/* 34 */
/* 2258 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x4,		/* 4 */
/* 2260 */	0x8,		/* 8 */
			0x7,		/* Ext Flags:  new corr desc, clt corr check, srv corr check, */
/* 2262 */	NdrFcShort( 0x1 ),	/* 1 */
/* 2264 */	NdrFcShort( 0x1 ),	/* 1 */
/* 2266 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBuffer */

/* 2268 */	NdrFcShort( 0x11b ),	/* Flags:  must size, must free, in, out, simple ref, */
/* 2270 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 2272 */	NdrFcShort( 0x154 ),	/* Type Offset=340 */

	/* Parameter pExtraErrorCode */

/* 2274 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 2276 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 2278 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 2280 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 2282 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 2284 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 2286 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 2288 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 2290 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetSupportedConfiguration */

/* 2292 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 2294 */	NdrFcLong( 0x0 ),	/* 0 */
/* 2298 */	NdrFcShort( 0x33 ),	/* 51 */
/* 2300 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 2302 */	NdrFcShort( 0xf80 ),	/* 3968 */
/* 2304 */	NdrFcShort( 0xfa2 ),	/* 4002 */
/* 2306 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 2308 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 2310 */	NdrFcShort( 0x1 ),	/* 1 */
/* 2312 */	NdrFcShort( 0x0 ),	/* 0 */
/* 2314 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBuffer */

/* 2316 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 2318 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 2320 */	NdrFcShort( 0x18a ),	/* Type Offset=394 */

	/* Parameter pExtraErrorCode */

/* 2322 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 2324 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 2326 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 2328 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 2330 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 2332 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 2334 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 2336 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 2338 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetGraphicsModes */

/* 2340 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 2342 */	NdrFcLong( 0x0 ),	/* 0 */
/* 2346 */	NdrFcShort( 0x34 ),	/* 52 */
/* 2348 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 2350 */	NdrFcShort( 0x9640 ),	/* -27072 */
/* 2352 */	NdrFcShort( 0x9662 ),	/* -27038 */
/* 2354 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 2356 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 2358 */	NdrFcShort( 0x1 ),	/* 1 */
/* 2360 */	NdrFcShort( 0x0 ),	/* 0 */
/* 2362 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBuffer */

/* 2364 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 2366 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 2368 */	NdrFcShort( 0x1a4 ),	/* Type Offset=420 */

	/* Parameter pExtraErrorCode */

/* 2370 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 2372 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 2374 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 2376 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 2378 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 2380 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 2382 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 2384 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 2386 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetSupportedGraphicsModes */

/* 2388 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 2390 */	NdrFcLong( 0x0 ),	/* 0 */
/* 2394 */	NdrFcShort( 0x35 ),	/* 53 */
/* 2396 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 2398 */	NdrFcShort( 0x9640 ),	/* -27072 */
/* 2400 */	NdrFcShort( 0x9662 ),	/* -27038 */
/* 2402 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 2404 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 2406 */	NdrFcShort( 0x1 ),	/* 1 */
/* 2408 */	NdrFcShort( 0x0 ),	/* 0 */
/* 2410 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBuffer */

/* 2412 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 2414 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 2416 */	NdrFcShort( 0x1a4 ),	/* Type Offset=420 */

	/* Parameter pExtraErrorCode */

/* 2418 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 2420 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 2422 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 2424 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 2426 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 2428 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 2430 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 2432 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 2434 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetVBIOSVersion */

/* 2436 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 2438 */	NdrFcLong( 0x0 ),	/* 0 */
/* 2442 */	NdrFcShort( 0x36 ),	/* 54 */
/* 2444 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 2446 */	NdrFcShort( 0x0 ),	/* 0 */
/* 2448 */	NdrFcShort( 0x22 ),	/* 34 */
/* 2450 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x4,		/* 4 */
/* 2452 */	0x8,		/* 8 */
			0x7,		/* Ext Flags:  new corr desc, clt corr check, srv corr check, */
/* 2454 */	NdrFcShort( 0x1 ),	/* 1 */
/* 2456 */	NdrFcShort( 0x1 ),	/* 1 */
/* 2458 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBuffer */

/* 2460 */	NdrFcShort( 0x11b ),	/* Flags:  must size, must free, in, out, simple ref, */
/* 2462 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 2464 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Parameter pExtraErrorCode */

/* 2466 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 2468 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 2470 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 2472 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 2474 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 2476 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 2478 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 2480 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 2482 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetGammaBrightnessContrast */

/* 2484 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 2486 */	NdrFcLong( 0x0 ),	/* 0 */
/* 2490 */	NdrFcShort( 0x37 ),	/* 55 */
/* 2492 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 2494 */	NdrFcShort( 0x60 ),	/* 96 */
/* 2496 */	NdrFcShort( 0x82 ),	/* 130 */
/* 2498 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 2500 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 2502 */	NdrFcShort( 0x1 ),	/* 1 */
/* 2504 */	NdrFcShort( 0x0 ),	/* 0 */
/* 2506 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBuffer */

/* 2508 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 2510 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 2512 */	NdrFcShort( 0x1c4 ),	/* Type Offset=452 */

	/* Parameter pExtraErrorCode */

/* 2514 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 2516 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 2518 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 2520 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 2522 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 2524 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 2526 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 2528 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 2530 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetGammaBrightnessContrast */

/* 2532 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 2534 */	NdrFcLong( 0x0 ),	/* 0 */
/* 2538 */	NdrFcShort( 0x38 ),	/* 56 */
/* 2540 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 2542 */	NdrFcShort( 0x60 ),	/* 96 */
/* 2544 */	NdrFcShort( 0x82 ),	/* 130 */
/* 2546 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 2548 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 2550 */	NdrFcShort( 0x1 ),	/* 1 */
/* 2552 */	NdrFcShort( 0x0 ),	/* 0 */
/* 2554 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBuffer */

/* 2556 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 2558 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 2560 */	NdrFcShort( 0x1c4 ),	/* Type Offset=452 */

	/* Parameter pExtraErrorCode */

/* 2562 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 2564 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 2566 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 2568 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 2570 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 2572 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 2574 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 2576 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 2578 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetSystemConfigurationAll */

/* 2580 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 2582 */	NdrFcLong( 0x0 ),	/* 0 */
/* 2586 */	NdrFcShort( 0x39 ),	/* 57 */
/* 2588 */	NdrFcShort( 0x20 ),	/* x86 Stack size/offset = 32 */
/* 2590 */	NdrFcShort( 0x18 ),	/* 24 */
/* 2592 */	NdrFcShort( 0x22 ),	/* 34 */
/* 2594 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x7,		/* 7 */
/* 2596 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 2598 */	NdrFcShort( 0x1 ),	/* 1 */
/* 2600 */	NdrFcShort( 0x0 ),	/* 0 */
/* 2602 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pSysConfigData */

/* 2604 */	NdrFcShort( 0x11b ),	/* Flags:  must size, must free, in, out, simple ref, */
/* 2606 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 2608 */	NdrFcShort( 0x1fc ),	/* Type Offset=508 */

	/* Parameter pExtraErrorCode */

/* 2610 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 2612 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 2614 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter opmode */

/* 2616 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 2618 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 2620 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter PriRotAngle */

/* 2622 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 2624 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 2626 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter SecRotAngle */

/* 2628 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 2630 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 2632 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pErrorDescription */

/* 2634 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 2636 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 2638 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 2640 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 2642 */	NdrFcShort( 0x1c ),	/* x86 Stack size/offset = 28 */
/* 2644 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetSystemConfiguration */

/* 2646 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 2648 */	NdrFcLong( 0x0 ),	/* 0 */
/* 2652 */	NdrFcShort( 0x3a ),	/* 58 */
/* 2654 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 2656 */	NdrFcShort( 0x0 ),	/* 0 */
/* 2658 */	NdrFcShort( 0x22 ),	/* 34 */
/* 2660 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x4,		/* 4 */
/* 2662 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 2664 */	NdrFcShort( 0x1 ),	/* 1 */
/* 2666 */	NdrFcShort( 0x0 ),	/* 0 */
/* 2668 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pSysConfigData */

/* 2670 */	NdrFcShort( 0x11b ),	/* Flags:  must size, must free, in, out, simple ref, */
/* 2672 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 2674 */	NdrFcShort( 0x1fc ),	/* Type Offset=508 */

	/* Parameter pExtraErrorCode */

/* 2676 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 2678 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 2680 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 2682 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 2684 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 2686 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 2688 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 2690 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 2692 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetSystemConfiguration */

/* 2694 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 2696 */	NdrFcLong( 0x0 ),	/* 0 */
/* 2700 */	NdrFcShort( 0x3b ),	/* 59 */
/* 2702 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 2704 */	NdrFcShort( 0x0 ),	/* 0 */
/* 2706 */	NdrFcShort( 0x22 ),	/* 34 */
/* 2708 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x4,		/* 4 */
/* 2710 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 2712 */	NdrFcShort( 0x1 ),	/* 1 */
/* 2714 */	NdrFcShort( 0x0 ),	/* 0 */
/* 2716 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBuffer */

/* 2718 */	NdrFcShort( 0x11b ),	/* Flags:  must size, must free, in, out, simple ref, */
/* 2720 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 2722 */	NdrFcShort( 0x1fc ),	/* Type Offset=508 */

	/* Parameter pExtraErrorCode */

/* 2724 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 2726 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 2728 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 2730 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 2732 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 2734 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 2736 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 2738 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 2740 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetMediaScalar */

/* 2742 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 2744 */	NdrFcLong( 0x0 ),	/* 0 */
/* 2748 */	NdrFcShort( 0x3c ),	/* 60 */
/* 2750 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 2752 */	NdrFcShort( 0x70 ),	/* 112 */
/* 2754 */	NdrFcShort( 0x92 ),	/* 146 */
/* 2756 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 2758 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 2760 */	NdrFcShort( 0x1 ),	/* 1 */
/* 2762 */	NdrFcShort( 0x0 ),	/* 0 */
/* 2764 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pMediaScalarData */

/* 2766 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 2768 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 2770 */	NdrFcShort( 0x212 ),	/* Type Offset=530 */

	/* Parameter pExtraErrorCode */

/* 2772 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 2774 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 2776 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 2778 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 2780 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 2782 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 2784 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 2786 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 2788 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetMediaScalar */

/* 2790 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 2792 */	NdrFcLong( 0x0 ),	/* 0 */
/* 2796 */	NdrFcShort( 0x3d ),	/* 61 */
/* 2798 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 2800 */	NdrFcShort( 0x70 ),	/* 112 */
/* 2802 */	NdrFcShort( 0x92 ),	/* 146 */
/* 2804 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 2806 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 2808 */	NdrFcShort( 0x1 ),	/* 1 */
/* 2810 */	NdrFcShort( 0x0 ),	/* 0 */
/* 2812 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pMediaScalarData */

/* 2814 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 2816 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 2818 */	NdrFcShort( 0x212 ),	/* Type Offset=530 */

	/* Parameter pExtraErrorCode */

/* 2820 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 2822 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 2824 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 2826 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 2828 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 2830 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 2832 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 2834 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 2836 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure InitilizeRemoveCustomModeArray */

/* 2838 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 2840 */	NdrFcLong( 0x0 ),	/* 0 */
/* 2844 */	NdrFcShort( 0x3e ),	/* 62 */
/* 2846 */	NdrFcShort( 0x28 ),	/* x86 Stack size/offset = 40 */
/* 2848 */	NdrFcShort( 0x38 ),	/* 56 */
/* 2850 */	NdrFcShort( 0x8 ),	/* 8 */
/* 2852 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x9,		/* 9 */
/* 2854 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 2856 */	NdrFcShort( 0x1 ),	/* 1 */
/* 2858 */	NdrFcShort( 0x0 ),	/* 0 */
/* 2860 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter monitorId */

/* 2862 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 2864 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 2866 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter i */

/* 2868 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 2870 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 2872 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter HzR */

/* 2874 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 2876 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 2878 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter VtR */

/* 2880 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 2882 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 2884 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter RR */

/* 2886 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 2888 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 2890 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter BPP */

/* 2892 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 2894 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 2896 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter Imode */

/* 2898 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 2900 */	NdrFcShort( 0x1c ),	/* x86 Stack size/offset = 28 */
/* 2902 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pErrorDescription */

/* 2904 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 2906 */	NdrFcShort( 0x20 ),	/* x86 Stack size/offset = 32 */
/* 2908 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 2910 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 2912 */	NdrFcShort( 0x24 ),	/* x86 Stack size/offset = 36 */
/* 2914 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure RemoveCustomMode */

/* 2916 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 2918 */	NdrFcLong( 0x0 ),	/* 0 */
/* 2922 */	NdrFcShort( 0x3f ),	/* 63 */
/* 2924 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 2926 */	NdrFcShort( 0xa8f0 ),	/* -22288 */
/* 2928 */	NdrFcShort( 0xa912 ),	/* -22254 */
/* 2930 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 2932 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 2934 */	NdrFcShort( 0x1 ),	/* 1 */
/* 2936 */	NdrFcShort( 0x0 ),	/* 0 */
/* 2938 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter rcm */

/* 2940 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 2942 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 2944 */	NdrFcShort( 0x230 ),	/* Type Offset=560 */

	/* Parameter pExtraErrorCode */

/* 2946 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 2948 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 2950 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 2952 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 2954 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 2956 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 2958 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 2960 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 2962 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure AddAdvancedCustomMode */

/* 2964 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 2966 */	NdrFcLong( 0x0 ),	/* 0 */
/* 2970 */	NdrFcShort( 0x40 ),	/* 64 */
/* 2972 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 2974 */	NdrFcShort( 0x7c ),	/* 124 */
/* 2976 */	NdrFcShort( 0x9e ),	/* 158 */
/* 2978 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 2980 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 2982 */	NdrFcShort( 0x1 ),	/* 1 */
/* 2984 */	NdrFcShort( 0x0 ),	/* 0 */
/* 2986 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pacmd */

/* 2988 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 2990 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 2992 */	NdrFcShort( 0x254 ),	/* Type Offset=596 */

	/* Parameter pExtraErrorCode */

/* 2994 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 2996 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 2998 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 3000 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 3002 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 3004 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 3006 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 3008 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 3010 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure AddBasicCustomMode */

/* 3012 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 3014 */	NdrFcLong( 0x0 ),	/* 0 */
/* 3018 */	NdrFcShort( 0x41 ),	/* 65 */
/* 3020 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 3022 */	NdrFcShort( 0x5c ),	/* 92 */
/* 3024 */	NdrFcShort( 0x7e ),	/* 126 */
/* 3026 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 3028 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 3030 */	NdrFcShort( 0x1 ),	/* 1 */
/* 3032 */	NdrFcShort( 0x0 ),	/* 0 */
/* 3034 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pbcmd */

/* 3036 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 3038 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 3040 */	NdrFcShort( 0x264 ),	/* Type Offset=612 */

	/* Parameter pExtraErrorCode */

/* 3042 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 3044 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 3046 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 3048 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 3050 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 3052 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 3054 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 3056 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 3058 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetCustomModeTiming */

/* 3060 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 3062 */	NdrFcLong( 0x0 ),	/* 0 */
/* 3066 */	NdrFcShort( 0x42 ),	/* 66 */
/* 3068 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 3070 */	NdrFcShort( 0x9c ),	/* 156 */
/* 3072 */	NdrFcShort( 0xbe ),	/* 190 */
/* 3074 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 3076 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 3078 */	NdrFcShort( 0x1 ),	/* 1 */
/* 3080 */	NdrFcShort( 0x0 ),	/* 0 */
/* 3082 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pcmt */

/* 3084 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 3086 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 3088 */	NdrFcShort( 0x276 ),	/* Type Offset=630 */

	/* Parameter pExtraErrorCode */

/* 3090 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 3092 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 3094 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 3096 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 3098 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 3100 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 3102 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 3104 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 3106 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetCustomModeList */

/* 3108 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 3110 */	NdrFcLong( 0x0 ),	/* 0 */
/* 3114 */	NdrFcShort( 0x43 ),	/* 67 */
/* 3116 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 3118 */	NdrFcShort( 0xa8f0 ),	/* -22288 */
/* 3120 */	NdrFcShort( 0xa912 ),	/* -22254 */
/* 3122 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 3124 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 3126 */	NdrFcShort( 0x1 ),	/* 1 */
/* 3128 */	NdrFcShort( 0x0 ),	/* 0 */
/* 3130 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pCustomerModeList */

/* 3132 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 3134 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 3136 */	NdrFcShort( 0x230 ),	/* Type Offset=560 */

	/* Parameter pExtraErrorCode */

/* 3138 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 3140 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 3142 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 3144 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 3146 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 3148 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 3150 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 3152 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 3154 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetMediaScaling */

/* 3156 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 3158 */	NdrFcLong( 0x0 ),	/* 0 */
/* 3162 */	NdrFcShort( 0x44 ),	/* 68 */
/* 3164 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 3166 */	NdrFcShort( 0xb0 ),	/* 176 */
/* 3168 */	NdrFcShort( 0xd2 ),	/* 210 */
/* 3170 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 3172 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 3174 */	NdrFcShort( 0x1 ),	/* 1 */
/* 3176 */	NdrFcShort( 0x0 ),	/* 0 */
/* 3178 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pMediaScalingData */

/* 3180 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 3182 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 3184 */	NdrFcShort( 0x294 ),	/* Type Offset=660 */

	/* Parameter pExtraErrorCode */

/* 3186 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 3188 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 3190 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 3192 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 3194 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 3196 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 3198 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 3200 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 3202 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetMediaScaling */

/* 3204 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 3206 */	NdrFcLong( 0x0 ),	/* 0 */
/* 3210 */	NdrFcShort( 0x45 ),	/* 69 */
/* 3212 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 3214 */	NdrFcShort( 0xb0 ),	/* 176 */
/* 3216 */	NdrFcShort( 0xd2 ),	/* 210 */
/* 3218 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 3220 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 3222 */	NdrFcShort( 0x1 ),	/* 1 */
/* 3224 */	NdrFcShort( 0x0 ),	/* 0 */
/* 3226 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pMediaScalingData */

/* 3228 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 3230 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 3232 */	NdrFcShort( 0x294 ),	/* Type Offset=660 */

	/* Parameter pExtraErrorCode */

/* 3234 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 3236 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 3238 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 3240 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 3242 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 3244 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 3246 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 3248 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 3250 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetMediaColor */

/* 3252 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 3254 */	NdrFcLong( 0x0 ),	/* 0 */
/* 3258 */	NdrFcShort( 0x46 ),	/* 70 */
/* 3260 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 3262 */	NdrFcShort( 0xd4 ),	/* 212 */
/* 3264 */	NdrFcShort( 0xf6 ),	/* 246 */
/* 3266 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 3268 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 3270 */	NdrFcShort( 0x1 ),	/* 1 */
/* 3272 */	NdrFcShort( 0x0 ),	/* 0 */
/* 3274 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pMediaColorData */

/* 3276 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 3278 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 3280 */	NdrFcShort( 0x2b0 ),	/* Type Offset=688 */

	/* Parameter pExtraErrorCode */

/* 3282 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 3284 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 3286 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 3288 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 3290 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 3292 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 3294 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 3296 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 3298 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetMediaColor */

/* 3300 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 3302 */	NdrFcLong( 0x0 ),	/* 0 */
/* 3306 */	NdrFcShort( 0x47 ),	/* 71 */
/* 3308 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 3310 */	NdrFcShort( 0xd4 ),	/* 212 */
/* 3312 */	NdrFcShort( 0xf6 ),	/* 246 */
/* 3314 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 3316 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 3318 */	NdrFcShort( 0x1 ),	/* 1 */
/* 3320 */	NdrFcShort( 0x0 ),	/* 0 */
/* 3322 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pMediaColorData */

/* 3324 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 3326 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 3328 */	NdrFcShort( 0x2b0 ),	/* Type Offset=688 */

	/* Parameter pExtraErrorCode */

/* 3330 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 3332 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 3334 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 3336 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 3338 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 3340 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 3342 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 3344 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 3346 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetVideoQuality */

/* 3348 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 3350 */	NdrFcLong( 0x0 ),	/* 0 */
/* 3354 */	NdrFcShort( 0x48 ),	/* 72 */
/* 3356 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 3358 */	NdrFcShort( 0x98 ),	/* 152 */
/* 3360 */	NdrFcShort( 0xba ),	/* 186 */
/* 3362 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 3364 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 3366 */	NdrFcShort( 0x1 ),	/* 1 */
/* 3368 */	NdrFcShort( 0x0 ),	/* 0 */
/* 3370 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pVideoQualityData */

/* 3372 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 3374 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 3376 */	NdrFcShort( 0x2d0 ),	/* Type Offset=720 */

	/* Parameter pExtraErrorCode */

/* 3378 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 3380 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 3382 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 3384 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 3386 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 3388 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 3390 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 3392 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 3394 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetVideoQuality */

/* 3396 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 3398 */	NdrFcLong( 0x0 ),	/* 0 */
/* 3402 */	NdrFcShort( 0x49 ),	/* 73 */
/* 3404 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 3406 */	NdrFcShort( 0x98 ),	/* 152 */
/* 3408 */	NdrFcShort( 0xba ),	/* 186 */
/* 3410 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 3412 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 3414 */	NdrFcShort( 0x1 ),	/* 1 */
/* 3416 */	NdrFcShort( 0x0 ),	/* 0 */
/* 3418 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pVideoQualityData */

/* 3420 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 3422 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 3424 */	NdrFcShort( 0x2d0 ),	/* Type Offset=720 */

	/* Parameter pExtraErrorCode */

/* 3426 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 3428 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 3430 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 3432 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 3434 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 3436 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 3438 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 3440 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 3442 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetAviInfoFrame */

/* 3444 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 3446 */	NdrFcLong( 0x0 ),	/* 0 */
/* 3450 */	NdrFcShort( 0x4a ),	/* 74 */
/* 3452 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 3454 */	NdrFcShort( 0x84 ),	/* 132 */
/* 3456 */	NdrFcShort( 0xa6 ),	/* 166 */
/* 3458 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 3460 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 3462 */	NdrFcShort( 0x1 ),	/* 1 */
/* 3464 */	NdrFcShort( 0x0 ),	/* 0 */
/* 3466 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pAVIFrameInfo */

/* 3468 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 3470 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 3472 */	NdrFcShort( 0x2ec ),	/* Type Offset=748 */

	/* Parameter pExtraErrorCode */

/* 3474 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 3476 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 3478 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 3480 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 3482 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 3484 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 3486 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 3488 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 3490 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetAviInfoFrame */

/* 3492 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 3494 */	NdrFcLong( 0x0 ),	/* 0 */
/* 3498 */	NdrFcShort( 0x4b ),	/* 75 */
/* 3500 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 3502 */	NdrFcShort( 0x84 ),	/* 132 */
/* 3504 */	NdrFcShort( 0xa6 ),	/* 166 */
/* 3506 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 3508 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 3510 */	NdrFcShort( 0x1 ),	/* 1 */
/* 3512 */	NdrFcShort( 0x0 ),	/* 0 */
/* 3514 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pAVIFrameInfo */

/* 3516 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 3518 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 3520 */	NdrFcShort( 0x2ec ),	/* Type Offset=748 */

	/* Parameter pExtraErrorCode */

/* 3522 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 3524 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 3526 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 3528 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 3530 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 3532 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 3534 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 3536 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 3538 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetAttachedDevices */

/* 3540 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 3542 */	NdrFcLong( 0x0 ),	/* 0 */
/* 3546 */	NdrFcShort( 0x4c ),	/* 76 */
/* 3548 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 3550 */	NdrFcShort( 0x6 ),	/* 6 */
/* 3552 */	NdrFcShort( 0x24 ),	/* 36 */
/* 3554 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 3556 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 3558 */	NdrFcShort( 0x1 ),	/* 1 */
/* 3560 */	NdrFcShort( 0x0 ),	/* 0 */
/* 3562 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter osType */

/* 3564 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 3566 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 3568 */	0xd,		/* FC_ENUM16 */
			0x0,		/* 0 */

	/* Parameter pAttachedDevices */

/* 3570 */	NdrFcShort( 0x2150 ),	/* Flags:  out, base type, simple ref, srv alloc size=8 */
/* 3572 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 3574 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pErrorDescription */

/* 3576 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 3578 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 3580 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 3582 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 3584 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 3586 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure EnumAttachedDevices */

/* 3588 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 3590 */	NdrFcLong( 0x0 ),	/* 0 */
/* 3594 */	NdrFcShort( 0x4d ),	/* 77 */
/* 3596 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 3598 */	NdrFcShort( 0x0 ),	/* 0 */
/* 3600 */	NdrFcShort( 0x24 ),	/* 36 */
/* 3602 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x3,		/* 3 */
/* 3604 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 3606 */	NdrFcShort( 0x1 ),	/* 1 */
/* 3608 */	NdrFcShort( 0x0 ),	/* 0 */
/* 3610 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pAttachedDevices */

/* 3612 */	NdrFcShort( 0x2150 ),	/* Flags:  out, base type, simple ref, srv alloc size=8 */
/* 3614 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 3616 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pErrorDescription */

/* 3618 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 3620 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 3622 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 3624 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 3626 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 3628 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure ChangeActiveDevices */

/* 3630 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 3632 */	NdrFcLong( 0x0 ),	/* 0 */
/* 3636 */	NdrFcShort( 0x4e ),	/* 78 */
/* 3638 */	NdrFcShort( 0x1c ),	/* x86 Stack size/offset = 28 */
/* 3640 */	NdrFcShort( 0x16 ),	/* 22 */
/* 3642 */	NdrFcShort( 0x22 ),	/* 34 */
/* 3644 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x6,		/* 6 */
/* 3646 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 3648 */	NdrFcShort( 0x1 ),	/* 1 */
/* 3650 */	NdrFcShort( 0x0 ),	/* 0 */
/* 3652 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter primaryMonitorID */

/* 3654 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 3656 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 3658 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter secondaryMonitorID */

/* 3660 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 3662 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 3664 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter dwFlags */

/* 3666 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 3668 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 3670 */	0xd,		/* FC_ENUM16 */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 3672 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 3674 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 3676 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 3678 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 3680 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 3682 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 3684 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 3686 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 3688 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure DummyFunction */

/* 3690 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 3692 */	NdrFcLong( 0x0 ),	/* 0 */
/* 3696 */	NdrFcShort( 0x4f ),	/* 79 */
/* 3698 */	NdrFcShort( 0x48 ),	/* x86 Stack size/offset = 72 */
/* 3700 */	NdrFcShort( 0x1ae ),	/* 430 */
/* 3702 */	NdrFcShort( 0x8 ),	/* 8 */
/* 3704 */	0x46,		/* Oi2 Flags:  clt must size, has return, has ext, */
			0x11,		/* 17 */
/* 3706 */	0x8,		/* 8 */
			0x1,		/* Ext Flags:  new corr desc, */
/* 3708 */	NdrFcShort( 0x0 ),	/* 0 */
/* 3710 */	NdrFcShort( 0x0 ),	/* 0 */
/* 3712 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pDisplayRelated */

/* 3714 */	NdrFcShort( 0x2008 ),	/* Flags:  in, srv alloc size=8 */
/* 3716 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 3718 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pOperatingMode */

/* 3720 */	NdrFcShort( 0x2008 ),	/* Flags:  in, srv alloc size=8 */
/* 3722 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 3724 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pDeviceType */

/* 3726 */	NdrFcShort( 0x2008 ),	/* Flags:  in, srv alloc size=8 */
/* 3728 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 3730 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pDisplayDeviceStatus */

/* 3732 */	NdrFcShort( 0x2008 ),	/* Flags:  in, srv alloc size=8 */
/* 3734 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 3736 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pDisplayTypes */

/* 3738 */	NdrFcShort( 0x2008 ),	/* Flags:  in, srv alloc size=8 */
/* 3740 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 3742 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pGeneric */

/* 3744 */	NdrFcShort( 0x2008 ),	/* Flags:  in, srv alloc size=8 */
/* 3746 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 3748 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pMediaFeatureTypes */

/* 3750 */	NdrFcShort( 0x2008 ),	/* Flags:  in, srv alloc size=8 */
/* 3752 */	NdrFcShort( 0x1c ),	/* x86 Stack size/offset = 28 */
/* 3754 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pColorQualities */

/* 3756 */	NdrFcShort( 0x2008 ),	/* Flags:  in, srv alloc size=8 */
/* 3758 */	NdrFcShort( 0x20 ),	/* x86 Stack size/offset = 32 */
/* 3760 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pTimingStandards */

/* 3762 */	NdrFcShort( 0x2008 ),	/* Flags:  in, srv alloc size=8 */
/* 3764 */	NdrFcShort( 0x24 ),	/* x86 Stack size/offset = 36 */
/* 3766 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pCustomModes */

/* 3768 */	NdrFcShort( 0x2008 ),	/* Flags:  in, srv alloc size=8 */
/* 3770 */	NdrFcShort( 0x28 ),	/* x86 Stack size/offset = 40 */
/* 3772 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter Resolution */

/* 3774 */	NdrFcShort( 0x10b ),	/* Flags:  must size, must free, in, simple ref, */
/* 3776 */	NdrFcShort( 0x2c ),	/* x86 Stack size/offset = 44 */
/* 3778 */	NdrFcShort( 0x1d4 ),	/* Type Offset=468 */

	/* Parameter Position */

/* 3780 */	NdrFcShort( 0x10a ),	/* Flags:  must free, in, simple ref, */
/* 3782 */	NdrFcShort( 0x30 ),	/* x86 Stack size/offset = 48 */
/* 3784 */	NdrFcShort( 0x88 ),	/* Type Offset=136 */

	/* Parameter pRefreshRate */

/* 3786 */	NdrFcShort( 0x10a ),	/* Flags:  must free, in, simple ref, */
/* 3788 */	NdrFcShort( 0x34 ),	/* x86 Stack size/offset = 52 */
/* 3790 */	NdrFcShort( 0x6e ),	/* Type Offset=110 */

	/* Parameter pDisplayConfigCodes */

/* 3792 */	NdrFcShort( 0x2008 ),	/* Flags:  in, srv alloc size=8 */
/* 3794 */	NdrFcShort( 0x38 ),	/* x86 Stack size/offset = 56 */
/* 3796 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pDisplayOrientation */

/* 3798 */	NdrFcShort( 0x2008 ),	/* Flags:  in, srv alloc size=8 */
/* 3800 */	NdrFcShort( 0x3c ),	/* x86 Stack size/offset = 60 */
/* 3802 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pMediaGamutCompressionValues */

/* 3804 */	NdrFcShort( 0x2008 ),	/* Flags:  in, srv alloc size=8 */
/* 3806 */	NdrFcShort( 0x40 ),	/* x86 Stack size/offset = 64 */
/* 3808 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Return value */

/* 3810 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 3812 */	NdrFcShort( 0x44 ),	/* x86 Stack size/offset = 68 */
/* 3814 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetCurrentConfig */

/* 3816 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 3818 */	NdrFcLong( 0x0 ),	/* 0 */
/* 3822 */	NdrFcShort( 0x50 ),	/* 80 */
/* 3824 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 3826 */	NdrFcShort( 0xbc ),	/* 188 */
/* 3828 */	NdrFcShort( 0xde ),	/* 222 */
/* 3830 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 3832 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 3834 */	NdrFcShort( 0x1 ),	/* 1 */
/* 3836 */	NdrFcShort( 0x0 ),	/* 0 */
/* 3838 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pDeviceDisplays */

/* 3840 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 3842 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 3844 */	NdrFcShort( 0x320 ),	/* Type Offset=800 */

	/* Parameter pExtraErrorCode */

/* 3846 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 3848 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 3850 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 3852 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 3854 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 3856 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 3858 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 3860 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 3862 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure IsWOW64 */

/* 3864 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 3866 */	NdrFcLong( 0x0 ),	/* 0 */
/* 3870 */	NdrFcShort( 0x51 ),	/* 81 */
/* 3872 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 3874 */	NdrFcShort( 0x1c ),	/* 28 */
/* 3876 */	NdrFcShort( 0x8 ),	/* 8 */
/* 3878 */	0x46,		/* Oi2 Flags:  clt must size, has return, has ext, */
			0x3,		/* 3 */
/* 3880 */	0x8,		/* 8 */
			0x5,		/* Ext Flags:  new corr desc, srv corr check, */
/* 3882 */	NdrFcShort( 0x0 ),	/* 0 */
/* 3884 */	NdrFcShort( 0x1 ),	/* 1 */
/* 3886 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pIsWOW64 */

/* 3888 */	NdrFcShort( 0x148 ),	/* Flags:  in, base type, simple ref, */
/* 3890 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 3892 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pErrorDescription */

/* 3894 */	NdrFcShort( 0x10b ),	/* Flags:  must size, must free, in, simple ref, */
/* 3896 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 3898 */	NdrFcShort( 0x1c ),	/* Type Offset=28 */

	/* Return value */

/* 3900 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 3902 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 3904 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure DoEscape */

/* 3906 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 3908 */	NdrFcLong( 0x0 ),	/* 0 */
/* 3912 */	NdrFcShort( 0x52 ),	/* 82 */
/* 3914 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 3916 */	NdrFcShort( 0x6 ),	/* 6 */
/* 3918 */	NdrFcShort( 0x8 ),	/* 8 */
/* 3920 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x4,		/* 4 */
/* 3922 */	0x8,		/* 8 */
			0x7,		/* Ext Flags:  new corr desc, clt corr check, srv corr check, */
/* 3924 */	NdrFcShort( 0x1 ),	/* 1 */
/* 3926 */	NdrFcShort( 0x1 ),	/* 1 */
/* 3928 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter osType */

/* 3930 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 3932 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 3934 */	0xd,		/* FC_ENUM16 */
			0x0,		/* 0 */

	/* Parameter pKeyName */

/* 3936 */	NdrFcShort( 0x10b ),	/* Flags:  must size, must free, in, simple ref, */
/* 3938 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 3940 */	NdrFcShort( 0x1c ),	/* Type Offset=28 */

	/* Parameter pErrorDescription */

/* 3942 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 3944 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 3946 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 3948 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 3950 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 3952 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetHueSaturation */

/* 3954 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 3956 */	NdrFcLong( 0x0 ),	/* 0 */
/* 3960 */	NdrFcShort( 0x53 ),	/* 83 */
/* 3962 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 3964 */	NdrFcShort( 0x7c ),	/* 124 */
/* 3966 */	NdrFcShort( 0x9e ),	/* 158 */
/* 3968 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 3970 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 3972 */	NdrFcShort( 0x1 ),	/* 1 */
/* 3974 */	NdrFcShort( 0x0 ),	/* 0 */
/* 3976 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pHueSat */

/* 3978 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 3980 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 3982 */	NdrFcShort( 0x33a ),	/* Type Offset=826 */

	/* Parameter pExtraErrorCode */

/* 3984 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 3986 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 3988 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 3990 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 3992 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 3994 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 3996 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 3998 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 4000 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetHueSaturation */

/* 4002 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 4004 */	NdrFcLong( 0x0 ),	/* 0 */
/* 4008 */	NdrFcShort( 0x54 ),	/* 84 */
/* 4010 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 4012 */	NdrFcShort( 0x7c ),	/* 124 */
/* 4014 */	NdrFcShort( 0x9e ),	/* 158 */
/* 4016 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 4018 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 4020 */	NdrFcShort( 0x1 ),	/* 1 */
/* 4022 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4024 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pHueSat */

/* 4026 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 4028 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 4030 */	NdrFcShort( 0x33a ),	/* Type Offset=826 */

	/* Parameter pExtraErrorCode */

/* 4032 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 4034 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 4036 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 4038 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 4040 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 4042 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 4044 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 4046 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 4048 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetVideoQualityExtended */

/* 4050 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 4052 */	NdrFcLong( 0x0 ),	/* 0 */
/* 4056 */	NdrFcShort( 0x55 ),	/* 85 */
/* 4058 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 4060 */	NdrFcShort( 0x100 ),	/* 256 */
/* 4062 */	NdrFcShort( 0x122 ),	/* 290 */
/* 4064 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 4066 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 4068 */	NdrFcShort( 0x1 ),	/* 1 */
/* 4070 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4072 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pVideoQualityEx */

/* 4074 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 4076 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 4078 */	NdrFcShort( 0x350 ),	/* Type Offset=848 */

	/* Parameter pExtraErrorCode */

/* 4080 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 4082 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 4084 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 4086 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 4088 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 4090 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 4092 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 4094 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 4096 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetVideoQualityExtended */

/* 4098 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 4100 */	NdrFcLong( 0x0 ),	/* 0 */
/* 4104 */	NdrFcShort( 0x56 ),	/* 86 */
/* 4106 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 4108 */	NdrFcShort( 0x100 ),	/* 256 */
/* 4110 */	NdrFcShort( 0x122 ),	/* 290 */
/* 4112 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 4114 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 4116 */	NdrFcShort( 0x1 ),	/* 1 */
/* 4118 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4120 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pVideoQualityEx */

/* 4122 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 4124 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 4126 */	NdrFcShort( 0x350 ),	/* Type Offset=848 */

	/* Parameter pExtraErrorCode */

/* 4128 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 4130 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 4132 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 4134 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 4136 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 4138 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 4140 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 4142 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 4144 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetSystemConfigDataNViews */

/* 4146 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 4148 */	NdrFcLong( 0x0 ),	/* 0 */
/* 4152 */	NdrFcShort( 0x57 ),	/* 87 */
/* 4154 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 4156 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4158 */	NdrFcShort( 0x22 ),	/* 34 */
/* 4160 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x4,		/* 4 */
/* 4162 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 4164 */	NdrFcShort( 0x1 ),	/* 1 */
/* 4166 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4168 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter dataNView */

/* 4170 */	NdrFcShort( 0x11b ),	/* Flags:  must size, must free, in, out, simple ref, */
/* 4172 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 4174 */	NdrFcShort( 0x398 ),	/* Type Offset=920 */

	/* Parameter pExtraErrorCode */

/* 4176 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 4178 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 4180 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 4182 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 4184 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 4186 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 4188 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 4190 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 4192 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetSystemConfigDataNViews */

/* 4194 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 4196 */	NdrFcLong( 0x0 ),	/* 0 */
/* 4200 */	NdrFcShort( 0x58 ),	/* 88 */
/* 4202 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 4204 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4206 */	NdrFcShort( 0x22 ),	/* 34 */
/* 4208 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x4,		/* 4 */
/* 4210 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 4212 */	NdrFcShort( 0x1 ),	/* 1 */
/* 4214 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4216 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter dataNView */

/* 4218 */	NdrFcShort( 0x11b ),	/* Flags:  must size, must free, in, out, simple ref, */
/* 4220 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 4222 */	NdrFcShort( 0x398 ),	/* Type Offset=920 */

	/* Parameter pExtraErrorCode */

/* 4224 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 4226 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 4228 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 4230 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 4232 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 4234 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 4236 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 4238 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 4240 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetScaling */

/* 4242 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 4244 */	NdrFcLong( 0x0 ),	/* 0 */
/* 4248 */	NdrFcShort( 0x59 ),	/* 89 */
/* 4250 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 4252 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4254 */	NdrFcShort( 0x22 ),	/* 34 */
/* 4256 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x4,		/* 4 */
/* 4258 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 4260 */	NdrFcShort( 0x1 ),	/* 1 */
/* 4262 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4264 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pData */

/* 4266 */	NdrFcShort( 0x11b ),	/* Flags:  must size, must free, in, out, simple ref, */
/* 4268 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 4270 */	NdrFcShort( 0x3ae ),	/* Type Offset=942 */

	/* Parameter pExtraErrorCode */

/* 4272 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 4274 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 4276 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 4278 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 4280 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 4282 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 4284 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 4286 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 4288 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetScaling */

/* 4290 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 4292 */	NdrFcLong( 0x0 ),	/* 0 */
/* 4296 */	NdrFcShort( 0x5a ),	/* 90 */
/* 4298 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 4300 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4302 */	NdrFcShort( 0x22 ),	/* 34 */
/* 4304 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x4,		/* 4 */
/* 4306 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 4308 */	NdrFcShort( 0x1 ),	/* 1 */
/* 4310 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4312 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pData */

/* 4314 */	NdrFcShort( 0x11b ),	/* Flags:  must size, must free, in, out, simple ref, */
/* 4316 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 4318 */	NdrFcShort( 0x3ae ),	/* Type Offset=942 */

	/* Parameter pExtraErrorCode */

/* 4320 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 4322 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 4324 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 4326 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 4328 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 4330 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 4332 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 4334 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 4336 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure QueryforVideoModeList */

/* 4338 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 4340 */	NdrFcLong( 0x0 ),	/* 0 */
/* 4344 */	NdrFcShort( 0x5b ),	/* 91 */
/* 4346 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 4348 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4350 */	NdrFcShort( 0x22 ),	/* 34 */
/* 4352 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x4,		/* 4 */
/* 4354 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 4356 */	NdrFcShort( 0x1 ),	/* 1 */
/* 4358 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4360 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pVideoModeList */

/* 4362 */	NdrFcShort( 0x11b ),	/* Flags:  must size, must free, in, out, simple ref, */
/* 4364 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 4366 */	NdrFcShort( 0x3e4 ),	/* Type Offset=996 */

	/* Parameter pExtraErrorCode */

/* 4368 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 4370 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 4372 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 4374 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 4376 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 4378 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 4380 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 4382 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 4384 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetIndividualVideoMode */

/* 4386 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 4388 */	NdrFcLong( 0x0 ),	/* 0 */
/* 4392 */	NdrFcShort( 0x5c ),	/* 92 */
/* 4394 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 4396 */	NdrFcShort( 0x8 ),	/* 8 */
/* 4398 */	NdrFcShort( 0x22 ),	/* 34 */
/* 4400 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x5,		/* 5 */
/* 4402 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 4404 */	NdrFcShort( 0x1 ),	/* 1 */
/* 4406 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4408 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pVideoMode */

/* 4410 */	NdrFcShort( 0x11b ),	/* Flags:  must size, must free, in, out, simple ref, */
/* 4412 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 4414 */	NdrFcShort( 0x1d4 ),	/* Type Offset=468 */

	/* Parameter index */

/* 4416 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 4418 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 4420 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 4422 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 4424 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 4426 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 4428 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 4430 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 4432 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 4434 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 4436 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 4438 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetTriClone */

/* 4440 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 4442 */	NdrFcLong( 0x0 ),	/* 0 */
/* 4446 */	NdrFcShort( 0x5d ),	/* 93 */
/* 4448 */	NdrFcShort( 0x1c ),	/* x86 Stack size/offset = 28 */
/* 4450 */	NdrFcShort( 0x18 ),	/* 24 */
/* 4452 */	NdrFcShort( 0x22 ),	/* 34 */
/* 4454 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x6,		/* 6 */
/* 4456 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 4458 */	NdrFcShort( 0x1 ),	/* 1 */
/* 4460 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4462 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter primaryMonitorID */

/* 4464 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 4466 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 4468 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter secondaryMonitorID */

/* 4470 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 4472 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 4474 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter tertiaryMonitorID */

/* 4476 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 4478 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 4480 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 4482 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 4484 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 4486 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 4488 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 4490 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 4492 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 4494 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 4496 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 4498 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetTriExtended */

/* 4500 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 4502 */	NdrFcLong( 0x0 ),	/* 0 */
/* 4506 */	NdrFcShort( 0x5e ),	/* 94 */
/* 4508 */	NdrFcShort( 0x1c ),	/* x86 Stack size/offset = 28 */
/* 4510 */	NdrFcShort( 0x18 ),	/* 24 */
/* 4512 */	NdrFcShort( 0x22 ),	/* 34 */
/* 4514 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x6,		/* 6 */
/* 4516 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 4518 */	NdrFcShort( 0x1 ),	/* 1 */
/* 4520 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4522 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter primaryMonitorID */

/* 4524 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 4526 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 4528 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter secondaryMonitorID */

/* 4530 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 4532 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 4534 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter tertiaryMonitorID */

/* 4536 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 4538 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 4540 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 4542 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 4544 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 4546 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 4548 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 4550 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 4552 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 4554 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 4556 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 4558 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetGamutData */

/* 4560 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 4562 */	NdrFcLong( 0x0 ),	/* 0 */
/* 4566 */	NdrFcShort( 0x5f ),	/* 95 */
/* 4568 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 4570 */	NdrFcShort( 0xa4 ),	/* 164 */
/* 4572 */	NdrFcShort( 0xc6 ),	/* 198 */
/* 4574 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 4576 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 4578 */	NdrFcShort( 0x1 ),	/* 1 */
/* 4580 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4582 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pGamutData */

/* 4584 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 4586 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 4588 */	NdrFcShort( 0x414 ),	/* Type Offset=1044 */

	/* Parameter pExtraErrorCode */

/* 4590 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 4592 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 4594 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 4596 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 4598 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 4600 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 4602 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 4604 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 4606 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetGamutData */

/* 4608 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 4610 */	NdrFcLong( 0x0 ),	/* 0 */
/* 4614 */	NdrFcShort( 0x60 ),	/* 96 */
/* 4616 */	NdrFcShort( 0x20 ),	/* x86 Stack size/offset = 32 */
/* 4618 */	NdrFcShort( 0xf8 ),	/* 248 */
/* 4620 */	NdrFcShort( 0xc6 ),	/* 198 */
/* 4622 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x7,		/* 7 */
/* 4624 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 4626 */	NdrFcShort( 0x1 ),	/* 1 */
/* 4628 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4630 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pGamutData */

/* 4632 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 4634 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 4636 */	NdrFcShort( 0x414 ),	/* Type Offset=1044 */

	/* Parameter CSCMatrixRow1 */

/* 4638 */	NdrFcShort( 0xa ),	/* Flags:  must free, in, */
/* 4640 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 4642 */	NdrFcShort( 0x404 ),	/* Type Offset=1028 */

	/* Parameter CSCMatrixRow2 */

/* 4644 */	NdrFcShort( 0xa ),	/* Flags:  must free, in, */
/* 4646 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 4648 */	NdrFcShort( 0x404 ),	/* Type Offset=1028 */

	/* Parameter CSCMatrixRow3 */

/* 4650 */	NdrFcShort( 0xa ),	/* Flags:  must free, in, */
/* 4652 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 4654 */	NdrFcShort( 0x404 ),	/* Type Offset=1028 */

	/* Parameter pExtraErrorCode */

/* 4656 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 4658 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 4660 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 4662 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 4664 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 4666 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 4668 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 4670 */	NdrFcShort( 0x1c ),	/* x86 Stack size/offset = 28 */
/* 4672 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetCSCData */

/* 4674 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 4676 */	NdrFcLong( 0x0 ),	/* 0 */
/* 4680 */	NdrFcShort( 0x61 ),	/* 97 */
/* 4682 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 4684 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4686 */	NdrFcShort( 0x22 ),	/* 34 */
/* 4688 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x4,		/* 4 */
/* 4690 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 4692 */	NdrFcShort( 0x1 ),	/* 1 */
/* 4694 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4696 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pCSCData */

/* 4698 */	NdrFcShort( 0x11b ),	/* Flags:  must size, must free, in, out, simple ref, */
/* 4700 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 4702 */	NdrFcShort( 0x43e ),	/* Type Offset=1086 */

	/* Parameter pExtraErrorCode */

/* 4704 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 4706 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 4708 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 4710 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 4712 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 4714 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 4716 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 4718 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 4720 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetCSCData */

/* 4722 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 4724 */	NdrFcLong( 0x0 ),	/* 0 */
/* 4728 */	NdrFcShort( 0x62 ),	/* 98 */
/* 4730 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 4732 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4734 */	NdrFcShort( 0x22 ),	/* 34 */
/* 4736 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x4,		/* 4 */
/* 4738 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 4740 */	NdrFcShort( 0x1 ),	/* 1 */
/* 4742 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4744 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pCSCData */

/* 4746 */	NdrFcShort( 0x11b ),	/* Flags:  must size, must free, in, out, simple ref, */
/* 4748 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 4750 */	NdrFcShort( 0x43e ),	/* Type Offset=1086 */

	/* Parameter pExtraErrorCode */

/* 4752 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 4754 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 4756 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 4758 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 4760 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 4762 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 4764 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 4766 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 4768 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetVideoQualityExtended2 */

/* 4770 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 4772 */	NdrFcLong( 0x0 ),	/* 0 */
/* 4776 */	NdrFcShort( 0x63 ),	/* 99 */
/* 4778 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 4780 */	NdrFcShort( 0xfc ),	/* 252 */
/* 4782 */	NdrFcShort( 0x11e ),	/* 286 */
/* 4784 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 4786 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 4788 */	NdrFcShort( 0x1 ),	/* 1 */
/* 4790 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4792 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pVideoQualityEx2 */

/* 4794 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 4796 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 4798 */	NdrFcShort( 0x454 ),	/* Type Offset=1108 */

	/* Parameter pExtraErrorCode */

/* 4800 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 4802 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 4804 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 4806 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 4808 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 4810 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 4812 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 4814 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 4816 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetVideoQualityExtended2 */

/* 4818 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 4820 */	NdrFcLong( 0x0 ),	/* 0 */
/* 4824 */	NdrFcShort( 0x64 ),	/* 100 */
/* 4826 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 4828 */	NdrFcShort( 0xfc ),	/* 252 */
/* 4830 */	NdrFcShort( 0x11e ),	/* 286 */
/* 4832 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 4834 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 4836 */	NdrFcShort( 0x1 ),	/* 1 */
/* 4838 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4840 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pVideoQualityEx2 */

/* 4842 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 4844 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 4846 */	NdrFcShort( 0x454 ),	/* Type Offset=1108 */

	/* Parameter pExtraErrorCode */

/* 4848 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 4850 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 4852 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 4854 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 4856 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 4858 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 4860 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 4862 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 4864 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetMediaColorExtended2 */

/* 4866 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 4868 */	NdrFcLong( 0x0 ),	/* 0 */
/* 4872 */	NdrFcShort( 0x65 ),	/* 101 */
/* 4874 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 4876 */	NdrFcShort( 0x124 ),	/* 292 */
/* 4878 */	NdrFcShort( 0x146 ),	/* 326 */
/* 4880 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 4882 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 4884 */	NdrFcShort( 0x1 ),	/* 1 */
/* 4886 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4888 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pMediaColorEx2 */

/* 4890 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 4892 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 4894 */	NdrFcShort( 0x492 ),	/* Type Offset=1170 */

	/* Parameter pExtraErrorCode */

/* 4896 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 4898 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 4900 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 4902 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 4904 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 4906 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 4908 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 4910 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 4912 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetMediaColorExtended2 */

/* 4914 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 4916 */	NdrFcLong( 0x0 ),	/* 0 */
/* 4920 */	NdrFcShort( 0x66 ),	/* 102 */
/* 4922 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 4924 */	NdrFcShort( 0x124 ),	/* 292 */
/* 4926 */	NdrFcShort( 0x146 ),	/* 326 */
/* 4928 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 4930 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 4932 */	NdrFcShort( 0x1 ),	/* 1 */
/* 4934 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4936 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pMediaColorEx2 */

/* 4938 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 4940 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 4942 */	NdrFcShort( 0x492 ),	/* Type Offset=1170 */

	/* Parameter pExtraErrorCode */

/* 4944 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 4946 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 4948 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 4950 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 4952 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 4954 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 4956 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 4958 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 4960 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetAuxInfo */

/* 4962 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 4964 */	NdrFcLong( 0x0 ),	/* 0 */
/* 4968 */	NdrFcShort( 0x67 ),	/* 103 */
/* 4970 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 4972 */	NdrFcShort( 0x54 ),	/* 84 */
/* 4974 */	NdrFcShort( 0x76 ),	/* 118 */
/* 4976 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 4978 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 4980 */	NdrFcShort( 0x1 ),	/* 1 */
/* 4982 */	NdrFcShort( 0x0 ),	/* 0 */
/* 4984 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pAuxInfo */

/* 4986 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 4988 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 4990 */	NdrFcShort( 0x4e0 ),	/* Type Offset=1248 */

	/* Parameter pExtraErrorCode */

/* 4992 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 4994 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 4996 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 4998 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 5000 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5002 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 5004 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 5006 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 5008 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetAuxInfo */

/* 5010 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 5012 */	NdrFcLong( 0x0 ),	/* 0 */
/* 5016 */	NdrFcShort( 0x68 ),	/* 104 */
/* 5018 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 5020 */	NdrFcShort( 0x54 ),	/* 84 */
/* 5022 */	NdrFcShort( 0x76 ),	/* 118 */
/* 5024 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 5026 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 5028 */	NdrFcShort( 0x1 ),	/* 1 */
/* 5030 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5032 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pAuxInfo */

/* 5034 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 5036 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 5038 */	NdrFcShort( 0x4e0 ),	/* Type Offset=1248 */

	/* Parameter pExtraErrorCode */

/* 5040 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 5042 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 5044 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 5046 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 5048 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5050 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 5052 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 5054 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 5056 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetSourceHdmiGBDdata */

/* 5058 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 5060 */	NdrFcLong( 0x0 ),	/* 0 */
/* 5064 */	NdrFcShort( 0x69 ),	/* 105 */
/* 5066 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 5068 */	NdrFcShort( 0x78 ),	/* 120 */
/* 5070 */	NdrFcShort( 0x9a ),	/* 154 */
/* 5072 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 5074 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 5076 */	NdrFcShort( 0x1 ),	/* 1 */
/* 5078 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5080 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pSourceHdmiGBDData */

/* 5082 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 5084 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 5086 */	NdrFcShort( 0x504 ),	/* Type Offset=1284 */

	/* Parameter pExtraErrorCode */

/* 5088 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 5090 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 5092 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 5094 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 5096 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5098 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 5100 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 5102 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 5104 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetSourceHdmiGBDdata */

/* 5106 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 5108 */	NdrFcLong( 0x0 ),	/* 0 */
/* 5112 */	NdrFcShort( 0x6a ),	/* 106 */
/* 5114 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 5116 */	NdrFcShort( 0x78 ),	/* 120 */
/* 5118 */	NdrFcShort( 0x9a ),	/* 154 */
/* 5120 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 5122 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 5124 */	NdrFcShort( 0x1 ),	/* 1 */
/* 5126 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5128 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pSourceHdmiGBDData */

/* 5130 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 5132 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 5134 */	NdrFcShort( 0x504 ),	/* Type Offset=1284 */

	/* Parameter pExtraErrorCode */

/* 5136 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 5138 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 5140 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 5142 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 5144 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5146 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 5148 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 5150 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 5152 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetSupportedConfigurationEx */

/* 5154 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 5156 */	NdrFcLong( 0x0 ),	/* 0 */
/* 5160 */	NdrFcShort( 0x6b ),	/* 107 */
/* 5162 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 5164 */	NdrFcShort( 0x1628 ),	/* 5672 */
/* 5166 */	NdrFcShort( 0x164a ),	/* 5706 */
/* 5168 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 5170 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 5172 */	NdrFcShort( 0x1 ),	/* 1 */
/* 5174 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5176 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBuffer */

/* 5178 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 5180 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 5182 */	NdrFcShort( 0x52c ),	/* Type Offset=1324 */

	/* Parameter pExtraErrorCode */

/* 5184 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 5186 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 5188 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 5190 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 5192 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5194 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 5196 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 5198 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 5200 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetColorGamut */

/* 5202 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 5204 */	NdrFcLong( 0x0 ),	/* 0 */
/* 5208 */	NdrFcShort( 0x6c ),	/* 108 */
/* 5210 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 5212 */	NdrFcShort( 0x4c ),	/* 76 */
/* 5214 */	NdrFcShort( 0x6e ),	/* 110 */
/* 5216 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 5218 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 5220 */	NdrFcShort( 0x1 ),	/* 1 */
/* 5222 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5224 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pGamutData */

/* 5226 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 5228 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 5230 */	NdrFcShort( 0x540 ),	/* Type Offset=1344 */

	/* Parameter pExtraErrorCode */

/* 5232 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 5234 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 5236 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 5238 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 5240 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5242 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 5244 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 5246 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 5248 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetColorGamut */

/* 5250 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 5252 */	NdrFcLong( 0x0 ),	/* 0 */
/* 5256 */	NdrFcShort( 0x6d ),	/* 109 */
/* 5258 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 5260 */	NdrFcShort( 0x4c ),	/* 76 */
/* 5262 */	NdrFcShort( 0x6e ),	/* 110 */
/* 5264 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 5266 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 5268 */	NdrFcShort( 0x1 ),	/* 1 */
/* 5270 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5272 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pGamutData */

/* 5274 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 5276 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 5278 */	NdrFcShort( 0x540 ),	/* Type Offset=1344 */

	/* Parameter pExtraErrorCode */

/* 5280 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 5282 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 5284 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 5286 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 5288 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5290 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 5292 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 5294 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 5296 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetXvYcc */

/* 5298 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 5300 */	NdrFcLong( 0x0 ),	/* 0 */
/* 5304 */	NdrFcShort( 0x6e ),	/* 110 */
/* 5306 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 5308 */	NdrFcShort( 0x34 ),	/* 52 */
/* 5310 */	NdrFcShort( 0x56 ),	/* 86 */
/* 5312 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 5314 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 5316 */	NdrFcShort( 0x1 ),	/* 1 */
/* 5318 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5320 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pXvyccData */

/* 5322 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 5324 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 5326 */	NdrFcShort( 0x88 ),	/* Type Offset=136 */

	/* Parameter pExtraErrorCode */

/* 5328 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 5330 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 5332 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 5334 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 5336 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5338 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 5340 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 5342 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 5344 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetXvYcc */

/* 5346 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 5348 */	NdrFcLong( 0x0 ),	/* 0 */
/* 5352 */	NdrFcShort( 0x6f ),	/* 111 */
/* 5354 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 5356 */	NdrFcShort( 0x34 ),	/* 52 */
/* 5358 */	NdrFcShort( 0x56 ),	/* 86 */
/* 5360 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 5362 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 5364 */	NdrFcShort( 0x1 ),	/* 1 */
/* 5366 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5368 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pXvyccData */

/* 5370 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 5372 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 5374 */	NdrFcShort( 0x88 ),	/* Type Offset=136 */

	/* Parameter pExtraErrorCode */

/* 5376 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 5378 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 5380 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 5382 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 5384 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5386 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 5388 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 5390 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 5392 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetYcBcr */

/* 5394 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 5396 */	NdrFcLong( 0x0 ),	/* 0 */
/* 5400 */	NdrFcShort( 0x70 ),	/* 112 */
/* 5402 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 5404 */	NdrFcShort( 0x34 ),	/* 52 */
/* 5406 */	NdrFcShort( 0x56 ),	/* 86 */
/* 5408 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 5410 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 5412 */	NdrFcShort( 0x1 ),	/* 1 */
/* 5414 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5416 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pYCBCRData */

/* 5418 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 5420 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 5422 */	NdrFcShort( 0x88 ),	/* Type Offset=136 */

	/* Parameter pExtraErrorCode */

/* 5424 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 5426 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 5428 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 5430 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 5432 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5434 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 5436 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 5438 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 5440 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetYcBcr */

/* 5442 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 5444 */	NdrFcLong( 0x0 ),	/* 0 */
/* 5448 */	NdrFcShort( 0x71 ),	/* 113 */
/* 5450 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 5452 */	NdrFcShort( 0x34 ),	/* 52 */
/* 5454 */	NdrFcShort( 0x56 ),	/* 86 */
/* 5456 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 5458 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 5460 */	NdrFcShort( 0x1 ),	/* 1 */
/* 5462 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5464 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pYCBCRData */

/* 5466 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 5468 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 5470 */	NdrFcShort( 0x88 ),	/* Type Offset=136 */

	/* Parameter pExtraErrorCode */

/* 5472 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 5474 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 5476 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 5478 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 5480 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5482 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 5484 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 5486 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 5488 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetGOPVersion */

/* 5490 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 5492 */	NdrFcLong( 0x0 ),	/* 0 */
/* 5496 */	NdrFcShort( 0x72 ),	/* 114 */
/* 5498 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 5500 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5502 */	NdrFcShort( 0x22 ),	/* 34 */
/* 5504 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x4,		/* 4 */
/* 5506 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 5508 */	NdrFcShort( 0x1 ),	/* 1 */
/* 5510 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5512 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pGopVersion */

/* 5514 */	NdrFcShort( 0x11b ),	/* Flags:  must size, must free, in, out, simple ref, */
/* 5516 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 5518 */	NdrFcShort( 0x552 ),	/* Type Offset=1362 */

	/* Parameter pExtraErrorCode */

/* 5520 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 5522 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 5524 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 5526 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 5528 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5530 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 5532 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 5534 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 5536 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetVideoModeListEx */

/* 5538 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 5540 */	NdrFcLong( 0x0 ),	/* 0 */
/* 5544 */	NdrFcShort( 0x73 ),	/* 115 */
/* 5546 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 5548 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5550 */	NdrFcShort( 0x22 ),	/* 34 */
/* 5552 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x4,		/* 4 */
/* 5554 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 5556 */	NdrFcShort( 0x1 ),	/* 1 */
/* 5558 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5560 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pVideoModeListEx */

/* 5562 */	NdrFcShort( 0x11b ),	/* Flags:  must size, must free, in, out, simple ref, */
/* 5564 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 5566 */	NdrFcShort( 0x3e4 ),	/* Type Offset=996 */

	/* Parameter pExtraErrorCode */

/* 5568 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 5570 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 5572 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 5574 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 5576 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5578 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 5580 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 5582 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 5584 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetVideoGamutMapping */

/* 5586 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 5588 */	NdrFcLong( 0x0 ),	/* 0 */
/* 5592 */	NdrFcShort( 0x74 ),	/* 116 */
/* 5594 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 5596 */	NdrFcShort( 0x4c ),	/* 76 */
/* 5598 */	NdrFcShort( 0x6e ),	/* 110 */
/* 5600 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 5602 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 5604 */	NdrFcShort( 0x1 ),	/* 1 */
/* 5606 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5608 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pMediaGamutMapping */

/* 5610 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 5612 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 5614 */	NdrFcShort( 0x540 ),	/* Type Offset=1344 */

	/* Parameter pExtraErrorCode */

/* 5616 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 5618 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 5620 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 5622 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 5624 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5626 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 5628 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 5630 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 5632 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetVideoGamutMapping */

/* 5634 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 5636 */	NdrFcLong( 0x0 ),	/* 0 */
/* 5640 */	NdrFcShort( 0x75 ),	/* 117 */
/* 5642 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 5644 */	NdrFcShort( 0x4c ),	/* 76 */
/* 5646 */	NdrFcShort( 0x6e ),	/* 110 */
/* 5648 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 5650 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 5652 */	NdrFcShort( 0x1 ),	/* 1 */
/* 5654 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5656 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pMediaGamutMapping */

/* 5658 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 5660 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 5662 */	NdrFcShort( 0x540 ),	/* Type Offset=1344 */

	/* Parameter pExtraErrorCode */

/* 5664 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 5666 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 5668 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 5670 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 5672 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5674 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 5676 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 5678 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 5680 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetChipSetInformation */

/* 5682 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 5684 */	NdrFcLong( 0x0 ),	/* 0 */
/* 5688 */	NdrFcShort( 0x76 ),	/* 118 */
/* 5690 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 5692 */	NdrFcShort( 0x1c ),	/* 28 */
/* 5694 */	NdrFcShort( 0x3e ),	/* 62 */
/* 5696 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 5698 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 5700 */	NdrFcShort( 0x1 ),	/* 1 */
/* 5702 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5704 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pChipsetInfo */

/* 5706 */	NdrFcShort( 0x158 ),	/* Flags:  in, out, base type, simple ref, */
/* 5708 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 5710 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 5712 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 5714 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 5716 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 5718 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 5720 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5722 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 5724 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 5726 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 5728 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetVideoFeatureSupportList */

/* 5730 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 5732 */	NdrFcLong( 0x0 ),	/* 0 */
/* 5736 */	NdrFcShort( 0x77 ),	/* 119 */
/* 5738 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 5740 */	NdrFcShort( 0x2c ),	/* 44 */
/* 5742 */	NdrFcShort( 0x4e ),	/* 78 */
/* 5744 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 5746 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 5748 */	NdrFcShort( 0x1 ),	/* 1 */
/* 5750 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5752 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pVideoSupportList */

/* 5754 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 5756 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 5758 */	NdrFcShort( 0xec ),	/* Type Offset=236 */

	/* Parameter pExtraErrorCode */

/* 5760 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 5762 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 5764 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 5766 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 5768 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5770 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 5772 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 5774 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 5776 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetMediaScalingEx2 */

/* 5778 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 5780 */	NdrFcLong( 0x0 ),	/* 0 */
/* 5784 */	NdrFcShort( 0x78 ),	/* 120 */
/* 5786 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 5788 */	NdrFcShort( 0x88 ),	/* 136 */
/* 5790 */	NdrFcShort( 0xaa ),	/* 170 */
/* 5792 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 5794 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 5796 */	NdrFcShort( 0x1 ),	/* 1 */
/* 5798 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5800 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter mediaScalingEx2 */

/* 5802 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 5804 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 5806 */	NdrFcShort( 0x564 ),	/* Type Offset=1380 */

	/* Parameter pExtraErrorCode */

/* 5808 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 5810 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 5812 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 5814 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 5816 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5818 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 5820 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 5822 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 5824 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetMediaScalingEx2 */

/* 5826 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 5828 */	NdrFcLong( 0x0 ),	/* 0 */
/* 5832 */	NdrFcShort( 0x79 ),	/* 121 */
/* 5834 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 5836 */	NdrFcShort( 0x88 ),	/* 136 */
/* 5838 */	NdrFcShort( 0xaa ),	/* 170 */
/* 5840 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 5842 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 5844 */	NdrFcShort( 0x1 ),	/* 1 */
/* 5846 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5848 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter mediaScalingEx2 */

/* 5850 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 5852 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 5854 */	NdrFcShort( 0x564 ),	/* Type Offset=1380 */

	/* Parameter pExtraErrorCode */

/* 5856 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 5858 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 5860 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 5862 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 5864 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5866 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 5868 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 5870 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 5872 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure ReadRegistryEnableNLAS */

/* 5874 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 5876 */	NdrFcLong( 0x0 ),	/* 0 */
/* 5880 */	NdrFcShort( 0x7a ),	/* 122 */
/* 5882 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5884 */	NdrFcShort( 0x1c ),	/* 28 */
/* 5886 */	NdrFcShort( 0x8 ),	/* 8 */
/* 5888 */	0x44,		/* Oi2 Flags:  has return, has ext, */
			0x2,		/* 2 */
/* 5890 */	0x8,		/* 8 */
			0x1,		/* Ext Flags:  new corr desc, */
/* 5892 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5894 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5896 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter regvalue */

/* 5898 */	NdrFcShort( 0x148 ),	/* Flags:  in, base type, simple ref, */
/* 5900 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 5902 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Return value */

/* 5904 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 5906 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 5908 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure ReadRegistryNLASVerticalCrop */

/* 5910 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 5912 */	NdrFcLong( 0x0 ),	/* 0 */
/* 5916 */	NdrFcShort( 0x7b ),	/* 123 */
/* 5918 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5920 */	NdrFcShort( 0x1c ),	/* 28 */
/* 5922 */	NdrFcShort( 0x8 ),	/* 8 */
/* 5924 */	0x44,		/* Oi2 Flags:  has return, has ext, */
			0x2,		/* 2 */
/* 5926 */	0x8,		/* 8 */
			0x1,		/* Ext Flags:  new corr desc, */
/* 5928 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5930 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5932 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter regvalue */

/* 5934 */	NdrFcShort( 0x148 ),	/* Flags:  in, base type, simple ref, */
/* 5936 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 5938 */	0xa,		/* FC_FLOAT */
			0x0,		/* 0 */

	/* Return value */

/* 5940 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 5942 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 5944 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure ReadRegistryNLASHLinearRegion */

/* 5946 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 5948 */	NdrFcLong( 0x0 ),	/* 0 */
/* 5952 */	NdrFcShort( 0x7c ),	/* 124 */
/* 5954 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5956 */	NdrFcShort( 0x1c ),	/* 28 */
/* 5958 */	NdrFcShort( 0x8 ),	/* 8 */
/* 5960 */	0x44,		/* Oi2 Flags:  has return, has ext, */
			0x2,		/* 2 */
/* 5962 */	0x8,		/* 8 */
			0x1,		/* Ext Flags:  new corr desc, */
/* 5964 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5966 */	NdrFcShort( 0x0 ),	/* 0 */
/* 5968 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter regvalue */

/* 5970 */	NdrFcShort( 0x148 ),	/* Flags:  in, base type, simple ref, */
/* 5972 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 5974 */	0xa,		/* FC_FLOAT */
			0x0,		/* 0 */

	/* Return value */

/* 5976 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 5978 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 5980 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure ReadRegistryNLASNonLinearCrop */

/* 5982 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 5984 */	NdrFcLong( 0x0 ),	/* 0 */
/* 5988 */	NdrFcShort( 0x7d ),	/* 125 */
/* 5990 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 5992 */	NdrFcShort( 0x1c ),	/* 28 */
/* 5994 */	NdrFcShort( 0x8 ),	/* 8 */
/* 5996 */	0x44,		/* Oi2 Flags:  has return, has ext, */
			0x2,		/* 2 */
/* 5998 */	0x8,		/* 8 */
			0x1,		/* Ext Flags:  new corr desc, */
/* 6000 */	NdrFcShort( 0x0 ),	/* 0 */
/* 6002 */	NdrFcShort( 0x0 ),	/* 0 */
/* 6004 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter regvalue */

/* 6006 */	NdrFcShort( 0x148 ),	/* Flags:  in, base type, simple ref, */
/* 6008 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 6010 */	0xa,		/* FC_FLOAT */
			0x0,		/* 0 */

	/* Return value */

/* 6012 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 6014 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 6016 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure EnumAttachableDevices */

/* 6018 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 6020 */	NdrFcLong( 0x0 ),	/* 0 */
/* 6024 */	NdrFcShort( 0x7e ),	/* 126 */
/* 6026 */	NdrFcShort( 0x20 ),	/* x86 Stack size/offset = 32 */
/* 6028 */	NdrFcShort( 0x24 ),	/* 36 */
/* 6030 */	NdrFcShort( 0x5c ),	/* 92 */
/* 6032 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x7,		/* 7 */
/* 6034 */	0x8,		/* 8 */
			0x7,		/* Ext Flags:  new corr desc, clt corr check, srv corr check, */
/* 6036 */	NdrFcShort( 0x1 ),	/* 1 */
/* 6038 */	NdrFcShort( 0x1 ),	/* 1 */
/* 6040 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter displayName */

/* 6042 */	NdrFcShort( 0x8b ),	/* Flags:  must size, must free, in, by val, */
/* 6044 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 6046 */	NdrFcShort( 0x1c ),	/* Type Offset=28 */

	/* Parameter index */

/* 6048 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 6050 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 6052 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pMonitorID */

/* 6054 */	NdrFcShort( 0x2150 ),	/* Flags:  out, base type, simple ref, srv alloc size=8 */
/* 6056 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 6058 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pDevType */

/* 6060 */	NdrFcShort( 0x158 ),	/* Flags:  in, out, base type, simple ref, */
/* 6062 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 6064 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pDevStatus */

/* 6066 */	NdrFcShort( 0x2150 ),	/* Flags:  out, base type, simple ref, srv alloc size=8 */
/* 6068 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 6070 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pErrorDescription */

/* 6072 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 6074 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 6076 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 6078 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 6080 */	NdrFcShort( 0x1c ),	/* x86 Stack size/offset = 28 */
/* 6082 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetGraphcisRestoreDefault */

/* 6084 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 6086 */	NdrFcLong( 0x0 ),	/* 0 */
/* 6090 */	NdrFcShort( 0x7f ),	/* 127 */
/* 6092 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 6094 */	NdrFcShort( 0x0 ),	/* 0 */
/* 6096 */	NdrFcShort( 0x22 ),	/* 34 */
/* 6098 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x4,		/* 4 */
/* 6100 */	0x8,		/* 8 */
			0x7,		/* Ext Flags:  new corr desc, clt corr check, srv corr check, */
/* 6102 */	NdrFcShort( 0x1 ),	/* 1 */
/* 6104 */	NdrFcShort( 0x1 ),	/* 1 */
/* 6106 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pGraphicsRestoreDefault */

/* 6108 */	NdrFcShort( 0x11b ),	/* Flags:  must size, must free, in, out, simple ref, */
/* 6110 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 6112 */	NdrFcShort( 0x598 ),	/* Type Offset=1432 */

	/* Parameter pExtraErrorCode */

/* 6114 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 6116 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 6118 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 6120 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 6122 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 6124 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 6126 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 6128 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 6130 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetDisplayInformation */

/* 6132 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 6134 */	NdrFcLong( 0x0 ),	/* 0 */
/* 6138 */	NdrFcShort( 0x80 ),	/* 128 */
/* 6140 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 6142 */	NdrFcShort( 0x1c ),	/* 28 */
/* 6144 */	NdrFcShort( 0x3e ),	/* 62 */
/* 6146 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 6148 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 6150 */	NdrFcShort( 0x1 ),	/* 1 */
/* 6152 */	NdrFcShort( 0x0 ),	/* 0 */
/* 6154 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pDisplayInfo */

/* 6156 */	NdrFcShort( 0x158 ),	/* Flags:  in, out, base type, simple ref, */
/* 6158 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 6160 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 6162 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 6164 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 6166 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 6168 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 6170 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 6172 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 6174 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 6176 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 6178 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetIndividualRefreshRate */

/* 6180 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 6182 */	NdrFcLong( 0x0 ),	/* 0 */
/* 6186 */	NdrFcShort( 0x81 ),	/* 129 */
/* 6188 */	NdrFcShort( 0x1c ),	/* x86 Stack size/offset = 28 */
/* 6190 */	NdrFcShort( 0x1c0 ),	/* 448 */
/* 6192 */	NdrFcShort( 0x1da ),	/* 474 */
/* 6194 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x6,		/* 6 */
/* 6196 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 6198 */	NdrFcShort( 0x1 ),	/* 1 */
/* 6200 */	NdrFcShort( 0x0 ),	/* 0 */
/* 6202 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter rr */

/* 6204 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 6206 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 6208 */	NdrFcShort( 0x6e ),	/* Type Offset=110 */

	/* Parameter refreshrate */

/* 6210 */	NdrFcShort( 0x1a ),	/* Flags:  must free, in, out, */
/* 6212 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 6214 */	NdrFcShort( 0x76 ),	/* Type Offset=118 */

	/* Parameter index */

/* 6216 */	NdrFcShort( 0x48 ),	/* Flags:  in, base type, */
/* 6218 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 6220 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Parameter pExtraErrorCode */

/* 6222 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 6224 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 6226 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 6228 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 6230 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 6232 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 6234 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 6236 */	NdrFcShort( 0x18 ),	/* x86 Stack size/offset = 24 */
/* 6238 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetBusInfo */

/* 6240 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 6242 */	NdrFcLong( 0x0 ),	/* 0 */
/* 6246 */	NdrFcShort( 0x82 ),	/* 130 */
/* 6248 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 6250 */	NdrFcShort( 0x0 ),	/* 0 */
/* 6252 */	NdrFcShort( 0x22 ),	/* 34 */
/* 6254 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x4,		/* 4 */
/* 6256 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 6258 */	NdrFcShort( 0x1 ),	/* 1 */
/* 6260 */	NdrFcShort( 0x0 ),	/* 0 */
/* 6262 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBusInfo */

/* 6264 */	NdrFcShort( 0x11b ),	/* Flags:  must size, must free, in, out, simple ref, */
/* 6266 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 6268 */	NdrFcShort( 0x5b0 ),	/* Type Offset=1456 */

	/* Parameter pExtraErrorCode */

/* 6270 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 6272 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 6274 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 6276 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 6278 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 6280 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 6282 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 6284 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 6286 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetBusInfo */

/* 6288 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 6290 */	NdrFcLong( 0x0 ),	/* 0 */
/* 6294 */	NdrFcShort( 0x83 ),	/* 131 */
/* 6296 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 6298 */	NdrFcShort( 0x0 ),	/* 0 */
/* 6300 */	NdrFcShort( 0x22 ),	/* 34 */
/* 6302 */	0x47,		/* Oi2 Flags:  srv must size, clt must size, has return, has ext, */
			0x4,		/* 4 */
/* 6304 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 6306 */	NdrFcShort( 0x1 ),	/* 1 */
/* 6308 */	NdrFcShort( 0x0 ),	/* 0 */
/* 6310 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBusInfo */

/* 6312 */	NdrFcShort( 0x11b ),	/* Flags:  must size, must free, in, out, simple ref, */
/* 6314 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 6316 */	NdrFcShort( 0x5b0 ),	/* Type Offset=1456 */

	/* Parameter pExtraErrorCode */

/* 6318 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 6320 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 6322 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 6324 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 6326 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 6328 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 6330 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 6332 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 6334 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetAviInfoFrameEx */

/* 6336 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 6338 */	NdrFcLong( 0x0 ),	/* 0 */
/* 6342 */	NdrFcShort( 0x84 ),	/* 132 */
/* 6344 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 6346 */	NdrFcShort( 0xb8 ),	/* 184 */
/* 6348 */	NdrFcShort( 0xda ),	/* 218 */
/* 6350 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 6352 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 6354 */	NdrFcShort( 0x1 ),	/* 1 */
/* 6356 */	NdrFcShort( 0x0 ),	/* 0 */
/* 6358 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pAVIFrameInfoEx */

/* 6360 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 6362 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 6364 */	NdrFcShort( 0x5ca ),	/* Type Offset=1482 */

	/* Parameter pExtraErrorCode */

/* 6366 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 6368 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 6370 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 6372 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 6374 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 6376 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 6378 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 6380 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 6382 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetAviInfoFrameEx */

/* 6384 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 6386 */	NdrFcLong( 0x0 ),	/* 0 */
/* 6390 */	NdrFcShort( 0x85 ),	/* 133 */
/* 6392 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 6394 */	NdrFcShort( 0xb8 ),	/* 184 */
/* 6396 */	NdrFcShort( 0xda ),	/* 218 */
/* 6398 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 6400 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 6402 */	NdrFcShort( 0x1 ),	/* 1 */
/* 6404 */	NdrFcShort( 0x0 ),	/* 0 */
/* 6406 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pAVIFrameInfoEx */

/* 6408 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 6410 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 6412 */	NdrFcShort( 0x5ca ),	/* Type Offset=1482 */

	/* Parameter pExtraErrorCode */

/* 6414 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 6416 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 6418 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 6420 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 6422 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 6424 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 6426 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 6428 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 6430 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetBezel */

/* 6432 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 6434 */	NdrFcLong( 0x0 ),	/* 0 */
/* 6438 */	NdrFcShort( 0x86 ),	/* 134 */
/* 6440 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 6442 */	NdrFcShort( 0x80 ),	/* 128 */
/* 6444 */	NdrFcShort( 0xa2 ),	/* 162 */
/* 6446 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 6448 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 6450 */	NdrFcShort( 0x1 ),	/* 1 */
/* 6452 */	NdrFcShort( 0x0 ),	/* 0 */
/* 6454 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBezelConfig */

/* 6456 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 6458 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 6460 */	NdrFcShort( 0x5e8 ),	/* Type Offset=1512 */

	/* Parameter pExtraErrorCode */

/* 6462 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 6464 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 6466 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 6468 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 6470 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 6472 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 6474 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 6476 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 6478 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetBezel */

/* 6480 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 6482 */	NdrFcLong( 0x0 ),	/* 0 */
/* 6486 */	NdrFcShort( 0x87 ),	/* 135 */
/* 6488 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 6490 */	NdrFcShort( 0x80 ),	/* 128 */
/* 6492 */	NdrFcShort( 0xa2 ),	/* 162 */
/* 6494 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 6496 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 6498 */	NdrFcShort( 0x1 ),	/* 1 */
/* 6500 */	NdrFcShort( 0x0 ),	/* 0 */
/* 6502 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pBezelConfig */

/* 6504 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 6506 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 6508 */	NdrFcShort( 0x5e8 ),	/* Type Offset=1512 */

	/* Parameter pExtraErrorCode */

/* 6510 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 6512 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 6514 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 6516 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 6518 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 6520 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 6522 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 6524 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 6526 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetCollageStatus */

/* 6528 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 6530 */	NdrFcLong( 0x0 ),	/* 0 */
/* 6534 */	NdrFcShort( 0x88 ),	/* 136 */
/* 6536 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 6538 */	NdrFcShort( 0x48 ),	/* 72 */
/* 6540 */	NdrFcShort( 0x6a ),	/* 106 */
/* 6542 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 6544 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 6546 */	NdrFcShort( 0x1 ),	/* 1 */
/* 6548 */	NdrFcShort( 0x0 ),	/* 0 */
/* 6550 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pCollageStatus */

/* 6552 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 6554 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 6556 */	NdrFcShort( 0x5fa ),	/* Type Offset=1530 */

	/* Parameter pExtraErrorCode */

/* 6558 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 6560 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 6562 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 6564 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 6566 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 6568 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 6570 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 6572 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 6574 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetCollageStatus */

/* 6576 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 6578 */	NdrFcLong( 0x0 ),	/* 0 */
/* 6582 */	NdrFcShort( 0x89 ),	/* 137 */
/* 6584 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 6586 */	NdrFcShort( 0x48 ),	/* 72 */
/* 6588 */	NdrFcShort( 0x6a ),	/* 106 */
/* 6590 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 6592 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 6594 */	NdrFcShort( 0x1 ),	/* 1 */
/* 6596 */	NdrFcShort( 0x0 ),	/* 0 */
/* 6598 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pCollageStatus */

/* 6600 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 6602 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 6604 */	NdrFcShort( 0x5fa ),	/* Type Offset=1530 */

	/* Parameter pExtraErrorCode */

/* 6606 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 6608 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 6610 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 6612 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 6614 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 6616 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 6618 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 6620 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 6622 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetAudioTopology */

/* 6624 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 6626 */	NdrFcLong( 0x0 ),	/* 0 */
/* 6630 */	NdrFcShort( 0x8a ),	/* 138 */
/* 6632 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 6634 */	NdrFcShort( 0x88 ),	/* 136 */
/* 6636 */	NdrFcShort( 0xaa ),	/* 170 */
/* 6638 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 6640 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 6642 */	NdrFcShort( 0x1 ),	/* 1 */
/* 6644 */	NdrFcShort( 0x0 ),	/* 0 */
/* 6646 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pAudioFeatureInfo */

/* 6648 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 6650 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 6652 */	NdrFcShort( 0x610 ),	/* Type Offset=1552 */

	/* Parameter pExtraErrorCode */

/* 6654 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 6656 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 6658 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 6660 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 6662 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 6664 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 6666 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 6668 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 6670 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetAudioTopology */

/* 6672 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 6674 */	NdrFcLong( 0x0 ),	/* 0 */
/* 6678 */	NdrFcShort( 0x8b ),	/* 139 */
/* 6680 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 6682 */	NdrFcShort( 0x88 ),	/* 136 */
/* 6684 */	NdrFcShort( 0xaa ),	/* 170 */
/* 6686 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 6688 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 6690 */	NdrFcShort( 0x1 ),	/* 1 */
/* 6692 */	NdrFcShort( 0x0 ),	/* 0 */
/* 6694 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pAudioFeatureInfo */

/* 6696 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 6698 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 6700 */	NdrFcShort( 0x610 ),	/* Type Offset=1552 */

	/* Parameter pExtraErrorCode */

/* 6702 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 6704 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 6706 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 6708 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 6710 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 6712 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 6714 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 6716 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 6718 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure EnableAudioWTVideo */

/* 6720 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 6722 */	NdrFcLong( 0x0 ),	/* 0 */
/* 6726 */	NdrFcShort( 0x8c ),	/* 140 */
/* 6728 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 6730 */	NdrFcShort( 0x88 ),	/* 136 */
/* 6732 */	NdrFcShort( 0xaa ),	/* 170 */
/* 6734 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 6736 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 6738 */	NdrFcShort( 0x1 ),	/* 1 */
/* 6740 */	NdrFcShort( 0x0 ),	/* 0 */
/* 6742 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pAudioFeatureInfo */

/* 6744 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 6746 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 6748 */	NdrFcShort( 0x610 ),	/* Type Offset=1552 */

	/* Parameter pExtraErrorCode */

/* 6750 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 6752 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 6754 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 6756 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 6758 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 6760 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 6762 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 6764 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 6766 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure DisableAudioWTVideo */

/* 6768 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 6770 */	NdrFcLong( 0x0 ),	/* 0 */
/* 6774 */	NdrFcShort( 0x8d ),	/* 141 */
/* 6776 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 6778 */	NdrFcShort( 0x88 ),	/* 136 */
/* 6780 */	NdrFcShort( 0xaa ),	/* 170 */
/* 6782 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 6784 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 6786 */	NdrFcShort( 0x1 ),	/* 1 */
/* 6788 */	NdrFcShort( 0x0 ),	/* 0 */
/* 6790 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pAudioFeatureInfo */

/* 6792 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 6794 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 6796 */	NdrFcShort( 0x610 ),	/* Type Offset=1552 */

	/* Parameter pExtraErrorCode */

/* 6798 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 6800 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 6802 */	NdrFcShort( 0x40 ),	/* Type Offset=64 */

	/* Parameter pErrorDescription */

/* 6804 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 6806 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 6808 */	NdrFcShort( 0x36 ),	/* Type Offset=54 */

	/* Return value */

/* 6810 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 6812 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 6814 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

			0x0
        }
    };

static const Display_Util_MIDL_TYPE_FORMAT_STRING Display_Util__MIDL_TypeFormatString =
    {
        0,
        {
			NdrFcShort( 0x0 ),	/* 0 */
/*  2 */	
			0x12, 0x0,	/* FC_UP */
/*  4 */	NdrFcShort( 0xe ),	/* Offset= 14 (18) */
/*  6 */	
			0x1b,		/* FC_CARRAY */
			0x1,		/* 1 */
/*  8 */	NdrFcShort( 0x2 ),	/* 2 */
/* 10 */	0x9,		/* Corr desc: FC_ULONG */
			0x0,		/*  */
/* 12 */	NdrFcShort( 0xfffc ),	/* -4 */
/* 14 */	NdrFcShort( 0x1 ),	/* Corr flags:  early, */
/* 16 */	0x6,		/* FC_SHORT */
			0x5b,		/* FC_END */
/* 18 */	
			0x17,		/* FC_CSTRUCT */
			0x3,		/* 3 */
/* 20 */	NdrFcShort( 0x8 ),	/* 8 */
/* 22 */	NdrFcShort( 0xfff0 ),	/* Offset= -16 (6) */
/* 24 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 26 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 28 */	0xb4,		/* FC_USER_MARSHAL */
			0x83,		/* 131 */
/* 30 */	NdrFcShort( 0x0 ),	/* 0 */
/* 32 */	NdrFcShort( 0x4 ),	/* 4 */
/* 34 */	NdrFcShort( 0x0 ),	/* 0 */
/* 36 */	NdrFcShort( 0xffde ),	/* Offset= -34 (2) */
/* 38 */	
			0x11, 0xc,	/* FC_RP [alloced_on_stack] [simple_pointer] */
/* 40 */	0x8,		/* FC_LONG */
			0x5c,		/* FC_PAD */
/* 42 */	
			0x11, 0x8,	/* FC_RP [simple_pointer] */
/* 44 */	0x8,		/* FC_LONG */
			0x5c,		/* FC_PAD */
/* 46 */	
			0x11, 0x4,	/* FC_RP [alloced_on_stack] */
/* 48 */	NdrFcShort( 0x6 ),	/* Offset= 6 (54) */
/* 50 */	
			0x13, 0x0,	/* FC_OP */
/* 52 */	NdrFcShort( 0xffde ),	/* Offset= -34 (18) */
/* 54 */	0xb4,		/* FC_USER_MARSHAL */
			0x83,		/* 131 */
/* 56 */	NdrFcShort( 0x0 ),	/* 0 */
/* 58 */	NdrFcShort( 0x4 ),	/* 4 */
/* 60 */	NdrFcShort( 0x0 ),	/* 0 */
/* 62 */	NdrFcShort( 0xfff4 ),	/* Offset= -12 (50) */
/* 64 */	
			0x11, 0xc,	/* FC_RP [alloced_on_stack] [simple_pointer] */
/* 66 */	0xd,		/* FC_ENUM16 */
			0x5c,		/* FC_PAD */
/* 68 */	
			0x11, 0x0,	/* FC_RP */
/* 70 */	NdrFcShort( 0x8 ),	/* Offset= 8 (78) */
/* 72 */	
			0x1d,		/* FC_SMFARRAY */
			0x1,		/* 1 */
/* 74 */	NdrFcShort( 0x200 ),	/* 512 */
/* 76 */	0x6,		/* FC_SHORT */
			0x5b,		/* FC_END */
/* 78 */	
			0x15,		/* FC_STRUCT */
			0x1,		/* 1 */
/* 80 */	NdrFcShort( 0x600 ),	/* 1536 */
/* 82 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 84 */	NdrFcShort( 0xfff4 ),	/* Offset= -12 (72) */
/* 86 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 88 */	NdrFcShort( 0xfff0 ),	/* Offset= -16 (72) */
/* 90 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 92 */	NdrFcShort( 0xffec ),	/* Offset= -20 (72) */
/* 94 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 96 */	
			0x11, 0x0,	/* FC_RP */
/* 98 */	NdrFcShort( 0x2 ),	/* Offset= 2 (100) */
/* 100 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 102 */	NdrFcShort( 0x14 ),	/* 20 */
/* 104 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 106 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 108 */	0x8,		/* FC_LONG */
			0x5b,		/* FC_END */
/* 110 */	
			0x15,		/* FC_STRUCT */
			0x1,		/* 1 */
/* 112 */	NdrFcShort( 0x4 ),	/* 4 */
/* 114 */	0x6,		/* FC_SHORT */
			0x6,		/* FC_SHORT */
/* 116 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 118 */	
			0x1d,		/* FC_SMFARRAY */
			0x1,		/* 1 */
/* 120 */	NdrFcShort( 0x50 ),	/* 80 */
/* 122 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 124 */	NdrFcShort( 0xfff2 ),	/* Offset= -14 (110) */
/* 126 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 128 */	
			0x11, 0x0,	/* FC_RP */
/* 130 */	NdrFcShort( 0xffec ),	/* Offset= -20 (110) */
/* 132 */	
			0x11, 0x4,	/* FC_RP [alloced_on_stack] */
/* 134 */	NdrFcShort( 0x2 ),	/* Offset= 2 (136) */
/* 136 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 138 */	NdrFcShort( 0x10 ),	/* 16 */
/* 140 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 142 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 144 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 146 */	
			0x11, 0x0,	/* FC_RP */
/* 148 */	NdrFcShort( 0x8 ),	/* Offset= 8 (156) */
/* 150 */	
			0x1d,		/* FC_SMFARRAY */
			0x0,		/* 0 */
/* 152 */	NdrFcShort( 0x100 ),	/* 256 */
/* 154 */	0x2,		/* FC_CHAR */
			0x5b,		/* FC_END */
/* 156 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 158 */	NdrFcShort( 0x10c ),	/* 268 */
/* 160 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 162 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 164 */	0x0,		/* 0 */
			NdrFcShort( 0xfff1 ),	/* Offset= -15 (150) */
			0x5b,		/* FC_END */
/* 168 */	
			0x11, 0x4,	/* FC_RP [alloced_on_stack] */
/* 170 */	NdrFcShort( 0x2 ),	/* Offset= 2 (172) */
/* 172 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 174 */	NdrFcShort( 0x4 ),	/* 4 */
/* 176 */	0x8,		/* FC_LONG */
			0x5b,		/* FC_END */
/* 178 */	
			0x11, 0x0,	/* FC_RP */
/* 180 */	NdrFcShort( 0x2 ),	/* Offset= 2 (182) */
/* 182 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 184 */	NdrFcShort( 0x60 ),	/* 96 */
/* 186 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 188 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 190 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 192 */	NdrFcShort( 0xffc8 ),	/* Offset= -56 (136) */
/* 194 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 196 */	NdrFcShort( 0xffc4 ),	/* Offset= -60 (136) */
/* 198 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 200 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 202 */	NdrFcShort( 0xff9a ),	/* Offset= -102 (100) */
/* 204 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 206 */	NdrFcShort( 0xff96 ),	/* Offset= -106 (100) */
/* 208 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 210 */	
			0x11, 0x0,	/* FC_RP */
/* 212 */	NdrFcShort( 0x2 ),	/* Offset= 2 (214) */
/* 214 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 216 */	NdrFcShort( 0x34 ),	/* 52 */
/* 218 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 220 */	0x0,		/* 0 */
			NdrFcShort( 0xffab ),	/* Offset= -85 (136) */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 224 */	0x0,		/* 0 */
			NdrFcShort( 0xffa7 ),	/* Offset= -89 (136) */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 228 */	0x0,		/* 0 */
			NdrFcShort( 0xffa3 ),	/* Offset= -93 (136) */
			0x5b,		/* FC_END */
/* 232 */	
			0x11, 0x0,	/* FC_RP */
/* 234 */	NdrFcShort( 0xa ),	/* Offset= 10 (244) */
/* 236 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 238 */	NdrFcShort( 0x8 ),	/* 8 */
/* 240 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 242 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 244 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 246 */	NdrFcShort( 0x44 ),	/* 68 */
/* 248 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 250 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 252 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 254 */	0x0,		/* 0 */
			NdrFcShort( 0xffed ),	/* Offset= -19 (236) */
			0x8,		/* FC_LONG */
/* 258 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 260 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 262 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 264 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 266 */	0x8,		/* FC_LONG */
			0x5b,		/* FC_END */
/* 268 */	
			0x11, 0x0,	/* FC_RP */
/* 270 */	NdrFcShort( 0x2 ),	/* Offset= 2 (272) */
/* 272 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 274 */	NdrFcShort( 0x68 ),	/* 104 */
/* 276 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 278 */	0x0,		/* 0 */
			NdrFcShort( 0xff4d ),	/* Offset= -179 (100) */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 282 */	0x0,		/* 0 */
			NdrFcShort( 0xff49 ),	/* Offset= -183 (100) */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 286 */	0x0,		/* 0 */
			NdrFcShort( 0xff45 ),	/* Offset= -187 (100) */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 290 */	0x0,		/* 0 */
			NdrFcShort( 0xff41 ),	/* Offset= -191 (100) */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 294 */	0x0,		/* 0 */
			NdrFcShort( 0xff3d ),	/* Offset= -195 (100) */
			0x5b,		/* FC_END */
/* 298 */	
			0x11, 0x0,	/* FC_RP */
/* 300 */	NdrFcShort( 0xffc0 ),	/* Offset= -64 (236) */
/* 302 */	
			0x11, 0x0,	/* FC_RP */
/* 304 */	NdrFcShort( 0x24 ),	/* Offset= 36 (340) */
/* 306 */	
			0x1a,		/* FC_BOGUS_STRUCT */
			0x3,		/* 3 */
/* 308 */	NdrFcShort( 0xc ),	/* 12 */
/* 310 */	NdrFcShort( 0x0 ),	/* 0 */
/* 312 */	NdrFcShort( 0x0 ),	/* Offset= 0 (312) */
/* 314 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 316 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 318 */	NdrFcShort( 0xfef8 ),	/* Offset= -264 (54) */
/* 320 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 322 */	
			0x1d,		/* FC_SMFARRAY */
			0x0,		/* 0 */
/* 324 */	NdrFcShort( 0x8 ),	/* 8 */
/* 326 */	0x1,		/* FC_BYTE */
			0x5b,		/* FC_END */
/* 328 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 330 */	NdrFcShort( 0x10 ),	/* 16 */
/* 332 */	0x8,		/* FC_LONG */
			0x6,		/* FC_SHORT */
/* 334 */	0x6,		/* FC_SHORT */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 336 */	0x0,		/* 0 */
			NdrFcShort( 0xfff1 ),	/* Offset= -15 (322) */
			0x5b,		/* FC_END */
/* 340 */	
			0x1a,		/* FC_BOGUS_STRUCT */
			0x3,		/* 3 */
/* 342 */	NdrFcShort( 0x48 ),	/* 72 */
/* 344 */	NdrFcShort( 0x0 ),	/* 0 */
/* 346 */	NdrFcShort( 0x0 ),	/* Offset= 0 (346) */
/* 348 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 350 */	NdrFcShort( 0xffd4 ),	/* Offset= -44 (306) */
/* 352 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 354 */	NdrFcShort( 0xffe6 ),	/* Offset= -26 (328) */
/* 356 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 358 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 360 */	NdrFcShort( 0xffda ),	/* Offset= -38 (322) */
/* 362 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 364 */	0x0,		/* 0 */
			NdrFcShort( 0xffd5 ),	/* Offset= -43 (322) */
			0x8,		/* FC_LONG */
/* 368 */	0xd,		/* FC_ENUM16 */
			0x8,		/* FC_LONG */
/* 370 */	0x8,		/* FC_LONG */
			0x5b,		/* FC_END */
/* 372 */	
			0x11, 0x0,	/* FC_RP */
/* 374 */	NdrFcShort( 0x14 ),	/* Offset= 20 (394) */
/* 376 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 378 */	NdrFcShort( 0xc ),	/* 12 */
/* 380 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 382 */	0x8,		/* FC_LONG */
			0x5b,		/* FC_END */
/* 384 */	
			0x1d,		/* FC_SMFARRAY */
			0x3,		/* 3 */
/* 386 */	NdrFcShort( 0x690 ),	/* 1680 */
/* 388 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 390 */	NdrFcShort( 0xfff2 ),	/* Offset= -14 (376) */
/* 392 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 394 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 396 */	NdrFcShort( 0x69c ),	/* 1692 */
/* 398 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 400 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 402 */	0x0,		/* 0 */
			NdrFcShort( 0xffed ),	/* Offset= -19 (384) */
			0x5b,		/* FC_END */
/* 406 */	
			0x11, 0x0,	/* FC_RP */
/* 408 */	NdrFcShort( 0xc ),	/* Offset= 12 (420) */
/* 410 */	
			0x1d,		/* FC_SMFARRAY */
			0x3,		/* 3 */
/* 412 */	NdrFcShort( 0x4b00 ),	/* 19200 */
/* 414 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 416 */	NdrFcShort( 0xfee8 ),	/* Offset= -280 (136) */
/* 418 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 420 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 422 */	NdrFcShort( 0x4b1c ),	/* 19228 */
/* 424 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 426 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 428 */	0x6,		/* FC_SHORT */
			0x3e,		/* FC_STRUCTPAD2 */
/* 430 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 432 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 434 */	NdrFcShort( 0xffe8 ),	/* Offset= -24 (410) */
/* 436 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 438 */	
			0x11, 0x0,	/* FC_RP */
/* 440 */	NdrFcShort( 0xfe7e ),	/* Offset= -386 (54) */
/* 442 */	
			0x11, 0x0,	/* FC_RP */
/* 444 */	NdrFcShort( 0x8 ),	/* Offset= 8 (452) */
/* 446 */	
			0x1d,		/* FC_SMFARRAY */
			0x3,		/* 3 */
/* 448 */	NdrFcShort( 0x24 ),	/* 36 */
/* 450 */	0x8,		/* FC_LONG */
			0x5b,		/* FC_END */
/* 452 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 454 */	NdrFcShort( 0x2c ),	/* 44 */
/* 456 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 458 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 460 */	NdrFcShort( 0xfff2 ),	/* Offset= -14 (446) */
/* 462 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 464 */	
			0x11, 0x0,	/* FC_RP */
/* 466 */	NdrFcShort( 0x2a ),	/* Offset= 42 (508) */
/* 468 */	
			0x1a,		/* FC_BOGUS_STRUCT */
			0x3,		/* 3 */
/* 470 */	NdrFcShort( 0x1c ),	/* 28 */
/* 472 */	NdrFcShort( 0x0 ),	/* 0 */
/* 474 */	NdrFcShort( 0x0 ),	/* Offset= 0 (474) */
/* 476 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 478 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 480 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 482 */	0x6,		/* FC_SHORT */
			0x3e,		/* FC_STRUCTPAD2 */
/* 484 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 486 */	
			0x1a,		/* FC_BOGUS_STRUCT */
			0x3,		/* 3 */
/* 488 */	NdrFcShort( 0x40 ),	/* 64 */
/* 490 */	NdrFcShort( 0x0 ),	/* 0 */
/* 492 */	NdrFcShort( 0x0 ),	/* Offset= 0 (492) */
/* 494 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 496 */	0x0,		/* 0 */
			NdrFcShort( 0xffe3 ),	/* Offset= -29 (468) */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 500 */	0x0,		/* 0 */
			NdrFcShort( 0xfe93 ),	/* Offset= -365 (136) */
			0x8,		/* FC_LONG */
/* 504 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 506 */	0x8,		/* FC_LONG */
			0x5b,		/* FC_END */
/* 508 */	
			0x1a,		/* FC_BOGUS_STRUCT */
			0x3,		/* 3 */
/* 510 */	NdrFcShort( 0x84 ),	/* 132 */
/* 512 */	NdrFcShort( 0x0 ),	/* 0 */
/* 514 */	NdrFcShort( 0x0 ),	/* Offset= 0 (514) */
/* 516 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 518 */	0x0,		/* 0 */
			NdrFcShort( 0xffdf ),	/* Offset= -33 (486) */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 522 */	0x0,		/* 0 */
			NdrFcShort( 0xffdb ),	/* Offset= -37 (486) */
			0x5b,		/* FC_END */
/* 526 */	
			0x11, 0x0,	/* FC_RP */
/* 528 */	NdrFcShort( 0x2 ),	/* Offset= 2 (530) */
/* 530 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 532 */	NdrFcShort( 0x2c ),	/* 44 */
/* 534 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 536 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 538 */	0x0,		/* 0 */
			NdrFcShort( 0xfe6d ),	/* Offset= -403 (136) */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 542 */	0x0,		/* 0 */
			NdrFcShort( 0xfe69 ),	/* Offset= -407 (136) */
			0x5b,		/* FC_END */
/* 546 */	
			0x11, 0x0,	/* FC_RP */
/* 548 */	NdrFcShort( 0xc ),	/* Offset= 12 (560) */
/* 550 */	
			0x1d,		/* FC_SMFARRAY */
			0x3,		/* 3 */
/* 552 */	NdrFcShort( 0x5dc0 ),	/* 24000 */
/* 554 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 556 */	NdrFcShort( 0xfe38 ),	/* Offset= -456 (100) */
/* 558 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 560 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 562 */	NdrFcShort( 0x5dcc ),	/* 24012 */
/* 564 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 566 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 568 */	0x0,		/* 0 */
			NdrFcShort( 0xffed ),	/* Offset= -19 (550) */
			0x5b,		/* FC_END */
/* 572 */	
			0x11, 0x0,	/* FC_RP */
/* 574 */	NdrFcShort( 0x16 ),	/* Offset= 22 (596) */
/* 576 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 578 */	NdrFcShort( 0x3c ),	/* 60 */
/* 580 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 582 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 584 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 586 */	0xa,		/* FC_FLOAT */
			0x8,		/* FC_LONG */
/* 588 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 590 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 592 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 594 */	0x8,		/* FC_LONG */
			0x5b,		/* FC_END */
/* 596 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 598 */	NdrFcShort( 0x48 ),	/* 72 */
/* 600 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 602 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 604 */	0x0,		/* 0 */
			NdrFcShort( 0xffe3 ),	/* Offset= -29 (576) */
			0x5b,		/* FC_END */
/* 608 */	
			0x11, 0x0,	/* FC_RP */
/* 610 */	NdrFcShort( 0x2 ),	/* Offset= 2 (612) */
/* 612 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 614 */	NdrFcShort( 0x28 ),	/* 40 */
/* 616 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 618 */	0x8,		/* FC_LONG */
			0xa,		/* FC_FLOAT */
/* 620 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 622 */	0x0,		/* 0 */
			NdrFcShort( 0xfdf5 ),	/* Offset= -523 (100) */
			0x5b,		/* FC_END */
/* 626 */	
			0x11, 0x0,	/* FC_RP */
/* 628 */	NdrFcShort( 0x2 ),	/* Offset= 2 (630) */
/* 630 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 632 */	NdrFcShort( 0x58 ),	/* 88 */
/* 634 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 636 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 638 */	NdrFcShort( 0xfde6 ),	/* Offset= -538 (100) */
/* 640 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 642 */	NdrFcShort( 0xffbe ),	/* Offset= -66 (576) */
/* 644 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 646 */	
			0x11, 0x0,	/* FC_RP */
/* 648 */	NdrFcShort( 0xc ),	/* Offset= 12 (660) */
/* 650 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 652 */	NdrFcShort( 0x14 ),	/* 20 */
/* 654 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 656 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 658 */	0xa,		/* FC_FLOAT */
			0x5b,		/* FC_END */
/* 660 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 662 */	NdrFcShort( 0x4c ),	/* 76 */
/* 664 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 666 */	0x0,		/* 0 */
			NdrFcShort( 0xfe51 ),	/* Offset= -431 (236) */
			0x8,		/* FC_LONG */
/* 670 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 672 */	NdrFcShort( 0xffea ),	/* Offset= -22 (650) */
/* 674 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 676 */	NdrFcShort( 0xffe6 ),	/* Offset= -26 (650) */
/* 678 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 680 */	NdrFcShort( 0xffe2 ),	/* Offset= -30 (650) */
/* 682 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 684 */	
			0x11, 0x0,	/* FC_RP */
/* 686 */	NdrFcShort( 0x2 ),	/* Offset= 2 (688) */
/* 688 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 690 */	NdrFcShort( 0x60 ),	/* 96 */
/* 692 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 694 */	0x0,		/* 0 */
			NdrFcShort( 0xfe35 ),	/* Offset= -459 (236) */
			0x8,		/* FC_LONG */
/* 698 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 700 */	NdrFcShort( 0xffce ),	/* Offset= -50 (650) */
/* 702 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 704 */	NdrFcShort( 0xffca ),	/* Offset= -54 (650) */
/* 706 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 708 */	NdrFcShort( 0xffc6 ),	/* Offset= -58 (650) */
/* 710 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 712 */	NdrFcShort( 0xffc2 ),	/* Offset= -62 (650) */
/* 714 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 716 */	
			0x11, 0x0,	/* FC_RP */
/* 718 */	NdrFcShort( 0x2 ),	/* Offset= 2 (720) */
/* 720 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 722 */	NdrFcShort( 0x34 ),	/* 52 */
/* 724 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 726 */	0x0,		/* 0 */
			NdrFcShort( 0xfe15 ),	/* Offset= -491 (236) */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 730 */	0x0,		/* 0 */
			NdrFcShort( 0xfe11 ),	/* Offset= -495 (236) */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 734 */	0x0,		/* 0 */
			NdrFcShort( 0xfe0d ),	/* Offset= -499 (236) */
			0x8,		/* FC_LONG */
/* 738 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 740 */	NdrFcShort( 0xffa6 ),	/* Offset= -90 (650) */
/* 742 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 744 */	
			0x11, 0x0,	/* FC_RP */
/* 746 */	NdrFcShort( 0x2 ),	/* Offset= 2 (748) */
/* 748 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 750 */	NdrFcShort( 0x50 ),	/* 80 */
/* 752 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 754 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 756 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 758 */	0x0,		/* 0 */
			NdrFcShort( 0xfe4b ),	/* Offset= -437 (322) */
			0x8,		/* FC_LONG */
/* 762 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 764 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 766 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 768 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 770 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 772 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 774 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 776 */	
			0x11, 0x0,	/* FC_RP */
/* 778 */	NdrFcShort( 0xfeca ),	/* Offset= -310 (468) */
/* 780 */	
			0x11, 0x0,	/* FC_RP */
/* 782 */	NdrFcShort( 0xfd7a ),	/* Offset= -646 (136) */
/* 784 */	
			0x11, 0x0,	/* FC_RP */
/* 786 */	NdrFcShort( 0xe ),	/* Offset= 14 (800) */
/* 788 */	
			0x1d,		/* FC_SMFARRAY */
			0x1,		/* 1 */
/* 790 */	NdrFcShort( 0x50 ),	/* 80 */
/* 792 */	0x5,		/* FC_WCHAR */
			0x5b,		/* FC_END */
/* 794 */	
			0x1d,		/* FC_SMFARRAY */
			0x3,		/* 3 */
/* 796 */	NdrFcShort( 0x18 ),	/* 24 */
/* 798 */	0x8,		/* FC_LONG */
			0x5b,		/* FC_END */
/* 800 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 802 */	NdrFcShort( 0x78 ),	/* 120 */
/* 804 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 806 */	0x0,		/* 0 */
			NdrFcShort( 0xffed ),	/* Offset= -19 (788) */
			0x8,		/* FC_LONG */
/* 810 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 812 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 814 */	NdrFcShort( 0xffec ),	/* Offset= -20 (794) */
/* 816 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 818 */	
			0x11, 0x0,	/* FC_RP */
/* 820 */	NdrFcShort( 0xfce8 ),	/* Offset= -792 (28) */
/* 822 */	
			0x11, 0x0,	/* FC_RP */
/* 824 */	NdrFcShort( 0x2 ),	/* Offset= 2 (826) */
/* 826 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 828 */	NdrFcShort( 0x38 ),	/* 56 */
/* 830 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 832 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 834 */	0x0,		/* 0 */
			NdrFcShort( 0xff47 ),	/* Offset= -185 (650) */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 838 */	0x0,		/* 0 */
			NdrFcShort( 0xff43 ),	/* Offset= -189 (650) */
			0x8,		/* FC_LONG */
/* 842 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 844 */	
			0x11, 0x0,	/* FC_RP */
/* 846 */	NdrFcShort( 0x2 ),	/* Offset= 2 (848) */
/* 848 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 850 */	NdrFcShort( 0x5c ),	/* 92 */
/* 852 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 854 */	NdrFcShort( 0xff7a ),	/* Offset= -134 (720) */
/* 856 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 858 */	NdrFcShort( 0xfd92 ),	/* Offset= -622 (236) */
/* 860 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 862 */	NdrFcShort( 0xfd8e ),	/* Offset= -626 (236) */
/* 864 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 866 */	NdrFcShort( 0xff28 ),	/* Offset= -216 (650) */
/* 868 */	0x8,		/* FC_LONG */
			0x5b,		/* FC_END */
/* 870 */	
			0x11, 0x0,	/* FC_RP */
/* 872 */	NdrFcShort( 0x30 ),	/* Offset= 48 (920) */
/* 874 */	
			0x1a,		/* FC_BOGUS_STRUCT */
			0x3,		/* 3 */
/* 876 */	NdrFcShort( 0x44 ),	/* 68 */
/* 878 */	NdrFcShort( 0x0 ),	/* 0 */
/* 880 */	NdrFcShort( 0x0 ),	/* Offset= 0 (880) */
/* 882 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 884 */	0x0,		/* 0 */
			NdrFcShort( 0xfe5f ),	/* Offset= -417 (468) */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 888 */	0x0,		/* 0 */
			NdrFcShort( 0xfd0f ),	/* Offset= -753 (136) */
			0x8,		/* FC_LONG */
/* 892 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 894 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 896 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 898 */	
			0x21,		/* FC_BOGUS_ARRAY */
			0x3,		/* 3 */
/* 900 */	NdrFcShort( 0x6 ),	/* 6 */
/* 902 */	NdrFcLong( 0xffffffff ),	/* -1 */
/* 906 */	NdrFcShort( 0x0 ),	/* Corr flags:  */
/* 908 */	NdrFcLong( 0xffffffff ),	/* -1 */
/* 912 */	NdrFcShort( 0x0 ),	/* Corr flags:  */
/* 914 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 916 */	NdrFcShort( 0xffd6 ),	/* Offset= -42 (874) */
/* 918 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 920 */	
			0x1a,		/* FC_BOGUS_STRUCT */
			0x3,		/* 3 */
/* 922 */	NdrFcShort( 0x1a8 ),	/* 424 */
/* 924 */	NdrFcShort( 0x0 ),	/* 0 */
/* 926 */	NdrFcShort( 0x0 ),	/* Offset= 0 (926) */
/* 928 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 930 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 932 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 934 */	NdrFcShort( 0xffdc ),	/* Offset= -36 (898) */
/* 936 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 938 */	
			0x11, 0x0,	/* FC_RP */
/* 940 */	NdrFcShort( 0x2 ),	/* Offset= 2 (942) */
/* 942 */	
			0x1a,		/* FC_BOGUS_STRUCT */
			0x3,		/* 3 */
/* 944 */	NdrFcShort( 0x58 ),	/* 88 */
/* 946 */	NdrFcShort( 0x0 ),	/* 0 */
/* 948 */	NdrFcShort( 0x0 ),	/* Offset= 0 (948) */
/* 950 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 952 */	NdrFcShort( 0xfd34 ),	/* Offset= -716 (236) */
/* 954 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 956 */	0x0,		/* 0 */
			NdrFcShort( 0xfe17 ),	/* Offset= -489 (468) */
			0x8,		/* FC_LONG */
/* 960 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 962 */	0x0,		/* 0 */
			NdrFcShort( 0xfca1 ),	/* Offset= -863 (100) */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 966 */	0x0,		/* 0 */
			NdrFcShort( 0xfc9d ),	/* Offset= -867 (100) */
			0x5b,		/* FC_END */
/* 970 */	
			0x11, 0x0,	/* FC_RP */
/* 972 */	NdrFcShort( 0x18 ),	/* Offset= 24 (996) */
/* 974 */	
			0x21,		/* FC_BOGUS_ARRAY */
			0x3,		/* 3 */
/* 976 */	NdrFcShort( 0x1 ),	/* 1 */
/* 978 */	NdrFcLong( 0xffffffff ),	/* -1 */
/* 982 */	NdrFcShort( 0x0 ),	/* Corr flags:  */
/* 984 */	NdrFcLong( 0xffffffff ),	/* -1 */
/* 988 */	NdrFcShort( 0x0 ),	/* Corr flags:  */
/* 990 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 992 */	NdrFcShort( 0xfdf4 ),	/* Offset= -524 (468) */
/* 994 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 996 */	
			0x1a,		/* FC_BOGUS_STRUCT */
			0x3,		/* 3 */
/* 998 */	NdrFcShort( 0x1d4 ),	/* 468 */
/* 1000 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1002 */	NdrFcShort( 0x0 ),	/* Offset= 0 (1002) */
/* 1004 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1006 */	NdrFcShort( 0xfcfe ),	/* Offset= -770 (236) */
/* 1008 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1010 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1012 */	NdrFcShort( 0xff8e ),	/* Offset= -114 (898) */
/* 1014 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1016 */	0x6,		/* FC_SHORT */
			0x3e,		/* FC_STRUCTPAD2 */
/* 1018 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 1020 */	0x0,		/* 0 */
			NdrFcShort( 0xffd1 ),	/* Offset= -47 (974) */
			0x5b,		/* FC_END */
/* 1024 */	
			0x11, 0x0,	/* FC_RP */
/* 1026 */	NdrFcShort( 0x12 ),	/* Offset= 18 (1044) */
/* 1028 */	
			0x1d,		/* FC_SMFARRAY */
			0x3,		/* 3 */
/* 1030 */	NdrFcShort( 0xc ),	/* 12 */
/* 1032 */	0xa,		/* FC_FLOAT */
			0x5b,		/* FC_END */
/* 1034 */	
			0x1d,		/* FC_SMFARRAY */
			0x3,		/* 3 */
/* 1036 */	NdrFcShort( 0x24 ),	/* 36 */
/* 1038 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1040 */	NdrFcShort( 0xfff4 ),	/* Offset= -12 (1028) */
/* 1042 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 1044 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 1046 */	NdrFcShort( 0x40 ),	/* 64 */
/* 1048 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1050 */	NdrFcShort( 0xfcd2 ),	/* Offset= -814 (236) */
/* 1052 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1054 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1056 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1058 */	NdrFcShort( 0xffe8 ),	/* Offset= -24 (1034) */
/* 1060 */	0x8,		/* FC_LONG */
			0x5b,		/* FC_END */
/* 1062 */	
			0x11, 0x0,	/* FC_RP */
/* 1064 */	NdrFcShort( 0x16 ),	/* Offset= 22 (1086) */
/* 1066 */	
			0x1a,		/* FC_BOGUS_STRUCT */
			0x3,		/* 3 */
/* 1068 */	NdrFcShort( 0x4c ),	/* 76 */
/* 1070 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1072 */	NdrFcShort( 0x0 ),	/* Offset= 0 (1072) */
/* 1074 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1076 */	NdrFcShort( 0xffd6 ),	/* Offset= -42 (1034) */
/* 1078 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1080 */	NdrFcShort( 0xffd2 ),	/* Offset= -46 (1034) */
/* 1082 */	0x2,		/* FC_CHAR */
			0x3f,		/* FC_STRUCTPAD3 */
/* 1084 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 1086 */	
			0x1a,		/* FC_BOGUS_STRUCT */
			0x3,		/* 3 */
/* 1088 */	NdrFcShort( 0x5c ),	/* 92 */
/* 1090 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1092 */	NdrFcShort( 0x0 ),	/* Offset= 0 (1092) */
/* 1094 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1096 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1098 */	NdrFcShort( 0xffe0 ),	/* Offset= -32 (1066) */
/* 1100 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1102 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 1104 */	
			0x11, 0x0,	/* FC_RP */
/* 1106 */	NdrFcShort( 0x2 ),	/* Offset= 2 (1108) */
/* 1108 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 1110 */	NdrFcShort( 0xc8 ),	/* 200 */
/* 1112 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1114 */	NdrFcShort( 0xfc92 ),	/* Offset= -878 (236) */
/* 1116 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1118 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1120 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1122 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1124 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1126 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1128 */	0xa,		/* FC_FLOAT */
			0x8,		/* FC_LONG */
/* 1130 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1132 */	0x8,		/* FC_LONG */
			0xa,		/* FC_FLOAT */
/* 1134 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1136 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1138 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1140 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1142 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1144 */	0x8,		/* FC_LONG */
			0xa,		/* FC_FLOAT */
/* 1146 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1148 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1150 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1152 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1154 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1156 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1158 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1160 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1162 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1164 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 1166 */	
			0x11, 0x0,	/* FC_RP */
/* 1168 */	NdrFcShort( 0x2 ),	/* Offset= 2 (1170) */
/* 1170 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 1172 */	NdrFcShort( 0xf0 ),	/* 240 */
/* 1174 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1176 */	NdrFcShort( 0xfc54 ),	/* Offset= -940 (236) */
/* 1178 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1180 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1182 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1184 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1186 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1188 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1190 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1192 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1194 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1196 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1198 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1200 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1202 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1204 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1206 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1208 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1210 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1212 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1214 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1216 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1218 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1220 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1222 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1224 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1226 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1228 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1230 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1232 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1234 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1236 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 1238 */	
			0x11, 0x0,	/* FC_RP */
/* 1240 */	NdrFcShort( 0x8 ),	/* Offset= 8 (1248) */
/* 1242 */	
			0x1d,		/* FC_SMFARRAY */
			0x0,		/* 0 */
/* 1244 */	NdrFcShort( 0x10 ),	/* 16 */
/* 1246 */	0x1,		/* FC_BYTE */
			0x5b,		/* FC_END */
/* 1248 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 1250 */	NdrFcShort( 0x20 ),	/* 32 */
/* 1252 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1254 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1256 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1258 */	NdrFcShort( 0xfff0 ),	/* Offset= -16 (1242) */
/* 1260 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 1262 */	
			0x11, 0x0,	/* FC_RP */
/* 1264 */	NdrFcShort( 0x14 ),	/* Offset= 20 (1284) */
/* 1266 */	
			0x1d,		/* FC_SMFARRAY */
			0x0,		/* 0 */
/* 1268 */	NdrFcShort( 0x1c ),	/* 28 */
/* 1270 */	0x1,		/* FC_BYTE */
			0x5b,		/* FC_END */
/* 1272 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 1274 */	NdrFcShort( 0x24 ),	/* 36 */
/* 1276 */	0x6,		/* FC_SHORT */
			0x3e,		/* FC_STRUCTPAD2 */
/* 1278 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 1280 */	0x0,		/* 0 */
			NdrFcShort( 0xfff1 ),	/* Offset= -15 (1266) */
			0x5b,		/* FC_END */
/* 1284 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 1286 */	NdrFcShort( 0x34 ),	/* 52 */
/* 1288 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1290 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1292 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1294 */	NdrFcShort( 0xffea ),	/* Offset= -22 (1272) */
/* 1296 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 1298 */	
			0x11, 0x0,	/* FC_RP */
/* 1300 */	NdrFcShort( 0x18 ),	/* Offset= 24 (1324) */
/* 1302 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 1304 */	NdrFcShort( 0x18 ),	/* 24 */
/* 1306 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1308 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1310 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1312 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 1314 */	
			0x1d,		/* FC_SMFARRAY */
			0x3,		/* 3 */
/* 1316 */	NdrFcShort( 0xd20 ),	/* 3360 */
/* 1318 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1320 */	NdrFcShort( 0xffee ),	/* Offset= -18 (1302) */
/* 1322 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 1324 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 1326 */	NdrFcShort( 0xd34 ),	/* 3380 */
/* 1328 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1330 */	NdrFcShort( 0xfbba ),	/* Offset= -1094 (236) */
/* 1332 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1334 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 1336 */	0x0,		/* 0 */
			NdrFcShort( 0xffe9 ),	/* Offset= -23 (1314) */
			0x5b,		/* FC_END */
/* 1340 */	
			0x11, 0x0,	/* FC_RP */
/* 1342 */	NdrFcShort( 0x2 ),	/* Offset= 2 (1344) */
/* 1344 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 1346 */	NdrFcShort( 0x18 ),	/* 24 */
/* 1348 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1350 */	NdrFcShort( 0xfba6 ),	/* Offset= -1114 (236) */
/* 1352 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1354 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1356 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 1358 */	
			0x11, 0x0,	/* FC_RP */
/* 1360 */	NdrFcShort( 0x2 ),	/* Offset= 2 (1362) */
/* 1362 */	
			0x1a,		/* FC_BOGUS_STRUCT */
			0x3,		/* 3 */
/* 1364 */	NdrFcShort( 0x10 ),	/* 16 */
/* 1366 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1368 */	NdrFcShort( 0x0 ),	/* Offset= 0 (1368) */
/* 1370 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1372 */	0x8,		/* FC_LONG */
			0x3,		/* FC_SMALL */
/* 1374 */	0x3f,		/* FC_STRUCTPAD3 */
			0x5b,		/* FC_END */
/* 1376 */	
			0x11, 0x0,	/* FC_RP */
/* 1378 */	NdrFcShort( 0x2 ),	/* Offset= 2 (1380) */
/* 1380 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 1382 */	NdrFcShort( 0x54 ),	/* 84 */
/* 1384 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1386 */	NdrFcShort( 0xfb82 ),	/* Offset= -1150 (236) */
/* 1388 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1390 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1392 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1394 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1396 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1398 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1400 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1402 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1404 */	0xa,		/* FC_FLOAT */
			0xa,		/* FC_FLOAT */
/* 1406 */	0xa,		/* FC_FLOAT */
			0x5b,		/* FC_END */
/* 1408 */	
			0x11, 0x8,	/* FC_RP [simple_pointer] */
/* 1410 */	0xa,		/* FC_FLOAT */
			0x5c,		/* FC_PAD */
/* 1412 */	
			0x11, 0x0,	/* FC_RP */
/* 1414 */	NdrFcShort( 0x12 ),	/* Offset= 18 (1432) */
/* 1416 */	
			0x1a,		/* FC_BOGUS_STRUCT */
			0x3,		/* 3 */
/* 1418 */	NdrFcShort( 0x14 ),	/* 20 */
/* 1420 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1422 */	NdrFcShort( 0x0 ),	/* Offset= 0 (1422) */
/* 1424 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1426 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1428 */	NdrFcShort( 0xfb9e ),	/* Offset= -1122 (306) */
/* 1430 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 1432 */	
			0x1a,		/* FC_BOGUS_STRUCT */
			0x3,		/* 3 */
/* 1434 */	NdrFcShort( 0x14 ),	/* 20 */
/* 1436 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1438 */	NdrFcShort( 0x0 ),	/* Offset= 0 (1438) */
/* 1440 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1442 */	NdrFcShort( 0xffe6 ),	/* Offset= -26 (1416) */
/* 1444 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 1446 */	
			0x11, 0x0,	/* FC_RP */
/* 1448 */	NdrFcShort( 0x8 ),	/* Offset= 8 (1456) */
/* 1450 */	
			0x1d,		/* FC_SMFARRAY */
			0x0,		/* 0 */
/* 1452 */	NdrFcShort( 0x80 ),	/* 128 */
/* 1454 */	0x1,		/* FC_BYTE */
			0x5b,		/* FC_END */
/* 1456 */	
			0x1a,		/* FC_BOGUS_STRUCT */
			0x3,		/* 3 */
/* 1458 */	NdrFcShort( 0x9c ),	/* 156 */
/* 1460 */	NdrFcShort( 0x0 ),	/* 0 */
/* 1462 */	NdrFcShort( 0x0 ),	/* Offset= 0 (1462) */
/* 1464 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1466 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1468 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1470 */	0x1,		/* FC_BYTE */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 1472 */	0x0,		/* 0 */
			NdrFcShort( 0xffe9 ),	/* Offset= -23 (1450) */
			0x3f,		/* FC_STRUCTPAD3 */
/* 1476 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 1478 */	
			0x11, 0x0,	/* FC_RP */
/* 1480 */	NdrFcShort( 0x2 ),	/* Offset= 2 (1482) */
/* 1482 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 1484 */	NdrFcShort( 0x64 ),	/* 100 */
/* 1486 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1488 */	NdrFcShort( 0xfb1c ),	/* Offset= -1252 (236) */
/* 1490 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1492 */	NdrFcShort( 0xfd18 ),	/* Offset= -744 (748) */
/* 1494 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1496 */	0x8,		/* FC_LONG */
			0x5b,		/* FC_END */
/* 1498 */	
			0x11, 0x0,	/* FC_RP */
/* 1500 */	NdrFcShort( 0xc ),	/* Offset= 12 (1512) */
/* 1502 */	
			0x1d,		/* FC_SMFARRAY */
			0x3,		/* 3 */
/* 1504 */	NdrFcShort( 0x20 ),	/* 32 */
/* 1506 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1508 */	NdrFcShort( 0xfaa4 ),	/* Offset= -1372 (136) */
/* 1510 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 1512 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 1514 */	NdrFcShort( 0x2c ),	/* 44 */
/* 1516 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1518 */	NdrFcShort( 0xfafe ),	/* Offset= -1282 (236) */
/* 1520 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 1522 */	0x0,		/* 0 */
			NdrFcShort( 0xffeb ),	/* Offset= -21 (1502) */
			0x5b,		/* FC_END */
/* 1526 */	
			0x11, 0x0,	/* FC_RP */
/* 1528 */	NdrFcShort( 0x2 ),	/* Offset= 2 (1530) */
/* 1530 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 1532 */	NdrFcShort( 0x14 ),	/* 20 */
/* 1534 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1536 */	NdrFcShort( 0xfaec ),	/* Offset= -1300 (236) */
/* 1538 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1540 */	0x8,		/* FC_LONG */
			0x5b,		/* FC_END */
/* 1542 */	
			0x11, 0x0,	/* FC_RP */
/* 1544 */	NdrFcShort( 0x8 ),	/* Offset= 8 (1552) */
/* 1546 */	
			0x1d,		/* FC_SMFARRAY */
			0x3,		/* 3 */
/* 1548 */	NdrFcShort( 0xc ),	/* 12 */
/* 1550 */	0x8,		/* FC_LONG */
			0x5b,		/* FC_END */
/* 1552 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 1554 */	NdrFcShort( 0x34 ),	/* 52 */
/* 1556 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1558 */	NdrFcShort( 0xfad6 ),	/* Offset= -1322 (236) */
/* 1560 */	0x8,		/* FC_LONG */
			0x4c,		/* FC_EMBEDDED_COMPLEX */
/* 1562 */	0x0,		/* 0 */
			NdrFcShort( 0xffef ),	/* Offset= -17 (1546) */
			0x8,		/* FC_LONG */
/* 1566 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 1568 */	NdrFcShort( 0xffea ),	/* Offset= -22 (1546) */
/* 1570 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 1572 */	0x8,		/* FC_LONG */
			0x5b,		/* FC_END */

			0x0
        }
    };

static const USER_MARSHAL_ROUTINE_QUADRUPLE UserMarshalRoutines[ WIRE_MARSHAL_TABLE_SIZE ] = 
        {
            
            {
            BSTR_UserSize
            ,BSTR_UserMarshal
            ,BSTR_UserUnmarshal
            ,BSTR_UserFree
            }

        };



/* Object interface: IUnknown, ver. 0.0,
   GUID={0x00000000,0x0000,0x0000,{0xC0,0x00,0x00,0x00,0x00,0x00,0x00,0x46}} */


/* Object interface: IDispatch, ver. 0.0,
   GUID={0x00020400,0x0000,0x0000,{0xC0,0x00,0x00,0x00,0x00,0x00,0x00,0x46}} */


/* Object interface: IDisplayUtil, ver. 0.0,
   GUID={0xEA9FB107,0x8829,0x4672,{0xB1,0x6C,0x9E,0x5B,0x0E,0xEF,0xDE,0x17}} */

#pragma code_seg(".orpc")
static const unsigned short IDisplayUtil_FormatStringOffsetTable[] =
    {
    (unsigned short) -1,
    (unsigned short) -1,
    (unsigned short) -1,
    (unsigned short) -1,
    0,
    66,
    126,
    180,
    228,
    282,
    336,
    390,
    444,
    492,
    546,
    600,
    654,
    702,
    750,
    804,
    852,
    906,
    954,
    1002,
    1068,
    1116,
    1182,
    1236,
    1290,
    1344,
    1398,
    1452,
    1512,
    1572,
    1620,
    1668,
    1716,
    1764,
    1812,
    1860,
    1908,
    1956,
    2004,
    2052,
    2100,
    2148,
    2196,
    2244,
    2292,
    2340,
    2388,
    2436,
    2484,
    2532,
    2580,
    2646,
    2694,
    2742,
    2790,
    2838,
    2916,
    2964,
    3012,
    3060,
    3108,
    3156,
    3204,
    3252,
    3300,
    3348,
    3396,
    3444,
    3492,
    3540,
    3588,
    3630,
    3690,
    3816,
    3864,
    3906,
    3954,
    4002,
    4050,
    4098,
    4146,
    4194,
    4242,
    4290,
    4338,
    4386,
    4440,
    4500,
    4560,
    4608,
    4674,
    4722,
    4770,
    4818,
    4866,
    4914,
    4962,
    5010,
    5058,
    5106,
    5154,
    5202,
    5250,
    5298,
    5346,
    5394,
    5442,
    5490,
    5538,
    5586,
    5634,
    5682,
    5730,
    5778,
    5826,
    5874,
    5910,
    5946,
    5982,
    6018,
    6084,
    6132,
    6180,
    6240,
    6288,
    6336,
    6384,
    6432,
    6480,
    6528,
    6576,
    6624,
    6672,
    6720,
    6768
    };

static const MIDL_STUBLESS_PROXY_INFO IDisplayUtil_ProxyInfo =
    {
    &Object_StubDesc,
    Display_Util__MIDL_ProcFormatString.Format,
    &IDisplayUtil_FormatStringOffsetTable[-3],
    0,
    0,
    0
    };


static const MIDL_SERVER_INFO IDisplayUtil_ServerInfo = 
    {
    &Object_StubDesc,
    0,
    Display_Util__MIDL_ProcFormatString.Format,
    &IDisplayUtil_FormatStringOffsetTable[-3],
    0,
    0,
    0,
    0};
CINTERFACE_PROXY_VTABLE(142) _IDisplayUtilProxyVtbl = 
{
    &IDisplayUtil_ProxyInfo,
    &IID_IDisplayUtil,
    IUnknown_QueryInterface_Proxy,
    IUnknown_AddRef_Proxy,
    IUnknown_Release_Proxy ,
    0 /* IDispatch::GetTypeInfoCount */ ,
    0 /* IDispatch::GetTypeInfo */ ,
    0 /* IDispatch::GetIDsOfNames */ ,
    0 /* IDispatch_Invoke_Proxy */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetDeviceStatus */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::EnumActiveDisplay */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetMonitorID */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SingleDisplaySwitch */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::DualDisplayClone */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::DualDisplayTwin */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::ExtendedDesktop */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::EnableRotation */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::DisableRotation */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::IsRotationEnabled */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetRotationAngle */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::Rotate */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetFullScreen */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetScreenCentered */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::EnablePortraitPolicy */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::DisablePortraitPolicy */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::EnableLandscapePolicy */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::DisableLandscapePolicy */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetSupportedEvents */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::RegisterEvent */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::UnRegisterEvent */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetAspectScalingCapabilities */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetAspectPreference */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetGammaRamp */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetGammaRamp */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::PopulateSetValidGamma */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::PopulateSetInvalidGamma */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetCloneRefreshRate */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetCloneView */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetDVMTData */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetEDIDData */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::IsOverlayOn */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetOverScanData */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetOverScanData */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::IsDownScalingSupported */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::IsDownScalingEnabled */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::EnableDownScaling */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::DisableDownScaling */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetConfiguration */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetConfiguration */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::Overlay_Set */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::Overlay_Get */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::CVT_Get */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SDVO_Set */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetSupportedConfiguration */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetGraphicsModes */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetSupportedGraphicsModes */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetVBIOSVersion */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetGammaBrightnessContrast */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetGammaBrightnessContrast */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetSystemConfigurationAll */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetSystemConfiguration */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetSystemConfiguration */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetMediaScalar */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetMediaScalar */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::InitilizeRemoveCustomModeArray */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::RemoveCustomMode */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::AddAdvancedCustomMode */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::AddBasicCustomMode */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetCustomModeTiming */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetCustomModeList */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetMediaScaling */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetMediaScaling */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetMediaColor */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetMediaColor */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetVideoQuality */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetVideoQuality */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetAviInfoFrame */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetAviInfoFrame */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetAttachedDevices */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::EnumAttachedDevices */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::ChangeActiveDevices */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::DummyFunction */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetCurrentConfig */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::IsWOW64 */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::DoEscape */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetHueSaturation */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetHueSaturation */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetVideoQualityExtended */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetVideoQualityExtended */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetSystemConfigDataNViews */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetSystemConfigDataNViews */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetScaling */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetScaling */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::QueryforVideoModeList */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetIndividualVideoMode */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetTriClone */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetTriExtended */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetGamutData */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetGamutData */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetCSCData */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetCSCData */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetVideoQualityExtended2 */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetVideoQualityExtended2 */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetMediaColorExtended2 */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetMediaColorExtended2 */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetAuxInfo */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetAuxInfo */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetSourceHdmiGBDdata */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetSourceHdmiGBDdata */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetSupportedConfigurationEx */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetColorGamut */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetColorGamut */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetXvYcc */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetXvYcc */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetYcBcr */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetYcBcr */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetGOPVersion */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetVideoModeListEx */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetVideoGamutMapping */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetVideoGamutMapping */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetChipSetInformation */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetVideoFeatureSupportList */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetMediaScalingEx2 */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::GetMediaScalingEx2 */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::ReadRegistryEnableNLAS */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::ReadRegistryNLASVerticalCrop */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::ReadRegistryNLASHLinearRegion */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::ReadRegistryNLASNonLinearCrop */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::EnumAttachableDevices */ ,
    (void *) (INT_PTR) -1 /* IDisplayUtil::SetGraphcisRestoreDefault */ ,
    IDisplayUtil_GetDisplayInformation_Proxy ,
    IDisplayUtil_GetIndividualRefreshRate_Proxy ,
    IDisplayUtil_GetBusInfo_Proxy ,
    IDisplayUtil_SetBusInfo_Proxy ,
    IDisplayUtil_GetAviInfoFrameEx_Proxy ,
    IDisplayUtil_SetAviInfoFrameEx_Proxy ,
    IDisplayUtil_GetBezel_Proxy ,
    IDisplayUtil_SetBezel_Proxy ,
    IDisplayUtil_GetCollageStatus_Proxy ,
    IDisplayUtil_SetCollageStatus_Proxy ,
    IDisplayUtil_SetAudioTopology_Proxy ,
    IDisplayUtil_GetAudioTopology_Proxy ,
    IDisplayUtil_EnableAudioWTVideo_Proxy ,
    IDisplayUtil_DisableAudioWTVideo_Proxy
};


static const PRPC_STUB_FUNCTION IDisplayUtil_table[] =
{
    STUB_FORWARDING_FUNCTION,
    STUB_FORWARDING_FUNCTION,
    STUB_FORWARDING_FUNCTION,
    STUB_FORWARDING_FUNCTION,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2
};

CInterfaceStubVtbl _IDisplayUtilStubVtbl =
{
    &IID_IDisplayUtil,
    &IDisplayUtil_ServerInfo,
    142,
    &IDisplayUtil_table[-3],
    CStdStubBuffer_DELEGATING_METHODS
};

static const MIDL_STUB_DESC Object_StubDesc = 
    {
    0,
    NdrOleAllocate,
    NdrOleFree,
    0,
    0,
    0,
    0,
    0,
    Display_Util__MIDL_TypeFormatString.Format,
    1, /* -error bounds_check flag */
    0x50002, /* Ndr library version */
    0,
    0x8000253, /* MIDL Version 8.0.595 */
    0,
    UserMarshalRoutines,
    0,  /* notify & notify_flag routine table */
    0x1, /* MIDL flag */
    0, /* cs routines */
    0,   /* proxy/server info */
    0
    };

const CInterfaceProxyVtbl * const _Display_Util_ProxyVtblList[] = 
{
    ( CInterfaceProxyVtbl *) &_IDisplayUtilProxyVtbl,
    0
};

const CInterfaceStubVtbl * const _Display_Util_StubVtblList[] = 
{
    ( CInterfaceStubVtbl *) &_IDisplayUtilStubVtbl,
    0
};

PCInterfaceName const _Display_Util_InterfaceNamesList[] = 
{
    "IDisplayUtil",
    0
};

const IID *  const _Display_Util_BaseIIDList[] = 
{
    &IID_IDispatch,
    0
};


#define _Display_Util_CHECK_IID(n)	IID_GENERIC_CHECK_IID( _Display_Util, pIID, n)

int __stdcall _Display_Util_IID_Lookup( const IID * pIID, int * pIndex )
{
    
    if(!_Display_Util_CHECK_IID(0))
        {
        *pIndex = 0;
        return 1;
        }

    return 0;
}

const ExtendedProxyFileInfo Display_Util_ProxyFileInfo = 
{
    (PCInterfaceProxyVtblList *) & _Display_Util_ProxyVtblList,
    (PCInterfaceStubVtblList *) & _Display_Util_StubVtblList,
    (const PCInterfaceName * ) & _Display_Util_InterfaceNamesList,
    (const IID ** ) & _Display_Util_BaseIIDList,
    & _Display_Util_IID_Lookup, 
    1,
    2,
    0, /* table of [async_uuid] interfaces */
    0, /* Filler1 */
    0, /* Filler2 */
    0  /* Filler3 */
};
#pragma optimize("", on )
#if _MSC_VER >= 1200
#pragma warning(pop)
#endif


#endif /* !defined(_M_IA64) && !defined(_M_AMD64) && !defined(_ARM_) */

