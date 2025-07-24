namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using IgfxExtBridge_DotNet;
    using System.Threading;

    /*  Get Set YcbCr through CUI SDK 7.0 */
    class YCbCr_v1 : FunctionalBase, ISDK
    {
        private IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.IGFX_SUCCESS;
        private string errorDesc = @"";

        public object Get(object args)
        {
            XvYccYcbXr XvYccYcbXrObj = args as XvYccYcbXr;
            IGFX_YCBCR_INFO xvyccStru = new IGFX_YCBCR_INFO();
            DisplayInfo displayInfo = new DisplayInfo();
            xvyccStru.dwDeviceID = base.EnumeratedDisplays.Find(dI => dI.DisplayType == XvYccYcbXrObj.displayType).CUIMonitorID;
            SdkExtensions.LDisplayUtil.GetYcBcr(ref xvyccStru, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                Log.Message("Successfully get YcBcr info for display {0} through SDK", XvYccYcbXrObj.displayType);
                XvYccYcbXrObj.isEnabled = xvyccStru.bEnableYCbCr;
            }
            else
            {
                Log.Fail("Fail to get YcBcr info for display {0} through SDK - Error Code: {1}  ErrorDec: {2}", XvYccYcbXrObj.displayType, igfxErrorCode, errorDesc);
            }
            return XvYccYcbXrObj;
        }

        public object Set(object args)
        {
            bool status = false;
            XvYccYcbXr XvYccYcbXrObj = args as XvYccYcbXr;
            IGFX_YCBCR_INFO xvyccStru = new IGFX_YCBCR_INFO();
            xvyccStru.dwDeviceID = base.EnumeratedDisplays.Find(dI => dI.DisplayType == XvYccYcbXrObj.displayType).CUIMonitorID;
            SdkExtensions.LDisplayUtil.GetYcBcr(ref xvyccStru, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                if (xvyccStru.bIsYCbCrSupported == 1)
                {
                    xvyccStru.bEnableYCbCr = XvYccYcbXrObj.isEnabled;
                    SdkExtensions.LDisplayUtil.SetYcBcr(ref xvyccStru, out igfxErrorCode, out errorDesc);
                    if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
                    {
                        Thread.Sleep(3000);
                        Log.Message("Successfully enable YcbCr on display {0}", XvYccYcbXrObj.displayType);
                        status = true;
                    }
                    else
                    {
                        Log.Fail("Fail to enable YcbCr on display {0} Error Code: {1} Error Desc: {2}", XvYccYcbXrObj.displayType, igfxErrorCode, errorDesc);
                    }
                }
                else
                {
                    Log.Message("YcbCr doesn’t support on display {0}", XvYccYcbXrObj.displayType);
                }
            }
            else
            {
                Log.Fail("Fail to get YcBcr info for display {0} through SDK - Error Code: {1}  ErrorDec: {2}", XvYccYcbXrObj.displayType, igfxErrorCode, errorDesc);
            }
            return status;
        }

        public object GetAll(object args)
        {
            Log.Fail("Method not implemented");
            throw new System.NotImplementedException();
        }
    }
}
