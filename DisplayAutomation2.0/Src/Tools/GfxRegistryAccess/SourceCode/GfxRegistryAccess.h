#pragma once
#include "windows.h"
#include "..\..\..\SystemUtility\SystemUtility\SystemUtility.h"

#define MAX_LOG_BUFFER_SIZE 4096

#define REGISTRY_ACCESS_NULL_CHECK(address) \
    {                                       \
        if (NULL == address)                \
            return ERROR_NOT_ENOUGH_MEMORY; \
    }

typedef enum _OPERATION
{
    NONE,
    READ,
    WRITE
} OPERATION;

typedef enum _TEXT_COLOR
{
    BLACK        = 0,
    BLUE         = 1,
    GREEN        = 2,
    CYAN         = 3,
    RED          = 4,
    MAGENTA      = 5,
    BROWN        = 6,
    LIGHTGRAY    = 7,
    DARKGRAY     = 8,
    LIGHTBLUE    = 9,
    LIGHTGREEN   = 10,
    LIGHTCYAN    = 11,
    LIGHTRED     = 12,
    LIGHTMAGENTA = 13,
    YELLOW       = 14,
    WHITE        = 15,
} TEXT_COLOR;

typedef struct _REGISTRY_ACCESS_ARGS
{
    _In_ REGISTRY_ACCESS_PROVIDER provider;
    _In_ OPERATION operation;
    _In_ PCHAR key;
    _In_ PCHAR subKey;
    _In_ REGISTRY_TYPES dataType;
    _In_ ULONG dataCount;
    _In_ PVOID input_buffer;
    _In_ PCHAR data;
} REGISTRY_ACCESS_ARGS, *PREGISTRY_ACCESS_ARGS;

typedef LONG(__cdecl *PFN_IGFX_REGISTRY_ACCESS)(VOID);

VOID ToUpper(PCHAR str, PUINT size);

LONG ParseCmdLine(int argc, char *argv[]);

VOID Logger(TEXT_COLOR argsTextColor, CONST PCHAR logMsgFormat, ...);

LONG RegistryReadDword();

LONG RegistryReadBinary();

LONG GfxRegistryWrite();

LONG RegistryWriteDword();

LONG RegistryWriteBinary();
