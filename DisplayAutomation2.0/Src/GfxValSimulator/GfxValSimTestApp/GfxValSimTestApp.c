/**
 * @file
 * @brief DisplayDeviceSimulationApp Test source file contains test functions to validate exposed
 * APIs of DisplayDeviceSumaltion.dll
 *
 * @ref GfxValSimTestApp.c
 * @author Reeju Srivastava, Aafiya Kaleem, Bharath Venkatesh
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

#pragma once
#include "GfxValSimTestApp.h"
#include "argtable3.h" //Argument parser library
#include "..\..\OsInterfaces\OsInterfaces\HeaderFiles\DisplayConfig.h"
#define GFX_0_ADPTER_INDEX L"gfx_0" // MA WA

/* global arg_xxx structs */
struct arg_lit * param_low_power, *help, *version;                  // litral arguments
struct arg_file *param_edid_file, *param_dpcd_file;                 // file arguments
struct arg_str * param_action, *param_ports, *param_connector_type; // string arguments
struct arg_int * param_lfp;                                         // unsigned integer arguments
struct arg_end * end;                                               // end of arguments
GFX_ADAPTER_INFO GFX_0_ADPTER_INFO;

int main(int argc, char *argv[])
{
    BOOL low_power_mode = FALSE;
    CHAR progname[]     = "GfxValSimTestApp.exe";
    UINT ret_val        = 1; // 1 = Failure; 0 = Success
    UINT exitcode       = 0; // 1 = Failure; 0 = Success
    UINT port_no        = 0;
    INT  nerrors        = 0;

    /* the global arg_xxx structs are initialised within the argtable */
    void *argtable[] = {
        help                 = arg_litn(NULL, "help", 0, 1, "Display this help and exit"),
        version              = arg_litn(NULL, "version", 0, 1, "Display version info and exit"),
        param_action         = arg_strn("a", "action", "<str>", 1, 1, "Action to perform plug/unplug/init"),
        param_ports          = arg_strn("p", "port", "<str>", 0, 5, "DP_A, HDMI_B, DP_B, HDMI_C"),
        param_low_power      = arg_litn("l", "low_power_mode", 0, 1, "Action in low power mode"),
        param_edid_file      = arg_filen("e", "edid_file", "<file>", 0, 5, "Edid file"),
        param_dpcd_file      = arg_filen("d", "dpcd_file", "<file>", 0, 5, "DPCD file"),
        param_connector_type = arg_strn("t", "port_type", "<str>", 0, 5, "Connector type (native/tc/tbt)"),
        param_lfp            = arg_intn(NULL, "is_lfp", "<int>", 0, 1, "Local flat panel"),
        end                  = arg_end(20),
    };

    GetAdapterInfo();
    if (0 != wcscmp(GFX_0_ADPTER_INFO.gfxIndex, GFX_0_ADPTER_INDEX))
    {
        printf("wrong adapter info exiting !!");
        return 1;
    }

    /* Error count while parsing command-line*/
    nerrors = arg_parse(argc, argv, argtable);

    /* special case: '--help' takes precedence over error reporting */
    if (help->count > 0)
    {
        printf("Usage: %s", progname);
        arg_print_syntax(stdout, argtable, "\n");
        printf("GfxValSimTestApp to plug and unplug simulated display panel.\n\n");
        arg_print_glossary(stdout, argtable, "  %-25s %s\n");
        exitcode = 0;
        goto exit;
    }

    if (version->count > 0)
    {
        printf("ValSim DLL version = %d\n", GetDLLVersion());
        exitcode = 0;
        goto exit;
    }

    /* If the parser returned any errors then display them and exit */
    if (nerrors > 0)
    {
        /* Display the error details contained in the arg_end struct.*/
        arg_print_errors(stdout, end, progname);
        printf("Try '%s --help' for more information.\n", progname);
        exitcode = 1;
        goto exit;
    }

    if (param_low_power->count > 0)
    {
        low_power_mode = TRUE;
    }

    /* Get GfxValSim handle*/
    if (GetGfxValSimHandle() != NULL)
        printf("GfxValSimHandle obtained successfully\n");
    else
    {
        printf("GfxValSimHandle failed\n");
        exitcode = 1;
        goto exit;
    }

    if (param_ports->count > 0)
    {
        for (int port = 0; port < param_ports->count; port++)
        {
            if (strcmp(*param_action->sval, "init") == 0 || strcmp(*param_action->sval, "INIT") == 0)
            {
                /* Call helper function to initialize all ports*/
                ret_val = HelperInit();
                if (ret_val == 0)
                    printf("Initialized specified ports successfully\n");
                else
                {
                    printf("Initializing specified ports failed\n");
                    exitcode = 1;
                }
                break;
            }
            else if (strcmp(*param_action->sval, "plug") == 0 || strcmp(*param_action->sval, "PLUG") == 0)
            {
                /* call helper function to plug*/
                printf("Port No %d\n", port);
                ret_val = HelperPlug(port, low_power_mode);
                if (ret_val == 0)
                    printf("Plug successful\n");
                else
                {
                    printf("Plug failed\n");
                    printf("Try to initialize the port before plugging\n");
                    exitcode = 1;
                }
            }
            else if (strcmp(*param_action->sval, "unplug") == 0 || strcmp(*param_action->sval, "UNPLUG") == 0)
            {
                /* call helper function to unplug*/
                ret_val = HelperUnPlug(port, low_power_mode);
                if (ret_val == 0)
                    printf("UnPlug successful\n");
                else
                {
                    printf("UnPlug failed\n");
                    exitcode = 1;
                }
            }
            else
            {
                printf("Specify proper action to perform\n");
                printf("Try '%s --help' for more information.\n", progname);
                exitcode = 1;
                break;
            }
        }
    }
    else
    {
        printf("Specify ports to perform action\n");
        printf("Try '%s --help' for more information.\n", progname);
        exitcode = 1;
    }

exit:
    /* deallocate each non-null entry in argtable[] */
    arg_freetable(argtable, sizeof(argtable) / sizeof(argtable[0]));
    return exitcode;
}

