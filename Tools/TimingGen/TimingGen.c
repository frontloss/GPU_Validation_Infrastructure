// TimingGen.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "string.h"
#include <stdlib.h>
#include <assert.h>
#include <windows.h>
#include "..\\..\\..\\..\\gfx_Development\\mainline\\Source\\Softbios\\Napa\\CSL\\CSLCommon\\GlobalTimings.h"

#define GFXDBG_OFF             (0x00000000)
#define GFXDBG_CRITICAL        (0x00000001)
#define GFXDBG_NORMAL          (0x00000002) //| GFXDBG_CRITICAL)
#define GFXDBG_VERBOSE         (0x00000004) //| GFXDBG_NORMAL)
#define GFXDBG_FUNCTION_ENTRY  (0x80000000)
// Miniport specific levels
#define DBG_OFF                     GFXDBG_OFF
#define DBG_CRITICAL                GFXDBG_CRITICAL
#define DBG_CRITICAL_DEBUG          GFXDBG_CRITICAL
#define DBG_FUNCTION_ENTRY          GFXDBG_FUNCTION_ENTRY       
#define DBG_NORMAL                  GFXDBG_NORMAL
#define DBG_NONCRITICAL             GFXDBG_NORMAL
#define DBG_VERBOSE                 GFXDBG_VERBOSE
#define DBG_VERBOSE_VERBOSITY       GFXDBG_VERBOSE

#define SOFTBIOSASSERT assert

///////////////////////////////////////////////////
//
// Any special #define's required for implementation
//
///////////////////////////////////////////////////
#define ROUNDTONEARESTINT(p) (int)(p + 0.5)
#define PRECISION3DEC        1000       //multiply the floating point no to get 3 places after decimal
#define PRECISION4DEC        10000      //multiply the floating point no to get 4 places after decimal

// Required for CVT Timing Calculation
#define         ROUNDTO3DECIMALS(z)   (float)(ROUNDTONEARESTINT((z)*1000))/1000
#define         CHECK_ASPECTRATIO(q) (ULONG)(ulCellGran* (ULONG)(ulVpixels* q /ulCellGran))

////////////////////////////////////////////
//
//  18-byte DTD block
//  Refer Table 3.16, 3.17 & 3.18 of 
//  EDID spec
//
////////////////////////////////////////////
typedef struct _EDID_DTD_TIMING
{
#pragma pack(1)

    WORD wPixelClock;                   // Pixel clock / 10000

    UCHAR ucHA_low;                     // Lower 8 bits of H. active pixels
    UCHAR ucHBL_low;                    // Lower 8 bits of H. blanking
    union {
        UCHAR ucHAHBL_high;
        struct {
            UCHAR   ucHBL_high : 4;     // Upper 4 bits of H. blanking
            UCHAR   ucHA_high  : 4;     // Upper 4 bits of H. active pixels
        };
    };

    UCHAR ucVA_low;                     // Lower 8 bits of V. active lines
    UCHAR ucVBL_low;                    // Lower 8 bits of V. blanking
    union {
        UCHAR ucVAVBL_high;
        struct {
            UCHAR   ucVBL_high : 4;     // Upper 4 bits of V. blanking
            UCHAR   ucVA_high  : 4;     // Upper 4 bits of V. active pixels
        };
    };

    UCHAR ucHSO_low;                    // Lower 8 bits of H. sync offset
    UCHAR ucHSPW_low;                   // Lower 8 bits of H. sync pulse width
    union {
        UCHAR ucVSOVSPW_low;
        struct {
            UCHAR   ucVSPW_low : 4;     // Lower 4 bits of V. sync pulse width
            UCHAR   ucVSO_low  : 4;     // Lower 4 bits of V. sync offset
        };
    };
    union {
        UCHAR ucHSVS_high;
        struct {
            UCHAR   ucVSPW_high : 2;    // Upper 2 bits of V. sync pulse width
            UCHAR   ucVSO_high  : 2;    // Upper 2 bits of V. sync offset
            UCHAR   ucHSPW_high : 2;    // Upper 2 bits of H. sync pulse width
            UCHAR   ucHSO_high  : 2;    // Upper 2 bits of H. sync offset
        };
    };

    UCHAR ucHIS_low;                    // Lower 8 bits of H. image size in mm
    UCHAR ucVIS_low;                    // Lower 8 bits of V. image size in mm
    union {
        UCHAR ucHISVIS_high;
        struct {
            UCHAR   ucVIS_high : 4;     // Upper 4 bits of V. image size
            UCHAR   ucHIS_high : 4;     // Upper 4 bits of H. image size
        };
    };

    UCHAR ucHBorder;                    // H. border in pixels
    UCHAR ucVBorder;                    // V. border in pixels

    union {
        UCHAR ucFlags;                  // Hsync & Vsync polarity, etc. flags
        struct {
            UCHAR   ucStereo1    : 1;   // Stereo definition with bit[6:5]
            UCHAR   ucHSync_Pol  : 1;   // Hsync polarity (0: Neg, 1: Pos)
            UCHAR   ucVSync_Pol  : 1;   // Vsync polarity (0: Neg, 1: Pos)
            UCHAR   ucSync_Conf  : 2;   // Sync configuration
                                        // 00 : Analog composite
                                        // 01 : Bipolar analog composite
                                        // 00 : Digital composite
                                        // 00 : Digital separate
            UCHAR   ucStereo2    : 2;   // Stereo definition
                                        // 00 : Normal display, no stereo 
                                        // xx : Stereo definition with bit0
            UCHAR   ucInterlaced : 1;   // Interlaced / Non-interlaced
                                        // 0 : Non-interlaced
                                        // 1 : Interlaced
        };
    };

#pragma pack()
} EDID_DTD_TIMING, *PEDID_DTD_TIMING;

void PrintUsage(void);
int ComputeGTF(int argc, char* argv[]);
int ComputeCVT(int argc, char* argv[]);
int FindDMT(int argc, char* argv[]);

TIMING_INFO EDIDPARSER_GetTimingFromDTD(PEDID_DTD_TIMING pDTD);
BOOLEAN EDIDPARSER_GetDTDFromTimingInfo(PTIMING_INFO pTimingInfo, PEDID_DTD_TIMING pDTD);
TIMING_INFO EDIDPARSER_CreateGTFTiming(ULONG ulXRes, ULONG ulYRes, ULONG ulRRate, BOOLEAN bProgressiveMode);
TIMING_INFO EDIDPARSER_CreateCVTTimings(ULONG ulXRes, ULONG ulYRes, ULONG ulRRate, BOOLEAN bMargin_Req,BOOLEAN  bInterLaced, BOOLEAN   bRed_Blank_Req);

