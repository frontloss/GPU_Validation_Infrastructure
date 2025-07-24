namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

    [Test(Type = TestType.HasReboot)]
    class MP_CI_Gamma_S3 : TestBase
    {
        PowerParams _powerParams = null;
        private DisplayConfig _intialConfig = null;
        List<ColorOptions> listColorOptions = null;
        private Dictionary<ColorOptions, double> _colorGammaOptions = new Dictionary<ColorOptions, double>()
        {
            {ColorOptions.All, 1.0},
            {ColorOptions.Red,2.0},
            {ColorOptions.Green,4.0},
            {ColorOptions.Blue,5.0}
        };
        [Test(Type = TestType.Method, Order = 0)]
        public void TestStep0()
        {
            Log.Message(true, "Set config via OS call");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
            _intialConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message("Apply All possible Color Enhancement Value");
            if (!AccessInterface.SetFeature<bool, DecisionActions>(Features.LaunchCUI, Action.SetMethod, DecisionActions.No))
                Log.Abort("Unable to launch CUI");
            AccessInterface.Navigate(Features.SelectDisplay);
            ColorOptions[] colorOptionArray = (ColorOptions[])Enum.GetValues(typeof(ColorOptions));
            listColorOptions = colorOptionArray.ToList();
            foreach (ColorOptions colorOptions in listColorOptions)
            {
                foreach (DisplayType display in base.CurrentConfig.DisplayList)
                {
                    ApplyColorChange(colorOptions, display);
                }
                Log.Message(true, "Put the system into {0} state & resume", PowerStates.S3);
                this._powerParams = new PowerParams() { Delay = 30, };
                base.InvokePowerEvent(this._powerParams, PowerStates.S3);
                this.CheckConfigChange(_intialConfig);
                Log.Message(true, "Verify that gamma values are unchanged after resuming from {0}", PowerStates.S3);
                foreach (DisplayType display in base.CurrentConfig.DisplayList)
                {
                    VerifyAfterPowerEvent(colorOptions, display, " after S3");
                }
            }
        }
        [Test(Type = TestType.PostCondition, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Make the Gamma values default for all Displays");
            foreach (DisplayType display in base.CurrentConfig.DisplayList)
            {
                Log.Message("Making Gamma value default for {0}", display);
                AccessInterface.SetFeature(Features.SelectDisplay, Action.Set, display);
                AccessInterface.SetFeature<bool, AppBarOptions>(Features.AppBar, Action.SetMethod, AppBarOptions.RestoreDefault);
                if (AccessInterface.SetFeature<bool, AppBarOptions>(Features.AppBar, Action.SetMethod, AppBarOptions.Apply))
                    AccessInterface.SetFeature(Features.ConfirmationPopup, Action.Set, DecisionActions.Yes);
            }
        }
        [Test(Type = TestType.PostCondition, Order = 3)]
        public void TestStep3()
        {
            AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
        }
        private void ApplyColorChange(ColorOptions currentColorOption, DisplayType display)
        {
            double valueAdded = (double)GetHierarchyValue(base.CurrentConfig.DisplayList, display);
            if (currentColorOption == ColorOptions.Blue || currentColorOption == ColorOptions.Green)
                valueAdded = 0 - valueAdded;
            Log.Message("Apply gamma value {0} for {1} on display {2}", _colorGammaOptions[currentColorOption] + valueAdded, currentColorOption, display);
            this.ApplyGammaValue(currentColorOption, display, _colorGammaOptions[currentColorOption] + valueAdded);
            if (this.VerifyGammaValue(currentColorOption, display, _colorGammaOptions[currentColorOption] + valueAdded))
                Log.Success("The Gamma value {0} has been applied and verified for {1} on display {2}", _colorGammaOptions[currentColorOption] + valueAdded, currentColorOption, display);
        }
        private void VerifyAfterPowerEvent(ColorOptions currentColorOption, DisplayType display, string afterEvent)
        {
            double valueAdded = (double)GetHierarchyValue(base.CurrentConfig.DisplayList, display);
            if (currentColorOption == ColorOptions.Blue || currentColorOption == ColorOptions.Green)
                valueAdded = 0 - valueAdded;
            if (this.VerifyGammaValue(currentColorOption, display, _colorGammaOptions[currentColorOption] + valueAdded))
                Log.Success("The Gamma value {0} have verified for {1} after {2} on display {3}", _colorGammaOptions[currentColorOption] + valueAdded, currentColorOption, afterEvent, display);
        }
        private int GetHierarchyValue(List<DisplayType> argCustomDisplayList, DisplayType argDisplayType)
        {
            int index = argCustomDisplayList.FindIndex(dT => dT != DisplayType.None && dT == argDisplayType);
            return index;
        }
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
        private void CheckConfigChange(DisplayConfig argInitialConfig)
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