void GetAdapterInfo()
{
    GFX_ADAPTER_DETAILS adapterDetails = { 0 };
    GetAllGfxAdapterDetails(&adapterDetails);
    for (int adapterIndex = 0; adapterIndex < adapterDetails.numDisplayAdapter; adapterIndex++)
    {
        if (0 == wcscmp(adapterDetails.adapterInfo->gfxIndex, GFX_0_ADPTER_INDEX))
        {
            memcpy_s(&GFX_0_ADPTER_INFO, sizeof(GFX_ADAPTER_INFO), adapterDetails.adapterInfo, sizeof(GFX_ADAPTER_INFO));
        }
    }
}

/* Helper function to initialize all the ports specified via command line*/
UINT HelperInit()
{
    UINT     port_no   = 0;
    UINT     ret_val   = 1; // 1 = Failure; 0 = Success
    UINT *   uiPortNum = (UINT *)malloc(sizeof(UINT) * param_ports->count);
    BOOL *   uiIsLfp   = (BOOL *)malloc(sizeof(BOOL) * param_ports->count);
    RX_TYPE *eRxType   = (RX_TYPE *)malloc(sizeof(UINT) * param_ports->count);

    printf("Initializing ports\n");
    printf("Number of ports:\t%d \n", param_ports->count);
    for (int i = 0; i < param_ports->count; i++)
    {
        port_no          = GetPortNo(*(param_ports->sval + i));
        *(uiPortNum + i) = port_no;
        if (*(param_lfp->ival + i) == 1)
        {
            *(uiIsLfp + i) = TRUE;
        }
        else
        {
            *(uiIsLfp + i) = FALSE;
        }
        if (strstr(*(param_ports->sval + i), "DP_"))
        {
            *(eRxType + i) = DP;
        }
        else if (strstr(*(param_ports->sval + i), "HDMI_"))
        {
            *(eRxType + i) = HDMI;
        }
        else
        {
            *(eRxType + i) = RxInvalidType;
        }
        printf("port_no = %d \t port_name = %s \t sink_type = %d \t is_lfp = %d\n", uiPortNum[i], param_ports->sval[i], eRxType[i], uiIsLfp[i]);
    }
    ret_val = InitAllPorts(&GFX_0_ADPTER_INFO, sizeof(GFX_ADAPTER_INFO), param_ports->count, uiPortNum, eRxType, uiIsLfp);
    return ret_val;
}

