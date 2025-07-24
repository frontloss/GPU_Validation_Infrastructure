using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AudioEndpointVerification
{
    public class AudioRegDataWrapper
    {
        public DisplayType DisplayType { get; set; }
        public string DisplayHierarchy { get; set; }
        public string AudioSupport { get; set; }
        public string Pipe { get; set; }
        public int RegValue { get; set; }
        public string Status { get; set; }
    }
}
