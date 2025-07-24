namespace Intel.VPG.Display.Automation
{
    class MP_FuzzComEsc_18_2 : MP_FuzzyBase
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void SetConfigMethod()
        {
            Log.Message(true, "Set Current config via OS call");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
                Log.Abort("Unable to set display config.");
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void RunTest()
        {
            Log.Message(true, "Fuzzer Tool Invoke");
            FuzzDisplayEscapes(escMajorCode, escMinorCode);
            Log.Success("Test Successfully Completed...");
        }
    }
}
