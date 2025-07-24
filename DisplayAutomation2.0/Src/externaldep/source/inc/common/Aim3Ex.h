/*+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
**
** Copyright (c) Intel Corporation (1998-2003).
**
** INTEL MAKES NO WARRANTY OF ANY KIND REGARDING THE CODE.  THIS CODE IS LICENSED
** ON AN ""AS IS"" BASIS AND INTEL WILL NOT PROVIDE ANY SUPPORT, ASSISTANCE,
** INSTALLATION, TRAINING OR OTHER SERVICES.  INTEL DOES NOT PROVIDE ANY UPDATES,
** ENHANCEMENTS OR EXTENSIONS.  INTEL SPECIFICALLY DISCLAIMS ANY WARRANTY OF
** MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR ANY PARTICULAR PURPOSE, OR ANY
** OTHER WARRANTY.  Intel disclaims all liability, including liability for
** infringement of any proprietary rights, relating to use of the code. No license,
** express or implied, by estoppel or otherwise, to any intellectual property
** rights is granted herein.
**
**
** File Name:   	Aim3Ex.h
**
** Abstract:
**
**
** Environment: 	Win95, Win98, WinNT, 2k, XP, Vista
**
**+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

#ifndef __IAIM_H__
#define __IAIM_H__

#pragma pack(1)

// Following Interface would be used for querying Connector Related Info per Display UID.
// {E79CF31D-8E4D-4a91-BD49-CCCDD76693F7}

#define INTEL_GETCONNECTOR_INFO_GUID "{E79CF31D-8E4D-4a91-BD49-CCCDD76693F7}"
DEFINE_GUID(GUID_INTEL_GETCONNECTORINFO, 0xe79cf31d, 0x8e4d, 0x4a91, 0xbd, 0x49, 0xcc, 0xcd, 0xd7, 0x66, 0x93, 0xf7);

// SupportedConnectors -> Return the supportedConnectors based on DisplayUID
// Attached Connectors -> If Display is attached then return the connector type i.e. attached
// Active Connectors -> If Display is Active then return the connector type

typedef struct _GET_CONNECTOR_INFO
{
    GUID Guid;
    OUT DWORD dwSupportedConnectors; // Use the Below Defined Macros for Connector Types.
    OUT DWORD dwAttachedConnectors;  // Use the Below Defined Macros for Connector Types.
    OUT DWORD dwActiveConnectors;    // Use the Below Defined Macros for Connector Types.
} GET_CONNECTOR_INFO, *PGET_CONNECTOR_INFO;

#pragma pack()

#define CONNECTOR_TYPE_UNKNOWN 0xffffffff
#define CONNECTOR_TYPE_NONE 0x00000000
#define CONNECTOR_TYPE_VGA 0x00000001 // For CRT
#define CONNECTOR_TYPE_LVDS 0x00000002
#define CONNECTOR_TYPE_DVI 0x00000004
#define CONNECTOR_TYPE_HDMI 0x00000008
#define CONNECTOR_TYPE_SVIDEO 0x00000010
#define CONNECTOR_TYPE_COMPOSITE_VIDEO 0x00000020
#define CONNECTOR_TYPE_COMPONENT_VIDEO 0x00000040
#define CONNECTOR_TYPE_SCART_VIDEO 0x00000080
#define CONNECTOR_TYPE_DISPLAYPORT 0x00000100
#define CONNECTOR_TYPE_EMBEDDED_DISPLAY_PORT 0x00000200
#define CONNECTOR_TYPE_MIPI 0x00000400

// End of Interface Details for querying Connector Related Info per Display UID.

#endif //__IAIM_H__
