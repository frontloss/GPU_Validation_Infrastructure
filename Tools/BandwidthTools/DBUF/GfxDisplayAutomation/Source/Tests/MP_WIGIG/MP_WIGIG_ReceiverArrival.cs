namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;

    class MP_WiGig_ReceiverArrival : MP_WiGig_Base
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void ReceiverArrival()
        {
            Log.Message("WiGig Receiver Arrival test started ....");
            List<DisplayType> displist =base.CurrentConfig.DisplayList.ToList();
            foreach (DisplayType display in displist)
            {
                if (DisplayExtensions.GetDisplayType(display) == DisplayType.WIGIG_DP)
                {
                    WiGigParams wigigInputParam = new WiGigParams();
                    wigigInputParam.wigigSyncInput = WIGIG_SYNC.Receiver_Arrival;
                    wigigInputParam.wigigDisplay = display;
                    base.ReceiverArrival(wigigInputParam);
                }
            }           
        }

        //Function to perform Receiver Kill
        [Test(Type = TestType.Method, Order = 2)]
        public void ReceiverKill()
        {
            Log.Message("WiGig Receiver Kill test started ....");
            WiGigParams wigigInputParam = new WiGigParams();
            wigigInputParam.wigigSyncInput = WIGIG_SYNC.RF_Kill;
            base.ReceiverKill(wigigInputParam);
        }
    }
}
