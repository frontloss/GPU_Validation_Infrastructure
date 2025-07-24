namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Collections.Generic;

    class MP_BAT_DisableEnable_CO : TestBase
    {
        private List<DisplayType> InitialDisplayList = null;
        int LoopCount = 1, DelayOnDisable = 0, DelayOnEnable = 0;
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config {0} Applied", base.CurrentConfig.GetCurrentConfigStr());
            else
                Log.Abort("Failed to apply config {0}", base.CurrentConfig.GetCurrentConfigStr());

            string fileName = string.Concat(Directory.GetCurrentDirectory(), @"\DisableEnableTestCount.txt");
            if (!File.Exists(fileName))
                Log.Abort("Disable enable test count file not found");
            else
            {
                string[] countStr = File.ReadAllLines(fileName);

                if (countStr.Count() <= 0)
                    Log.Abort("Enter count value in DisableEnableTestCount.txt");

                string[] data = countStr[0].Split(' ');
                for (int i = 0; i < data.Length; i++)
                {
                    switch (i)
                    {
                        case 0:
                            LoopCount = Convert.ToInt16(data[0]); Log.Verbose("Loop Count {0}", LoopCount); break;
                        case 1: DelayOnDisable = Convert.ToInt16(data[1]); Log.Verbose("DelayOnDisable {0}", DelayOnDisable); break;
                        case 2: DelayOnEnable = Convert.ToInt16(data[2]); Log.Verbose("DelayOnEnable {0}", DelayOnEnable); break;
                        default: break;
                    }
                }
            }
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            for (int i = 0; i < LoopCount; i++)
            {
                Log.Alert("\n\n  Running Iteration Number: {0}", i + 1);
                InitialDisplayList = new List<DisplayType>();
                InitialDisplayList = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType != DisplayType.None).Select(dI => dI.DisplayType).ToList();

                DisplayConfig InitialConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
                Log.Message("The configuration before disabling driver is  is {0}", InitialConfig.GetCurrentConfigStr());
                base.AssertDriverState(Features.DisableDriver, DriverState.Disabled, new[] { 3, 3 });
                Thread.Sleep(DelayOnDisable * 1000);

                DisplayConfig DisabledConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
                Log.Message("The configuration after disabling driver is {0}", DisabledConfig.GetCurrentConfigStr());

                base.AssertDriverState(Features.EnableDriver, DriverState.Running, new[] { 3, 3 });
                Thread.Sleep(DelayOnEnable * 1000);

                List<DisplayType> CurrentConfig = new List<DisplayType>();
                CurrentConfig = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType != DisplayType.None).Select(dI => dI.DisplayType).ToList();
                DisplayConfig DispConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
                Log.Message("The configuration after enablin driver is {0}", DispConfig.GetCurrentConfigStr());

                if (InitialDisplayList.Except(CurrentConfig).Count() != 0 || CurrentConfig.Except(InitialDisplayList).Count() != 0)
                {
                    Log.Fail("Mismatch between the display's before and after the disable-enable");

                    Log.Verbose("Display Before Disable-Enable");
                    foreach (DisplayType DT in InitialDisplayList)
                        Log.Verbose(DT.ToString());

                    Log.Verbose("Display after Disable-Enable");
                    foreach (DisplayType DT in CurrentConfig)
                        Log.Verbose(DT.ToString());
                    Log.Verbose("\n");
                }
                else
                {
                    Log.Success("The Displays Match before and after disable-enable");
                }
                if (InitialConfig.GetCurrentConfigStr().Equals(DispConfig.GetCurrentConfigStr()))
                    Log.Message("Config {0} is same , before and after Disable Enable", InitialConfig.GetCurrentConfigStr());
                else
                    Log.Message("config changed from {0} to {1} after Disable Enable", InitialConfig.GetCurrentConfigStr(), DispConfig.GetCurrentConfigStr());
            }
        }
    }
}