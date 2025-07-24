namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
     [Test(Type = TestType.HasPlugUnPlug)]
    class SB_Hotplug_Unplug_Basic_Semiautomated:SB_Hotplug_Unplug_Basic
    {
        [Test(Type = TestType.Method, Order = 2)]
        public override void TestStep2()
        {
            base.TestStep2();          
            base.CurrentConfig.DisplayList.ForEach(curDisp=>
            {
                if (_semiAutomatedDispList.Contains(curDisp))
                    base.PerformSemiautomated("Unplug " + curDisp);               
            });         
        }
        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            base.TestStep3();
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                if (_semiAutomatedDispList.Contains(curDisp))
                    base.PerformSemiautomated("Plug  " + curDisp);
            });
            List<DisplayInfo> enumeratedDisplays = AccessInterface.GetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);
           AccessInterface.SetFeature<bool, List<DisplayInfo>>(Features.DisplayEnumeration, Action.SetMethod, enumeratedDisplays);
           base.CurrentConfig.EnumeratedDisplays.Clear();
           base.CurrentConfig.EnumeratedDisplays.AddRange(enumeratedDisplays);
        }
    }
}
