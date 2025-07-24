using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    public class PipePlaneParams
    {
        private DisplayType displayType;
        private PIPE pipe;
        private PLANE plane;

        public PipePlaneParams(DisplayType display)
		{
			this.displayType =  display;
		}        
		
		public PIPE Pipe 
		{
			get{ return this.pipe ; }
			set{ this.pipe = value ; } 			
		}

        public PLANE Plane
        {
            get { return this.plane; }
            set { this.plane = value; } 	
        }

        public DisplayType DisplayType
        {
            get { return this.displayType; }
        }
    }
}
