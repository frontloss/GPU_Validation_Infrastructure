namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.HasINFModify)]
    [Test(Type = TestType.HasUpgrade)]
    class MP_BAT_DriverUpgrade_Start_Stop_Basic : MP_BAT_DriverUpgrade_Start_Stop
    {
        [Test(Type = TestType.Method, Order = 5)]
        public override void TestStep5()
        {
            Log.Alert("Power Events is skipped!");
        }
    }
}