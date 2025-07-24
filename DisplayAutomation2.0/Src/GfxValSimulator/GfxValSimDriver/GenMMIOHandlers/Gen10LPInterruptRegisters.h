#ifndef __GEN10LPINTERRUPTREGISTERS_H__
#define __GEN10LPINTERRUPTREGISTERS_H__

/*===========================================================================
; Gen10LpPortInterface.h - Gen10LpPortInterface interface functions
;----------------------------------------------------------------------------
;   Copyright (c) Intel Corporation (2000 - 2017)
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
;       This file contains all the Gen10LpPortInterface related interface functions
;--------------------------------------------------------------------------*/

#include "..//CommonInclude//DisplayDefs.h"

// IMPLICIT ENUMERATIONS USED BY PORT_CL1CM_DW0_GLKd
//
typedef enum _PORT_CL1CM_DW0_A_INSTANCE_GLK
{
    PORT_CL1CM_DW0_A_INSTANCE_ADDRESS_GLK = 0x162000,
} PORT_CL1CM_DW0_A_INSTANCE_GLK;

typedef enum _PORT_CL1CM_DW0_B_INSTANCE_GLK
{
    PORT_CL1CM_DW0_B_INSTANCE_ADDRESS_GLK = 0x6C000,
} PORT_CL1CM_DW0_B_INSTANCE_GLK;

typedef enum _PORT_CL1CM_DW0_C_INSTANCE_GLK
{
    PORT_CL1CM_DW0_C_INSTANCE_ADDRESS_GLK = 0x163000,
} PORT_CL1CM_DW0_C_INSTANCE_GLK;

typedef enum _PORT_CL1CM_DW0_MASKS_GLK
{
    PORT_CL1CM_DW0_MASKS_PBC_GLK = 0xFFF0FFFF,
    PORT_CL1CM_DW0_MASKS_WO_GLK  = 0x0,
    PORT_CL1CM_DW0_MASKS_MBZ_GLK = 0x0,
} PORT_CL1CM_DW0_MASKS_GLK;

/*****************************************************************************\
PHY CL1 Dword 0
Instances per PHY dual/single
DDIA: PHY single, base 0x162000
DDIB/C: PHY dual, base 0x6C000
CL1 common config base 0x0
\*****************************************************************************/
typedef union _PORT_CL1CM_DW0_GLK {
    struct
    {
        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(0, 15); // PBC

        /*****************************************************************************\
        PHY power good status
        \*****************************************************************************/
        DDU32 Iphypwrgood : DD_BITFIELD_BIT(16); //

        /*****************************************************************************\
        PHY power ack status
        \*****************************************************************************/
        DDU32 Iphypwrgack : DD_BITFIELD_BIT(17); //

        /*****************************************************************************\
        status bit to indicate any data lane is powered down
        \*****************************************************************************/
        DDU32 Ianydl_Powerdown : DD_BITFIELD_BIT(18); //

        /*****************************************************************************\
        status bit to indicate all data lanes are powered down
        \*****************************************************************************/
        DDU32 Ialldl_Powerdown : DD_BITFIELD_BIT(19); //

        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(20, 31); // PBC
    };
    DDU32 Value;
} PORT_CL1CM_DW0_GLK;

C_ASSERT(4 == sizeof(PORT_CL1CM_DW0_GLK));

// IMPLICIT ENUMERATIONS USED BY PORT_CL1CM_DW9_GLK
//
typedef enum _PORT_CL1CM_DW9_A_INSTANCE_GLK
{
    PORT_CL1CM_DW9_A_INSTANCE_ADDRESS_GLK = 0x162024,
} PORT_CL1CM_DW9_A_INSTANCE_GLK;

typedef enum _PORT_CL1CM_DW9_B_INSTANCE_GLK
{
    PORT_CL1CM_DW9_B_INSTANCE_ADDRESS_GLK = 0x6C024,
} PORT_CL1CM_DW9_B_INSTANCE_GLK;

typedef enum _PORT_CL1CM_DW9_C_INSTANCE_GLK
{
    PORT_CL1CM_DW9_C_INSTANCE_ADDRESS_GLK = 0x163024,
} PORT_CL1CM_DW9_C_INSTANCE_GLK;

typedef enum _PORT_CL1CM_DW9_MASKS_GLK
{
    PORT_CL1CM_DW9_MASKS_PBC_GLK = 0xFFFF00FF,
    PORT_CL1CM_DW9_MASKS_WO_GLK  = 0x0,
    PORT_CL1CM_DW9_MASKS_MBZ_GLK = 0x0,
} PORT_CL1CM_DW9_MASKS_GLK;

/*****************************************************************************\
PHY CL1 Dword 9
Instances per PHY dual/single
DDIA: PHY single, base 0x162000
DDIB/C: PHY dual, base 0x6C000
CL1 common config base 0x0
\*****************************************************************************/
typedef union _PORT_CL1CM_DW9_GLK {
    struct
    {
        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(0, 7); // PBC
        DDU32 Iref0rcoffset : DD_BITFIELD_RANGE(8, 15);       //

        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(16, 31); // PBC
    };
    DDU32 Value;
} PORT_CL1CM_DW9_GLK;

C_ASSERT(4 == sizeof(PORT_CL1CM_DW9_GLK));

// IMPLICIT ENUMERATIONS USED BY PORT_CL1CM_DW10_GLK
//
typedef enum _PORT_CL1CM_DW10_A_INSTANCE_GLK
{
    PORT_CL1CM_DW10_A_INSTANCE_ADDRESS_GLK = 0x162028,
} PORT_CL1CM_DW10_A_INSTANCE_GLK;

typedef enum _PORT_CL1CM_DW10_B_INSTANCE_GLK
{
    PORT_CL1CM_DW10_B_INSTANCE_ADDRESS_GLK = 0x6C028,
} PORT_CL1CM_DW10_B_INSTANCE_GLK;

typedef enum _PORT_CL1CM_DW10_C_INSTANCE_GLK
{
    PORT_CL1CM_DW10_C_INSTANCE_ADDRESS_GLK = 0x163028,
} PORT_CL1CM_DW10_C_INSTANCE_GLK;

typedef enum _PORT_CL1CM_DW10_MASKS_GLK
{
    PORT_CL1CM_DW10_MASKS_PBC_GLK = 0xFFFF00FF,
    PORT_CL1CM_DW10_MASKS_WO_GLK  = 0x0,
    PORT_CL1CM_DW10_MASKS_MBZ_GLK = 0x0,
} PORT_CL1CM_DW10_MASKS_GLK;

/*****************************************************************************\
PHY CL1 Dword 10
Instances per PHY dual/single
DDIA: PHY single, base 0x162000
DDIB/C: PHY dual, base 0x6C000
CL1 common config base 0x0
\*****************************************************************************/
typedef union _PORT_CL1CM_DW10_GLK {
    struct
    {
        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(0, 7); // PBC
        DDU32 Iref1rcoffset : DD_BITFIELD_RANGE(8, 15);       //

        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(16, 31); // PBC
    };
    DDU32 Value;
} PORT_CL1CM_DW10_GLK;

C_ASSERT(4 == sizeof(PORT_CL1CM_DW10_GLK));

// IMPLICIT ENUMERATIONS USED BY PORT_CL1CM_DW28_GLK
//
typedef enum _PORT_CL1CM_DW28_A_INSTANCE_GLK
{
    PORT_CL1CM_DW28_A_INSTANCE_ADDRESS_GLK = 0x162070,
} PORT_CL1CM_DW28_A_INSTANCE_GLK;

typedef enum _PORT_CL1CM_DW28_B_INSTANCE_GLK
{
    PORT_CL1CM_DW28_B_INSTANCE_ADDRESS_GLK = 0x6C070,
} PORT_CL1CM_DW28_B_INSTANCE_GLK;

typedef enum _PORT_CL1CM_DW28_C_INSTANCE_GLK
{
    PORT_CL1CM_DW28_C_INSTANCE_ADDRESS_GLK = 0x163070,
} PORT_CL1CM_DW28_C_INSTANCE_GLK;

typedef enum _PORT_CL1CM_DW28_MASKS_GLK
{
    PORT_CL1CM_DW28_MASKS_PBC_GLK = 0xFF3FFFFC,
    PORT_CL1CM_DW28_MASKS_WO_GLK  = 0x0,
    PORT_CL1CM_DW28_MASKS_MBZ_GLK = 0x0,
} PORT_CL1CM_DW28_MASKS_GLK;

/*****************************************************************************\
PHY CL1 Dword 28
Instances per PHY dual/single
DDIA: PHY single, base 0x162000
DDIB/C: PHY dual, base 0x6C000
CL1 common config base 0x0
\*****************************************************************************/
typedef union _PORT_CL1CM_DW28_GLK {
    struct
    {
        DDU32 Sus_Clk_Config : DD_BITFIELD_RANGE(0, 1); //

        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(2, 21); // PBC
        DDU32 Oldo_Dynpwrdownen : DD_BITFIELD_BIT(22);         //
        DDU32 Ocl1powerdownen : DD_BITFIELD_BIT(23);           //

        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(24, 31); // PBC
    };
    DDU32 Value;
} PORT_CL1CM_DW28_GLK;

C_ASSERT(4 == sizeof(PORT_CL1CM_DW28_GLK));

// IMPLICIT ENUMERATIONS USED BY PORT_CL1CM_DW30_GLK
//
typedef enum _PORT_CL1CM_DW30_A_INSTANCE_GLK
{
    PORT_CL1CM_DW30_A_INSTANCE_ADDRESS_GLK = 0x162078,
} PORT_CL1CM_DW30_A_INSTANCE_GLK;

typedef enum _PORT_CL1CM_DW30_B_INSTANCE_GLK
{
    PORT_CL1CM_DW30_B_INSTANCE_ADDRESS_GLK = 0x6C078,
} PORT_CL1CM_DW30_B_INSTANCE_GLK;

typedef enum _PORT_CL1CM_DW30_C_INSTANCE_GLK
{
    PORT_CL1CM_DW30_C_INSTANCE_ADDRESS_GLK = 0x163078,
} PORT_CL1CM_DW30_C_INSTANCE_GLK;

typedef enum _PORT_CL1CM_DW30_MASKS_GLK
{
    PORT_CL1CM_DW30_MASKS_PBC_GLK = 0xFFFFFFBF,
    PORT_CL1CM_DW30_MASKS_WO_GLK  = 0x0,
    PORT_CL1CM_DW30_MASKS_MBZ_GLK = 0x0,
} PORT_CL1CM_DW30_MASKS_GLK;

/*****************************************************************************\
PHY CL1 Dword 30
Instances per PHY dual/single
DDIA: PHY single, base 0x162000
DDIB/C: PHY dual, base 0x6C000
CL1 common config base 0x0
\*****************************************************************************/
typedef union _PORT_CL1CM_DW30_GLK {
    struct
    {
        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(0, 5); // PBC
        DDU32 Ocl2_Ldofuse_Pwrenb : DD_BITFIELD_BIT(6);       //

        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(7, 31); // PBC
    };
    DDU32 Value;
} PORT_CL1CM_DW30_GLK;

C_ASSERT(4 == sizeof(PORT_CL1CM_DW30_GLK));

// IMPLICIT ENUMERATIONS USED BY PORT_TX_DW2_GLK
//
typedef enum _PORT_TX_DW2_LN0_A_INSTANCE_GLK
{
    PORT_TX_DW2_LN0_A_INSTANCE_ADDRESS_GLK = 0x162508,
} PORT_TX_DW2_LN0_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW2_LN1_A_INSTANCE_GLK
{
    PORT_TX_DW2_LN1_A_INSTANCE_ADDRESS_GLK = 0x162588,
} PORT_TX_DW2_LN1_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW2_LN2_A_INSTANCE_GLK
{
    PORT_TX_DW2_LN2_A_INSTANCE_ADDRESS_GLK = 0x162708,
} PORT_TX_DW2_LN2_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW2_LN3_A_INSTANCE_GLK
{
    PORT_TX_DW2_LN3_A_INSTANCE_ADDRESS_GLK = 0x162788,
} PORT_TX_DW2_LN3_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW2_GRP_A_INSTANCE_GLK
{
    PORT_TX_DW2_GRP_A_INSTANCE_ADDRESS_GLK = 0x162D08,
} PORT_TX_DW2_GRP_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW2_LN0_B_INSTANCE_GLK
{
    PORT_TX_DW2_LN0_B_INSTANCE_ADDRESS_GLK = 0x6C508,
} PORT_TX_DW2_LN0_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW2_LN1_B_INSTANCE_GLK
{
    PORT_TX_DW2_LN1_B_INSTANCE_ADDRESS_GLK = 0x6C588,
} PORT_TX_DW2_LN1_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW2_LN2_B_INSTANCE_GLK
{
    PORT_TX_DW2_LN2_B_INSTANCE_ADDRESS_GLK = 0x6C708,
} PORT_TX_DW2_LN2_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW2_LN3_B_INSTANCE_GLK
{
    PORT_TX_DW2_LN3_B_INSTANCE_ADDRESS_GLK = 0x6C788,
} PORT_TX_DW2_LN3_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW2_GRP_B_INSTANCE_GLK
{
    PORT_TX_DW2_GRP_B_INSTANCE_ADDRESS_GLK = 0x6CD08,
} PORT_TX_DW2_GRP_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW2_LN0_C_INSTANCE_GLK
{
    PORT_TX_DW2_LN0_C_INSTANCE_ADDRESS_GLK = 0x163508,
} PORT_TX_DW2_LN0_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW2_LN1_C_INSTANCE_GLK
{
    PORT_TX_DW2_LN1_C_INSTANCE_ADDRESS_GLK = 0x163588,
} PORT_TX_DW2_LN1_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW2_LN2_C_INSTANCE_GLK
{
    PORT_TX_DW2_LN2_C_INSTANCE_ADDRESS_GLK = 0x163708,
} PORT_TX_DW2_LN2_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW2_LN3_C_INSTANCE_GLK
{
    PORT_TX_DW2_LN3_C_INSTANCE_ADDRESS_GLK = 0x163788,
} PORT_TX_DW2_LN3_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW2_GRP_C_INSTANCE_GLK
{
    PORT_TX_DW2_GRP_C_INSTANCE_ADDRESS_GLK = 0x163D08,
} PORT_TX_DW2_GRP_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW2_MASKS_GLK
{
    PORT_TX_DW2_MASKS_PBC_GLK = 0xFF0000FF,
    PORT_TX_DW2_MASKS_WO_GLK  = 0x0,
    PORT_TX_DW2_MASKS_MBZ_GLK = 0x0,
} PORT_TX_DW2_MASKS_GLK;

/*****************************************************************************\
PHY TX Dword 2
Instances per lane 0-3, per channel 0-1, and per PHY dual/single
DDIA: lane 0-3, channel 0, PHY single, base 0x162000
DDIB: lane 0-3, channel 0, PHY dual, base 0x6C000
DDIC: lane 0-3, channel 1, PHY dual, base 0x6C000
Channel0 Lane0 0x500
Channel0 Lane1 0x580
Channel0 Lane2 0x700
Channel0 Lane3 0x780

Channel1 Lane0 0x900
Channel1 Lane1 0x980
Channel1 Lane2 0xB00
Channel1 Lane3 0xB80

Channel0 Group access 0xD00
Channel1 Group access 0xF00
\*****************************************************************************/
typedef union _PORT_TX_DW2_GLK {
    struct
    {
        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(0, 7); // PBC
        DDU32 Ouniqtranscale : DD_BITFIELD_RANGE(8, 15);      //
        DDU32 Omargin000 : DD_BITFIELD_RANGE(16, 23);         //

        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(24, 31); // PBC
    };
    DDU32 Value;
} PORT_TX_DW2_GLK;

C_ASSERT(4 == sizeof(PORT_TX_DW2_GLK));