void PrintTimingInfo(PTIMING_INFO pTimingInfo);
void PrintDTD(PEDID_DTD_TIMING pDTD);

int main(int argc, char* argv[])
{
    printf("Timing Generator\r\n");
    printf("Copyright(c) 2009 Intel Corporation\r\n");
    printf("Note: DMT timings updated as of %s\r\n\r\n", __DATE__);

    if (argc <= 1)
    {
        PrintUsage();
    }
    else
    {
        if (strcmp(argv[1], "/gtf") == 0)
        {
            ComputeGTF(argc, argv);
        }
        else if (strcmp(argv[1], "/cvt") == 0)
        {
            ComputeCVT(argc, argv);
        }
        else if (strcmp(argv[1], "/dmt") == 0)
        {
            FindDMT(argc, argv);
        }
        else
        {
            PrintUsage();
        }
    }

    return 0;
}


void PrintUsage(void)
{
    printf("Missing parameters!\r\n");
    printf("Usage:-\r\n");
    printf(" TimingGen /gtf X Y RR i/p    - Uses VESA GTF to get timings\r\n");
    printf(" TimingGen /cvt X Y RR i/p    - Uses VESA CVT to get timings\r\n"); 
    printf("                                (No margin, reduced blanking option)\r\n");
    printf(" TimingGen /cvt X Y RR i/p nb - Uses VESA CVT to get timings\r\n");
    printf("                                (No margin, no reduced blanking option)\r\n");
    printf(" -where X, Y, RR is the mode information\r\n");
    printf("  i - Interlaced, p - Progressive, nb - Non-reduced blanking\r\n");

    return;
}

int ComputeGTF(int argc, char* argv[])
{
    ULONG ulXRes, ulYRes, ulRR;
    TIMING_INFO stTimingInfo;
    //TIMING_INFO stTempTiming;
    EDID_DTD_TIMING stDTD;

    if (argc == 5)
    {
        // Interlaved/progressive selection may not be present
        // Format is TimingGen /gtf X Y RR
        ulXRes = atoi(argv[2]);
        ulYRes = atoi(argv[3]);
        ulRR = atoi(argv[4]);

        stTimingInfo = EDIDPARSER_CreateGTFTiming(ulXRes, ulYRes, ulRR, TRUE);

        PrintTimingInfo(&stTimingInfo);
        EDIDPARSER_GetDTDFromTimingInfo(&stTimingInfo, &stDTD);
        PrintDTD(&stDTD);

        /*// Extra check?
        stTempTiming = EDIDPARSER_GetTimingFromDTD(&stDTD);
        if (memcmp(&stTempTiming, &stTimingInfo, sizeof(TIMING_INFO)) != 0)
        {
            printf("Timings from DTD:-\r\n");
            PrintTimingInfo(&stTempTiming);
        }*/
    }
    else if (argc == 6)
    {
        // Interlaved/progressive selection is present
        // Format is TimingGen /gtf X Y RR i/p
        ulXRes = atoi(argv[2]);
        ulYRes = atoi(argv[3]);
        ulRR = atoi(argv[4]);

        if (strcmp(argv[5], "i") == 0)
            stTimingInfo = EDIDPARSER_CreateGTFTiming(ulXRes, ulYRes, ulRR, FALSE);
        else
            stTimingInfo = EDIDPARSER_CreateGTFTiming(ulXRes, ulYRes, ulRR, TRUE);

        PrintTimingInfo(&stTimingInfo);
        EDIDPARSER_GetDTDFromTimingInfo(&stTimingInfo, &stDTD);
        PrintDTD(&stDTD);
    }
    else
    {
        PrintUsage();
    }

    return 0;
}

int ComputeCVT(int argc, char* argv[])
{
    ULONG ulXRes, ulYRes, ulRR;
    TIMING_INFO stTimingInfo;
    //TIMING_INFO stTempTiming;
    EDID_DTD_TIMING stDTD;
    BOOLEAN bReducedBlanking = TRUE;
    BOOLEAN bInterlaced = FALSE;

    if (argc == 5)
    {
        // Interlaved/progressive selection may not be present
        // Format is TimingGen /cvt X Y RR
        ulXRes = atoi(argv[2]);
        ulYRes = atoi(argv[3]);
        ulRR = atoi(argv[4]);

        stTimingInfo = EDIDPARSER_CreateCVTTimings(ulXRes, ulYRes, ulRR, FALSE, FALSE, TRUE);

        PrintTimingInfo(&stTimingInfo);
        EDIDPARSER_GetDTDFromTimingInfo(&stTimingInfo, &stDTD);
        PrintDTD(&stDTD);

        /*// Extra check?
        stTempTiming = EDIDPARSER_GetTimingFromDTD(&stDTD);
        if (memcmp(&stTempTiming, &stTimingInfo, sizeof(TIMING_INFO)) != 0)
        {
            printf("Timings from DTD:-\r\n");
            PrintTimingInfo(&stTempTiming);
        }*/
    }
    else if (argc >= 6)
    {
        // Interlaved/progressive selection is present
        // Format is TimingGen /cvt X Y RR i/p
        // OR        TimingGen /cvt X Y RR i/p nb
        ulXRes = atoi(argv[2]);
        ulYRes = atoi(argv[3]);
        ulRR = atoi(argv[4]);

        bReducedBlanking = TRUE;
        bInterlaced = FALSE;

        if (strcmp(argv[5], "i") == 0)
            bInterlaced = TRUE;

        if (argc > 6)
        {
            if (strcmp(argv[6], "nb") == 0)
                bReducedBlanking = FALSE;   
        }

        stTimingInfo = EDIDPARSER_CreateCVTTimings(ulXRes, ulYRes, ulRR, FALSE, bInterlaced, bReducedBlanking);

        PrintTimingInfo(&stTimingInfo);
        EDIDPARSER_GetDTDFromTimingInfo(&stTimingInfo, &stDTD);
        PrintDTD(&stDTD);
    }
    else
    {
        PrintUsage();
    }

    return 0;
}

