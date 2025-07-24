namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System;
    using System.IO;

    class SB_RGBQuantization_Base : TestBase
    {
        public int ImgCounter = 0;
        public enum ImageColors
        {
            White,
            Black
        }
        protected void ApplyResolution(DisplayType display, bool ceaMode)
        {
            DisplayMode displayMode = new DisplayMode();
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.CustomDisplayList);

            DisplayModeList currentModeList = allModeList.Where(item => item.display == display).First();
            if(ceaMode)
            displayMode = currentModeList.supportedModes.Where(item => (item.VtRes == 1080 && item.ScalingOptions.Contains((uint)ScalingOptions.Maintain_Display_Scaling))).Last();
            else
             displayMode = currentModeList.supportedModes.Where(item => (item.VtRes == 1024 && item.ScalingOptions.Contains((uint)ScalingOptions.Maintain_Display_Scaling))).First();


            if (displayMode.HzRes == 0 || displayMode.VtRes == 0)
                Log.Fail("Mode not available for {0}",ceaMode?"CEA mode":"PC Mode");

            ApplyModeOS(displayMode, display);
     
        }
        private void ApplyModeOS(DisplayMode argSelectedMode, DisplayType argDisplayType)
        {
            Log.Message(true, "Set supported mode {0} for {1}", argSelectedMode.GetCurrentModeStr(false), argDisplayType);
            argSelectedMode.display = argDisplayType;
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argSelectedMode))
            {
                Log.Success("Mode applied Successfully");
            }
            else
                Log.Fail("Fail to apply Mode");
        }
        private void VerifyModeOS(DisplayMode argSelectedMode, DisplayType argDisplayType)
        {
            Log.Message(true, "Verify the  mode  for {0} through OS", argDisplayType);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplayType).First();
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            if (actualMode.GetCurrentModeStr(true).Equals(argSelectedMode.GetCurrentModeStr(true)))
            {
                Log.Success("Mode {0} is verified for {1}", actualMode.GetCurrentModeStr(false), argDisplayType);
            }
            else
                Log.Fail("Mode chosen {0} is not applied for {1}! Actual is {2}", argSelectedMode.GetCurrentModeStr(false), argDisplayType, actualMode.GetCurrentModeStr(false));
        }
        protected void Hotplug(FunctionName FuncArg, DisplayType DisTypeArg, DVMU_PORT PortArg)
        {
            HotPlugUnplug _HotPlugUnplug = null;
            _HotPlugUnplug = new HotPlugUnplug(FuncArg, DisTypeArg, PortArg);
            bool status = AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, _HotPlugUnplug);
        }
        protected void Hotplug(FunctionName FuncArg, DisplayType DisTypeArg, DVMU_PORT PortArg, string edidFile)
        {
            HotPlugUnplug _HotPlugUnplug = null;
            _HotPlugUnplug = new HotPlugUnplug(FuncArg, PortArg, edidFile);
            bool status = AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, _HotPlugUnplug);
        }
        protected void PrepareBackground(bool bInitialize, ImageColors imageColor)
        {
            if (bInitialize)
            {
                string imagePath = imageColor.ToString() + ".jpg";
                SetUpDesktopArgs desktopArgs = new SetUpDesktopArgs(SetUpDesktopArgs.SetUpDesktopOperation.PrepareDesktop, imagePath);
                bool status = AccessInterface.SetFeature<bool, SetUpDesktopArgs>(Features.SetUpDesktop, Action.SetMethod, desktopArgs);    
            }
            else
            {
                SetUpDesktopArgs desktopArgs = new SetUpDesktopArgs(SetUpDesktopArgs.SetUpDesktopOperation.RestoreDesktop);
                bool status = AccessInterface.SetFeature<bool, SetUpDesktopArgs>(Features.SetUpDesktop, Action.SetMethod, desktopArgs);
            }
        }

        protected bool VerifyColorValue(ImageColors imageColor, RGB_QUANTIZATION_RANGE quantizationRange, bool IsCEAmode)
        {
            bool status = false;
            string fileName = "Image" + ImgCounter++;

            HotPlugUnplug obj = new HotPlugUnplug();
            obj.FunctionName = FunctionName.CaptureFrame;
            obj.FrameFileName = fileName;
            AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, obj);

            status = IsColorFormatAccurate(300, 300, fileName + ".bmp", imageColor, quantizationRange, IsCEAmode);

            return status;
        }

        private bool IsColorFormatAccurate(int x, int y, string filename, ImageColors imageColor, RGB_QUANTIZATION_RANGE quantizationRange, bool IsCEAmode)
        {
            bool status = true;
            PixelColorInfo expectedColor = GetDefaultColorValue(imageColor, quantizationRange, IsCEAmode);
            ImageProcessingParams imageParams = new ImageProcessingParams();
            imageParams.ImageProcessingOption = ImageProcessOptions.GetPixelInfo;
            imageParams.SourceImage = filename;

            pointApi currentPoint = new pointApi();
            currentPoint.x = x;
            currentPoint.y = y;
            imageParams.pixelPosition = currentPoint;

            AccessInterface.GetFeature<ImageProcessingParams, ImageProcessingParams>(Features.ImageProcessing, Action.GetMethod,Source.AccessAPI, imageParams);

            if (expectedColor.Red != imageParams.pixelColorInfo.Red || expectedColor.Green != imageParams.pixelColorInfo.Green || expectedColor.Blue != imageParams.pixelColorInfo.Blue)
                status = false;

            return status;
        }

        private PixelColorInfo GetDefaultColorValue(ImageColors imageColor, RGB_QUANTIZATION_RANGE quantizationRange, bool IsCEAmode)
        {
            PixelColorInfo pixelInfo = new PixelColorInfo();
            bool isFullRange = quantizationRange == RGB_QUANTIZATION_RANGE.FULL ? true : false;

            if (quantizationRange == RGB_QUANTIZATION_RANGE.DEFAULT)
            {
                isFullRange = IsCEAmode ? false : true;
            }
            if (imageColor == ImageColors.Black)
            {
                pixelInfo.Red = pixelInfo.Green = pixelInfo.Blue = pixelInfo.Alpha = isFullRange ? 0 : 16;
            }
            else if (quantizationRange == RGB_QUANTIZATION_RANGE.LIMITED)
            {
                pixelInfo.Red = pixelInfo.Green = pixelInfo.Blue = pixelInfo.Alpha = isFullRange ? 235 : 255;
            }

            return pixelInfo;
        }

        protected bool SetQuantizationRange(DisplayType display, RGB_QUANTIZATION_RANGE quantizationRange)
        {
            bool status = false;
            QuantizationRangeParams quantizationParams = new QuantizationRangeParams();
            quantizationParams.DisplayType = display;
            quantizationParams.QuantizationRange = quantizationRange;
            status = AccessInterface.SetFeature<bool,QuantizationRangeParams>(Features.QuantizationRange, Action.SetMethod, quantizationParams);
            
            return status;
        }

        protected RGB_QUANTIZATION_RANGE GetQuantizationRange(DisplayType display)
        {
            QuantizationRangeParams quantizationParams = new QuantizationRangeParams();
            quantizationParams.DisplayType = display;
            AccessInterface.GetFeature<QuantizationRangeParams, QuantizationRangeParams>(Features.QuantizationRange, Action.GetMethod,Source.AccessAPI, quantizationParams);


            DisplayInfo pDisplay = base.EnumeratedDisplays.Where(item => item.DisplayType == display).First();
            // check DEEP COLOR Enable for DVMU
            if (pDisplay.DvmuPort != DVMU_PORT.None)
            {
                InfoFrame _infoFrame = new InfoFrame();
                _infoFrame.infoFrameType = InfoFrameType.AVI;
                _infoFrame.functionInfoFrame = FunctionInfoFrame.ComputeRGBQuantizationRange;
                _infoFrame.port = pDisplay.DvmuPort;

                InfoFrame deepColorInfoframe = AccessInterface.GetFeature<InfoFrame, InfoFrame>(Features.InfoFrameParsing, Action.GetMethod, Source.AccessAPI, _infoFrame);
                RGB_QUANTIZATION_RANGE rgbQuantDVMU = (RGB_QUANTIZATION_RANGE)Enum.Parse(typeof(RGB_QUANTIZATION_RANGE), deepColorInfoframe.infoFrameData.First());

                if (quantizationParams.QuantizationRange == rgbQuantDVMU)
                {
                    Log.Message("DVMU Quantization range matched with applied value. {0}", rgbQuantDVMU);
                }
                else
                {
                    Log.Message("DVMU QuantizationRange:{0} not matched with driver:{1}", rgbQuantDVMU, quantizationParams.QuantizationRange);
                }
               
            }

            return quantizationParams.QuantizationRange;


        }
    }
}