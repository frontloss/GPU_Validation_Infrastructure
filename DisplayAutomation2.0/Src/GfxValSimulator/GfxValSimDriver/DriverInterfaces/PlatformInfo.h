#pragma once

#define GFX_GMD_ARCH_30 (30)
#define GFX_GMD_ARCH_30_RELEASE_XE3_LPG_XS (2)

// Macro to identify WCL based on GMD-ID
#define GFX_IS_WCL_CONFIG(stGfxGmdId) ((((stGfxGmdId).GmdID.GMDArch) == GFX_GMD_ARCH_30) && (((stGfxGmdId).GmdID.GMDRelease) == GFX_GMD_ARCH_30_RELEASE_XE3_LPG_XS))

typedef enum
{
    eIGFX_UNKNOWN = 0,
    eIGFX_GRANTSDALE_G,
    eIGFX_ALVISO_G,
    eIGFX_LAKEPORT_G,
    eIGFX_CALISTOGA_G,
    eIGFX_BROADWATER_G,
    eIGFX_CRESTLINE_G,
    eIGFX_BEARLAKE_G,
    eIGFX_CANTIGA_G,
    eIGFX_CEDARVIEW_G,
    eIGFX_EAGLELAKE_G,
    eIGFX_IRONLAKE_G,
    eIGFX_GT,
    eIGFX_IVYBRIDGE,
    eIGFX_HASWELL,
    eIGFX_VALLEYVIEW,
    eIGFX_BROADWELL,
    eIGFX_CHERRYVIEW,
    eIGFX_SKYLAKE,
    eIGFX_KABYLAKE,
    eIGFX_COFFEELAKE,
    eIGFX_WILLOWVIEW,
    eIGFX_BROXTON,
    eIGFX_GEMINILAKE,
    eIGFX_GLENVIEW,
    eIGFX_GOLDWATERLAKE,
    eIGFX_CANNONLAKE,
    eIGFX_CNX_G,
    eIGFX_ICELAKE,
    eIGFX_ICELAKE_LP,
    eIGFX_LAKEFIELD,
    eIGFX_JASPERLAKE,
    eIGFX_LAKEFIELD_R,
    eIGFX_TIGERLAKE_LP,
    eIGFX_RYEFIELD,
    eIGFX_ROCKETLAKE,
    eIGFX_ALDERLAKE_S,
    eIGFX_ALDERLAKE_P,
    eIGFX_DG100        = 1210,
    eIGFX_TIGERLAKE_HP = 1250,
    eIGFX_DG2          = 1270,
    eIGFX_PVC          = 1271,
    eIGFX_METEORLAKE   = 1272,
    eIGFX_ELG          = 1273,
    eIGFX_LUNARLAKE    = 1274,
    eIGFX_ARROWLAKE    = 1275,
    eIGFX_ALDERLAKE_N  = 1276,
    eIGFX_PTL          = 1300,
    eIGFX_CLS          = 1310,
    IGFX_NVL_XE3G      = 1340,
    eIGFX_FCS          = 1350,
    eIGFX_NVL          = 1360,
    eIGFX_NVL_AX       = 1365,

    eIGFX_MAX_PRODUCT,

    eIGFX_GENNEXT              = 0x7ffffffe,
    PRODUCT_FAMILY_FORCE_ULONG = 0x7fffffff
} IGFX_PLATFORM;

typedef enum
{
    PCH_UNKNOWN = 0,
    PCH_IBX,                                     // Ibexpeak
    PCH_CPT,                                     // Cougarpoint,
    PCH_CPTR,                                    // Cougarpoint Refresh,
    PCH_PPT,                                     // Panther Point
    PCH_LPT,                                     // Lynx Point
    PCH_LPTR,                                    // Lynx Point Refresh
    PCH_WPT,                                     // Wildcat point
    PCH_SPT,                                     // Sunrise point
    PCH_KBP,                                     // Kabylake PCH
    PCH_CNP_LP,                                  // Cannonlake LP PCH
    PCH_CNP_H,                                   // Cannonlake Halo PCH
    PCH_ICP_LP,                                  // ICL LP PCH
    PCH_ICP_N,                                   // ICL N PCH
    PCH_ICP_HP,                                  // ICL HP PCH
    PCH_LKF,                                     // LKF PCH
    PCH_TGL_LP,                                  // TGL LP PCH
    PCH_TGL_H,                                   // TGL H PCH
    PCH_CMP_LP,                                  // CML LP PCH
    PCH_CMP_H,                                   // CML Halo PCH
    PCH_CMP_V,                                   // CML V PCH
    PCH_EHL,                                     // MCC (Mule Creek Canyon) IOTG PCH IDs for Elkhart Lake
    PCH_JSP_N,                                   // JSL N PCH Device IDs for JSL+ Rev02
    PCH_ADL_S,                                   // ADL_S PCH
    PCH_ADL_P,                                   // ADL_P PCH
    PCH_ADL_N,                                   // ADL_N PCH
    PCH_MTL,                                     // MTL PCH
    PCH_RPL_S,                                   // RPL_S PCH
    PCH_ARL,                                     // ARL PCH
    PCH_DONT_CARE                  = 0x7ffffffe, // PCH information not needed post Gen13+ platforms, Need to keep this as +ve number as there are checks for < PCH_UNKNOWN
    PCH_PRODUCT_FAMILY_FORCE_ULONG = 0x7fffffff
} PCH_PRODUCT_FAMILY;

