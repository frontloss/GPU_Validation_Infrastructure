namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    public class QuantizationRange : FunctionalBase, IGetMethod, IParse,ISetMethod
    {
        public bool SetMethod(object argMessage)
        {
            QuantizationRangeParams args = (QuantizationRangeParams)argMessage;
            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkQuantizationRange = sdkExtn.GetSDKHandle(SDKServices.QuantizationRange);
            return (bool)sdkQuantizationRange.Set(args);
        }

        public object GetMethod(object argMessage)
        {
            QuantizationRangeParams args = (QuantizationRangeParams)argMessage;
            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkQuantizationRange = sdkExtn.GetSDKHandle(SDKServices.QuantizationRange);
            return (QuantizationRangeParams)sdkQuantizationRange.Get(args);
        }

        public void Parse(string[] args)
        {
            QuantizationRangeParams quantizationParams = new QuantizationRangeParams();
            DisplayType tempDisplay;
            RGB_QUANTIZATION_RANGE tempLevel = RGB_QUANTIZATION_RANGE.Unsupported;

            if (args.Length == 3 && args[0].ToLower().Contains("set"))
            {
                if (Enum.TryParse<DisplayType>(args[1], true, out tempDisplay) && Enum.TryParse<RGB_QUANTIZATION_RANGE>(args[2], true, out tempLevel))
                {
                    quantizationParams.DisplayType = tempDisplay;
                    quantizationParams.QuantizationRange = tempLevel;
                    Log.Verbose("Setting QuantizationRange: {0} for display {1}", quantizationParams.QuantizationRange, quantizationParams.DisplayType);
                    SetMethod(quantizationParams);
                }
                else
                {
                    this.HelpText();
                }              
            }
            else if (args.Length == 2 && args[0].ToLower().Contains("get"))
            {
                if (Enum.TryParse<DisplayType>(args[1], true, out tempDisplay))
                {
                    quantizationParams.DisplayType = tempDisplay;
                    GetMethod(quantizationParams);
                    Log.Message("QuantizationRange for display {0} is {1}", quantizationParams.DisplayType, quantizationParams.QuantizationRange);
                }
                else
                {
                    this.HelpText();
                }
            }
            else
                this.HelpText();
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("..\\>Problem with Commandline Parameters. \n Please type : Execute.exe RGB_QUANTIZATION_RANGE set/get DisplayType <DEFAULT/LIMITED/FULL>").Append(Environment.NewLine);
            sb.Append("For example : Execute.exe RGB_QUANTIZATION_RANGE set HDMI LIMITED");
            sb.Append("For example : Execute.exe RGB_QUANTIZATION_RANGE get HDMI");
            sb.Append("For example : Execute.exe RGB_QUANTIZATION_RANGE set HDMI FULL");
            Log.Message(sb.ToString());
        }
    }
}