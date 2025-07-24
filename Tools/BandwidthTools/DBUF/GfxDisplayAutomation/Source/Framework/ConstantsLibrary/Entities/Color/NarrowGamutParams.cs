using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    public class NarrowGamutParams
    {
        public DisplayType DisplayType { get; set; }
        public NarrowGamutOption narrowGamutOption { get; set; }
        public string INFFilePath { get; set; }
        public bool driverStatus { get; set; }
    }
}
