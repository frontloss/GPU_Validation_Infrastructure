using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
     [Test(Type = TestType.HasINFModify)]
    class SB_NarrowGamut_S3 : SB_NarrowGamut_DisplaySwap
    {
        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
        {
            base.PowerEvent(PowerStates.S3);

            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            if (currentConfig.GetCurrentConfigStr().Equals(base.CurrentConfig.GetCurrentConfigStr()))
                Log.Success("{0} is retained", base.CurrentConfig.GetCurrentConfigStr());
            else
                Log.Fail("Expected: {0} , current {1}", base.CurrentConfig.GetCurrentConfigStr(), currentConfig.GetCurrentConfigStr());

            base.NarrowGamutSupportedDisplays.Intersect(base.CurrentConfig.DisplayList).ToList().ForEach(curDisp =>
            {
                base.CheckNarrowGamutRegister(curDisp, NarrowGamutOption.EnableNarrowGamut);
            });
        }
    }
}
