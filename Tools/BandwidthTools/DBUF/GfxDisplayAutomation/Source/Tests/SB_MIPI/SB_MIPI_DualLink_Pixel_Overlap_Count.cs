using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_MIPI_DualLink_Pixel_Overlap_Count : SB_MIPI_Native_Resolution
    {        
        protected override void VerifyRegisters()
        {
            Dual_Link_Mode dualLinkMode = GetMIPIDualLinkMode();
            Log.Message("Current Link Mode is: {0}.", dualLinkMode);

            if (dualLinkMode == Dual_Link_Mode.Dual_Link_Front_Back_Mode || dualLinkMode == Dual_Link_Mode.Dual_Link_Pixel_Alternative_Mode)
            {
                string st = Enum.GetName(typeof(Dual_Link_Mode), dualLinkMode);
                uint PixelOverlapCount_Vbt = GetMIPIDualLinkPixelOverlap();

                availablePorts.ForEach(eachPort =>
                {
                    base.VerifyRegisters(st, eachPort);

                    uint PixelOverlap_Driver = GetRegisterValue(MIPI_PIXEL_OVERLAP_COUNT, PIPE.NONE, PLANE.NONE, eachPort);
                    
                    if (PixelOverlapCount_Vbt == PixelOverlap_Driver)
                        Log.Success("DualLink Pixel Overlap Count Matched with programmed in VBT: {0} for Port:{1}", PixelOverlapCount_Vbt, eachPort);
                    else
                        Log.Fail("Mismatch in DualLink Pixel Overlap Count for Port:{0}. VBT: {1}, Driver Programmed: {2}", eachPort, PixelOverlapCount_Vbt, PixelOverlap_Driver);
                });
            }
            else
                Log.Fail("Should plan this test with Single Link MIPI panel/VBT.");
        }
    }
}