// IMPLICIT ENUMERATIONS USED BY PORT_TX_DW3_GLK
//
typedef enum _PORT_TX_DW3_LN0_A_INSTANCE_GLK
{
    PORT_TX_DW3_LN0_A_INSTANCE_ADDRESS_GLK = 0x16250C,
} PORT_TX_DW3_LN0_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW3_LN1_A_INSTANCE_GLK
{
    PORT_TX_DW3_LN1_A_INSTANCE_ADDRESS_GLK = 0x16258C,
} PORT_TX_DW3_LN1_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW3_LN2_A_INSTANCE_GLK
{
    PORT_TX_DW3_LN2_A_INSTANCE_ADDRESS_GLK = 0x16270C,
} PORT_TX_DW3_LN2_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW3_LN3_A_INSTANCE_GLK
{
    PORT_TX_DW3_LN3_A_INSTANCE_ADDRESS_GLK = 0x16278C,
} PORT_TX_DW3_LN3_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW3_GRP_A_INSTANCE_GLK
{
    PORT_TX_DW3_GRP_A_INSTANCE_ADDRESS_GLK = 0x162D0C,
} PORT_TX_DW3_GRP_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW3_LN0_B_INSTANCE_GLK
{
    PORT_TX_DW3_LN0_B_INSTANCE_ADDRESS_GLK = 0x6C50C,
} PORT_TX_DW3_LN0_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW3_LN1_B_INSTANCE_GLK
{
    PORT_TX_DW3_LN1_B_INSTANCE_ADDRESS_GLK = 0x6C58C,
} PORT_TX_DW3_LN1_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW3_LN2_B_INSTANCE_GLK
{
    PORT_TX_DW3_LN2_B_INSTANCE_ADDRESS_GLK = 0x6C70C,
} PORT_TX_DW3_LN2_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW3_LN3_B_INSTANCE_GLK
{
    PORT_TX_DW3_LN3_B_INSTANCE_ADDRESS_GLK = 0x6C78C,
} PORT_TX_DW3_LN3_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW3_GRP_B_INSTANCE_GLK
{
    PORT_TX_DW3_GRP_B_INSTANCE_ADDRESS_GLK = 0x6CD0C,
} PORT_TX_DW3_GRP_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW3_LN0_C_INSTANCE_GLK
{
    PORT_TX_DW3_LN0_C_INSTANCE_ADDRESS_GLK = 0x16350C,
} PORT_TX_DW3_LN0_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW3_LN1_C_INSTANCE_GLK
{
    PORT_TX_DW3_LN1_C_INSTANCE_ADDRESS_GLK = 0x16358C,
} PORT_TX_DW3_LN1_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW3_LN2_C_INSTANCE_GLK
{
    PORT_TX_DW3_LN2_C_INSTANCE_ADDRESS_GLK = 0x16370C,
} PORT_TX_DW3_LN2_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW3_LN3_C_INSTANCE_GLK
{
    PORT_TX_DW3_LN3_C_INSTANCE_ADDRESS_GLK = 0x16378C,
} PORT_TX_DW3_LN3_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW3_GRP_C_INSTANCE_GLK
{
    PORT_TX_DW3_GRP_C_INSTANCE_ADDRESS_GLK = 0x163D0C,
} PORT_TX_DW3_GRP_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW3_MASKS_GLK
{
    PORT_TX_DW3_MASKS_PBC_GLK = 0xF3FFFFFF,
    PORT_TX_DW3_MASKS_WO_GLK  = 0x0,
    PORT_TX_DW3_MASKS_MBZ_GLK = 0x0,
} PORT_TX_DW3_MASKS_GLK;

/*****************************************************************************\
PHY TX Dword 3
Instances per lane 0-3, per channel 0-1, and per PHY dual/single
DDIA: lane 0-3, channel 0, PHY single, base 0x162000
DDIB: lane 0-3, channel 0, PHY dual, base 0x6C000
DDIC: lane 0-3, channel 1, PHY dual, base 0x6C000
Channel0 Lane0 0x500
Channel0 Lane1 0x580
Channel0 Lane2 0x700
Channel0 Lane3 0x780

Channel1 Lane0 0x900
Channel1 Lane1 0x980
Channel1 Lane2 0xB00
Channel1 Lane3 0xB80

Channel0 Group access 0xD00
Channel1 Group access 0xF00
\*****************************************************************************/
typedef union _PORT_TX_DW3_GLK {
    struct
    {
        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(0, 25); // PBC
        DDU32 Oscaledcompmethod : DD_BITFIELD_BIT(26);         //
        DDU32 Ouniqetrangenmethod : DD_BITFIELD_BIT(27);       //

        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(28, 31); // PBC
    };
    DDU32 Value;
} PORT_TX_DW3_GLK;

C_ASSERT(4 == sizeof(PORT_TX_DW3_GLK));

// IMPLICIT ENUMERATIONS USED BY PORT_TX_DW4_GLK
//
typedef enum _PORT_TX_DW4_LN0_A_INSTANCE_GLK
{
    PORT_TX_DW4_LN0_A_INSTANCE_ADDRESS_GLK = 0x162510,
} PORT_TX_DW4_LN0_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW4_LN1_A_INSTANCE_GLK
{
    PORT_TX_DW4_LN1_A_INSTANCE_ADDRESS_GLK = 0x162590,
} PORT_TX_DW4_LN1_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW4_LN2_A_INSTANCE_GLK
{
    PORT_TX_DW4_LN2_A_INSTANCE_ADDRESS_GLK = 0x162710,
} PORT_TX_DW4_LN2_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW4_LN3_A_INSTANCE_GLK
{
    PORT_TX_DW4_LN3_A_INSTANCE_ADDRESS_GLK = 0x162790,
} PORT_TX_DW4_LN3_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW4_GRP_A_INSTANCE_GLK
{
    PORT_TX_DW4_GRP_A_INSTANCE_ADDRESS_GLK = 0x162D10,
} PORT_TX_DW4_GRP_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW4_LN0_B_INSTANCE_GLK
{
    PORT_TX_DW4_LN0_B_INSTANCE_ADDRESS_GLK = 0x6C510,
} PORT_TX_DW4_LN0_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW4_LN1_B_INSTANCE_GLK
{
    PORT_TX_DW4_LN1_B_INSTANCE_ADDRESS_GLK = 0x6C590,
} PORT_TX_DW4_LN1_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW4_LN2_B_INSTANCE_GLK
{
    PORT_TX_DW4_LN2_B_INSTANCE_ADDRESS_GLK = 0x6C710,
} PORT_TX_DW4_LN2_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW4_LN3_B_INSTANCE_GLK
{
    PORT_TX_DW4_LN3_B_INSTANCE_ADDRESS_GLK = 0x6C790,
} PORT_TX_DW4_LN3_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW4_GRP_B_INSTANCE_GLK
{
    PORT_TX_DW4_GRP_B_INSTANCE_ADDRESS_GLK = 0x6CD10,
} PORT_TX_DW4_GRP_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW4_LN0_C_INSTANCE_GLK
{
    PORT_TX_DW4_LN0_C_INSTANCE_ADDRESS_GLK = 0x163510,
} PORT_TX_DW4_LN0_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW4_LN1_C_INSTANCE_GLK
{
    PORT_TX_DW4_LN1_C_INSTANCE_ADDRESS_GLK = 0x163590,
} PORT_TX_DW4_LN1_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW4_LN2_C_INSTANCE_GLK
{
    PORT_TX_DW4_LN2_C_INSTANCE_ADDRESS_GLK = 0x163710,
} PORT_TX_DW4_LN2_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW4_LN3_C_INSTANCE_GLK
{
    PORT_TX_DW4_LN3_C_INSTANCE_ADDRESS_GLK = 0x163790,
} PORT_TX_DW4_LN3_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW4_GRP_C_INSTANCE_GLK
{
    PORT_TX_DW4_GRP_C_INSTANCE_ADDRESS_GLK = 0x163D10,
} PORT_TX_DW4_GRP_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW4_MASKS_GLK
{
    PORT_TX_DW4_MASKS_WO_GLK  = 0x0,
    PORT_TX_DW4_MASKS_MBZ_GLK = 0x0,
    PORT_TX_DW4_MASKS_PBC_GLK = 0xFFFFFF,
} PORT_TX_DW4_MASKS_GLK;

/*****************************************************************************\
PHY TX Dword 4
Instances per lane 0-3, per channel 0-1, and per PHY dual/single
DDIA: lane 0-3, channel 0, PHY single, base 0x162000
DDIB: lane 0-3, channel 0, PHY dual, base 0x6C000
DDIC: lane 0-3, channel 1, PHY dual, base 0x6C000
Channel0 Lane0 0x500
Channel0 Lane1 0x580
Channel0 Lane2 0x700
Channel0 Lane3 0x780

Channel1 Lane0 0x900
Channel1 Lane1 0x980
Channel1 Lane2 0xB00
Channel1 Lane3 0xB80

Channel0 Group access 0xD00
Channel1 Group access 0xF00
\*****************************************************************************/
typedef union _PORT_TX_DW4_GLK {
    struct
    {
        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(0, 23); // PBC
        DDU32 Ow2tapdeemph9p5 : DD_BITFIELD_RANGE(24, 31);     //
    };
    DDU32 Value;
} PORT_TX_DW4_GLK;

C_ASSERT(4 == sizeof(PORT_TX_DW4_GLK));

// IMPLICIT ENUMERATIONS USED BY PORT_TX_DW5_GLK
//
typedef enum _RESETDATA_L_GLK
{
    OVRD_RESETDATA_L_UNNAMED_1_GLK = 0x1,
} OVRD_RESETDATA_L_GLK;

typedef enum _SETDATA_L_GLK
{
    OVRD_SETDATA_L_UNNAMED_1_GLK = 0x1,
} OVRD_SETDATA_L_GLK;

typedef enum _RESETDATA_H_GLK
{
    OVRD_RESETDATA_H_UNNAMED_1_GLK = 0x1,
} OVRD_RESETDATA_H_GLK;

typedef enum _SETDATA_H_GLK
{
    OVRD_SETDATA_H_UNNAMED_1_GLK = 0x1,
} OVRD_SETDATA_H_GLK;

typedef enum _PORT_TX_DW5_LN0_A_INSTANCE_GLK
{
    PORT_TX_DW5_LN0_A_INSTANCE_ADDRESS_GLK = 0x162514,
} PORT_TX_DW5_LN0_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW5_LN1_A_INSTANCE_GLK
{
    PORT_TX_DW5_LN1_A_INSTANCE_ADDRESS_GLK = 0x162594,
} PORT_TX_DW5_LN1_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW5_LN2_A_INSTANCE_GLK
{
    PORT_TX_DW5_LN2_A_INSTANCE_ADDRESS_GLK = 0x162714,
} PORT_TX_DW5_LN2_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW5_LN3_A_INSTANCE_GLK
{
    PORT_TX_DW5_LN3_A_INSTANCE_ADDRESS_GLK = 0x162794,
} PORT_TX_DW5_LN3_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW5_GRP_A_INSTANCE_GLK
{
    PORT_TX_DW5_GRP_A_INSTANCE_ADDRESS_GLK = 0x162D14,
} PORT_TX_DW5_GRP_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW5_LN0_B_INSTANCE_GLK
{
    PORT_TX_DW5_LN0_B_INSTANCE_ADDRESS_GLK = 0x6C514,
} PORT_TX_DW5_LN0_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW5_LN1_B_INSTANCE_GLK
{
    PORT_TX_DW5_LN1_B_INSTANCE_ADDRESS_GLK = 0x6C594,
} PORT_TX_DW5_LN1_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW5_LN2_B_INSTANCE_GLK
{
    PORT_TX_DW5_LN2_B_INSTANCE_ADDRESS_GLK = 0x6C714,
} PORT_TX_DW5_LN2_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW5_LN3_B_INSTANCE_GLK
{
    PORT_TX_DW5_LN3_B_INSTANCE_ADDRESS_GLK = 0x6C794,
} PORT_TX_DW5_LN3_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW5_GRP_B_INSTANCE_GLK
{
    PORT_TX_DW5_GRP_B_INSTANCE_ADDRESS_GLK = 0x6CD14,
} PORT_TX_DW5_GRP_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW5_LN0_C_INSTANCE_GLK
{
    PORT_TX_DW5_LN0_C_INSTANCE_ADDRESS_GLK = 0x163514,
} PORT_TX_DW5_LN0_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW5_LN1_C_INSTANCE_GLK
{
    PORT_TX_DW5_LN1_C_INSTANCE_ADDRESS_GLK = 0x163594,
} PORT_TX_DW5_LN1_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW5_LN2_C_INSTANCE_GLK
{
    PORT_TX_DW5_LN2_C_INSTANCE_ADDRESS_GLK = 0x163714,
} PORT_TX_DW5_LN2_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW5_LN3_C_INSTANCE_GLK
{
    PORT_TX_DW5_LN3_C_INSTANCE_ADDRESS_GLK = 0x163794,
} PORT_TX_DW5_LN3_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW5_GRP_C_INSTANCE_GLK
{
    PORT_TX_DW5_GRP_C_INSTANCE_ADDRESS_GLK = 0x163D14,
} PORT_TX_DW5_GRP_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW5_MASKS_GLK
{
    PORT_TX_DW5_MASKS_WO_GLK  = 0x0,
    PORT_TX_DW5_MASKS_PBC_GLK = 0x0,
    PORT_TX_DW5_MASKS_MBZ_GLK = 0x3F80F0FF,
} PORT_TX_DW5_MASKS_GLK;

typedef union _PORT_TX_DW5_GLK {
    struct
    {
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(0, 7); // MBZ

        /*****************************************************************************\
        Adjust DCC delay range to 2nd setting
        \*****************************************************************************/
        DDU32 DccDelayRange2 : DD_BITFIELD_BIT(8); //

        /*****************************************************************************\
        Adjust DCC delay range to 1st setting
        \*****************************************************************************/
        DDU32 DccDelayRange1 : DD_BITFIELD_BIT(9); //

        /*****************************************************************************\
        Invert the DCC compout polarity
        \*****************************************************************************/
        DDU32 DccCompoutPolarity : DD_BITFIELD_BIT(10);         //
        DDU32 Otxclkspare : DD_BITFIELD_BIT(11);                //
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(12, 15); // MBZ
        DDU32 Ovrd_Dccmode : DD_BITFIELD_BIT(16);               //
        DDU32 Ovrd_Dfxbypassen : DD_BITFIELD_BIT(17);           //
        DDU32 Ovrd_Dcc1010en : DD_BITFIELD_BIT(18);             //
        DDU32 Ovrd_Resetdata_L : DD_BITFIELD_BIT(19);           // OVRD_RESETDATA_L_GLK
        DDU32 Ovrd_Setdata_L : DD_BITFIELD_BIT(20);             // OVRD_SETDATA_L_GLK
        DDU32 Ovrd_Resetdata_H : DD_BITFIELD_BIT(21);           // OVRD_RESETDATA_H_GLK
        DDU32 Ovrd_Setdata_H : DD_BITFIELD_BIT(22);             // OVRD_SETDATA_H_GLK
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(23, 29); // MBZ
        DDU32 Ocalccont : DD_BITFIELD_BIT(30);                  //
        DDU32 Ocalcinit : DD_BITFIELD_BIT(31);                  //
    };
    DDU32 Value;
} PORT_TX_DW5_GLK;

C_ASSERT(4 == sizeof(PORT_TX_DW5_GLK));

// IMPLICIT ENUMERATIONS USED BY PORT_TX_DW14_GLK
//
typedef enum _PORT_TX_DW14_LN0_A_INSTANCE_GLK
{
    PORT_TX_DW14_LN0_A_INSTANCE_ADDRESS_GLK = 0x162538,
} PORT_TX_DW14_LN0_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW14_LN1_A_INSTANCE_GLK
{
    PORT_TX_DW14_LN1_A_INSTANCE_ADDRESS_GLK = 0x1625B8,
} PORT_TX_DW14_LN1_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW14_LN2_A_INSTANCE_GLK
{
    PORT_TX_DW14_LN2_A_INSTANCE_ADDRESS_GLK = 0x162738,
} PORT_TX_DW14_LN2_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW14_LN3_A_INSTANCE_GLK
{
    PORT_TX_DW14_LN3_A_INSTANCE_ADDRESS_GLK = 0x1627B8,
} PORT_TX_DW14_LN3_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW14_GRP_A_INSTANCE_GLK
{
    PORT_TX_DW14_GRP_A_INSTANCE_ADDRESS_GLK = 0x162D38,
} PORT_TX_DW14_GRP_A_INSTANCE_GLK;

typedef enum _PORT_TX_DW14_LN0_B_INSTANCE_GLK
{
    PORT_TX_DW14_LN0_B_INSTANCE_ADDRESS_GLK = 0x6C538,
} PORT_TX_DW14_LN0_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW14_LN1_B_INSTANCE_GLK
{
    PORT_TX_DW14_LN1_B_INSTANCE_ADDRESS_GLK = 0x6C5B8,
} PORT_TX_DW14_LN1_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW14_LN2_B_INSTANCE_GLK
{
    PORT_TX_DW14_LN2_B_INSTANCE_ADDRESS_GLK = 0x6C738,
} PORT_TX_DW14_LN2_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW14_LN3_B_INSTANCE_GLK
{
    PORT_TX_DW14_LN3_B_INSTANCE_ADDRESS_GLK = 0x6C7B8,
} PORT_TX_DW14_LN3_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW14_GRP_B_INSTANCE_GLK
{
    PORT_TX_DW14_GRP_B_INSTANCE_ADDRESS_GLK = 0x6CD38,
} PORT_TX_DW14_GRP_B_INSTANCE_GLK;

