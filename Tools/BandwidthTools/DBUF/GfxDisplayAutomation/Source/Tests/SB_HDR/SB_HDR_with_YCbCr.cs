using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace Intel.VPG.Display.Automation
{
    class SB_HDR_with_YCbCr : SB_HDR_Base
    {

        protected ColorType _colorType = ColorType.YCbCr;
        protected XvYccYcbXr xvyccObject = null;
        protected string enableEvent = "YCBCR_ENABLE";
        protected string disableEvent = "YCBCR_DISABLE";
        protected string eventCalled = "";

        
        //enabling YCbCr
        [Test(Type = TestType.PreCondition, Order = 1)]
        public virtual void TestStep1()
        {

            base.ApplyConfigOS(base.CurrentConfig);


            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Find(dp1 => dp1.DisplayType == DisplayType.DP);
            
            if (displayInfo.ColorInfo.IsYcBcr)
            {
                Log.Message("{0} is supported on {1}", _colorType, displayInfo.DisplayType);
                xvyccObject = new XvYccYcbXr()
                {
                    displayType = displayInfo.DisplayType,
                    currentConfig = base.CurrentConfig,
                    colorType = _colorType,
                    isEnabled = 1
                };
                if (AccessInterface.SetFeature<bool, XvYccYcbXr>(Features.YCbCr, Action.SetMethod, xvyccObject))
                {
                    Log.Success("{0} is enabled on {1}", _colorType, displayInfo.DisplayType);
                    Log.Message(true, "Verify {0} enabled on {1} using Registers and CUI", _colorType, displayInfo.DisplayType);
                    eventCalled = enableEvent;
                    PipePlaneParams pipePlane1 = new PipePlaneParams(DisplayType.DP);
                    pipePlane1 = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane1);
                    Log.Message("For display : {0}  @@@  PIPE : {1} @@@ PLANE : {2}", DisplayType.DP, pipePlane1.Pipe, pipePlane1.Plane);

                    if (VerifyRegisters(enableEvent, pipePlane1.Pipe,pipePlane1.Plane,PORT.NONE))
                    {
                        Log.Success("YCbCr enabled successfully");
                    }
                    else
                    {
                        Log.Fail("YCbCr not enabled !!");
                    }
                }
                else
                    Log.Fail("{0} is not enabled on {1}", _colorType, displayInfo.DisplayType);
            }

        }


        // verifying metadata in 4k2k@30 case
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            DisplayMode argMode = new DisplayMode();
            argMode.Angle = 0;
            argMode.HzRes = 3840;
            argMode.VtRes = 2160;
            argMode.RR = 30;
            argMode.InterlacedFlag = 0;
            argMode.Bpp = 32;
            argMode.ScalingOptions = new List<uint>();
            argMode.ScalingOptions.Add(Convert.ToUInt32(ScalingOptions.Maintain_Display_Scaling));

            ApplyModeOS(argMode, DisplayType.DP);
            VerifyModeOS(argMode, DisplayType.DP);

            LaunchTenPlayerFullScreen(DisplayType.DP, "HDR1", "metadata1",10);


            Thread.Sleep(10000);
            // bool Status = ParseHDRLog();

            //if (Status)
            // {
            ValidateMetadata("hdrmetadata1");
            ValidateColorRegistersProgramming(_HDR_Verification30, DisplayType.DP);
            ValidateBPCProgramming(_HDR_BPC12, DisplayType.DP);
            ValidateCSCCoeff_PostOffsetRegisters(DisplayType.DP);
            // }
            // CRC verification
            CRCComputation(DisplayType.DP);

            CloseTenPlayerFullScreen();
        }
    }
}
