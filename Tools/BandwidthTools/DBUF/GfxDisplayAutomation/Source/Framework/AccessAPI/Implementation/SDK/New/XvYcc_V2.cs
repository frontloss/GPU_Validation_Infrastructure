namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using igfxSDKLib;
    using System.Threading;

    /*  Get Set XvYcc through CUI SDK 8.0 */
    class XvYcc_v2 : FunctionalBase, ISDK
    {
        private IxvYCC XvYcc;
        public object Get(object args)
        {
            XvYccYcbXr XvYccYcbXrObj = args as XvYccYcbXr;
            GfxSDKClass GfxSDK = new GfxSDKClass();
            XvYcc = GfxSDK.Display.Color.xvYCC;
            uint windowsID = base.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(XvYccYcbXrObj.displayType)).WindowsMonitorID;
            XvYcc.Get(windowsID);
            if (XvYcc.Error == (uint)XVYCC_ERROR_CODES.XVYCC_SUCCESS)
            {
                Log.Message("Successfully get XvYcc info through SDK");
                XvYccYcbXrObj.isEnabled = Convert.ToInt32(XvYcc.ENABLE);
            }
            else
            {
                Log.Fail("Fail to get XvYcc info through SDK - Error Code: {0}", XvYcc.Error);
            }
            return XvYccYcbXrObj;
        }

        public object Set(object args)
        {
            bool status = false;
            XvYccYcbXr XvYccYcbXrObj = args as XvYccYcbXr;
            GfxSDKClass GfxSDK = new GfxSDKClass();
            XvYcc = GfxSDK.Display.Color.xvYCC;
            uint windowsID = base.EnumeratedDisplays.Find(dI => dI.DisplayType.Equals(XvYccYcbXrObj.displayType)).WindowsMonitorID;
            XvYcc.Get(windowsID);
            if (XvYcc.Error == (uint)XVYCC_ERROR_CODES.XVYCC_SUCCESS)
            {
                if (XvYcc.get_Supported(windowsID))
                {
                    XvYcc.ENABLE = Convert.ToBoolean(XvYccYcbXrObj.isEnabled);
                    XvYcc.Set(windowsID);
                    if (XvYcc.Error == (uint)XVYCC_ERROR_CODES.XVYCC_SUCCESS)
                    {
                        Thread.Sleep(3000);
                        Log.Message("Successfully enable XvYcc on display {0}", XvYccYcbXrObj.displayType);
                        status = true;
                    }
                    else
                    {
                        Log.Fail("Fail to enable XvYcc on display {0} Error Code: {1}", XvYccYcbXrObj.displayType, XvYcc.Error);
                    }
                }
                else
                {
                    Log.Message("XvYcc doesn’t support on display {0}", XvYccYcbXrObj.displayType);
                }
            }
            else
            {
                Log.Fail("Fail to get XvYcc info for display {0} through SDK - Error Code: {1}", XvYccYcbXrObj.displayType, XvYcc.Error);
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