int FindDMT(int argc, char* argv[])
{
    ULONG ulXRes, ulYRes, ulRR;
    EDID_DTD_TIMING stDTD;
    ULONG i = 0;

    // Format is TimingGen /dmt X Y RR

    if (argc == 5)
    {
        // Interlaved/progressive selection may not be present
        // Format is TimingGen /cvt X Y RR
        ulXRes = atoi(argv[2]);
        ulYRes = atoi(argv[3]);
        ulRR = atoi(argv[4]);

        for (i = 0; i < g_ulTotalStaticModes; i++)
        {
            if ((g_StaticModeTable[i].usXResolution == ulXRes) &&
                (g_StaticModeTable[i].usYResolution == ulYRes) &&
                (g_StaticModeTable[i].usRefreshRate == ulRR) &&
                (g_StaticModeTable[i].pTimingInfo != NULL))
            {
                PrintTimingInfo(g_StaticModeTable[i].pTimingInfo);
                EDIDPARSER_GetDTDFromTimingInfo(g_StaticModeTable[i].pTimingInfo, &stDTD);
                PrintDTD(&stDTD);

                return 0;
            }

        }
    }

    printf("No known DMTS timings for this!\r\n");
    PrintUsage();

    return 0;
}

void SoftbiosDebugMessage(ULONG ulDebugLevel, char *DebugMessageFmt, ...)
{
    va_list ArgList;
    va_start (ArgList, DebugMessageFmt);

    vprintf(DebugMessageFmt, ArgList);

    return;
}

void PrintTimingInfo(PTIMING_INFO pTimingInfo)
{
    if (pTimingInfo)
    {
        printf("TIMING_INFO structure elements (%d x %d @ %dHz", pTimingInfo->dwHActive, pTimingInfo->dwVActive, pTimingInfo->dwVRefresh);
        if (pTimingInfo->flFlags.bInterlaced)
            printf(" Interlaced)\r\n");
        else
            printf(" Progressive)\r\n");

        printf("dwSize          = %d (Hex: %X) \r\n", pTimingInfo->dwSize, pTimingInfo->dwSize);
        printf("dwDotClock      = %d (Hex: %X) \r\n", pTimingInfo->dwDotClock, pTimingInfo->dwDotClock);
        printf("dwHTotal        = %d (Hex: %X) \r\n", pTimingInfo->dwHTotal,pTimingInfo->dwHTotal);
        printf("dwHActive       = %d (Hex: %X) \r\n", pTimingInfo->dwHActive, pTimingInfo->dwHActive);
        printf("dwHBlankStart   = %d (Hex: %X) \r\n", pTimingInfo->dwHBlankStart, pTimingInfo->dwHBlankStart);
        printf("dwHBlankEnd     = %d (Hex: %X) \r\n", pTimingInfo->dwHBlankEnd, pTimingInfo->dwHBlankEnd);
        printf("dwHSyncStart    = %d (Hex: %X) \r\n", pTimingInfo->dwHSyncStart, pTimingInfo->dwHSyncStart);
        printf("dwHSyncEnd      = %d (Hex: %X) \r\n", pTimingInfo->dwHSyncEnd, pTimingInfo->dwHSyncEnd);
        printf("dwHRefresh      = %d (Hex: %X) \r\n", pTimingInfo->dwHRefresh, pTimingInfo->dwHRefresh);
        printf("dwVTotal        = %d (Hex: %X) \r\n", pTimingInfo->dwVTotal, pTimingInfo->dwVTotal);
        printf("dwVActive       = %d (Hex: %X) \r\n", pTimingInfo->dwVActive, pTimingInfo->dwVActive);
        printf("dwVBlankStart   = %d (Hex: %X) \r\n", pTimingInfo->dwVBlankStart, pTimingInfo->dwVBlankStart);
        printf("dwVBlankEnd     = %d (Hex: %X) \r\n", pTimingInfo->dwVBlankEnd, pTimingInfo->dwVBlankEnd);
        printf("dwVSyncStart    = %d (Hex: %X) \r\n", pTimingInfo->dwVSyncStart, pTimingInfo->dwVSyncStart);
        printf("dwVSyncEnd      = %d (Hex: %X) \r\n", pTimingInfo->dwVSyncEnd, pTimingInfo->dwVSyncEnd);
        printf("dwVRefresh      = %d (Hex: %X) \r\n", pTimingInfo->dwVRefresh, pTimingInfo->dwVRefresh);
        printf("flFlags         = %d (Hex: %X) \r\n", pTimingInfo->flFlags, pTimingInfo->flFlags);
        printf("\r\n");
    }

    return;
}

void PrintDTD(PEDID_DTD_TIMING pDTD)
{
    if (pDTD)
    {
        PUCHAR pTemp = (PUCHAR)pDTD;
        int i = 0;

        printf("DTD structure elements in hex:-\r\n");
        for (i = 0; i < sizeof(EDID_DTD_TIMING); i++)
        {
            printf("%Xh\r\n", *pTemp);
            pTemp++;
        }
        printf("\r\n");

        pTemp = (PUCHAR)pDTD;
        printf("DTD structure elements in hex for C code:-\r\n");
        for (i = 0; i < sizeof(EDID_DTD_TIMING); i++)
        {
            printf("0x%X, ", *pTemp);
            pTemp++;
        }
        printf("\r\n");

    }

    return;
}


BOOLEAN MODESMANAGER_IsDoubleWideMode(PTIMING_INFO pTimingInfo)
{
    return FALSE;
}

