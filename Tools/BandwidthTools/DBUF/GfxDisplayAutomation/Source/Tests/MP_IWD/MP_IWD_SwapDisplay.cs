namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.WiDi)]
    class MP_IWD_SwapDisplay : MP_IWDBase
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
                this.SetNValidateConfig(dC);
            });
        }
    }
}

