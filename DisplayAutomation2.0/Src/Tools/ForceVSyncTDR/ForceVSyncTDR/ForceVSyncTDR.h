/**
 * @file
 * @author Suraj Gaikwad
 */

/**********************************************************************************
 * INTEL CONFIDENTIAL. Copyright (c) 2016 Intel Corporation All Rights Reserved.
 *  <br>The source code contained or described herein and all documents related to the source code
 *  ("Material") are owned by Intel Corporation or its suppliers or licensors. Title to the
 *  Material remains with Intel Corporation or its suppliers and licensors. The Material contains
 *  trade secrets and proprietary and confidential information of Intel or its suppliers and licensors.
 *  The Material is protected by worldwide copyright and trade secret laws and treaty provisions.
 *  No part of the Material may be used, copied, reproduced, modified, published, uploaded, posted,
 *  transmitted, distributed, or disclosed in any way without Intel’s prior express written permission.
 *  <br>No license under any patent, copyright, trade secret or other intellectual property right is
 *  granted to or conferred upon you by disclosure or delivery of the Materials, either expressly,
 *  by implication, inducement, estoppel or otherwise. Any license under such intellectual property
 *  rights must be express and approved by Intel in writing.
 */

/* DLL's header include*/

#ifndef _D3DKMDT_H
#define _D3DKMDT_H

#pragma once
#include <d3dukmdt.h>

#endif /* _D3DKMDT_H */

/* Exposed API function poinetrs of SystemUtility DLL*/

typedef HRESULT(__cdecl *TDRDriverEscapeCall)(HRESULT *);

typedef struct _D3DKMT_OPENADAPTERFROMHDC
{
    HDC                            hDc;           // in:  DC that maps to a single display
    D3DKMT_HANDLE                  hAdapter;      // out: adapter handle
    LUID                           AdapterLuid;   // out: adapter LUID
    D3DDDI_VIDEO_PRESENT_SOURCE_ID VidPnSourceId; // out: VidPN source ID for that particular display
} D3DKMT_OPENADAPTERFROMHDC;

typedef struct _D3DKMT_CLOSEADAPTER
{
    D3DKMT_HANDLE hAdapter; // in: adapter handle
} D3DKMT_CLOSEADAPTER;

typedef enum _D3DKMT_ESCAPETYPE
{
    D3DKMT_ESCAPE_DRIVERPRIVATE = 0,
    D3DKMT_ESCAPE_VIDMM         = 1,
    D3DKMT_ESCAPE_TDRDBGCTRL    = 2,
    D3DKMT_ESCAPE_VIDSCH        = 3,
} D3DKMT_ESCAPETYPE;

typedef enum _D3DKMT_TDRDBGCTRLTYPE
{
    D3DKMT_TDRDBGCTRLTYPE_FORCETDR         = 0, // Simulate a TDR
    D3DKMT_TDRDBGCTRLTYPE_DISABLEBREAK     = 1, // Disable DebugBreak on timeout
    D3DKMT_TDRDBGCTRLTYPE_ENABLEBREAK      = 2, // Enable DebugBreak on timeout
    D3DKMT_TDRDBGCTRLTYPE_UNCONDITIONAL    = 3, // Disables all safety conditions (e.g. check for consecutive recoveries).
    D3DKMT_TDRDBGCTRLTYPE_VSYNCTDR         = 4, // Simulate VSync TDR
    D3DKMT_TDRDBGCTRLTYPE_GPUTDR           = 5, // Simulate GPU TDR
    D3DKMT_TDRDBGCTRLTYPE_FORCEDODTDR      = 6, // Simulate a display-only present TDR.
    D3DKMT_TDRDBGCTRLTYPE_FORCEDODVSYNCTDR = 7, // Simulate a display-only VSync TDR.
    D3DKMT_TDRDBGCTRLTYPE_ENGINETDR        = 8  // Simulate an engine TDR.
} D3DKMT_TDRDBGCTRLTYPE;

typedef struct _D3DKMT_ESCAPE
{
    D3DKMT_HANDLE      hAdapter;              // in: adapter handle
    D3DKMT_HANDLE      hDevice;               // in: device handle [Optional]
    D3DKMT_ESCAPETYPE  Type;                  // in: escape type.
    D3DDDI_ESCAPEFLAGS Flags;                 // in: flags
    VOID *             pPrivateDriverData;    // in/out: escape data
    UINT               PrivateDriverDataSize; // in: size of escape data
    D3DKMT_HANDLE      hContext;              // in: context handle [Optional]
} D3DKMT_ESCAPE;

typedef NTSTATUS(APIENTRY *PFND3DKMT_OPENADAPTERFROMHDC)(IN OUT D3DKMT_OPENADAPTERFROMHDC *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_CLOSEADAPTER)(IN CONST D3DKMT_CLOSEADAPTER *);
typedef NTSTATUS(APIENTRY *PFND3DKMT_ESCAPE)(IN CONST D3DKMT_ESCAPE *);
