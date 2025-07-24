namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.IO;
    using System.Threading;
    using System.Diagnostics;


    public class AppDetail
    {
        public string className { get; set; }
        public string processName { get; set; }
        public IntPtr handle { get; set; }
        public DisplayConfig displayConfig { get; set; }
        public DisplayHierarchy displayHierarchy { get; set; }
    }
}
