namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    [Test(Type = TestType.HasReboot)]
    class SB_Config_Modes_S5 : SB_Config_Modes_S3
    {
        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            InvokePowerEvent(PowerStates.S5);
        }
        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
        {
            DisplayConfig curConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            Log.Message("The config from CUI on resuming from S5 {0}", curConfig.GetCurrentConfigStr());
            _modeList = new List<DisplayModeList>();
            _modeList = base.GetMaxModeForConfig(base.CurrentConfig.DisplayList, base.CurrentConfig.ConfigType.GetUnifiedConfig());
            //base.TestStep4();
        }
    }
}
