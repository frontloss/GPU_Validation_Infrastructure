/*------------------------------------------------------------------------------------------------*
 *
 * @file     DisplayColor.h
 * @brief    This header file contains Implementation of macros, GUIDs and structures used in
 *           Display Color SDK library
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#include "SdkSharedHeader.h"

#pragma once

#define GE_VERSIONS_SUPPORTED 1
#define IS_GAMUT_VERSION_SUPPORTED(x) (x <= GE_VERSIONS_SUPPORTED)
#define IS_GE_VERSION_SUPPORTED(x) (x <= GE_VERSIONS_SUPPORTED)
#define CSC_COEFFICIENTS 3

static const GUID IGFX_DESKTOP_GAMMA                = { 0x155f7ac, 0xf8a1, 0x4e64, { 0xb2, 0xe0, 0x5b, 0x58, 0xf7, 0x82, 0x1d, 0xc3 } };
static const GUID IGFX_GET_SET_GAMUT_EXPANSION_GUID = { 0x6b669a75, 0x4bc3, 0x4f92, { 0x91, 0x38, 0x6f, 0x44, 0xe1, 0x35, 0xb5, 0x22 } };
static const GUID IGFX_GET_SET_GAMUT_GUID           = { 0x808cdfeb, 0xe04f, 0x4214, { 0xab, 0xd2, 0x3e, 0x7b, 0xbe, 0x62, 0x95, 0x99 } };
static const GUID IGFX_GET_SET_HUESAT_INFO_GUID     = { 0x1cc2bb24, 0x5d6f, 0x4557, { 0x8b, 0xfb, 0x83, 0xc, 0x4f, 0x4d, 0xa7, 0x1 } };

#define IGFX_REDGAMMA 0x00
#define IGFX_GREENGAMMA 0x01
#define IGFX_BLUEGAMMA 0x02
#define IGFX_REDBRIGHTNESS 0x03
#define IGFX_GREENBRIGHTNESS 0x04
#define IGFX_BLUEBRIGHTNESS 0x05
#define IGFX_REDCONTRAST 0x06
#define IGFX_GREENCONTRAST 0x07
#define IGFX_BLUECONTRAST 0x08

typedef struct
{
    DWORD deviceUID;
    DWORD flags; // Reserved
    LONG  gammaValues[9];
} IGFX_DESKTOP_GAMMA_ARGS;

typedef struct _IGFX_GAMUT_EXPANSION
{
    IGFX_VERSION_HEADER versionHeader;
#if IS_GE_VERSION_SUPPORTED(1)
    DWORD deviceUID;
    BOOL  isFeatureSupported;
    DWORD gamutExpansionLevel;
    BOOL  useCustomCsc;
    FLOAT customCscMatrix[CSC_COEFFICIENTS][CSC_COEFFICIENTS];
    DWORD reserved;
#endif
} IGFX_GAMUT_EXPANSION;

typedef struct _IGFX_COLOR_DATA
{
    float currentValue; // Current Value
    float defaultValue; // Default Value
    float minValue;     // Minimium Value
    float maxValue;     // Maximium Value
    float stepValue;    // Adjustment value for each step
} IGFX_COLOR_DATA;

typedef struct _IGFX_HUESAT_INFO
{
    BOOL            isFeatureSupported; // Supported? TRUE: FALSE
    BOOL            isRGB;              // RGB (TRUE) or YUV (FALSE)
    DWORD           deviceID;           // Device ID
    IGFX_COLOR_DATA hueSettings;        // Hue Settings
    IGFX_COLOR_DATA saturationSettings; // Saturation Settings
    DWORD           flags;              // Reserved
} IGFX_HUESAT_INFO;

typedef struct _IGFX_GAMUT
{
    IGFX_VERSION_HEADER versionHeader;
#if IS_GAMUT_VERSION_SUPPORTED(1)
    DWORD deviceUID;
    BOOL  isFeatureSupported;
    BOOL  enableDisable;
    DWORD reserved;
#endif
} IGFX_GAMUT;
