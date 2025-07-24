namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;

    class MP_WIGIG_Receiver_Arrival : MP_WIGIG_Base
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void ReceiverArrival()
        {
            Log.Message("Receiver Arrival");
            WIGIGParams wigigInputParam = new WIGIGParams();
            wigigInputParam.wigigSyncInput = WIGIG_SYNC.Receiver_Arrival;
            wigigInputParam.WigigReceiverArrival.Set(DisplayType.WIGIG_DP1, "DP_3011.EDID");
            base.ReceiverArrival(wigigInputParam);
            if (base.CurrentConfig.EnumeratedDisplays.Select(DT => DT.DisplayType.Equals(DisplayType.WIGIG_DP1)).FirstOrDefault())
            {
                Log.Success("Successfully Receiver arrival");
            }
            else
            {
                Log.Fail("Fail");
            }
            
        }
    }
}
