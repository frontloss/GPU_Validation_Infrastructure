namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    class MP_WiGig_QuickCapture : MP_WiGig_Base
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void QuickCapture()
        {
            WiGigParams wigigInputParam = new WiGigParams();
            wigigInputParam.wigigSyncInput = WIGIG_SYNC.QuickCapture;
            base.QuickCapture(wigigInputParam);
        }
    }
}