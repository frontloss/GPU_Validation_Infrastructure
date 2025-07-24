namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;

    public class ConnectorType
    {
        public ConnectorType() { connectorType = string.Empty; deviceType = string.Empty; }
        public string connectorType { get; set; }
        public string deviceType { get; set; }
    }
}
