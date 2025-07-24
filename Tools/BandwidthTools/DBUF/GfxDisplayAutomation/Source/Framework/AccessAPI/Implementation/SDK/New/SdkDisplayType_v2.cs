namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using igfxSDKLib;
    using System;

    /*  Get SDK Display type through CUI SDK 8.0 */
    public class SdkDisplayType_v2 : FunctionalBase, ISDK
    {
        private IDisplay Display;
        public object Get(object args)
        {
            DisplayUIDMapper argDisplay = args as DisplayUIDMapper;
            GfxSDKClass GfxSDK = new GfxSDKClass();
            Display = GfxSDK.Display;

            IConnectedDisplays[] ConnectedDisplay = (IConnectedDisplays[])Display.GetConnectedDisplays();
            if (Display.Error == (uint)DISPLAY_ERROR_CODES.DISPLAY_SUCCESS &&
                ConnectedDisplay != null)
            {
                return GetDisplayType(ConnectedDisplay.Where(ID => ID.DisplayID.Equals(argDisplay.WindowsID)).FirstOrDefault().DisplayType);
            }
            else
                Log.Fail("Failed to GetConnectedDisplays : errorCode : {0}", Display.Error);
            return DisplayType.None;
        }

        private DisplayType GetDisplayType(IGFX_DISPLAYTYPE deviceType)
        {
            switch (deviceType)
            {
                case IGFX_DISPLAYTYPE.IGFX_DISPLAYTYPE_CRT:
                    return DisplayType.CRT;
                case IGFX_DISPLAYTYPE.IGFX_DISPLAYTYPE_DISPLAYPORT:
                    return DisplayType.DP;
                case IGFX_DISPLAYTYPE.IGFX_DISPLAYTYPE_HDMI:
                    return DisplayType.HDMI;
                case IGFX_DISPLAYTYPE.IGFX_DISPLAYTYPE_EMBEDDED_DISPLAYPORT:
                    return DisplayType.EDP;
                case IGFX_DISPLAYTYPE.IGFX_DISPLAYTYPE_WIRELESS_DISPLAY:
                    return DisplayType.WIDI;
                case IGFX_DISPLAYTYPE.IGFX_DISPLAYTYPE_DVI:
                    return DisplayType.DVI;
                default:
                    return DisplayType.None;
            }
        }


        public object GetAll(object args)
        {
            Log.Fail("Method not implemented");
            throw new NotImplementedException();
        }

        public object Set(object args)
        {
            Log.Fail("Method not implemented");
            throw new NotImplementedException();
        }
    }
}
