namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using igfxSDKLib;

    /*  Get Set Quantization Range through SDK SDK 8.0 */
    class QuantizationRange_v2 : FunctionalBase, ISDK
    {
        private IHDMIFeatures sdkHDMI;
        public object Get(object args)
        {
            GfxSDKClass GfxSDK = new GfxSDKClass();
            QuantizationRangeParams quantizationParams = args as QuantizationRangeParams;
            sdkHDMI = GfxSDK.Display.HDMIFeatures;
            uint windowsID = base.EnumeratedDisplays.Where(dI => dI.DisplayType == quantizationParams.DisplayType).Select(dI => dI.CUIMonitorID).FirstOrDefault();
            sdkHDMI.Get(windowsID);
            if (sdkHDMI.Error == (uint)HDMI_ERROR_CODES.DISPLAY_HDMI_NOT_SUPPORTED)
            {
                Log.Message("QuantizationRange feature not supported for display {0}", quantizationParams.DisplayType);
                quantizationParams.QuantizationRange = RGB_QUANTIZATION_RANGE.Unsupported;
            }
            else if (sdkHDMI.Error == (uint)HDMI_ERROR_CODES.DISPLAY_HDMI_SUCCESS)
            {
                Log.Message("Successfully fetch QuantizationRange through SDK");
                quantizationParams.QuantizationRange = (RGB_QUANTIZATION_RANGE)sdkHDMI.QuantizationRange;
            }
            else
            {
                Log.Fail("Unable to fetch QuantizationRange through SDK - Error Code {0}", sdkHDMI.Error);
                quantizationParams.QuantizationRange = RGB_QUANTIZATION_RANGE.Unsupported;
            }
            return quantizationParams;
        }

        public object Set(object args)
        {
            bool status = false;
            GfxSDKClass GfxSDK = new GfxSDKClass();
            QuantizationRangeParams quantizationParams = args as QuantizationRangeParams;
            sdkHDMI = GfxSDK.Display.HDMIFeatures;
            uint windowsID = base.EnumeratedDisplays.Where(dI => dI.DisplayType == quantizationParams.DisplayType).Select(dI => dI.CUIMonitorID).FirstOrDefault();
            sdkHDMI.Get(windowsID);
            if (sdkHDMI.Error == (uint)HDMI_ERROR_CODES.DISPLAY_HDMI_NOT_SUPPORTED )
            {
                Log.Message("QuantizationRange feature not supported for display {0}", quantizationParams.DisplayType);
                quantizationParams.QuantizationRange = RGB_QUANTIZATION_RANGE.Unsupported;
            }
            else if (sdkHDMI.Error == (uint)HDMI_ERROR_CODES.DISPLAY_HDMI_SUCCESS)
            {
                sdkHDMI.QuantizationRange = (HDMI_QUANTIZATION_RANGE)quantizationParams.QuantizationRange;
                sdkHDMI.Set(windowsID);
                if (sdkHDMI.Error == (uint)HDMI_ERROR_CODES.DISPLAY_HDMI_SUCCESS)
                {
                    Log.Message("QuantizationRange set to {0} for {1}", quantizationParams.QuantizationRange, quantizationParams.DisplayType);
                    status = true;
                }
                else
                {
                    Log.Fail("Unable to set QuantizationRange for {0} through SDK - Error Code: {1}", quantizationParams.DisplayType, sdkHDMI.Error);
                    quantizationParams.QuantizationRange = RGB_QUANTIZATION_RANGE.Unsupported;
                }
            }
            else
            {
                Log.Fail("Unable to fetch QuantizationRange through SDK - Error Code {0}", sdkHDMI.Error);
                quantizationParams.QuantizationRange = RGB_QUANTIZATION_RANGE.Unsupported;
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
