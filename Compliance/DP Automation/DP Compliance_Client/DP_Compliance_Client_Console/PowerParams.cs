using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DP_Compliance_Client_Console
{
    public class PowerParams
    {
        public PowerStates PowerStates { get; set; }
        public RebootReason rebootReason { get; set; }
        public int Delay { get; set; }
    }
    public class MonitorTurnOffParam
    {
        public int waitingTime { get; set; }
        public MonitorOnOff onOffParam { get; set; }
    }
}
