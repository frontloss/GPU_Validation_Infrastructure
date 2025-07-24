/*------------------------------------------------------------------------------------------------*
 *
 * @file	log.c
 * @brief	This file contains Implementation of Log, Initialize, Cleanup, DumpLastWindowsError
 * @author	Kiran Kumar Lakshmanan, Amit Sau
 *
 *------------------------------------------------------------------------------------------------*/

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <time.h>
#include <windows.h>
#include <strsafe.h>

#include "log.h"
#include "ETWTestLogging.h"

#define BUFFER_SIZE 1024

// Log File - Global file pointer
FILE *fp;
FILE *fpConfig;

static bool debugLog = false;

void DumpLastWindowsError();

static const char *Levels[] = { "DEBUG", "INFO", "WARNING", "ERROR", "FAIL" };

/*********************************************************************************
 * Log function performs logging by using the log level and other user parameters
 * Internally called by Logger MACROS defined in log.h based on the log level
 *
 * @param	pDllName		Refers to the DLL from which the API is called
 * @param	level			Logging level indicator (DEBUG/INFO/WARNING/ERROR/FAIL)
 * @param	functionName	Function name from which the logging API was called
 * @param	line			Line number from which the logging API was called
 * @param	pFmtString		Arguments passed by User API call
 *
 * @return	Returns Nothing
 ********************************************************************************/
void Log(const char *pDllName, int level, const char *functionName, int line, const char *pFmtString, ...)
{
    va_list   args;
    char      timestampBuffer[32];
    struct tm localTime;

    time_t currentTime = time(0);
    localtime_s(&localTime, &currentTime);

    if (fp == NULL || functionName == NULL || pDllName == NULL)
        return;

    // Do not log if "-loglevel debug" is not passed as argument from test commandline
    if (level == LOG_DEBUG && debugLog == false)
        return;

    timestampBuffer[strftime(timestampBuffer, sizeof(timestampBuffer), "%Y-%m-%d %H:%M:%S", &localTime)] = '\0';
    fprintf(fp, "[ %s  %-20s - %-4d:  %-32s() : %-8s ] ", timestampBuffer, pDllName, line, functionName, Levels[level]);

    // If Log level is Error/Failure, printing Windows last error code and message
    // if (strcmp(Levels[level], "ERROR") == EXIT_SUCCESS || strcmp(Levels[level], "FAIL") == EXIT_SUCCESS)
    // {
    //     DumpLastWindowsError();
    // }

    va_start(args, pFmtString);
    vfprintf(fp, pFmtString, args);
    va_end(args);

    fprintf(fp, "\n");
    fflush(fp);
}

/*********************************************************************************
 * DisplayConfigLog function writes user parameters to display_config_log.txt file
 * Internally called by Logger MACRO (DISPCONFIG_LOG) defined in log.h
 *
 * @param	functionName    Function name from which the logging API was called
 * @param	line            Line number from which the logging API was called
 * @param	pFmtString      Arguments passed by User API call
 *
 * @return	Returns Nothing
 ********************************************************************************/
void DisplayConfigLog(const char *pFunctionName, int line, const char *pFmtString, ...)
{
    va_list   args;
    char      timestampBuffer[32];
    struct tm localTime;

    time_t currentTime = time(0);
    localtime_s(&localTime, &currentTime);

    if (fpConfig == NULL || pFunctionName == NULL)
        return;

    timestampBuffer[strftime(timestampBuffer, sizeof(timestampBuffer), "%Y-%m-%d %H:%M:%S", &localTime)] = '\0';
    fprintf(fpConfig, "[ %s - %-4d:  %-18s()] ", timestampBuffer, line, pFunctionName);

    va_start(args, pFmtString);
    vfprintf(fpConfig, pFmtString, args);
    va_end(args);

    fprintf(fpConfig, "\n");
    fflush(fpConfig);
}

