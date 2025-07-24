#include "CuiSdkTestApp.h"
#include "log.h"

char *LIBRARY_NAME = "CuiSdkApp";

int main(int argc, char *argv[])
{
    do
    {
        Initialize("CuiSdkTestAppLog.txt", true);

        // Initialize CUI SDK
        CheckInitializeCUISDK();

        // Uninitialize CUI SDK
        CheckUninitializeCUISDK();

        Cleanup();
    } while (FALSE);
    return 0;
}

VOID CheckInitializeCUISDK()
{
    BOOLEAN status = FALSE;
    status         = InitializeCUISDKN();

    LogMessage("InitializeCUISDK", LOG_STATUS(status));
}

VOID CheckUninitializeCUISDK()
{
    BOOLEAN status = FALSE;
    status         = UninitializeCUISDKN();

    LogMessage("UninitializeCUISDK", LOG_STATUS(status));
}

// LogMessage function implements reusable INFO Logging and console print (Internal API)
VOID LogMessage(const char *str, const char *status)
{
    printf("\n%-60s -> %5s", str, status);
    INFO_LOG("%-80s -> %5s", str, status);
}
