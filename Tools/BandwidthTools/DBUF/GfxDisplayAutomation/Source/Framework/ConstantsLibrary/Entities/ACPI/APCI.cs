namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    using System.IO;
    using System.Threading;
    using System.Diagnostics;

    public struct apciDisplayList
    {
        public DisplayConfigType DisplayConfig;
         public List<DisplayType> DisplayTypeList;
    };

    public class APCI
    {
       // public int FunctionNumber { get; set; }
       // public int StepNumber { get; set; }

        public string Platform { get; set; }
        public string Key { get; set; }

        public List<DisplayType> DisplayTypeList { get; set; }
        public List<apciDisplayList> ApciToggleList { get; set; }
        //public Dictionary<String, List<String>> ApciToggleList{get;set;}
    }
}
