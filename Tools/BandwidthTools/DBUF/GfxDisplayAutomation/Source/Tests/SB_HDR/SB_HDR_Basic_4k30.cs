using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace Intel.VPG.Display.Automation
{
    class SB_HDR_Basic_4k30 : SB_HDR_Base
    {
        
        // verifying metadata in 4k2k@30 case
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            
            base.ApplyConfigOS(base.CurrentConfig);
            base.VerifyConfigOS(base.CurrentConfig);

            //List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>,DisplayType>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, DisplayType.DP);
            //DisplayMode maxMode = new DisplayMode();
                          
            //allModeList.ForEach(curDisp =>
            //{
            //   maxMode = curDisp.supportedModes.Last();
            //});

            //if (maxMode.HzRes != 4096 || maxMode.VtRes != 2084)
            //    Log.Abort("The connected display doesnt dupport 4k2k mode..Aborting Test");

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

            LaunchTenPlayerFullScreen(DisplayType.DP, "HDR1", "metadata1", 10);


            Thread.Sleep(10000);
            // bool Status = ParseHDRLog();
            //if (Status)
            // {

            ValidateMetadata("hdrmetadata1");
            ValidateBPCProgramming(_HDR_BPC12, DisplayType.DP);   
            ValidateColorRegistersProgramming(_HDR_Verification30, DisplayType.DP);  
            ValidateCSCCoeff_PostOffsetRegisters(DisplayType.DP);
            ValidateDPCD(DisplayType.DP, false);
            // }
            
            // CRC verification
            CRCComputation(DisplayType.DP);
           
            CloseTenPlayerFullScreen();
        }

        public void TestStep2()
        {
            base.ApplyConfigOS(base.CurrentConfig);
            ValidateHDrReset(_HDRMetadataEvent, DisplayType.DP);

        }
    }
}


