namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Xml.Linq;
    using System.Diagnostics;

    [Test(Type = TestType.WiDi)]
    class MP_SwitchableGraphics_IWD_Modes : MP_SwitchableGraphics_Base
    {
        private List<DisplayConfig> switchPatternList = new List<DisplayConfig>();
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            if (!base.CurrentConfig.EnumeratedDisplays.Any(DI => DI.DisplayType == DisplayType.WIDI))
            {
                if (!base.WiDiReConnect(true))
                    Log.Abort("Unable to connect");
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message("Get display switch pattern list");
            this.DisplaySwitch(switchPatternList);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Apply all possible modes");
            for (int index = 0; index < switchPatternList.Count; index++)
            {
                Log.Message(true, "Apply {0} config if all displays connected", base.GetConfigString(switchPatternList[index]));
                if (CheckConfigPossible(switchPatternList[index]))
                {
                    Log.Message("Applying {0}", base.GetConfigString(switchPatternList[index]));
                    this.SetNValidateConfig(switchPatternList[index]);
                    if (!base.GetAllModesForActiceDisplay(switchPatternList[index]).Count.Equals(0))
                    {
                        DisplayInfo currentDisplayInfo = null;
                        commonDisplayModeList.ForEach(dML =>
                        {
                            Log.Message(true, "Applying All modes for display {0}", dML.display.ToString());
                            DisplayConfig OSConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
                            Log.Verbose(OSConfig.GetCurrentConfigStr());
                            if (OSConfig.ConfigType != switchPatternList[index].ConfigType &&
                                OSConfig.PrimaryDisplay != switchPatternList[index].PrimaryDisplay &&
                                OSConfig.SecondaryDisplay != switchPatternList[index].SecondaryDisplay &&
                                OSConfig.TertiaryDisplay != switchPatternList[index].TertiaryDisplay)
                            {
                                Log.Fail("Configuration missmatch test config: {0} and current config: {1}", this.CurrentConfig.GetCurrentConfigStr(), OSConfig.GetCurrentConfigStr());
                                this.SetNValidateConfig(switchPatternList[index]);
                            }
                            currentDisplayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == dML.display).First();
                            dML.supportedModes.ForEach(dM => this.ApplyModeAndVerify(dM));
                        });
                    }
                    else
                    {
                        Log.Fail("Unable to find mode list");
                    }
                }
                else
                    continue;
            }
        }
        private void DisplaySwitch(List<DisplayConfig> argList)
        {
            Log.Verbose("Preparing Display Switch Pattern");
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = DisplayType.WIDI });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = DisplayType.WIDI, SecondaryDisplay = DisplayType.EDP, TertiaryDisplay = DisplayType.HDMI });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = DisplayType.EDP, SecondaryDisplay = DisplayType.WIDI, TertiaryDisplay = DisplayType.HDMI });
        }
        private bool CheckConfigPossible(DisplayConfig argConfig)
        {
            foreach (DisplayType dT in argConfig.CustomDisplayList)
                if (!base.CurrentConfig.EnumeratedDisplays.Any(DI => DI.DisplayType == dT))
                    return false;
            return true;
        }


    }
}
