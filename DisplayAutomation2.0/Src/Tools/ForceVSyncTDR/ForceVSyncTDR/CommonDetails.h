/**
 * @file
 * @author Suraj Gaikwad
 */

/**********************************************************************************
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

/* Avoid multi inclusion of header file*/
#pragma once

/* System header(s)*/
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <tchar.h>
#include <stdint.h>
#include <Windows.h>
#include <malloc.h>

#define DEBUG true

/* Required to comple on VS13 as _func_ is not defined in tool kit*/
#if defined(WIN32)
#define __func__ __FUNCTION__
#endif

/* Constants*/
#define MAX_DISPLAYS 16

/**
 * @brief         Debug multi args macro to print msg, filename, line and funtion name
 *				 Enable DEBUG defined in utility.h to print the messages on console
 *
 * @param[in]     fmt Can take multiple args or messgae
 *
 * @return        void
 */
#define DEBUGPRINT(fmt, ...)                                                                  \
    do                                                                                        \
    {                                                                                         \
        if (DEBUG)                                                                            \
            fprintf(stderr, "\n%s:%d:%s(): " fmt, __FILE__, __LINE__, __func__, __VA_ARGS__); \
    } while (0)

/**
 * @brief         Generic macro to check for the error is S_OK
 *
 * @param[in]     errorCode  - runtime error message
 *
 * @return        void
 */
#define RETERROR(errorCode)    \
    do                         \
    {                          \
        if (errorCode != S_OK) \
        {                      \
            return;            \
        }                      \
    } while (false)

/**
 * @brief         Generic macro to check for the error and return if error present
 *
 * @param[in]     hr - Expression to check for null
 * @param[in]     errorCode  - runtime error message
 *
 * @return        void
 */
#define CHECKERR(hr, errorCode) \
    errorCode = hr;             \
    RETERROR(hr)

/**
 * @brief         Generic macro for null pointer check
 *
 * @param[in]     expr - Expression to check for null
 * @param[in]     msg  - runtime error message
 *
 * @return        void
 */
#define NULLPTRCHECK(expr, errorCode) \
    {                                 \
        if ((NULL == expr))           \
        {                             \
            errorCode = E_POINTER;    \
            return;                   \
        }                             \
    }

/**
 * @brief         Generic macro for free memory
 *
 * @param[in]     ptr - Memory to free
 *
 * @return        void
 */
#define MEMRELEASE(ptr) \
    do                  \
    {                   \
        free((ptr));    \
        (ptr) = NULL;   \
    } while (0)