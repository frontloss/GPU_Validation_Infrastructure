/*+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
**
** Copyright (c) Intel Corporation (1998).
**
** INTEL MAKES NO WARRANTY OF ANY KIND REGARDING THE CODE.  THIS CODE IS LICENSED
** ON AN "AS IS" BASIS AND INTEL WILL NOT PROVIDE ANY SUPPORT, ASSISTANCE,
** INSTALLATION, TRAINING OR OTHER SERVICES.  INTEL DOES NOT PROVIDE ANY UPDATES,
** ENHANCEMENTS OR EXTENSIONS.  INTEL SPECIFICALLY DISCLAIMS ANY WARRANTY OF
** MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR ANY PARTICULAR PURPOSE, OR ANY
** OTHER WARRANTY.  Intel disclaims all liability, including liability for
** infringement of any proprietary rights, relating to use of the code. No license,
** express or implied, by estoppel or otherwise, to any intellectual property
** rights is granted herein.
**
**
** File Name: ILFP.h (from LCDX.H)
**
** Abstract:  Local Flat Panel Transmitter defines
**
** Authors:   Venky Ramani
**
** Notes:
**
** Items In File:
**
**+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

#ifndef __ILFP_H__
#define __ILFP_H__

/////////////////////////////////////////////////////////
//
// LFP Parameters
//

// GUID for LFP Parameters
#define INTEL_LFPP_GUID "{1E42CD49-FFB4-41c5-9B79-D39D53FC7CB3}"
DEFINE_GUID(GUID_INTEL_LFPP, 0x1e42cd49, 0xffb4, 0x41c5, 0x9b, 0x79, 0xd3, 0x9d, 0x53, 0xfc, 0x7c, 0xb3);

#pragma pack(1)

typedef struct _LFPPARAMETERS
{
    GUID  Guid;        // GUID for this structure {1E42CD49-FFB4-41c5-9B79-D39D53FC7CB3}
    DWORD dwCommand;   // LFPP_COMMAND_*                       SET or GET
    DWORD dwFlags;     // bitfield, defined below              SET or GET
    DWORD dwEnabled;   // is LFP Panel on                      SET or GET
    DWORD dwMaxWidth;  // Max Horiz. Resolution of LFP Panel          GET
    DWORD dwMaxHeight; // Max Vert. Resolution of LFP Panel           GET
    UCHAR byEDID[128]; // EDID Block                                  GET
    ULONG ulEDIDSz;    // Size of EDID Block                          GET
} LFPPARAMETERS, *PLFPPARAMETERS, FAR *LPLFPPARAMETERS;

#pragma pack()

#define LFPP_COMMAND_GET 0x0001
#define LFPP_COMMAND_SET 0x0002

#define LFPP_FLAGS_PANEL_ATTACHED 0x0001
#define LFPP_FLAGS_PANEL_ENABLE 0x0002
#define LFPP_FLAGS_PANEL_FITTING 0x0004

#define LFPP_LFP_DISABLED 0x0000
#define LFPP_LFP_ENABLED 0x0001

#endif //__ILFP_H__
