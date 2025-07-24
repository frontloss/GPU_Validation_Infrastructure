namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading;

    [Test(Type = TestType.WiDi)]
    class MP_WIDI_Driver_Disable_Enable : MP_WIDIBase
    {
        DriverInfo drivInfo;
        [Test(Type = TestType.Method, Order = 1)]
        public void SetConfigMethod()
        {
            this.SetNValidateConfig(this.CurrentConfig);
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void DisableEnableIGD()
        {
            Log.Message("Disable the driver");
            base.AssertDriverState(Features.DisableDriver, DriverState.Disabled, new[] { 3, 4 });
            drivInfo = AccessInterface.GetFeature<DriverInfo, DriverAdapterType>(Features.DriverFunction, Action.GetMethod, Source.AccessAPI, DriverAdapterType.Intel);
            if (drivInfo.Status.ToLower().Equals("disabled"))
                Log.Success("IGD Disabled.");
            else
                Log.Fail("IGD not Disabled.");

            Log.Message("Enable the driver");
            base.AssertDriverState(Features.EnableDriver, DriverState.Running, new[] { 5, 6 });
            drivInfo = AccessInterface.GetFeature<DriverInfo, DriverAdapterType>(Features.DriverFunction, Action.GetMethod, Source.AccessAPI, DriverAdapterType.Intel);
            if (drivInfo.Status.ToLower().Equals("running"))
            {
                Log.Success("IGD Enabled.");
                AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
            }
            else
                Log.Fail("IGD not Enabled.");
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void ReConnectWIDI()
        {
            if (!IsWiDiConnected())
            {
                Log.Message("Wait for some time and try to connect WiDi display");
                Thread.Sleep(15000);
                if (base.WiDiReConnect(true))
                    Log.Success("Successfully re-connect WiDi display");
                else
                    Log.Fail("Unable to connect WiDi display");
            }
            else
                Log.Alert("WiDi display is connected");
        }
    }
}
