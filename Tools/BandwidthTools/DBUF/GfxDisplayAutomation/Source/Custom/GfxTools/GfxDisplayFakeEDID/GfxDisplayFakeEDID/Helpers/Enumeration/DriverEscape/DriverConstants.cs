namespace Intel.VPG.Display.Automation
{
    internal enum DISPLAY_DETAILS_FLAG
    {
        QUERY_DISPLAYUID = 1,
        QUERY_DISPLAYTYPE_INDEX
    }
    public enum PORT_TYPES
    {
        NULL_PORT_TYPE = -1,
        ANALOG_PORT = 0,
        DVOA_PORT,
        DVOB_PORT,
        DVOC_PORT,
        DVOD_PORT,
        LVDS_PORT,
        RESERVED_PORT,
        INTHDMIB_PORT,
        INTHDMIC_PORT,
        INTHDMID_PORT,
        INT_DVI_PORT, //NA
        INTDPA_PORT, //Embedded DP For ILK
        INTDPB_PORT,
        INTDPC_PORT,
        INTDPD_PORT,
        TPV_PORT,  //This is for all the TPV Ports..
        INTMIPIA_PORT,
        INTMIPIC_PORT,
        MAX_PORTS
    }
    internal enum DISPLAY_TYPE
    {
        // DONOT change the order of type definitions
        // Add new types just before MAX_DISPLAY_TYPES & increment value of MAX_DISPLAY_TYPES
        NULL_DISPLAY_TYPE = 0,
        CRT_TYPE,
        TV_TYPE,
        DFP_TYPE,
        LFP_TYPE,
        MAX_DISPLAY_TYPES = LFP_TYPE
    }

    internal enum TOOLS_ESCAPE_CODE
    {
        TOOL_ESC_READ_MMIO_REGISTER,//DP Applet Tool, Test Automation
        TOOL_ESC_DP_APPLET_MISC_FUNC,//DP Applet Tool
        TOOL_ESC_GET_PNM_PIXELCLK_DATA,//PNM TOOL
        TOOL_ESC_SET_PNM_PIXELCLK_DATA,//PNM TOOL
        TOOL_ESC_GET_PSR_RESIDENCY_COUNTER,//BLA Tool 
        TOOL_ESC_QUERY_DISPLAY_DETAILS,//DP Applet Tool 
        TOOL_ESC_SIMULATE_DP12_TOPOLOGY,//DP Topology Simulator
        // MAX_CUI_COM_FUNCTIONS should be the last value in this enum
        MAX_TOOLS_ESCAPES
    }
}