typedef enum _PORT_TX_DW14_LN0_C_INSTANCE_GLK
{
    PORT_TX_DW14_LN0_C_INSTANCE_ADDRESS_GLK = 0x163538,
} PORT_TX_DW14_LN0_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW14_LN1_C_INSTANCE_GLK
{
    PORT_TX_DW14_LN1_C_INSTANCE_ADDRESS_GLK = 0x1635B8,
} PORT_TX_DW14_LN1_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW14_LN2_C_INSTANCE_GLK
{
    PORT_TX_DW14_LN2_C_INSTANCE_ADDRESS_GLK = 0x163738,
} PORT_TX_DW14_LN2_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW14_LN3_C_INSTANCE_GLK
{
    PORT_TX_DW14_LN3_C_INSTANCE_ADDRESS_GLK = 0x1637B8,
} PORT_TX_DW14_LN3_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW14_GRP_C_INSTANCE_GLK
{
    PORT_TX_DW14_GRP_C_INSTANCE_ADDRESS_GLK = 0x163D38,
} PORT_TX_DW14_GRP_C_INSTANCE_GLK;

typedef enum _PORT_TX_DW14_MASKS_GLK
{
    PORT_TX_DW14_MASKS_PBC_GLK = 0xBFFFFFFF,
    PORT_TX_DW14_MASKS_WO_GLK  = 0x0,
    PORT_TX_DW14_MASKS_MBZ_GLK = 0x0,
} PORT_TX_DW14_MASKS_GLK;

typedef union _PORT_TX_DW14_GLK {
    struct
    {
        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(0, 29); // PBC
        DDU32 Latency_Optim : DD_BITFIELD_BIT(30);             //

        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(31); // PBC
    };
    DDU32 Value;
} PORT_TX_DW14_GLK;

C_ASSERT(4 == sizeof(PORT_TX_DW14_GLK));

// IMPLICIT ENUMERATIONS USED BY PORT_PCS_DW10_GLK
//
typedef enum _PORT_PCS_DW10_LN01_A_INSTANCE_GLK
{
    PORT_PCS_DW10_LN01_A_INSTANCE_ADDRESS_GLK = 0x162428,
} PORT_PCS_DW10_LN01_A_INSTANCE_GLK;

typedef enum _PORT_PCS_DW10_LN23_A_INSTANCE_GLK
{
    PORT_PCS_DW10_LN23_A_INSTANCE_ADDRESS_GLK = 0x162628,
} PORT_PCS_DW10_LN23_A_INSTANCE_GLK;

typedef enum _PORT_PCS_DW10_GRP_A_INSTANCE_GLK
{
    PORT_PCS_DW10_GRP_A_INSTANCE_ADDRESS_GLK = 0x162C28,
} PORT_PCS_DW10_GRP_A_INSTANCE_GLK;

typedef enum _PORT_PCS_DW10_LN01_B_INSTANCE_GLK
{
    PORT_PCS_DW10_LN01_B_INSTANCE_ADDRESS_GLK = 0x6C428,
} PORT_PCS_DW10_LN01_B_INSTANCE_GLK;

typedef enum _PORT_PCS_DW10_LN23_B_INSTANCE_GLK
{
    PORT_PCS_DW10_LN23_B_INSTANCE_ADDRESS_GLK = 0x6C628,
} PORT_PCS_DW10_LN23_B_INSTANCE_GLK;

typedef enum _PORT_PCS_DW10_GRP_B_INSTANCE_GLK
{
    PORT_PCS_DW10_GRP_B_INSTANCE_ADDRESS_GLK = 0x6CC28,
} PORT_PCS_DW10_GRP_B_INSTANCE_GLK;

typedef enum _PORT_PCS_DW10_LN01_C_INSTANCE_GLK
{
    PORT_PCS_DW10_LN01_C_INSTANCE_ADDRESS_GLK = 0x163428,
} PORT_PCS_DW10_LN01_C_INSTANCE_GLK;

typedef enum _PORT_PCS_DW10_LN23_C_INSTANCE_GLK
{
    PORT_PCS_DW10_LN23_C_INSTANCE_ADDRESS_GLK = 0x163628,
} PORT_PCS_DW10_LN23_C_INSTANCE_GLK;

typedef enum _PORT_PCS_DW10_GRP_C_INSTANCE_GLK
{
    PORT_PCS_DW10_GRP_C_INSTANCE_ADDRESS_GLK = 0x163C28,
} PORT_PCS_DW10_GRP_C_INSTANCE_GLK;

typedef enum _PORT_PCS_DW10_MASKS_GLK
{
    PORT_PCS_DW10_MASKS_WO_GLK  = 0x0,
    PORT_PCS_DW10_MASKS_PBC_GLK = 0xFFFFFF,
    PORT_PCS_DW10_MASKS_MBZ_GLK = 0x3C000000,
} PORT_PCS_DW10_MASKS_GLK;

/*****************************************************************************\
Refer to CRI register map in DDI.
\*****************************************************************************/
typedef union _PORT_PCS_DW10_GLK {
    struct
    {
        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(0, 23);  // PBC
        DDU32 Reg_Tx2deemp : DD_BITFIELD_BIT(24);               //
        DDU32 Reg_Tx1deemp : DD_BITFIELD_BIT(25);               //
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(26, 29); // MBZ
        DDU32 Reg_Tx1swingcalcinit : DD_BITFIELD_BIT(30);       //
        DDU32 Reg_Tx2swingcalcinit : DD_BITFIELD_BIT(31);       //
    };
    DDU32 Value;
} PORT_PCS_DW10_GLK;

C_ASSERT(4 == sizeof(PORT_PCS_DW10_GLK));

// IMPLICIT ENUMERATIONS USED BY PORT_PCS_DW12_GLK
//
typedef enum _REG_LANESTAGGER_STRAP_GLK
{
    REG_LANESTAGGER_STRAP_2_GLK  = 0x2,  // Symbol rate 25 to 33 MHz
    REG_LANESTAGGER_STRAP_4_GLK  = 0x4,  // Symbol rate 34 to 67 MHz
    REG_LANESTAGGER_STRAP_7_GLK  = 0x7,  // Symbol rate 68 to 135 MHz
    REG_LANESTAGGER_STRAP_13_GLK = 0xD,  // Symbol rate 136 to 270 MHz
    REG_LANESTAGGER_STRAP_24_GLK = 0x18, // Symbol rate 271 to 540 MHz
} REG_LANESTAGGER_STRAP_GLK;

typedef enum _REG_TX1_STAGGER_MULT_GLK
{
    REG_TX1_STAGGER_MULT_0X_GLK  = 0x0,
    REG_TX1_STAGGER_MULT_1X_GLK  = 0x1,
    REG_TX1_STAGGER_MULT_2X_GLK  = 0x2,
    REG_TX1_STAGGER_MULT_4X_GLK  = 0x3,
    REG_TX1_STAGGER_MULT_8X_GLK  = 0x4,
    REG_TX1_STAGGER_MULT_16X_GLK = 0x5,
    REG_TX1_STAGGER_MULT_32X_GLK = 0x6,
    REG_TX1_STAGGER_MULT_64X_GLK = 0x7,
} REG_TX1_STAGGER_MULT_GLK;

typedef enum _REG_TX2_STAGGER_MULT_GLK
{
    REG_TX2_STAGGER_MULT_0X_GLK  = 0x0,
    REG_TX2_STAGGER_MULT_1X_GLK  = 0x1,
    REG_TX2_STAGGER_MULT_2X_GLK  = 0x2,
    REG_TX2_STAGGER_MULT_4X_GLK  = 0x3,
    REG_TX2_STAGGER_MULT_8X_GLK  = 0x4,
    REG_TX2_STAGGER_MULT_16X_GLK = 0x5,
    REG_TX2_STAGGER_MULT_32X_GLK = 0x6,
    REG_TX2_STAGGER_MULT_64X_GLK = 0x7,
} REG_TX2_STAGGER_MULT_GLK;

typedef enum _PORT_PCS_DW12_LN01_A_INSTANCE_GLK
{
    PORT_PCS_DW12_LN01_A_INSTANCE_ADDRESS_GLK = 0x162430,
} PORT_PCS_DW12_LN01_A_INSTANCE_GLK;

typedef enum _PORT_PCS_DW12_LN23_A_INSTANCE_GLK
{
    PORT_PCS_DW12_LN23_A_INSTANCE_ADDRESS_GLK = 0x162630,
} PORT_PCS_DW12_LN23_A_INSTANCE_GLK;

typedef enum _PORT_PCS_DW12_GRP_A_INSTANCE_GLK
{
    PORT_PCS_DW12_GRP_A_INSTANCE_ADDRESS_GLK = 0x162C30,
} PORT_PCS_DW12_GRP_A_INSTANCE_GLK;

typedef enum _PORT_PCS_DW12_LN01_B_INSTANCE_GLK
{
    PORT_PCS_DW12_LN01_B_INSTANCE_ADDRESS_GLK = 0x6C430,
} PORT_PCS_DW12_LN01_B_INSTANCE_GLK;

typedef enum _PORT_PCS_DW12_LN23_B_INSTANCE_GLK
{
    PORT_PCS_DW12_LN23_B_INSTANCE_ADDRESS_GLK = 0x6C630,
} PORT_PCS_DW12_LN23_B_INSTANCE_GLK;

typedef enum _PORT_PCS_DW12_GRP_B_INSTANCE_GLK
{
    PORT_PCS_DW12_GRP_B_INSTANCE_ADDRESS_GLK = 0x6CC30,
} PORT_PCS_DW12_GRP_B_INSTANCE_GLK;

typedef enum _PORT_PCS_DW12_LN01_C_INSTANCE_GLK
{
    PORT_PCS_DW12_LN01_C_INSTANCE_ADDRESS_GLK = 0x163430,
} PORT_PCS_DW12_LN01_C_INSTANCE_GLK;

typedef enum _PORT_PCS_DW12_LN23_C_INSTANCE_GLK
{
    PORT_PCS_DW12_LN23_C_INSTANCE_ADDRESS_GLK = 0x163630,
} PORT_PCS_DW12_LN23_C_INSTANCE_GLK;

typedef enum _PORT_PCS_DW12_GRP_C_INSTANCE_GLK
{
    PORT_PCS_DW12_GRP_C_INSTANCE_ADDRESS_GLK = 0x163C30,
} PORT_PCS_DW12_GRP_C_INSTANCE_GLK;

typedef enum _PORT_PCS_DW12_MASKS_GLK
{
    PORT_PCS_DW12_MASKS_MBZ_GLK = 0xFF80FFA0,
    PORT_PCS_DW12_MASKS_WO_GLK  = 0x0,
    PORT_PCS_DW12_MASKS_PBC_GLK = 0x0,
} PORT_PCS_DW12_MASKS_GLK;

/*****************************************************************************\
Refer to Geminilake CRI register map section under DDI.
\*****************************************************************************/
typedef union _PORT_PCS_DW12_GLK {
    struct
    {
        DDU32 Reg_Lanestagger_Strap : DD_BITFIELD_RANGE(0, 4); // REG_LANESTAGGER_STRAP_GLK
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(5);       // MBZ
        DDU32 Reg_Lanestagger_Strap_Ovrd : DD_BITFIELD_BIT(6); //
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(7, 15); // MBZ

        /*****************************************************************************\
        These bits set the lane staggering multiplier for the transmitter based on the linkclk period.
        \*****************************************************************************/
        DDU32 Reg_Tx1_Stagger_Mult : DD_BITFIELD_RANGE(16, 18); // REG_TX1_STAGGER_MULT_GLK
        DDU32 Reg_Lanestagger_By_Group : DD_BITFIELD_BIT(19);   //

        /*****************************************************************************\
        These bits set the lane staggering multiplier for the transmitter based on the linkclk period.
        \*****************************************************************************/
        DDU32 Reg_Tx2_Stagger_Mult : DD_BITFIELD_RANGE(20, 22); // REG_TX2_STAGGER_MULT_GLK
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(23, 31); // MBZ
    };
    DDU32 Value;
} PORT_PCS_DW12_GLK;

C_ASSERT(4 == sizeof(PORT_PCS_DW12_GLK));

// IMPLICIT ENUMERATIONS USED BY PORT_REF_DW3_GLK
//
typedef enum _PORT_REF_DW3_A_INSTANCE_GLK
{
    PORT_REF_DW3_A_INSTANCE_ADDRESS_GLK = 0x16218C,
} PORT_REF_DW3_A_INSTANCE_GLK;

typedef enum _PORT_REF_DW3_B_INSTANCE_GLK
{
    PORT_REF_DW3_B_INSTANCE_ADDRESS_GLK = 0x6C18C,
} PORT_REF_DW3_B_INSTANCE_GLK;

typedef enum _PORT_REF_DW3_C_INSTANCE_GLK
{
    PORT_REF_DW3_C_INSTANCE_ADDRESS_GLK = 0x16318C,
} PORT_REF_DW3_C_INSTANCE_GLK;

typedef enum _PORT_REF_DW3_MASKS_GLK
{
    PORT_REF_DW3_MASKS_PBC_GLK = 0xFFBFFFFF,
    PORT_REF_DW3_MASKS_WO_GLK  = 0x0,
    PORT_REF_DW3_MASKS_MBZ_GLK = 0x0,
} PORT_REF_DW3_MASKS_GLK;

/*****************************************************************************\
PHY Ref Dword 3
Instances per PHY dual/single
DDIA: PHY single, base 0x162000
DDIB/C: PHY dual, base 0x6C000
CL1 Ref base 0x180
\*****************************************************************************/
typedef union _PORT_REF_DW3_GLK {
    struct
    {
        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(0, 21); // PBC
        DDU32 Grc_Done : DD_BITFIELD_BIT(22);                  //

        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(23, 31); // PBC
    };
    DDU32 Value;
} PORT_REF_DW3_GLK;

C_ASSERT(4 == sizeof(PORT_REF_DW3_GLK));

// IMPLICIT ENUMERATIONS USED BY PORT_CL2CM_DW6_GLK
//
typedef enum _PORT_CL2CM_DW6_A_INSTANCE_GLK
{
    PORT_CL2CM_DW6_A_INSTANCE_ADDRESS_GLK = 0x162358,
} PORT_CL2CM_DW6_A_INSTANCE_GLK;

typedef enum _PORT_CL2CM_DW6_B_INSTANCE_GLK
{
    PORT_CL2CM_DW6_B_INSTANCE_ADDRESS_GLK = 0x6C358,
} PORT_CL2CM_DW6_B_INSTANCE_GLK;

typedef enum _PORT_CL2CM_DW6_C_INSTANCE_GLK
{
    PORT_CL2CM_DW6_C_INSTANCE_ADDRESS_GLK = 0x163358,
} PORT_CL2CM_DW6_C_INSTANCE_GLK;

typedef enum _PORT_CL2CM_DW6_MASKS_GLK
{
    PORT_CL2CM_DW6_MASKS_PBC_GLK = 0xEFFFFFFF,
    PORT_CL2CM_DW6_MASKS_WO_GLK  = 0x0,
    PORT_CL2CM_DW6_MASKS_MBZ_GLK = 0x0,
} PORT_CL2CM_DW6_MASKS_GLK;

/*****************************************************************************\
PHY CL2 Dword 6
Instances per PHY dual/single
DDIA: PHY single, base 0x162000
DDIB/C: PHY dual, base 0x6C000
CL2 common config base 0x340
\*****************************************************************************/
typedef union _PORT_CL2CM_DW6_GLK {
    struct
    {
        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(0, 27); // PBC
        DDU32 Oldo_Dynpwrdownen : DD_BITFIELD_BIT(28);         //

        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(29, 31); // PBC
    };
    DDU32 Value;
} PORT_CL2CM_DW6_GLK;

C_ASSERT(4 == sizeof(PORT_CL2CM_DW6_GLK));

// IMPLICIT ENUMERATIONS USED BY PORT_REF_DW6_GLK
//
typedef enum _OGRCCODE_NOM_GLK
{
    OGRCCODE_NOM_UNNAMED_128_GLK = 0x80,
} OGRCCODE_NOM_GLK;

typedef enum _OGRCCODE_SLOW_GLK
{
    OGRCCODE_SLOW_UNNAMED_128_GLK = 0x80,
} OGRCCODE_SLOW_GLK;

typedef enum _OGRCCODE_FAST_GLK
{
    OGRCCODE_FAST_UNNAMED_128_GLK = 0x80,
} OGRCCODE_FAST_GLK;

typedef enum _PORT_REF_DW6_A_INSTANCE_GLK
{
    PORT_REF_DW6_A_INSTANCE_ADDRESS_GLK = 0x162198,
} PORT_REF_DW6_A_INSTANCE_GLK;

