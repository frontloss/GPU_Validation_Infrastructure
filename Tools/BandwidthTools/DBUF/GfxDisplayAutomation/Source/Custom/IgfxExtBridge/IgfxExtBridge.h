

/* this ALWAYS GENERATED file contains the definitions for the interfaces */


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


/* verify that the <rpcndr.h> version is high enough to compile this file*/
#ifndef __REQUIRED_RPCNDR_H_VERSION__
#define __REQUIRED_RPCNDR_H_VERSION__ 475
#endif

#include "rpc.h"
#include "rpcndr.h"

#ifndef __RPCNDR_H_VERSION__
#error this stub requires an updated version of <rpcndr.h>
#endif // __RPCNDR_H_VERSION__


#ifndef __IgfxExtBridge_h__
#define __IgfxExtBridge_h__

#if defined(_MSC_VER) && (_MSC_VER >= 1020)
#pragma once
#endif

/* Forward Declarations */ 

#ifndef __DisplayUtil_FWD_DEFINED__
#define __DisplayUtil_FWD_DEFINED__

#ifdef __cplusplus
typedef class DisplayUtil DisplayUtil;
#else
typedef struct DisplayUtil DisplayUtil;
#endif /* __cplusplus */

#endif 	/* __DisplayUtil_FWD_DEFINED__ */


#ifndef __MCCSUtil_FWD_DEFINED__
#define __MCCSUtil_FWD_DEFINED__

#ifdef __cplusplus
typedef class MCCSUtil MCCSUtil;
#else
typedef struct MCCSUtil MCCSUtil;
#endif /* __cplusplus */

#endif 	/* __MCCSUtil_FWD_DEFINED__ */


#ifndef __PowerUtil_FWD_DEFINED__
#define __PowerUtil_FWD_DEFINED__

#ifdef __cplusplus
typedef class PowerUtil PowerUtil;
#else
typedef struct PowerUtil PowerUtil;
#endif /* __cplusplus */

#endif 	/* __PowerUtil_FWD_DEFINED__ */


#ifndef __TVSetting_FWD_DEFINED__
#define __TVSetting_FWD_DEFINED__

#ifdef __cplusplus
typedef class TVSetting TVSetting;
#else
typedef struct TVSetting TVSetting;
#endif /* __cplusplus */

#endif 	/* __TVSetting_FWD_DEFINED__ */


#ifndef __D3DSetting_FWD_DEFINED__
#define __D3DSetting_FWD_DEFINED__

#ifdef __cplusplus
typedef class D3DSetting D3DSetting;
#else
typedef struct D3DSetting D3DSetting;
#endif /* __cplusplus */

#endif 	/* __D3DSetting_FWD_DEFINED__ */


#ifndef __SGUtil_FWD_DEFINED__
#define __SGUtil_FWD_DEFINED__

#ifdef __cplusplus
typedef class SGUtil SGUtil;
#else
typedef struct SGUtil SGUtil;
#endif /* __cplusplus */

#endif 	/* __SGUtil_FWD_DEFINED__ */


/* header files for imported files */
#include "oaidl.h"
#include "ocidl.h"
#include "Display_Util.h"
#include "MCCS_Util.h"
#include "Power_Util.h"
#include "TV_Setting.h"
#include "D3D_Setting.h"
#include "SG_Util.h"

#ifdef __cplusplus
extern "C"{
#endif 



#ifndef __IGFXEXTBRIDGELib_LIBRARY_DEFINED__
#define __IGFXEXTBRIDGELib_LIBRARY_DEFINED__

/* library IGFXEXTBRIDGELib */
/* [helpstring][version][uuid] */ 


EXTERN_C const IID LIBID_IGFXEXTBRIDGELib;

EXTERN_C const CLSID CLSID_DisplayUtil;

#ifdef __cplusplus

class DECLSPEC_UUID("2CE674BB-62B3-45e9-899F-F90B6BC970A7")
DisplayUtil;
#endif

EXTERN_C const CLSID CLSID_MCCSUtil;

#ifdef __cplusplus

class DECLSPEC_UUID("C1603752-CB01-412d-894E-FDDD113F1073")
MCCSUtil;
#endif

EXTERN_C const CLSID CLSID_PowerUtil;

#ifdef __cplusplus

class DECLSPEC_UUID("6A344570-2BDF-49db-8B6C-3EA32F026991")
PowerUtil;
#endif

EXTERN_C const CLSID CLSID_TVSetting;

#ifdef __cplusplus

class DECLSPEC_UUID("635A3AE2-8A58-4b2d-B701-7AD0050EC81C")
TVSetting;
#endif

EXTERN_C const CLSID CLSID_D3DSetting;

#ifdef __cplusplus

class DECLSPEC_UUID("2e9bbf19-0701-4675-ab17-b0d13e7cb124")
D3DSetting;
#endif

EXTERN_C const CLSID CLSID_SGUtil;

#ifdef __cplusplus

class DECLSPEC_UUID("2299C8C2-634E-4745-923A-DE0C8D03E7BB")
SGUtil;
#endif
#endif /* __IGFXEXTBRIDGELib_LIBRARY_DEFINED__ */

/* Additional Prototypes for ALL interfaces */

/* end of Additional Prototypes */

#ifdef __cplusplus
}
#endif

#endif


