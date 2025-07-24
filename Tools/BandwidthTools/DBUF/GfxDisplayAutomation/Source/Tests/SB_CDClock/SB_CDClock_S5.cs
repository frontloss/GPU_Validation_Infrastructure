using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_CDClock_S5 : SB_CDClock_S3
    {
        public SB_CDClock_S5()
        {
            _PowerState = PowerStates.S5;
        }
    }
}
