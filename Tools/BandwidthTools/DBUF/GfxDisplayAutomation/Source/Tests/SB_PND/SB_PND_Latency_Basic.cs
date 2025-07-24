namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;

    class SB_PND_Latency_Basic : SB_PND_Base
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.ConfigTypeCount > base.CurrentConfig.DisplayList.Count())
                Log.Abort("{0} requires atleast {1} Displays to be enumerated, current Display count: {2}", base.CurrentConfig.ConfigType, base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("{0} Applied successfully", base.CurrentConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", base.CurrentConfig.GetCurrentConfigStr());

        }

        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            foreach (DisplayType disp in base.CurrentConfig.CustomDisplayList)
            {
                CheckPNDLatency(disp);
            }
        }
        private void CheckPNDLatency(DisplayType currentDisplay)
        {
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentDisplay).First();
            DisplayMode displayMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);

            CheckPNDLatency(currentDisplay, displayMode);
        }
        protected void CheckPNDLatency(DisplayType currentDisplay, DisplayMode displayMode)
        {
            if (Platform.CHV == this.MachineInfo.PlatformDetails.Platform && this.CurrentConfig.ConfigType != DisplayConfigType.SD)
            {
                Log.Alert("Skipping PNDLatency check other than SingleDisplay as per bug:5617028");
            }
            else
            {
                PipePlaneParams pipePlaneParam = new PipePlaneParams(currentDisplay);
                pipePlaneParam = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlaneParam);

                TestPndLatency(pipePlaneParam, displayMode.Bpp, (uint)displayMode.pixelClock);
            }
        }
    }
}
