namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Text.RegularExpressions;

    class MP_Gamma_Base : TestBase
    {
        protected void ApplyGammaValue(ColorOptions argColorOptions, DisplayType argDisplay, double argGammaValue)
        {
            Log.Message(true, "Applying gamma {0} value for {1} in display {2}", argGammaValue, argColorOptions, argDisplay);
            AccessInterface.SetFeature(Features.SelectDisplay, Action.Set, argDisplay);
            AccessInterface.Navigate(Features.Gamma);
            AccessInterface.SetFeature<ColorOptions>(Features.Colour, Action.Set, argColorOptions);
            AccessInterface.SetFeature<string>(Features.Gamma, Action.Set, argGammaValue.ToString());
            if (AccessInterface.SetFeature<bool, AppBarOptions>(Features.AppBar, Action.SetMethod, AppBarOptions.Apply))
                AccessInterface.SetFeature(Features.ConfirmationPopup, Action.Set, DecisionActions.Yes);
        }
        protected bool VerifyGammaValue(ColorOptions argColorOptions, DisplayType argDisplay, double argGammaValue)
        {
            Log.Message("Verifing gamma {0} value for {1} in display {2}", argGammaValue, argColorOptions, argDisplay);
            AccessInterface.Navigate(Features.SelectDisplay);
            AccessInterface.SetFeature(Features.SelectDisplay, Action.Set, argDisplay);
            AccessInterface.Navigate(Features.Gamma);
            AccessInterface.SetFeature<ColorOptions>(Features.Colour, Action.Set, argColorOptions);
            AccessInterface.SetFeature(Features.SelectDisplay, Action.Set, argDisplay);
            double valueReturned = AccessInterface.GetFeature<double>(Features.Gamma, Action.Get);
            if (valueReturned != argGammaValue)
            {
                Log.Fail("Value expected is {0}, but CUI shows {1}", argGammaValue, valueReturned);
                return false;
            }
            else
                return (valueReturned == argGammaValue);
        }
        protected void CheckConfigChange(DisplayConfig argInitialConfig)
        {
            List<DisplayInfo> _displayAfterPowerEvent = AccessInterface.GetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll, Source.AccessAPI);
            bool flagExists = false;
            foreach (DisplayType display in base.CurrentConfig.DisplayList)
            {
                flagExists = false;
                foreach (DisplayInfo displayInfo in _displayAfterPowerEvent)
                {
                    if (displayInfo.DisplayType == display)
                        flagExists = true;
                }
                if (flagExists == false)
                    Log.Abort("Display {0} does not exist after resuming from powerevent", display);
            }
            DisplayConfig DispConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            if (argInitialConfig.GetCurrentConfigStr().Equals(DispConfig.GetCurrentConfigStr()))
                Log.Message("No change in config");
            else
            {
                if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                    Log.Success("Config applied successfully");
                else
                {
                    base.ListEnumeratedDisplays();
                    Log.Abort("Config not applied!");
                }
            }
        }
    }
}