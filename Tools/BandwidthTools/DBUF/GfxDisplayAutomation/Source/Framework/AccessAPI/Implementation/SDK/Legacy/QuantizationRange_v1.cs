namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using IgfxExtBridge_DotNet;

    /*  Get Set Quantization Range through SDK SDK 7.0 */
    class QuantizationRange_v1 : FunctionalBase, ISDK
    {
        private IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.UNKNOWN_ERROR;
        private string errorDesc = "";

        public object Set(object args)
        {
            bool status = false;
            QuantizationRangeParams quantizationParams = args as QuantizationRangeParams;
            IGFX_AVI_INFOFRAME infoFrame = new IGFX_AVI_INFOFRAME();

            //.infoFrame.dwAspectRatio = 1;
            infoFrame.dwDeviceID = base.EnumeratedDisplays.Where(dI => dI.DisplayType == quantizationParams.DisplayType).Select(dI => dI.CUIMonitorID).FirstOrDefault();
            APIExtensions.DisplayUtil.GetAviInfoFrame(ref infoFrame, out igfxErrorCode, out errorDesc);

            if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_UNSUPPORTED_FEATURE)
            {
                Log.Message("QuantizationRange feature not supported for display {0}", quantizationParams.DisplayType);
                quantizationParams.QuantizationRange = RGB_QUANTIZATION_RANGE.Unsupported;
            }
            else if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                infoFrame.dwQuantRange = (uint)quantizationParams.QuantizationRange;
                APIExtensions.DisplayUtil.SetAviInfoFrame(ref infoFrame, out igfxErrorCode, out errorDesc);
                if (igfxErrorCode != IGFX_ERROR_CODES.IGFX_SUCCESS)
                {
                    Log.Fail("Unable to set QuantizationRange for {0} through SDK - Error Code: {1} Error Desc: {2}", quantizationParams.DisplayType, igfxErrorCode.ToString(), errorDesc);
                    quantizationParams.QuantizationRange = RGB_QUANTIZATION_RANGE.Unsupported;
                }
                else if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
                {
                    Log.Message("QuantizationRange set to {0} for {1}", quantizationParams.QuantizationRange, quantizationParams.DisplayType);
                    status = true;
                }
            }
            else
            {
                Log.Fail("Unable to fetch QuantizationRange through SDK - Error Code: {0} Error Desc: {1}", igfxErrorCode.ToString(), errorDesc);
                quantizationParams.QuantizationRange = RGB_QUANTIZATION_RANGE.Unsupported;
            }
            return status;
        }

        public object Get(object args)
        {
            QuantizationRangeParams quantizationParams = args as QuantizationRangeParams;
            IGFX_AVI_INFOFRAME infoFrame = new IGFX_AVI_INFOFRAME();
            infoFrame.dwDeviceID = base.EnumeratedDisplays.Where(dI => dI.DisplayType == quantizationParams.DisplayType).Select(dI => dI.CUIMonitorID).FirstOrDefault();
            APIExtensions.DisplayUtil.GetAviInfoFrame(ref infoFrame, out igfxErrorCode, out errorDesc);

            if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_UNSUPPORTED_FEATURE)
            {
                Log.Verbose("QuantizationRange feature not supported for display {0}", quantizationParams.DisplayType);
                quantizationParams.QuantizationRange = RGB_QUANTIZATION_RANGE.Unsupported;
            }
            else if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                Log.Message("Successfully fetch QuantizationRange through SDK");
                quantizationParams.QuantizationRange = (RGB_QUANTIZATION_RANGE)Enum.Parse(typeof(RGB_QUANTIZATION_RANGE), infoFrame.dwQuantRange.ToString());
            }
            else
            {
                Log.Fail("Unable to fetch QuantizationRange through SDK - Error Code: {0} Error Desc: {1} ", igfxErrorCode.ToString(), errorDesc);
                quantizationParams.QuantizationRange = RGB_QUANTIZATION_RANGE.Unsupported;
            }
            return quantizationParams;
        }

        public object GetAll(object args)
        {
            Log.Fail("Method not implemented");
            throw new NotImplementedException();
        }
    }
}
