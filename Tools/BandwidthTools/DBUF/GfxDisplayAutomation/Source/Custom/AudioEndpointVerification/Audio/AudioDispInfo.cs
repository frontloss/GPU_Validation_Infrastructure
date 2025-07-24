using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AudioEndpointVerification
{
    public class AudioDispInfo
    {
        public DisplayType DisplayType { get; set; }
        public string CompleteDisplayName { get; set; }
        public PORT Port { get; set; }
        public string AudioCapable { get; set; }
    }
}
