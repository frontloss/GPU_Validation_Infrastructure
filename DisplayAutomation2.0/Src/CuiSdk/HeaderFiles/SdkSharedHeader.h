/*------------------------------------------------------------------------------------------------*
 *
 * @file     SdkSharedHeader.h
 * @brief    This header file contains the Commonly used macros and structures used commonly across
 *           both Display Color and Display Port SDKs
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#pragma once
#include "Windows.h"
#include "IgfxExt.h"
#include "..\Logger\log.h"

#define NULL_PTR_CHECK(ptr)                         \
    {                                               \
        if (NULL == ptr)                            \
        {                                           \
            ERROR_LOG("NULL Pointer, Exiting !!!"); \
            return FALSE;                           \
        }                                           \
    }

#define VERIFY_STATUS(status)                \
    {                                        \
        if (0 != status)                     \
        {                                    \
            ERROR_LOG("SDK Request Failed"); \
            return FALSE;                    \
        }                                    \
    }

typedef struct _IGFX_VERSION_HEADER
{
    DWORD version;
    DWORD reserved;
} IGFX_VERSION_HEADER;
