using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_VRR_Check_Status : SB_VRR_Base
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.ConfigTypeCount != base.CurrentConfig.DisplayList.Count())
                Log.Abort("This test requires atleast {0} displays , current display count: {1}", base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Checking VRR live status");
            DisplayList VrrSupportedDisplayList = new DisplayList();
            GetVRRCapableDisplays(VrrSupportedDisplayList);
            if (VrrSupportedDisplayList.Count == 0)
                Log.Abort("This test requires VRR capable displays. None of the connected displays are VRR capable.");

            VrrSupportedDisplayList.ForEach(disp =>
            {
                uint ret= base.IsVRREnabled(disp);
                if (ret == 0)
                    Log.Message("VRR is disabled on display {0}", disp.ToString());
                else
                    Log.Message("VRR is enabled on display {0}", disp.ToString());
            });
        }
    }
}
