using System.Collections.Generic;
using System.Linq;
using System.Diagnostics;
using System.IO;
using System;
using System.Windows.Forms;
using System.Drawing;

namespace Intel.VPG.Display.Automation
{
    class SB_Scaling_CaptureFrame:TestBase
    {

        [Test(Type = TestType.Method, Order = 0)]
        public void TestStep0()
        {

            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("{0} Applied successfully", base.CurrentConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", base.CurrentConfig.GetCurrentConfigStr());

            //Array.ForEach(Directory.GetFiles(Path.Combine(Directory.GetCurrentDirectory(), "Images")), File.Delete);

            List<DisplayModeList> listDisplayMode = new List<DisplayModeList>();
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);
            
            SetUpDesktopArgs desktopArgs = new SetUpDesktopArgs(SetUpDesktopArgs.SetUpDesktopOperation.PrepareDesktop);
            bool stat = AccessInterface.SetFeature<bool, SetUpDesktopArgs>(Features.SetUpDesktop, Action.SetMethod, desktopArgs);

            allModeList.ForEach(DisplayModeList => {
                if (DisplayModeList.display == DisplayType.HDMI)
                {
                    //DisplayModeList.supportedModes.ForEach(curMode=>{

                    foreach (DisplayMode curMode in DisplayModeList.supportedModes)
                    {
                        Log.Message(true, "DVMU4 {0}", curMode.GetCurrentModeStr(false));
                        string fileName = GetDisplayModeToString(curMode);
                        ApplyModeOS(curMode, curMode.display);
                        Log.Message("Capturing Frame");

                       //hides taskbar          
                        desktopArgs.FunctionName = SetUpDesktopArgs.SetUpDesktopOperation.HideTaskBar;
                        stat = AccessInterface.SetFeature<bool, SetUpDesktopArgs>(Features.SetUpDesktop, Action.SetMethod, desktopArgs);

                        HotPlugUnplug obj = new HotPlugUnplug();
                        obj.FunctionName = FunctionName.CaptureFrame;
                        obj.FrameFileName = fileName;
                        bool status = AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, obj);

                        ImageProcessingParams imageParams = new ImageProcessingParams();
                        imageParams.ImageProcessingOption = ImageProcessOptions.CompareImages;
                        imageParams.SourceImage = Directory.GetCurrentDirectory() + "\\Images\\" + fileName + ".bmp";
                        imageParams.TargetImage = fileName+".bmp";

                        status = AccessInterface.SetFeature<bool, ImageProcessingParams>(Features.ImageProcessing, Action.SetMethod, imageParams);
                        Log.Message("Image Capture Done");                 
                    }
                }
            });

            desktopArgs.FunctionName = SetUpDesktopArgs.SetUpDesktopOperation.RestoreDesktop;
            stat = AccessInterface.SetFeature<bool, SetUpDesktopArgs>(Features.SetUpDesktop, Action.SetMethod, desktopArgs);

        }
        
        protected void ApplyModeOS(DisplayMode argSelectedMode, DisplayType argDisplayType)
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
        protected string GetDisplayModeToString(DisplayMode argDispMode)
        {
            string modeStr = string.Concat(argDispMode.display,"_",argDispMode.HzRes,"_",argDispMode.VtRes, "_", argDispMode.RR, argDispMode.InterlacedFlag.Equals(0) ? "p_Hz" : "i_Hz", "_", argDispMode.Bpp, "_Bit", "_", argDispMode.Angle, "_Deg");
            if (null != argDispMode.ScalingOptions && !argDispMode.ScalingOptions.Count.Equals(0))
                modeStr = string.Concat(modeStr, "_", (ScalingOptions)argDispMode.ScalingOptions.First());
            return modeStr;
        }

    }
}