/* Helper function to plug all the ports specified via command line*/
UINT HelperPlug(port_idx, low_power_mode)
{
    UINT port_no   = INVALID_PORT;
    UINT port_type = NATIVE;
    UINT ret_val   = 1; // 1 = Failure; 0 = Success
    BOOL is_lfp    = FALSE;

    port_no = GetPortNo(param_ports->sval[port_idx]);
    printf("HelperPlug port_no = %d\n", port_no);
    /* Get port connector type (Native/TC/TBT)*/
    port_type = ConnectorType(param_connector_type->sval[port_idx]);

    if (param_edid_file->count == 0)
    {
        printf("Specify proper EDID file for each ports\n");
        return ret_val;
    }

    /* During Plug of HDMI DPCD file path will be an empty string, making it NULL to handle from DLL*/
    if (param_dpcd_file->filename[port_idx] == "")
    {
        param_dpcd_file->filename[port_idx] = NULL;
    }

    if (*(param_lfp->ival + port_idx) == 1)
    {
        is_lfp = TRUE;
    }

    printf("\nPerforming plug of %s \n", param_ports->sval[port_idx]);
    printf("\nAction:\t%s \nPort:\t%s \nPort Number:\t%d \nConnector Type:\t%s \nLow power mode:\t%d \nedid_file:\t%s \ndpcd_file:\t%s \nis_lfp:\t%d \n", *param_action->sval,
           param_ports->sval[port_idx], port_no, param_connector_type->sval[port_idx], low_power_mode, param_edid_file->filename[port_idx], param_dpcd_file->filename[port_idx],
           is_lfp);
    if (port_no > 0)
    {
        printf("Calling plug\n");
        ret_val = Plug(&GFX_0_ADPTER_INFO, sizeof(GFX_ADAPTER_INFO), port_no, param_edid_file->filename[port_idx], param_dpcd_file->filename[port_idx], NULL, low_power_mode,
                       port_type, is_lfp, 0);
        Sleep(2000);
    }
    else
        printf("Invalid port number for Plug operation\n");

    return ret_val;
}

/* Helper function to unplug all the ports specified via command line*/
UINT HelperUnPlug(port_idx, low_power_mode)
{
    UINT port_no   = INVALID_PORT;
    UINT port_type = NATIVE;
    UINT ret_val   = 1; // 1 = Failure; 0 = Success

    port_no = GetPortNo(param_ports->sval[port_idx]);
    /* Get port connector type (Native/TC/TBT)*/
    port_type = ConnectorType(param_connector_type->sval[port_idx]);

    printf("\nPeforming unplug of %s \n", param_ports->sval[port_idx]);
    printf("\nAction:\t%s \nPort:\t%s \nPort Number:\t%d \nConnector Type:\t%s \nLow power mode:\t%d \n", *param_action->sval, param_ports->sval[port_idx], port_no,
           param_connector_type->sval[port_idx], low_power_mode);
    if (port_no > 0)
    {
        printf("Calling unplug\n");
        ret_val = UnPlug(&GFX_0_ADPTER_INFO, sizeof(GFX_ADAPTER_INFO), port_no, low_power_mode, port_type);
        Sleep(2000);
    }
    else
        printf("Invalid port number for UnPlug operation\n");

    return ret_val;
}

/* Function to map port number with port name*/
UINT GetPortNo(const char *port_name)
{
    UINT port_no = INVALID_PORT;
    if (param_ports->count == 0)
    {
        return port_no;
    }

    char port_index = '0';
    if (strstr(port_name, "HDMI"))
    {
        port_index = *(port_name + 5);
        switch (port_index)
        {
        case 'A':
        case 'a':
            port_no = INVALID_PORT;
            break;
        case 'B':
        case 'b':
            port_no = SIM_HDMI_B;
            break;
        case 'C':
        case 'c':
            port_no = SIM_HDMI_C;
            break;
        case 'D':
        case 'd':
            port_no = SIM_HDMI_D;
            break;
        case 'E':
        case 'e':
            port_no = SIM_HDMI_E;
            break;
        case 'F':
        case 'f':
            port_no = SIM_HDMI_F;
            break;
        case 'G':
        case 'g':
            port_no = SIM_HDMI_G;
            break;
        case 'H':
        case 'h':
            port_no = SIM_HDMI_H;
            break;
        case 'I':
        case 'i':
            port_no = SIM_HDMI_I;
            break;
        default:
            break;
        }
    }
    else if (strstr(port_name, "DP"))
    {
        port_index = *(port_name + 3);
        switch (port_index)
        {
        case 'A':
        case 'a':
            port_no = SIM_DP_A;
            break;
        case 'B':
        case 'b':
            port_no = SIM_DP_B;
            break;
        case 'C':
        case 'c':
            port_no = SIM_DP_C;
            break;
        case 'D':
        case 'd':
            port_no = SIM_DP_D;
            break;
        case 'E':
        case 'e':
            port_no = SIM_DP_E;
            break;
        case 'F':
        case 'f':
            port_no = SIM_DP_F;
            break;
        case 'G':
        case 'g':
            port_no = SIM_DP_G;
            break;
        case 'H':
        case 'h':
            port_no = SIM_DP_H;
            break;
        case 'I':
        case 'i':
            port_no = SIM_DP_I;
            break;
        default:
            break;
        }
    }

    return port_no;
}

UINT ConnectorType(const char *port_type)
{
    UINT type = NATIVE;
    if ((strstr(port_type, "tc")) || strstr(port_type, "TC"))
    {
        type = TC;
    }
    else if ((strstr(port_type, "tbt")) || strstr(port_type, "TBT"))
    {
        type = TBT;
    }

    return type;
}