typedef enum _PORT_REF_DW6_B_INSTANCE_GLK
{
    PORT_REF_DW6_B_INSTANCE_ADDRESS_GLK = 0x6C198,
} PORT_REF_DW6_B_INSTANCE_GLK;

typedef enum _PORT_REF_DW6_C_INSTANCE_GLK
{
    PORT_REF_DW6_C_INSTANCE_ADDRESS_GLK = 0x163198,
} PORT_REF_DW6_C_INSTANCE_GLK;

typedef enum _PORT_REF_DW6_MASKS_GLK
{
    PORT_REF_DW6_MASKS_WO_GLK  = 0x0,
    PORT_REF_DW6_MASKS_MBZ_GLK = 0x0,
    PORT_REF_DW6_MASKS_PBC_GLK = 0x0,
} PORT_REF_DW6_MASKS_GLK;

/*****************************************************************************\
Refer to CRI register map in DDI section.
\*****************************************************************************/
typedef union _PORT_REF_DW6_GLK {
    struct
    {
        /*****************************************************************************\

        Programming Notes:
        For RTL testing, program the ogrccode fields with 0x80 when copying Rcomp to the dual channel PHY.
        \*****************************************************************************/
        DDU32 Ogrccode_Nom : DD_BITFIELD_RANGE(0, 7); // OGRCCODE_NOM_GLK

        /*****************************************************************************\

        Programming Notes:
        For RTL testing, program the ogrccode fields with 0x80 when copying Rcomp to the dual channel PHY.
        \*****************************************************************************/
        DDU32 Ogrccode_Slow : DD_BITFIELD_RANGE(8, 15); // OGRCCODE_SLOW_GLK

        /*****************************************************************************\

        Programming Notes:
        For RTL testing, program the ogrccode fields with 0x80 when copying Rcomp to the dual channel PHY.
        \*****************************************************************************/
        DDU32 Ogrccode_Fast : DD_BITFIELD_RANGE(16, 23); // OGRCCODE_FAST_GLK
        DDU32 Grccode : DD_BITFIELD_RANGE(24, 31);       //
    };
    DDU32 Value;
} PORT_REF_DW6_GLK;

C_ASSERT(4 == sizeof(PORT_REF_DW6_GLK));

// IMPLICIT ENUMERATIONS USED BY PORT_REF_DW8_GLK
//
typedef enum _FCOMPREFSEL_GLK
{
    FCOMPREFSEL_400_OHM_GLK = 0x0,
    FCOMPREFSEL_100_OHM_GLK = 0x1,
} FCOMPREFSEL_GLK;

typedef enum _PORT_REF_DW8_A_INSTANCE_GLK
{
    PORT_REF_DW8_A_INSTANCE_ADDRESS_GLK = 0x1621A0,
} PORT_REF_DW8_A_INSTANCE_GLK;

typedef enum _PORT_REF_DW8_B_INSTANCE_GLK
{
    PORT_REF_DW8_B_INSTANCE_ADDRESS_GLK = 0x6C1A0,
} PORT_REF_DW8_B_INSTANCE_GLK;

typedef enum _PORT_REF_DW8_C_INSTANCE_GLK
{
    PORT_REF_DW8_C_INSTANCE_ADDRESS_GLK = 0x1631A0,
} PORT_REF_DW8_C_INSTANCE_GLK;

typedef enum _PORT_REF_DW8_MASKS_GLK
{
    PORT_REF_DW8_MASKS_WO_GLK  = 0x0,
    PORT_REF_DW8_MASKS_MBZ_GLK = 0x0,
    PORT_REF_DW8_MASKS_PBC_GLK = 0x7FFF7FFD,
} PORT_REF_DW8_MASKS_GLK;

/*****************************************************************************\
Refer to CRI register map in DDI.
\*****************************************************************************/
typedef union _PORT_REF_DW8_GLK {
    struct
    {
        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(0); // PBC
        DDU32 Grc_Rdy_Ovrd : DD_BITFIELD_BIT(1);         //

        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(2, 14); // PBC
        DDU32 Grcdis : DD_BITFIELD_BIT(15);                    //

        /*****************************************************************************\
        The values in this field must not be changed.  Use read/modify/write to update this register.
        \*****************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(16, 30); // PBC

        /*****************************************************************************\
        GRC Flash Comparator Ref Select
        \*****************************************************************************/
        DDU32 Fcomprefsel : DD_BITFIELD_BIT(31); // FCOMPREFSEL_GLK
    };
    DDU32 Value;
} PORT_REF_DW8_GLK;

C_ASSERT(4 == sizeof(PORT_REF_DW8_GLK));

// IMPLICIT ENUMERATIONS USED BY PHY_CTL_DDI_GLK
//
typedef enum _LANE_RESET_OVERRIDE_ENABLE_GLK
{
    LANE_RESET_OVERRIDE_ENABLE_DISABLE_GLK = 0x0,
    LANE_RESET_OVERRIDE_ENABLE_ENABLE_GLK  = 0x1,
} LANE_RESET_OVERRIDE_ENABLE_GLK;

typedef enum _LANE_STATUS_GLK
{
    LANE_STATUS_DISABLE_GLK = 0x0,
    LANE_STATUS_ENABLE_GLK  = 0x1,
} LANE_STATUS_GLK;

typedef enum _PHY_CTL_DDI_A_INSTANCE_GLK
{
    PHY_CTL_DDI_A_INSTANCE_ADDRESS_GLK = 0x64C00,
} PHY_CTL_DDI_A_INSTANCE_GLK;

typedef enum _PHY_CTL_DDI_B_INSTANCE_GLK
{
    PHY_CTL_DDI_B_INSTANCE_ADDRESS_GLK = 0x64C10,
} PHY_CTL_DDI_B_INSTANCE_GLK;

typedef enum _PHY_CTL_DDI_C_INSTANCE_GLK
{
    PHY_CTL_DDI_C_INSTANCE_ADDRESS_GLK = 0x64C20,
} PHY_CTL_DDI_C_INSTANCE_GLK;

typedef enum _PHY_CTL_DDI_MASKS_GLK
{
    PHY_CTL_DDI_MASKS_WO_GLK  = 0x0,
    PHY_CTL_DDI_MASKS_MBZ_GLK = 0x0,
    PHY_CTL_DDI_MASKS_PBC_GLK = 0x0,
} PHY_CTL_DDI_MASKS_GLK;

/*****************************************************************************\
This register is on the ungated clock and the chip reset, not the FLR or display debug reset.
Writes to this register will not trigger PSR exit.
\*****************************************************************************/
typedef union _PHY_CTL_DDI_GLK {
    struct
    {
        /*****************************************************************************\
        This field sets the override values for the lane resets.
        \*****************************************************************************/
        DDU32 LaneResets : DD_BITFIELD_RANGE(0, 3); //

        /*****************************************************************************\
        This field enables the override on the lane resets.
        \*****************************************************************************/
        DDU32 LaneResetOverrideEnable : DD_BITFIELD_BIT(4);  // LANE_RESET_OVERRIDE_ENABLE_GLK
        DDU32 Spare5 : DD_BITFIELD_BIT(5);                   //
        DDU32 Spare6 : DD_BITFIELD_BIT(6);                   //
        DDU32 Spare7 : DD_BITFIELD_BIT(7);                   //
        DDU32 LaneStatus : DD_BITFIELD_BIT(8);               // LANE_STATUS_GLK
        DDU32 LanePowerdownAcknowledge : DD_BITFIELD_BIT(9); //

        /*****************************************************************************\
        ocl*_powerdown_ack
        \*****************************************************************************/
        DDU32 CommonLanePowerdownAcknowledge : DD_BITFIELD_BIT(10); //
        DDU32 Spare11 : DD_BITFIELD_BIT(11);                        //
        DDU32 Spare12 : DD_BITFIELD_BIT(12);                        //
        DDU32 Spare13 : DD_BITFIELD_BIT(13);                        //
        DDU32 Spare14 : DD_BITFIELD_BIT(14);                        //
        DDU32 Spare15 : DD_BITFIELD_BIT(15);                        //
        DDU32 DebugInputLane0 : DD_BITFIELD_RANGE(16, 17);          //
        DDU32 DebugInputLane1 : DD_BITFIELD_RANGE(18, 19);          //
        DDU32 DebugInputLane2 : DD_BITFIELD_RANGE(20, 21);          //
        DDU32 DebugInputLane3 : DD_BITFIELD_RANGE(22, 23);          //
        DDU32 DebugOutputLane0 : DD_BITFIELD_RANGE(24, 25);         //
        DDU32 DebugOutputLane1 : DD_BITFIELD_RANGE(26, 27);         //
        DDU32 DebugOutputLane2 : DD_BITFIELD_RANGE(28, 29);         //
        DDU32 DebugOutputLane3 : DD_BITFIELD_RANGE(30, 31);         //
    };
    DDU32 Value;
} PHY_CTL_DDI_GLK;

C_ASSERT(4 == sizeof(PHY_CTL_DDI_GLK));

// IMPLICIT ENUMERATIONS USED BY PHY_CTL_FAMILY_GLK
//
typedef enum _POWERGOOD_GLK
{
    POWERGOOD_NOT_GOOD_GLK = 0x0,
    POWERGOOD_GOOD_GLK     = 0x1,
} POWERGOOD_GLK;

typedef enum _COMMON_RESET_GLK
{
    COMMON_RESET_DISABLE_GLK = 0x0,
    COMMON_RESET_ENABLE_GLK  = 0x1,
} COMMON_RESET_GLK;

typedef enum _PHY_CTL_FAMILY_EDP_INSTANCE_GLK
{
    PHY_CTL_FAMILY_EDP_INSTANCE_ADDRESS_GLK = 0x64C80,
} PHY_CTL_FAMILY_EDP_INSTANCE_GLK;

typedef enum _PHY_CTL_FAMILY_DDI_B_INSTANCE_GLK
{
    PHY_CTL_FAMILY_DDI_B_INSTANCE_ADDRESS_GLK = 0x64C90,
} PHY_CTL_FAMILY_DDI_B_INSTANCE_GLK;

typedef enum _PHY_CTL_FAMILY_DDI_C_INSTANCE_GLK
{
    PHY_CTL_FAMILY_DDI_C_INSTANCE_ADDRESS_GLK = 0x64CA0,
} PHY_CTL_FAMILY_DDI_C_INSTANCE_GLK;

typedef enum _PHY_CTL_FAMILY_MASKS_GLK
{
    PHY_CTL_FAMILY_MASKS_WO_GLK  = 0x0,
    PHY_CTL_FAMILY_MASKS_MBZ_GLK = 0x0,
    PHY_CTL_FAMILY_MASKS_PBC_GLK = 0x0,
} PHY_CTL_FAMILY_MASKS_GLK;

/*****************************************************************************\
This register is on the ungated clock and the chip reset, not the FLR or display debug reset.
Writes to this register will not trigger PSR exit.
\*****************************************************************************/
typedef union _PHY_CTL_FAMILY_GLK {
    struct
    {
        /*****************************************************************************\
        icl1_bonus[3:0]

        This field is unused in GLK.
        \*****************************************************************************/
        DDU32 Cl1Bonus : DD_BITFIELD_RANGE(0, 3); //

        /*****************************************************************************\
        BXT sends the EDP version of this signal to all the PHYs.  The DDI version is unused.

        This field is unused in GLK.

        ildopgseq_delay[1:0]
        \*****************************************************************************/
        DDU32 LdopgseqDelay : DD_BITFIELD_RANGE(4, 5); //
        DDU32 Spare6 : DD_BITFIELD_BIT(6);             //
        DDU32 Spare7 : DD_BITFIELD_BIT(7);             //
        DDU32 Spare8 : DD_BITFIELD_BIT(8);             //
        DDU32 Spare9 : DD_BITFIELD_BIT(9);             //
        DDU32 Spare10 : DD_BITFIELD_BIT(10);           //
        DDU32 Spare11 : DD_BITFIELD_BIT(11);           //
        DDU32 Spare12 : DD_BITFIELD_BIT(12);           //
        DDU32 Spare13 : DD_BITFIELD_BIT(13);           //
        DDU32 Spare14 : DD_BITFIELD_BIT(14);           //
        DDU32 Spare15 : DD_BITFIELD_BIT(15);           //
        DDU32 Spare16 : DD_BITFIELD_BIT(16);           //
        DDU32 Spare17 : DD_BITFIELD_BIT(17);           //
        DDU32 Spare18 : DD_BITFIELD_BIT(18);           //
        DDU32 Spare19 : DD_BITFIELD_BIT(19);           //
        DDU32 Spare20 : DD_BITFIELD_BIT(20);           //
        DDU32 Spare21 : DD_BITFIELD_BIT(21);           //
        DDU32 Spare22 : DD_BITFIELD_BIT(22);           //
        DDU32 Spare23 : DD_BITFIELD_BIT(23);           //
        DDU32 Spare24 : DD_BITFIELD_BIT(24);           //
        DDU32 Spare25 : DD_BITFIELD_BIT(25);           //
        DDU32 Spare26 : DD_BITFIELD_BIT(26);           //
        DDU32 Spare27 : DD_BITFIELD_BIT(27);           //
        DDU32 Spare28 : DD_BITFIELD_BIT(28);           //
        DDU32 Spare29 : DD_BITFIELD_BIT(29);           //

        /*****************************************************************************\
        This field indicates that the PHY is powered up.
        \*****************************************************************************/
        DDU32 Powergood : DD_BITFIELD_BIT(30); // POWERGOOD_GLK

        /*****************************************************************************\
        This field controls the reset_b (active low reset) which enables the PHY.
        \*****************************************************************************/
        DDU32 CommonReset : DD_BITFIELD_BIT(31); // COMMON_RESET_GLK
    };
    DDU32 Value;
} PHY_CTL_FAMILY_GLK;

C_ASSERT(4 == sizeof(PHY_CTL_FAMILY_GLK));

typedef enum _P_CR_GT_DISP_PWRON_0_2_0_GTTMMADR_INSTANCE_GLK
{
    P_CR_GT_DISP_PWRON_0_2_0_GTTMMADR_INSTANCE_ADDRESS_GLK = 0x138090,
} P_CR_GT_DISP_PWRON_0_2_0_GTTMMADR_INSTANCE_GLK;

typedef union _P_CR_GT_DISP_PWRON_0_2_0_GTTMMADR_GLK {
    struct
    {
        /**********************************************************************\
        GT Display DDIB Power On
        \**********************************************************************/
        DDU32 CH0_PWRREQ1P0_SUS : DD_BITFIELD_BIT(0);

        /**********************************************************************\
        GT Display DDIC Power On
        \**********************************************************************/
        DDU32 CH1_PWRREQ1P0_SUS : DD_BITFIELD_BIT(1);

        /*********************************************************************\
        MIPIO reset control
        \*********************************************************************/
        DDU32 MIPIO_RST_CTRL : DD_BITFIELD_BIT(2);

        /**********************************************************************\
        GT Display eDP/DDIA Power On
        \**********************************************************************/
        DDU32 EDP_PWRREQ1P0_SUS : DD_BITFIELD_BIT(3);

        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(4, 31);
    };
    DDU32 Value;
} P_CR_GT_DISP_PWRON_0_2_0_GTTMMADR_GLK;

// IMPLICIT ENUMERATIONS USED BY CHICKEN_MISC_2_CNL
//
typedef enum _CL0_POWERDOWN_ENABLE_CNL
{
    CL0_POWERDOWN_ENABLE_UNNAMED_1_CNL = 0x1,
} CL0_POWERDOWN_ENABLE_CNL;

typedef enum _CL1_POWERDOWN_ENABLE_CNL
{
    CL1_POWERDOWN_ENABLE_UNNAMED_1_CNL = 0x1,
} CL1_POWERDOWN_ENABLE_CNL;

typedef enum _CL2_POWERDOWN_ENABLE_CNL
{
    CL2_POWERDOWN_ENABLE_UNNAMED_1_CNL = 0x1,
} CL2_POWERDOWN_ENABLE_CNL;

typedef enum _SPARE_16_CNL
{
    SPARE_16_ENABLE_CNL  = 0x0,
    SPARE_16_DISABLE_CNL = 0x1,
} SPARE_16_CNL;

typedef enum _KVMRCAP_REG_DOUBLE_BUFFER_CNL
{
    KVMRCAP_REG_DOUBLE_BUFFER_DISABLE_DOUBLE_BUFFER_CNL = 0x0,
    KVMRCAP_REG_DOUBLE_BUFFER_ENABLE_DOUBLE_BUFFER_CNL  = 0x1,
} KVMRCAP_REG_DOUBLE_BUFFER_CNL;

