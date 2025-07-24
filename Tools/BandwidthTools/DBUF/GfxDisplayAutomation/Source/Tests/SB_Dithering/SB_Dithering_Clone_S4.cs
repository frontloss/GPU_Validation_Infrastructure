using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_Dithering_Clone_S4:SB_Dithering_Clone_S3
    {
        public SB_Dithering_Clone_S4()
        {
            base._powerState = PowerStates.S4;
        }
    }
}
