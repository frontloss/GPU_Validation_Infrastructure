namespace Intel.VPG.Display.Automation
{
    using System.Threading;
    class MP_ConnectedStandbyStartStopDevice : MP_ConnectedStandbyBase
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
                this.CleanUP();
                Log.Abort("Config not applied!");
            }
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void StartStopDevice()
        {
            Log.Message(true, "Disabling Gfx Driver and enabling it back after 30 sec");
            Log.Verbose("Disabling Gfx Driver");
            if (!AccessInterface.SetFeature<bool>(Features.DisableDriver, Action.SetNoArgs))
            {
                this.CleanUP();
                Log.Abort("Unable to disable Gfx Driver");
            }
            else
                Log.Success("Gfx driver successfully disabled");
            AccessInterface.SetFeature<bool>(Features.DriverFunction, Action.SetNoArgs);
            base.MachineInfo.Driver.PrintBasicDetails();
            Log.Verbose("Waiting for 30 sec");
            Thread.Sleep(30000);
            if (AccessInterface.SetFeature<bool>(Features.EnableDriver, Action.SetNoArgs))
                Log.Success("Gfx Driver Successfully Enabled");
            else
            {
                this.CleanUP();
                Log.Abort("Gfx Driver not Enabled!");
            }
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void SendSysytemToS0ix()
        {
            this.S0ixCall();
            StartStopDevice();
        }

        #endregion

        #region PostCondition
        [Test(Type = TestType.PostCondition, Order = 4)]
        public void TestPostCondition()
        {
            this.CleanUP();
        }
        #endregion
    }
}