typedef enum _SPARE_21_CNL
{
    SPARE_21_ENABLE_CNL  = 0x0,
    SPARE_21_DISABLE_CNL = 0x1,
} SPARE_21_CNL;

typedef enum _DE_TO_IO_MISC_CNL
{
    DE_TO_IO_MISC_UNNAMED_2_CNL = 0x2,
    DE_TO_IO_MISC_UNNAMED_3_CNL = 0x3,
} DE_TO_IO_MISC_CNL;

typedef enum _MISC_CHICKEN_BITS_2_INSTANCE_CNL
{
    MISC_CHICKEN_BITS_2_ADDR_CNL = 0x42084,
} MISC_CHICKEN_BITS_2_INSTANCE_CNL;

typedef enum _CHICKEN_MISC_2_MASKS_CNL
{
    CHICKEN_MISC_2_MASKS_WO_CNL  = 0x0,
    CHICKEN_MISC_2_MASKS_MBZ_CNL = 0x0,
    CHICKEN_MISC_2_MASKS_PBC_CNL = 0x0,
} CHICKEN_MISC_2_MASKS_CNL;

/*****************************************************************************\
This register is on the ungated clock and the chip reset, not the FLR or display debug reset.
Writes to this register will not trigger PSR exit.
\*****************************************************************************/
typedef union _CHICKEN_MISC_2_CNL {
    struct
    {
        /*****************************************************************************\
        PSR Global mask bit used by hardware for save and restore.  Software should not program this bit.
        \*****************************************************************************/
        DDU32 Spare0 : DD_BITFIELD_BIT(0);              //
        DDU32 Spare1 : DD_BITFIELD_BIT(1);              //
        DDU32 Spare2 : DD_BITFIELD_BIT(2);              //
        DDU32 Spare3 : DD_BITFIELD_BIT(3);              //
        DDU32 Spare4 : DD_BITFIELD_BIT(4);              //
        DDU32 Spare5 : DD_BITFIELD_BIT(5);              //
        DDU32 Spare6 : DD_BITFIELD_BIT(6);              //
        DDU32 Spare7 : DD_BITFIELD_BIT(7);              //
        DDU32 Spare8 : DD_BITFIELD_BIT(8);              //
        DDU32 Spare9 : DD_BITFIELD_BIT(9);              //
        DDU32 Cl0PowerdownEnable : DD_BITFIELD_BIT(10); // CL0_POWERDOWN_ENABLE_CNL
        DDU32 Cl1PowerdownEnable : DD_BITFIELD_BIT(11); // CL1_POWERDOWN_ENABLE_CNL
        DDU32 Cl2PowerdownEnable : DD_BITFIELD_BIT(12); // CL2_POWERDOWN_ENABLE_CNL
        DDU32 Spare13 : DD_BITFIELD_BIT(13);            //
        DDU32 Spare14 : DD_BITFIELD_BIT(14);            //
        DDU32 Spare15 : DD_BITFIELD_BIT(15);            // VRR Back To Back Master Flip Support Override

        /*****************************************************************************\
        This field disables the arbiter fix for handling LP read requests correctly when the display buffer bypass queue is full.
        \*****************************************************************************/
        DDU32 Spare16 : DD_BITFIELD_BIT(16); // SPARE_16_CNL
        DDU32 Spare17 : DD_BITFIELD_BIT(17); //
        DDU32 Spare18 : DD_BITFIELD_BIT(18); //
        DDU32 Spare19 : DD_BITFIELD_BIT(19); //

        /*****************************************************************************\
        This field controls whether KVMR capture registers are double-buffered.
        \*****************************************************************************/
        DDU32 KvmrcapRegDoubleBuffer : DD_BITFIELD_BIT(20); // KVMRCAP_REG_DOUBLE_BUFFER_CNL

        /*****************************************************************************\
        This field enables/disables the arbiter fix for IPC problems with buffer fill.
        \*****************************************************************************/
        DDU32 Spare21 : DD_BITFIELD_BIT(21);           // SPARE_21_CNL
        DDU32 Spare22 : DD_BITFIELD_BIT(22);           //
        DDU32 DeToIoCompPwrDown : DD_BITFIELD_BIT(23); //
        DDU32 IoToDeMisc : DD_BITFIELD_RANGE(24, 27);  //
        DDU32 DeToIoMisc : DD_BITFIELD_RANGE(28, 31);  // DE_TO_IO_MISC_CNL
    };
    DDU32 Value;
} CHICKEN_MISC_2_CNL;

C_ASSERT(4 == sizeof(CHICKEN_MISC_2_CNL));

// IMPLICIT ENUMERATIONS USED BY DDI_BUF_CTL_SKL
//
typedef enum _INIT_DISPLAY_DETECTED_SKL
{
    INIT_DISPLAY_DETECTED_NOT_DETECTED_SKL = 0x0, // Digital display not detected during initialization
    INIT_DISPLAY_DETECTED_DETECTED_SKL     = 0x1, // Digital display detected during initialization
} INIT_DISPLAY_DETECTED_SKL;

typedef enum _DP_PORT_WIDTH_SELECTION_SKL
{
    DP_PORT_WIDTH_SELECTION_X1_SKL = 0x0, // x1 Mode
    DP_PORT_WIDTH_SELECTION_X2_SKL = 0x1, // x2 Mode
    DP_PORT_WIDTH_SELECTION_X4_SKL = 0x3, // x4 Mode (not allowed with DDI E, some restrictions with DDI A)
} DP_PORT_WIDTH_SELECTION_SKL;

typedef enum _DDIA_LANE_CAPABILITY_CONTROL_SKL
{
    DDIA_LANE_CAPABILITY_CONTROL_DDIA_X2_SKL = 0x0, // DDI A supports 2 lanes and DDI E supports 2 lanes
    DDIA_LANE_CAPABILITY_CONTROL_DDIA_X4_SKL = 0x1, // DDI A supports 4 lanes and DDI E is not used
} DDIA_LANE_CAPABILITY_CONTROL_SKL;

typedef enum _DDI_IDLE_STATUS_SKL
{
    DDI_IDLE_STATUS_BUFFER_NOT_IDLE_SKL = 0x0,
    DDI_IDLE_STATUS_BUFFER_IDLE_SKL     = 0x1,
} DDI_IDLE_STATUS_SKL;

typedef enum _PORT_REVERSAL_SKL
{
    PORT_REVERSAL_NOT_REVERSED_SKL = 0x0,
    PORT_REVERSAL_REVERSED_SKL     = 0x1,
} PORT_REVERSAL_SKL;

typedef enum _DP_VSWING_EMP_SEL_SKL
{
    DP_VSWING_EMP_SEL_SELECT_9_SKL = 0x9, // Select buffer translation 9.  Valid only with DDIA and DDIE.
} DP_VSWING_EMP_SEL_SKL;

typedef enum _DDI_BUFFER_ENABLE_SKL
{
    DDI_BUFFER_ENABLE_DISABLE_SKL = 0x0,
    DDI_BUFFER_ENABLE_ENABLE_SKL  = 0x1,
} DDI_BUFFER_ENABLE_SKL;

typedef enum _DDI_A_BUFFER_CONTROL_INSTANCE_SKL
{
    DDI_A_BUFFER_CONTROL_INSTANCE_ADDRESS_SKL = 0x64000,
} DDI_A_BUFFER_CONTROL_INSTANCE_SKL;

typedef enum _DDI_B_BUFFER_CONTROL_INSTANCE_SKL
{
    DDI_B_BUFFER_CONTROL_INSTANCE_ADDRESS_SKL = 0x64100,
} DDI_B_BUFFER_CONTROL_INSTANCE_SKL;

typedef enum _DDI_C_BUFFER_CONTROL_INSTANCE_SKL
{
    DDI_C_BUFFER_CONTROL_INSTANCE_ADDRESS_SKL = 0x64200,
} DDI_C_BUFFER_CONTROL_INSTANCE_SKL;

typedef enum _DDI_D_BUFFER_CONTROL_INSTANCE_SKL
{
    DDI_D_BUFFER_CONTROL_INSTANCE_ADDRESS_SKL = 0x64300,
} DDI_D_BUFFER_CONTROL_INSTANCE_SKL;

typedef enum _DDI_E_BUFFER_CONTROL_INSTANCE_SKL
{
    DDI_E_BUFFER_CONTROL_INSTANCE_ADDRESS_SKL = 0x64400,
} DDI_E_BUFFER_CONTROL_INSTANCE_SKL;

typedef enum _DDI_F_BUFFER_CONTROL_INSTANCE_CNL
{
    DDI_F_BUFFER_CONTROL_INSTANCE_ADDRESS_CNL = 0x64500,
} DDI_F_BUFFER_CONTROL_INSTANCE_CNL;

typedef enum _DDI_BUF_CTL_MASKS_SKL
{
    DDI_BUF_CTL_MASKS_WO_SKL  = 0x0,
    DDI_BUF_CTL_MASKS_PBC_SKL = 0x0,
    DDI_BUF_CTL_MASKS_MBZ_SKL = 0x70FEFF60,
} DDI_BUF_CTL_MASKS_SKL;

/*****************************************************************************\
There is one DDI Buffer Control per each DDI A/B/C/D/E.
\*****************************************************************************/
typedef union _DDI_BUF_CTL_SKL {
    struct
    {
        /*****************************************************************************\
        Strap indicating whether a display was detected on this port during initialization.
        It signifies the level of the port detect pin at boot.
        This bit is only informative. It does not prevent this port from being enabled in hardware.
        This field only indicates the DDIA detection.
        DDIB detection is read from SFUSE_STRAP 0xC2014 bit 2.
        DDIC detection is read from SFUSE_STRAP 0xC2014 bit 1.
        DDID detection is read from SFUSE_STRAP 0xC2014 bit 0.
        \*****************************************************************************/
        DDU32 InitDisplayDetected : DD_BITFIELD_BIT(0); // INIT_DISPLAY_DETECTED_SKL

        /*****************************************************************************\
        This bit selects the number of lanes to be enabled on the DDI link for DisplayPort.

        This field is ignored for HDMI and DVI which always use all 4 lanes.

        Programming Notes:
        Restriction : When in DisplayPort mode the value selected here must match the value selected
        in the DDI Buffer Control register for the DDI attached to this pipe.

        Restriction : This field must not be changed while the DDI is enabled.
        DDI E only supports x1 and and x2 when DDI_BUF_CTL_A DDIA Lane Capability Control is set to DDIA x2, otherwise DDI E is not supported.
        DDI A (EDP) supports x1, x2, and x4 when DDI_BUF_CTL_A DDIA Lane Capability Control is set to DDIA x4, otherwise DDI A only supports x1 and x2.
        \*****************************************************************************/
        DDU32 DpPortWidthSelection : DD_BITFIELD_RANGE(1, 3); // DP_PORT_WIDTH_SELECTION_SKL

        /*****************************************************************************\
        This bit selects how lanes are shared between DDI A and DDI E.
        This field is only used in the DDI A instance of this register.
        See the DDI A and DDI E lane mapping table in the Introduction section.

        Programming Notes:
        Restriction : This field must be programmed at system boot based on board configuration and may not be changed afterwards.
        \*****************************************************************************/
        DDU32 DdiaLaneCapabilityControl : DD_BITFIELD_BIT(4); // DDIA_LANE_CAPABILITY_CONTROL_SKL
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(5, 6); // MBZ

        /*****************************************************************************\
        This bit indicates when the DDI buffer is idle.
        \*****************************************************************************/
        DDU32 DdiIdleStatus : DD_BITFIELD_BIT(7);              // DDI_IDLE_STATUS_SKL
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(8, 15); // MBZ

        /*****************************************************************************\
        This field enables lane reversal within the port.  Lane reversal swaps the data on the lanes as they are output from the port.

        Programming Notes:
        DDI B, C, and D reversal always swaps the four lanes, so lane 0 is swapped with lane 3, and lane 1 is swapped with lane 2.
        If DDIA Lane Capability Control selects DDIA x2, then DDI A reversal swaps the two lanes, so lane 0 is swapped with lane 1.
        If DDIA Lane Capability Control selects DDIA x4, then DDI A reversal swaps the four lanes, so lane 0 is swapped with lane 3, and lane 1 is swapped with lane 2.

        Restriction : This field must not be changed while the DDI is enabled.
        DDI E does not support reversal.
        \*****************************************************************************/
        DDU32 PortReversal : DD_BITFIELD_BIT(16);               // PORT_REVERSAL_SKL
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(17, 23); // MBZ

        /*****************************************************************************\
        These bits are used to select the voltage swing and emphasis for DisplayPort.

        This field is ignored for HDMI and DVI.
        The values programmed in DDI_BUF_TRANS determine the voltage swing and emphasis for each selection.
        \*****************************************************************************/
        DDU32 DpVswingEmpSel : DD_BITFIELD_RANGE(24, 27);       // DP_VSWING_EMP_SEL_SKL
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(28, 30); // MBZ

        /*****************************************************************************\
        This bit enables the DDI buffer.
        \*****************************************************************************/
        DDU32 DdiBufferEnable : DD_BITFIELD_BIT(31); // DDI_BUFFER_ENABLE_SKL
    };
    DDU32 Value;
} DDI_BUF_CTL_SKL;

C_ASSERT(4 == sizeof(DDI_BUF_CTL_SKL));

// IMPLICIT ENUMERATIONS USED BY DP_TP_CTL_SKL
//
typedef enum _ALTERNATE_SR_ENABLE_SKL
{
    ALTERNATE_SR_ENABLE_DISABLE_SKL = 0x0,
    ALTERNATE_SR_ENABLE_ENABLE_SKL  = 0x1,
} ALTERNATE_SR_ENABLE_SKL;

typedef enum _SCRAMBLING_DISABLE_SKL
{
    SCRAMBLING_DISABLE_ENABLE_SKL  = 0x0,
    SCRAMBLING_DISABLE_DISABLE_SKL = 0x1,
} SCRAMBLING_DISABLE_SKL;

typedef enum _DP_LINK_TRAINING_ENABLE_SKL
{
    DP_LINK_TRAINING_ENABLE_PATTERN_1_SKL = 0x0, // Training Pattern 1 enabled
    DP_LINK_TRAINING_ENABLE_PATTERN_2_SKL = 0x1, // Training Pattern 2 enabled
    DP_LINK_TRAINING_ENABLE_IDLE_SKL      = 0x2, // Idle Pattern enabled
    DP_LINK_TRAINING_ENABLE_NORMAL_SKL    = 0x3, // Link not in training: Send normal pixels
    DP_LINK_TRAINING_ENABLE_PATTERN_3_SKL = 0x4, // Training Pattern 3 enabled
} DP_LINK_TRAINING_ENABLE_SKL;

typedef enum _ENHANCED_FRAMING_ENABLE_SKL
{
    ENHANCED_FRAMING_ENABLE_DISABLED_SKL = 0x0,
    ENHANCED_FRAMING_ENABLE_ENABLED_SKL  = 0x1,
} ENHANCED_FRAMING_ENABLE_SKL;

typedef enum _FORCE_ACT_SKL
{
    FORCE_ACT_DO_NOT_FORCE_SKL = 0x0, // Do not force ACT to be sent
    FORCE_ACT_FORCE_SKL        = 0x1, // Force ACT to be sent one time
} FORCE_ACT_SKL;

typedef enum _TRANSPORT_MODE_SELECT_SKL
{
    TRANSPORT_MODE_SELECT_SST_MODE_SKL = 0x0, // DisplayPort SST mode
    TRANSPORT_MODE_SELECT_MST_MODE_SKL = 0x1, // DisplayPort MST mode
} TRANSPORT_MODE_SELECT_SKL;

typedef enum _TRANSPORT_ENABLE_SKL
{
    TRANSPORT_ENABLE_DISABLE_SKL = 0x0,
    TRANSPORT_ENABLE_ENABLE_SKL  = 0x1,
} TRANSPORT_ENABLE_SKL;

typedef enum _DDI_A_DISPLAYPORT_TRANSPORT_CONTROL_INSTANCE_SKL
{
    DDI_A_DISPLAYPORT_TRANSPORT_CONTROL_INSTANCE_ADDRESS_SKL = 0x64040,
} DDI_A_DISPLAYPORT_TRANSPORT_CONTROL_INSTANCE_SKL;

typedef enum _DDI_B_DISPLAYPORT_TRANSPORT_CONTROL_INSTANCE_SKL
{
    DDI_B_DISPLAYPORT_TRANSPORT_CONTROL_INSTANCE_ADDRESS_SKL = 0x64140,
} DDI_B_DISPLAYPORT_TRANSPORT_CONTROL_INSTANCE_SKL;

