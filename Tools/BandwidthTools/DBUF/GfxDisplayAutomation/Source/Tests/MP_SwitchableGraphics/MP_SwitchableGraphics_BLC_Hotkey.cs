namespace Intel.VPG.Display.Automation
{
    using System.Windows.Forms;
    using System.Collections.Generic;
    using System.Threading;
    using System.Linq;
    using System;

    class MP_SwitchableGraphics_BLC_Hotkey : MP_SwitchableGraphics_Base
    {
        PowerParams _powerParams = null;

        [Test(Type = TestType.PreCondition, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Check if EDP is connected to the system");
            if (!(base.CurrentConfig.EnumeratedDisplays.Any(dI => dI.DisplayType == DisplayType.EDP)))
            {
                Log.Abort("EDP has to be connected to system");
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Enable AC Mode");
            PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);
            if (powerState == PowerLineStatus.Offline)
            {
                if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                    Log.Success("System is Running in AC Mode");
                else
                    Log.Fail("Fail to set AC mode");
            }
            else
                Log.Success("System is Running in AC Mode");
            LaunchCUIAndSetConfig();
            int brightnessB4Changing = base.CurrentMonitorBrightness();
            ChangeBrightness("Decrease", "F9");
            int difference = VerifyChangeInBrightness(brightnessB4Changing);
            if (difference < 0)
                Log.Success("Brightness has been decreased");
            else
                Log.Fail("Brightness has not decreased");
            brightnessB4Changing = base.CurrentMonitorBrightness();
            ChangeBrightness("Increase", "F10");
            difference = VerifyChangeInBrightness(brightnessB4Changing);
            if (difference > 0)
                Log.Success("Brightness has been increased");
            else
                Log.Fail("Brightness has not increased");
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Enable DC Mode");
            PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);

            if (powerState == PowerLineStatus.Online)
            {
                if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                    Log.Success("System is Running in DC Mode");
                else
                    Log.Fail("Fail to set DC Mode");
            }
            else
                Log.Success("System is Running in DC Mode");
            LaunchCUIAndSetConfig();
            int brightnessB4Changing = base.CurrentMonitorBrightness();
            ChangeBrightness("Decrease", "F9");
            int difference = VerifyChangeInBrightness(brightnessB4Changing);
            if (difference < 0)
                Log.Success("Brightness has been decreased");
            else
                Log.Fail("Brightness has not decreased");
            brightnessB4Changing = base.CurrentMonitorBrightness();
            ChangeBrightness("Increase", "F10");
            difference = VerifyChangeInBrightness(brightnessB4Changing);
            if (difference > 0)
                Log.Success("Brightness has been increased");
            else
                Log.Fail("Brightness has not increased");
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Check if brightness level is persistant after resuming from S3");
            int currentBrightnessLevel = base.CurrentMonitorBrightness();
            this._powerParams = new PowerParams() { Delay = 30, };
            base.InvokePowerEvent(this._powerParams, PowerStates.S3);
            Log.Message("Verify that the brightness level is persistant after resuming from S3");
            PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);
            if (powerState == PowerLineStatus.Online)
                AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5);

            int brightnessAfterResumingFromS3 = base.CurrentMonitorBrightness();
            if (currentBrightnessLevel == brightnessAfterResumingFromS3)
                Log.Success("Brightness level persistant after S3");
            else
                Log.Fail("Brightness level not persistant, Before S3 = {0}, after S3 = {1}", currentBrightnessLevel, brightnessAfterResumingFromS3);
        }

        private void ChangeBrightness(string argIncreaseDecrease, string argKey)
        {
            Log.Message(true, "{0} the brightness of EDP", argIncreaseDecrease);
            Log.Message("{0} the brightness using Ctrl+Alt+Shift+{1}", argIncreaseDecrease, argKey);
            AccessInterface.SetFeature<bool, string>(Features.ACPIFunctions, Action.SetMethod, argKey);
        }
        private int VerifyChangeInBrightness(int argInitialValue)
        {
            int currentBrightnessValue = base.CurrentMonitorBrightness();
            Log.Message("Initial Brightness value = {0} Current Brightness Value {1}", argInitialValue, currentBrightnessValue);
            return currentBrightnessValue - argInitialValue;
        }
        private void LaunchCUIAndSetConfig()
        {
            DisplayConfig displayConfig = new DisplayConfig()
            {
                ConfigType = DisplayConfigType.SD,
                PrimaryDisplay = DisplayType.EDP
            };
            string setConfigString = base.GetConfigString(displayConfig);
            AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, displayConfig);
        }
    }
}