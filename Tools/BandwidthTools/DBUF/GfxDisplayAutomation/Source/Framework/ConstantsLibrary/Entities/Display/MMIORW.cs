using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using System.Diagnostics;
using System.Text.RegularExpressions;

namespace Intel.VPG.Display.Automation
{
   public class MMIORW
    {
       public string FeatureName { get; set; }
       public List<RegisterInf> RegInfList { get; set; }
       public List<PORT> PortList { get; set; }
       public DisplayConfig currentConfig { get; set; }
    }
}
