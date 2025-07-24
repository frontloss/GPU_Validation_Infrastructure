namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;

    internal class Scaling : Modes, IParse, ISetMethod, IGetMethod, IGetAllMethod
    {
        [ParseAttribute(InterfaceName = InterfaceType.ISetMethod, InterfaceData = new string[] { "DisplayType:DisplayType:sp", "ScalingOptions:Scaling" }, Comment = "Sets the scaling option for a display")]
        [ParseAttribute(InterfaceName = InterfaceType.IGetMethod, InterfaceData = new string[] { "DisplayType:DisplayType" }, Comment = "Gets the scaling option of a display")]
        public new void Parse(string[] args)
        {
            if (args[0].ToLower().Contains("get"))
            {
                #region GET CALL
                DisplayType displayType = base.EnumeratedDisplays.Select(dI => dI.DisplayType).First();
                if (args.Length.Equals(2) && !string.IsNullOrEmpty(args[1]))
                    Enum.TryParse(args[1], true, out displayType);

                GetCurrentScaling(displayType);
                #endregion
            }
            if (args[0].ToLower().Contains("set"))
            {
                #region SET CALL
                args = args.Skip(1).ToArray();
                DisplayType display = (DisplayType)Enum.Parse(typeof(DisplayType), args[0], true);
                ScalingOptions scaleOpt = ScalingOptions.None;
                switch (args[1].ToUpper())
                {
                    case "MDS":
                    case "MAINTAIN_DISPLAY_SCALING":
                        scaleOpt = ScalingOptions.Maintain_Display_Scaling;
                        break;
                    case "FULL":
                    case "SCALE_FULL_SCREEN":
                        scaleOpt = ScalingOptions.Scale_Full_Screen;
                        break;
                    case "CENTER":
                    case "CENTER_IMAGE":
                        scaleOpt = ScalingOptions.Center_Image;
                        break;
                    case "MAR":
                    case "MAINTAIN_ASPECT_RATIO":
                        scaleOpt = ScalingOptions.Maintain_Aspect_Ratio;
                        break;
                    case "CAR":
                    case "Customize_Aspect_Ratio":
                        scaleOpt = ScalingOptions.Customize_Aspect_Ratio;
                        break;
                    default:
                        Log.Abort("Invalid Scaling Option");
                        break;
                }

                DisplayScaling ds = new DisplayScaling(display, scaleOpt);

                if (ds.scaling == ScalingOptions.Customize_Aspect_Ratio)
                {
                    if(args.Length != 4)
                        Log.Abort("Invalid Scaling Option");

                    ds.customX = Convert.ToUInt32(args[2]);
                    ds.customY = Convert.ToUInt32(args[3]);
                    ds.display = display;
                }                

                SetScaling(ds);
                #endregion
            }
        }

        public new object GetMethod(object argMessage)
        {
            DisplayType displayType = (DisplayType)argMessage;
            return GetCurrentScaling(displayType);
        }

        public new bool SetMethod(object argMessage)
        {
            DisplayScaling dispScaling = (DisplayScaling)argMessage;
            return SetScaling(dispScaling);
        }

        public new object GetAllMethod(object argMessage)
        {
            DisplayType displayType = (DisplayType)argMessage;
            DisplayMode currentMode = base.GetCurrentMode(displayType, base.EnumeratedDisplays.Where(dI => dI.DisplayType == displayType).Select(dI => dI.WindowsMonitorID).FirstOrDefault());

            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkScaling = sdkExtn.GetSDKHandle(SDKServices.Scaling);
            List<uint> scalings = (List<uint>)sdkScaling.GetAll(currentMode);
            List<ScalingOptions> scalingOptions = new List<ScalingOptions>();
            scalings.ForEach(sc =>
            {
                scalingOptions.Add((ScalingOptions)sc);
            });

            return scalingOptions;
        }

        private bool SetScaling(DisplayScaling pDispScl)
        {
            bool status = false;
            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkScaling = sdkExtn.GetSDKHandle(SDKServices.Scaling);
            if ((bool)sdkScaling.Set(pDispScl))
            {
                Log.Success("{0} successfully applied to {1}", pDispScl.ToString(), pDispScl.display);
                status = true;
            }
            else
                Log.Fail("Fail to apply {0} to {1}", pDispScl.scaling, pDispScl.display);
            return status;
        }

        private DisplayScaling GetCurrentScaling(DisplayType pDisplayType)
        {
            DisplayMode currentMode = base.GetCurrentMode(pDisplayType, base.EnumeratedDisplays.Where(dI => dI.DisplayType == pDisplayType).Select(dI => dI.WindowsMonitorID).FirstOrDefault());

            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkScaling = sdkExtn.GetSDKHandle(SDKServices.Scaling);
            DisplayScaling scalingOptions = (DisplayScaling)sdkScaling.Get(currentMode);
            Log.Message("Current Resolution on Display {0} HRes - {1}, VRes - {2}, bpp - {3}, RR - {4}{5} Angle: {6} Scaling: {7}",
                currentMode.display, currentMode.HzRes, currentMode.VtRes, currentMode.Bpp, currentMode.RR, (Convert.ToBoolean(currentMode.InterlacedFlag) ? "i" : "p"), currentMode.Angle, scalingOptions.scaling.ToString());
            return scalingOptions;
        }

    }
}