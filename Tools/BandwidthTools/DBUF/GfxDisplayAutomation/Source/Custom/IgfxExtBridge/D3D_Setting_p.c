

/* this ALWAYS GENERATED file contains the proxy stub code */


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


#include "D3D_Setting.h"

#define TYPE_FORMAT_STRING_SIZE   105                               
#define PROC_FORMAT_STRING_SIZE   193                               
#define EXPR_FORMAT_STRING_SIZE   1                                 
#define TRANSMIT_AS_TABLE_SIZE    0            
#define WIRE_MARSHAL_TABLE_SIZE   1            

typedef struct _D3D_Setting_MIDL_TYPE_FORMAT_STRING
    {
    short          Pad;
    unsigned char  Format[ TYPE_FORMAT_STRING_SIZE ];
    } D3D_Setting_MIDL_TYPE_FORMAT_STRING;

typedef struct _D3D_Setting_MIDL_PROC_FORMAT_STRING
    {
    short          Pad;
    unsigned char  Format[ PROC_FORMAT_STRING_SIZE ];
    } D3D_Setting_MIDL_PROC_FORMAT_STRING;

typedef struct _D3D_Setting_MIDL_EXPR_FORMAT_STRING
    {
    long          Pad;
    unsigned char  Format[ EXPR_FORMAT_STRING_SIZE ];
    } D3D_Setting_MIDL_EXPR_FORMAT_STRING;


static const RPC_SYNTAX_IDENTIFIER  _RpcTransferSyntax = 
{{0x8A885D04,0x1CEB,0x11C9,{0x9F,0xE8,0x08,0x00,0x2B,0x10,0x48,0x60}},{2,0}};


extern const D3D_Setting_MIDL_TYPE_FORMAT_STRING D3D_Setting__MIDL_TypeFormatString;
extern const D3D_Setting_MIDL_PROC_FORMAT_STRING D3D_Setting__MIDL_ProcFormatString;
extern const D3D_Setting_MIDL_EXPR_FORMAT_STRING D3D_Setting__MIDL_ExprFormatString;


extern const MIDL_STUB_DESC Object_StubDesc;


extern const MIDL_SERVER_INFO ID3DSetting_ServerInfo;
extern const MIDL_STUBLESS_PROXY_INFO ID3DSetting_ProxyInfo;


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


