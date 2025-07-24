//namespace Intel.VPG.Display.Automation
//{
//    using System.Linq;
//    using System.Windows.Forms;

//    [Test(Type = TestType.HasReboot)]
//    class MP_InstallUninstall_BootSystem_DC_AC : TestBase
//    {
//        private PowerParams _powerParams = null;
//        [Test(Type = TestType.PreCondition, Order = 0)]
//        public void TestPreCondition()
//        {
//            DisplayConfig objDisplayConfig = new DisplayConfig();
//            objDisplayConfig.ConfigType = DisplayConfigType.SD;
//            objDisplayConfig.PrimaryDisplay = DisplayType.EDP;
//            AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, objDisplayConfig);
//        }
//        [Test(Type = TestType.Method, Order = 1)]
//        public void TestStep1()
//        {
//            Log.Message(true, "Enable AC Mode");
//            PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);
//            if (powerState == PowerLineStatus.Offline)
//            {
//                if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
//                    Log.Success("System is Running in AC Mode");
//                else
//                    Log.Fail("Fail to set AC mode");
//            }
//            else
//                Log.Success("System is Running in AC Mode");
//        }
//        [Test(Type = TestType.Method, Order = 2)]
//        public void TestStep2()
//        {
//            Log.Message(true, "Switch to DC Mode");
//            PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);
//            if (powerState == PowerLineStatus.Online)
//            {
//                if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
//                    Log.Success("System is Running in DC Mode");
//                else
//                    Log.Fail("Fail to set DC Mode");
//            }
//            else
//                Log.Success("System is Running in DC Mode");
//        }
//        [Test(Type = TestType.Method, Order = 3)]
//        public void TestStep3()
//        {
//            Log.Message(true, "Reboot the system");
//            PowerStates powerState = PowerStates.S5;
//            this._powerParams = new PowerParams() { Delay = 30, rebootReason = RebootReason.DriverModify };
//            base.EventResult(powerState, base.InvokePowerEvent(this._powerParams, powerState));
//        }
//        [Test(Type = TestType.Method, Order = 4)]
//        public void TestStep4()
//        {
//            Log.Message(true, "Verify System is still in DC Mode");
//            PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);
//            if (powerState == PowerLineStatus.Offline)
//                Log.Success("System in DC Mode after restart");
//            else
//                Log.Fail("System in AC, expected to be in DC Mode");
//        }
//        [Test(Type = TestType.Method, Order = 5)]
//        public void TestStep5()
//        {
//            Log.Message("Switch to AC Mode");
//            PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);
//            if (powerState == PowerLineStatus.Offline)
//            {
//                if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
//                    Log.Success("System is Running in AC Mode");
//                else
//                    Log.Fail("Fail to set AC mode");
//            }
//            else
//                Log.Success("System is Running in AC Mode");
//        }
//        [Test(Type = TestType.Method, Order = 6)]
//        public void TestStep6()
//        {
//            Log.Message(true, "Reboot the system");
//            PowerStates powerState = PowerStates.S5;
//            this._powerParams = new PowerParams() { Delay = 30, rebootReason = RebootReason.DriverModify };
//            base.EventResult(powerState, base.InvokePowerEvent(this._powerParams, powerState));
//        }
//        [Test(Type = TestType.Method, Order = 7)]
//        public void TestStep7()
//        {
//            Log.Message(true, "Verify System is still in AC Mode");
//            PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);
//            if (powerState == PowerLineStatus.Online)
//                Log.Success("System in AC Mode after restart");
//            else
//                Log.Fail("System in DC, expected to be in AC Mode");
//        }

//    }
//}

