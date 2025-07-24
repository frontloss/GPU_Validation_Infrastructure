using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    public class PipeDbufInfo
    {
        public PipeDbufInfo()
        {
            MinDBufNeeded = 0;
        }
        public DisplayType DisplayType { get; set; }
        public DisplayConfigType DisplayConfigType { get; set; }
        public uint DbufAllocated { get; set; }
        public PIPE Pipe { get; set; }
        public PLANE plane { get; set; }
        public DBufInfo PlaneA { get; set; }
        public DBufInfo PlaneB { get; set; }
        public DBufInfo PlaneC { get; set; }
        public uint MinDBufNeeded { get; set; }
    }
}