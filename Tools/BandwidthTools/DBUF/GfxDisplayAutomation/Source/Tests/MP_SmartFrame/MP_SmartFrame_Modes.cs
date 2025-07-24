namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Collections.Generic;

    [Test(Type = TestType.HasReboot)]
    class MP_SmartFrame_Modes : MP_SmartFrame_Base
    {
        private List<DisplayMode> minMaxInter = new List<DisplayMode>();

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            Log.Message(true, "Set config SD {0} via OS", base.GetInternalDisplay());
            DisplayConfig config = new DisplayConfig();
            config.ConfigType = DisplayConfigType.SD;
            config.PrimaryDisplay = base.GetInternalDisplay();
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, config))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
            Log.Message(true, "Get min, max and intermediate Modes for SD {0}", base.GetInternalDisplay());
            List<DisplayType> paramDispList = new List<DisplayType>() { base.GetInternalDisplay() };
            List<DisplayModeList> allMode = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, paramDispList);
            List<DisplayMode> edpSupportedModes = allMode.Where(dI => dI.display == base.GetInternalDisplay()).Select(dI => dI.supportedModes).FirstOrDefault();
            if (edpSupportedModes.Count() > 0)
            {
                minMaxInter.Add(edpSupportedModes.First());
                minMaxInter.Add(edpSupportedModes[edpSupportedModes.Count / 2]);
                minMaxInter.Add(edpSupportedModes.Last());
            }
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {

            Log.Message(true, "Apply Max Resolution");
            bool result = AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, minMaxInter.Last());
            Log.Message(true, "Enable Smart Frame");
            base.EnableRegistryForSF();
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            base.EnableSF();
            base.VerifySmartFrameStatus(true, SmartFrameRegistryEvent);
            this.VerifyResolutionPersistance(minMaxInter.Last());
            foreach (DisplayMode mode in minMaxInter)
            {
                Log.Message(true, "Apply {0}x{1}, {2} RR, {3} Bpp", mode.HzRes, mode.VtRes, mode.RR, mode.Bpp);
                bool result = AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, mode);
                base.VerifySmartFrameStatus(true, SmartFrameRegistryEvent);
                this.VerifyResolutionPersistance(mode);
                Log.Message(true, "Disable Smart Frame");
                base.DisableSF();
                base.VerifySmartFrameStatus(false, SmartFrameRegistryEvent);
                this.VerifyResolutionPersistance(mode);
                base.EnableSF();
            }
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Disable Smart Frame");
            base.DisableSF();
            base.DisableRegistryForSF();
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            base.VerifySmartFrameStatus(false, SmartFrameRegistryEvent);
        }
        private void VerifyResolutionPersistance(DisplayMode argMode)
        {
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == base.GetInternalDisplay()).First();
            DisplayMode currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            if ((currentMode.HzRes == argMode.HzRes) && (currentMode.VtRes == argMode.VtRes))
                Log.Success("Resolution is persisting after enabling SmartFrame");
            else
                Log.Fail("Resolution not persisting, expected resolution {0}x{1}, actual resolution {2}x{3}", argMode.HzRes, argMode.VtRes, currentMode.HzRes, currentMode.VtRes);
        }
    }
}