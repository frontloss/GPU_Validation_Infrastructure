namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;

    class MP_Gamma_Timer_Hot_Plug : MP_Gamma_Base
    {
        private Dictionary<ColorOptions, double> _colorGammaOptions = new Dictionary<ColorOptions, double>()
        {
            {ColorOptions.All,1.0},
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
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message("Apply All possible Color Enhancement Value");
            if (!AccessInterface.SetFeature<bool, DecisionActions>(Features.LaunchCUI, Action.SetMethod, DecisionActions.No))
                Log.Abort("Unable to launch CUI");
            AccessInterface.Navigate(Features.SelectDisplay);
            foreach (ColorOptions colorOptions in Enum.GetValues(typeof(ColorOptions)))
            {
                foreach (DisplayType display in base.CurrentConfig.DisplayList)
                {
                    double valueAdded = (double)GetHierarchyValue(base.CurrentConfig.DisplayList, display);
                    if (colorOptions == ColorOptions.Blue || colorOptions == ColorOptions.Green)
                        valueAdded = 0 - valueAdded;
                    Log.Message("Apply gamma value {0} for {1} on display {2}", _colorGammaOptions[colorOptions] + valueAdded, colorOptions, display);
                    base.ApplyGammaValue(colorOptions, display, _colorGammaOptions[colorOptions] + valueAdded);
                    if (base.VerifyGammaValue(colorOptions, display, _colorGammaOptions[colorOptions] + valueAdded))
                        Log.Success("The Gamma value {0} has been applied and verified for {1} on display {2}", _colorGammaOptions[colorOptions] + valueAdded, colorOptions, display);
                }
                Log.Message(true, "Turn off the monitor for 1 min & resume");
                MonitorTurnOffParam monitorOnOffParam = new MonitorTurnOffParam();
                monitorOnOffParam.onOffParam = MonitorOnOff.OffOn;
                monitorOnOffParam.waitingTime = 60;
                if (AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorOnOffParam))
                {
                    Log.Message(true, "Verify that gamma values are unchanged after resuming from monitor turn off");
                    foreach (DisplayType display in base.CurrentConfig.DisplayList)
                    {
                        double valueAdded = (double)GetHierarchyValue(base.CurrentConfig.DisplayList, display);
                        if (colorOptions == ColorOptions.Blue || colorOptions == ColorOptions.Green)
                            valueAdded = 0 - valueAdded;
                        if (base.VerifyGammaValue(colorOptions, display, _colorGammaOptions[colorOptions] + valueAdded))
                            Log.Success("The Gamma value {0} have verified for {1} after resuming from Monitor Turn Off on display {2}", _colorGammaOptions[colorOptions] + valueAdded, colorOptions, display);
                    }
                }
                else
                    Log.Fail("Error in Turning off the monitor.");
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
        private int GetHierarchyValue(List<DisplayType> argCustomDisplayList, DisplayType argDisplayType)
        {
            int index = argCustomDisplayList.FindIndex(dT => dT != DisplayType.None && dT == argDisplayType);
            return index;
        }
    }
}
