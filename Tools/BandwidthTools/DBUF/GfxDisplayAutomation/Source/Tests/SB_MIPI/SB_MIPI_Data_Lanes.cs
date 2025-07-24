using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_MIPI_Data_Lanes : SB_MIPI_Native_Resolution
    {
        protected override void VerifyRegisters()
        {
            UInt32 Lanes_Vbt = GetNoOfLanes();

            availablePorts.ForEach(eachPort =>
            {
                uint Lanes_Driver = GetRegisterValue(MIPI_DATA_LANES, PIPE.NONE, PLANE.NONE, eachPort);

                if (Lanes_Vbt == Lanes_Driver)
                    Log.Success("No. of lanes Matched with programmed in VBT: {0} for Port:{1}", Lanes_Vbt, eachPort);
                else
                    Log.Fail("Mismatch in Number of lanes for Port:{0}. VBT: {1}, Driver Programmed: {2}", eachPort, Lanes_Vbt, Lanes_Driver);
            });
        }
    }
}
