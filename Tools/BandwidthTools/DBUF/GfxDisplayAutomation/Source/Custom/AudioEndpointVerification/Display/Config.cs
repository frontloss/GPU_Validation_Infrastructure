namespace AudioEndpointVerification
{
    using System;
    using System.Text;
    using System.Linq;
    using System.Threading;
    using System.Collections.Generic;

    public class Config
    {
        //SDC Flags
        const uint SDC_TOPOLOGY_INTERNAL = 0x00000001;
        const uint SDC_TOPOLOGY_CLONE = 0x00000002;
        const uint SDC_TOPOLOGY_EXTEND = 0x00000004;
        const uint SDC_TOPOLOGY_EXTERNAL = 0x00000008;
        const uint SDC_TOPOLOGY_SUPPLIED = 0x00000010;
        const uint SDC_USE_DATABASE_CURRENT = (SDC_TOPOLOGY_INTERNAL | SDC_TOPOLOGY_CLONE | SDC_TOPOLOGY_EXTEND | SDC_TOPOLOGY_EXTERNAL);
        const uint SDC_USE_SUPPLIED_DISPLAY_CONFIG = 0x00000020;
        const uint SDC_VALIDATE = 0x00000040;
        const uint SDC_APPLY = 0x00000080;
        const uint SDC_NO_OPTIMIZATION = 0x00000100;
        const uint SDC_SAVE_TO_DATABASE = 0x00000200;
        const uint SDC_ALLOW_CHANGES = 0x00000400;
        const uint SDC_PATH_PERSIST_IF_REQUIRED = 0x00000800;
        const uint SDC_FORCE_MODE_ENUMERATION = 0x00001000;
        const uint HSYNC_SDC_NUM = 4;
        const uint HSYNC_SDC_DENOM = 0;
        const UInt32 DISPLAYCONFIG_PATH_ACTIVE = 0x00000001;
        const int PRECISION3DEC = 1000;
        List<DisplayInfo> enumList;
        public Config(List<DisplayInfo> argenumList)
        {
            enumList = argenumList;
        }

        private DisplayType GetDisplayTypeByWinMonitorID(uint argMonitorID)
        {
            DisplayInfo displayInfo = enumList.Where(dI => dI.WindowsMonitorID == argMonitorID).FirstOrDefault();
            if (null != displayInfo)
                return displayInfo.DisplayType;
            return DisplayType.None;
        }

         
        public DisplayConfig GetConfig()
        {
            DisplayConfig dispConfig = new DisplayConfig();
            dispConfig.DisplayList = new List<DisplayType>();
            UInt32 numPathArrayElements = 0, numModeInfoArrayElements = 0;
            int returnVal = Interop.GetDisplayConfigBufferSizes((uint)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, ref numModeInfoArrayElements);
            DISPLAYCONFIG_PATH_INFO[] pathInfo = new DISPLAYCONFIG_PATH_INFO[numPathArrayElements];
            DISPLAYCONFIG_MODE_INFO[] modeInfo = new DISPLAYCONFIG_MODE_INFO[numModeInfoArrayElements];
            DISPLAYCONFIG_TOPOLOGY_ID topologyId = DISPLAYCONFIG_TOPOLOGY_ID.DISPLAYCONFIG_TOPOLOGY_NULL;
            returnVal = Interop.QueryDisplayConfig((UInt32)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, pathInfo,
            ref numModeInfoArrayElements, modeInfo, topologyId);
            if (returnVal != (int)QDC_SDC_StatusCode.SUCCESS)
            {
                return dispConfig;
            }

            if (numModeInfoArrayElements == 2 && numPathArrayElements == 1)
            {
                dispConfig.ConfigType = DisplayConfigType.SD;
                dispConfig.PrimaryDisplay = GetDisplayTypeByWinMonitorID(pathInfo[0].targetInfo.id);
                dispConfig.dispListParam.Add("Primary Display", dispConfig.PrimaryDisplay);
                dispConfig.SecondaryDisplay = DisplayType.None;
                dispConfig.TertiaryDisplay = DisplayType.None;
            }
            else if (numModeInfoArrayElements == 3 && numPathArrayElements == 2)
            {
                dispConfig.ConfigType = DisplayConfigType.DDC;
                dispConfig.PrimaryDisplay = GetDisplayTypeByWinMonitorID(pathInfo[0].targetInfo.id);
                dispConfig.SecondaryDisplay = GetDisplayTypeByWinMonitorID(pathInfo[1].targetInfo.id);
                dispConfig.dispListParam.Add("Primary Display", dispConfig.PrimaryDisplay);
                dispConfig.dispListParam.Add("Secondary Display", dispConfig.SecondaryDisplay);
                dispConfig.TertiaryDisplay = DisplayType.None;
            }
            else if (numModeInfoArrayElements == 4 && numPathArrayElements == 3)
            {
                dispConfig.ConfigType = DisplayConfigType.TDC;
                dispConfig.PrimaryDisplay = GetDisplayTypeByWinMonitorID(pathInfo[0].targetInfo.id);
                dispConfig.SecondaryDisplay = GetDisplayTypeByWinMonitorID(pathInfo[1].targetInfo.id);
                dispConfig.TertiaryDisplay = GetDisplayTypeByWinMonitorID(pathInfo[2].targetInfo.id);

                dispConfig.dispListParam.Add("Primary Display", dispConfig.PrimaryDisplay);
                dispConfig.dispListParam.Add("Secondary Display", dispConfig.SecondaryDisplay);
                dispConfig.dispListParam.Add("Tertiary Display", dispConfig.TertiaryDisplay);
            }
            else if (numModeInfoArrayElements == 4 && numPathArrayElements == 2)
            {
                dispConfig.ConfigType = DisplayConfigType.ED;
                dispConfig.PrimaryDisplay = GetDisplayTypeByWinMonitorID(pathInfo[0].targetInfo.id);
                dispConfig.SecondaryDisplay = GetDisplayTypeByWinMonitorID(pathInfo[1].targetInfo.id);
                dispConfig.dispListParam.Add("Primary Display", dispConfig.PrimaryDisplay);
                dispConfig.dispListParam.Add("Secondary Display", dispConfig.SecondaryDisplay);
                dispConfig.TertiaryDisplay = DisplayType.None;
            }
            //Tri Extended Config            
            else if (numModeInfoArrayElements == 6 && numPathArrayElements == 3)
            {
                dispConfig.ConfigType = DisplayConfigType.TED;
                dispConfig.PrimaryDisplay = GetDisplayTypeByWinMonitorID(pathInfo[0].targetInfo.id);
                dispConfig.SecondaryDisplay = GetDisplayTypeByWinMonitorID(pathInfo[1].targetInfo.id);
                dispConfig.TertiaryDisplay = GetDisplayTypeByWinMonitorID(pathInfo[2].targetInfo.id);
                dispConfig.dispListParam.Add("Primary Display", dispConfig.PrimaryDisplay);
                dispConfig.dispListParam.Add("Secondary Display", dispConfig.SecondaryDisplay);
                dispConfig.dispListParam.Add("Tertiary Display", dispConfig.TertiaryDisplay);
            }
            return dispConfig;
        }
    }
}