#include<stdio.h>
#include<string.h>


#define TRUE  1
#define FALSE 0
#define MAX_SIZE 50

void printHelp()
{
    printf("Usage: DmcBin2H.exe <Platform> <Dmc binary name>\n");
    printf("      <Platform> SKL || BXT || CNL \n");
    printf("      e.g. DmcBin2H.exe BXT bxt_dmc_ver1_06.bin \n");
}

int main(int argc, char *argv[])
{
    int ulStatus = FALSE;
    FILE *ifp = NULL;
    FILE *ofp = NULL;
    unsigned int ucData = 0;
    unsigned long ulData = 0;
    int i = 0, count = 0;
    char ucPlatformName[MAX_SIZE] = { 0 };
    char ucHeaderFileName[MAX_SIZE] = { 0 };

    do
    {
        if (argc != 3)
        {
            printHelp();
            break;
        }

        if ((strcmp(argv[1], "SKL") != 0) && ((strcmp(argv[1], "BXT") != 0)) && ((strcmp(argv[1], "CNL") != 0)))
        {
            printHelp();
            break;
        }

        if ((fopen_s(&ifp, argv[2], "rb") != 0))
        {
            printf("%s file not found!!! \n", argv[2]);
            printHelp();
            break;
        }

        strcpy_s(ucHeaderFileName, MAX_SIZE, argv[2]);
        strcat_s(ucHeaderFileName, MAX_SIZE, ".h");

        if ((fopen_s(&ofp, ucHeaderFileName, "w") != 0))
        {
            break;
        }

        strcpy_s(ucPlatformName, MAX_SIZE, "ULONG g_ulCSR_Binary_");
        strcat_s(ucPlatformName, MAX_SIZE, argv[1]);
        strcat_s(ucPlatformName, MAX_SIZE, "[] = \n{");

        fprintf_s(ofp, "\n \n");
        fprintf_s(ofp, "%s", ucPlatformName);
        fprintf_s(ofp, "\n\t");

        while (fread_s(&ucData, 1, 1, 1, ifp) != 0)
        {
            ulData |= ucData << (i * 8);
            ucData = 0;
            if (i == 3)
            {
                fprintf_s(ofp, "0x%08X,  ", ulData);
                //printf("0x%08X,  ", ulData);
                ulData = 0;
            }

            if (++i == 4)
                i = 0;

            if ((++count % 16) == 0)
            {
                fprintf_s(ofp, "\n\t");
            }
        }
        fprintf_s(ofp, "\n};");

        fclose(ifp);
        fclose(ofp);

        ulStatus = TRUE;

    } while (FALSE);

    return ulStatus;
}
