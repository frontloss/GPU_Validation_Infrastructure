#pragma once
#include "CuiSdk.h"

#define LOG_STATUS(status) status == 1 ? "PASS" : "FAIL"

VOID LogMessage(const char *, const char *);

// CUI SDK Common APIs

VOID CheckInitializeCUISDK();
VOID CheckUninitializeCUISDK();
