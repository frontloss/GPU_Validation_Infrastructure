/*+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
**
** Copyright (c) Intel Corporation (2008-2012).
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
** File Name: HAS_SIM.H
**
** Abstract:  Defines the interface between driver and simlation. Driver and Simulation
**            have the same copy of the file; any modification to the file in either module
**            must immediately done to the file in the other module IN ORDER TO maintain
**            SYNCHRONIZATION !!!
**
**+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

#pragma once

#include "HAS_SIM_ENABLE.h" // Includes #define HAS

//  From Grantsdale-G There seems to be a conflict in the addresses 0xF8 and
//  0xFC.  Also there will be another Base Address we need to trap which will contain
//  GTT data.  Therefore we have changed the above method of trapping to differnt method.

//  The old method used to be writing MMIO_LINEAR address at offset 0xF8 and
//  Write APERTURE_LINEAR_ADDRESS at address 0xFC.  HAS Would monitor the PCI Config
//  write and start trapping the MMIOs etc.

//  The new method will monitor 0x90 of PCI Config address for commands and when it receives
//  commands next write will be for the data at offset 0x94.

//  Define the Offset for Command and Data
#define CFG_COMMAND_OFFSET 0xF8 // Pre-PC14 0x90
#define CFG_DATA_OFFSET 0xFC    // Pre-PC14 0x94

// FCH SLE specific...
#define PCI_CFG_SSID_SVID 0x2C       // SubSysVenID & SubSysID
#define FCH_SLE_SSID_SVID 0x87658086 // SVID/SSID value of SLE platform
#define PCI_CFG_DEVID 0x02           // Device ID Offset

//  Commands for Offset 0x90
#define INVALID_DRV_COMMAND 0x00000000
#define SET_MMIO_MAPPED_LINEAR_ADDRESS 0x00000001
#define SET_IO_LINEAR_ADDRESS 0x00000002
#define SET_APERTURE_LINEAR_ADDRESS 0x00000003
#define SET_HW_STATUS_PAGE_SIZE 0x00000004
#define SET_GTT_TABLE_SIZE 0x00000005
#define SET_GTT_TABLE_LINEAR_ADDRESS 0x00000006
#define DELETE_APERTURE_LINEAR_ADDRESS 0x00000007
#define GET_HAS_STATUS 0x00000010
#define GET_HOST_DEVICE_ID 0x00000011
#define GET_HOST_REVISION_ID 0x00000012
#define GET_MMIO_MAPPED_LINEAR_ADDRESS 0x00000013
#define GET_RAMBO_GFX_PHYS_ADDRESS 0x00000014
#define GET_RAMBO_STATUS_PAGE_PHYS_ADDRESS 0x00000015
#define GET_RAMBO_STATUS_PAGE_LINEAR_ADDRESS 0x00000016
#define GET_RAMBO_MEMORY_SIZE 0x00000017

//  Bugcheck notification related command and data
#define BUG_CHECK_NOTIFICATION 0x00000020
#define EXECUTE_MACHINE_DUMP 0x00000001

#define RAMBO_GTT_SIZE 512 * 1024

#define GFXADDR_TO_QT_RAMBO_PHYSADDR(a, GfxAddr) (((HW_DEVICE_EXTENSION *)a)->ulRamboGfxAperturePhyAddress.QuadPart + GfxAddr)
// assumption that there is a 1:1 mapping between Rambo physical address space and graphics address space.

// HAS Mode for simulator
enum THASMode
{
    HAS_IS_ACTIVE = 0x80000000, // Some form of HAS is active
    RC6_IS_ACTIVE = 0x40000000, // RC6 is active
    EMU_IS_ACTIVE = 0x20000000, // emulation is active
    HAS_MODE_MASK = 0xFF,       // Mask for HASMODE field

    HASMODE_INVALID   = 0,
    HASMODE_HW        = 1, // I/O will be sent to HW_Serv
    HASMODE_FULSIM    = 2, // I/O will be sent to Fulsim
    HASMODE_FULCHIP   = 3, // QuickTurn - FULL CHIP Emulation
    HASMODE_PIPE3D    = 4, // Pipe 3D Emulation
    HASMODE_PIPE2D    = 5, // Pipe 2D Emulation
    HASMODE_PIPEMEDIA = 6, // Media Pipe Emulation
    HASMODE_NET       = 7, // Transport all data via TCP/IP
    HASMODE_XEN       = 8, // VT with using Xen VMM
};

#pragma pack(push, 1)

typedef struct
{
    unsigned long dwLinearBase; // The beginning of the linear address
    unsigned long dwSize;       // Size of the linear address range

} HAS_APERTURE_LINEAR_ADDR_DATA, *PHAS_APERTURE_LINEAR_ADDR_DATA;

// Simulation environment structure
typedef struct _SIM_ENV
{
    union {
        struct
        {
            unsigned char SimEnv_Fulsim : 1;    // Bit 0 - Fulsim environment
            unsigned char SimEnv_Fulchip : 1;   // Bit 1 - Fulchip environment
            unsigned char SimEnv_Pipe3d : 1;    // Bit 2 - Pipe3d environment
            unsigned char SimEnv_Pipe2d : 1;    // Bit 3 - Pipe2d environment
            unsigned char SimEnv_PipeMedia : 1; // Bit 4 - PipeMedia environment
            unsigned char SimEnv_Net : 1;       // Bit 5 - Net environment
            unsigned char SimEnv_Xen : 1;       // Bit 6 - Xen environment
        };

        unsigned char Value; // Bitfield value
    };

} SIM_ENV, *PSIM_ENV;

// TODO: rename the HASCONFIG to DISPLAY_SIM_CONFIG
// In order to provide backward compatibiliy we should be adding new member
// definitions at the end of structure before variable "Reserved" (bits for Reserved must be modified accordingly)
// for e.g in future DDIG comes, and we want to add simulation support for it.
// "unsigned __int64 SimulateDDIG : 1"
// "unsigned __int64 Reserved:26"
typedef struct _HASCONFIG
{
    union {
        unsigned __int64 ulValue;
        struct
        {
            // below flag enables HAS display configs
            unsigned __int64 HASDisplayEnabled : 1; // BIT0

            // Display configs related  (for HAS/Fulsim and ULT framework
            unsigned __int64 SimulateEncoder : 1; // BIT1
            unsigned __int64 HDMIEnc : 1;         // enable HDMI encoder in HAS                        //BIT2
            unsigned __int64 DPEnc : 1;           // enable DP encoder in HAS                            //BIT3

            unsigned __int64 SimulateStrapState : 1; // BIT4
            unsigned __int64 SimulateLiveState : 1;  // BIT5
            unsigned __int64 SimulateDPCD : 1;       // 1: use simulated data           //BIT6

            unsigned __int64 SimulateDDIA : 1; // BIT7
            unsigned __int64 EDP : 1;          // EDP port A, 1: Live state true           //BIT8

            unsigned __int64 SimulateDDIB : 1; // BIT9
            unsigned __int64 DPB : 1;          // 1: attached 0: detached         //BIT10
            unsigned __int64 HDMIB : 1;        // 1: attached 0: detached         //BIT11

            unsigned __int64 SimulateDDIC : 1; // BIT12
            unsigned __int64 DPC : 1;          // 1: attached 0: detached         //BIT13
            unsigned __int64 HDMIC : 1;        // 1: attached 0: detached         //BIT14

            unsigned __int64 SimulateDDID : 1; // BIT15
            unsigned __int64 DPD : 1;          // 1: attached 0: detached         //BIT16
            unsigned __int64 HDMID : 1;        // 1: attached 0: detached         //BIT17

            unsigned __int64 SimulateDDIE : 1; // BIT18
            unsigned __int64 CRT : 1;          // HSW/BDW                         //BIT19
            unsigned __int64 DPE : 1;          // DP E for SKL, 1: attached 0: detached   //BIT20

            // feature flags
            unsigned __int64 DP12 : 1;       // DP 1.2 MST feature              //BIT21
            unsigned __int64 S3D : 1;        // simulate S3D EDID               //BIT22
            unsigned __int64 eDPx4Lane : 1;  // Disable CRT and enable 4 lane EDP, SimulateDDIE should be false               //BIT23
            unsigned __int64 EnablePSR : 1;  //                                 //BIT24
            unsigned __int64 EnablePSR2 : 1; //                                 //BIT25
            unsigned __int64 bCHVGTUC : 1;   //                                 //BIT26

            unsigned __int64 SimulateMIPI : 1; // BIT27
            unsigned __int64 MIPIA : 1;        // BIT28
            unsigned __int64 MIPIC : 1;        // BIT29
            unsigned __int64 DP13 : 1;         // BIT30

            unsigned __int64 SimulateDDIF : 1; // Bit 31
            unsigned __int64 DPF : 1;          // Bit 32
            unsigned __int64 HDMIF : 1;        // Bit 33

            unsigned __int64 CoG : 1;         // Bit 34
            unsigned __int64 eDpVDSC : 1;     // Bit 35, Flag for embedded display port(eDP) VDSC
            unsigned __int64 HDMIE : 1;       // For Gen11+                      //Bit 36
            unsigned __int64 TypeC_DDIC : 1;  // Bit 37
            unsigned __int64 TypeC_DDID : 1;  // Bit 38
            unsigned __int64 TypeC_DDIE : 1;  // Bit 39
            unsigned __int64 TypeC_DDIF : 1;  // Bit 40
            unsigned __int64 TBT_DDIC : 1;    // Bit 41
            unsigned __int64 TBT_DDID : 1;    // Bit 42
            unsigned __int64 TBT_DDIE : 1;    // Bit 43
            unsigned __int64 TBT_DDIF : 1;    // Bit 44
            unsigned __int64 DpVDSC : 1;      // Bit 45, Flag for display port(DP) VDSC
            unsigned __int64 MipiDsiVDSC : 1; // Bit 46, Flag for MIPI DSI VDSC
            unsigned __int64 Reserved : 17;   // Bit 47 - 63
        };
    };
} HASCONFIG, *PHASCONFIG;

#define SET_HAS_SIMULATION_BITS(stSimConfig)                                                                                                                           \
    (stSimConfig.SimulateDDIA = stSimConfig.SimulateDDIB = stSimConfig.SimulateDDIC = stSimConfig.SimulateDDID = stSimConfig.SimulateDDIE = stSimConfig.SimulateDDIF = \
     stSimConfig.SimulateMIPI = stSimConfig.SimulateEncoder = stSimConfig.SimulateLiveState = stSimConfig.SimulateStrapState = stSimConfig.HASDisplayEnabled)

C_ASSERT(sizeof(HASCONFIG) == 8);

// Simulation control table.  Allows customization of driver
// behavior for various simulation environments

typedef struct _SIM_CNTL_TABLE
{
    SIM_ENV SimCntl_HASIsActive;                          // HAS is active (includes Xen)
    SIM_ENV SimCntl_SimIsActive;                          // Simulation is active
    SIM_ENV SimCntl_NoSyncFlushOpWA;                      // Don't execute sync flush WA if
                                                          // simulation is active
    SIM_ENV SimCntl_UseRamboHwStatus;                     // For simulation environments using
                                                          // Aperture Rambo cards, HwStatus is
                                                          // on the Rambo card
    SIM_ENV SimCntl_UseSimHostInfo;                       // Save simulation host information
                                                          // so SoftBIOS will be aware of the
                                                          // underlying display hardware
    SIM_ENV SimCntl_DisablePowerCons;                     // Disable power conservation in
                                                          // simulation environments
    SIM_ENV SimCntl_UseRambo;                             // Simulation environment uses a
                                                          // Aperture Rambo card
    SIM_ENV       SimCntl_DisableHotPlug;                 // Disable hot plug detection in SoftBIOS
    SIM_ENV       SimCntl_OutputToCRT;                    // Set SoftBIOS to output to CRT only
    SIM_ENV       SimCntl_Use1MBGTT;                      // Force 1MB for GTT
    SIM_ENV       SimCntl_Use512KBGTT;                    // Force 512KB for GTT
    SIM_ENV       SimCntl_MediaSubmitNoReset;             // Setting for FPGA environment
    SIM_ENV       SimCntl_MediaForceApertOnlyTileSegPref; // Setting for FPGA environment
    SIM_ENV       SimCntl_OptimizedPresentPath;           // Setting for optimized present path through blitter
    SIM_ENV       SimCntl_DisableVblankInterrupt;         // WA to disable vblank interrupt
    SIM_ENV       SimCntl_WaDisableForceWake;             // WA to disable Force Wake with certain simulation / emulation environments
    SIM_ENV       SimCntl_UseGfxDeviceForBSM;             // Force driver to using GFX defice for reading BSM instead of 0:0:0
    SIM_ENV       SimCntl_TestFenceIdAllBltNodes;         // WA to test all Blitter nodes if interrupt occurs because Fulsim does not support pending interrupts properly
    SIM_ENV       SimCntl_EnablePavpSimTestingSupport;    // Enable PAVP testing support in simulated env
    SIM_ENV       SimCntl_EnablePavpEmuTestingSupport;    // Enable PAVP testing support in emulated env with virtual platform
    SIM_ENV       SimCntl_SimDisplayP2PStatusForPavp;     // Simulate Display P2P status for PAVP testing
    HASCONFIG     SimCntl_HASDisplayConfig;               // Display configuration to be enabled through SoftBios
    unsigned long IsFCHSLESystem;                         // Just to indicate if it's FCH SLE system or not...

} SIM_CNTL_TABLE, *PSIM_CNTL_TABLE;

#pragma pack(pop)

// Enable the below flag when testing Gen6GT interrups on HAS/Fulsim
#if HAS == 1
#define HAS_GEN6_GT_INTERRUPTS 0
#endif

// Enable Gen6 MFX on Gen5 for hybrid media simulation testing
#if HAS == 1
#define HAS_GEN6_MFX_ON_GEN5 0
#define HAS_GEN6_MEDIA_ON_GEN5 0
#endif

// Enable Gen7 MFX on Gen5 for hybrid media simulation testing
#if HAS == 1
#define HAS_GEN7_MFX_ON_GEN5 0
#define HAS_GEN7_MEDIA_ON_GEN5 0
#endif

// Enable Gen7.5 Media on Gen6 and Gen7 for hybrid media simulation testing
#if HAS == 1
#define HAS_GEN7_5_ON_GEN7 0
#define HAS_GEN7_5_ON_GEN6 0
#define HAS_ALLOW_VE_INTERRUPTS 0
#endif

#if HAS == 1
#define HAS_CHV_ON_BDW 0
#endif

#if HAS == 1
// Simulation control eveluation macros (returns AND of SIM_ENV and control point in SIM_CNTL_TABLE)
// These macros will return "0" if HAS == 0 (see below)
#define SIM_CNTL_TEST(x, feat) (((x)->SimEnv.Value) & ((x)->SimCntlTable.feat.Value))
#define SIM_CNTL_EXT_TEST(se, feat) (((se).Value) & ((feat).Value))
#else
#define SIM_CNTL_TEST(x, feat) (0)
#define SIM_CNTL_EXT_TEST(se, feat) (0)

#endif // HAS == 1