////////////////////////////////////////////////
//
// EDIDPARSER_GetTimingFromDTD: Method to get 
// TIMING_INFO from DTD.
// Returns an empty timing info if failed
//
////////////////////////////////////////////////
TIMING_INFO EDIDPARSER_GetTimingFromDTD(PEDID_DTD_TIMING pDTD)
{
    TIMING_INFO stTimingInfo;
    ULONG  ulXRes, ulYRes, ulRRate;
    ULONG  ulHTotal, ulVTotal, ulPixelClock, ulHBlank, ulVBlank, ulHSPW, ulVSPW;
    ULONG  ulHSO, ulVSO;

    memset(&stTimingInfo, 0, sizeof(stTimingInfo));

    ulXRes = (pDTD->ucHA_high << 8) + pDTD->ucHA_low;
    ulYRes = (pDTD->ucVA_high << 8) + pDTD->ucVA_low;

    if (pDTD->ucInterlaced)
        ulYRes = ulYRes*2;

    ulPixelClock = pDTD->wPixelClock * 10000;

    if((ulPixelClock==0)||(ulXRes==0)||(ulYRes==0))
    {
        SoftbiosDebugMessage(DBG_CRITICAL,"EDIDPARSER_GetTimingFromDTD() - Invalid DTD in the Edid\n");
        //SOFTBIOSASSERTPRINT(FALSE);
        return stTimingInfo;
    }

    //  Calculate refresh rate  
    ulHBlank = (pDTD->ucHBL_high << 8) + pDTD->ucHBL_low;
    ulHTotal = ulXRes + ulHBlank;
    ulVBlank = (pDTD->ucVBL_high << 8) + pDTD->ucVBL_low;
    if (pDTD->ucInterlaced)
        ulVBlank = ulVBlank*2;
    ulVTotal = ulYRes + ulVBlank;
    ulRRate = (ulPixelClock + ulHTotal * ulVTotal / 2)/ (ulHTotal * ulVTotal);
    if (pDTD->ucInterlaced)
        ulRRate = ulRRate*2;

    //  Calculate sync pulse width
    ulHSPW = (pDTD->ucHSPW_high << 8) + pDTD->ucHSPW_low;
    ulVSPW = (pDTD->ucVSPW_high << 4) + pDTD->ucVSPW_low;
    //Fix for 1940035: For interlaced mode, sync pulse width is doubled.
    if (pDTD->ucInterlaced)
        ulVSPW = ulVSPW*2;

    //  Calculate sync offset
    ulHSO = (pDTD->ucHSO_high << 8) + pDTD->ucHSO_low;
    ulVSO = (pDTD->ucVSO_high << 4) + pDTD->ucVSO_low;
    if (pDTD->ucInterlaced)
        ulVSO = ulVSO*2;

    //  Update mode timing infomation
    stTimingInfo.dwSize = sizeof (TIMING_INFO);
    stTimingInfo.dwDotClock = ulPixelClock;
    stTimingInfo.dwHTotal = ulHTotal;
    stTimingInfo.dwHActive = ulXRes;
    stTimingInfo.dwHBlankStart = ulXRes + pDTD->ucHBorder;
    stTimingInfo.dwHBlankEnd = ulHTotal - pDTD->ucHBorder - 1;
    stTimingInfo.dwHSyncStart = ulXRes + ulHSO;
    stTimingInfo.dwHSyncEnd = stTimingInfo.dwHSyncStart + ulHSPW - 1;
    stTimingInfo.dwHRefresh = ulPixelClock / ulHTotal;

    stTimingInfo.dwVTotal = ulVTotal;
    stTimingInfo.dwVActive = ulYRes;
    stTimingInfo.dwVBlankStart = ulYRes + pDTD->ucVBorder;
    stTimingInfo.dwVBlankEnd = ulVTotal - pDTD->ucVBorder - 1;
    stTimingInfo.dwVSyncStart = ulYRes + ulVSO;

    stTimingInfo.dwVSyncEnd = stTimingInfo.dwVSyncStart + ulVSPW - 1;
    stTimingInfo.dwVRefresh = ulRRate;

    stTimingInfo.flFlags.bInterlaced = pDTD->ucInterlaced;

    //  The sync polarity definition of TIMING_INFO is reversed from that of DTD's
    stTimingInfo.flFlags.bHSyncPolarity = ~pDTD->ucHSync_Pol;
    stTimingInfo.flFlags.bVSyncPolarity = ~pDTD->ucVSync_Pol;

    // Set double wide mode flag
    stTimingInfo.flFlags.bDoubleWideMode = MODESMANAGER_IsDoubleWideMode(&stTimingInfo);

    return stTimingInfo;
}

////////////////////////////////////////////////
//
// EDIDPARSER_GetDTDFromTimingInfo: Method to get 
// DTD from TIMING_INFO. Returns FALSE if failed
//
// Source: TranslateTiming2DTD() method in UAIM
//
////////////////////////////////////////////////
BOOLEAN EDIDPARSER_GetDTDFromTimingInfo(PTIMING_INFO pTimingInfo, PEDID_DTD_TIMING pDTD)
{
    BOOLEAN bRet = FALSE;

    if (pTimingInfo && pDTD)
    {
        DWORD dwHA      = 0;
        DWORD dwHBL     = 0;  
        DWORD dwVA      = 0; 
        DWORD dwVBL     = 0;  
        DWORD dwHSO     = 0; 
        DWORD dwHSPW    = 0; 
        DWORD dwVSO     = 0;
        DWORD dwVSPW    = 0; 

        memset(pDTD, 0, sizeof(EDID_DTD_TIMING));
        dwHA   = pTimingInfo->dwHActive;    
        dwHBL  = pTimingInfo->dwHTotal - pTimingInfo->dwHActive; 
        dwVA   = pTimingInfo->dwVActive;
        dwVBL  = pTimingInfo->dwVTotal - pTimingInfo->dwVActive;
        dwHSO  = (pTimingInfo->dwHSyncStart - pTimingInfo->dwHActive);
        dwHSPW = (pTimingInfo->dwHSyncEnd - pTimingInfo->dwHSyncStart + 1);
        dwVSO  = (pTimingInfo->dwVSyncStart - pTimingInfo->dwVActive);
        if((dwVSO & 0x3F) != 0)
            dwVSO = dwVSO >>1;
        dwVSPW = (pTimingInfo->dwVSyncEnd - pTimingInfo->dwVSyncStart + 1);

        // Fill out the DTD part #1
        pDTD->wPixelClock   = (WORD)(pTimingInfo->dwDotClock/10000); // Hz to 10KHz

        pDTD->ucHA_low      = (BYTE)(dwHA & 0xFF);
        pDTD->ucHBL_low     = (BYTE)(dwHBL & 0xFF);
        pDTD->ucHAHBL_high  = (BYTE)(((dwHA >> 8) << 4) | (dwHBL >> 8));
        pDTD->ucVA_low      = (BYTE)(dwVA & 0xFF);
        pDTD->ucVBL_low     = (BYTE)(dwVBL & 0xFF);
        pDTD->ucVAVBL_high  = (BYTE)(((dwVA >> 8) << 4) | (dwVBL >> 8));

        // Fill out the DTD part #1
        pDTD->ucHSO_low     = (BYTE)(dwHSO & 0xFF);
        pDTD->ucHSPW_low    = (BYTE)(dwHSPW & 0xFF);

        pDTD->ucVSOVSPW_low = (BYTE)(((dwVSO & 0x0F) << 4) | (dwVSPW & 0x0F));
        pDTD->ucHSVS_high = (BYTE)(((dwHSO >> 8) << 6) |
                                    ((dwHSPW >> 8) << 4) |
                                    ((dwVSO >> 8) << 2) |
                                    (dwVSPW >> 8));

        // Tibet 1549938 - The polarity of H/Vsync is fixed and not effected by resolution on DVI monitor
        // Fix - Setup the interlace and polarity flags in DTD using TimingInfo structure
        if(pTimingInfo->flFlags.bInterlaced)
            pDTD->ucFlags |= BIT7;

        // Let bits[6:5] = [0:0] = normal display, no stereo

        pDTD->ucFlags |= BIT4|BIT3;  // [4:3] = [1:1] = digital separate

        if (!pTimingInfo->flFlags.bVSyncPolarity)
            pDTD->ucFlags|= BIT2;       // Set + VSync Polarity
        if (!pTimingInfo->flFlags.bHSyncPolarity)
            pDTD->ucFlags |= BIT1;       // Set + HSync Polarity

        pDTD->ucVSO_high = (BYTE)((dwVSO >> 8) << 6);

        bRet = TRUE;
    }
    else
    {
        SOFTBIOSASSERT(FALSE);
    }

    return bRet;
}

