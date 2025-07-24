namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
     [Test(Type = TestType.HasPlugUnPlug)]
    class SB_Hotplug_Unplug_S3_Semiautomated:SB_Hotplug_Unplug_S3
    {
        [Test(Type = TestType.Method, Order = 2)]
        public override void TestStep2()
        {
            base.TestStep2();
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                if (_semiAutomatedDispList.Contains(curDisp))
                {
                    base.PerformSemiautomated("Unplug " + curDisp);
                }
            });
        }
        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            base.TestStep3();
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                if (_semiAutomatedDispList.Contains(curDisp))
                {
                    base.PerformSemiautomated("Plug " + curDisp + " after the system initiate's S3 ");
                    InvokePowerEvent(PowerStates.S3);
                }
            });
            List<DisplayInfo> enumeratedDisplay = AccessInterface.GetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);
            base.CurrentConfig.EnumeratedDisplays.Clear();
            base.CurrentConfig.EnumeratedDisplays.AddRange(enumeratedDisplay);
        }
    }
}