static const D3D_Setting_MIDL_PROC_FORMAT_STRING D3D_Setting__MIDL_ProcFormatString =
    {
        0,
        {

	/* Procedure GetD3DInfo */

			0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/*  2 */	NdrFcLong( 0x0 ),	/* 0 */
/*  6 */	NdrFcShort( 0x7 ),	/* 7 */
/*  8 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 10 */	NdrFcShort( 0x50 ),	/* 80 */
/* 12 */	NdrFcShort( 0x72 ),	/* 114 */
/* 14 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 16 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 18 */	NdrFcShort( 0x1 ),	/* 1 */
/* 20 */	NdrFcShort( 0x0 ),	/* 0 */
/* 22 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pD3D */

/* 24 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 26 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 28 */	NdrFcShort( 0x6 ),	/* Type Offset=6 */

	/* Parameter pExtraErrorCode */

/* 30 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 32 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 34 */	NdrFcShort( 0x16 ),	/* Type Offset=22 */

	/* Parameter pErrorDescription */

/* 36 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 38 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 40 */	NdrFcShort( 0x38 ),	/* Type Offset=56 */

	/* Return value */

/* 42 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 44 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 46 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetD3DInfo */

/* 48 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 50 */	NdrFcLong( 0x0 ),	/* 0 */
/* 54 */	NdrFcShort( 0x8 ),	/* 8 */
/* 56 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 58 */	NdrFcShort( 0x50 ),	/* 80 */
/* 60 */	NdrFcShort( 0x72 ),	/* 114 */
/* 62 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 64 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 66 */	NdrFcShort( 0x1 ),	/* 1 */
/* 68 */	NdrFcShort( 0x0 ),	/* 0 */
/* 70 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pD3D */

/* 72 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 74 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 76 */	NdrFcShort( 0x6 ),	/* Type Offset=6 */

	/* Parameter pExtraErrorCode */

/* 78 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 80 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 82 */	NdrFcShort( 0x16 ),	/* Type Offset=22 */

	/* Parameter pErrorDescription */

/* 84 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 86 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 88 */	NdrFcShort( 0x38 ),	/* Type Offset=56 */

	/* Return value */

/* 90 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 92 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 94 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure GetD3DInfoEx */

/* 96 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 98 */	NdrFcLong( 0x0 ),	/* 0 */
/* 102 */	NdrFcShort( 0x9 ),	/* 9 */
/* 104 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 106 */	NdrFcShort( 0x80 ),	/* 128 */
/* 108 */	NdrFcShort( 0xa2 ),	/* 162 */
/* 110 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 112 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 114 */	NdrFcShort( 0x1 ),	/* 1 */
/* 116 */	NdrFcShort( 0x0 ),	/* 0 */
/* 118 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pD3D */

/* 120 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 122 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 124 */	NdrFcShort( 0x4e ),	/* Type Offset=78 */

	/* Parameter pExtraErrorCode */

/* 126 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 128 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 130 */	NdrFcShort( 0x16 ),	/* Type Offset=22 */

	/* Parameter pErrorDescription */

/* 132 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 134 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 136 */	NdrFcShort( 0x38 ),	/* Type Offset=56 */

	/* Return value */

/* 138 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 140 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 142 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

	/* Procedure SetD3DInfoEx */

/* 144 */	0x33,		/* FC_AUTO_HANDLE */
			0x6c,		/* Old Flags:  object, Oi2 */
/* 146 */	NdrFcLong( 0x0 ),	/* 0 */
/* 150 */	NdrFcShort( 0xa ),	/* 10 */
/* 152 */	NdrFcShort( 0x14 ),	/* x86 Stack size/offset = 20 */
/* 154 */	NdrFcShort( 0x80 ),	/* 128 */
/* 156 */	NdrFcShort( 0xa2 ),	/* 162 */
/* 158 */	0x45,		/* Oi2 Flags:  srv must size, has return, has ext, */
			0x4,		/* 4 */
/* 160 */	0x8,		/* 8 */
			0x3,		/* Ext Flags:  new corr desc, clt corr check, */
/* 162 */	NdrFcShort( 0x1 ),	/* 1 */
/* 164 */	NdrFcShort( 0x0 ),	/* 0 */
/* 166 */	NdrFcShort( 0x0 ),	/* 0 */

	/* Parameter pD3D */

/* 168 */	NdrFcShort( 0x11a ),	/* Flags:  must free, in, out, simple ref, */
/* 170 */	NdrFcShort( 0x4 ),	/* x86 Stack size/offset = 4 */
/* 172 */	NdrFcShort( 0x4e ),	/* Type Offset=78 */

	/* Parameter pExtraErrorCode */

/* 174 */	NdrFcShort( 0x2010 ),	/* Flags:  out, srv alloc size=8 */
/* 176 */	NdrFcShort( 0x8 ),	/* x86 Stack size/offset = 8 */
/* 178 */	NdrFcShort( 0x16 ),	/* Type Offset=22 */

	/* Parameter pErrorDescription */

/* 180 */	NdrFcShort( 0x2113 ),	/* Flags:  must size, must free, out, simple ref, srv alloc size=8 */
/* 182 */	NdrFcShort( 0xc ),	/* x86 Stack size/offset = 12 */
/* 184 */	NdrFcShort( 0x38 ),	/* Type Offset=56 */

	/* Return value */

/* 186 */	NdrFcShort( 0x70 ),	/* Flags:  out, return, base type, */
/* 188 */	NdrFcShort( 0x10 ),	/* x86 Stack size/offset = 16 */
/* 190 */	0x8,		/* FC_LONG */
			0x0,		/* 0 */

			0x0
        }
    };

