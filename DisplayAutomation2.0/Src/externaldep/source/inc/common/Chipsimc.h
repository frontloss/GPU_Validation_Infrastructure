/*+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
**
** Copyright (c) Intel Corporation (1998).
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
** ChipsImc.h - SoftBIOS InterModule Communications
**
** File Description:
** 	This module contains the definitions for any data shared
**	between Display, Miniport & Chips Control Panel.
**  Note: This file is also used by OMP tool.So any changes
**  to this file should be compatable with the tool as well.
**
**+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

#ifndef _CHIPSIMC_H_
#define _CHIPSIMC_H_

#define HWCURSOR_A 1
#define HWCURSOR_B 2
#define MAX_PLANES_PER_PIPE_GEN9 4                         // use MAX_PLANES_PER_PIPE_GENX for loop checks.
#define MAX_PLANES_PER_PIPE_GEN10 MAX_PLANES_PER_PIPE_GEN9 // use MAX_PLANES_PER_PIPE_GENX for loop checks.
#define MAX_PLANES_PER_PIPE_GEN11 5                        // use MAX_PLANES_PER_PIPE_GENX for loop checks.
#define MAX_PLANES_PER_PIPE MAX_PLANES_PER_PIPE_GEN11      // use MAX_PLANES_PER_PIPE for struct sizes.
#define MAX_Y_PLANES_PER_PIPE_GEN11 2
#define GEN11_MAX_PLANES_FOR_WM (MAX_PLANES_PER_PIPE_GEN11 + MAX_Y_PLANES_PER_PIPE_GEN11)
#define MAX_PLANES_FOR_WATERMARK GEN11_MAX_PLANES_FOR_WM
#define MAX_HDR_PLANES_PER_PIPE_GEN11 3

typedef enum _PLANE_TYPE
{
    NULL_PLANE     = 0x7F,
    PLANE_VGA      = 0,
    PLANE_A        = 1,
    PLANE_B        = 2,
    PLANE_C        = 3,
    PLANE_D        = 4,
    PLANE_SPRITE_A = 5,
    PLANE_SPRITE_B = 6,
    PLANE_SPRITE_C = 7,
    PLANE_SPRITE_D = 8,
    PLANE_SPRITE_E = 9,
    PLANE_SPRITE_F = 10,
    PLANE_SPRITE_G = 11,
    PLANE_SPRITE_H = 12,
    CURSORPLANE_A  = 13,
    CURSORPLANE_B  = 14,
    CURSORPLANE_C  = 15,
    CURSORPLANE_D  = 16,
    PLANE_OVERLAY  = 17, // Generic enum for all overlay planes
    PLANE_ALL      = 20,
    TPV_PLANE      = 60,

    // Planes on Pipe A
    PLANE_1_A = 21,
    PLANE_2_A,
    PLANE_3_A,
    PLANE_4_A,
    PLANE_5_A,

    // Planes on Pipe B
    PLANE_1_B = 31,
    PLANE_2_B,
    PLANE_3_B,
    PLANE_4_B,
    PLANE_5_B,

    // Planes on Pipe C
    PLANE_1_C = 41,
    PLANE_2_C,
    PLANE_3_C,
    PLANE_4_C,
    PLANE_5_C,

} PLANE_TYPE;
/*
typedef enum _GENPLANE_TYPE {
    NULL_PLANE_MPO = 0x7F,
    PLANE_0 = PLANE_VGA,
    PLANE_1_A = 1,            //PLANE_A
    PLANE_2_A = 2,            //PLANE_SPRITE_A
    PLANE_3_A = 3,            //PLANE_SPRITE_B
    PLANE_4_A,

    PLANE_1_B ,            //PLANE_B
    PLANE_2_B ,            //PLANE_SPRITE_C
    PLANE_3_B ,            //PLANE_SPRITE_D
    PLANE_4_B,

    PLANE_1_C = MAX_PLANES_PER_PIPE * 2 + 1,          //PLANE_C
    PLANE_2_C,           //PLANE_SPRITE_E
    PLANE_3_C,          //PLANE_SPRITE_F
    PLANE_4_C,
}GENPLANE_TYPE;
*/
typedef enum _GEN_PLANE_TYPE
{
    PLANE_CURSOR_A = CURSORPLANE_A,
    PLANE_CURSOR_B = CURSORPLANE_B,
    PLANE_CURSOR_C = CURSORPLANE_C,
    PLANE_NONE     = 20,
    PLANE_1        = 21,
    PLANE_2        = 22,
    PLANE_3        = 23,
    PLANE_4        = 24,
    PLANE_5        = 25,
    PLANE_6        = 26,
    PLANE_7        = 27,
    PLANE_8        = 28,
    PLANE_9        = 29,
    PLANE_10       = 30,
    PLANE_11       = 31,
    PLANE_12       = 32,
    PLANE_13       = 33,
    PLANE_14       = 34,
    PLANE_15       = 35,
    PLANE_16       = 36,
    PLANE_17       = 37,
    PLANE_18       = 38,
    PLANE_19       = 39,
    PLANE_20       = 40,
    PLANE_21       = 41,
    PLANE_22       = 42,
    PLANE_23       = 43,
    PLANE_24       = 44,
    PLANE_25       = 45,
    PLANE_26       = 46,
    PLANE_27       = 47,
    PLANE_28       = 48,
    PLANE_MAX,
    GEN9_PLANE_ALL = 14, // 11 diplay plane for BXT and 3 cursor planes, excluding VGA.
} GEN_PLANE_TYPE;

