namespace WiDiConnectionApp
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;

    public class WiDiParam
    {
        private Initialize initializeStatus;
        private List<string> adapterIds;
        private Initialize connectionStatus;

        public Initialize ConnectionStatus
        {
            get { return connectionStatus; }
            set { connectionStatus = value; }
        }
        public Initialize InitializeStatus
        {
            get { return initializeStatus; }
            set { initializeStatus = value; }
        }
        public List<string> AdapterIds
        {
            get { return adapterIds; }
            set { adapterIds = value; }
        }

    }
}
