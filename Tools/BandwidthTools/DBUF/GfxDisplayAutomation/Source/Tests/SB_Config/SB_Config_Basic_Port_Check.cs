namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    class SB_Config_Basic_Port_Check : SB_Config_Base
    {
        
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.ConfigTypeCount != base.CurrentConfig.DisplayList.Count())
                Log.Abort("This test requires atleast {0} displays , current display count: {1}", base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());
           
        }
        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            ApplyConfigOS(this.CurrentConfig);
            VerifyConfigOS(this.CurrentConfig);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            this.CurrentConfig.CustomDisplayList.ForEach(disp =>
                {
                    DisplayInfo displayInfo = this.CurrentConfig.EnumeratedDisplays.Find(dispInfo => dispInfo.DisplayType == disp);

                    string eventName = disp + "_ENABLED";
                    if (VerifyRegisters(eventName, PIPE.NONE, PLANE.NONE, displayInfo.Port, true))
                        Log.Success("{0} is enabled on expected port {1}", disp,displayInfo.Port);
                    else
                        Log.Fail("{0} is not enabled on expected port {1}",disp,displayInfo.Port);
                });
        }
    }
}