typedef enum _PLANE_ZORDER
{
    ZORDER_INVALID = 0x7F,
    ZORDER_1       = 0, // lower most plane
    ZORDER_2       = 1,
    ZORDER_3       = 2,
    ZORDER_4       = 3, // upper most plane (BXT)
    ZORDER_5       = 4,
    ZORDER_6       = 5,
    ZORDER_Y1      = ZORDER_6, // Plane 6 maps to Zorder6 which is Y1 plane.
    ZORDER_7       = 6,
    ZORDER_Y2      = ZORDER_7 // Plane 7 maps to Zorder7 which is Y1 plane.
} PLANE_ZORDER;

typedef enum
{
    TRANSCODER_NULL = 0,
    TRANSCODER_EDP,
    TRANSCODER_DSI0,
    TRANSCODER_DSI1,
    TRANSCODER_A,
    TRANSCODER_B,
    TRANSCODER_C,
    TRANSCODER_D,
    MAX_TRANSCODERS
} TRANSCODER_TYPE,
*PTRANSCODER_TYPE;

#define MAX_PHYSICAL_PIPES 4

#define MAX_VIRTUAL_PIPES 1

typedef enum _PIPE_ID
{
    NULL_PIPE = 0x7F,
    PIPE_ANY  = 0x7E,
    PIPE_A    = 0,
    PIPE_B    = 1,
    PIPE_C    = 2,
    PIPE_D    = 3,
    // Start the Virtual pipes at 16 to have a guard band between Physical pipes and virtual pipes
    VIRTUAL_PIPE_START = 16,
    VIRTUAL_PIPE_A     = VIRTUAL_PIPE_START,
    VIRTUAL_PIPE_MAX   = VIRTUAL_PIPE_START + MAX_VIRTUAL_PIPES,

} PIPE_ID,
*PPIPE_ID;

extern unsigned long GETMAXPIPES(void);
#define TPV_PIPE(Index_Num) (Index_Num + GETMAXPIPES())
#define IS_INTEL_PIPE(Index) (((unsigned long)(Index)) < GETMAXPIPES())
#define IS_TPV_PIPE(Index) (((((unsigned long)(Index)) >= GETMAXPIPES()) && Index < NULL_PIPE) ? TRUE : FALSE)
#define RETRIEVE_TPV_PIPE_INDEX_NUM(ulPipeIndex) (ulPipeIndex - GETMAXPIPES())

#define VIRTUAL_PIPE(Index_Num) (Index_Num + VIRTUAL_PIPE_START)
#define IS_PHYSICAL_PIPE(PipeIndex) (((unsigned long)(PipeIndex)) < MAX_PHYSICAL_PIPES)
#define IS_VIRTUAL_PIPE(PipeIndex) ((PipeIndex >= VIRTUAL_PIPE_START && PipeIndex < VIRTUAL_PIPE_MAX) ? TRUE : FALSE)
#define RETRIEVE_VIRTUAL_PIPE_INDEX_NUM(PipeIndex) (PipeIndex - VIRTUAL_PIPE_START)

#define GET_PLANE_FROM_PIPE(ulPipe) ((ulPipe == PIPE_A) ? PLANE_A : (ulPipe == PIPE_B) ? PLANE_B : (ulPipe == PIPE_C) ? PLANE_C : (ulPipe == PIPE_D) ? PLANE_D : NULL_PLANE)
#define MAP_LAYER_INDEX_TO_ZORDER(ulNumPlane, ulLayerIndex) (ulNumPlane - 1 - ulLayerIndex) // 0 - top most layer, bottob most Z-order

#endif // _CHIPSIMC_H_
