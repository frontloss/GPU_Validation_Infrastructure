namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;

    [Test(Type = TestType.WiDi)]
    class MP_WIDI_SwapDisplays_CUI : MP_WIDIBase
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
            if (!IsWiDiConnected())
            {
                if (!WiDiReConnect())
                    CheckWiDiStatus();
            }
            Log.Message(true, "Setting display config using CUI");
            this.switchPatternList.ForEach(dC =>
            {
                if (SetNValidateConfigCUI(dC.DispConfig))
                    Log.Success("Switch successful to {0}", dC.DispConfig.GetCurrentConfigStr());
                else
                    Log.Fail("Failed to switch display config {0}", dC.DispConfig.GetCurrentConfigStr());

            });
            Log.Message("closing CUI");
            AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
        }

        private bool SetNValidateConfigCUI(DisplayConfig argConfig)
        {
            if (!IsWiDiConnected())
            {
                if (!WiDiReConnect())
                    CheckWiDiStatus();
            }
            AccessInterface.SetFeature<bool, DisplayConfig>(Features.SDKConfig, Action.SetMethod, argConfig);
            DisplayConfig currConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            return (currConfig.GetCurrentConfigStr().Equals(argConfig.GetCurrentConfigStr()));
        }

    }
}
