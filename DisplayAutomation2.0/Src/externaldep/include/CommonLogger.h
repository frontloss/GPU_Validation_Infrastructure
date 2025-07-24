/**
 * @file
 * @addtogroup CDll_CommonLogger
 * @brief
 * DLL provides interface to log the details and provide additional mechanims for custom log handlers.
 * @remarks
 * CommonLogger dll exposes APIs to register callback function for customer logger and macro to log messages.
 * <ul>
 * <li> @ref SetPythonLogger		\n \copybrief SetPythonLogger \n
 * <li> @ref CommonLogger			\n \copybrief CommonLogger	 \n
 * </ul>
 *
 * @author Beeresh
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

/* System defined headers*/
#include "windows.h"
#include <stdbool.h>
#include <stdarg.h>

/* Preprocessor Macros*/
#define EXPORT_API __declspec(dllexport)
#define MAX_LOG_BUFFER_SIZE 4096

/* Supported log categories*/
typedef enum _LOG_LEVEL
{
    ALL_LOGS      = 0,
    DEBUG_LOGS    = 10,
    INFO_LOGS     = 20,
    WARNING_LOGS  = 30,
    ERROR_LOGS    = 40,
    CRITICAL_LOGS = 50
} LOG_LEVEL;

typedef void (*LOGGERCALLBACK)(int verbose, const char *pMsg);

/**
 * @brief			Initilize the logger object received from python scripts
 * @param[in]        pLogger contains python object handler
 *
 * @return           True or False based on request success
 */
EXPORT_API void *SetLoggerCB(LOGGERCALLBACK pLogger);

EXPORT_API void ClearLoggerCB(PVOID pLogLock);

/**
* @brief            writes the log message to the log file
* @param[in]        pDllName - specify the DLL name which initiated logging
* @param[in]        type specify the logging level details like debug, info etc..,
* @param[in]        pMsg - Any message to be logged

*
* @return           True or False based on request success
*/
EXPORT_API void CommonLogger(char *pDllName, LOG_LEVEL type, char *pFunctionName, unsigned lineNo, char *pMsg, ...);

EXPORT_API VOID DLLLogger(char *pDllName, char *pFunctionName, unsigned lineNo, char *pMsg, ...);

#define TRACE_LOG(level, msg, ...)                                               \
    do                                                                           \
    {                                                                            \
        CommonLogger(DLL_NAME, level, __FUNCTION__, __LINE__, msg, __VA_ARGS__); \
    } while (FALSE);

#define DLL_TRACE_LOG(msg, ...)                                        \
    do                                                                 \
    {                                                                  \
        DLLLogger(DLL_NAME, __FUNCTION__, __LINE__, msg, __VA_ARGS__); \
    } while (FALSE);