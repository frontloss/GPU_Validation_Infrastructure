/**
 * @file		PowerConsEscapesTest.h
 * @brief	Contains function pointer declarations and prototypes used in PowerConsEscapesTest.c
 *
 * @author	Ashish Tripathi
 */

/* Avoid multi inclusion of header file */
#pragma once

#include "..\PowerConsEscapes\PowerConsEscapes.h"
#include <stdio.h>

typedef INT (*INT_NO_ARGS)();

/**
 * @brief		Loads the PowerConsEscapes.dll
 * @return		HMODULE
 */
HMODULE LoadDLL();

/**
 * @brief									Driver Escapes for PowerCons
 * @param[in]	override					Boolean argument to override
 * @param[in]	lux							lux value
 * @return		VOID
 */
VOID TestALSOverride(BOOLEAN override, INT lux);