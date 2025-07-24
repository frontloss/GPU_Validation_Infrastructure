#include "SHEUtilityTestApp.h"

// HMODULE hLib;

/* Main entry point*/
int main(int argc, char *argv[])
{
    /* Load and verify*/
    hLib = LoadDLL();
    if (NULL == hLib)
    {
        printf("\nFalied to Load DLL\n");
        return FALSE;
    }

    /* Loop multiple times to test the H/W*/
    if (SHEDeviceAttached())
    {
        int milliseconds = 5000;

        if ((strcmp(argv[1], "UNPLUG") == 0) && (strcmp(argv[2], "EDP") == 0) && (strcmp(argv[4], "PLUG") == 0) && (strcmp(argv[6], "RESERVON") == 0))
        {
            DISPLAYTYPE dType  = GetDisplayType(argv[2]);
            int         delay1 = atoi(argv[3]);
            int         delay2 = atoi(argv[5]);
            if (dType != UNKNOWN_DISPLAYTYPE)
            {
                DispeDPUnplugPLugHibernateWake(dType, delay1, delay2);
            }
        }
        else if ((strcmp(argv[1], "UNPLUG") == 0) && (strcmp(argv[2], "EDP") == 0) && (strcmp(argv[4], "PLUG") == 0))
        {
            DISPLAYTYPE dType  = GetDisplayType(argv[2]);
            int         delay1 = atoi(argv[3]);
            int         delay2 = atoi(argv[5]);
            if (dType != UNKNOWN_DISPLAYTYPE)
            {
                DispeDPUnplugPLug(dType, delay1, delay2);
            }
        }
        else if (strcmp(argv[1], "PLUG") == 0)
        {
            DISPLAYTYPE dType = GetDisplayType(argv[2]);
            int         delay = atoi(argv[3]);
            if (dType != UNKNOWN_DISPLAYTYPE)
            {
                HotPlugDisplay(dType, delay);
            }
        }
        else if (strcmp(argv[1], "UNPLUG") == 0)
        {
            DISPLAYTYPE dType = GetDisplayType(argv[2]);
            int         delay = atoi(argv[3]);
            if (dType != UNKNOWN_DISPLAYTYPE)
            {
                HotUnPlugDisplay(dType, delay);
            }
        }
        else if ((strcmp(argv[1], "DOCK") == 0) || (strcmp(argv[1], "UNDOCK") == 0))
        {
            int delay = atoi(argv[2]);
            if (strcmp(argv[1], "DOCK") == 0)
            {
                DockStatusSwitch(DOCK, delay);
                printf(" %s : %d", argv[1], delay);
            }
            else
            {
                DockStatusSwitch(UNDOCK, delay);
                printf(" %s : %d", argv[1], delay);
            }
        }
        else if ((strcmp(argv[1], "RESERVON") == 0) || (strcmp(argv[1], "RESERVOFF") == 0))
        {
            int delay = atoi(argv[2]);
            if (strcmp(argv[1], "RESERVON") == 0)
            {
                ReservedStatusSwitch(RESERVED_ON, delay);
                printf(" %s : %d", argv[1], delay);
            }
            else
            {
                ReservedStatusSwitch(RESERVED_OFF, delay);
                printf(" %s : %d", argv[1], delay);
            }
        }
    }

    return TRUE;
}

/* Load systemutility DLL*/
HMODULE LoadDLL()
{
    /* Load and get handle*/
    HMODULE retVal    = LoadLibraryA("SHEUtility.dll");
    DWORD   valReturn = GetLastError();
    return retVal;
}

DISPLAYTYPE GetDisplayType(char *displayStr)
{
    DISPLAYTYPE dType = UNKNOWN_DISPLAYTYPE;
    if (strcmp(displayStr, "EDP") == 0)
        dType = EDP;
    else if (strcmp(displayStr, "DP_1") == 0)
        dType = DP_1;
    else if (strcmp(displayStr, "DP_2") == 0)
        dType = DP_2;
    else if (strcmp(displayStr, "DP_3") == 0)
        dType = DP_3;
    else if (strcmp(displayStr, "DP_4") == 0)
        dType = DP_4;
    else if (strcmp(displayStr, "HDMI_1") == 0)
        dType = HDMI_1;
    else if (strcmp(displayStr, "HDMI_2") == 0)
        dType = HDMI_2;

    return dType;
}

char *GetDisplayTypeStr(DISPLAYTYPE dType)
{
    char *displaystr = "UNKNOWN_DISPLAYTYPE";
    if (dType == EDP)
        displaystr = "EDP";
    else if (dType == DP_1)
        displaystr = "DP_1";
    else if (dType == DP_2)
        displaystr = "DP_2";
    else if (dType == DP_3)
        displaystr = "DP_3";
    else if (dType == DP_4)
        displaystr = "DP_4";
    else if (dType == HDMI_1)
        displaystr = "HDMI_1";
    else if (dType == HDMI_2)
        displaystr = "HDMI_2";

    return displaystr;
}
bool SHEDeviceAttached()
{
    bool             status        = false;
    SHEDevicePresent fptrSHEDevice = (SHEDevicePresent)GetProcAddress(hLib, "IsSHEDeviceConnected");
    DWORD            valReturn     = GetLastError();
    if ((fptrSHEDevice)())
    {
        printf("Success:SHE Device is connected\n");
        status = true;
    }

    else
        printf("Error:SHE Device is not connected \n");

    return status;
}

