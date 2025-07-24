namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    class MP_Mode_ApplyConfiguration : TestBase
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            if (base.CurrentConfig.ConfigTypeCount > base.CurrentConfig.DisplayList.Count())
            {
                Log.Abort("{0} requires atleast {1} Displays to be enumerated, current Display count: {2}", base.CurrentConfig.ConfigType, base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());
            }
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            DisplayConfig configToBeSet = new DisplayConfig();
            configToBeSet.ConfigType = base.CurrentConfig.ConfigType;

            switch (base.CurrentConfig.ConfigTypeCount)
            {
                case 1: PerformSingleDisplayConfigSwitch(configToBeSet); break;
                case 2: PerformDualDisplayConfigSwitch(configToBeSet); break;
                case 3: PerformTriDisplayConfigSwitch(configToBeSet); break;
                default: break;
            }
        }
        private void SetConfig(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("Config Applied successfully");
            else
            {
                Log.Fail(false, "Failed to apply Config,Expected config {0}",argDispConfig.GetCurrentConfigStr());
                Log.Message("Current enumerated displays");
                List<uint> winMonitorIDs = AccessInterface.GetFeature<List<uint>>(Features.WindowsMonitorID, Action.GetAll);
                DisplayInfo displayInfo = null;
                winMonitorIDs.ForEach(iD =>
                {
                    displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.WindowsMonitorID.Equals(iD)).FirstOrDefault();
                    if (null != displayInfo)
                        Log.Message("{0} - {1}", displayInfo.DisplayType, displayInfo.CompleteDisplayName);
                });
            }
        }
        private void PerformTriDisplayConfigSwitch(DisplayConfig argConfigToBeSet)
        {
            List<List<int>> triDisplaySwitch = new List<List<int>>()
            {
                {new List<int>(){0,1,2}},
                {new List<int>(){0,2,1}},
                {new List<int>(){1,2,0}},
                {new List<int>(){1,0,2}},
                {new List<int>(){2,0,1}},
                {new List<int>(){2,1,0}}
            };
            foreach (List<int> currentList in triDisplaySwitch)
            {
                argConfigToBeSet.PrimaryDisplay = base.CurrentConfig.DisplayList.ElementAt(currentList.ElementAt(0));
                argConfigToBeSet.SecondaryDisplay = base.CurrentConfig.DisplayList.ElementAt(currentList.ElementAt(1));
                argConfigToBeSet.TertiaryDisplay = base.CurrentConfig.DisplayList.ElementAt(currentList.ElementAt(2));
                SetConfig(argConfigToBeSet);
            }
        }
        private void PerformDualDisplayConfigSwitch(DisplayConfig argConfigToBeSet)
        {
            DisplayType primaryDisplay = base.CurrentConfig.DisplayList.First();
            DisplayType secondaryDisplay = base.CurrentConfig.DisplayList.ElementAt(1);

            argConfigToBeSet.PrimaryDisplay = primaryDisplay;
            argConfigToBeSet.SecondaryDisplay = secondaryDisplay;
            SetConfig(argConfigToBeSet);
       
            argConfigToBeSet.PrimaryDisplay = secondaryDisplay;
            argConfigToBeSet.SecondaryDisplay = primaryDisplay;
            SetConfig(argConfigToBeSet);
        }     
        private void PerformSingleDisplayConfigSwitch(DisplayConfig argConfigToBeSet)
        {
            foreach (DisplayType currentDispType in base.CurrentConfig.DisplayList)
            {
                argConfigToBeSet.PrimaryDisplay = currentDispType;
                SetConfig(argConfigToBeSet);
            }
        }
    }
}

