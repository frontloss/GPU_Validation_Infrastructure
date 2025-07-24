namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using igfxSDKLib;

    /*  Set Narrow Gamut through CUI SDK 8.0 */
    class NarrowGamut_v2 : FunctionalBase, ISDK
    {
        private INarrowGamut NarrowGamut;
        public object Set(object args)
        {
            NarrowGamutParams NarrowGamutData = args as NarrowGamutParams;
            bool status = false;
            GfxSDKClass GfxSDK = new GfxSDKClass();
            NarrowGamut = GfxSDK.Display.Color.NarrowGamut;
            uint windowsID = base.EnumeratedDisplays.Where(dI => dI.DisplayType == NarrowGamutData.DisplayType).Select(dI => dI.WindowsMonitorID).FirstOrDefault();
            NarrowGamut.Get(windowsID);

            if (NarrowGamut.Supported(windowsID))
            {
                NarrowGamut.ENABLE = (NarrowGamutData.narrowGamutOption == NarrowGamutOption.EnableNarrowGamut) ? true : false;
                NarrowGamut.Set(windowsID);
                if (NarrowGamut.Error == (uint)NARROW_GAMUT_ERROR_CODES.NARROW_GAMUT_SUCCESS)
                {
                    Log.Message("Narrowgamut set {0} was success", NarrowGamutData.narrowGamutOption.ToString());
                    status = true;
                }
                else
                {
                    Log.Message("Unable to set Narrowgamut for {0}", NarrowGamutData.DisplayType);
                    status = false;
                }
            }
            else
            {
                Log.Message(String.Format("NarrowGamut feature not supported for {0}", NarrowGamutData.DisplayType));
                status = false;
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


        public object GetAll(object args)
        {
            Log.Fail("Method not implemented");
            throw new NotImplementedException();
        }

        public object Get(object args)
        {
            Log.Fail("Method not implemented");
            throw new NotImplementedException();
        }
    }
}
