namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;

    [Test(Type = TestType.WiDi)]
    class MP_WIDI_Modes_OSPage : MP_WIDIBase
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void SetConfigMethod()
        {
            Log.Message(true, "Set display Config using Windows API");
            this.SetNValidateConfig(this.CurrentConfig);
            if (!this.GetAllModesForActiceDisplay().Count.Equals(0))
            {
                commonDisplayModeList.ForEach(dML =>
                {
                    Log.Message(true,"Applying All modes for display {0}", dML.display.ToString());
                    DisplayConfig OSConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
                    Log.Verbose(OSConfig.GetCurrentConfigStr());
                    if (OSConfig.ConfigType != this.CurrentConfig.ConfigType && 
                        OSConfig.PrimaryDisplay != this.CurrentConfig.PrimaryDisplay &&
                        OSConfig.SecondaryDisplay != this.CurrentConfig.SecondaryDisplay &&
                        OSConfig.TertiaryDisplay != this.CurrentConfig.TertiaryDisplay)
                    {
                        Log.Fail("Configuration missmatch test config: {0} and current config: {1}", this.CurrentConfig.GetCurrentConfigStr(), OSConfig.GetCurrentConfigStr());
                        this.SetNValidateConfig(this.CurrentConfig);
                    }
                    dML.supportedModes.ForEach(dM => this.ApplyModeAndVerify(dM));
                });
            }
            else
            {
                Log.Fail("Unable to find mode list");
            }

        }
    }
}
