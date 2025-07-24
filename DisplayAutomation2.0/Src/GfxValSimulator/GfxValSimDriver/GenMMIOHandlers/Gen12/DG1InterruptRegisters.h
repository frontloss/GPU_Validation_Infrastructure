/*===========================================================================
; DG1InterruptRegisters.h - Gen12DG1 InterruptHandler interface
;----------------------------------------------------------------------------
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
;
;   File Description:
;       This file contains all the InterruptHandler interface function and data structure definitions for GEN12 DG1
;--------------------------------------------------------------------------*/

#ifndef __DG1_INTERRUPT_REGS_H__
#define __DG1_INTERRUPT_REGS_H__

typedef enum _GRAPHICS_MASTER_TILE_INTERRUPT_INSTANCE_DG1
{
    GFX_MSTR_TILE_INTR_ADDR_DG1 = 0x190008,
} GRAPHICS_MASTER_TILE_INTERRUPT_INSTANCE_DG1;

/*************************************************************************************
Description:  Top level register that indicates interrupt from hardware.
Bits in this register are set interrupts are pending in the corresponding GT Tiles

*************************************************************************************/
typedef union _GRAPHICS_MASTER_TILE_INTERRUPT_DG1 {
    struct
    {
        DDU32 Tile0 : DD_BITFIELD_BIT(0);
        DDU32 Tile1 : DD_BITFIELD_BIT(1);
        DDU32 Tile2 : DD_BITFIELD_BIT(2);
        DDU32 Tile3 : DD_BITFIELD_BIT(3);
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(4, 30); // RESERVED
        /* This is the master control for graphics interrupts. This must be enabled for any of these interrupts to propagate to PCI device 2 interrupt processing*/
        DDU32 MasterInterrupt : DD_BITFIELD_BIT(31);
    };
    DDU32 Value;

} GRAPHICS_MASTER_TILE_INTERRUPT_DG1, *PGRAPHICS_MASTER_TILE_INTERRUPT_DG1;

C_ASSERT(4 == sizeof(GRAPHICS_MASTER_TILE_INTERRUPT_DG1));

#define IGT_PAVP_FUSE_2 0x9120

#endif
