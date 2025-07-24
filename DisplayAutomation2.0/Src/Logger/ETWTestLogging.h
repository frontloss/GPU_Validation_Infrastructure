#pragma once
#include "Windows.h"
#include "DisplayAutomationTestCrimson.h"
#ifdef _DLL_EXPORTS
#define CDLL_EXPORT __declspec(dllexport)
#endif

#define GFXTEST_MEDIA_OPERATION(Target, Operation) EventWriteMediaOperation(NULL, Target, Operation)
CDLL_EXPORT void EtwMediaOperation(UINT target_id, UINT operation);
CDLL_EXPORT void EtwGetDriverEscape(UINT minorEscapeCode, UINT majorEscapeCode, UINT minorInterfaceVersion, UINT majorInterfaceVersion);
CDLL_EXPORT void EtwSetDriverEscape(UINT minorEscapeCode, UINT majorEscapeCode, UINT minorInterfaceVersion, UINT majorInterfaceVersion);
CDLL_EXPORT void EtwTdrEscape(WCHAR deviceID[], WCHAR deviceInstanceID[], UINT tdrType);
CDLL_EXPORT void EtwReadRegistry(UINT feature, WCHAR reg_path[], WCHAR sub_key[], WCHAR reg_name[], UINT reg_type, WCHAR reg_value[]);
CDLL_EXPORT void EtwWriteRegistry(UINT feature, WCHAR reg_path[], WCHAR sub_key[], WCHAR reg_name[], UINT reg_type, WCHAR reg_value[]);
CDLL_EXPORT void EtwGetMode(UINT gfxIndex, UINT targetId, UINT status, BOOL virtualModeSetAware, UINT HzRes, UINT VtRes, UINT refreshRate, UINT scaling, UINT rotation,
                            UINT scanlineOrdering, UINT BPP, UINT64 pixelClock_Hz, UINT rrMode);
CDLL_EXPORT void EtwSetMode(UINT gfxIndex, UINT targetId, UINT status, BOOL virtualModeSetAware, UINT HzRes, UINT VtRes, UINT refreshRate, UINT scaling, UINT rotation,
                            UINT scanlineOrdering, UINT BPP, UINT64 pixelClock_Hz, UINT rrMode);
CDLL_EXPORT void EtwGetDisplayConfig(UINT status, UINT topology, UINT numberOfDisplays);
CDLL_EXPORT void EtwSetDisplayConfig(UINT status, UINT topology, UINT numberOfDisplays);
CDLL_EXPORT void EtwTargetDetails(UINT gfxIndex, UINT targetId, BOOL isActive);
CDLL_EXPORT void EtwMpo3FlipData(UINT SourceID, UINT Flags, UINT PlaneCount, UINT Duration, UINT64 TargetFlipTime);
CDLL_EXPORT void EtwMpo3FlipPlane(UINT LayerIndex, UINT Flags, UINT64 PresentID, UINT Rsvd);
CDLL_EXPORT void EtwMpo3FlipPlane_Details(UINT MaxImmFlipLine, UINT PlaneAttribFlag, UINT Blend, UINT ClrSpace, UINT Rotation, UINT StretchQuality, UINT SDRWhiteLevel,
                                          INT64 SrcLeft, INT64 SrcTop, INT64 SrcRight, INT64 SrcBottom, INT64 DestLeft, INT64 DestTop, INT64 DestRight, INT64 DestBottom,
                                          INT64 ClipLeft, INT64 ClipTop, INT64 ClipRight, INT64 ClipBottom, INT64 DirtyRectLeft, INT64 DirtyRectTop, INT64 DirtyRectRight,
                                          INT64 DirtyRectBottom, VOID *hallocation);