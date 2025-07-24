namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Windows.Forms;
    using System.Collections.Generic;

    class MP_Rotation_OSPage_S3 : MP_Rotation_Basic
    {
       List<uint> _cloneRotation=new List<uint>(){ 90, 180, 270, 0 };
       List<List<uint>> _extendedRotationSequence = new List<List<uint>>(){ { new List<uint>(){180, 270, 0}}, 
                                                    {new  List<uint>(){ 90, 0, 270}}
                                                    };
        protected PowerStates _powerStateOption;
        int _retry = 0;

        public MP_Rotation_OSPage_S3()
        {
            _powerStateOption = PowerStates.S3;
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void SetConfigMethod()
        {
            base.ApplyConfig(base.CurrentConfig);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void PowerEvent()
        {
            //Log.Message(true, "Switch to AC Power Source");
            //if (AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get, Source.AccessAPI) == PowerLineStatus.Online || 
            //    AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
            //    Log.Success("System is in AC power mode");
            //else
            //    Log.Fail("Switch to AC power option failed");
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void RotationMethod()
        {
            curAppliedConfig = base.CurrentConfig;
            if (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Extended)
            {
                _extendedRotationSequence.ForEach(curAngle =>
                    {
                        base._angle = new List<uint>();
                        for (int i=0;i<base.CurrentConfig.DisplayList.Count();i++)
                        {
                           uint angle= curAngle.ElementAt(i);
                            base._angle.Add(angle);
                        }                       
                        ApplyNonNative();
                        base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();
                        SwitchToPowerEvent();
                    });                
            }
            else
            {
              _cloneRotation.ForEach(curAngle=>
                  {
                      base._angle = new List<uint>() {curAngle };
                        ApplyNonNative();
                        base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();
                        SwitchToPowerEvent();
                  });
            }
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void CleanUp()
        {
            //this.CloseCUI();
            AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig);
            if (AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get, Source.AccessAPI) != PowerLineStatus.Online)
                AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5);
        }

        private List<DisplayMode> TestModes(List<DisplayMode> displayModeList)
        {
            List<DisplayMode> testModes = new List<DisplayMode>();
            testModes.Add(displayModeList.First());
            testModes.Add(displayModeList[displayModeList.Count / 2]);
            testModes.Add(displayModeList.Last());
            return testModes;
        }

        private DisplayMode VerifyRotation(DisplayType argDisplay, DisplayMode argSetMode)
        {
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplay).First();
            DisplayMode currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            if (currentMode.CanFlip())
            {
                uint temp = currentMode.HzRes;
                currentMode.HzRes = currentMode.VtRes;
                currentMode.VtRes = temp;
            }
            return currentMode;
        }
        private void SwitchToPowerEvent()
        {
            DisplayConfig displayConfigBeforePowerEvent = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            PowerParams powerParam = new PowerParams() { Delay = 30, PowerStates = _powerStateOption };
            if (AccessInterface.SetFeature<bool, PowerParams>(Features.PowerEvent, Action.SetMethod, powerParam))
                Log.Success("{0} completed successfully", powerParam.PowerStates);
            else
                Log.Fail("{0} power state event failed !! ", powerParam.PowerStates);

            DisplayConfig displayConfigAfterPowerEvent = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            if (displayConfigBeforePowerEvent.GetCurrentConfigStr().CompareTo(displayConfigAfterPowerEvent.GetCurrentConfigStr())!=0)
            {
                Log.Fail("Display Config {0} after power event {1} - is {2}", displayConfigBeforePowerEvent.GetCurrentConfigStr(), _powerStateOption, displayConfigAfterPowerEvent.GetCurrentConfigStr());
            }
            else
                Log.Success("Display Config retained after power event {0} - {1}", _powerStateOption, displayConfigAfterPowerEvent.GetCurrentConfigStr());

            int i = 0;
            base._angle.ForEach(curAngle =>
                {
                    DisplayType disp= curAppliedConfig.DisplayList.ElementAt(i);
                    DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == disp).First();
                    DisplayMode currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
                    if (currentMode.Angle == curAngle)
                        Log.Success("{0} has persisted the angle {1} after {2}", disp, curAngle, _powerStateOption);
                    else
                        Log.Fail("{0} has not persisted the angle {1} after {2} , current angle {3}",disp,curAngle,_powerStateOption,currentMode.Angle);
                    i++;
                });           
        }
        private void SwitchtoOthePowerSource()
        {
            if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                Log.Success("Switch to other power source (AC/DC) Success");
            else
                Log.Fail("Switch to other power mode (AC/DC) failed!");
        }
       
    }
}
