namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;

    class SB_PPC_Apply_All_Modes : SB_PPC_Config_Basic
    {
        private List<DisplayModeList> _commonDisplayModeList = new List<DisplayModeList>();

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
                    base.VerifyPPC();
                });
            });
        }
    }
}