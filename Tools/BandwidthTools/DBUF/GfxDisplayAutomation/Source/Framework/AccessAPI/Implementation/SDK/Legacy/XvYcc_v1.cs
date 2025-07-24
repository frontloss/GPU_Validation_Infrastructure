namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using IgfxExtBridge_DotNet;
    using System.Threading;

    /*  Get Set XvYcc through CUI SDK 7.0 */
    class XvYcc_v1 : FunctionalBase, ISDK
    {
        private IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.IGFX_SUCCESS;
        private string errorDesc = @"";

        public object Get(object args)
        {
            XvYccYcbXr XvYccYcbXrObj = args as XvYccYcbXr;
            IGFX_XVYCC_INFO xvyccStru = new IGFX_XVYCC_INFO();
            DisplayInfo displayInfo = new DisplayInfo();
            xvyccStru.dwDeviceID = base.EnumeratedDisplays.Find(dI => dI.DisplayType == XvYccYcbXrObj.displayType).CUIMonitorID;
            SdkExtensions.LDisplayUtil.GetXvYcc(ref xvyccStru, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                Log.Message("Successfully get XvYcc info for display {0} through SDK", XvYccYcbXrObj.displayType);
                XvYccYcbXrObj.isEnabled = xvyccStru.bEnableXvYCC;
            }
            else
                Log.Fail("Fail to get YcBcr info through SDK - Error Code: {0}  ErrorDec: {1}", igfxErrorCode, errorDesc);
            return XvYccYcbXrObj;
        }

        public object Set(object args)
        {
            bool status = false;
            XvYccYcbXr XvYccYcbXrObj = args as XvYccYcbXr;
            IGFX_XVYCC_INFO xvyccStru = new IGFX_XVYCC_INFO();
            xvyccStru.dwDeviceID = base.EnumeratedDisplays.Find(dI => dI.DisplayType == XvYccYcbXrObj.displayType).CUIMonitorID;
            SdkExtensions.LDisplayUtil.GetXvYcc(ref xvyccStru, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                if (xvyccStru.bIsXvYCCSupported == 1)
                {
                    xvyccStru.bEnableXvYCC = XvYccYcbXrObj.isEnabled;
                    SdkExtensions.LDisplayUtil.SetXvYcc(ref xvyccStru, out igfxErrorCode, out errorDesc);
                    if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
                    {
                        Thread.Sleep(3000);
                        Log.Message("Successfully enable XvYcc on display {0}", XvYccYcbXrObj.displayType);
                        status = true;
                    }
                    else
                    {
                        Log.Fail("Fail to enable XvYcc on display {0} Error Code: {1} Error Desc: {2}", XvYccYcbXrObj.displayType, igfxErrorCode, errorDesc);
                    }
                }
                else
                {
                    Log.Message("XvYcc doesn’t support on display {0}", XvYccYcbXrObj.displayType);
                }
            }
            else
            {
                Log.Fail("Fail to get XvYcc info for display {0} through SDK - Error Code: {1}  ErrorDec: {2}", XvYccYcbXrObj.displayType, igfxErrorCode, errorDesc);
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
