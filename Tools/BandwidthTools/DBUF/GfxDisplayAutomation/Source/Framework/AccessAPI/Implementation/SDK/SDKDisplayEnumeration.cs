namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;
    using IgfxExtBridge_DotNet;

    public class SDKDisplayEnumeration : FunctionalBase
    {

        private const uint CRT_MONITOR_ID = 1;
        private const uint EDP_MONITOR_ID = 4096;

        public DisplayType CUISDKDisplayType(uint argSDKMonId)
        {
            DisplayType dispType = GetCUISDKDisplayType(argSDKMonId);

            if (dispType == DisplayType.None)
            {
                Log.Fail(" CUI SDK display type is {0}", DisplayType.None);
                Log.Message("Registering igfxdh.dll and igfxdi.dll and query cuisdk again.");
                CommonExtensions.StartProcess("regsvr32", string.Concat(@"/s ", "c:\\windows\\system32\\igfxdh.dll"), 1);
                CommonExtensions.StartProcess("regsvr32", string.Concat(@"/s ", "c:\\windows\\system32\\igfxdi.dll"), 1);

                dispType = GetCUISDKDisplayType(argSDKMonId);
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
                        APIExtensions.DisplayUtil.GetDeviceStatus(displayAdapter, index, out pMonitorID, ref pDevType, out pDevStatus, out pErrorDescription);
                        //Log.Verbose("DisplayUtil.GetDeviceStatus, AdapterName:{0}, Index:{1}, monitorID:{2}, pDevType:{3}, pDevStatus:{4}, pErrorDescription:{5}, DisplayType:{6}", displayAdapter, index, pMonitorID, pDevType, pDevStatus, pErrorDescription, (IGFX_DISPLAY_TYPES)pDevType);
                        if (pDevStatus != 1 && pMonitorID != 0)
                        {
                            if (pMonitorID == argSDKMonId)
                            {
                                Log.Verbose("MonitorID:{0} & displaytype:{1} for getting displaytype", pMonitorID, pDevType);
                                DisplayType dispType = GetDisplayType((IGFX_DISPLAY_TYPES)pDevType, base.EnumeratedDisplays);
                                return dispType;
                            }
                        }
                    }
                }
            }
            return DisplayType.None;
        }

        internal byte[] GetEDID(uint CUImonID)
        {
            List<byte> EDIDData = new List<byte>();
            IGFX_EDID_1_0 displayEDIDData = new IGFX_EDID_1_0();
            IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.UNKNOWN_ERROR;
            string errorDesc = "";

            Log.Verbose("Reading base EDID for display with Monitor ID - {0}", CUImonID);
            displayEDIDData.dwDisplayDevice = CUImonID;
            APIExtensions.DisplayUtil.GetEDIDData(ref displayEDIDData, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode != IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                Log.Verbose("GetEDIDData(). monitorID:{0}, Block:{1}", displayEDIDData.dwDisplayDevice, displayEDIDData.dwEDIDBlock);
                Log.Fail(false, "SDK:{0}:Unable to get base EDID-{1}", igfxErrorCode, errorDesc);
                return null;
            }

            if(displayEDIDData.EDID_Data[126] ==0) //This condition is kept to be in compliant with the existing functionality of taking 256 bytes of edid.
                EDIDData.AddRange(displayEDIDData.EDID_Data);
            else
                EDIDData.AddRange(displayEDIDData.EDID_Data.Take(128));
            
            Log.Verbose("Reading CEA extn EDID for display with Monitor ID - {0}", CUImonID);
            for (uint i = 0; i < displayEDIDData.EDID_Data[126]; i++)
            {
                IGFX_EDID_1_0 ceaEDIDData = new IGFX_EDID_1_0();
                ceaEDIDData.dwDisplayDevice = CUImonID;
                ceaEDIDData.dwEDIDBlock = i + 1;
                APIExtensions.DisplayUtil.GetEDIDData(ref ceaEDIDData, out igfxErrorCode, out errorDesc);
                if (igfxErrorCode != IGFX_ERROR_CODES.IGFX_SUCCESS)
                {
                    Log.Verbose("Extn Block: GetEDIDData(). monitorID:{0}, Block:{1}", ceaEDIDData.dwDisplayDevice, ceaEDIDData.dwEDIDBlock);
                    Log.Fail("SDK:{0}:Unable to get CEA extn EDID-{1}! A reboot might be required.", igfxErrorCode, errorDesc);
                    PowerEvent powerEvent = new PowerEvent();
                    powerEvent.SetMethod(new PowerParams() { PowerStates = PowerStates.S5, Delay = 10 });
                    return null;
                }
                EDIDData.AddRange(ceaEDIDData.EDID_Data.Take(128));
            }
            
            return EDIDData.ToArray();
        }
        private DisplayType GetDisplayType(IGFX_DISPLAY_TYPES deviceType, List<DisplayInfo> argEnumeratedDisplays)
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
        private DisplayType ConvertToDisplayType(List<DisplayInfo> argEnumeratedDisplays, DisplayType argDisplayType)
        {
            if (argEnumeratedDisplays.Any(dI => dI.DisplayType == argDisplayType))
                return argDisplayType + 1;
            return argDisplayType;
        }
    }
}