typedef enum _DDI_C_DISPLAYPORT_TRANSPORT_CONTROL_INSTANCE_SKL
{
    DDI_C_DISPLAYPORT_TRANSPORT_CONTROL_INSTANCE_ADDRESS_SKL = 0x64240,
} DDI_C_DISPLAYPORT_TRANSPORT_CONTROL_INSTANCE_SKL;

typedef enum _DDI_D_DISPLAYPORT_TRANSPORT_CONTROL_INSTANCE_SKL
{
    DDI_D_DISPLAYPORT_TRANSPORT_CONTROL_INSTANCE_ADDRESS_SKL = 0x64340,
} DDI_D_DISPLAYPORT_TRANSPORT_CONTROL_INSTANCE_SKL;

typedef enum _DDI_E_DISPLAYPORT_TRANSPORT_CONTROL_INSTANCE_SKL
{
    DDI_E_DISPLAYPORT_TRANSPORT_CONTROL_INSTANCE_ADDRESS_SKL = 0x64440,
} DDI_E_DISPLAYPORT_TRANSPORT_CONTROL_INSTANCE_SKL;

typedef enum _DDI_F_DISPLAYPORT_TRANSPORT_CONTROL_INSTANCE_CNL
{
    DDI_F_DISPLAYPORT_TRANSPORT_CONTROL_INSTANCE_ADDRESS_CNL = 0x64540,
} DDI_F_DISPLAYPORT_TRANSPORT_CONTROL_INSTANCE_CNL;

typedef enum _DP_TP_CTL_MASKS_SKL
{
    DP_TP_CTL_MASKS_WO_SKL  = 0x0,
    DP_TP_CTL_MASKS_PBC_SKL = 0x0,
    DP_TP_CTL_MASKS_MBZ_SKL = 0x75FBF83F,
} DP_TP_CTL_MASKS_SKL;

typedef union _DP_TP_CTL_SKL {
    struct
    {
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(0, 5); // MBZ

        /*****************************************************************************\
        This bit enables the DisplayPort Alternate Scrambler Reset, intended for use only with embedded DisplayPort receivers.

        Programming Notes:
        Restriction : This field must not be changed while the DDI function is enabled.
        \*****************************************************************************/
        DDU32 AlternateSrEnable : DD_BITFIELD_BIT(6); // ALTERNATE_SR_ENABLE_SKL

        /*****************************************************************************\
        This bit disables scrambling for DisplayPort.

        Programming Notes:
        Restriction : This field must not be changed while the DDI function is enabled.
        \*****************************************************************************/
        DDU32 ScramblingDisable : DD_BITFIELD_BIT(7); // SCRAMBLING_DISABLE_SKL

        /*****************************************************************************\
        These bits are used for DisplayPort link initialization as defined in the DisplayPort specification.
        DP_TP_STATUS has an indication that the required number of idle patterns has been sent.

        Programming Notes:
        Restriction : When enabling the port, it must be turned on with pattern 1 enabled.
        When retraining a link, the port must be disabled, then re-enabled with pattern 1 enabled.
        \*****************************************************************************/
        DDU32 DpLinkTrainingEnable : DD_BITFIELD_RANGE(8, 10);  // DP_LINK_TRAINING_ENABLE_SKL
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(11, 17); // MBZ

        /*****************************************************************************\
        This bit selects enhanced framing for DisplayPort SST.

        Hardware internally enables enhanced framing for DisplayPort MST.

        Programming Notes:
        Restriction : In DisplayPort MST mode this bit must be set to Disabled.
        This field must not be changed while the DDI function is enabled.
        \*****************************************************************************/
        DDU32 EnhancedFramingEnable : DD_BITFIELD_BIT(18);      // ENHANCED_FRAMING_ENABLE_SKL
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(19, 24); // MBZ

        /*****************************************************************************\
        This bit forces DisplayPort MST ACT to be sent one time at the next link frame boundary.
        After ACT is sent, as indicated in the ACT sent status bit, this bit can be cleared and set again to send ACT again.
        This bit is ignored by DDI A (EDP) and DDI E since they do not support multistreaming.
        \*****************************************************************************/
        DDU32 ForceAct : DD_BITFIELD_BIT(25);             // FORCE_ACT_SKL
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(26); // MBZ

        /*****************************************************************************\
        This bit selects between DisplayPort SST and MST modes of operation.
        This bit is ignored by DDI A (EDP) and DDI E since they do not support multistreaming.

        Programming Notes:
        Restriction : The DisplayPort mode (SST or MST) selected here must match the mode selected in the
        Transcoder DDI Function Control registers for the transcoders attached to this transport.
        This field must not be changed while the DDI function is enabled.
        \*****************************************************************************/
        DDU32 TransportModeSelect : DD_BITFIELD_BIT(27);        // TRANSPORT_MODE_SELECT_SKL
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(28, 30); // MBZ

        /*****************************************************************************\
        This bit enables the DisplayPort transport function.
        \*****************************************************************************/
        DDU32 TransportEnable : DD_BITFIELD_BIT(31); // TRANSPORT_ENABLE_SKL
    };
    DDU32 Value;
} DP_TP_CTL_SKL;

C_ASSERT(4 == sizeof(DP_TP_CTL_SKL));

// IMPLICIT ENUMERATIONS USED BY DP_TP_STATUS_SKL
//
typedef enum _PAYLOAD_MAPPING_VC0_SKL
{
    PAYLOAD_MAPPING_VC0_A_SKL = 0x0, // Transcoder A mapped to this VC
    PAYLOAD_MAPPING_VC0_B_SKL = 0x1, // Transcoder B mapped to this VC
    PAYLOAD_MAPPING_VC0_C_SKL = 0x2, // Transcoder C mapped to this VC
} PAYLOAD_MAPPING_VC0_SKL;

typedef enum _PAYLOAD_MAPPING_VC1_SKL
{
    PAYLOAD_MAPPING_VC1_A_SKL = 0x0, // Transcoder A mapped to this VC
    PAYLOAD_MAPPING_VC1_B_SKL = 0x1, // Transcoder B mapped to this VC
    PAYLOAD_MAPPING_VC1_C_SKL = 0x2, // Transcoder C mapped to this VC
} PAYLOAD_MAPPING_VC1_SKL;

typedef enum _PAYLOAD_MAPPING_VC2_SKL
{
    PAYLOAD_MAPPING_VC2_A_SKL = 0x0, // Transcoder A mapped to this VC
    PAYLOAD_MAPPING_VC2_B_SKL = 0x1, // Transcoder B mapped to this VC
    PAYLOAD_MAPPING_VC2_C_SKL = 0x2, // Transcoder C mapped to this VC
} PAYLOAD_MAPPING_VC2_SKL;

typedef enum _STREAMS_ENABLED_SKL
{
    STREAMS_ENABLED_ZERO_SKL  = 0x0, // Zero streams enabled
    STREAMS_ENABLED_ONE_SKL   = 0x1, // One stream enabled
    STREAMS_ENABLED_TWO_SKL   = 0x2, // Two streams enabled
    STREAMS_ENABLED_THREE_SKL = 0x3, // Three streams enabled
} STREAMS_ENABLED_SKL;

typedef enum _MODE_STATUS_SKL
{
    MODE_STATUS_SST_SKL = 0x0, // Single-stream mode
    MODE_STATUS_MST_SKL = 0x1, // Multi-stream mode
} MODE_STATUS_SKL;

typedef enum _ACT_SENT_STATUS_SKL
{
    ACT_SENT_STATUS_ACT_NOT_SENT_SKL = 0x0,
    ACT_SENT_STATUS_ACT_SENT_SKL     = 0x1,
} ACT_SENT_STATUS_SKL;

typedef enum _MIN_IDLES_SENT_SKL
{
    MIN_IDLES_SENT_MIN_IDLES_NOT_SENT_SKL = 0x0,
    MIN_IDLES_SENT_MIN_IDLES_SENT_SKL     = 0x1,
} MIN_IDLES_SENT_SKL;

typedef enum _ACTIVE_LINK_FRAME_STATUS_SKL
{
    ACTIVE_LINK_FRAME_STATUS_ACTIVE_LINK_FRAME_NOT_SENT_SKL = 0x0,
    ACTIVE_LINK_FRAME_STATUS_ACTIVE_LINK_FRAME_SENT_SKL     = 0x1,
} ACTIVE_LINK_FRAME_STATUS_SKL;

typedef enum _IDLE_LINK_FRAME_STATUS_SKL
{
    IDLE_LINK_FRAME_STATUS_IDLE_LINK_FRAME_NOT_SENT_SKL = 0x0,
    IDLE_LINK_FRAME_STATUS_IDLE_LINK_FRAME_SENT_SKL     = 0x1,
} IDLE_LINK_FRAME_STATUS_SKL;

typedef enum _DDI_B_DISPLAYPORT_TRANSPORT_STATUS_INSTANCE_SKL
{
    DDI_B_DISPLAYPORT_TRANSPORT_STATUS_INSTANCE_ADDRESS_SKL = 0x64144,
} DDI_B_DISPLAYPORT_TRANSPORT_STATUS_INSTANCE_SKL;

typedef enum _DDI_C_DISPLAYPORT_TRANSPORT_STATUS_INSTANCE_SKL
{
    DDI_C_DISPLAYPORT_TRANSPORT_STATUS_INSTANCE_ADDRESS_SKL = 0x64244,
} DDI_C_DISPLAYPORT_TRANSPORT_STATUS_INSTANCE_SKL;

typedef enum _DDI_D_DISPLAYPORT_TRANSPORT_STATUS_INSTANCE_SKL
{
    DDI_D_DISPLAYPORT_TRANSPORT_STATUS_INSTANCE_ADDRESS_SKL = 0x64344,
} DDI_D_DISPLAYPORT_TRANSPORT_STATUS_INSTANCE_SKL;

typedef enum _DDI_E_DISPLAYPORT_TRANSPORT_STATUS_INSTANCE_SKL
{
    DDI_E_DISPLAYPORT_TRANSPORT_STATUS_INSTANCE_ADDRESS_SKL = 0x64444,
} DDI_E_DISPLAYPORT_TRANSPORT_STATUS_INSTANCE_SKL;

typedef enum _DDI_F_DISPLAYPORT_TRANSPORT_STATUS_INSTANCE_CNL
{
    DDI_F_DISPLAYPORT_TRANSPORT_STATUS_INSTANCE_ADDRESS_CNL = 0x64544,
} DDI_F_DISPLAYPORT_TRANSPORT_STATUS_INSTANCE_CNL;

typedef enum _DP_TP_STATUS_MASKS_SKL
{
    DP_TP_STATUS_MASKS_MBZ_SKL = 0xF07CFCCC,
    DP_TP_STATUS_MASKS_WO_SKL  = 0x0,
    DP_TP_STATUS_MASKS_PBC_SKL = 0x0,
} DP_TP_STATUS_MASKS_SKL;

/*****************************************************************************\
There is one DisplayPort Transport Status register per each DDI B/C/D/E.  DDI A does not have a status register.
\*****************************************************************************/
typedef union _DP_TP_STATUS_SKL {
    struct
    {
        /*****************************************************************************\
        This field indicates which transcoder is mapped to Virtual Channel 0 during multistream operation.
        This field should be ignored if the number of streams enabled is less than one.
        This field should be ignored in single stream mode.
        \*****************************************************************************/
        DDU32 PayloadMappingVc0 : DD_BITFIELD_RANGE(0, 1);    // PAYLOAD_MAPPING_VC0_SKL
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(2, 3); // MBZ

        /*****************************************************************************\
        This field indicates which transcoder is mapped to Virtual Channel 1 during multistream operation.
        This field should be ignored if the number of streams enabled is less than two.
        This field should be ignored in single stream mode.
        \*****************************************************************************/
        DDU32 PayloadMappingVc1 : DD_BITFIELD_RANGE(4, 5);    // PAYLOAD_MAPPING_VC1_SKL
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(6, 7); // MBZ

        /*****************************************************************************\
        This field indicates which transcoder is mapped to Virtual Channel 2 during multistream operation.
        This field should be ignored if the number of streams enabled is less than three.
        This field should be ignored in single stream mode.
        \*****************************************************************************/
        DDU32 PayloadMappingVc2 : DD_BITFIELD_RANGE(8, 9);      // PAYLOAD_MAPPING_VC2_SKL
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(10, 15); // MBZ

        /*****************************************************************************\
        This field indicates the number of streams (transcoders) enabled on this port during multistream operation.
        This field should be ignored in single stream mode.
        \*****************************************************************************/
        DDU32 StreamsEnabled : DD_BITFIELD_RANGE(16, 17);       // STREAMS_ENABLED_SKL
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(18, 22); // MBZ

        /*****************************************************************************\
        This bit indicates what mode the transport is currently in.
        \*****************************************************************************/
        DDU32 ModeStatus : DD_BITFIELD_BIT(23); // MODE_STATUS_SKL

        /*****************************************************************************\
        This bit indicates if DisplayPort MST ACT has been sent.
        This is a sticky bit, cleared by writing 1b to it.
        \*****************************************************************************/
        DDU32 ActSentStatus : DD_BITFIELD_BIT(24); // ACT_SENT_STATUS_SKL

        /*****************************************************************************\
        This bit indicates that the minimum required number of idle patterns has been sent when DP_TP_CTL is set to send idle patterns.
        This bit will clear itself when DP_TP_CTL is not longer set to send idle patterns.
        \*****************************************************************************/
        DDU32 MinIdlesSent : DD_BITFIELD_BIT(25); // MIN_IDLES_SENT_SKL

        /*****************************************************************************\
        This bit indicates if a link frame boundary has been sent in active (at least one VC enabled).
        This is a sticky bit, cleared by writing 1b to it.
        \*****************************************************************************/
        DDU32 ActiveLinkFrameStatus : DD_BITFIELD_BIT(26); // ACTIVE_LINK_FRAME_STATUS_SKL

        /*****************************************************************************\
        This bit indicates if a link frame boundary has been sent in idle pattern.
        This is a sticky bit, cleared by writing 1b to it.
        \*****************************************************************************/
        DDU32 IdleLinkFrameStatus : DD_BITFIELD_BIT(27);        // IDLE_LINK_FRAME_STATUS_SKL
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(28, 31); // MBZ
    };
    DDU32 Value;
} DP_TP_STATUS_SKL;

C_ASSERT(4 == sizeof(DP_TP_STATUS_SKL));

// IMPLICIT ENUMERATIONS USED BY PP_STATUS_GLK
//
typedef enum _INTERNAL_SEQUENCE_STATE_GLK
{
    INTERNAL_SEQUENCE_STATE_POWER_OFF_IDLE_S0_0_GLK                 = 0x0,
    INTERNAL_SEQUENCE_STATE_POWER_OFF_WAIT_FOR_CYCLE_DELAY_S0_1_GLK = 0x1,
    INTERNAL_SEQUENCE_STATE_POWER_OFF_S0_2_GLK                      = 0x2,
    INTERNAL_SEQUENCE_STATE_POWER_OFF_S0_3_GLK                      = 0x3,
    INTERNAL_SEQUENCE_STATE_POWER_ON_IDLE_S1_0_GLK                  = 0x8,
    INTERNAL_SEQUENCE_STATE_POWER_ON_S1_1_GLK                       = 0x9,
    INTERNAL_SEQUENCE_STATE_POWER_ON_S1_2_GLK                       = 0xA,
    INTERNAL_SEQUENCE_STATE_POWER_ON_WAIT_FOR_CYCLE_DELAY_S1_3_GLK  = 0xB,
    INTERNAL_SEQUENCE_STATE_RESET_GLK                               = 0xF,
} INTERNAL_SEQUENCE_STATE_GLK;

typedef enum _POWER_CYCLE_DELAY_ACTIVE_GLK
{
    POWER_CYCLE_DELAY_ACTIVE_NOT_ACTIVE_GLK = 0x0,
    POWER_CYCLE_DELAY_ACTIVE_ACTIVE_GLK     = 0x1,
} POWER_CYCLE_DELAY_ACTIVE_GLK;

typedef enum _POWER_SEQUENCE_PROGRESS_GLK
{
    POWER_SEQUENCE_PROGRESS_NONE_GLK       = 0x0, // Panel is not in a power sequence
    POWER_SEQUENCE_PROGRESS_POWER_UP_GLK   = 0x1, // Panel is in a power up sequence (may include power cycle delay)
    POWER_SEQUENCE_PROGRESS_POWER_DOWN_GLK = 0x2, // Panel is in a power down sequence
} POWER_SEQUENCE_PROGRESS_GLK;

typedef enum _PANEL_POWER_ON_STATUS_GLK
{
    PANEL_POWER_ON_STATUS_OFF_GLK = 0x0, // Panel power down has completed. A power cycle delay may be currently active.
    PANEL_POWER_ON_STATUS_ON_GLK  = 0x1, // Panel power up has completed or power down sequence in progress.
} PANEL_POWER_ON_STATUS_GLK;

