namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Threading;
    using System.Collections.Generic;

    [Test(Type = TestType.HasReboot)]
    class MP_TDR_TestPanelFittingACPIHotkey : MP_TDR_Base
    {
        private DisplayInfo _displayInfo = null;
        private DisplayMode _currentMode;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public override void TestPreCondition()
        {
            if (!base.CurrentConfig.DisplayList.Contains(DisplayType.EDP))
                Log.Abort("This test runs only on EDP!");
            else
            {
                DisplayConfig displayConfigObj = new DisplayConfig();
                displayConfigObj.ConfigType = DisplayConfigType.SD;
                displayConfigObj.PrimaryDisplay = base.GetInternalDisplay();
                if(AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, displayConfigObj))
                    Log.Success("Config applied successfully");
                else
                    Log.Abort("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            List<ScalingOptions> scalingOptionList = ApplyNonNativeResolutionToEDP();
            PerformACPIf8(scalingOptionList, true);
        }
        [Test(Type = TestType.PostCondition, Order = 2)]
        public void PostCondition()
        {
            Log.Message(true, "TestCleanup:: Connect the displays planned in the grid");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                this.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }
        protected void PerformACPIf8(List<ScalingOptions> argScalingOptionList, bool argRetryFlag)
        {
            base.RunTDRNVerify(false);
            if (AccessInterface.SetFeature<bool, string>(Features.ACPIFunctions, Action.SetMethod, "F11"))
            {
                Log.Success("ACPI Switched successfull for dislay config {0} ", base.CurrentConfig.ToString());
            }
            else
            {
                Log.Fail("ACPI Switching Failed for the display config {0}", base.CurrentConfig.ToString());
            }
        }
        private ScalingOptions GetCurrentScaling()
        {
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == DisplayType.EDP).First();
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            return (ScalingOptions)actualMode.ScalingOptions.First();
        }
        protected List<ScalingOptions> ApplyNonNativeResolutionToEDP()
        {
            List<DisplayType> paramDispList = new List<DisplayType>() { base.GetInternalDisplay() };
            List<DisplayModeList> allMode = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, paramDispList);
            List<DisplayMode> edpSupportedModes = allMode.Where(dI => dI.display == base.GetInternalDisplay()).Select(dI => dI.supportedModes).FirstOrDefault();
            edpSupportedModes.Reverse();
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, edpSupportedModes.Last()))
                Log.Success("Mode applied Successfully");
            else
                Log.Fail(false, "Fail to apply Mode");

            List<ScalingOptions> scalingOptionList = new List<ScalingOptions>();
            scalingOptionList = edpSupportedModes.Last().ScalingOptions.Select(dI => (ScalingOptions)dI).ToList();
            return scalingOptionList;
        }
    }
}