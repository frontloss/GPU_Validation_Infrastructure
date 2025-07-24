namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    
    class SB_Config_Modes_S4:SB_Config_Modes_S3
    {
        const string S4_Config_File = "S4PowerData.config";
        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            int cyc = GetNoOfCycles(S4_Config_File);
            for(int i=0;i<cyc;i++)
            InvokePowerEvent(PowerStates.S4);
        }
    }
}