typedef enum _PANEL_POWER_1_STATUS_INSTANCE_GLK
{
    PANEL_POWER_1_STATUS_INSTANCE_ADDRESS_GLK = 0xC7200,
} PANEL_POWER_1_STATUS_INSTANCE_GLK;

typedef enum _PANEL_POWER_2_STATUS_INSTANCE_GLK
{
    PANEL_POWER_2_STATUS_INSTANCE_ADDRESS_GLK = 0xC7300,
} PANEL_POWER_2_STATUS_INSTANCE_GLK;

typedef enum _PP_STATUS_MASKS_GLK
{
    PP_STATUS_MASKS_WO_GLK  = 0x0,
    PP_STATUS_MASKS_PBC_GLK = 0x0,
    PP_STATUS_MASKS_MBZ_GLK = 0x47FFFFF0,
} PP_STATUS_MASKS_GLK;

typedef union _PP_STATUS_GLK {
    struct
    {
        DDU32 InternalSequenceState : DD_BITFIELD_RANGE(0, 3); // INTERNAL_SEQUENCE_STATE_GLK
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(4, 26); // MBZ

        /*****************************************************************************\
        Power cycle delays occur after a panel power down sequence or after a hardware reset.
        \*****************************************************************************/
        DDU32 PowerCycleDelayActive : DD_BITFIELD_BIT(27);       // POWER_CYCLE_DELAY_ACTIVE_GLK
        DDU32 PowerSequenceProgress : DD_BITFIELD_RANGE(28, 29); // POWER_SEQUENCE_PROGRESS_GLK
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(30);        // MBZ

        /*****************************************************************************\

        Programming Notes:
        Software is responsible for enabling the embedded panel display only at the correct point as defined in the mode set sequence.
        \*****************************************************************************/
        DDU32 PanelPowerOnStatus : DD_BITFIELD_BIT(31); // PANEL_POWER_ON_STATUS_GLK
    };
    DDU32 Value;
} PP_STATUS_GLK;

C_ASSERT(4 == sizeof(PP_STATUS_GLK));

// IMPLICIT ENUMERATIONS USED BY PP_CONTROL_GLK
//
typedef enum _POWER_STATE_TARGET_GLK
{
    POWER_STATE_TARGET_OFF_GLK =
    0x0, // If panel power is currently on, the power off sequence starts immediately.,
         // If a power on sequence is currently in progress, the power off sequence starts after the power on state is reached, which may include a power cycle delay.
    POWER_STATE_TARGET_ON_GLK = 0x1, // If panel power is currently off, the power on sequence starts immediately.
                                     // If a power off sequence is currently in progress, the power on sequence starts after the power
                                     // off state is reached and the power cycle delay is met.
} POWER_STATE_TARGET_GLK;

typedef enum _POWER_DOWN_ON_RESET_GLK
{
    POWER_DOWN_ON_RESET_DO_NOT_RUN_POWER_DOWN_ON_RESET_GLK = 0x0,
    POWER_DOWN_ON_RESET_RUN_POWER_DOWN_ON_RESET_GLK        = 0x1,
} POWER_DOWN_ON_RESET_GLK;

typedef enum _BACKLIGHT_ENABLE_GLK
{
    BACKLIGHT_ENABLE_DISABLE_GLK = 0x0,
    BACKLIGHT_ENABLE_ENABLE_GLK  = 0x1,
} BACKLIGHT_ENABLE_GLK;

typedef enum _VDD_OVERRIDE_GLK
{
    VDD_OVERRIDE_NOT_FORCE_GLK = 0x0,
    VDD_OVERRIDE_FORCE_GLK     = 0x1,
} VDD_OVERRIDE_GLK;

typedef enum _POWER_CYCLE_DELAY_GLK
{
    POWER_CYCLE_DELAY_NO_DELAY_GLK = 0x0,
    POWER_CYCLE_DELAY_400_MS_GLK   = 0x5,
} POWER_CYCLE_DELAY_GLK;

typedef enum _PANEL_POWER_1_CONTROL_INSTANCE_GLK
{
    PANEL_POWER_1_CONTROL_INSTANCE_ADDRESS_GLK = 0xC7204,
} PANEL_POWER_1_CONTROL_INSTANCE_GLK;

typedef enum _PANEL_POWER_2_CONTROL_INSTANCE_GLK
{
    PANEL_POWER_2_CONTROL_INSTANCE_ADDRESS_GLK = 0xC7304,
} PANEL_POWER_2_CONTROL_INSTANCE_GLK;

typedef enum _PP_CONTROL_MASKS_GLK
{
    PP_CONTROL_MASKS_MBZ_GLK = 0xFFFFFE00,
    PP_CONTROL_MASKS_WO_GLK  = 0x0,
    PP_CONTROL_MASKS_PBC_GLK = 0x0,
} PP_CONTROL_MASKS_GLK;

typedef union _PP_CONTROL_GLK {
    struct
    {
        /*****************************************************************************\
        This field sets the panel power state target.
        It can be written at any time and takes effect at the completion of any current power cycle.
        \*****************************************************************************/
        DDU32 PowerStateTarget : DD_BITFIELD_BIT(0); // POWER_STATE_TARGET_GLK

        /*****************************************************************************\
        This field selects whether the panel will run the power down sequence when a reset is detected.

        Programming Notes:
        Running power down on reset is recommended for panel protection.
        \*****************************************************************************/
        DDU32 PowerDownOnReset : DD_BITFIELD_BIT(1); // POWER_DOWN_ON_RESET_GLK

        /*****************************************************************************\
        This field enables the backlight when hardware is in the correct panel power sequence state.
        \*****************************************************************************/
        DDU32 BacklightEnable : DD_BITFIELD_BIT(2); // BACKLIGHT_ENABLE_GLK

        /*****************************************************************************\
        This field forces VDD on.  This is intended for panels that require VDD to be asserted before accessing AUX channel.

        Programming Notes:
        Restriction : When software clears this bit from '1' to '0' (stop forcing VDD on) it must ensure that T4 power cycle delay is met before setting this bit to '1' again.
        \*****************************************************************************/
        DDU32 VddOverride : DD_BITFIELD_BIT(3); // VDD_OVERRIDE_GLK

        /*****************************************************************************\
        This field provides the delay for the eDP T12 time; the shortest time from panel power disable to power enable.
        If panel power power state target is set to on during this delay, the power on sequence will not commence until the delay is complete.
        The value should be programmed to (desired delay / 100 milliseconds) + 1.
        Writing a value of 0 selects no delay or is used to abort the delay if it is active.

        Programming Notes:
        Restriction : A correct value must be programmed before enabling panel power.
        \*****************************************************************************/
        DDU32 PowerCycleDelay : DD_BITFIELD_RANGE(4, 8);       // POWER_CYCLE_DELAY_GLK
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(9, 31); // MBZ
    };
    DDU32 Value;
} PP_CONTROL_GLK;

C_ASSERT(4 == sizeof(PP_CONTROL_GLK));

// IMPLICIT ENUMERATIONS USED BY PP_ON_DELAYS_GLK
//
typedef enum _PANEL_POWER_1_ON_DELAYS_INSTANCE_GLK
{
    PANEL_POWER_1_ON_DELAYS_INSTANCE_ADDRESS_GLK = 0xC7208,
} PANEL_POWER_1_ON_DELAYS_INSTANCE_GLK;

typedef enum _PANEL_POWER_2_ON_DELAYS_INSTANCE_GLK
{
    PANEL_POWER_2_ON_DELAYS_INSTANCE_ADDRESS_GLK = 0xC7308,
} PANEL_POWER_2_ON_DELAYS_INSTANCE_GLK;

typedef enum _PP_ON_DELAYS_MASKS_GLK
{
    PP_ON_DELAYS_MASKS_MBZ_GLK = 0xE000E000,
    PP_ON_DELAYS_MASKS_WO_GLK  = 0x0,
    PP_ON_DELAYS_MASKS_PBC_GLK = 0x0,
} PP_ON_DELAYS_MASKS_GLK;

typedef union _PP_ON_DELAYS_GLK {
    struct
    {
        /*****************************************************************************\
        This field provides the power on to backlight enable delay.
        Software controls the source valid video data output and can enable backlight after this delay has been met.
        Hardware will not allow the backlight to enable until after the power up delay (eDP T3) and this delay have passed.
        The time unit is 100us.
        \*****************************************************************************/
        DDU32 PowerOnToBacklightOn : DD_BITFIELD_RANGE(0, 12);  //
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(13, 15); // MBZ

        /*****************************************************************************\
        This field provides the delay during panel power up.
        Software programs this field with the delay for eDP T3; the time from enabling panel power to when the sink HPD and AUX channel should be ready.
        Software controls when AUX channel transactions start.
        The time unit is 100us.
        \*****************************************************************************/
        DDU32 PowerUpDelay : DD_BITFIELD_RANGE(16, 28);         //
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(29, 31); // MBZ
    };
    DDU32 Value;
} PP_ON_DELAYS_GLK;

C_ASSERT(4 == sizeof(PP_ON_DELAYS_GLK));

// IMPLICIT ENUMERATIONS USED BY PP_OFF_DELAYS_GLK
//
typedef enum _PANEL_POWER_1_OFF_DELAYS_INSTANCE_GLK
{
    PANEL_POWER_1_OFF_DELAYS_INSTANCE_ADDRESS_GLK = 0xC720C,
} PANEL_POWER_1_OFF_DELAYS_INSTANCE_GLK;

typedef enum _PANEL_POWER_2_OFF_DELAYS_INSTANCE_GLK
{
    PANEL_POWER_2_OFF_DELAYS_INSTANCE_ADDRESS_GLK = 0xC730C,
} PANEL_POWER_2_OFF_DELAYS_INSTANCE_GLK;

typedef enum _PP_OFF_DELAYS_MASKS_GLK
{
    PP_OFF_DELAYS_MASKS_MBZ_GLK = 0xE000E000,
    PP_OFF_DELAYS_MASKS_WO_GLK  = 0x0,
    PP_OFF_DELAYS_MASKS_PBC_GLK = 0x0,
} PP_OFF_DELAYS_MASKS_GLK;

typedef union _PP_OFF_DELAYS_GLK {
    struct
    {
        /*****************************************************************************\
        This field provides the backlight off to power down delay.
        Software programs this field with the time delay for the eDP T9 time value; the time from backlight disable to source ending valid video data.
        Software controls the backlight disable and source valid video data output.
        The time unit is 100us.
        \*****************************************************************************/
        DDU32 BacklightOffToPowerDown : DD_BITFIELD_RANGE(0, 12); //
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(13, 15);   // MBZ

        /*****************************************************************************\
        This fields provides the delay during power down.
        Software programs this field with the time delay for the eDP T10 time value;
        the time from source ending valid video data to source disabling panel power.
        Software controls the source valid video data output.
        The time unit is 100us.
        \*****************************************************************************/
        DDU32 PowerDownDelay : DD_BITFIELD_RANGE(16, 28);       //
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(29, 31); // MBZ
    };
    DDU32 Value;
} PP_OFF_DELAYS_GLK;

C_ASSERT(4 == sizeof(PP_OFF_DELAYS_GLK));

// IMPLICIT ENUMERATIONS USED BY UTIL_PIN_CTL_GLK
//
typedef enum _UTIL_PIN_OUTPUT_POLARITY_GLK
{
    UTIL_PIN_OUTPUT_POLARITY_NOT_INVERTED_GLK = 0x0,
    UTIL_PIN_OUTPUT_POLARITY_INVERTED_GLK     = 0x1,
} UTIL_PIN_OUTPUT_POLARITY_GLK;

typedef enum _UTIL_PIN_OUTPUT_DATA_GLK
{
    UTIL_PIN_OUTPUT_DATA_0_GLK = 0x0,
    UTIL_PIN_OUTPUT_DATA_1_GLK = 0x1,
} UTIL_PIN_OUTPUT_DATA_GLK;

typedef enum _UTIL_PIN_MODE_GLK
{
    UTIL_PIN_MODE_DATA_GLK                 = 0x0, // Output the Util_Pin_Output_Data value.
    UTIL_PIN_MODE_PWM_GLK                  = 0x1, // Output from the backlight PWM circuit.
    UTIL_PIN_MODE_VBLANK_GLK               = 0x4, // Output the vertical blank.
    UTIL_PIN_MODE_VSYNC_GLK                = 0x5, // Output the vertical sync.
    UTIL_PIN_MODE_RIGHT_LEFT_EYE_LEVEL_GLK = 0x8, // Output the stereo 3D right/left eye level signal. Asserted for the left eye and de-asserted for the right eye.
} UTIL_PIN_MODE_GLK;

typedef enum _PIPE_SELECT_GLK
{
    PIPE_SELECT_PIPE_A_GLK = 0x0,
    PIPE_SELECT_PIPE_B_GLK = 0x1,
    PIPE_SELECT_PIPE_C_GLK = 0x2,
} PIPE_SELECT_GLK;

typedef enum _UTIL_PIN_ENABLE_GLK
{
    UTIL_PIN_ENABLE_DISABLE_GLK = 0x0,
    UTIL_PIN_ENABLE_ENABLE_GLK  = 0x1,
} UTIL_PIN_ENABLE_GLK;

typedef enum _UTILITY_PIN_CONTROL_INSTANCE_GLK
{
    UTILITY_PIN_CONTROL_INSTANCE_ADDRESS_GLK = 0x48400,
} UTILITY_PIN_CONTROL_INSTANCE_GLK;

typedef enum _UTIL_PIN_CTL_MASKS_GLK
{
    UTIL_PIN_CTL_MASKS_WO_GLK  = 0x0,
    UTIL_PIN_CTL_MASKS_MBZ_GLK = 0x0,
    UTIL_PIN_CTL_MASKS_PBC_GLK = 0x0,
} UTIL_PIN_CTL_MASKS_GLK;

/*****************************************************************************\
This register controls the display utility pin.  The nominal supply is 1 Volt and can be level shifted depending on usage.  The maximum switching frequency is 100 KHz.
\*****************************************************************************/
typedef union _UTIL_PIN_CTL_GLK {
    struct
    {
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(0, 21); //

        /*****************************************************************************\
        This bit inverts the polarity of the pin output.
        \*****************************************************************************/
        DDU32 UtilPinOutputPolarity : DD_BITFIELD_BIT(22); // UTIL_PIN_OUTPUT_POLARITY_GLK

        /*****************************************************************************\
        This bit selects what the value to drive as an output when in the data mode.
        \*****************************************************************************/
        DDU32 UtilPinOutputData : DD_BITFIELD_BIT(23); // UTIL_PIN_OUTPUT_DATA_GLK

        /*****************************************************************************\
        This bit configures the utility pin mode of operation for output.

        Programming Notes:
        Restriction : The field should only be changed when the utility pin is disabled.
        \*****************************************************************************/
        DDU32 UtilPinMode : DD_BITFIELD_RANGE(24, 27);    // UTIL_PIN_MODE_GLK
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(28); //

        /*****************************************************************************\
        This bit selects which pipe will be used when the utility pin is outputting timing related signals.

        Programming Notes:
        Restriction : The field should only be changed when the utility pin is disabled or not configured to use any timing signals.
        \*****************************************************************************/
        DDU32 PipeSelect : DD_BITFIELD_RANGE(29, 30); // PIPE_SELECT_GLK

        /*****************************************************************************\
        This bit enables the utility pin.
        \*****************************************************************************/
        DDU32 UtilPinEnable : DD_BITFIELD_BIT(31); // UTIL_PIN_ENABLE_GLK
    };
    DDU32 Value;
} UTIL_PIN_CTL_GLK;

C_ASSERT(4 == sizeof(UTIL_PIN_CTL_GLK));

// IMPLICIT ENUMERATIONS USED BY BLC_PWM_CTL_GLK
//
typedef enum _PWM_POLARITY_GLK
{
    PWM_POLARITY_ACTIVE_HIGH_GLK = 0x0,
    PWM_POLARITY_ACTIVE_LOW_GLK  = 0x1,
} PWM_POLARITY_GLK;

typedef enum _PWM_ENABLE_GLK
{
    PWM_ENABLE_DISABLE_GLK = 0x0,
    PWM_ENABLE_ENABLE_GLK  = 0x1,
} PWM_ENABLE_GLK;

typedef enum _BACKLIGHT_1_PWM_CONTROL_INSTANCE_GLK
{
    BACKLIGHT_1_PWM_CONTROL_INSTANCE_ADDRESS_GLK = 0xC8250,
} BACKLIGHT_1_PWM_CONTROL_INSTANCE_GLK;

