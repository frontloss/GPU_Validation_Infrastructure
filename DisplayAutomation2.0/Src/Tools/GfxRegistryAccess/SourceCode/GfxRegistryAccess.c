#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <malloc.h>
#include <string.h>
#include "GfxRegistryAccess.h"
#include "..\..\..\SystemUtility\SystemUtility\CommonDetails.h"

REGISTRY_ACCESS_ARGS     registryAccessArgs;
PFN_IGFX_REGISTRY_ACCESS pfnRegistryAccess = NULL;

int main(int argc, char *argv[])
{
    LONG registryAccessStatus = 0;
    Logger(WHITE, "********** Gfx Registry Access ***************\n\n");
    registryAccessStatus = ParseCmdLine(argc, argv);
    REGISTRY_ACCESS_STATUS_CHECK(registryAccessStatus);

    /* Set Default data count as 1 */
    if (0 == registryAccessArgs.dataCount)
    {
        registryAccessArgs.dataCount = 1;
    }
    Logger(LIGHTGRAY, "Key = %s ", registryAccessArgs.key);
    if (NULL != registryAccessArgs.subKey)
    {
        Logger(LIGHTGRAY, "& Sub_Key = %s", registryAccessArgs.subKey);
    }
    Logger(LIGHTGRAY, "\n");

    /* Access Gfx Registry*/
    if (NULL != pfnRegistryAccess)
        registryAccessStatus = pfnRegistryAccess();

    REGISTRY_ACCESS_STATUS_CHECK(registryAccessStatus);
    return ERROR_SUCCESS;
}

VOID ToUpper(PCHAR str, PUINT size)
{
    if (NULL == str)
        return;
    *size = 0;
    while (str[*size])
    {
        str[*size] = (toupper(str[*size]));
        (*size)++;
    }
    return str;
}

LONG ParseCmdLine(int argc, char *argv[])
{
    UINT  size    = 0;
    PCHAR cmdArgs = NULL;
    memset(&registryAccessArgs, 0, sizeof(REGISTRY_ACCESS_ARGS));
    for (UINT index = 1; index < argc; index++)
    {
        PCHAR args = argv[index];
        REGISTRY_ACCESS_NULL_CHECK(args);
        ToUpper(args, &size);
        if ((strcmp("/READ", args) == 0) || (strcmp("/R", args) == 0))
        {
            registryAccessArgs.operation = READ;
        }
        else if ((strcmp("/WRITE", args) == 0) || (strcmp("/W", args) == 0))
        {
            registryAccessArgs.operation = WRITE;
        }
        else if ((strcmp("/KEY", args) == 0) || (strcmp("/K", args) == 0))
        {
            registryAccessArgs.key = (argv[index + 1]);
            index++;
        }
        else if ((strcmp("/SUB_KEY", args) == 0) || (strcmp("/SK", args) == 0))
        {
            registryAccessArgs.subKey = (argv[index + 1]);
            index++;
        }
        else if ((strcmp("/TYEP", args) == 0) || (strcmp("/T", args) == 0))
        {
            cmdArgs = argv[index + 1];
            REGISTRY_ACCESS_NULL_CHECK(cmdArgs);
            ToUpper(cmdArgs, &size);
            index++;
            if (strcmp("REG_DWORD", cmdArgs) == 0)
                registryAccessArgs.dataType = REGISTRY_DWORD;

            else if (strcmp("REG_BINARY", cmdArgs) == 0)
                registryAccessArgs.dataType = REGISTRY_BINARY;
            else
            {
                Logger(RED, "Invalid data type !!\n");
                REGISTRY_ACCESS_STATUS_CHECK(ERROR_INVALID_DATA);
            }
        }
        else if ((strcmp("/AP", args) == 0))
        {
            cmdArgs = argv[index + 1];
            REGISTRY_ACCESS_NULL_CHECK(cmdArgs);
            ToUpper(cmdArgs, &size);
            index++;
            if (strcmp("GFX_0", cmdArgs) == 0)
                registryAccessArgs.provider = GFX_0;
            else if (strcmp("GFX_1", cmdArgs) == 0)
                registryAccessArgs.provider = GFX_1;
            else if (strcmp("AUDIO_BUS_DRV", cmdArgs) == 0)
                registryAccessArgs.provider = AUDIO_BUS_DRV;
            else if (strcmp("USB_KEYBOARD", cmdArgs) == 0)
                registryAccessArgs.provider = USB_KEYBOARD;
            else if (strcmp("INTERNAL_KEYBOARD", cmdArgs) == 0)
                registryAccessArgs.provider = INTERNAL_KEYBOARD;
            else
            {
                Logger(RED, "Invalid Access Provider !!\n");
                REGISTRY_ACCESS_STATUS_CHECK(ERROR_INVALID_DATA);
            }
        }
        else if ((strcmp("/DATA_COUNT", args) == 0) || (strcmp("/C", args) == 0))
        {
            PCHAR endptr;
            cmdArgs = argv[index + 1];
            REGISTRY_ACCESS_NULL_CHECK(cmdArgs);
            ToUpper(cmdArgs, &size);
            index++;
            registryAccessArgs.dataCount = strtoul(cmdArgs, &endptr, 10);
        }
        else if ((strcmp("/VALUE", args) == 0) || (strcmp("/V", args) == 0))
        {
            cmdArgs = argv[index + 1];
            REGISTRY_ACCESS_NULL_CHECK(cmdArgs);
            ToUpper(cmdArgs, &size);
            registryAccessArgs.data = cmdArgs;
            index++;
        }
        else
        {
            Logger(RED, "Invalid commandline parameters !!\n");
            REGISTRY_ACCESS_STATUS_CHECK(ERROR_INVALID_DATA);
        }
    }

    /* Verify command line arguments */
    if (registryAccessArgs.operation == NULL || registryAccessArgs.key == NULL || registryAccessArgs.dataType == NULL)
    {
        Logger(RED, "Invalid commandline parameters !!\n");
        REGISTRY_ACCESS_STATUS_CHECK(ERROR_INVALID_DATA);
    }

    if (registryAccessArgs.operation == READ && registryAccessArgs.dataType == REGISTRY_DWORD)
        pfnRegistryAccess = (PFN_IGFX_REGISTRY_ACCESS)RegistryReadDword;
    if (registryAccessArgs.operation == READ && registryAccessArgs.dataType == REGISTRY_BINARY)
        pfnRegistryAccess = (PFN_IGFX_REGISTRY_ACCESS)RegistryReadBinary;

    if (registryAccessArgs.operation == WRITE && registryAccessArgs.dataType == REGISTRY_DWORD)
        pfnRegistryAccess = (PFN_IGFX_REGISTRY_ACCESS)RegistryWriteDword;
    if (registryAccessArgs.operation == WRITE && registryAccessArgs.dataType == REGISTRY_BINARY)
        pfnRegistryAccess = (PFN_IGFX_REGISTRY_ACCESS)RegistryWriteBinary;
    return ERROR_SUCCESS;
}

