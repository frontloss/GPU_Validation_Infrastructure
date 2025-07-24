namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using System.Xml.Linq;
    using System.IO;
    using System.Text;
    using System;

    public class RegisterInf
    {
        public String Offset;
        public String Bitmap;
        public String Value;
        public String Deviation;
        public String RegisterValue;
        public uint BitmappedValue;
        public RegisterInf(string offset, string bitmap, string value, string deviation = "0")
        {
            Offset = offset;
            Bitmap = bitmap;
            Value = value;
            Deviation = deviation;
        }
    }    
    public class EventInfo
    {
        public PORT port { get; set; }
        public PIPE pipe { get; set; }
        public PLANE plane { get; set; }
        public string eventName { get; set; }
        public bool RegistersMatched { get; set; }
        public List<RegisterInf> listRegisters { get; set; }
    }    
}
