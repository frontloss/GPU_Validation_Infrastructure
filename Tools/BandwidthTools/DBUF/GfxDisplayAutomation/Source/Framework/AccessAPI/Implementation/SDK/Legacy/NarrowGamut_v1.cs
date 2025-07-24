namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using IgfxExtBridge_DotNet;

    /*  Set Narrow Gamut through CUI SDK 7.0 */
    class NarrowGamut_v1 : FunctionalBase, ISDK
    {
        private IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.IGFX_SUCCESS;
        private string errorDesc = "";

        public object Set(object args)
        {
            NarrowGamutParams NarrowGamutData = args as NarrowGamutParams;
            IGFX_GAMUT gamut = new IGFX_GAMUT();
            bool status = true;
            gamut.dwDeviceUID = base.EnumeratedDisplays.Where(dI => dI.DisplayType == NarrowGamutData.DisplayType).Select(dI => dI.CUIMonitorID).FirstOrDefault();
            gamut.versionHeader.dwVersion = 1;
            SdkExtensions.LDisplayUtil.GetColorGamut(ref gamut, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_UNSUPPORTED_FEATURE)
            {
                Log.Message("NarrowGamut feature not supported for {0}", NarrowGamutData.DisplayType);
                status = false;
            }
            else if (igfxErrorCode != IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                Log.Message("Unable to fetch narrow gamut data for {0}", NarrowGamutData.DisplayType);
                status = false;
            }
            else if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                gamut.bEnableDisable = (NarrowGamutData.narrowGamutOption == NarrowGamutOption.EnableNarrowGamut) ? 1 : 0;
                APIExtensions.DisplayUtil.SetColorGamut(ref gamut, out igfxErrorCode, out errorDesc);
                if (igfxErrorCode != IGFX_ERROR_CODES.IGFX_SUCCESS)
                {
                    Log.Message("Unable to set Narrowgamut for {0}", NarrowGamutData.DisplayType);
                    status = false;
                }
                else if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
                {
                    Log.Message("Narrowgamut set {0} was success", NarrowGamutData.narrowGamutOption.ToString());
                    status = true;
                }
            }
            if (NarrowGamutData.driverStatus)
            {
                if (!status)
                    Log.Fail("Narrow gamut is not enabled after installing the driver");
                else
                    Log.Success("Narriw gamut is enbaled after installing driver");
            }
            else
            {
                //driver is not enabled for narrow gamut
                if (status)
                    Log.Fail("Narrow gamut is enabled after uninstalling driver");
                else
                    Log.Success("Narrow gamut is disbaled after unistalling driver");
            }
            return status;
        }

        public object Get(object args)
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
