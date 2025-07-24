namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Runtime.InteropServices;
    using System.Text;
    public class InterfaceParam
    {
        public string ParameterName { get; set; }
        public string ParameterValue { get; set; }
        public string Delimeter { get; set; }
    }
    public enum InterfaceType
    {
        None = 0,
        IGet,
        IGetMethod,
        IGetAll,
        IGetAllMethod,
        ISet,
        ISetMethod,
        ISetAllMethod,
        ISetNoArgs
    }
    [AttributeUsage(AttributeTargets.Method | AttributeTargets.Class, AllowMultiple = true)]
    public class ParseAttribute : Attribute
    {
        public InterfaceType InterfaceName { get; set; }
        public String[] InterfaceData { get; set; }
        public String Comment { get; set; }
        public ParseAttribute()
        {

            // this.InterfaceData = new List<string>();
        }
    }
}
