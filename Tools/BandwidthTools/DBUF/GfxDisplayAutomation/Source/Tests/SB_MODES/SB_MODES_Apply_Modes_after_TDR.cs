namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System.Threading;
    using System.Windows.Automation;
    using System.Windows;
    using System.IO;

    class SB_MODES_Apply_Modes_after_TDR : SB_MODES_Base
    {
        private List<DisplayModeList> _commonDisplayModeList = new List<DisplayModeList>();

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {
            //if (base.CurrentConfig.ConfigTypeCount > base.CurrentConfig.DisplayList.Count())
            //    Log.Abort("{0} requires atleast {1} Displays to be enumerated, current Display count: {2}", base.CurrentConfig.ConfigType, base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());
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
            Log.Message(true, "Force TDR");
            RunTDRNVerify(true, 1);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Verify that display comes up in same configuration as before TDR");
            DisplayConfig displayConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            if (displayConfig.ConfigType != base.CurrentConfig.ConfigType)
                Log.Abort("The config has changed after TDR");
            else
                Log.Success("The config has remained the same after TDR..");
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Get the list of all the modes for the config passed and apply the First, Last and Intermediate One");
            List<DisplayMode> modeList = null;
            _commonDisplayModeList = base.GetAllModes(base.CurrentConfig.CustomDisplayList);

            _commonDisplayModeList.ForEach(dML =>
            {
                modeList = GetMinMaxInterModes(dML.supportedModes.ToList());
                modeList.ForEach(dM =>
                {
                    base.ApplyModeOS(dM, dML.display);
                    base.VerifyModeOS(dM, dML.display);
                });
            });
        }
        private void RunTDRNVerify(bool argIsLogMessageParent, int argOverrideIdx)
        {
            Log.Message(argIsLogMessageParent, "Run ForceTDR.exe as given in note, 'To Run TDR Application'");
            if (this.RunTDR(argOverrideIdx))
                Log.Success("TDR Successful");
            else
                Log.Fail(false, "TDR Unsuccessful!");
        }
        private bool RunTDR(int argOverrideIdx)
        {
            Log.Verbose("Running TDR");
            if (!AccessInterface.SetFeature<bool>(Features.ForceTDR, Action.SetNoArgs))
            {
                if (!CommonExtensions.HasRetryThruRebootFile())
                {
                    Log.Sporadic(true, "TDR unsuccessful! A reboot may be required.");
                    this.InvokePowerEvent(new PowerParams() { Delay = 5, PowerStates = PowerStates.S5}, PowerStates.S5);
                }
                else
                    CommonExtensions.ClearRetryThruRebootFile();
            }
            else
            {
                CommonExtensions.ClearRetryThruRebootFile();
                return true;
            }
            return false;
        }
        private List<DisplayMode> GetMinMaxInterModes(List<DisplayMode> argmodeList)
        {
            List<DisplayMode> minMaxInterMode = new List<DisplayMode>();
            minMaxInterMode.Add(argmodeList.First());
            minMaxInterMode.Add(argmodeList[argmodeList.Count / 2]);
            minMaxInterMode.Add(argmodeList.Last());
            return minMaxInterMode;
        }
    }
}