void HotPlugDisplay(DISPLAYTYPE displayType, int delay)
{
    HotPlugUnPlug fptrHotPlugUnPlug = (HotPlugUnPlug)GetProcAddress(hLib, "HotPlug");
    printf(" HotPlug request recieved for %s \n", GetDisplayTypeStr(displayType));
    int retVal = (fptrHotPlugUnPlug)(displayType, delay);

    if (retVal)
        printf("Success:HotPlug of Display %s \n", GetDisplayTypeStr(displayType));
    else
        printf("Error:HotPlug of Display %s  Failed\n", GetDisplayTypeStr(displayType));
}

void HotUnPlugDisplay(DISPLAYTYPE displayType, int delay)
{
    HotPlugUnPlug fptrHotPlugUnPlug = (HotPlugUnPlug)GetProcAddress(hLib, "HotUnPlug");
    printf(" HotUnPlug request recieved for %s \n", GetDisplayTypeStr(displayType));
    int retVal = (fptrHotPlugUnPlug)(displayType, delay);

    if (retVal)
        printf("Success:HotUnPlug of Display %s \n", GetDisplayTypeStr(displayType));
    else
        printf("Error:HotUnPlug of Display %s  Failed\n", GetDisplayTypeStr(displayType));
}

void DispeDPUnplugPLug(DISPLAYTYPE displayType, int delay1, int delay2)
{
    eDPUnplugPLug fptreDPUnplugPLug = (eDPUnplugPLug)GetProcAddress(hLib, "DisplayeDPUnplugPLug");
    printf(" Display eDP Unplug PLug request recieved for %s \n", GetDisplayTypeStr(displayType));
    int retVal = (fptreDPUnplugPLug)(displayType, delay1, delay2);

    if (retVal)
        printf("Success:eDP Unplug PLug of Display %s \n", GetDisplayTypeStr(displayType));
    else
        printf("Error:eDP Unplug PLug of Display %s  Failed\n", GetDisplayTypeStr(displayType));
}

void DispeDPUnplugPLugHibernateWake(DISPLAYTYPE displayType, int delay1, int delay2)
{
    eDPUnplugPLugHibernateWake fptreDPUnplugPLugHibernateWake = (eDPUnplugPLugHibernateWake)GetProcAddress(hLib, "DisplayeDPUnplugPLugHibernateWake");
    printf(" Display eDP Unplug PLug request recieved for %s \n", GetDisplayTypeStr(displayType));
    int retVal = (fptreDPUnplugPLugHibernateWake)(displayType, delay1, delay2);

    if (retVal)
        printf("Success:eDP Unplug PLug Hibernate Wake of Display %s \n", GetDisplayTypeStr(displayType));
    else
        printf("Error:eDP Unplug PLug Hibernate Wake of Display %s  Failed\n", GetDisplayTypeStr(displayType));
}

void PowerLineSwitch(POWERLINE val, int delay)
{
    PowerSwitch fptrPowerLine = (PowerSwitch)GetProcAddress(hLib, "SwitchPowerLine");
    printf(" Powerline switch request recieved for %d \n", val);
    int retVal = (fptrPowerLine)(val, delay);

    if (retVal)
        printf("Success:Device is in %d status(AC(0)/DC(1)\n", val);
    else
        printf("Error:Device power state not changed \n");
}

void DockStatusSwitch(DOCKSWITCHSTATE val, int delay)
{
    DockSwitch fptrDock = (DockSwitch)GetProcAddress(hLib, "SwitchDock");
    printf(" Dock switch request recieved for %d \n", val);
    int retVal = (fptrDock)(val, delay);

    if (retVal)
        printf("Success:Device is in %d status(Dock(13)/UNDOCK(14)\n", val);
    else
        printf("Error:Device power state not changed \n");
}

void ReservedStatusSwitch(RESERVEDSTATE val, int delay)
{
    ReservedPortSwitch fptrDock = (ReservedPortSwitch)GetProcAddress(hLib, "SwitchReservedStatus");
    printf(" Reserved Port Status switch request recieved for %d \n", val);
    int retVal = (fptrDock)(val, delay);

    if (retVal)
        printf("Success:Device is in %d status(ON(15)/OFF(16)\n", val);
    else
        printf("Error:Device power state not changed \n");
}

void CheckLidSwitch(LIDSWITCHSTATE action)
{
    LidSwitch fptrLid = (LidSwitch)GetProcAddress(hLib, "LidSwitchButtonPress");
    int       retVal  = (fptrLid)(action, 0);

    if (retVal)
        printf("Success:Device Lidswitch Done\n");
    else
        printf("Error:Device Lidswitch not Done\n");
}
