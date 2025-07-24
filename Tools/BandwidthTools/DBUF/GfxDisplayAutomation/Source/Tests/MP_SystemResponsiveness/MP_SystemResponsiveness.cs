namespace Intel.VPG.Display.Automation
{
    class MP_SystemResponsiveness : TestBase
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            AccessInterface.SetFeature<bool>(Features.SystemResponsiveness, Action.Set, Source.AccessUI);
        }
    }
}
