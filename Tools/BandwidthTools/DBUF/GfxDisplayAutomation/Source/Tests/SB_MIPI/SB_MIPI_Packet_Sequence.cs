using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_MIPI_Packet_Sequence : SB_MIPI_Native_Resolution
    {        
        protected override void VerifyRegisters()
        {
            Packet_Sequence_Video_Mode MipiPacketSequence = GetPacketSequence();

            string st = Enum.GetName(typeof(Packet_Sequence_Video_Mode), MipiPacketSequence);

            availablePorts.ForEach(eachPort => base.VerifyRegisters(st, eachPort));
        }
    }
}
