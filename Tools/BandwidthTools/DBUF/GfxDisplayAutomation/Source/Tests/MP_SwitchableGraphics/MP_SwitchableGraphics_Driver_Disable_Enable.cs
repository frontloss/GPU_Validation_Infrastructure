namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Xml.Linq;
    using System.Diagnostics;

    class MP_SwitchableGraphics_Driver_Disable_Enable : MP_SwitchableGraphics_Base
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Set config via OS call");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Disable ATI,Intel..Enable ATI,Intel");
            Log.Message("Disable ATI Adapter");
            this.AssertDriverState(Features.DisableDriver, DriverState.Disabled, DriverAdapterType.ATI);
            Log.Message("Disable Intel Adapter");
            this.AssertDriverState(Features.DisableDriver, DriverState.Disabled, DriverAdapterType.Intel);
            Log.Message("Enable ATI Adapter");
            this.AssertDriverState(Features.EnableDriver, DriverState.Running, DriverAdapterType.ATI);
            Log.Message("Enable Intel Adapter");
            this.AssertDriverState(Features.EnableDriver, DriverState.Running, DriverAdapterType.Intel);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Disable ATI,Intel..Enable Intel,ATI");
            Log.Message("Disable ATI Adapter");
            this.AssertDriverState(Features.DisableDriver, DriverState.Disabled, DriverAdapterType.ATI);
            Log.Message("Disable Intel Adapter");
            this.AssertDriverState(Features.DisableDriver, DriverState.Disabled, DriverAdapterType.Intel);
            Log.Message("Enable Intel Adapter");
            this.AssertDriverState(Features.EnableDriver, DriverState.Running, DriverAdapterType.Intel);
            Log.Message("Enable ATI Adapter");
            this.AssertDriverState(Features.EnableDriver, DriverState.Running, DriverAdapterType.ATI);
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Disable Intel,ATI..Enable ATI,Intel");
            Log.Message("Disable Intel Adapter");
            this.AssertDriverState(Features.DisableDriver, DriverState.Disabled, DriverAdapterType.Intel);
            Log.Message("Disable ATI Adapter");
            this.AssertDriverState(Features.DisableDriver, DriverState.Disabled, DriverAdapterType.ATI);
            Log.Message("Enable ATI Adapter");
            this.AssertDriverState(Features.EnableDriver, DriverState.Running, DriverAdapterType.ATI);
            Log.Message("Enable Intel Adapter");
            this.AssertDriverState(Features.EnableDriver, DriverState.Running, DriverAdapterType.Intel);
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Disable Intel,ATI..Enable Intel,ATI");
            Log.Message("Disable Intel Adapter");
            this.AssertDriverState(Features.DisableDriver, DriverState.Disabled, DriverAdapterType.Intel);
            Log.Message("Disable ATI Adapter");
            this.AssertDriverState(Features.DisableDriver, DriverState.Disabled, DriverAdapterType.ATI);
            Log.Message("Enable Intel Adapter");
            this.AssertDriverState(Features.EnableDriver, DriverState.Running, DriverAdapterType.Intel);
            Log.Message("Enable ATI Adapter");
            this.AssertDriverState(Features.EnableDriver, DriverState.Running, DriverAdapterType.ATI);
        }
        internal void AssertDriverState(Features argFeature, DriverState argState, DriverAdapterType argAdapterType)
        {
            if (this.ChangeDriverState(argFeature, argState, argAdapterType))
                Log.Success("{0} {1}", argAdapterType, argState);
            else
                Log.Abort("{0} not {1}!", argAdapterType, argState);
        }
        internal bool ChangeDriverState(Features argFeature, DriverState argState, DriverAdapterType argAdapterType)
        {
            Log.Message(true, "{0} {1}", argState, argAdapterType);
            bool initState = AccessInterface.SetFeature<bool, DriverAdapterType>(argFeature, Action.SetMethod, argAdapterType);
            DriverInfo driverInfo = AccessInterface.GetFeature<DriverInfo, DriverAdapterType>(Features.DriverFunction, Action.GetMethod, Source.AccessAPI, argAdapterType);
            if (initState)
            {
                Log.Message(true, "Verify {0} got {1}.", argAdapterType, argState);
                return driverInfo.Status.ToLower().Equals(argState.ToString().ToLower());
            }
            return false;
        }
    }
}
