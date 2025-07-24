namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;

    [Test(Type = TestType.WiDi)]
    class MP_IWD_HDMIModes : MP_IWDBase
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void SetConfigMethod()
        {
            Log.Message(true, "Set display Config using Windows API");
            if (base.CurrentConfig.CustomDisplayList.Count == 3)
                GetThreeDisplaySwitchingPattern(this.switchPatternList);
            else
                this.GetTwoDisplaySwitchPattern(this.switchPatternList);

            this.switchPatternList.ForEach(dC =>
            {
                if (this.SetNValidateConfig(dC))
                {
                    if (!this.GetAllModesForActiceDisplay().Count.Equals(0))
                    {
                        DisplayInfo currentDisplayInfo = null;
                        List<DisplayMode> testModes = null;
                        commonDisplayModeList.ForEach(dML =>
                        {
                            currentDisplayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == dML.display).First();
                            testModes = this.TestModes(dML.supportedModes);
                            testModes.ForEach(dM => this.ApplyAndVerify(dM, currentDisplayInfo));
                        });
                    }
                }
            });

        }
    }
}
