namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;

    public class MP_WiGig_Base : TestBase
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {
            
            List<DisplayType> displist =base.CurrentConfig.DisplayList.ToList();
            bool status=false;
            foreach (DisplayType display in displist)
            {
                if (DisplayExtensions.GetDisplayType(display) == DisplayType.WIGIG_DP)
                {
                    status=true;
                    break;
                }
            }
            if(status)
                Log.Message("WiGig Display is active...");
            else
                Log.Abort("WiGig display not enumerated");
        }
        public void ApplyConfig()
        {
              if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                {
                    Log.Success("Config applied successfully");
                }
                else
                {
                    Log.Abort("Config not applied!");
                }
        }
        
        public void ReceiverArrival(WiGigParams wigigParam)
        {
            if (AccessInterface.SetFeature<bool, WiGigParams>(Features.WIGIG, Action.SetMethod, wigigParam))
                Log.Success("WD Function is enabled");
            else
                Log.Fail("WD Function is not enabled");
        }
        
        public void ReceiverKill(WiGigParams wigigParam)
        {
            if(AccessInterface.SetFeature<bool, WiGigParams>(Features.WIGIG, Action.SetMethod, wigigParam))
                Log.Success("WD Function is disabled");
            else
                Log.Fail("WD Function is not disabled");
        }
        
        public void Pipe_Assignment(WiGigParams wigigParam)
        {
            if (AccessInterface.SetFeature<bool, WiGigParams>(Features.WIGIG, Action.GetMethod, wigigParam))
                Log.Success("WiGig active on correct pipe");
            else
                Log.Fail("WiGig active on different pipe");
        }
       
        public void RFLinkLost(WiGigParams wigigParam)
        {
            if (AccessInterface.SetFeature<bool, WiGigParams>(Features.WIGIG, Action.SetMethod, wigigParam))
                Log.Success("Link Lost happened successfully");
            else
                Log.Fail("Link Lost didn't happen successfully");
        }
        
        public void QuickCapture(WiGigParams wigigParam)
        {
            if (AccessInterface.SetFeature<bool, WiGigParams>(Features.WIGIG, Action.SetMethod, wigigParam))
                Log.Success("QC test passed successfully");
            else
                Log.Fail("QC test failed");
        }
    }
}
