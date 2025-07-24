/*------------------------------------------------------------------------------------------------*
 *
 * @file  log.h
 * @brief This file contains Implementation of Log, Initialize, Cleanup
 *
 *------------------------------------------------------------------------------------------------*/
#pragma once

#ifndef LOG_H
#define LOG_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdarg.h>
#include <string.h>
#include <windows.h>
#include <strsafe.h>
#include <time.h>

/* Preprocessor Macros*/
#ifdef _DLL_EXPORTS
#define CDLL_EXPORT __declspec(dllexport)
#else
#define CDLL_EXPORT __declspec(dllimport)
#endif

#define LOG_VERSION "1.0"

enum
{
    LOG_DEBUG,
    LOG_INFO,
    LOG_WARN,
    LOG_ERROR,
    LOG_FAIL
};

#ifdef __cplusplus
extern "C"
{
    extern char LIBRARY_NAME[22];
}
#else
extern char *LIBRARY_NAME; // Use this variable to assign independent library name
#endif

#define DEBUG_LOG(...) Log(LIBRARY_NAME, LOG_DEBUG, __FUNCTION__, __LINE__, __VA_ARGS__)
#define INFO_LOG(...) Log(LIBRARY_NAME, LOG_INFO, __FUNCTION__, __LINE__, __VA_ARGS__)
#define WARNING_LOG(...) Log(LIBRARY_NAME, LOG_WARN, __FUNCTION__, __LINE__, __VA_ARGS__)
#define ERROR_LOG(...) Log(LIBRARY_NAME, LOG_ERROR, __FUNCTION__, __LINE__, __VA_ARGS__)
#define FAIL_LOG(...) Log(LIBRARY_NAME, LOG_FAIL, __FUNCTION__, __LINE__, __VA_ARGS__)

#ifdef __cplusplus
extern "C"
{
#endif
    CDLL_EXPORT void Log(const char *pDllName, int level, const char *pFunctionName, int line, const char *pFmtString, ...);
#ifdef __cplusplus
}
#endif
// CDLL_EXPORT void Log(const char *pDllName, int level, const char *pFunctionName, int line, const char *pFmtString, ...);

CDLL_EXPORT void Initialize(const char *pFilePath, bool enableDebug);

CDLL_EXPORT void Cleanup();

#endif
