using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_Config_S3_S4_Reboot_Scale_swap_HPD_overlay : SB_Config_Disp_Conf_Swap_Reboot_S4_CS_S3
    {
        protected List<DisplayConfig> _dispSwitchOrder = null;
        [Test(Type = TestType.Method, Order = 5)]
        public override void TestStep5()
        {
            //move cursor from one display to other display,if it is in extended config
            base.ApplyConfigOS(base.CurrentConfig);
            if (base.CurrentConfig.ConfigType == DisplayConfigType.ED || base.CurrentConfig.ConfigType == DisplayConfigType.TED)
            {
                for (int i = 0; i < 5; i++)
                {
                    base.CurrentConfig.DisplayList.ForEach(curDisp =>
                    {
                        DisplayHierarchy dh = base.GetDispHierarchy(base.CurrentConfig.CustomDisplayList, curDisp);
                        base.MoveCursor(dh, base.CurrentConfig, curDisp);
                        Thread.Sleep(1000);
                    });
                }
            }
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            //apply different resolution/scaling/RR on displays based on Config type mentioned in test
            int mid = 0;
            DisplayMode mode;
            ScalingOptions displayScaling = ScalingOptions.None;
            ScalingOptions curScalingOption = ScalingOptions.None;
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);
            allModeList.ForEach(curDisp =>
            {
                mid = curDisp.supportedModes.Count / 2;
                mode = curDisp.supportedModes.ElementAt(mid);
                if (base.CurrentConfig.ConfigType == DisplayConfigType.DDC)
                {
                    if (mode.display == base.CurrentConfig.PrimaryDisplay)
                    {
                        this.ApplyandVerifyMode(mode);
                        curScalingOption = AccessInterface.GetFeature<DisplayScaling, DisplayType>(Features.Scaling, Action.GetMethod, Source.AccessAPI, mode.display).scaling;
                        displayScaling = this.ApplyandVerifyScaling(mode, curScalingOption);
                    }
                    else if (mode.display == base.CurrentConfig.SecondaryDisplay)
                    {
                        mode = base.GetAppliedMode(curDisp.display);
                        displayScaling = this.ApplyandVerifyScaling(mode, displayScaling);
                        this.ApplyRRandVerify(mode, curDisp.supportedModes);
                    }
                }
                if (base.CurrentConfig.ConfigType == DisplayConfigType.ED)
                {
                    this.ApplyandVerifyMode(mode);
                    if (mode.display == base.CurrentConfig.PrimaryDisplay)
                    {
                        curScalingOption = AccessInterface.GetFeature<DisplayScaling, DisplayType>(Features.Scaling, Action.GetMethod, Source.AccessAPI, mode.display).scaling;       
                        displayScaling = this.ApplyandVerifyScaling(mode, curScalingOption);
                    }
                    else if (mode.display == base.CurrentConfig.SecondaryDisplay)
                    {
                        mode = base.GetAppliedMode(curDisp.display);
                        displayScaling = this.ApplyandVerifyScaling(mode, displayScaling);
                    }
                }
                if (base.CurrentConfig.ConfigType == DisplayConfigType.TDC)
                {

                    if (mode.display == base.CurrentConfig.PrimaryDisplay)
                        this.ApplyandVerifyMode(mode);
                    else if (mode.display == base.CurrentConfig.SecondaryDisplay)
                    {
                        mode = base.GetAppliedMode(curDisp.display);                        
                        this.ApplyRRandVerify(mode, curDisp.supportedModes);
                    }
                    else if (mode.display == base.CurrentConfig.TertiaryDisplay)
                    {
                        mode = base.GetAppliedMode(curDisp.display);                        
                        curScalingOption = AccessInterface.GetFeature<DisplayScaling, DisplayType>(Features.Scaling, Action.GetMethod, Source.AccessAPI, mode.display).scaling;
                        displayScaling = this.ApplyandVerifyScaling(mode, curScalingOption);
                    }
                }
                if (base.CurrentConfig.ConfigType == DisplayConfigType.TED)
                {                   
                    this.ApplyandVerifyMode(mode);
                    mode = base.GetAppliedMode(curDisp.display);                        
                    curScalingOption = AccessInterface.GetFeature<DisplayScaling, DisplayType>(Features.Scaling, Action.GetMethod, Source.AccessAPI, mode.display).scaling;
                    if (mode.display == base.CurrentConfig.PrimaryDisplay)
                        displayScaling = curScalingOption;
                    displayScaling = this.ApplyandVerifyScaling(mode, displayScaling);
                    this.ApplyRRandVerify(mode, curDisp.supportedModes);
                }
            });
            VerifyConfigOS(base.CurrentConfig);
        }
        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            //open overlay App, move from windowed mode to full screen mode and move from one display to other display.
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                DisplayHierarchy dh = base.GetDispHierarchy(base.CurrentConfig.CustomDisplayList, curDisp);
                base.PlayAndMoveVideo(dh, base.CurrentConfig);
                base.FullScreenVideo(dh, base.CurrentConfig);
                base.StopVideo(dh, base.CurrentConfig);
                VerifyConfigOS(base.CurrentConfig);
            });
        }
        [Test(Type = TestType.Method, Order = 8)]
        public virtual void TestStep8()
        {
            //TurnOff monitor for 1min and resume
            if (base.MachineInfo.PlatformDetails.IsLowpower)
            {
                Log.Alert("Monitor turn off/on will not work on CS enable system, Hence Skipping...");
            }
            else
            {
                Log.Message(true, "Turn off the monitor for 1 min & resume");
                MonitorTurnOffParam monitorTurnOffOnObject = new MonitorTurnOffParam()
                {
                    onOffParam = MonitorOnOff.OffOn,
                    waitingTime = 60
                };
                if (AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorTurnOffOnObject))
                    Log.Message(true, "Monitor turn Off and turn on successful");
                VerifyConfigOS(base.CurrentConfig);
            }
        }
        [Test(Type = TestType.Method, Order = 9)]
        public void TestStep9()
        {
            //If dual display config, swap primary and secondary and hotplug and unplug
            if (base.CurrentConfig.ConfigType == DisplayConfigType.DDC || base.CurrentConfig.ConfigType == DisplayConfigType.ED)
            {
                
                DisplayConfig config = new DisplayConfig()
                {
                    ConfigType = base.CurrentConfig.ConfigType,
                    PrimaryDisplay = base.CurrentConfig.SecondaryDisplay,
                    SecondaryDisplay = base.CurrentConfig.PrimaryDisplay
                };
                base.ApplyConfigOS(config);
                base.VerifyConfigOS(config);

                base.CurrentConfig.PluggableDisplayList.ForEach(curDisp =>
                {
                    base.HotUnPlug(curDisp);
                    Thread.Sleep(1000);
                    base.HotPlug(curDisp, _availableDisplays[curDisp]);
                    base.VerifyConfigOS(config);
                });                          
           }
        }
        [Test(Type = TestType.Method, Order = 10)]
        public void TestStep10()
        {
            //Apply different config for dual display config
            if (base.CurrentConfig.ConfigType == DisplayConfigType.DDC || base.CurrentConfig.ConfigType == DisplayConfigType.ED)
            {
                DisplaySwitch_2pipe();
                _dispSwitchOrder.ForEach(curConfig =>
                {
                    ApplyConfigOS(curConfig);
                    VerifyConfigOS(curConfig);
                });
            }
        }
        [Test(Type = TestType.Method, Order = 11)]
        public void TestStep11()
        {
            Log.Message(true, "Test clean up- Unplug all displays");
            base.UnPlugDisplays();
        }

        private void ApplyRRandVerify(DisplayMode mode, List<DisplayMode> dispModes)
        {

            DisplayMode applyDiffRR = dispModes.Where(dI => dI.HzRes == mode.HzRes && dI.VtRes == mode.VtRes && dI.RR != mode.RR).FirstOrDefault();
            if (applyDiffRR.HzRes == 0 || applyDiffRR.VtRes == 0 || applyDiffRR.RR == 0 || applyDiffRR.ScalingOptions.Count == 0 || applyDiffRR.Bpp == 0)
            {
                Log.Message(true, "No Different RR found for mode {0}", mode);
            }
            else
            {
                ApplyandVerifyMode(applyDiffRR);
            }
        }
        private void ApplyandVerifyMode(DisplayMode mode)
        {
            base.ApplyModeOS(mode, mode.display);
            base.VerifyConfigOS(base.CurrentConfig);
        }
        private ScalingOptions ApplyandVerifyScaling(DisplayMode mode,ScalingOptions otherDisplayScaling)
        {
            ScalingOptions appliedScaling = (ScalingOptions)mode.ScalingOptions.FirstOrDefault();
            bool isScalingApplied = false;
            mode.ScalingOptions.ForEach(scale =>
            {
                ScalingOptions scaleOption = (ScalingOptions)scale;               
                if (!scaleOption.Equals(otherDisplayScaling) && !isScalingApplied)
                {
                    DisplayScaling dsScaling = new DisplayScaling(mode.display, scaleOption);
                    AccessInterface.SetFeature<bool, DisplayScaling>(Features.Scaling, Action.SetMethod, dsScaling);
                    DisplayScaling curr_Scalling_SDK_Manager = AccessInterface.GetFeature<DisplayScaling, DisplayType>(Features.Scaling, Action.GetMethod, Source.AccessAPI, mode.display);
                    if (dsScaling.Equals(curr_Scalling_SDK_Manager))
                        Log.Success("Current Scalling : {0}  ------  Expected(Applied) Scalling : {1}", curr_Scalling_SDK_Manager.ToString(), dsScaling);
                    else
                        Log.Fail("Scalling Differ - Current Scalling from SDK Manager : {0} Expected(Applied) Scalling : {1}", curr_Scalling_SDK_Manager.ToString(), dsScaling);
                    base.VerifyConfigOS(base.CurrentConfig);
                    appliedScaling = scaleOption;
                    isScalingApplied = true;
                }
            });
            return appliedScaling;
        }
        public void DisplaySwitch_2pipe()
        {
            DisplayConfig dispSwitch1 = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay };
            DisplayConfig dispSwitch2 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay };
            DisplayConfig dispSwitch3 = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig dispSwitch4 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };           
            _dispSwitchOrder = new List<DisplayConfig>() { dispSwitch1, dispSwitch2, dispSwitch3, dispSwitch4 };
        }
    }
}
