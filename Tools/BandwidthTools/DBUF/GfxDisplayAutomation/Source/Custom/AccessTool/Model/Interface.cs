using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Intel.VPG.Display.Automation
{
  public  class Interface:BaseEntity
    {
      public Interface(String argInterfaceName)
      {
          this.InterfaceName = argInterfaceName;
      }
        private string interfaceName;

        public string InterfaceName
        {
            get { return interfaceName; }
            set { interfaceName = value;
            Notify("InterfaceName");
            }
        }
    }
}
