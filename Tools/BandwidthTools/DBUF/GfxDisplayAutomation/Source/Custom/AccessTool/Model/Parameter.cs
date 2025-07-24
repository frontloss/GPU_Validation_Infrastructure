using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
   public class Parameter:BaseEntity
    {
       public Dictionary<String, List<string>> parameterData;

        public Dictionary<String, List<string>> ParameterData
        {
            get { return parameterData; }
            set { parameterData = value;
            Notify("ParameterData");
            }
        }
    }
}
