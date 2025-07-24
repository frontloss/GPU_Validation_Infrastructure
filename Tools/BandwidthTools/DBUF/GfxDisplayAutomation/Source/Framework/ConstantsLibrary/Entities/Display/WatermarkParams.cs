using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    public class Watermark_Params
    {
        private DisplayType displayType;
        public DisplayConfig CurrentConfig { get; set; }
        public Dictionary<DisplayType, DisplayParams> DisplayParametersList { get; set; }

        public Watermark_Params(DisplayType display)
		{
			this.displayType =  display;
		}

        public DisplayType DisplayType
        {
            get { return this.displayType; }
        }

        public struct DisplayParams
        {
            public DisplayMode displayMode;
            public PipePlaneParams pipePlaneParams;
        }
    }
}