typedef enum
{
    IGFX_UNKNOWN_CORE = 0,
    IGFX_GEN3_CORE    = 1,  // Gen3 Family
    IGFX_GEN3_5_CORE  = 2,  // Gen3.5 Family
    IGFX_GEN4_CORE    = 3,  // Gen4 Family
    IGFX_GEN4_5_CORE  = 4,  // Gen4.5 Family
    IGFX_GEN5_CORE    = 5,  // Gen5 Family
    IGFX_GEN5_5_CORE  = 6,  // Gen5.5 Family
    IGFX_GEN5_75_CORE = 7,  // Gen5.75 Family
    IGFX_GEN6_CORE    = 8,  // Gen6 Family
    IGFX_GEN7_CORE    = 9,  // Gen7 Family
    IGFX_GEN7_5_CORE  = 10, // Gen7.5 Family
    IGFX_GEN8_CORE    = 11, // Gen8 Family
    IGFX_GEN9_CORE    = 12, // Gen9 Family
    IGFX_GEN10_CORE   = 13, // Gen10 Family
    IGFX_GEN11_CORE   = 14, // Gen11 Family
    IGFX_GEN12_CORE   = 15, // Gen12 Family
                            // Please add new GENs BEFORE THIS !
    IGFX_MAX_CORE = 16,     // Max Family, for lookup table

    IGFX_GENNEXT_CORE          = 0x7ffffffe, // GenNext
    GFXCORE_FAMILY_FORCE_ULONG = 0x7fffffff
} GFXCORE_FAMILY;

typedef enum
{
    IGFX_SKU_NONE = 0, // IGFX_SKU_UNKNOWN defined in \opengl\source\desktop\ail\ailgl_profiles.h
    IGFX_SKU_ULX  = 1,
    IGFX_SKU_ULT  = 2,
    IGFX_SKU_T    = 3,
    IGFX_SKU_ALL  = 0xff
} PLATFORM_SKU;

typedef enum __GTTYPE
{
    GTTYPE_GT1 = 0x0,
    GTTYPE_GT2,
    GTTYPE_GT2_FUSED_TO_GT1,
    GTTYPE_GT2_FUSED_TO_GT1_6, // IVB
    GTTYPE_GTL,                // HSW
    GTTYPE_GTM,                // HSW
    GTTYPE_GTH,                // HSW
    GTTYPE_GT1_5,              // HSW
    GTTYPE_GT1_75,             // HSW
    GTTYPE_GT3,                // BDW
    GTTYPE_GT4,                // BDW
    GTTYPE_GT0,                // BDW
    GTTYPE_GTA,                // BXT
    GTTYPE_GTC,                // BXT
    GTTYPE_GTX,                // BXT
    GTTYPE_GT2_5,              // CNL
    GTTYPE_GT3_5,              // SKL
    GTTYPE_UNDEFINED,          // Always at the end.
} GTTYPE,
*PGTTYPE;

typedef enum
{
    PLATFORM_NONE    = 0x00,
    PLATFORM_DESKTOP = 0x01,
    PLATFORM_MOBILE  = 0x02,
    PLATFORM_TABLET  = 0X03,
    PLATFORM_ALL     = 0xff, // flag used for applying any feature/WA for All platform types
} PLATFORM_TYPE;

typedef struct _SIMDRV_GFX_GMD_ID_DEF
{
    union {
        struct
        {
            unsigned int RevisionID : 6;
            unsigned int Reserved : 8;
            unsigned int GMDRelease : 8;
            unsigned int GMDArch : 10;
        } GmdID;
        unsigned int Value;
    };
} SIMDRV_GFX_GMD_ID;

typedef struct _PLATFORM_INFO
{
    IGFX_PLATFORM eProductFamily;
    // In future, if required we can extend PLATFORM_INFO to get below details as well
    PCH_PRODUCT_FAMILY ePCHProductFamily;
    GFXCORE_FAMILY     eDisplayCoreFamily;
    GFXCORE_FAMILY     eRenderCoreFamily;
    IGFX_PLATFORM      ePlatformType;
    unsigned short     usDeviceID;
    unsigned short     usRevId;
    unsigned short     usDeviceID_PCH;
    unsigned short     usRevId_PCH;
    GTTYPE             eGTType;
    unsigned int       sDisplayBlockID; /* of type SIMDRV_GFX_GMD_ID */
} PLATFORM_INFO, *PPLATFORM_INFO;
