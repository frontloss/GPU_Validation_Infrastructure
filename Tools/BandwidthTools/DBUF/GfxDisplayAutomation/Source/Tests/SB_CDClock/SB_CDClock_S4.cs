using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_CDClock_S4 : SB_CDClock_S3
    {
        public SB_CDClock_S4()
        {
            _PowerState = PowerStates.S4;
        }
    }
}
