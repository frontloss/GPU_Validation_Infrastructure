using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    public enum WIGIG_SYNC
    {
        None = 0,
        Receiver_Arrival,
        RF_Kill,
        RF_LinkLost,
        WiGigDisplayPipe,//Pipe Assignment Enum     
        QuickCapture// QuickCapture enum
    }
}
