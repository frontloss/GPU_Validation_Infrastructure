namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Threading;

    [Test(Type = TestType.WiDi)]
    class MP_WIDI_SwapDisplay : MP_WIDIBase
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void PreCondition()
        {
            Log.Message(true, "Preparing display config switching list");
            if (base.CurrentConfig.DisplayList.Count < 2)
            {
                Log.Fail("To run the test minimum two maximum three display config required");
                Log.Abort("Exiting...");
            }
            switchPatternList = new List<DisplayConfigWrapper>();
            int dispFetchKey = base.CurrentConfig.CustomDisplayList.Count;
            int dispByPlatform = base.MachineInfo.PlatformDetails.Platform.GetDisplaysCount();
            if (dispFetchKey > dispByPlatform)
                dispFetchKey = dispByPlatform;
            this.SwitchPatternList[dispFetchKey](switchPatternList);
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void SetConfigMethod()
        {
            Log.Message(true, "Set display Config using Windows API");
            this.switchPatternList.ForEach(dC =>
            {
                this.SetNValidateConfig(dC.DispConfig);
                Thread.Sleep(10000);
            });
        }
    }
}

