#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <time.h>
#include <windows.h>
#include <strsafe.h>

#include "ETWTestLogging.h"

void EtwMediaOperation(UINT target_id, UINT operation)
{
    GFXTEST_MEDIA_OPERATION(target_id, operation);
    return;
}

void EtwGetDriverEscape(UINT minorEscapeCode, UINT majorEscapeCode, UINT minorInterfaceVersion, UINT majorInterfaceVersion)
{
    EventWriteGetDriverEscape(NULL, minorEscapeCode, majorEscapeCode, minorInterfaceVersion, majorInterfaceVersion);
}

void EtwSetDriverEscape(UINT minorEscapeCode, UINT majorEscapeCode, UINT minorInterfaceVersion, UINT majorInterfaceVersion)
{
    EventWriteSetDriverEscape(NULL, minorEscapeCode, majorEscapeCode, minorInterfaceVersion, majorInterfaceVersion);
}

void EtwTdrEscape(WCHAR deviceID[], WCHAR deviceInstanceID[], UINT tdrType)
{
    EventWriteTdrEscape(NULL, deviceID, deviceInstanceID, tdrType);
}

void EtwReadRegistry(UINT feature, WCHAR reg_path[], WCHAR sub_key[], WCHAR reg_name[], UINT reg_type, WCHAR reg_value[])
{
    EventWriteReadRegistry(NULL, feature, reg_path, sub_key, reg_name, reg_type, reg_value);
}

void EtwWriteRegistry(UINT feature, WCHAR reg_path[], WCHAR sub_key[], WCHAR reg_name[], UINT reg_type, WCHAR reg_value[])
{
    EventWriteWriteRegistry(NULL, feature, reg_path, sub_key, reg_name, reg_type, reg_value);
}

void EtwGetMode(UINT gfxIndex, UINT targetId, UINT status, BOOL virtualModeSetAware, UINT HzRes, UINT VtRes, UINT refreshRate, UINT scaling, UINT rotation, UINT scanlineOrdering,
                UINT BPP, UINT64 pixelClock_Hz, UINT rrMode)
{
    EventWriteGetModeDetails(NULL, gfxIndex, targetId, status, virtualModeSetAware, HzRes, VtRes, refreshRate, scaling, rotation, scanlineOrdering, BPP, pixelClock_Hz, rrMode);
}

void EtwSetMode(UINT gfxIndex, UINT targetId, UINT status, BOOL virtualModeSetAware, UINT HzRes, UINT VtRes, UINT refreshRate, UINT scaling, UINT rotation, UINT scanlineOrdering,
                UINT BPP, UINT64 pixelClock_Hz, UINT rrMode)
{
    EventWriteSetModeDetails(NULL, gfxIndex, targetId, status, virtualModeSetAware, HzRes, VtRes, refreshRate, scaling, rotation, scanlineOrdering, BPP, pixelClock_Hz, rrMode);
}

void EtwGetDisplayConfig(UINT status, UINT topology, UINT numberOfDisplays)
{
    EventWriteGetConfiguration(NULL, status, topology, numberOfDisplays);
}

void EtwSetDisplayConfig(UINT status, UINT topology, UINT numberOfDisplays)
{
    EventWriteSetConfiguration(NULL, status, topology, numberOfDisplays);
}

void EtwTargetDetails(UINT gfxIndex, UINT targetId, BOOL isActive)
{
    EventWriteTargetDetails(NULL, gfxIndex, targetId, isActive);
}

void EtwMpo3FlipData(UINT SourceID, UINT Flags, UINT PlaneCount, UINT Duration, UINT64 TargetFlipTime)
{
    EventWriteMpo3Flip_Start(NULL, SourceID, Flags, PlaneCount, Duration, TargetFlipTime);
}

void EtwMpo3FlipPlane(UINT LayerIndex, UINT Flags, UINT64 PresentID, UINT Rsvd)
{
    EventWriteMpo3Flip_Plane(NULL, LayerIndex, Flags, PresentID, Rsvd);
}

void EtwMpo3FlipPlane_Details(UINT MaxImmFlipLine, UINT PlaneAttribFlag, UINT Blend, UINT ClrSpace, UINT Rotation, UINT StretchQuality, UINT SDRWhiteLevel, INT64 SrcLeft,
                              INT64 SrcTop, INT64 SrcRight, INT64 SrcBottom, INT64 DestLeft, INT64 DestTop, INT64 DestRight, INT64 DestBottom, INT64 ClipLeft, INT64 ClipTop,
                              INT64 ClipRight, INT64 ClipBottom, INT64 DirtyRectLeft, INT64 DirtyRectTop, INT64 DirtyRectRight, INT64 DirtyRectBottom, VOID *hallocation)
{
    EventWriteMPO3FlipPlane_Details(NULL, MaxImmFlipLine, PlaneAttribFlag, Blend, ClrSpace, Rotation, StretchQuality, SDRWhiteLevel, SrcLeft, SrcTop, SrcRight, SrcBottom, DestLeft,
                                    DestTop, DestRight, DestBottom, ClipLeft, ClipTop, ClipRight, ClipBottom, DirtyRectLeft, DirtyRectTop, DirtyRectRight, DirtyRectBottom,
                                    hallocation);
}