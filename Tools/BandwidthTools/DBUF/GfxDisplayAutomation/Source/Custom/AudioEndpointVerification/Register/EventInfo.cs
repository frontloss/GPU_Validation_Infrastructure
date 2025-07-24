namespace AudioEndpointVerification
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
        public RegisterInf(string offset, string bitmap, string value)
        {
            Offset = offset;
            Bitmap = bitmap;
            Value = value;
        }
    }    
    public class EventInfo
    {
        public PORT port { get; set; }
        public PIPE pipe { get; set; }
        public PLANE plane { get; set; }
        public string eventName { get; set; }
        public List<RegisterInf> listRegisters { get; set; }
    }    
}
