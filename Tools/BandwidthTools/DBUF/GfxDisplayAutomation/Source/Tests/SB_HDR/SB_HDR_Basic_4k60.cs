using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace Intel.VPG.Display.Automation
{
    class SB_HDR_Basic_4k60:SB_HDR_Base
    {

        // verifying metadata in 4k2k@60 case
        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            if((currentConfig.ConfigType == DisplayConfigType.SD) && (currentConfig.PrimaryDisplay == DisplayType.DP))
               Log.Message("Skipping Apply Config - Already Set!");
            else
                base.ApplyConfigOS(base.CurrentConfig);

            // applyy 4k2k 60 SD mode
            DisplayMode argMode = new DisplayMode();

            argMode.Angle = 0;
            argMode.HzRes = 3840;
            argMode.VtRes = 2160;
            argMode.RR = 60;
            argMode.InterlacedFlag = 0;
            argMode.Bpp = 32;
                       
            argMode.ScalingOptions = new List<uint>();
            argMode.ScalingOptions.Add(Convert.ToUInt32(ScalingOptions.Maintain_Display_Scaling));

            ApplyModeOS(argMode,DisplayType.DP);
            VerifyModeOS(argMode,DisplayType.DP);

            LaunchTenPlayerFullScreen(DisplayType.DP, "HDR1", "metadata1",10);
         
            Thread.Sleep(10000);
          //  bool Status = ParseHDRLog();
          //  if (Status)
          //  {
                ValidateMetadata("hdrmetadata1");
                ValidateColorRegistersProgramming(_HDR_Verification60, DisplayType.DP);
                ValidateBPCProgramming(_HDR_BPC10, DisplayType.DP);
                ValidateCSCCoeff_PostOffsetRegisters(DisplayType.DP);
                ValidateDPCD(DisplayType.DP, true);
          //  }
            // CRC verification

                CRCComputation(DisplayType.DP);
                CloseTenPlayerFullScreen();
        }

        // verifying HDR reset
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            base.ApplyConfigOS(base.CurrentConfig);
            ValidateHDrReset(_HDRMetadataEvent, DisplayType.DP);
           
        }
    }
}
