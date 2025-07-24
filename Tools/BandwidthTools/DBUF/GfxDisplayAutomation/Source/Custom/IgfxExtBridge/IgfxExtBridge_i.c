

/* this ALWAYS GENERATED file contains the IIDs and CLSIDs */

/* link this file in with the server and any clients */


 /* File created by MIDL compiler version 8.00.0595 */
/* at Mon Jun 15 12:52:05 2015
 */
/* Compiler settings for IgfxExtBridge.idl:
    Oicf, W1, Zp8, env=Win32 (32b run), target_arch=X86 8.00.0595 
    protocol : dce , ms_ext, c_ext, robust
    error checks: allocation ref bounds_check enum stub_data 
    VC __declspec() decoration level: 
         __declspec(uuid()), __declspec(selectany), __declspec(novtable)
         DECLSPEC_UUID(), MIDL_INTERFACE()
*/
/* @@MIDL_FILE_HEADING(  ) */

#pragma warning( disable: 4049 )  /* more than 64k source lines */


#ifdef __cplusplus
extern "C"{
#endif 


#include <rpc.h>
#include <rpcndr.h>

#ifdef _MIDL_USE_GUIDDEF_

#ifndef INITGUID
#define INITGUID
#include <guiddef.h>
#undef INITGUID
#else
#include <guiddef.h>
#endif

#define MIDL_DEFINE_GUID(type,name,l,w1,w2,b1,b2,b3,b4,b5,b6,b7,b8) \
        DEFINE_GUID(name,l,w1,w2,b1,b2,b3,b4,b5,b6,b7,b8)

#else // !_MIDL_USE_GUIDDEF_

#ifndef __IID_DEFINED__
#define __IID_DEFINED__

typedef struct _IID
{
    unsigned long x;
    unsigned short s1;
    unsigned short s2;
    unsigned char  c[8];
} IID;

#endif // __IID_DEFINED__

#ifndef CLSID_DEFINED
#define CLSID_DEFINED
typedef IID CLSID;
#endif // CLSID_DEFINED

#define MIDL_DEFINE_GUID(type,name,l,w1,w2,b1,b2,b3,b4,b5,b6,b7,b8) \
        const type name = {l,w1,w2,{b1,b2,b3,b4,b5,b6,b7,b8}}

#endif !_MIDL_USE_GUIDDEF_

MIDL_DEFINE_GUID(IID, LIBID_IGFXEXTBRIDGELib,0x9A650EBC,0x929B,0x4210,0xBA,0x05,0x76,0xD5,0xD0,0x21,0xB1,0x40);


MIDL_DEFINE_GUID(CLSID, CLSID_DisplayUtil,0x2CE674BB,0x62B3,0x45e9,0x89,0x9F,0xF9,0x0B,0x6B,0xC9,0x70,0xA7);


MIDL_DEFINE_GUID(CLSID, CLSID_MCCSUtil,0xC1603752,0xCB01,0x412d,0x89,0x4E,0xFD,0xDD,0x11,0x3F,0x10,0x73);


MIDL_DEFINE_GUID(CLSID, CLSID_PowerUtil,0x6A344570,0x2BDF,0x49db,0x8B,0x6C,0x3E,0xA3,0x2F,0x02,0x69,0x91);


MIDL_DEFINE_GUID(CLSID, CLSID_TVSetting,0x635A3AE2,0x8A58,0x4b2d,0xB7,0x01,0x7A,0xD0,0x05,0x0E,0xC8,0x1C);


MIDL_DEFINE_GUID(CLSID, CLSID_D3DSetting,0x2e9bbf19,0x0701,0x4675,0xab,0x17,0xb0,0xd1,0x3e,0x7c,0xb1,0x24);


MIDL_DEFINE_GUID(CLSID, CLSID_SGUtil,0x2299C8C2,0x634E,0x4745,0x92,0x3A,0xDE,0x0C,0x8D,0x03,0xE7,0xBB);

#undef MIDL_DEFINE_GUID

#ifdef __cplusplus
}
#endif



