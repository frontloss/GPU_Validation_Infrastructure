using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_MIPI_ColorFormat : SB_MIPI_Native_Resolution
    {
        protected override void VerifyRegisters()
        {
            Color_Format_Video_Mode MipiColorFormat = Color_Format_Video_Mode.MIPI_ColorFormat_Not_Supported;

            if (IsMipiVideoMode)
                MipiColorFormat = GetMIPIColorFormat();    

            string st = Enum.GetName(typeof(Color_Format_Video_Mode), MipiColorFormat);
            
            availablePorts.ForEach(eachPort => base.VerifyRegisters(st, eachPort));
        }
    }
}
