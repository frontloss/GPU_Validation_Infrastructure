using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_CorruptionCheck_Config_Hotplug_Unplug_Basic:SB_Config_Hotplug_Unplug_Basic
    {
        public SB_CorruptionCheck_Config_Hotplug_Unplug_Basic()
        {
            base._Corruption = base.CheckCorruptionViaDVMU;           
        }
        [Test(Type = TestType.PreCondition, Order = 0)]
        public override void TestStep0()
        {
            base.TestStep0();
            SetUpDesktopArgs desktopArgs = new SetUpDesktopArgs(SetUpDesktopArgs.SetUpDesktopOperation.PrepareDesktop);
            bool status = AccessInterface.SetFeature<bool, SetUpDesktopArgs>(Features.SetUpDesktop, Action.SetMethod, desktopArgs);            
        }
        [Test(Type = TestType.Method, Order = 4)]
        public  void TestStep4()
        {
            SetUpDesktopArgs desktopArgs = new SetUpDesktopArgs(SetUpDesktopArgs.SetUpDesktopOperation.RestoreDesktop);
            bool status = AccessInterface.SetFeature<bool, SetUpDesktopArgs>(Features.SetUpDesktop, Action.SetMethod, desktopArgs);

        }
    }
}
