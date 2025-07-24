namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using igfxSDKLib;

    class WideGamut_v2 : FunctionalBase, ISDK
    {
        private WideGamutParams wideGamutParams;
        private IWideGamut SDKWideGamut;
        public object Set(object args)
        {
            wideGamutParams = args as WideGamutParams;
            Log.Message("Applying widegamut {0} to {1}", wideGamutParams.WideGamutLevel, wideGamutParams.DisplayType);
            if (base.MachineInfo.PlatformDetails.IsLowpower)
                return SetWideGamutForLP();
            else
                return SetWideGamutForGen();
        }

        public object Get(object args)
        {
            wideGamutParams = args as WideGamutParams;
            if (base.MachineInfo.PlatformDetails.IsLowpower)
                GetWideGamutForLP();
            else
                GetWideGamutForGen();
            return 0;
        }

        public object GetAll(object args)
        {
            Log.Fail("Method not implemented");
            throw new NotImplementedException();
        }

        private void GetWideGamutForLP()
        {
            Log.Fail("Method not implemented");
        }

        private void GetWideGamutForGen()
        {
            GfxSDKClass GfxSDK = new GfxSDKClass();
            SDKWideGamut = GfxSDK.Display.Color.WideGamut;
            uint windowsID = base.EnumeratedDisplays.Where(dI => dI.DisplayType == wideGamutParams.DisplayType).Select(dI => dI.WindowsMonitorID).FirstOrDefault();

            SDKWideGamut.Get(windowsID);
            if (SDKWideGamut.Error == (uint)WIDE_GAMUT_ERROR_CODES.WIDE_GAMUT_SUCCESS)
            {
                wideGamutParams.WideGamutLevel = (WideGamutLevel)SDKWideGamut.ExpansionLevel;
            }
            else if (SDKWideGamut.Error == (uint)WIDE_GAMUT_ERROR_CODES.WIDE_GAMUT_NOT_SUPPORTED)
            {
                wideGamutParams.WideGamutLevel = WideGamutLevel.Unsupported;
                Log.Fail("WideGamut feature not supported for display {0}", wideGamutParams.DisplayType);
            }
            else
            {
                Log.Fail("Unable to fetch widegamut level - Error Code: {0}", SDKWideGamut.Error);
            }
        }

        private bool SetWideGamutForGen()
        {
            bool status = false;
            GfxSDKClass GfxSDK = new GfxSDKClass();
            SDKWideGamut = GfxSDK.Display.Color.WideGamut;
            uint windowsID = base.EnumeratedDisplays.Where(dI => dI.DisplayType == wideGamutParams.DisplayType).Select(dI => dI.WindowsMonitorID).FirstOrDefault();

            SDKWideGamut.Get(windowsID);
            if (SDKWideGamut.Error == (uint)WIDE_GAMUT_ERROR_CODES.WIDE_GAMUT_SUCCESS)
            {
                SDKWideGamut.ExpansionLevel = (uint)wideGamutParams.WideGamutLevel;
                SDKWideGamut.Set(windowsID);
                if (SDKWideGamut.Error == (uint)WIDE_GAMUT_ERROR_CODES.WIDE_GAMUT_SUCCESS)
                {
                    Log.Success("widegamut level set to {0} for {1}", wideGamutParams.WideGamutLevel, wideGamutParams.DisplayType);
                    status = true;
                }
                else
                {
                    Log.Fail("Unable to set widegamut level for {0}- Error Code {1}", wideGamutParams.DisplayType, SDKWideGamut.Error);
                    wideGamutParams.WideGamutLevel = WideGamutLevel.Unsupported;
                }
            }
            else
            {
                Log.Fail("Fail to get Wide Gamut data for display {0} Error Code {1}", wideGamutParams.DisplayType, SDKWideGamut.Error);
            }
            return status;
        }

        private bool SetWideGamutForLP()
        {
            Log.Fail("Method not implemented");
            return false;
        }
    }
}
