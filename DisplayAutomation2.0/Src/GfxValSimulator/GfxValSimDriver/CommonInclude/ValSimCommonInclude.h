#ifndef __VALSIMCOMMONINCLUDE_H__
#define __VALSIMCOMMONINCLUDE_H__

#define MAX_PATH_STRING_LEN 128

typedef enum _PORT_TYPE
{
    PORT_NONE = 0,

    INTHDMIA_PORT = 33,
    INTHDMIB_PORT = 7,
    INTHDMIC_PORT = 8,
    INTHDMID_PORT = 9,
    INTHDMIE_PORT = 23,
    INTHDMIF_PORT = 20,
    INTHDMIG_PORT = 26,
    INTHDMIH_PORT = 29,
    INTHDMII_PORT = 32,

    INTDPA_PORT = 11, // Embedded DP For ILK
    INTDPB_PORT = 12,
    INTDPC_PORT = 13,
    INTDPD_PORT = 14,
    INTDPE_PORT = 6,
    INTDPF_PORT = 21,
    INTDPG_PORT = 24,
    INTDPH_PORT = 27,
    INTDPI_PORT = 30,
    DP_ALL_PORTS,

} PORT_TYPE,
*PPORT_TYPE;

typedef enum _MIPI_DSI_PORT_TYPE
{

    DD_PORT_TYPE_DSI_PORT_0    = 1,
    DD_PORT_TYPE_DSI_PORT_1    = 2,
    DD_PORT_TYPE_DSI_PORT_DUAL = 3,

} MIPI_DSI_PORT_TYPE,
*PMIPI_DSI_PORT_TYPE;

/*
This structure is used to control the behaviour of the GfxValSim driver.
Currently this is a place holder future CL will use this structure and
interface to this structure will defined through IOCTL.
*/
typedef struct _GFXVALSIM_FEATURE_CONTROL
{
    union {
        unsigned int ulValue;
        struct
        {
            unsigned int DisableSinkSimulation : 1;
            unsigned int VBTSimulation : 1;
            unsigned int HybridSimulation : 1;
            unsigned int InitMmioReg : 1;
            unsigned int reserved1 : 28;
        };
    };

} GFXVALSIM_FEATURE_CONTROL, *PGFXVALSIM_FEATURE_CONTROL;

typedef enum _DPCD_STATUS
{
    SUCCESS          = 0,
    INVALID_OFFSET   = 1,
    INVALID_TOPOLOGY = 2,

} DPCD_STATUS;

#endif
