using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_CorruptionCheck_ApplyModes_Basic:SB_Modes_ApplyModes_Basic
    {
        public SB_CorruptionCheck_ApplyModes_Basic()
        {
            base._Corruption = base.CheckCorruptionViaDVMU;           
        }
        [Test(Type = TestType.PreCondition, Order = 0)]
        public override void TestStep0()
        {
            base.TestStep0();
            //SetUpDesktopArgs desktopArgs = new SetUpDesktopArgs(SetUpDesktopArgs.SetUpDesktopOperation.PrepareDesktop);
            //bool status = AccessInterface.SetFeature<bool, SetUpDesktopArgs>(Features.SetUpDesktop, Action.SetMethod, desktopArgs);            
        }
        [Test(Type = TestType.Method, Order = 3)]
        public  void TestStep3()
        {
            //SetUpDesktopArgs desktopArgs = new SetUpDesktopArgs(SetUpDesktopArgs.SetUpDesktopOperation.RestoreDesktop);
            //bool status = AccessInterface.SetFeature<bool, SetUpDesktopArgs>(Features.SetUpDesktop, Action.SetMethod, desktopArgs);

        }
    }
}
