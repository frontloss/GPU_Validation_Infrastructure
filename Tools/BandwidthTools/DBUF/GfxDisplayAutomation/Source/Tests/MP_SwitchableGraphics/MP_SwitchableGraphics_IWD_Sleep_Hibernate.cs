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
    class MP_SwitchableGraphics_IWD_Sleep_Hibernate : MP_SwitchableGraphics_Base
    {
        private List<DisplayConfig> switchPatternList = new List<DisplayConfig>();
        PowerParams _powerParams = null;
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
            Log.Message(true, "Verify IWD is disconnected after resuming from Sleep");
            for (int index = 0; index < switchPatternList.Count; index++)
            {
                Log.Message(true, "Apply {0} config if all displays connected", base.GetConfigString(switchPatternList[index]));
                if (CheckConfigPossible(switchPatternList[index]))
                {
                    Log.Message("Applying {0}", base.GetConfigString(switchPatternList[index]));
                    base.SetNValidateConfig(switchPatternList[index]);
                    Log.Message("Put the system into {0} state & resume", PowerStates.S3);
                    this._powerParams = new PowerParams() { Delay = 30, };
                    base.InvokePowerEvent(this._powerParams, PowerStates.S3);
                    if (!base.IsWiDiConnected())
                    {
                        Log.Success("WiDi disconnected after resuming from {0}..verified using enumerated displays", PowerStates.S3);
                        if (!base.WiDiReConnect(true))
                            Log.Abort("Unable to connect");
                    }
                    else
                        Log.Fail("Widi still connected after resuming from {0}", PowerStates.S3);
                }
                else
                    continue;
            }
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Verify IWD is disconnected after resuming from Hibernate");
            for (int index = 0; index < switchPatternList.Count; index++)
            {
                Log.Message(true, "Apply {0} config if all displays connected", base.GetConfigString(switchPatternList[index]));
                if (CheckConfigPossible(switchPatternList[index]))
                {
                    Log.Message("Applying {0}", base.GetConfigString(switchPatternList[index]));
                    base.SetNValidateConfig(switchPatternList[index]);
                    Log.Message("Put the system into {0} state & resume", PowerStates.S4);
                    this._powerParams = new PowerParams() { Delay = 30, };
                    base.InvokePowerEvent(this._powerParams, PowerStates.S4);
                    if (!base.IsWiDiConnected())
                    {
                        Log.Success("WiDi disconnected after resuming from {0}", PowerStates.S4);
                        if (!base.WiDiReConnect(true))
                            Log.Abort("Unable to connect");
                    }
                    else
                        Log.Fail("Widi still connected after resuming from {0}", PowerStates.S4);
                }
                else
                    continue;
            }
        }
        private void DisplaySwitch(List<DisplayConfig> argList)
        {
            Log.Verbose("Preparing Display Switch Pattern");
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = DisplayType.WIDI });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = DisplayType.WIDI, SecondaryDisplay = DisplayType.DP });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = DisplayType.DP, SecondaryDisplay = DisplayType.EDP });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = DisplayType.DP, SecondaryDisplay = DisplayType.WIDI });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = DisplayType.WIDI, SecondaryDisplay = DisplayType.HDMI });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = DisplayType.EDP, SecondaryDisplay = DisplayType.DP, TertiaryDisplay = DisplayType.WIDI });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = DisplayType.EDP, SecondaryDisplay = DisplayType.WIDI, TertiaryDisplay = DisplayType.DP });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = DisplayType.CRT, SecondaryDisplay = DisplayType.EDP, TertiaryDisplay = DisplayType.WIDI });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = DisplayType.DP, SecondaryDisplay = DisplayType.EDP, TertiaryDisplay = DisplayType.WIDI });
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
