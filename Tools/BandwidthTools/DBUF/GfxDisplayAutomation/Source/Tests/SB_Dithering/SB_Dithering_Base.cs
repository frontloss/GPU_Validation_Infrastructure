using System.Threading;
using System.IO;
using System.Diagnostics;
using System.Windows.Forms;
using System;
using System.Collections.Generic;
using System.Linq;
namespace Intel.VPG.Display.Automation
{
    class SB_Dithering_Base:TestBase
    {
        protected string _ditheringEnable = "DITHERING_ENABLE";
        protected string _ditheringDisable = "DITHERING_DISABLE";
        protected string _deepcolorEnable = "DEEPCOLOR_ENABLED";
        protected string _deepcolorDisable = "DEEPCOLOR_DISABLED";
        DeepColorParams _DPParam = new DeepColorParams(); 
        protected DisplayType _nonDithering = DisplayType.HDMI;
        protected Dictionary<DeepColorAppType, uint> _appBPCValue = new Dictionary<DeepColorAppType, uint>() { { DeepColorAppType.N10BitScanOut, 10 }, { DeepColorAppType.FP16, 16 }, { DeepColorAppType.None, 8 } };
        protected void InstallDirectX()
        {
            if (Directory.Exists(@"C:\Program Files (x86)\Microsoft DirectX SDK (June 2010)") || (Directory.Exists(@"C:\Program Files\Microsoft DirectX SDK (June 2010)")))
            {
                Log.Message("DirectX is installed");
            }
            //}
            else
            {
                Log.Message("Installing DirectX SDK. Do not touch any UI buttons.");
                Process p = Process.Start(base.ApplicationManager.ApplicationSettings.DirectX, "/U");
                p.WaitForExit();
                Log.Message("Installion of  DirectX SDK was successfull");
            }
        }

        protected void EnableFP16()
        {
            DisplayConfig dispConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);

            //Enabling Deep color Feature
            Log.Message(true, "Enabling Feature : FP16");
            _DPParam = new DeepColorParams();
            _DPParam.DeepColorAppType = DeepColorAppType.FP16;
            _DPParam.CurrentConfig = dispConfig;
            _DPParam.DeepColorOptions = DeepColorOptions.Enable;
            AccessInterface.SetFeature<DeepColorParams>(Features.DeepColor, Action.Set, _DPParam);

            Log.Success("Enabled  Feature : FP16");

