namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    [Test(Type = TestType.WiDi)]
    class MP_WIDI_Modes_CUI : MP_WIDIBase
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void SetConfigMethod()
        {
            this.SetNValidateConfig(this.CurrentConfig);
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void GetNSetModes()
        {
            if (!this.GetAllModesForActiceDisplay().Count.Equals(0))
            {
                DisplayInfo currentDisplayInfo = null;
                commonDisplayModeList.ForEach(dML =>
                {
                    Log.Message(true, "Applying All modes for display {0}", dML.display.ToString());
                    DisplayConfig OSConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
                    Log.Verbose(OSConfig.GetCurrentConfigStr());
                    if (OSConfig.ConfigType != this.CurrentConfig.ConfigType &&
                        OSConfig.PrimaryDisplay != this.CurrentConfig.PrimaryDisplay &&
                        OSConfig.SecondaryDisplay != this.CurrentConfig.SecondaryDisplay &&
                        OSConfig.TertiaryDisplay != this.CurrentConfig.TertiaryDisplay)
                    {
                        Log.Fail(false,"Configuration missmatch test config: {0} and current config: {1}", this.CurrentConfig.GetCurrentConfigStr(), OSConfig.GetCurrentConfigStr());
                        this.SetNValidateConfig(this.CurrentConfig);
                    }
                    currentDisplayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == dML.display).First();
                    dML.supportedModes.ForEach(dM => this.ApplyModeNVerify_CUI(dM));
                });
            }
            else
            {
                Log.Fail("Unable to find mode list");
            }
        }
    }
}
