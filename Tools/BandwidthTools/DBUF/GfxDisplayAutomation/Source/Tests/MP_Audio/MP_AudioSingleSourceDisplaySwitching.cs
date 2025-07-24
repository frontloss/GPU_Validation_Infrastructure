namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    class MP_AudioSingleSourceDisplaySwitching : MP_Audio_Base
    {
        #region Test

        private Dictionary<int, Action<List<DisplayConfig>>> _switchPatternList = null;

        [Test(Type = TestType.Method, Order = 1)]
        public void SetAudioSource()
        {
            base.SetAudioSource();
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void SetConfigMethod()
        {
            int bRet;
            int DispSwitch, Current_Config = 0, Pre_Config = 0, feature_Config = 0;
            bool SeqCheck = false;
            SeqCheck = base.IsPDBpresent();

            if (base.CurrentConfig.CustomDisplayList.Count == 1)
                Log.Abort("DisplaySwitch_OSPage test requires atleast 2 displays connected!");
            List<DisplayConfig> switchPatternList = new List<DisplayConfig>();
            int dispFetchKey = base.CurrentConfig.CustomDisplayList.Count;
            int dispByPlatform = base.MachineInfo.PlatformDetails.Platform.GetDisplaysCount();
            if (dispFetchKey > dispByPlatform)
                dispFetchKey = dispByPlatform;
            this.SwitchPatternList[dispFetchKey](switchPatternList);
            String x = base.CurrentConfig.ConfigType.ToString();
            Current_Config = base.Get_current_Config();


            switchPatternList.ForEach(dC =>
                {
                    feature_Config = 0;
                    if (true == SeqCheck)
                        base.StartLog();

                    Log.Message(true, "Switching to display config {0}", dC.GetCurrentConfigStr());
                    if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dC))
                    {
                        Log.Success("Switch successful to : {0}", dC.GetCurrentConfigStr());
                        Log.Message("Fetching Audio endpoint data");
                        if (true == SeqCheck)
                            base.StopLog();

                        if ((dC.PrimaryDisplay.ToString() == "HDMI") || (dC.PrimaryDisplay.ToString() == "DP"))
                        {
                            feature_Config++;
                        }
                        if ((dC.SecondaryDisplay.ToString() == "HDMI") || (dC.SecondaryDisplay.ToString() == "DP"))
                        {
                            feature_Config++;
                        }
                        if ((dC.TertiaryDisplay.ToString() == "HDMI") || (dC.TertiaryDisplay.ToString() == "DP"))
                        {
                            feature_Config++;
                        }
                        Pre_Config = Current_Config;
                        Current_Config = feature_Config;

                        base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));

                        if (true == SeqCheck)
                        {
                            if ((dC.ConfigType.ToString() == "eDP") && (dC.ConfigTypeCount.ToString() == "SD"))
                            {
                                if (PWR_Status.No_PWR_Change != base.VerifyPWRSequence())
                                    Log.Fail("PWR Sequence is wrong");
                                else
                                    Log.Success("PowerWELL sequence verified sucessfully");

                            }
                            VerifyAUDseq_DispSwitchEvent(Pre_Config, Current_Config);
                        }
                        Log.Verbose("Default audio endpoint device {0}", base.GetDefaultEndPoint().FriendlyName);
                    }
                    else
                        Log.Fail("Switch failed to : {0}", dC.GetCurrentConfigStr());
                });
        }

        private Dictionary<int, Action<List<DisplayConfig>>> SwitchPatternList
        {
            get
            {
                if (null == this._switchPatternList)
                {
                    this._switchPatternList = new Dictionary<int, Action<List<DisplayConfig>>>();
                    this._switchPatternList.Add(2, this.GetSwitchPatternForDualDisplayMode);
                    this._switchPatternList.Add(3, this.GetSwitchPatternForTriDisplayMode);
                }
                return this._switchPatternList;
            }
        }
        private void GetSwitchPatternForDualDisplayMode(List<DisplayConfig> argList)
        {
            Log.Verbose("Preparing Switch Pattern for DualDisplay Mode");
            DisplayConfig displayWrapper = null;

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay };
            argList.Add(displayWrapper);
        }
        private void GetSwitchPatternForTriDisplayMode(List<DisplayConfig> argList)
        {
            Log.Verbose("Preparing Switch Pattern for TriDisplay Mode");
            DisplayConfig displayWrapper = null;

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay, TertiaryDisplay = base.CurrentConfig.PrimaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay, TertiaryDisplay = base.CurrentConfig.PrimaryDisplay };
            argList.Add(displayWrapper);
        }

        #endregion
    }
}
