using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace Intel.VPG.Display.Automation
{
    class SB_HDR_MultiDisplay : SB_HDR_Base
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {

            Log.Message(true, "Checking Preconditions and Plugging in HDR supported panel");
            if (!base.CurrentConfig.DisplayList.Contains(DisplayType.DP))
                Log.Abort("DP not passed in command line...Aborting the test");
            else if (base.CurrentConfig.ConfigType == DisplayConfigType.SD)
                Log.Abort("MultiConfig not planned..Aborting test");
        }

        // verifying multiconfig negative case
        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {

            base.ApplyConfigOS(base.CurrentConfig);

          
            DisplayMode argMode = new DisplayMode();

            argMode.Angle = 0;
            argMode.HzRes = 3840;
            argMode.VtRes = 2160;
            argMode.RR = 60;
            argMode.InterlacedFlag = 0;
            argMode.Bpp = 32;

            argMode.ScalingOptions = new List<uint>();
            argMode.ScalingOptions.Add(Convert.ToUInt32(ScalingOptions.Maintain_Display_Scaling));

            ApplyModeOS(argMode, DisplayType.DP);
            VerifyModeOS(argMode, DisplayType.DP);

            LaunchTenPlayerFullScreen(DisplayType.DP, "HDR1", "metadata1", 10);

            Thread.Sleep(10000);
            //  bool Status = ParseHDRLog();
            ValidateHDrReset(_HDRMetadataEvent, DisplayType.DP);
            // CRC verification
            CloseTenPlayerFullScreen();
        }


    }
}
