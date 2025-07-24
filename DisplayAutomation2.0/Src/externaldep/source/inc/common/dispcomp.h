/****************************************************************************
** Copyright (c) Intel Corporation (2003).                                  *
**                                                                          *
** INTEL MAKES NO WARRANTY OF ANY KIND REGARDING THE CODE.  THIS CODE IS    *
** LICENSED ON AN "AS IS" BASIS AND INTEL WILL NOT PROVIDE ANY SUPPORT,     *
** ASSISTANCE, INSTALLATION, TRAINING OR OTHER SERVICES.  INTEL DOES NOT    *
** PROVIDE ANY UPDATES, ENHANCEMENTS OR EXTENSIONS.  INTEL SPECIFICALLY     *
** DISCLAIMS ANY WARRANTY OF MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR  *
** ANY PARTICULAR PURPOSE, OR ANY OTHER WARRANTY.  Intel disclaims all      *
** liability, including liability for infringement of any proprietary       *
** rights, relating to use of the code. No license, express or implied, by  *
** estoppel or otherwise, to any intellectual property rights is            *
** granted herein.                                                          *
*****************************************************************************
**
** File Name  : dispcomp.h
**
** Abstract   : This file contains all the structure definitions related to
**              device compensations.
**
**------------------------------------------------------------------------ */
#ifndef _DISPCOMP_H_
#define _DISPCOMP_H_

// Types of compensation
#define COMP_NOT_SUPPORTED 0
#define COMP_CENTERING (1 << 0)
#define COMP_FULL_SCREEN (1 << 1)
#define COMP_MAINTAIN_ASPECT_SCALING (1 << 2)
#define COMP_CUSTOM_SCALING (1 << 3)
#define COMP_MEDIA_SCALING_FS (1 << 4)
#define COMP_MEDIA_SCALING_AR (1 << 5)
#define COMP_NO_SCALING (1 << 6)
#define COMP_ALL_SCALING (~0)

// Maximum no. of valid compensations
#define MAX_POSSIBLE_COMPENSATIONS 7

// Custom compensation information
typedef struct _CUSTOM_COMPENSATION_INFO
{
    ULONG ulMinCustomScaling;     // Maximum down scaling
    ULONG ulMaxCustomScaling;     // Maximum up scaling
    ULONG ulStep;                 // Steps in which scaling can be requested
    ULONG ulCurrentCustomScaling; // Current value of custom scaling
    ULONG ulDefault;              // Default value of custom scaling
} CUSTOM_COMPENSATION_INFO, *PCUSTOM_COMPENSATION_INFO;

// Structure to get individual display compensation information
typedef struct _GET_DISPLAY_COMPENSATION
{
    ULONG ulDisplayUID;            // Display Identifier
    ULONG ulCompensationCaps;      // Compensation capabilities of the
                                   // display indicated in ulDisplayUID
    ULONG ulCurrentCompensation;   // Current compensation of the
                                   // display indicated in ulDisplayUID
    ULONG ulPreferredCompensation; // Preferred compensation of the
                                   // display indicated in ulDisplayUID
    // TBD - TO be removed as it's no longer used
    ULONG ulMediaCompensationCaps;    // Media Compensation Capabilities of the
                                      // display indicated in ulDisplayUID
    ULONG ulCurrentMediaCompensation; // Current Media Compensation capabilities of the
                                      // display indicated in ulDisplayUID

    CUSTOM_COMPENSATION_INFO CustomCompX; // Horizontal custom comp info
    CUSTOM_COMPENSATION_INFO CustomCompY; // Vertical custom comp info
} GET_DISPLAY_COMPENSATION, *PGET_DISPLAY_COMPENSATION;

// Structure to set display compensation.
typedef struct _DISPLAY_COMPENSATION
{
    ULONG ulDisplayUID; // Display Identifier
    ULONG ulCurrentCompensation;
    ULONG ulCurrentMediaCompensation;
    ULONG ulCompensationCaps;
    ULONG ulPreferredCompensation;
    ULONG ulCurrentCustomCompX; // This field is applicable only for HDMI devices as of today.
    ULONG ulCurrentCustomCompY; // This field is applicable only for HDMI devices as of today.
} DISPLAY_COMPENSATION, *PDISPLAY_COMPENSATION;

// Structure to set display compensation.
typedef struct _SET_DISPLAY_COMPENSATION
{
    ULONG   ulDisplayUID; // Display Identifier
    ULONG   ulCompensation;
    ULONG   ulNewCustomCompX;
    ULONG   ulNewCustomCompY;
    BOOLEAN bPostponeCompensationChange;
    BOOLEAN bSFRequest;
    ULONG   ulYPosition;
} SET_DISPLAY_COMPENSATION, *PSET_DISPLAY_COMPENSATION;

// Relative compensation record: The following structure will cater
// to the available compensations on a device for a particular
// selection on the other device.
typedef struct _RELATIVE_COMPENSATION_REC
{
    ULONG ulCompOnOtherDevice; // Given compensation on other device
    ULONG ulAvailableComps;    // Compensations available on this
                               // device (Bitmask).
} RELATIVE_COMPENSATION_REC, *PRELATIVE_COMPENSATION_REC;

// Map of relative compensations. The number of available records in the map
// at any point of time is indicated by the element ulNumEntries
typedef struct _RELATIVE_COMPENSATION_MAP
{
    ULONG ulNumEntries; // No. of recs available in the relative
                        // compensation map
    RELATIVE_COMPENSATION_REC CompRec[MAX_POSSIBLE_COMPENSATIONS];
} RELATIVE_COMPENSATION_MAP, *PRELATIVE_COMPENSATION_MAP;

typedef struct _GET_REL_COMP_IN_CONFIG
{
    ULONG ulDeviceConfig;                    // Display Config in which relative
                                             // compensations are queried
    GET_DISPLAY_COMPENSATION PriCompInfo;    // Primary compensation info
    GET_DISPLAY_COMPENSATION SecCompInfo;    // Secondary compensation info
    GET_DISPLAY_COMPENSATION ThirdCompInfo;  // Third compensation info
    GET_DISPLAY_COMPENSATION FourthCompInfo; // Fourth compensation info

    RELATIVE_COMPENSATION_MAP PriCompInfoRelativeToSec; // Available compensations
                                                        // on primary for a given compensation
                                                        // on secondary/tertiary.
    RELATIVE_COMPENSATION_MAP SecCompInfoRelativeToPri; // Available compensations
                                                        // on secondary for a given compensation
                                                        // on primary/tertiary

    RELATIVE_COMPENSATION_MAP TerCompInfoRelativeToPri; // Available compensations
                                                        // on tertiary for a given compensation
                                                        // on primary/secondary
} GET_REL_COMP_IN_CONFIG, *PGET_REL_COMP_IN_CONFIG;

#endif //_DISPCOMP_H_