            //waiting for 15 Sec
            Thread.Sleep((15) * 1000);
        }
        protected void MoveFP16(DisplayHierarchy pDispHierarchy)
        {
            //Moving Deep color Instant
            Log.Message("Moving  Feature to {0}", pDispHierarchy);
            _DPParam.DeepColorOptions = DeepColorOptions.Move;
            _DPParam.DisplayHierarchy = pDispHierarchy;
            AccessInterface.SetFeature<DeepColorParams>(Features.DeepColor, Action.Set, _DPParam);

            Log.Success("Moved Feature to {0}", pDispHierarchy);
        }
        protected void DisableFP16()
        {
            Log.Message(true, "Disabling  Feature : FP16");
            _DPParam.DeepColorOptions = DeepColorOptions.Disable;
            AccessInterface.SetFeature<DeepColorParams>(Features.DeepColor, Action.Set, _DPParam);

            Log.Message("Disabled Deepcolor Feature : FP16");
            //waiting for 15 Sec
            Thread.Sleep((15) * 1000);
        }
        protected void Enable10BitScanner(uint argBPC=10)
        {
            Log.Message(true, "Enabling  Feature : 10 Bit Scanner with {0} BPC",argBPC);

            DisplayConfig dispConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            _DPParam = new DeepColorParams();
            _DPParam.CurrentConfig = dispConfig;
            _DPParam.DeepColorAppType = DeepColorAppType.N10BitScanOut;
            _DPParam.DeepColorOptions = DeepColorOptions.Enable;
            _DPParam.Bpc = argBPC;
            AccessInterface.SetFeature<DeepColorParams>(Features.DeepColor, Action.Set, _DPParam);

            //waiting for 15 Sec
            Thread.Sleep((15) * 1000);
            Log.Success("Enabled  Feature : 10 Bit Scanner");
            for (int i = 0; i < 11; i++)
            {
                Thread.Sleep(1000);
                SendKeys.SendWait(" ");
            }
            Thread.Sleep(10000);
        }
        protected void ApplyConfigOS(DisplayConfig argDispConfig)
        {
            Log.Message(true,"Applying config {0}",argDispConfig.GetCurrentConfigStr());
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());
        }
        protected bool VerifyRegisters(string pRegisterEvent, PIPE pPipe, PLANE pPlane, PORT pPort, bool compare = true)
        {
            Log.Message("Verifying Register for event : {0}", pRegisterEvent);
            bool regValueMatched = true;

            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = pPipe;
            eventInfo.plane = pPlane;
            eventInfo.port = pPort;
            eventInfo.eventName = pRegisterEvent;
            EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);

            foreach (RegisterInf reginfo in returnEventInfo.listRegisters)
            {
                Log.Message("Offset being checked = {0} Bitmap being checked {1}  Value to be got = {2}", reginfo.Offset, reginfo.Bitmap, reginfo.Value);
                DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
                driverData.input = Convert.ToUInt32(reginfo.Offset, 16);
                DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
                if (!AccessInterface.SetFeature<bool, DriverEscapeParams>(Features.DriverEscape, Action.SetMethod, driverParams))
                    Log.Abort("Failed to read Register with offset as {0}", driverData.input);
                else
                    if (compare)
                    {
                        if (!CompareRegisters(driverData.output, reginfo))
                        {
                            Log.Fail("Register with offset {0} doesnot match required values", reginfo.Offset);
                            regValueMatched = false;
                        }
                    }
            }

            return regValueMatched;
        }

        protected bool CompareRegisters(uint argDriverData, RegisterInf argRegInfo)
        {
            uint bit = Convert.ToUInt32(argRegInfo.Bitmap, 16);
            Log.Verbose("Bitmap in uint = {0}, Value from register read = {1}", bit, argDriverData);
            uint hex = Convert.ToUInt32(String.Format("{0:X}", argDriverData), 16);
            Log.Verbose("value from reg read in ubit = {0}", hex);
            string value = String.Format("{0:X}", hex & bit);
            Log.Verbose("after bitmap = {0}", value);

            uint registerValue = Convert.ToUInt32(value);
            uint expectedValue = Convert.ToUInt32(argRegInfo.Value);
            //if (String.Equals(value, argRegInfo.Value))
            if(registerValue==expectedValue)
            {
                Log.Success("Current Value: {0}   Expected Value : {1}", registerValue, expectedValue);
                Log.Message("Register Values Matched");
                return true;
            }
            Log.Fail("Current Value: {0}   Expected Value : {1}",registerValue,expectedValue);
            return false;
        }
        protected void CheckDithering(DisplayType argDispType, DeepColorAppType argDeepColorApp)
        {            
            PipePlaneParams pipePlane1 = new PipePlaneParams(argDispType);
            pipePlane1 = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane1);
            Log.Message("For display : {0}  @@@  PIPE : {1} @@@ PLANE : {2}", argDispType, pipePlane1.Pipe, pipePlane1.Plane);

            DisplayInfo curDispInfo = new DisplayInfo();
            uint appValue=0;
            string eventName=_ditheringDisable;
            string deepColorEvent = _deepcolorDisable;
            if(_appBPCValue.Keys.ToList().Contains(argDeepColorApp))
            {
                appValue = _appBPCValue[argDeepColorApp];
                Log.Message("{0} creates frame buffer of {1}bpc",argDeepColorApp, appValue);
                curDispInfo = base.EnumeratedDisplays.Where(dI => dI.DisplayType == argDispType).FirstOrDefault();
                if (argDispType != _nonDithering)
                {                  
                    Log.Message("{0} supports {1}bpc", argDispType, curDispInfo.ColorInfo.MaxDeepColorValue);
                    int maxBpp = curDispInfo.ColorInfo.MaxDeepColorValue;
                    if (maxBpp < appValue)
                    {
                        eventName = _ditheringEnable;
                        deepColorEvent = _deepcolorEnable;
                    }
                }
            }
            Log.Message(true, "Verifying {0} for {1}", eventName,argDispType);
            VerifyRegisters(eventName, pipePlane1.Pipe, pipePlane1.Plane, PORT.NONE);

            Log.Message(true, "Verifying Dithering Type:Spatial  for {0}",argDispType);
            VerifyRegisters("DITHERING_TYPE", pipePlane1.Pipe, pipePlane1.Plane, PORT.NONE);

           
           // String regEvent = curDispInfo.DisplayType + "_" + curDispInfo.ColorInfo.MaxDeepColorValue + "_" + deepColorEvent;
            String regEvent = "BPC_" + curDispInfo.ColorInfo.MaxDeepColorValue;
            if (eventName == _ditheringDisable)
            {
                Log.Message("Verifying {0} for {1}",appValue , argDispType);
                //regEvent = curDispInfo.DisplayType + "_" + appValue + "_" + eventName;
                regEvent = "BPC_" + appValue;
            }
            Log.Message(true, "Verifying Dithering {0} for {1}", regEvent, argDispType);
            VerifyRegisters(regEvent, pipePlane1.Pipe, pipePlane1.Plane, PORT.NONE);

        }
        protected void CloseApp()
        {
            //Closing Deep color App
            Log.Message(true, "Closing App");
            _DPParam.DeepColorOptions = DeepColorOptions.Close;
            AccessInterface.SetFeature<DeepColorParams>(Features.DeepColor, Action.Set, _DPParam);

            Log.Success("Closed App");
        }
        protected void Disable10BitScanner()
        {
            Log.Message(true, "Disabling Feature : 10 bit Scanner");

            _DPParam.DeepColorOptions = DeepColorOptions.Disable;
            AccessInterface.SetFeature<DeepColorParams>(Features.DeepColor, Action.Set, _DPParam);

            Log.Success("Disabled Feature : 10 bit scanner");
        }
        protected void InvokePowerEvent(PowerStates argPowerState)
        {
            Log.Message(true, "Invoking power event {0}", argPowerState);
            PowerParams powerParams = new PowerParams() { Delay = 30 };
            powerParams.PowerStates = argPowerState;
            base.EventResult(powerParams.PowerStates, base.InvokePowerEvent(powerParams, powerParams.PowerStates));
        }
    }
}
