using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;
using System.Threading;
namespace Intel.VPG.Display.Automation
{
    class SB_Scaling_Smooth_CAR_Lock_S3_S4_Reboot : SB_Scaling_Smooth_CAR_basic
    {
        List<uint> xList = null;
        List<uint> yList = null;
        PowerParams powerParam = new PowerParams();

        DisplayScaling _scalingApplied = null;
        DisplayMode _modeApplied = new DisplayMode();
        [Test(Type = TestType.Method, Order = 1)]
        public override void TestStep1()
        {
            base.ApplyConfig(base.CurrentConfig);
            xList = new List<uint>() { 50 };
            yList = new List<uint>() { 50 };
            GetModeForScaling(ScalingOptions.Customize_Aspect_Ratio, base.CurrentConfig.PrimaryDisplay, xList, yList);

            PowerEvent(PowerStates.S3);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public virtual  void TestStep2()
        {
            VerifyPersistance(base.CurrentConfig.PrimaryDisplay,_scalingApplied,_modeApplied);

            xList = new List<uint>() { 100 };
            yList = new List<uint>() { 50 };
            GetModeForScaling(ScalingOptions.Customize_Aspect_Ratio, base.CurrentConfig.PrimaryDisplay, xList, yList);

            PowerEvent(PowerStates.S4);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep3()
        {
            VerifyPersistance(base.CurrentConfig.PrimaryDisplay, _scalingApplied, _modeApplied);

            xList = new List<uint>() { 0 };
            yList = new List<uint>() { 100 };
            GetModeForScaling(ScalingOptions.Customize_Aspect_Ratio, base.CurrentConfig.PrimaryDisplay, xList, yList);
        }

        public void VerifyPersistance(DisplayType argDisp,DisplayScaling argScalingApplied,DisplayMode argDispModeApplied)
        {
            Log.Message(true,"verify persistance");
            DisplayScaling curScale = AccessInterface.GetFeature<DisplayScaling, DisplayType>(Features.Scaling, Action.GetMethod, Source.AccessAPI,argDisp);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisp).First();
            DisplayMode curMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);

            if (curScale.Equals(argScalingApplied))
                Log.Success("Scaling {0} persister", argScalingApplied);
            else
                Log.Fail("Scaling switched from {0} to {1} after power event", argScalingApplied, curScale);

            if (curMode.GetCurrentModeStr(false).Equals(argDispModeApplied.GetCurrentModeStr(false)))
                Log.Success("Mode {0} persister after power event", curMode.GetCurrentModeStr(false));
            else
                Log.Fail("Mode switched from {0} to {1}", argDispModeApplied.GetCurrentModeStr(false), curMode.GetCurrentModeStr(false));
        }
        public void PowerEvent(PowerStates argPowerState)
        {
            Log.Message(true,"Invoke Power event {0}",argPowerState);
            _scalingApplied = AccessInterface.GetFeature<DisplayScaling, DisplayType>(Features.Scaling, Action.GetMethod, Source.AccessAPI, base.CurrentConfig.PrimaryDisplay);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == base.CurrentConfig.PrimaryDisplay).First();
            _modeApplied = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);


            powerParam.Delay = 30;
            powerParam.PowerStates = argPowerState;
            if (PowerStates.CS == argPowerState)
            {
                System.Diagnostics.Process.Start("rundll32.exe", "user32.dll,LockWorkStation");
                Thread.Sleep(5000);
                SendKeys.SendWait("{DOWN}"); //ctrl + esc  
            }
            else
            {
                base.InvokePowerEvent(powerParam, argPowerState);
            }
        }
    }
}
