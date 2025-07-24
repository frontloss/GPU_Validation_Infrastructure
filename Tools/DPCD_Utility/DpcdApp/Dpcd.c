#include "Dpcd.h"

extern char* LIBRARY_NAME = "DPCD App";

int main(int argc, char* argv[])
{
    BOOLEAN      status = FALSE;
    GFX_INFO_ARR gfxArr = { 0 };
    GFX_INFO     gfxInfo = { 0 };
    ULONG        buffer[MAX_LUT_AUX_BUFSIZE];

    if (argc != 2) {
        printf("Usage: %s <hex_value>\n", argv[0]);
        return 1;
    }

    char* offsetIn = argv[1];
    bool isHex = false;

    if (strncmp(offsetIn, "0x", 2) == 0)
    {
        offsetIn += 2;
        isHex = true;
    }

    ULONG offset = (ULONG)strtol(offsetIn, NULL, isHex ? 16 : 10);

    Initialize("Logger.txt", TRUE);

    do
    {
        status = QueryAdapterDetails(&gfxArr);
        printf("\n Adapter status: %d", status);

        for (int i = 0; i < gfxArr.count; i++)
        {
            // Fill data into GFX_INFO struct
            printf("\nCurrent target id - 0x%X and offset - 0x%X", gfxArr.arr[i].targetID, offset);
            gfxInfo.targetID = gfxArr.arr[i].targetID;
            gfxInfo.adapterID = gfxArr.arr[i].adapterID;
            gfxInfo.outputTechnology = gfxArr.arr[i].outputTechnology;

            // Call DPCD read
            status = DpcdRead(gfxInfo, offset, MAX_LUT_AUX_BUFSIZE, buffer);
            printf("\nDPCD data - 0x%X", buffer[0]);
            LogMessage("DPCD read status", status);
        }

    } while (FALSE);

    Cleanup();
    return 0;
}

VOID LogMessage(char* str, BOOLEAN status)
{
    printf("\n%-60s -> %5s", str, status == TRUE ? "PASS" : "FAIL");
    INFO_LOG("%-80s -> %5s", str, status == TRUE ? "PASS" : "FAIL");
}
