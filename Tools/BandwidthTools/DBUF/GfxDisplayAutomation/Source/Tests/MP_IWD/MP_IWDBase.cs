namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;

    [Test(Type = TestType.WiDi)]
    public class MP_IWDBase : TestBase
    {
        protected List<DisplayConfig> switchPatternList = new List<DisplayConfig>();
        protected List<DisplayModeList> commonDisplayModeList = new List<DisplayModeList>();
        private DisplayType _displayType = DisplayType.None;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            if (!base.CurrentConfig.EnumeratedDisplays.Any(DI => DI.DisplayType == DisplayType.WIDI))
            {
                Log.Alert("WiDi Display not enumerated try to reconnect to run the test");
                if (!WiDiReConnect())
                    Log.Abort("Unable to connect");
            }
        }

        internal bool WiDiReConnect()
        {
            Log.Verbose("Verify EDP/MIPI/CRT is connected ");
            this._displayType = base.CurrentConfig.DisplayList.FirstOrDefault(dT => (dT == DisplayType.EDP || dT == DisplayType.MIPI || dT == DisplayType.CRT));
            if (this._displayType != DisplayType.None)
                Log.Message("{0} is connected..test continues", this._displayType);
            else
                Log.Abort("EDP/MIPI/CRT is not connected..Aborting the test");
            Log.Message("Set the initial configuration as SD {0}", this._displayType);
            DisplayConfig displayConfig = new DisplayConfig();
            displayConfig.ConfigType = DisplayConfigType.SD;
            displayConfig.PrimaryDisplay = this._displayType;
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, displayConfig))
                Log.Message("Config (SD {0}) applied successfully", this._displayType);
            else
                Log.Abort("Config (SD {0}) not applied!", this._displayType);
            if (AccessInterface.SetFeature<bool>(Features.WiDiDisplayConnection, Action.SetNoArgs))
            {
                List<DisplayInfo> currentDisplayEnum = base.CurrentConfig.EnumeratedDisplays;
                List<DisplayInfo> enumeratedDisplay = AccessInterface.SetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);
                List<uint> winMonIDList = AccessInterface.GetFeature<List<uint>>(Features.WindowsMonitorID, Action.GetAll);
                List<uint> currentWinMonIDList = base.CurrentConfig.EnumeratedDisplays.Where(dI => !dI.WindowsMonitorID.Equals(0)).Select(dI => dI.WindowsMonitorID).ToList();
                List<uint> diffMonitorIdList = winMonIDList.Except(currentWinMonIDList).ToList();
                if (enumeratedDisplay.Count > currentDisplayEnum.Count)
                {
                    base.CurrentConfig.EnumeratedDisplays.Clear();
                    base.CurrentConfig.EnumeratedDisplays.AddRange(enumeratedDisplay);
                }
                return true;
            }
            return false;
        }

        protected void GetTwoDisplaySwitchPattern(List<DisplayConfig> argList)
        {
            argList.Add(new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay });
        }

        protected void GetThreeDisplaySwitchingPattern(List<DisplayConfig> argList)
        {
            argList.Add(new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay, TertiaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay });
        }

        protected bool SetNValidateConfig(DisplayConfig argConfig)
        {
            try
            {
                if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argConfig))
                {
                    Log.Success("Switch successful to {0}", argConfig.GetCurrentConfigStr());
                    Log.Message("Set the maximum display mode on all the active displays");
                    return true;
                }
                else
                    Log.Abort("Config not applied!");
                return false;
            }
            catch
            {
                if (!WiDiReConnect())
                    CheckWiDiStatus();
                return false;
            }
        }

        protected List<DisplayModeList> GetAllModesForActiceDisplay()
        {
            if (commonDisplayModeList.Count != 0)
                return commonDisplayModeList;
            else
            {
                try
                {
                    Log.Verbose("Getting all suppored modes for all active display");
                    List<DisplayModeList> displayModeList_OSPage = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);
                    List<DisplayMode> commonModes = null;
                    if (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
                    {
                        commonModes = displayModeList_OSPage.Where(dML => dML.display == base.CurrentConfig.PrimaryDisplay).Select(dML => dML.supportedModes).FirstOrDefault();
                        displayModeList_OSPage.Skip(1).ToList().ForEach(dML => commonModes = commonModes.Intersect(dML.supportedModes, new DisplayMode()).ToList());
                        if (commonModes.Count() > 0)
                            commonDisplayModeList.Add(new DisplayModeList() { display = base.CurrentConfig.PrimaryDisplay, supportedModes = commonModes });
                    }
                    else
                        commonDisplayModeList = displayModeList_OSPage;
                }
                catch
                {
                    CheckWiDiStatus();
                }
                return commonDisplayModeList;
            }
        }

        protected List<DisplayMode> TestModes(List<DisplayMode> displayModeList)
        {
            List<DisplayMode> testModes = new List<DisplayMode>();
            testModes.Add(displayModeList.First());
            testModes.Add(displayModeList[displayModeList.Count / 2]);
            testModes.Add(displayModeList.Last());
            return testModes;
        }

        protected void ApplyAndVerify(DisplayMode argDispMode, DisplayInfo argDisplayInfo)
        {
            Log.Message("Setting Mode : {0} for {1}", GetModeStr(argDispMode), argDispMode.display);
            try
            {
                if (!AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argDispMode))
                    Log.Fail("Fail to apply Mode");
                else
                    Log.Success("Mode applied successfully");
            }
            catch
            {
                if (!WiDiReConnect())
                    CheckWiDiStatus();
            }
        }

        protected string GetModeStr(DisplayMode argMode)
        {
            return string.Concat(argMode.HzRes, "x", argMode.VtRes, "x", argMode.RR, argMode.InterlacedFlag.Equals(0) ? "p Hz" : "i Hz", "x", argMode.Bpp);
        }

        protected void CheckWiDiStatus()
        {
            List<uint> winMonitorIDList = base.ListEnumeratedDisplays();
            List<uint> enumeratedWinMonIDList = base.CurrentConfig.EnumeratedDisplays.Where(dI => !dI.WindowsMonitorID.Equals(0)).Select(dI => dI.WindowsMonitorID).ToList();
            if (!enumeratedWinMonIDList.Count.Equals(winMonitorIDList.Count))
            {
                Log.Fail(false, "Some displays are not enumerated! may WiDi connection drops");
                Log.Verbose("Currently enumerated display list [{0}] mismatch with windows monitor id list [{1}]! A reboot is required.", enumeratedWinMonIDList.Count, winMonitorIDList.Count);
                Log.Abort("!!!!!!!!!! Exiting from test execution !!!!!!!!!!");
            }
        }
    }
}
