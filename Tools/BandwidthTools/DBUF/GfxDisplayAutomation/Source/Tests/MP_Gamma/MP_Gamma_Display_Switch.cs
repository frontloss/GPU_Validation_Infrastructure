namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Text;
    using System.Linq;

    class MP_Gamma_Display_Switch : MP_Gamma_Base
    {
        private List<DisplayConfig> switchPatternList = new List<DisplayConfig>();
        private Dictionary<ColorOptions, double> _colorGammaOptions = new Dictionary<ColorOptions, double>()
        {
            {ColorOptions.All, 1.0},
            {ColorOptions.Red,2.0},
            {ColorOptions.Green,3.0},
            {ColorOptions.Blue,4.0}
        };
        private Dictionary<DisplayType, int> _displayOccuringIndex = new Dictionary<DisplayType, int>();
        List<DisplayType> _hasAppeared = new List<DisplayType>();
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            if (base.CurrentConfig.DisplayList.Count < 2)
                Log.Abort("This test requires atleast 2 displays connected!");
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Verbose("Get display switch pattern list");
            int dispFetchKey = base.CurrentConfig.CustomDisplayList.Count;
            int dispByPlatform = base.MachineInfo.PlatformDetails.Platform.GetDisplaysCount();
            if (dispFetchKey > dispByPlatform)
                dispFetchKey = dispByPlatform;
            if (dispFetchKey == 3)
                this.TriDisplaySwitch(switchPatternList);
            else
                this.DualDisplaySwitch(switchPatternList);
            foreach (DisplayType display in base.CurrentConfig.CustomDisplayList)
                _displayOccuringIndex.Add(display, 0);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            string setConfigStr = string.Empty;
            string currentConfigStr = string.Empty;
            double valueAdded;
            ColorOptions[] colorOptionArray = (ColorOptions[])Enum.GetValues(typeof(ColorOptions));
            List<ColorOptions> listColorOptions = colorOptionArray.ToList();
            if (!AccessInterface.SetFeature<bool, DecisionActions>(Features.LaunchCUI, Action.SetMethod, DecisionActions.No))
                Log.Abort("Unable to launch CUI");
            AccessInterface.Navigate(Features.SelectDisplay);
            UpdateHasAppearedList(switchPatternList[0]);
            for (int index = 0; index < switchPatternList.Count; index++)
            {
                Log.Message(true, "Apply {0} config", this.GetConfigString(switchPatternList[index]));
                if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, switchPatternList[index]))
                {
                    DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
                    setConfigStr = this.GetConfigString(switchPatternList[index]);
                    currentConfigStr = this.GetConfigString(currentConfig);
                    if (setConfigStr.Equals(currentConfigStr))
                    {
                        Log.Success("Switch successful to {0}", setConfigStr);
                        Log.Message("Verify gamma Value");
                        if (index == 1)
                        {
                            foreach (DisplayType display in switchPatternList[index].CustomDisplayList)
                            {
                                if (!(NewDisplay(display)))
                                {
                                    valueAdded = (double)GetHierarchyValue(base.CurrentConfig.DisplayList, display);
                                    foreach (ColorOptions colorOptions in listColorOptions.Skip(1))
                                    {
                                        if (base.VerifyGammaValue(colorOptions, display, _colorGammaOptions[colorOptions] + valueAdded))
                                            Log.Success("The Gamma value {0} has been applied and verified for {1} in display {2}", _colorGammaOptions[colorOptions] + valueAdded, colorOptions, display);
                                    }
                                }
                                else
                                {
                                    foreach (ColorOptions colorOptions in listColorOptions.Skip(1))
                                    {
                                        if (base.VerifyGammaValue(colorOptions, display, 1.0))
                                            Log.Success("The Gamma value {0} has been applied and verified for {1} in display {2}", 1.0, colorOptions, display);
                                    }
                                }
                            }
                        }
                        if (index > 1)
                        {
                            foreach (DisplayType display in switchPatternList[index].CustomDisplayList)
                            {
                                int indexOfDisplay = GetDisplayIndex(display);
                                valueAdded = (double)GetHierarchyValue(base.CurrentConfig.DisplayList, display);
                                if (base.VerifyGammaValue(ColorOptions.All, display, _colorGammaOptions[ColorOptions.All] + valueAdded))
                                    Log.Success("The Gamma value {0} has been verified for {1} in display {2}", _colorGammaOptions[ColorOptions.All] + valueAdded, ColorOptions.All, display);
                            }
                        }
                        Log.Message("Change the Gamma Value");
                        if (index == 0)
                        {
                            Log.Verbose("Change the Red, Green and Blue values");
                            foreach (DisplayType display in switchPatternList[index].CustomDisplayList)
                            {
                                valueAdded = (double)GetHierarchyValue(base.CurrentConfig.DisplayList, display);
                                foreach (ColorOptions colorOptions in listColorOptions.Skip(1))
                                {
                                    base.ApplyGammaValue(colorOptions, display, _colorGammaOptions[colorOptions] + valueAdded);
                                    if (base.VerifyGammaValue(colorOptions, display, _colorGammaOptions[colorOptions] + valueAdded))
                                        Log.Success("The Gamma value {0} has been applied and verified for {1} in display {2}", _colorGammaOptions[colorOptions] + valueAdded, colorOptions, display);
                                }
                                //AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
                                foreach (ColorOptions colorOptions in listColorOptions.Skip(1))
                                {
                                    if (base.VerifyGammaValue(colorOptions, display, _colorGammaOptions[colorOptions] + valueAdded))
                                        Log.Success("The Gamma value {0} has been applied and verified for {1} in display {2}", _colorGammaOptions[colorOptions] + valueAdded, colorOptions, display);
                                }
                            }
                            continue;
                        }
                        else
                        {
                            Log.Verbose("Change the All Colour Value");
                            foreach (DisplayType display in switchPatternList[index].CustomDisplayList)
                            {
                                valueAdded = (double)GetHierarchyValue(base.CurrentConfig.DisplayList, display);
                                base.ApplyGammaValue(ColorOptions.All, display, _colorGammaOptions[ColorOptions.All] + valueAdded);
                                if (base.VerifyGammaValue(ColorOptions.All, display, _colorGammaOptions[ColorOptions.All] + valueAdded))
                                    Log.Success("The Gamma value {0} has been applied and verified for {1} in display {2}", _colorGammaOptions[ColorOptions.All] + valueAdded, ColorOptions.All, display);
                            }
                        }
                    }
                    else
                        Log.Fail("Switch unsuccessful, Expected Config = {0} but config aplied is {1} ", setConfigStr, currentConfigStr);
                }
                UpdateHasAppearedList(switchPatternList[index]);
                UpdateDisplayOccuringIndex(switchPatternList[index], index);
            }
            AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Set the initial config Back and  Make the Gamma values default for all Displays");

            foreach (DisplayType display in base.CurrentConfig.CustomDisplayList)
            {
                DisplayConfig displayConfig = new DisplayConfig()
                {
                    ConfigType = DisplayConfigType.SD,
                    PrimaryDisplay = display
                };
                if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, displayConfig))
                    Log.Success("Config applied successfully");
                if (!AccessInterface.SetFeature<bool, DecisionActions>(Features.LaunchCUI, Action.SetMethod, DecisionActions.No))
                    Log.Abort("Unable to launch CUI");
                AccessInterface.Navigate(Features.SelectDisplay);
                AccessInterface.SetFeature(Features.SelectDisplay, Action.Set, display);
                AccessInterface.SetFeature<bool, AppBarOptions>(Features.AppBar, Action.SetMethod, AppBarOptions.RestoreDefault);
                if (AccessInterface.SetFeature<bool, AppBarOptions>(Features.AppBar, Action.SetMethod, AppBarOptions.Apply))
                    AccessInterface.SetFeature(Features.ConfirmationPopup, Action.Set, DecisionActions.Yes);
                AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
            }
        }
        [Test(Type = TestType.PostCondition, Order = 4)]
        public void TestStep4()
        {
            AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
        }
        private void UpdateHasAppearedList(DisplayConfig argConfig)
        {
            foreach (DisplayType display in argConfig.CustomDisplayList)
                if (!(_hasAppeared.Contains(display)))
                    _hasAppeared.Add(display);
        }
        private void UpdateDisplayOccuringIndex(DisplayConfig argConfig, int argIndex)
        {
            foreach (DisplayType display in argConfig.CustomDisplayList)
                _displayOccuringIndex[display] = argIndex;
        }
        private int GetDisplayIndex(DisplayType argDisplay)
        {
            return _displayOccuringIndex[argDisplay];
        }
        private int GetHierarchyValue(List<DisplayType> argCustomDisplayList, DisplayType argDisplayType)
        {
            int index = argCustomDisplayList.FindIndex(dT => dT != DisplayType.None && dT == argDisplayType);
            return index;
        }
        private bool NewDisplay(DisplayType argdisplay)
        {
            if (!(_hasAppeared.Contains(argdisplay)))
                return true;
            else
                return false;
        }
        private void DualDisplaySwitch(List<DisplayConfig> argList)
        {
            Log.Verbose("Preparing Switch Pattern for Single & DualClone");
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay });
        }
        private void TriDisplaySwitch(List<DisplayConfig> argList)
        {
            Log.Verbose("Preparing Switch Pattern for Single, DualExtended & TriExtended");
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay });
        }
        private string GetConfigString(DisplayConfig argConfig)
        {
            StringBuilder sb = new StringBuilder(argConfig.ConfigType.ToString()).Append(" ");
            sb.Append(argConfig.PrimaryDisplay.ToString()).Append(" ");
            if (argConfig.SecondaryDisplay != DisplayType.None)
                sb.Append(argConfig.SecondaryDisplay.ToString()).Append(" ");
            if (argConfig.TertiaryDisplay != DisplayType.None)
                sb.Append(argConfig.TertiaryDisplay.ToString()).Append(" ");
            return sb.ToString();
        }
    }
}
