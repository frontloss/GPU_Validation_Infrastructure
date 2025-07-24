namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using igfxSDKLib;
    using System.Threading;

    /*  Get Set YcbCr through CUI SDK 8.0 */
    class YCbCr_v2 : FunctionalBase, ISDK
    {
        private IYCbCr YcbCr;
        public object Get(object args)
        {
            XvYccYcbXr XvYccYcbXrObj = args as XvYccYcbXr;
            GfxSDKClass GfxSDK = new GfxSDKClass();
            YcbCr = GfxSDK.Display.Color.YCbCr;
            uint windowsID = base.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(XvYccYcbXrObj.displayType)).WindowsMonitorID;
            YcbCr.Get(windowsID);
            if (YcbCr.Error == (uint)YCBCR_ERROR_CODES.YCBCR_SUCCESS)
            {
                Log.Message("Successfully get YcBcr info through SDK");
                XvYccYcbXrObj.isEnabled = Convert.ToInt32(YcbCr.ENABLE);
            }
            else
            {
                Log.Fail("Fail to get YcBcr info through SDK - Error Code: {0}", YcbCr.Error);
            }
            return XvYccYcbXrObj;
        }

        public object Set(object args)
        {
            bool status = false;
            XvYccYcbXr XvYccYcbXrObj = args as XvYccYcbXr;
            GfxSDKClass GfxSDK = new GfxSDKClass();
            YcbCr = GfxSDK.Display.Color.YCbCr;
            uint windowsID = base.EnumeratedDisplays.Find(dT => dT.DisplayType == XvYccYcbXrObj.displayType).WindowsMonitorID;
            YcbCr.Get(windowsID);
            if (YcbCr.Error == (uint)YCBCR_ERROR_CODES.YCBCR_SUCCESS)
            {
                if (YcbCr.get_Supported(windowsID))
                {
                    YcbCr.ENABLE = Convert.ToBoolean(XvYccYcbXrObj.isEnabled);
                    YcbCr.Set(windowsID);
                    if (YcbCr.Error == (uint)YCBCR_ERROR_CODES.YCBCR_SUCCESS)
                    {
                        Thread.Sleep(3000);
                        Log.Message("Successfully enable YcbCr on display {0}", XvYccYcbXrObj.displayType);
                        status = true;
                    }
                    else
                    {
                        Log.Fail("Fail to enable YcbCr on display {0} Error Code: {1}", XvYccYcbXrObj.displayType, YcbCr.Error);
                    }
                }
                else
                {
                    Log.Message("YcbCr doesn’t support on display {0}", XvYccYcbXrObj.displayType);
                }
            }
            else
            {
                Log.Fail("Fail to get YcBcr info for display {0} through SDK - Error Code: {1}", XvYccYcbXrObj.displayType, YcbCr.Error);
            }
            return status;
        }

        public object GetAll(object args)
        {
            Log.Fail("Method not implemented");
            throw new NotImplementedException();
        }
    }
}