VOID Logger(TEXT_COLOR argsTextColor, CONST PCHAR logMsgFormat, ...)
{
    va_list arg;
    va_start(arg, logMsgFormat);
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), argsTextColor);
    vfprintf(stdout, logMsgFormat, arg);
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), WHITE);
    va_end(arg);
}

LONG RegistryReadDword()
{
    LONG  status      = 0;
    DWORD dwordBuffer = 0;
    /* Read Registry */
    if (registryAccessArgs.subKey == NULL)
        status = ReadRegistry(registryAccessArgs.provider, registryAccessArgs.key, &dwordBuffer);
    else
        status = ReadRegistryEx(registryAccessArgs.provider, registryAccessArgs.key, registryAccessArgs.subKey, &dwordBuffer);

    /* Verify Status Code*/
    if (0 == status)
    {
        Logger(GREEN, "  Registry Access Success\n");
        Logger(LIGHTGRAY, "  Value = %d\n", dwordBuffer);
    }
    else
    {
        Logger(RED, "  Registry Access Failed !!\n");
    }
    return status;
}

LONG RegistryReadBinary()
{
    LONG  status    = 0;
    PBYTE outBuffer = (PBYTE)calloc(registryAccessArgs.dataCount, sizeof(BYTE));
    if (NULL == outBuffer)
    {
        Logger(RED, "Failed to allocate memory !!\n");
        return ERROR_NOT_ENOUGH_MEMORY;
    }

    /* Read Registry */
    if (registryAccessArgs.subKey == NULL)
        status = ReadRegistry(registryAccessArgs.provider, registryAccessArgs.key, outBuffer);
    else
        status = ReadRegistryEx(registryAccessArgs.provider, registryAccessArgs.key, registryAccessArgs.subKey, outBuffer);

    /* Verify Status Code*/
    if (0 == status)
    {
        Logger(GREEN, "  Registry Access Success\n");
        Logger(LIGHTGRAY, "  Value = ");
        for (UINT Index = 0; Index < registryAccessArgs.dataCount; Index++)
        {
            Logger(LIGHTGRAY, " %x", outBuffer[Index]);
        }
        Logger(LIGHTGRAY, "\n");
    }
    else
    {
        Logger(RED, "  Registry Access Failed !!\n");
    }
    free(outBuffer);
    outBuffer = NULL;
    return status;
}

LONG GfxRegistryWrite()
{
    LONG status = 0;
    /* Write Registry */

    if (registryAccessArgs.subKey == NULL)
        status = WriteRegistry(registryAccessArgs.provider, registryAccessArgs.key, registryAccessArgs.input_buffer, registryAccessArgs.dataType, registryAccessArgs.dataCount);
    else
        status = WriteRegistryEx(registryAccessArgs.provider, registryAccessArgs.key, registryAccessArgs.subKey, registryAccessArgs.input_buffer, registryAccessArgs.dataType,
                                 registryAccessArgs.dataCount);

    /* Verify Status Code*/
    if (0 == status)
    {
        Logger(GREEN, "  Registry Write Success\n");
    }
    else
    {
        Logger(RED, "  Registry Write Failed !!\n");
    }
    return status;
}

LONG RegistryWriteDword()
{
    PCHAR endptr;
    DWORD value                     = strtoul(registryAccessArgs.data, &endptr, 16);
    registryAccessArgs.input_buffer = &value;
    return GfxRegistryWrite();
}

LONG RegistryWriteBinary()
{
    // PCHAR values = (PCHAR)registryAccessArgs.data;
    LONG  status = 0;
    PCHAR token;
    PBYTE inBuffer    = NULL;
    ULONG value_index = 0;
    PCHAR rest        = registryAccessArgs.data;

    inBuffer = (PBYTE)calloc(registryAccessArgs.dataCount, sizeof(BYTE));
    if (NULL == inBuffer)
    {
        Logger(RED, "Failed to allocate memory !!\n");
        REGISTRY_ACCESS_STATUS_CHECK(ERROR_NOT_ENOUGH_MEMORY);
    }

    token = strtok(registryAccessArgs.data, ";");
    while (token != NULL)
    {
        inBuffer[value_index++] = strtol(token, NULL, 16);
        token                   = strtok(NULL, ";");
    }
    registryAccessArgs.input_buffer = inBuffer;
    status                          = GfxRegistryWrite();

    /* Deallocate memory*/
    free(inBuffer);
    inBuffer = NULL;
    return status;
}