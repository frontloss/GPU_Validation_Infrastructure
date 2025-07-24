namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using IgfxExtBridge_DotNet;

    /*  Get SDK Display type through CUI SDK 7.0 */
    public class SdkDisplayType_v1 : FunctionalBase, ISDK
    {
        private const uint CRT_MONITOR_ID = 1;
        private const uint EDP_MONITOR_ID = 4096;

        public object Get(object args)
        {
            DisplayUIDMapper argDisplay = args as DisplayUIDMapper;
            DisplayType dispType = GetCUISDKDisplayType(argDisplay.CuiID);
            if (dispType == DisplayType.None)
            {
                Log.Fail("SDK display type is {0}", DisplayType.None);
                Log.Message("Registering igfxdh.dll and igfxdi.dll and query cuisdk again.");
                CommonExtensions.StartProcess("regsvr32", string.Concat(@"/s ", "c:\\windows\\system32\\igfxdh.dll"), 1);
                CommonExtensions.StartProcess("regsvr32", string.Concat(@"/s ", "c:\\windows\\system32\\igfxdi.dll"), 1);
                dispType = GetCUISDKDisplayType(argDisplay.CuiID);
            }
            return dispType;
        }

        private DisplayType GetCUISDKDisplayType(uint argSDKMonId)
        {
            uint pMonitorID = 0; uint pDevType = 0; uint pDevStatus = 0;
            string pErrorDescription = "";
            List<string> displayAdapters = APIExtensions.GetDisplayAdapters();
            foreach (String displayAdapter in displayAdapters)
            {
                if (!displayAdapter.ToLower().Contains("v"))
                {
                    for (uint index = 0; index < 12; index++)
                    {
                        SdkExtensions.LDisplayUtil.GetDeviceStatus(displayAdapter, index, out pMonitorID, ref pDevType, out pDevStatus, out pErrorDescription);
                        if (pDevStatus != 1 && pMonitorID != 0)
                        {
                            if (pMonitorID == argSDKMonId)
                            {
                                //Log.Verbose("MonitorID:{0} & displaytype:{1} for getting displaytype", pMonitorID, pDevType);
                                DisplayType dispType = GetDisplayType((IGFX_DISPLAY_TYPES)pDevType);
                                return dispType;
                            }
                        }
                    }
                }
            }
            return DisplayType.None;
        }

        private DisplayType GetDisplayType(IGFX_DISPLAY_TYPES deviceType)
        {
            switch (deviceType)
            {
                case IGFX_DISPLAY_TYPES.IGFX_CRT:
                    return DisplayType.CRT;
                case IGFX_DISPLAY_TYPES.IGFX_DP:
                    return DisplayType.DP;
                case IGFX_DISPLAY_TYPES.IGFX_HDMI:
                    return DisplayType.HDMI;
                case IGFX_DISPLAY_TYPES.IGFX_LocalFP:
                    return DisplayType.EDP;
                case IGFX_DISPLAY_TYPES.IGFX_NIVO:
                    return DisplayType.WIDI;
                case IGFX_DISPLAY_TYPES.IGFX_ExternalFP:
                    return DisplayType.DVI;
                default:
                    return DisplayType.None;
            }
        }

        public object Set(object args)
        {
            Log.Fail("Method not implemented");
            throw new NotImplementedException();
        }

        public object GetAll(object args)
        {
            Log.Fail("Method not implemented");
            throw new NotImplementedException();
        }
    }
}
