namespace Intel.VPG.Display.Automation
{
    class MP_WiGig_RFLinkLost : MP_WiGig_Base
    {
        //Function to perform RF LinkLost
        [Test(Type = TestType.Method, Order = 0)]
        public void RFLinkLost()
        {
            Log.Message("WiGig RF Link Lost test started ....");
            WiGigParams wigigInputParam = new WiGigParams();
            wigigInputParam.wigigSyncInput = WIGIG_SYNC.RF_LinkLost;
            base.RFLinkLost(wigigInputParam);
        }
    }
}