static const D3D_Setting_MIDL_TYPE_FORMAT_STRING D3D_Setting__MIDL_TypeFormatString =
    {
        0,
        {
			NdrFcShort( 0x0 ),	/* 0 */
/*  2 */	
			0x11, 0x0,	/* FC_RP */
/*  4 */	NdrFcShort( 0x2 ),	/* Offset= 2 (6) */
/*  6 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/*  8 */	NdrFcShort( 0x2c ),	/* 44 */
/* 10 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 12 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 14 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 16 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 18 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 20 */	0x8,		/* FC_LONG */
			0x5b,		/* FC_END */
/* 22 */	
			0x11, 0xc,	/* FC_RP [alloced_on_stack] [simple_pointer] */
/* 24 */	0xd,		/* FC_ENUM16 */
			0x5c,		/* FC_PAD */
/* 26 */	
			0x11, 0x4,	/* FC_RP [alloced_on_stack] */
/* 28 */	NdrFcShort( 0x1c ),	/* Offset= 28 (56) */
/* 30 */	
			0x13, 0x0,	/* FC_OP */
/* 32 */	NdrFcShort( 0xe ),	/* Offset= 14 (46) */
/* 34 */	
			0x1b,		/* FC_CARRAY */
			0x1,		/* 1 */
/* 36 */	NdrFcShort( 0x2 ),	/* 2 */
/* 38 */	0x9,		/* Corr desc: FC_ULONG */
			0x0,		/*  */
/* 40 */	NdrFcShort( 0xfffc ),	/* -4 */
/* 42 */	NdrFcShort( 0x1 ),	/* Corr flags:  early, */
/* 44 */	0x6,		/* FC_SHORT */
			0x5b,		/* FC_END */
/* 46 */	
			0x17,		/* FC_CSTRUCT */
			0x3,		/* 3 */
/* 48 */	NdrFcShort( 0x8 ),	/* 8 */
/* 50 */	NdrFcShort( 0xfff0 ),	/* Offset= -16 (34) */
/* 52 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 54 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 56 */	0xb4,		/* FC_USER_MARSHAL */
			0x83,		/* 131 */
/* 58 */	NdrFcShort( 0x0 ),	/* 0 */
/* 60 */	NdrFcShort( 0x4 ),	/* 4 */
/* 62 */	NdrFcShort( 0x0 ),	/* 0 */
/* 64 */	NdrFcShort( 0xffde ),	/* Offset= -34 (30) */
/* 66 */	
			0x11, 0x0,	/* FC_RP */
/* 68 */	NdrFcShort( 0xa ),	/* Offset= 10 (78) */
/* 70 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 72 */	NdrFcShort( 0x8 ),	/* 8 */
/* 74 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 76 */	0x5c,		/* FC_PAD */
			0x5b,		/* FC_END */
/* 78 */	
			0x15,		/* FC_STRUCT */
			0x3,		/* 3 */
/* 80 */	NdrFcShort( 0x4c ),	/* 76 */
/* 82 */	0x4c,		/* FC_EMBEDDED_COMPLEX */
			0x0,		/* 0 */
/* 84 */	NdrFcShort( 0xfff2 ),	/* Offset= -14 (70) */
/* 86 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 88 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 90 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 92 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 94 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 96 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 98 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 100 */	0x8,		/* FC_LONG */
			0x8,		/* FC_LONG */
/* 102 */	0x8,		/* FC_LONG */
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


/* Object interface: ID3DSetting, ver. 0.0,
   GUID={0xdec5b974,0xc1c0,0x4f46,{0x8b,0x74,0xff,0x8f,0xa3,0x87,0xbd,0x23}} */

#pragma code_seg(".orpc")
static const unsigned short ID3DSetting_FormatStringOffsetTable[] =
    {
    (unsigned short) -1,
    (unsigned short) -1,
    (unsigned short) -1,
    (unsigned short) -1,
    0,
    48,
    96,
    144
    };

static const MIDL_STUBLESS_PROXY_INFO ID3DSetting_ProxyInfo =
    {
    &Object_StubDesc,
    D3D_Setting__MIDL_ProcFormatString.Format,
    &ID3DSetting_FormatStringOffsetTable[-3],
    0,
    0,
    0
    };


static const MIDL_SERVER_INFO ID3DSetting_ServerInfo = 
    {
    &Object_StubDesc,
    0,
    D3D_Setting__MIDL_ProcFormatString.Format,
    &ID3DSetting_FormatStringOffsetTable[-3],
    0,
    0,
    0,
    0};
CINTERFACE_PROXY_VTABLE(11) _ID3DSettingProxyVtbl = 
{
    &ID3DSetting_ProxyInfo,
    &IID_ID3DSetting,
    IUnknown_QueryInterface_Proxy,
    IUnknown_AddRef_Proxy,
    IUnknown_Release_Proxy ,
    0 /* IDispatch::GetTypeInfoCount */ ,
    0 /* IDispatch::GetTypeInfo */ ,
    0 /* IDispatch::GetIDsOfNames */ ,
    0 /* IDispatch_Invoke_Proxy */ ,
    (void *) (INT_PTR) -1 /* ID3DSetting::GetD3DInfo */ ,
    (void *) (INT_PTR) -1 /* ID3DSetting::SetD3DInfo */ ,
    (void *) (INT_PTR) -1 /* ID3DSetting::GetD3DInfoEx */ ,
    (void *) (INT_PTR) -1 /* ID3DSetting::SetD3DInfoEx */
};


static const PRPC_STUB_FUNCTION ID3DSetting_table[] =
{
    STUB_FORWARDING_FUNCTION,
    STUB_FORWARDING_FUNCTION,
    STUB_FORWARDING_FUNCTION,
    STUB_FORWARDING_FUNCTION,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2,
    NdrStubCall2
};

CInterfaceStubVtbl _ID3DSettingStubVtbl =
{
    &IID_ID3DSetting,
    &ID3DSetting_ServerInfo,
    11,
    &ID3DSetting_table[-3],
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
    D3D_Setting__MIDL_TypeFormatString.Format,
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

const CInterfaceProxyVtbl * const _D3D_Setting_ProxyVtblList[] = 
{
    ( CInterfaceProxyVtbl *) &_ID3DSettingProxyVtbl,
    0
};

const CInterfaceStubVtbl * const _D3D_Setting_StubVtblList[] = 
{
    ( CInterfaceStubVtbl *) &_ID3DSettingStubVtbl,
    0
};

PCInterfaceName const _D3D_Setting_InterfaceNamesList[] = 
{
    "ID3DSetting",
    0
};

const IID *  const _D3D_Setting_BaseIIDList[] = 
{
    &IID_IDispatch,
    0
};


#define _D3D_Setting_CHECK_IID(n)	IID_GENERIC_CHECK_IID( _D3D_Setting, pIID, n)

int __stdcall _D3D_Setting_IID_Lookup( const IID * pIID, int * pIndex )
{
    
    if(!_D3D_Setting_CHECK_IID(0))
        {
        *pIndex = 0;
        return 1;
        }

    return 0;
}

const ExtendedProxyFileInfo D3D_Setting_ProxyFileInfo = 
{
    (PCInterfaceProxyVtblList *) & _D3D_Setting_ProxyVtblList,
    (PCInterfaceStubVtblList *) & _D3D_Setting_StubVtblList,
    (const PCInterfaceName * ) & _D3D_Setting_InterfaceNamesList,
    (const IID ** ) & _D3D_Setting_BaseIIDList,
    & _D3D_Setting_IID_Lookup, 
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

