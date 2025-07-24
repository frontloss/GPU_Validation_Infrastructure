namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;

    class SB_MODES_Apply_All_Modes : SB_MODES_Base
    {
        private List<DisplayModeList> _commonDisplayModeList = new List<DisplayModeList>();

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {
            Log.Message(true, "Checking Preconditions for test");
            if (base.CurrentConfig.ConfigTypeCount != base.CurrentConfig.DisplayList.Count())
                Log.Abort("This test requires atleast {0} displays , current display count: {1}", base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Set current config via OS call");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Get the list of all the modes for the config passed and Apply them");
            _commonDisplayModeList = base.GetAllModes(base.CurrentConfig.CustomDisplayList);
            _commonDisplayModeList.ForEach(dML =>
            {
                dML.supportedModes.ToList().ForEach(dM =>
                {
                    base.ApplyModeOS(dM, dML.display);
                    base.VerifyModeOS(dM, dML.display);
                });
            });
        }
    }
}