namespace Intel.VPG.Display.Automation
{
    class SB_CDClock_DisplaySwap : SB_CDClock_Config_Basic
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPrerequisite()
        {
            if (base.CurrentConfig.ConfigType == DisplayConfigType.SD)
                Log.Abort("This test not applicable for {0}", base.CurrentConfig.GetCurrentConfigStr());
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            DisplayConfig currentConfig1 = new DisplayConfig();
            currentConfig1.ConfigType = base.CurrentConfig.ConfigType;
            currentConfig1.PrimaryDisplay = base.CurrentConfig.SecondaryDisplay;
            currentConfig1.SecondaryDisplay = base.CurrentConfig.PrimaryDisplay;
            currentConfig1.TertiaryDisplay = base.CurrentConfig.TertiaryDisplay;

            base.ApplyConfig(currentConfig1);
            VerifyCDClockRegisters();
        }
    }
}