/*********************************************************************************
 * Initialize function performs initialization the log file, it handles the file
 * pointer to be referenced throughout logging scope of the DLLs
 *
 * @param	pFilePath	Log FilePath where the DLL log is to be generated
 * @param	enableDebug	Enable debug logs
 *
 * @return	Returns Nothing
 ********************************************************************************/
void Initialize(const char *pFilePath, bool enableDebug)
{
    EventRegisterDisplayAutomation_Test();
    errno_t errorCode;
    char    prefix[100];
    memset(prefix, '=', 100);
    errorCode = fopen_s(&fp, pFilePath, "a");
    if (errorCode != EXIT_SUCCESS)
    {
        return;
    }
    debugLog = enableDebug ? true : false;
    SetLastError(0);
    fprintf(fp, "%.*s", 83, prefix);
    fprintf(fp, "DLL LOGGER START");
    fprintf(fp, "% .*s\n", 83, prefix);
}

/*********************************************************************************
 * Initialize function performs initialization the log file, it handles the file
 * pointer to be referenced throughout logging scope of the DLLs
 *
 * @param	pFilePath   Log FilePath for DisplayConfig log to be generated
 *
 * @return	Returns Nothing
 ********************************************************************************/
void InitDisplayConfigLogger(const char *pFilePath)
{
    errno_t errorCode;
    char    prefix[100];
    memset(prefix, '=', 100);
    errorCode = fopen_s(&fpConfig, pFilePath, "a");
    if (errorCode != EXIT_SUCCESS)
    {
        return;
    }
    fprintf(fpConfig, "%.*s", 63, prefix);
    fprintf(fpConfig, "DISPLAY CONFIG LOG START");
    fprintf(fpConfig, "% .*s\n", 63, prefix);
}

/*********************************************************************************
 * Cleanup function performs flushing the log files with the contents
 *
 * @return	Returns Nothing
 ********************************************************************************/
void Cleanup()
{
    EventUnregisterDisplayAutomation_Test();
    char prefix[100];
    memset(prefix, '=', 100);

    if (fp)
    {
        fprintf(fp, "%.*s", 84, prefix);
        fprintf(fp, " DLL LOGGER END");
        fprintf(fp, "%.*s\n", 84, prefix);
        fclose(fp);
    }
    if (fpConfig)
    {
        fprintf(fpConfig, "%.*s", 64, prefix);
        fprintf(fpConfig, " DISPLAY CONFIG LOG END");
        fprintf(fpConfig, "%.*s\n", 64, prefix);
        fclose(fpConfig);
    }
}

/*********************************************************************************
 * DumpLastWindowsError function performs handles the Error and Fail Logs invoked
 * from DLLs and implements the windows error code handling and Logging of the same
 *
 * @return	Returns Nothing
 ********************************************************************************/
void DumpLastWindowsError()
{
    if (fp == NULL)
    {
        return;
    }
    LPVOID lpMsgBuf;
    LPVOID lpDisplayBuf;
    char   errorMsg[BUFFER_SIZE];
    SIZE_T convertedChars = 0;

    DWORD dwErr = GetLastError();

    FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS, NULL, dwErr, MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
                  (LPTSTR)&lpMsgBuf, 0, NULL);

    lpDisplayBuf = (LPVOID)LocalAlloc(LMEM_ZEROINIT, (lstrlen((LPCTSTR)lpMsgBuf) * sizeof(TCHAR)));
    StringCchPrintf((LPTSTR)lpDisplayBuf, LocalSize(lpDisplayBuf), TEXT("%s"), lpMsgBuf);

    if (wcstombs_s(&convertedChars, errorMsg, sizeof(errorMsg), (LPTSTR)lpDisplayBuf, lstrlen((LPTSTR)lpDisplayBuf) - 2) != EXIT_SUCCESS)
    {
        fprintf(fp, "%s", "Memory insufficient to print error message.");
    }
    else if (dwErr != 0)
    {
        fprintf(fp, "[ WINDOWS ERROR ] - %s ", errorMsg);
    }

    LocalFree(lpMsgBuf);
    LocalFree(lpDisplayBuf);
}
