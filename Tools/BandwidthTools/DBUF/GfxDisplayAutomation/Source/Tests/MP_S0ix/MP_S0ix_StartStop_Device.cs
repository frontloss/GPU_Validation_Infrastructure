namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Threading;

    [Test(Type = TestType.ConnectedStandby)]
    class MP_S0ix_StartStop_Device : MP_S0ixBase
    {
        #region Test
        [Test(Type = TestType.Method, Order = 1)]
        public void SetConfigMethod()
        {
            Log.Message(true, "Set display Config using Windows API");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
            {
                Log.Success("Config applied successfully");
                Log.Message("Set the maximum display mode on all the active displays");
            }
            else
            {
                Log.Abort("Config not applied!");
            }
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void StartStopDevice()
        {
            Log.Message(true, "Disabling Gfx Driver and enabling it back after 30 sec");
            Log.Verbose("Disabling Gfx Driver");
            if (!AccessInterface.SetFeature<bool, DriverAdapterType>(Features.DisableDriver, Action.SetMethod, DriverAdapterType.Intel))
            {
                Log.Abort("Unable to disable Gfx Driver");
            }
            else
                Log.Success("Gfx driver successfully disabled");

            base.MachineInfo.Driver.PrintBasicDetails();
            Log.Verbose("Waiting for 30 sec");
            Thread.Sleep(30000);

            if (AccessInterface.SetFeature<bool, DriverAdapterType>(Features.EnableDriver, Action.SetMethod, DriverAdapterType.Intel))
            {
                Log.Success("Gfx Driver Successfully Enabled");
                foreach (DisplayType DT in base.CurrentConfig.PluggableDisplayList)
                {
                    if (base.HotPlug(DT))
                        Log.Success("Successfully hotplug display {0}", DT);
                    else
                        Log.Abort("Unable to hotplug display {0}", DT);
                }
                SetConfigMethod();
            }
            else
            {
                Log.Abort("Gfx Driver not Enabled!");
            }
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void SendSysytemToS0ix()
        {
            this.CSCall();
            StartStopDevice();
        }

        #endregion
    }
}
