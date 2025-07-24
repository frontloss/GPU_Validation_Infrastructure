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
    class MP_SwitchableGraphics_IWD_HDCP_Modes : MP_SwitchableGraphics_Base
    {
        private List<DisplayConfig> switchPatternList = new List<DisplayConfig>();
        private Dictionary<DisplayType, string> _myDictionary = null;
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Remove all instances of OPM tester in binary");
            string[] directories = Directory.GetDirectories(Directory.GetCurrentDirectory(), "OPM*");
            foreach (string dir in directories)
            {
                string[] files = Directory.GetFiles(dir);
                foreach (string g in files)
                {
                    File.SetAttributes(g, FileAttributes.Normal);
                    Thread.Sleep(1000);
                    File.Delete(g);
                }
                Directory.Delete(dir);
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            if (!base.CurrentConfig.EnumeratedDisplays.Any(DI => DI.DisplayType == DisplayType.WIDI))
            {
                if (!base.WiDiReConnect(true))
                    Log.Abort("Unable to connect");
            }
            this._myDictionary = new Dictionary<DisplayType, string>()
            {
                 { DisplayType.EDP,"SetProtectionHDCP Failed to set HDCP" },
                 { DisplayType.CRT,"SetProtectionHDCP Failed to set HDCP" },
                 { DisplayType.HDMI,"SetProtection HDCP succeeded" },
                 { DisplayType.DP,"SetProtection HDCP succeeded" },
                 {DisplayType.WIDI, "SetProtection HDCP succeeded"}
            };
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message("Get display switch pattern list");
            this.DisplaySwitch(switchPatternList);
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            for (int index = 0; index < switchPatternList.Count; index++)
            {
                Log.Message(true, "Apply {0} config if all displays connected", base.GetConfigString(switchPatternList[index]));
                if (CheckConfigPossible(switchPatternList[index]))
                {
                    Log.Message("Applying {0}", base.GetConfigString(switchPatternList[index]));
                    this.SetNValidateConfig(switchPatternList[index]);
                    if (!base.GetAllModesForActiceDisplay(switchPatternList[index]).Count.Equals(0))
                    {
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
                            dML.supportedModes.ForEach(dM =>
                            {
                                this.ApplyModeAndVerify(dM);
                                foreach (DisplayType dT in switchPatternList[index].CustomDisplayList)
                                {
                                    DisplayHierarchy dH = GetDispHierarchy(switchPatternList[index].CustomDisplayList, dT);
                                    Log.Message(true, "Run OPM Tester and choose Activate HDCP from menu");
                                    HDCPParams hdcpParams = new HDCPParams()
                                    {
                                        HDCPPlayerInstance = HDCPPlayerInstance.Player_1,
                                        HDCPOptions = HDCPOptions.ActivateHDCP,
                                        HDCPApplication = HDCPApplication.OPMTester,
                                        DisplayHierarchy = dH,
                                        CurrentConfig = switchPatternList[index]
                                    };
                                    AccessInterface.SetFeature<HDCPParams>(Features.HDCP, Action.Set, hdcpParams);
                                    base.VerifyProtectionHDCP(dT, "ON",1, _myDictionary);
                                    hdcpParams.HDCPOptions = HDCPOptions.Close;
                                    AccessInterface.SetFeature<HDCPParams>(Features.HDCP, Action.Set, hdcpParams);
                                    Log.Message(true, "Run OPM Tester and choose Deactivate HDCP from menu");
                                    hdcpParams.HDCPOptions = HDCPOptions.DeactivateHDCP;
                                    AccessInterface.SetFeature<HDCPParams>(Features.HDCP, Action.Set, hdcpParams);
                                    base.VerifyProtectionHDCP(dT, "OFF", 0,_myDictionary);
                                    if (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
                                        break;
                                }
                            });
                            Log.Message(true, "Run OPM tester and activate HDCP on each display");

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
       //     argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = DisplayType.WIDI, SecondaryDisplay = DisplayType.EDP });
            //argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = DisplayType.WIDI, SecondaryDisplay = DisplayType.EDP, TertiaryDisplay = DisplayType.DP });        
            //argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = DisplayType.EDP, SecondaryDisplay = DisplayType.WIDI, TertiaryDisplay = DisplayType.HDMI });
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
