namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Threading;

    class SB_LPSP_Overlay : SB_LPSP_Base
    {
        private DisplayType _Displaytype;
        private OverlayParams overlay = null;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public override void TestStep0()
        {
            if (CurrentConfig.ConfigType.GetUnifiedConfig() != DisplayUnifiedConfig.Extended)
                Log.Abort("This Test is applicable only for Extended mode only.");

            base.TestStep0();
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            foreach (KeyValuePair<System.Action, System.Action> _CurrentModeType in _applyMode)
            {
                // Step - 1                
                _CurrentModeType.Key();

                //Step - 2
                if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, CurrentConfig))
                    Log.Success("Config Appliyed : {0}", CurrentConfig.GetCurrentConfigStr());
                else
                    Log.Abort("Failed to Apply Config : {0}", CurrentConfig.GetCurrentConfigStr());

                //Step - 3          
                overlay = new OverlayParams()
                {
                    PlaybackOptions = OverlayPlaybackOptions.MovePlayer,
                    DisplayHierarchy = DisplayHierarchy.Display_1,
                    CurrentConfig = base.CurrentConfig
                };

                // Play overlay player to Primary Display 
                AccessInterface.SetFeature<OverlayParams>(Features.Overlay, Action.Set, overlay);

                overlay.DisplayHierarchy = CurrentConfig.PrimaryDisplay != DisplayType.EDP ? DisplayHierarchy.Display_1 : DisplayHierarchy.Unsupported;
                _Displaytype = CurrentConfig.PrimaryDisplay;

                if (overlay.DisplayHierarchy == DisplayHierarchy.Unsupported)
                {
                    overlay.DisplayHierarchy = CurrentConfig.SecondaryDisplay != DisplayType.EDP ? DisplayHierarchy.Display_2 : overlay.DisplayHierarchy;
                    _Displaytype = CurrentConfig.SecondaryDisplay;
                }

                if (base.CurrentConfig.ConfigType == DisplayConfigType.TED)
                {
                    if (overlay.DisplayHierarchy == DisplayHierarchy.Unsupported)
                    {
                        overlay.DisplayHierarchy = CurrentConfig.TertiaryDisplay != DisplayType.EDP ? DisplayHierarchy.Display_3 : overlay.DisplayHierarchy;
                        _Displaytype = CurrentConfig.TertiaryDisplay;
                    }
                }

                Log.Message(true, "Moving Overlay App to Display {0} ", _Displaytype);

                // Shift Overlay App to non EDP Panel
                overlay.PlaybackOptions = OverlayPlaybackOptions.MovePlayer;
                AccessInterface.SetFeature<OverlayParams>(Features.Overlay, Action.Set, overlay);
                Thread.Sleep(5000);

                // Step - 4
                Log.Message(true, "Verify LPSP Registers");
                LPSPRegisterVerify(false);

                // Step - 5
                Log.Message(true, "Verify Overlay Registers");
                OverlayRegisterVerify(true, _Displaytype);

                //Step - 6
                DisplayConfig dispConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = DisplayType.EDP };
                if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dispConfig))
                    Log.Success("Config SET : SD - EDP");
                else
                    Log.Fail("Failed to set Config : SD - EDP");

                // Step - 7
                ApplyNativeMode();

                // Step - 8
                Log.Message(true, "Verify LPSP Registers");
                LPSPRegisterVerify(true);

                // Step - 9
                Log.Message(true, "Verify Overlay Registers");
                OverlayRegisterVerify(true, DisplayType.EDP);

                // Step - 10
                Log.Message(true, "Closing Overlay Application");
                overlay.PlaybackOptions = OverlayPlaybackOptions.ClosePlayer;
                AccessInterface.SetFeature<OverlayParams>(Features.Overlay, Action.Set, overlay);
            }
        }
    }
}