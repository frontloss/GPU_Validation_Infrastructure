using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
     [Test(Type = TestType.HasPlugUnPlug)]
    class SB_Hotplug_Unplug_CS_Semiautomated:SB_Hotplug_Unplug_CS
    {
         [Test(Type = TestType.Method, Order = 3)]
         public override void TestStep3()
         {
             base.TestStep3();
             base.CurrentConfig.DisplayList.ForEach(curDisp =>
             {
                 if (_semiAutomatedDispList.Contains(curDisp))
                 {
                     base.PerformSemiautomated("Plug " + curDisp + " after the system initiate's CS ");
                     InvokePowerEvent(PowerStates.CS);
                 }
             });
             List<DisplayInfo> enumeratedDisplay = AccessInterface.GetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);
             base.CurrentConfig.EnumeratedDisplays.Clear();
             base.CurrentConfig.EnumeratedDisplays.AddRange(enumeratedDisplay);
         }
    }
}
