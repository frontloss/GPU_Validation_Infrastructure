/*=================================================================================================
;
;   Copyright (c) Intel Corporation (2000 - 2018)
;
;   INTEL MAKES NO WARRANTY OF ANY KIND REGARDING THE CODE.  THIS CODE IS LICENSED
;   ON AN "AS IS" BASIS AND INTEL WILL NOT PROVIDE ANY SUPPORT, ASSISTANCE,
;   INSTALLATION, TRAINING OR OTHER SERVICES.  INTEL DOES NOT PROVIDE ANY UPDATES,
;   ENHANCEMENTS OR EXTENSIONS.  INTEL SPECIFICALLY DISCLAIMS ANY WARRANTY OF
;   MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR ANY PARTICULAR PURPOSE, OR ANY
;   OTHER WARRANTY.  Intel disclaims all liability, including liability for
;   infringement of any proprietary rights, relating to use of the code. No license,
;   express or implied, by estoppel or otherwise, to any intellectual property
;   rights is granted herein.
;
;------------------------------------------------------------------------------------------------*/

//=================================================================================================
//									System Utility Header File
//=================================================================================================

/*------------------------------------------------------------------------------------------------*
*
* @file  SystemUtility.h
* @brief This file contains Implementation of GetDLLVersion, EnableDisableDFT,
                            GetSetVbtBlock, GetSetVbt, ResetVbt, DftMMIOAccess
*
*------------------------------------------------------------------------------------------------*/

/* Avoid multi inclusion of header file*/
#pragma once

/* System header(s) */
#include <windows.h>
#include "CommonDetails.h"
#include "GfxValStub_DisplayFeature.h"
#include "DisplayEscape.h"
#include "CommonInclude.h"

/* Preprocessor Macros*/
#ifdef _DLL_EXPORTS
#define CDLL_EXPORT __declspec(dllexport)
#else
#define CDLL_EXPORT __declspec(dllimport)
#endif

/* Enable or Disable DLL debug message logging on console if this debug */
#ifdef _DEBUG
#define DEBUG_PRINTS true
#else
#define DEBUG_PRINTS false
#endif
#ifndef IN_OUT
#define IN_OUT
#endif

/* DLL version information*/
#define UTILITY_INTERFACE_VERSION 0x2

/* Data structures detail */
// Going with Pack 1 as it is useful for various variable size arrays that we
// have defined at the end of structures
#pragma pack(1)

/* Enum for DFT based MMIO access type*/
typedef enum _DFT_MMIO_ACCESS_TYPE
{
    DFT_MMIO_READ = 0,
    DFT_MMIO_WRITE
} DFT_MMIO_ACCESS_TYPE;

/* Structure definition DFT based MMIO access */
typedef struct _DFT_MMIO_ACCESS
{
    _In_ DFT_MMIO_ACCESS_TYPE accessType; /**< Access type (read/write) */
    _In_ ULONG offset;                    /**< MMIO offset in Hex */
    _Inout_ ULONG value;                  /**< Register value in Hex */
} DFT_MMIO_ACCESS, *PDFT_MMIO_ACCESS;

/** Structure contains MMIO read information*/

typedef struct _TOOL_ESC_READ_MMIO_REGISTER_ARGS
{
    IN ULONG ulOffset; /* Offset of the MMIO register to be read*/
    OUT ULONG ulValue; /* Value of the MMIO register at the given offset*/
} TOOL_ESC_READ_MMIO_REGISTER_ARGS, *PTOOL_ESC_READ_MMIO_REGISTER_ARGS;

/* Helper variables to make driver escape call*/
TOOL_ESC_READ_MMIO_REGISTER_ARGS mmioRegDetail;

/* Internal & Exposed function*/
BOOL GetRegistryKey(PCWSTR filterServiceName, ULONG keyType, HKEY *pHKey);

CDLL_EXPORT VOID GetDLLVersion(PULONG pVersion);

CDLL_EXPORT BOOL EnableDisableDFT(BOOL bEnable);

CDLL_EXPORT BOOL GetSetVbtBlock(UINT blockId, PBYTE pBlockData, BOOLEAN bSet);

CDLL_EXPORT BOOL GetSetVbt(PBYTE pVbtData, PULONG pulVbtSize, BOOLEAN bSet);

CDLL_EXPORT BOOL ResetVbt();

CDLL_EXPORT VOID FreeAllocations();