typedef enum _BACKLIGHT_2_PWM_CONTROL_INSTANCE_GLK
{
    BACKLIGHT_2_PWM_CONTROL_INSTANCE_ADDRESS_GLK = 0xC8350,
} BACKLIGHT_2_PWM_CONTROL_INSTANCE_GLK;

typedef enum _BLC_PWM_CTL_MASKS_GLK
{
    BLC_PWM_CTL_MASKS_WO_GLK  = 0x0,
    BLC_PWM_CTL_MASKS_PBC_GLK = 0x0,
    BLC_PWM_CTL_MASKS_MBZ_GLK = 0x5FFFFFFF,
} BLC_PWM_CTL_MASKS_GLK;

typedef union _BLC_PWM_CTL_GLK {
    struct
    {
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(0, 28); // MBZ

        /*****************************************************************************\
        This field controls the polarity of the PWM signal.
        \*****************************************************************************/
        DDU32 PwmPolarity : DD_BITFIELD_BIT(29);          // PWM_POLARITY_GLK
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(30); // MBZ

        /*****************************************************************************\
        This bit enables the PWM.
        A disabled PWM will drive 0, which can be inverted to 1 with the polarity control.
        \*****************************************************************************/
        DDU32 PwmEnable : DD_BITFIELD_BIT(31); // PWM_ENABLE_GLK
    };
    DDU32 Value;
} BLC_PWM_CTL_GLK;

C_ASSERT(4 == sizeof(BLC_PWM_CTL_GLK));

// IMPLICIT ENUMERATIONS USED BY BLC_PWM_FREQ_GLK
//
typedef enum _BACKLIGHT_1_PWM_FREQUENCY_INSTANCE_GLK
{
    BACKLIGHT_1_PWM_FREQUENCY_INSTANCE_ADDRESS_GLK = 0xC8254,
} BACKLIGHT_1_PWM_FREQUENCY_INSTANCE_GLK;

typedef enum _BACKLIGHT_2_PWM_FREQUENCY_INSTANCE_GLK
{
    BACKLIGHT_2_PWM_FREQUENCY_INSTANCE_ADDRESS_GLK = 0xC8354,
} BACKLIGHT_2_PWM_FREQUENCY_INSTANCE_GLK;

typedef enum _BLC_PWM_FREQ_MASKS_GLK
{
    BLC_PWM_FREQ_MASKS_WO_GLK  = 0x0,
    BLC_PWM_FREQ_MASKS_MBZ_GLK = 0x0,
    BLC_PWM_FREQ_MASKS_PBC_GLK = 0x0,
} BLC_PWM_FREQ_MASKS_GLK;

typedef union _BLC_PWM_FREQ_GLK {
    struct
    {
        /*****************************************************************************\
        This field controls the backlight PWM frequency.
        The value should be programmed to (CD clock frequency / desired PWM frequency).
        \*****************************************************************************/
        DDU32 Frequency : DD_BITFIELD_RANGE(0, 31); //
    };
    DDU32 Value;
} BLC_PWM_FREQ_GLK;

C_ASSERT(4 == sizeof(BLC_PWM_FREQ_GLK));

// IMPLICIT ENUMERATIONS USED BY BLC_PWM_DUTY_GLK
//
typedef enum _BACKLIGHT_1_PWM_DUTY_CYCLE_INSTANCE_GLK
{
    BACKLIGHT_1_PWM_DUTY_CYCLE_INSTANCE_ADDRESS_GLK = 0xC8258,
} BACKLIGHT_1_PWM_DUTY_CYCLE_INSTANCE_GLK;

typedef enum _BACKLIGHT_2_PWM_DUTY_CYCLE_INSTANCE_GLK
{
    BACKLIGHT_2_PWM_DUTY_CYCLE_INSTANCE_ADDRESS_GLK = 0xC8358,
} BACKLIGHT_2_PWM_DUTY_CYCLE_INSTANCE_GLK;

typedef enum _BLC_PWM_DUTY_MASKS_GLK
{
    BLC_PWM_DUTY_MASKS_WO_GLK  = 0x0,
    BLC_PWM_DUTY_MASKS_MBZ_GLK = 0x0,
    BLC_PWM_DUTY_MASKS_PBC_GLK = 0x0,
} BLC_PWM_DUTY_MASKS_GLK;

typedef union _BLC_PWM_DUTY_GLK {
    struct
    {
        /*****************************************************************************\
        This field controls the active portion of the backlight PWM duty cycle.
        The value should be programmed to (BLC_PWM_FREQ Frequency * desired duty cycle percentage / 100).
        A value of zero will give a 0% active duty cycle. A value equal to BLC_PWM_FREQ Frequency will give a 100% active duty cycle.
        When written, the new value will take affect at the end of the current PWM cycle.

        Programming Notes:
        Restriction : This should never be larger than BLC_PWM_FREQ Frequency.
        \*****************************************************************************/
        DDU32 DutyCycle : DD_BITFIELD_RANGE(0, 31); //
    };
    DDU32 Value;
} BLC_PWM_DUTY_GLK;

C_ASSERT(4 == sizeof(BLC_PWM_DUTY_GLK));

// IMPLICIT ENUMERATIONS USED BY DDI_BUF_TRANS_SKL
//
typedef enum _DEEMP_LEVEL_SKL
{
    DEEMP_LEVEL_UNNAMED_24_SKL = 0x18,
} DEEMP_LEVEL_SKL;

typedef enum _BALANCE_LEG_ENABLE_SKL
{
    BALANCE_LEG_ENABLE_DISABLE_SKL = 0x0,
    BALANCE_LEG_ENABLE_ENABLE_SKL  = 0x1,
} BALANCE_LEG_ENABLE_SKL;

typedef enum _VSWING_SKL
{
    VSWING_UNNAMED_0_SKL = 0x0,
} VSWING_SKL;

typedef enum _VREF_SEL_SKL
{
    VREF_SEL_UNNAMED_0_SKL = 0x0,
} VREF_SEL_SKL;

typedef enum _DDI_A_BUFFER_TRANSLATION_INSTANCE_SKL
{
    DDI_A_BUFFER_TRANSLATION_INSTANCE_ADDRESS_SKL = 0x64E00,
} DDI_A_BUFFER_TRANSLATION_INSTANCE_SKL;

typedef enum _DDI_B_BUFFER_TRANSLATION_INSTANCE_SKL
{
    DDI_B_BUFFER_TRANSLATION_INSTANCE_ADDRESS_SKL = 0x64E60,
} DDI_B_BUFFER_TRANSLATION_INSTANCE_SKL;

typedef enum _DDI_C_BUFFER_TRANSLATION_INSTANCE_SKL
{
    DDI_C_BUFFER_TRANSLATION_INSTANCE_ADDRESS_SKL = 0x64EC0,
} DDI_C_BUFFER_TRANSLATION_INSTANCE_SKL;

typedef enum _DDI_D_BUFFER_TRANSLATION_INSTANCE_SKL
{
    DDI_D_BUFFER_TRANSLATION_INSTANCE_ADDRESS_SKL = 0x64F20,
} DDI_D_BUFFER_TRANSLATION_INSTANCE_SKL;

typedef enum _DDI_E_BUFFER_TRANSLATION_INSTANCE_SKL
{
    DDI_E_BUFFER_TRANSLATION_INSTANCE_ADDRESS_SKL = 0x64F80,
} DDI_E_BUFFER_TRANSLATION_INSTANCE_SKL;

typedef enum _DDI_BUF_TRANS_MASKS_SKL
{
    DDI_BUF_TRANS_MASKS_WO_SKL  = 0x0,
    DDI_BUF_TRANS_MASKS_PBC_SKL = 0x0,
    DDI_BUF_TRANS_MASKS_MBZ_SKL = 0x7FFC0000,
} DDI_BUF_TRANS_MASKS_SKL;

/*****************************************************************************\
These registers define the DDI buffer settings required for different voltage swing and emphasis selections.

In HDMI or DVI mode the HDMI/DVI translation registers are automatically selected.
In DisplayPort mode the DDI Buffer Control register programming will select which of these registers is used to drive the buffer.

For each DDI A/B/C/D/E there are 10 instances of this 2 DWord register format.
For DDI B/C/D, the first 9 instances (18 Dwords) are entries 0-8 which are used for DisplayPort,
and the last instance (2 Dwords) is entry 9 which is used for HDMI and DVI.
For DDI A and DDI E, the 10 instances (20 DWords) are entries 0-9 which are used for DisplayPort.
\*****************************************************************************/
typedef union _DDI_BUF_TRANS_SKL {
    struct
    {
        /*****************************************************************************\
        This field controls the De-emphasis level for the DDI buffer.
        \*****************************************************************************/
        DDU32 DeempLevel : DD_BITFIELD_RANGE(0, 17);            // DEEMP_LEVEL_SKL
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(18, 30); // MBZ

        /*****************************************************************************\
        This field controls the Balance Leg enable for the DDI buffer.
        \*****************************************************************************/
        DDU32 BalanceLegEnable : DD_BITFIELD_BIT(31); // BALANCE_LEG_ENABLE_SKL

        /*****************************************************************************\
        This field controls the voltage swing for the DDI buffer.
        \*****************************************************************************/
        DDU32 Vswing : DD_BITFIELD_RANGE(0, 10);                // VSWING_SKL
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(11, 15); // MBZ

        /*****************************************************************************\
        This field controls the voltage reference select for the DDI buffer.
        \*****************************************************************************/
        DDU32 VrefSel : DD_BITFIELD_RANGE(16, 20);              // VREF_SEL_SKL
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(21, 31); // MBZ
    };
    DDU32 Value[2];
} DDI_BUF_TRANS_SKL;

C_ASSERT(8 == sizeof(DDI_BUF_TRANS_SKL));

// IMPLICIT ENUMERATIONS USED BY HOTPLUG_CTL_GLK
//
typedef enum _DDI_B_HPD_STATUS_GLK
{
    DDI_B_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GLK    = 0x0,
    DDI_B_HPD_STATUS_SHORT_PULSE_DETECTED_GLK           = 0x1,
    DDI_B_HPD_STATUS_LONG_PULSE_DETECTED_GLK            = 0x2,
    DDI_B_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GLK = 0x3,
} DDI_B_HPD_STATUS_GLK;

typedef enum _DDI_B_HPD_INVERT_GLK
{
    DDI_B_HPD_INVERT_DO_NOT_INVERT_GLK = 0x0,
    DDI_B_HPD_INVERT_INVERT_GLK        = 0x1,
} DDI_B_HPD_INVERT_GLK;

typedef enum _DDI_B_HPD_INPUT_ENABLE_GLK
{
    DDI_B_HPD_INPUT_ENABLE_DISABLE_GLK = 0x0,
    DDI_B_HPD_INPUT_ENABLE_ENABLE_GLK  = 0x1,
} DDI_B_HPD_INPUT_ENABLE_GLK;

typedef enum _DDI_C_HPD_STATUS_GLK
{
    DDI_C_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GLK    = 0x0,
    DDI_C_HPD_STATUS_SHORT_PULSE_DETECTED_GLK           = 0x1,
    DDI_C_HPD_STATUS_LONG_PULSE_DETECTED_GLK            = 0x2,
    DDI_C_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GLK = 0x3,
} DDI_C_HPD_STATUS_GLK;

typedef enum _DDI_C_HPD_INVERT_GLK
{
    DDI_C_HPD_INVERT_DO_NOT_INVERT_GLK = 0x0,
    DDI_C_HPD_INVERT_INVERT_GLK        = 0x1,
} DDI_C_HPD_INVERT_GLK;

typedef enum _DDI_C_HPD_INPUT_ENABLE_GLK
{
    DDI_C_HPD_INPUT_ENABLE_DISABLE_GLK = 0x0,
    DDI_C_HPD_INPUT_ENABLE_ENABLE_GLK  = 0x1,
} DDI_C_HPD_INPUT_ENABLE_GLK;

typedef enum _DDI_A_HPD_STATUS_GLK
{
    DDI_A_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GLK    = 0x0,
    DDI_A_HPD_STATUS_SHORT_PULSE_DETECTED_GLK           = 0x1,
    DDI_A_HPD_STATUS_LONG_PULSE_DETECTED_GLK            = 0x2,
    DDI_A_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GLK = 0x3,
} DDI_A_HPD_STATUS_GLK;

typedef enum _DDI_A_HPD_INVERT_GLK
{
    DDI_A_HPD_INVERT_DO_NOT_INVERT_GLK = 0x0,
    DDI_A_HPD_INVERT_INVERT_GLK        = 0x1,
} DDI_A_HPD_INVERT_GLK;

typedef enum _DDI_A_HPD_INPUT_ENABLE_GLK
{
    DDI_A_HPD_INPUT_ENABLE_DISABLE_GLK = 0x0,
    DDI_A_HPD_INPUT_ENABLE_ENABLE_GLK  = 0x1,
} DDI_A_HPD_INPUT_ENABLE_GLK;

typedef enum _HOT_PLUG_CTL_INSTANCE_GLK
{
    HOT_PLUG_CTL_ADDR_GLK = 0xC4030,
} HOT_PLUG_CTL_INSTANCE_GLK;

typedef enum _HOTPLUG_CTL_MASKS_GLK
{
    HOTPLUG_CTL_MASKS_MBZ_GLK = 0xE4FFE4E4,
    HOTPLUG_CTL_MASKS_WO_GLK  = 0x0,
    HOTPLUG_CTL_MASKS_PBC_GLK = 0x0,
} HOTPLUG_CTL_MASKS_GLK;

/*****************************************************************************\
Hot plug detect (HPD) is used for notification of plug, unplug, and other sink events.
The short pulse durations are programmed in HPD_PULSE_CNT.
The hotplug ISR gives the live states of the HPD pins.
\*****************************************************************************/
typedef union _HOTPLUG_CTL_GLK {
    struct
    {
        /*****************************************************************************\
        This field indicates the hot plug detect status on port B.
        When HPD input is enabled and either a long or short pulse is detected, one of these bits will set and the hotplug IIR will be set (if unmasked in the IMR).
        These are sticky bits, cleared by writing 1s to both of them.
        \*****************************************************************************/
        DDU32 DdiBHpdStatus : DD_BITFIELD_RANGE(0, 1);   // DDI_B_HPD_STATUS_GLK
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(2); // MBZ

        /*****************************************************************************\
        This field inverts the HPD sense for digital port B.
        \*****************************************************************************/
        DDU32 DdiBHpdInvert : DD_BITFIELD_BIT(3); // DDI_B_HPD_INVERT_GLK

        /*****************************************************************************\
        This field enables the HPD buffer for digital port B.
        \*****************************************************************************/
        DDU32 DdiBHpdInputEnable : DD_BITFIELD_BIT(4);        // DDI_B_HPD_INPUT_ENABLE_GLK
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(5, 7); // MBZ

        /*****************************************************************************\
        This field indicates the hot plug detect status on port C.
        When HPD input is enabled and either a long or short pulse is detected, one of these bits will set and
        the hotplug IIR will be set (if unmasked in the IMR).
        These are sticky bits, cleared by writing 1s to both of them.
        \*****************************************************************************/
        DDU32 DdiCHpdStatus : DD_BITFIELD_RANGE(8, 9);    // DDI_C_HPD_STATUS_GLK
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(10); // MBZ

        /*****************************************************************************\
        This field inverts the HPD sense for digital port C.
        \*****************************************************************************/
        DDU32 DdiCHpdInvert : DD_BITFIELD_BIT(11); // DDI_C_HPD_INVERT_GLK

        /*****************************************************************************\
        This field enables the HPD buffer for digital port C.
        \*****************************************************************************/
        DDU32 DdiCHpdInputEnable : DD_BITFIELD_BIT(12);         // DDI_C_HPD_INPUT_ENABLE_GLK
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(13, 23); // MBZ

        /*****************************************************************************\
        This field indicates the hot plug detect status on port A.
        When HPD input is enabled and either a long or short pulse is detected,
        one of these bits will set and the hotplug IIR will be set (if unmasked in the IMR).
        These are sticky bits, cleared by writing 1s to both of them.
        \*****************************************************************************/
        DDU32 DdiAHpdStatus : DD_BITFIELD_RANGE(24, 25);  // DDI_A_HPD_STATUS_GLK
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(26); // MBZ

        /*****************************************************************************\
        This field inverts the HPD sense for digital port A.
        \*****************************************************************************/
        DDU32 DdiAHpdInvert : DD_BITFIELD_BIT(27); // DDI_A_HPD_INVERT_GLK

        /*****************************************************************************\
        This field enables the HPD buffer for digital port A.
        \*****************************************************************************/
        DDU32 DdiAHpdInputEnable : DD_BITFIELD_BIT(28);         // DDI_A_HPD_INPUT_ENABLE_GLK
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(29, 31); // MBZ
    };
    DDU32 Value;
} HOTPLUG_CTL_GLK;

#endif