////////////////////////////////////////////////
//
// CreateGTFTiming: Method to create a GTF timing
// as per VESA GTF standard
//
// Note: Copied from ValidateGTF source code
//
////////////////////////////////////////////////
TIMING_INFO EDIDPARSER_CreateGTFTiming(ULONG ulXRes, ULONG ulYRes, ULONG ulRRate, BOOLEAN bProgressiveMode)
{
    TIMING_INFO stTimingInfo = {0}; 
    
    if((ulRRate==0)||(ulXRes==0)||(ulYRes==0))
    {
        SoftbiosDebugMessage(DBG_CRITICAL,"Invalid inputs!\r\n");
        SOFTBIOSASSERT(FALSE);
    }
    else
    {
        //fixed defines as per VESA spec
        double flMarginPerct = 1.80;//size of top and bottom overscan margin as percentage of active vertical image
        double flCellGran   = 8.0;  //cell granularity
        ULONG  ulMinPorch   = 1;    // 1 line/char cell
        ULONG  ulVSyncRqd   = 3;    //width of vsync in lines
        float  flHSynchPerct    = 8.0;//width of hsync as a percentage of total line period
        float  flMin_Vsync_BP = 550.0;//Minimum time of vertical sync + back porch interval (us).
        double flBlankingGradient_M = 600.0;//The blanking formula gradient 
        double flBlankingOffset_C = 40.0;//The blanking formula offset
        double flBlankingScaling_K = 128.0;//The blanking formula scaling factor
        double flBlankingScalWeighing_J = 20.0;//The blanking formula scaling factor weighting
        //Spec defination ends here

        //Calculation of C',M'
        //C' = Basic offset constant
        //M' = Basic gradient constant
        double flCPrime = (flBlankingOffset_C - flBlankingScalWeighing_J)*(flBlankingScaling_K)/256.0 
                        + flBlankingScalWeighing_J;
        double flMPrime = flBlankingScaling_K/256 * flBlankingGradient_M;

        BOOLEAN bInterLaced = !bProgressiveMode;
        
        //calculation of timing paramters
        // Step 1: Round the Horizontal Resolution to nearest 8 pixel
        ULONG ulHPixels = ulXRes;
        ULONG ulHPixelsRnd = (ULONG) (ROUNDTONEARESTINT(ulHPixels/flCellGran)*flCellGran);

        // Step 2: Calculate Vertical line rounded to nearest integer   
        float flVLines = (float)ulYRes;
        ULONG ulVLinesRnd = (ULONG)ROUNDTONEARESTINT(bInterLaced?flVLines/2:flVLines);

        // Step 3: Find the field rate required (only useful for interlaced)
        float flVFieldRateRqd = (float)(bInterLaced?ulRRate*2:ulRRate);

        // Step 4 and 5: Calculate top and bottom margins, we assumed zero for now
        //assumption top/bottom margins are unused, if a requirement comes for use of
        //margin then it has to added as function input parameter
        ULONG ulTopMargin = 0;
        ULONG ulBottomMargin = 0;

        // Step 6: If Interlaced set this value which is used in the other calculations 
        float flInterLaced = (float)(bInterLaced?0.5:0);

        // Step 7: Estimate the Horizontal period in usec per line
        float flHPeriodEst = ((1/flVFieldRateRqd) - (flMin_Vsync_BP/1000000))/
                                (ulVLinesRnd+2*ulTopMargin+ulMinPorch+flInterLaced) * 1000000;

        // Step 8: Find the number of lines in V sync + back porch
        ULONG ulVSync_BP    = (ULONG)ROUNDTONEARESTINT(flMin_Vsync_BP/flHPeriodEst);

        // Step 9: Find the number of lines in V back porch alone
        ULONG ulVBackPorch = ulVSync_BP - ulVSyncRqd;

        // Step 10: Find the total number of lines in vertical field
        float flTotalVLines = ulVLinesRnd + ulTopMargin + ulBottomMargin + ulVSync_BP + flInterLaced
                              + ulMinPorch;

        // Step 11: Estimate the vertical field frequency
        float flVFieldRateEst = 1/flHPeriodEst/flTotalVLines * 1000000;

        // Step 12: Find actual horizontal period
        float flHPeriod       = flHPeriodEst/(flVFieldRateRqd/flVFieldRateEst);

        // Step 13: Find the actual vertical field frequency
        float flVFieldRate    = (1/flHPeriod/flTotalVLines)*1000000;

        // Step 14: Find the actual vertical frame frequency
        float flVFrameRate    = bInterLaced?flVFieldRate/2:flVFieldRate;
        
        // Step 15,16: Find the number of pixels in the left, right margins, we assume they are zero 
        ULONG ulLeftMargin = 0, ulRightMargin = 0;

        // Step 17: Find total number of active pixels in one line plus the margins 
        ULONG ulTotalActivePixels = ulHPixelsRnd + ulRightMargin + ulLeftMargin;

        // Step 18: Find the ideal blanking duty cycle form blanking duty cycle equation
        float flIdealDutyCycle = (float) (flCPrime - (flMPrime*flHPeriod/1000));
        
        // Step 19: Find the number of pixels in the blanking time to the nearest double charactr cell
        ULONG ulHBlankPixels = (ULONG) (ROUNDTONEARESTINT(ulTotalActivePixels*flIdealDutyCycle/(100 - flIdealDutyCycle)/(2*flCellGran))*(2*flCellGran));

        // Step 20: Find total number of pixels in one line
        ULONG ulTotalPixels = ulTotalActivePixels + ulHBlankPixels;

        // Step 21: Find pixel clock frequency
        //currently we are taking value till 3 places after decimal
        //If the precision need to be increased to 4 places of decimal replace the
        //PRECISION3DEC by PRECISION4DEC
        ULONG ulDecPrecisonPoint = PRECISION3DEC;
        //Get the pixel clcok till 3 places of decimals
        ULONG ulPixelClock = (ULONG)ROUNDTONEARESTINT((ulTotalPixels/flHPeriod)*ulDecPrecisonPoint);

        // Step 22:  Get the horizontal frequency
        float flHFreq       = (1000/flHPeriod)*1000;

        ULONG ulHSyncPixles = (ULONG) (ROUNDTONEARESTINT((ulTotalPixels/flCellGran) * (flHSynchPerct /100)) * flCellGran); 
        ULONG ulHSyncStart = ulTotalActivePixels + (ulHBlankPixels/2) - ulHSyncPixles;
        ULONG ulHSyncEnd   = ulTotalActivePixels + (ulHBlankPixels /2) - 1;
        //Gtf calculations ends here
        
        //This is the per frame total no of vertical lines
        ULONG ulTotalVLines = (ULONG)ROUNDTONEARESTINT(bInterLaced?2*flTotalVLines:flTotalVLines);

        // Set size
        stTimingInfo.dwSize = sizeof (TIMING_INFO);

        //This is done to get the pixel clock in Hz
        stTimingInfo.dwDotClock = ulPixelClock*(1000000/ulDecPrecisonPoint);    // from step 21
        stTimingInfo.dwHTotal = ulTotalPixels;          // from step 20
        stTimingInfo.dwHActive = ulTotalActivePixels;   // from step 17

        stTimingInfo.dwHBlankStart = ulTotalActivePixels;       
        stTimingInfo.dwHBlankEnd =  ulTotalPixels - 1;

        stTimingInfo.dwHSyncStart = ulHSyncStart;                               // from step 23                                             
        stTimingInfo.dwHSyncEnd = ulHSyncEnd;
        stTimingInfo.dwHRefresh = (ULONG)ROUNDTONEARESTINT(flHFreq);            // from step 22

        //calculate in case of interlaced the frame based parameters
        //instead of per field basis
        stTimingInfo.dwVTotal = ulTotalVLines;                                  // from step 10
        stTimingInfo.dwVActive = bInterLaced?ulVLinesRnd*2:ulVLinesRnd;         // from step 2

        stTimingInfo.dwVBlankStart = bInterLaced?ulVLinesRnd*2:ulVLinesRnd;                                 
        stTimingInfo.dwVBlankEnd =  ulTotalVLines - 1;

        //The interlaced paramter is also taken in to account to calculate the
        //sync start and end if the timings are to be generated for interlaced
        stTimingInfo.dwVSyncStart = (bInterLaced?ulVLinesRnd*2:ulVLinesRnd) + ulMinPorch +(ULONG)ROUNDTONEARESTINT(flInterLaced);                                               
        stTimingInfo.dwVSyncEnd = ulTotalVLines - (bInterLaced?2*ulVBackPorch:ulVBackPorch)- 3 *(ULONG)ROUNDTONEARESTINT(flInterLaced) - 1;         
        stTimingInfo.dwVRefresh = (ULONG)ROUNDTONEARESTINT(flVFrameRate);       // from step 14

        //Interlaced calculations are FIELD based instead of FRAME based
        //field related calculation are not done currently in the code. In future if 
        //this function is to be used for calculating the interlaced timings following
        //parameters need to be added and pipe registers should be programmed bsaed upon
        //the even field parameters.Parameters dependent on this are
        //1.Vertical Blank Time
        //2.Vertical Sync Time
        //3.Vertical Back Porch
        //vertical field period = flTotalVLines*flHPeriod/1000
        //odd  vertical blanking lines = ulVSync_BP+ulMinPorch
        //odd  vertical blanking time = (ulVSync_BP+ulMinPorch)*flHPeriod/1000
        //even vertical blanking lines = ulVSync_BP+ulMinPorch + 2*flInterLaced
        //odd vertical back porch time = ulVBackPorch+flInterLaced
        //even vertical back porch time = ulVBackPorch
        //odd  vertical front porch lines = (ulMinPorch+flInterLaced)
        //even vertical front porch lines = (ulMinPorch)

        // Flags info
        stTimingInfo.flFlags.ulFlags = 0;
        stTimingInfo.flFlags.bHSyncPolarity = 1;    // Negative
        stTimingInfo.flFlags.bVSyncPolarity = 0;    // Positive
        stTimingInfo.flFlags.bInterlaced = bInterLaced;

        // Set double wide mode flag
        stTimingInfo.flFlags.bDoubleWideMode = MODESMANAGER_IsDoubleWideMode(&stTimingInfo);
    }
    
    return stTimingInfo;
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////
//
// CreateCVTTimings: Method to create CVT timing
//
// Reference documents used are   CVT Standard (version 1.1) pdf file &
//   Spread Sheet provided by VESA for CVT timing calculation.
//
// In current version of CVT, there is no way of specifying values for input parameters
//    bMargin_Req & bInterLaced. So currently, these should be assigned FALSE. Check in future versions of CVT.
//////////////////////////////////////////////////////////////////////////////////////////////////////////////

TIMING_INFO EDIDPARSER_CreateCVTTimings(ULONG ulXRes, ULONG ulYRes, ULONG ulRRate, BOOLEAN bMargin_Req,BOOLEAN  bInterLaced, BOOLEAN   bRed_Blank_Req)
{
    TIMING_INFO stTimingInfo = {0}; 
    memset(&stTimingInfo, 0, sizeof(stTimingInfo));
    
    bMargin_Req = FALSE; //Not currently supported in CVT descriptor, so forcefully making it zero.

    if((ulRRate==0)||(ulXRes==0)||(ulYRes==0))
    {
        SoftbiosDebugMessage(DBG_CRITICAL,"EDIDPARSER_CreateCVTTimings:Invalid inputs!\r\n");
        SOFTBIOSASSERT(FALSE);
    }
    else
    {
        
    //fixed definations as per VESA spec

    // Constants which are same for Both Type of blankings
    const float flMarginPerct = 1.8f;               // margin percentage for all sides.
    const ULONG  ulCellGran = 8;                    // cell granularity
    const ULONG  ulMin_V_FPorch = 3;                // Variable for Both type of Blankings. Minimum V_Front Porch (in lines) given by spec
    const float  flClockStep = 0.250;               // Pixel clock freq should be integer multiple of this step.
    
    //Constants related to Normal-Blanking Calculations
    const ULONG  ulMin_V_BPorch = 6;                // minimum default back porch(in lines)
    const ULONG  ulHSynchPerct  = 8;                // width of hsync as a percentage of total line period
    const float  flMin_Vsync_BP = 550.0;            // Minimum time of vertical sync + back porch interval (us).
    const float  flBlankingGradient_M = 600.0;      // The blanking formula gradient 
    const float  flBlankingOffset_C = 40.0;         // The blanking formula offset
    const float  flBlankingScaling_K = 128.0;       // The blanking formula scaling factor
    const float  flBlankingScalWeighing_J = 20;     // The blanking formula scaling factor weighting
    

    //For Reduced Blanking (RB)
    float flRB_Min_VBlank=460.0;                  // In RB, minimum V Blanking period is 460 uSec.
    ULONG ulRB_Min_V_BPorch = 6;                  // Minimum V_Back Porch (in lines) given by spec
    

    // Common Variables in Both Type of Blankings.
    ULONG ulVSyncRqd=0;
    ULONG ulHBlankPixels = 0;   // In RB, Horizontal Blanking is fixed to 160 pixel clocks.                           
    float flHPeriodEst=0;
    float flTotalVLines=0;
    ULONG ulAct_VB_Lines=0;
    ULONG ulTotalPixels=0;
    float flAct_Pixel_Freq=0;
    float flAct_H_Freq=0;
    float flAct_VFieldRate=0;
    float flAct_VFrameRate=0;
    ULONG ulHSyncPixels=0;       // In RB, H sync width is fixed to 32 pixel clocks.

    // For Normal Blanking
    ULONG ulVSync_BP_Est=0;
    ULONG ulVSync_BP=0;
    ULONG ulVBackPorch=0;
    float flIdealDutyCycle=0;
    
    // For Reduced Blanking
    ULONG ulRB_VB_Lines=0;
    ULONG ulRB_Min_VB_Lines=0;
    ULONG ulRB_BackPorch=0;
        
    //Spec defination ends here
        
    //Calculation of C',M'
    //C' = Basic offset constant
    //M' = Basic gradient constant
    
    float flCPrime = (flBlankingOffset_C - flBlankingScalWeighing_J)*(flBlankingScaling_K)/256 
                    + flBlankingScalWeighing_J;
    float flMPrime = flBlankingScaling_K/256 * flBlankingGradient_M;


    //===========================================================================================
    //calculation of Common timing paramters
    //===========================================================================================
    
    // Step 1: Find the field rate required (only useful for interlaced)
    float flVFieldRateRqd = (float) ( bInterLaced ? (ulRRate*2) : ulRRate);

    // Step 2: Round the Horizontal Resolution to nearest 8 pixel--character cell multiple
    ULONG ulHPixels = ulXRes;
    ULONG ulHPixelsRnd = (ULONG) (ROUNDTONEARESTINT(ulHPixels/ulCellGran) * ulCellGran);

    //Step 3: Calculate side Margins.Implement when required.
    ULONG ulRightMargin=(ULONG) ( bMargin_Req ? ( ( (ulHPixelsRnd*flMarginPerct/100)/ulCellGran ) * ulCellGran) : 0 );
    ULONG ulLeftMargin = ulRightMargin;
    
    // Step 4: Find total number of active pixels in one line plus the margins 
    ULONG ulActivePixels = (ulHPixelsRnd + ulRightMargin + ulLeftMargin);
    
    // Step 5: Calculate Vertical line rounded to nearest integer   
    float flVLines = (float) (ulYRes);
    ULONG ulVLinesRnd = (ULONG) ROUNDTONEARESTINT(bInterLaced ? flVLines/2 : flVLines);

    ULONG ulVpixels= (ULONG) ROUNDTONEARESTINT(bInterLaced ? ulVLinesRnd*2 : ulVLinesRnd);
    
    // Step 6: Calculate top and bottom margins, 
    ULONG ulBottomMargin= bMargin_Req ? (ULONG) (ulVLinesRnd * flMarginPerct/100) : 0 ;
    ULONG ulTopMargin = ulBottomMargin;


    // Step 7: If Interlaced set this value which is used in the other calculations 
    double flInterLaced = bInterLaced?0.5:0;
    
    //Calculation of VSync width
    if (ulHPixelsRnd == CHECK_ASPECTRATIO(4/3) )
        ulVSyncRqd=4;

    else if (ulHPixelsRnd ==CHECK_ASPECTRATIO(16/9))
        ulVSyncRqd=5;

    else if (ulHPixelsRnd == CHECK_ASPECTRATIO(16/10))
        ulVSyncRqd=6;

    else if ((ulHPixelsRnd == CHECK_ASPECTRATIO(5/4)) ) 
        ulVSyncRqd=7;

    else if (ulHPixelsRnd == CHECK_ASPECTRATIO(15/9))
        ulVSyncRqd=7;
    else
        ulVSyncRqd=10;  // This is the case for custom Aspect Ratios

         
    //=============================================================================================
    //Calculation of CVT--CRT Timings
    //==============================================================================================
    
    if (! bRed_Blank_Req)
    {
    
        // Step 8: Estimate the Horizontal period in usec per line
         flHPeriodEst = (float)( ( (1/flVFieldRateRqd) - (flMin_Vsync_BP / 1000000) ) / (ulVLinesRnd+ 2*ulTopMargin + ulMin_V_FPorch + flInterLaced) * 1000000);
 
        // Step 9: Find the number of lines in V sync + back porch
         ulVSync_BP_Est = ( (ULONG) (flMin_Vsync_BP/flHPeriodEst) ) + 1;
         ulVSync_BP     = ulVSync_BP_Est < (ulVSyncRqd + ulMin_V_BPorch) ? (ulVSyncRqd + ulMin_V_BPorch) : ulVSync_BP_Est;
    
        
        // Step 10: Find the number of lines in V back porch alone
        ulVBackPorch = ulVSync_BP - ulVSyncRqd;
        ulVBackPorch= (ulVBackPorch < 7) ? 7 : ulVBackPorch;        // ulVBackPorch should always be >=7.
        ulVSync_BP  = ulVSyncRqd + ulVBackPorch;
    
        // For Step 11: Find the total number of lines in vertical field
        flTotalVLines = (float) (ulVLinesRnd + ulTopMargin * 2 + flInterLaced  + ulVSync_BP + ulMin_V_FPorch);      

        // Step 12: Find the ideal blanking duty cycle form blanking duty cycle equation
        flIdealDutyCycle =(flCPrime - (flMPrime * flHPeriodEst / 1000));
    
        // Step 13: Find the number of pixels in the blanking time to the nearest float character cell
        if (flIdealDutyCycle < 20)
            flIdealDutyCycle = 20;
    
        ulHBlankPixels = (ULONG) (((ULONG) (ulActivePixels * flIdealDutyCycle /(100 - flIdealDutyCycle) /(2*ulCellGran)))*(2*ulCellGran));
        
        // Step 14  Find total number of pixels in one line
        ulTotalPixels = ulActivePixels + ulHBlankPixels;

        // Step 15: Find Pixel clock freq.
         flAct_Pixel_Freq =( flClockStep * ((ULONG)((ulTotalPixels/flHPeriodEst)/flClockStep)));

        //Calculation of Horizontal Sync width

         ulHSyncPixels = (ULONG) (ROUNDTONEARESTINT(ulTotalPixels/ulCellGran * ulHSynchPerct /100) * ulCellGran);
    
        // Flags info
        stTimingInfo.flFlags.ulFlags = 0;
        stTimingInfo.flFlags.bHSyncPolarity = 1;    // Negative
        stTimingInfo.flFlags.bVSyncPolarity = 0;    // Positive
    
    }
    else
    {

    //=========================================================================================
    //CVT-Reduced Blanking Timing Calculation
    //=========================================================================================
            
        ulHBlankPixels = 160;
        ulHSyncPixels = 32;
        
        //Step 8:Estimate Horizontal Period

        flHPeriodEst = (float)( ((1000000/flVFieldRateRqd) - flRB_Min_VBlank) / (ulVLinesRnd + 2 * ulTopMargin));

        //Step 9:Find No. of Lines in Vertical Blanking
        ulRB_VB_Lines       = ((ULONG)  (flRB_Min_VBlank/flHPeriodEst))+1;

        //Step 10:Check Whether Vertical Blanking is sufficient.
        ulRB_Min_VB_Lines = ulVSyncRqd + ulMin_V_FPorch + ulRB_Min_V_BPorch;
        ulAct_VB_Lines = (ulRB_VB_Lines < ulRB_Min_VB_Lines) ? ulRB_Min_VB_Lines: ulRB_VB_Lines;

        //check on V_BackPorch ==6...in VESA CVT pdf file the limit is 7...but in Excel file it is 6.
        ulRB_BackPorch = ulAct_VB_Lines - ulVSyncRqd - ulMin_V_FPorch;
        ulRB_BackPorch = (ulRB_BackPorch < 6)? 6:ulRB_BackPorch;

        ulAct_VB_Lines = ulVSyncRqd + ulMin_V_FPorch + ulRB_BackPorch;
    
        // Step 11 for Both : Find the total number of lines in vertical field  
        flTotalVLines = (float) (ulVLinesRnd + ulTopMargin * 2 + flInterLaced  + ulAct_VB_Lines);

        // Step  12 : Find total number of pixels in one line
        ulTotalPixels = ulActivePixels + ulHBlankPixels;

        //Step 13:Find pixel clock freq.
        flAct_Pixel_Freq = (flClockStep * ((ULONG)((flVFieldRateRqd*flTotalVLines*ulTotalPixels/1000000)/flClockStep)));
    
        
        // Flags info
        stTimingInfo.flFlags.ulFlags = 0;
        stTimingInfo.flFlags.bHSyncPolarity = 0;    // Positive
        stTimingInfo.flFlags.bVSyncPolarity = 1;    // Negative
        
    }
        
        // Common equations for both type of timings.
         
        // Step 16 for NB & 14 ofr RB: Find actual horizontal Freq.
        flAct_H_Freq = (1000* flAct_Pixel_Freq/ulTotalPixels) ;


        // Step 17 for NB & 15 RB: Find the actual vertical field frequency
        flAct_VFieldRate  = (1000 * flAct_H_Freq/flTotalVLines);
    
        // Step 18 for NB & 16 for RB: Find the actual vertical frame frequency
        flAct_VFrameRate      = (bInterLaced ? flAct_VFieldRate/2 : flAct_VFieldRate);

        
        stTimingInfo.dwSize = sizeof (TIMING_INFO);
        stTimingInfo.dwDotClock =(ULONG) (ROUNDTO3DECIMALS(flAct_Pixel_Freq))*(1000000);            // from step 15-NB & 13- RB
        stTimingInfo.dwHTotal = ulTotalPixels;                                                      // from step 14-NB & 12-Rb
        stTimingInfo.dwHActive = ulActivePixels;                                                // from step 4 in Both

        stTimingInfo.dwHBlankStart = ulActivePixels;        
        stTimingInfo.dwHBlankEnd =  ulTotalPixels - 1;

        stTimingInfo.dwHSyncStart =  (ulActivePixels + (ulHBlankPixels/2) - ulHSyncPixels);         // from 23 in RB
        stTimingInfo.dwHSyncEnd = (ulActivePixels + (ulHBlankPixels /2) - 1);
        stTimingInfo.dwHRefresh = (ULONG)(ROUNDTONEARESTINT(ROUNDTO3DECIMALS(flAct_H_Freq)));       // from step 15-NB & 14-RB

        //calculate in case of interlaced the frame based parameters
        //instead of per field basis
        stTimingInfo.dwVTotal =(ULONG) (ROUNDTO3DECIMALS(flTotalVLines));                           // from step 11 in Both
        stTimingInfo.dwVActive = ulVpixels;                                                         // from step 5 in Both

        stTimingInfo.dwVBlankStart = ulVpixels;                                 
        stTimingInfo.dwVBlankEnd = (ULONG) (ROUNDTO3DECIMALS(flTotalVLines)) - 1;

        //The interlaced paramter is also taken in to account to calculate the
        //sync start and end if the timings are to be generated for interlaced
        stTimingInfo.dwVSyncStart = ulVpixels + ulMin_V_FPorch +(ULONG)ROUNDTONEARESTINT(ROUNDTO3DECIMALS(flInterLaced));                                               
        stTimingInfo.dwVSyncEnd = ulVpixels + ulMin_V_FPorch +(ULONG)ROUNDTONEARESTINT(ROUNDTO3DECIMALS(flInterLaced)) + ulVSyncRqd -1;         
        stTimingInfo.dwVRefresh = (ULONG)ROUNDTONEARESTINT(ROUNDTO3DECIMALS(flAct_VFrameRate));     // from step 18 in NB & 16 in RB
            
        stTimingInfo.flFlags.bInterlaced = bInterLaced;

        // Set double wide mode flag
        stTimingInfo.flFlags.bDoubleWideMode = MODESMANAGER_IsDoubleWideMode(&stTimingInfo);
    }
    return stTimingInfo;
}

