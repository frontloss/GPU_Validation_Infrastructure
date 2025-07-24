using System.Collections.Generic;
using System.Linq;
using System.Diagnostics;
using System.IO;
using System;
using System.Windows.Forms;
using System.Drawing;

namespace Intel.VPG.Display.Automation
{
    class SB_Scaling_CaptureCRC_DFT:SetUpDisplay
    {

        [Test(Type = TestType.Method, Order = 0)]
        public void TestStep0()
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("{0} Applied successfully", base.CurrentConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", base.CurrentConfig.GetCurrentConfigStr());


            List<DisplayModeList> listDisplayMode = new List<DisplayModeList>();
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);

            allModeList.ForEach(DisplayModeList =>
            {
                uint sourceID = (uint)base.CurrentConfig.CustomDisplayList.IndexOf(DisplayModeList.display);
               
                if (base.CurrentConfig.ConfigType == DisplayConfigType.SD || ((base.CurrentConfig.ConfigType == DisplayConfigType.DDC||base.CurrentConfig.ConfigType==DisplayConfigType.ED)&& sourceID==1)
                    ||((base.CurrentConfig.ConfigType == DisplayConfigType.TDC||base.CurrentConfig.ConfigType==DisplayConfigType.TED)&& sourceID==2))
                {
                    if (DisplayExtensions.GetUnifiedConfig(base.CurrentConfig.ConfigType) == DisplayUnifiedConfig.Clone)
                        sourceID = 0;

                    DisplayInfo dispInfo = base.EnumeratedDisplays.Where(d => d.DisplayType == DisplayModeList.display).First();

                    foreach (DisplayMode curMode in DisplayModeList.supportedModes)
                    {
                        if (curMode.InterlacedFlag == 1)
                        {
                            Log.Success("Skipping Interlaced Resolution: {0}", curMode.GetCurrentModeStr(false));
                            continue;
                        }
                        Log.Message(true, "Current Resolution: {0}", curMode.GetCurrentModeStr(false));
                        ApplyModeOS(curMode, curMode.display);
                        Log.Message("Capturing CRC");


                        if (sourceID == 0 || DisplayExtensions.GetUnifiedConfig(base.CurrentConfig.ConfigType) == DisplayUnifiedConfig.Clone)
                            EnableDisableCursor(false);

                        
                        Start(curMode.HzRes, curMode.VtRes, sourceID, ULT_PIXELFORMAT.SB_B8G8R8A8, ULT_TILE_FORMATS.ULT_TILE_FORMAT_X);

                        CRCComputation(DisplayModeList.display, dispInfo.Port, dispInfo, curMode);
                       
                        End();
                        if (sourceID == 0 || DisplayExtensions.GetUnifiedConfig(base.CurrentConfig.ConfigType) == DisplayUnifiedConfig.Clone)
                            EnableDisableCursor(true);
                    }
                }
            });
        }
        private void EnableDisableCursor(bool enable)
        {
            SetUpDesktopArgs driverParams = new SetUpDesktopArgs(SetUpDesktopArgs.SetUpDesktopOperation.ShowCursor);
            if (enable == false)
                driverParams.FunctionName = SetUpDesktopArgs.SetUpDesktopOperation.HideCursor;

            if (!AccessInterface.SetFeature<bool, SetUpDesktopArgs>(Features.SetUpDesktop, Action.SetMethod, driverParams))
                Log.Abort("Failed to {0} Cursor", enable?"enable":"disable");

            //DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
            //driverData.input = 0x70080;
            //driverData.output = 0;
            
            //if(enable==true)
            //driverData.output=0x4000027;
            
            //DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.GTARegisterWrite, driverData);
            //if (!AccessInterface.SetFeature<bool, DriverEscapeParams>(Features.DriverEscape, Action.SetMethod, driverParams))
            //    Log.Abort("Failed to write Register with offset as {0}", driverData.input);
                
        }
        protected virtual void CRCComputation(DisplayType display, PORT port, DisplayInfo dispInfo, DisplayMode curMode)
        {

            string stPlatform = base.MachineInfo.PlatformDetails.Platform.ToString();

            CrcGoldenDataWrapper wrapper = new CrcGoldenDataWrapper(stPlatform, dispInfo, base.MachineInfo.OS.Type);
            
            uint crc = 0;
            if (GetCRC(display, port, ref crc) == true)
            {
                if (crc == 0)
                    Log.Fail("CRC Value Should not be 0: {0}", curMode.GetCurrentModeStr(false));
                else
                {
                    ModeCRC modeCRC = ConvertToCRCMode(curMode, crc);
                    wrapper.AddToXML(modeCRC, dispInfo);
                }
            }
            else
            {
                Log.Fail("CRC Value Not Consistent: {0}", curMode.GetCurrentModeStr(false));
            }
        }

        private bool GetCRC(DisplayType display, PORT port,ref uint tempCRC)
        {
            int attempt = 1;
            int matchCount = 0;
            tempCRC = 0;
            bool status = true;

            while (attempt <= 5)
            {
                CRCArgs obj = new CRCArgs();
                obj.displayType = display;
                obj.port = port;
                obj = AccessInterface.GetFeature<CRCArgs, CRCArgs>(Features.CRC, Action.GetMethod, Source.AccessAPI, obj);

                if (tempCRC==obj.CRCValue)
                {
                    matchCount++;
                }
                else
                {
                    matchCount = 0;
                }
                tempCRC = obj.CRCValue;
                attempt++;

                if (matchCount == 2)
                {
                    Log.Message("CRC Value Consistent.");
                    break;
                }
            }
            if (matchCount != 2)
            {
                status = false;
                Log.Verbose("CRC Value Not Consistent across captures.");
            }
            return status;
        }

        private ModeCRC ConvertToCRCMode(DisplayMode displayMode, uint crc)
        {
            ModeCRC modeCRC = new ModeCRC();

            modeCRC.resolution = displayMode.HzRes + "x" + displayMode.VtRes;
            modeCRC.refreshRate = displayMode.RR;
            modeCRC.IsInterlaced = displayMode.InterlacedFlag;
            modeCRC.colorDepth = displayMode.Bpp;
            modeCRC.scaling = ((ScalingOptions)displayMode.ScalingOptions.First()).ToString();
            modeCRC.customHorizontalScaling = 0;
            modeCRC.customVerticalScaling = 0;
            modeCRC.CRC = crc;
            
            return modeCRC;
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
        
    }
}
