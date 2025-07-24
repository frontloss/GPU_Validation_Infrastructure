namespace Intel.VPG.Display.Automation
{
    using System.Net.NetworkInformation;
    using System.Management;
    using System.Threading;

    public class NetworkConnection : FunctionalBase, ISetMethod, IGet
    {
        public bool SetMethod(object argMessage)
        {
            NetParam networkParam = argMessage as NetParam;
            return NetworkExtensions.SetNetworkConnection(networkParam);
        }

        public object Get
        {
            get { return NetworkExtensions.GetWLANStatus(); }
        }
    }
}
