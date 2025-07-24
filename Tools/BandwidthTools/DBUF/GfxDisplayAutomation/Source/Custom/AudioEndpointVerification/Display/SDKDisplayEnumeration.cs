namespace AudioEndpointVerification
{
    using System;
    using System.Linq;
    using System.Collections.Generic;
    using IgfxExtBridge_DotNet;

    public class SDKDisplayEnumeration
    {

        private const uint CRT_MONITOR_ID = 1;
        private const uint EDP_MONITOR_ID = 4096;

        public DisplayType CUISDKDisplayType(uint argSDKMonId)
        {
            uint pMonitorID = 0; uint pDevType = 0; uint pDevStatus = 0;
            string pErrorDescription = "";
            List<string> displayAdapters = APIExtensions.GetDisplayAdapters();
            foreach (String displayAdapter in displayAdapters)
            {
                if (!displayAdapter.ToLower().Contains("v"))
                {
                    for (uint index = 0; index < 6; index++)
                    {
                        APIExtensions.DisplayUtil.GetDeviceStatus(displayAdapter, index, out pMonitorID, ref pDevType, out pDevStatus, out pErrorDescription);
                        if (pDevStatus != 1 && pMonitorID != 0)
                        {
                            if (pMonitorID == argSDKMonId)
                                return GetDisplayType((IGFX_DISPLAY_TYPES)pDevType);
                        }
                    }
                }
            }
            return DisplayType.None;
        }

        internal byte[] GetEDID(uint CUImonID)
        {
            byte[] EDIDData = new byte[256];
            IGFX_EDID_1_0 displayEDIDData = new IGFX_EDID_1_0();
            IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.UNKNOWN_ERROR;
            string errorDesc = "";

            //Console.WriteLine("Reading base EDID for display with Monitor ID - {0}", CUImonID);
            displayEDIDData.dwDisplayDevice = CUImonID;
            APIExtensions.DisplayUtil.GetEDIDData(ref displayEDIDData, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode != IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                Console.WriteLine("SDK:{0}:Unable to get base EDID-{1}", igfxErrorCode, errorDesc);
                return null;
            }

            //Console.WriteLine("Reading CEA extn EDID for display with Monitor ID - {0}", CUImonID);
            for (uint i = 0; i < displayEDIDData.EDID_Data[126]; i++)
            {
                IGFX_EDID_1_0 ceaEDIDData = new IGFX_EDID_1_0();
                ceaEDIDData.dwDisplayDevice = CUImonID;
                ceaEDIDData.dwEDIDBlock = i + 1;
                APIExtensions.DisplayUtil.GetEDIDData(ref ceaEDIDData, out igfxErrorCode, out errorDesc);
                if (igfxErrorCode != IGFX_ERROR_CODES.IGFX_SUCCESS)
                {
                    Console.WriteLine("CUI SDK FAILED");
                    return null;
                }
                int startIdx = 0;
                if (ceaEDIDData.EDID_Data[127] == 0)
                    startIdx = 128 * ((int)i + 1);
                for (uint j = (i * 128); j < ((i + 1) * 128); j++)
                    displayEDIDData.EDID_Data[j + 128] = ceaEDIDData.EDID_Data[j + startIdx];
            }
            displayEDIDData.EDID_Data.CopyTo(EDIDData, 0);
            return EDIDData;
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