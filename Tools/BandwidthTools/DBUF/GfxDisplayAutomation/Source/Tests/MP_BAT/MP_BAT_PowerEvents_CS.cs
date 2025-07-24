namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasReboot)]
    class MP_BAT_PowerEvents_CS : MP_BAT_PowerEvents
    {
        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            Log.Alert("CS PowerState not yet implemented!");
        }
        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
        {
            Log.Alert("S4 PowerState not yet implemented!");
        }
    }
}