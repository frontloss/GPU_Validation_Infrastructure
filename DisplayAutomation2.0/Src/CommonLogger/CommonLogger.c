/**
 * @file
 * @section CommonLogger_c
 * @brief Interface proivde TRACE_LOG macros for DLL to log messages. Adding provide callback mechanism to register
 *        logger handlers.
 *
 * @author Beeresh
 * @ref CommonLogger.c
 */

/***********************************************************************************************
 * INTEL CONFIDENTIAL. Copyright (c) 2016 Intel Corporation All Rights Reserved.
 *  <br>The source code contained or described herein and all documents related to the source code
 *  ("Material") are owned by Intel Corporation or its suppliers or licensors. Title to the
 *  Material remains with Intel Corporation or its suppliers and licensors. The Material contains
 *  trade secrets and proprietary and confidential information of Intel or its suppliers and licensors.
 *  The Material is protected by worldwide copyright and trade secret laws and treaty provisions.
 *  No part of the Material may be used, copied, reproduced, modified, published, uploaded, posted,
 *  transmitted, distributed, or disclosed in any way without Intel’s prior express written permission.
 *  <br>No license under any patent, copyright, trade secret or other intellectual property right is
 *  granted to or conferred upon you by disclosure or delivery of the Materials, either expressly,
 *  by implication, inducement, estoppel or otherwise. Any license under such intellectual property
 *  rights must be express and approved by Intel in writing.
 */

#pragma once

#include <time.h>
#include "stdio.h"
#include <stdlib.h>
#include <CommonLogger.h>

FILE *LOGGER_HANDLE; ///< File handle for write to a text file
CONST PCHAR LOG_FILE_NAME = "Logs\\DLLLogger.txt";

/* Callback function to log */
static LOGGERCALLBACK pLoggerCB      = NULL;
static int            g_logger_count = 0;

typedef struct _lock
{
    int lock_value;
} LoggerLock;

/**
 * @brief			Configures the python call back function received from python scripts
 * @param[in]        pLogger contains function pointer for python logging function
 *
 * @return           True or False based on request success
 */
EXPORT_API void *SetLoggerCB(LOGGERCALLBACK pLogger)
{
    pLoggerCB = pLogger;
    if (pLoggerCB != NULL)
    {
        if (g_logger_count == 0)
        {
            LoggerLock *log_lock = (LoggerLock *)malloc(sizeof(LoggerLock));
            if (log_lock != NULL)
            {
                log_lock->lock_value = g_logger_count++;
                return (PVOID)log_lock;
            }
        }
        else
        {
            fprintf_s(stderr, "Logger callback in use, release previous callback !!");
        }
    }
    else
    {
        fprintf_s(stderr, "Callback funtion pointer is NULL !!");
    }

    return NULL;
}

/**
 * @brief			API clear the logger CB function
 * @param[in]        pLogLock pointer to Logger Lock object
 *
 * @return           None
 */
EXPORT_API void ClearLoggerCB(PVOID pLogLock)
{
    if (pLogLock != NULL)
    {
        if (g_logger_count > 0)
        {
            free(pLogLock);
            pLoggerCB = NULL;
            g_logger_count--;
            fprintf_s(stderr, "Callback funtion pointer cleared !!");
        }
        else
        {
            fprintf_s(stderr, "Logger ref counter invalid !!");
        }
    }
    else
    {
        fprintf_s(stderr, "Callback funtion pointer is NULL, no action taken !!");
    }
}

/**
 * @brief            writes the log message to the log file
 * @param[in]        pDllName - specify the DLL name which initiated logging
 * @param[in]        type specify the logging level details like debug, info etc..,
 * @param[in]        pMsg - Any message to be logged
 *
 * @return           void
 */
EXPORT_API void CommonLogger(char *pDllName, LOG_LEVEL type, char *pFunctionName, unsigned lineNo, char *pMsgFormat, ...)
{
    va_list logArgs = NULL;                    // Variable argument list
    char    logMsgFormat[MAX_LOG_BUFFER_SIZE]; // log buffer which contains only formatted string
    char    logOutput[MAX_LOG_BUFFER_SIZE];    // log buffer which contains expanded format string of variable args
    va_start(logArgs, pMsgFormat);             // Retreive the variable arguments

    /* Formation of formatted string*/
    sprintf_s(logMsgFormat, MAX_LOG_BUFFER_SIZE, "%s:%s:%d - %s", pDllName, pFunctionName, lineNo, pMsgFormat);

    /* Expansion of formatted string with variable args*/
    vsprintf_s(logOutput, MAX_LOG_BUFFER_SIZE, logMsgFormat, logArgs);

    /* Check if python logger callback exists*/
    if (pLoggerCB == NULL)
    {
        // Enabling printf causes PSR entry and exit failures
        // fprintf_s(stderr, logOutput);
        return;
    }
    else
    {
        (*pLoggerCB)(type, logOutput);
    }
}

EXPORT_API VOID DLLLogger(char *pDllName, char *pFunctionName, unsigned lineNo, char *pMsg, ...)
{
    LOGGER_HANDLE = fopen(LOG_FILE_NAME, "a");
    char       logMsgFormat[MAX_LOG_BUFFER_SIZE];
    va_list    arg;
    time_t     s;
    struct tm *current_time;
    // time in seconds
    s = time(NULL);
    // to get current time
    current_time = localtime(&s);

    if (NULL != LOGGER_HANDLE)
    {
        va_start(arg, pMsg);

        sprintf_s(logMsgFormat, MAX_LOG_BUFFER_SIZE, "%02d:%02d:%02d    %s: %s:            %d - %s", current_time->tm_hour, current_time->tm_min, current_time->tm_sec, pDllName,
                  pFunctionName, lineNo, pMsg);
        vfprintf(LOGGER_HANDLE, logMsgFormat, arg);
        va_end(arg);
        fclose(LOGGER_HANDLE);
    }
}