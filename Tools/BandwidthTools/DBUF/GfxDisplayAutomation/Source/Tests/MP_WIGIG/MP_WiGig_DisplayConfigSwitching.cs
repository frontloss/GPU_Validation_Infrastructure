// This test performs Display configuration switching based on number of display given as input.
// For example, if input is eDP, HDMI & WiGig displays, then all the possible combinations will be set and checked for correctness.

namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;

    class MP_WiGig_DisplayConfigSwitching : MP_WiGig_Base
    {
        /// <summary>
        /// to check if required number of displays are present to set a particular configuration
        /// </summary>
        [Test(Type = TestType.PreCondition, Order = 1)]
        public void PreCondition()
        {
            if (base.CurrentConfig.DisplayList.Count() < 1)
            {
                Log.Abort("Display Config Switching requires atleast two Displays to be enumerated, current Display count: {0}", base.CurrentConfig.DisplayList.Count());
            }
        }
     
        /// <summary>
        /// Function to call appropriate display config switch function based on the number of displays
        /// </summary>
        [Test(Type = TestType.Method, Order = 2)]
        public void CallConfigSwitch()
        {
            DisplayConfig configToBeSet = new DisplayConfig();
            configToBeSet.ConfigType = base.CurrentConfig.ConfigType;

            switch (base.CurrentConfig.ConfigTypeCount)
            {
                case 2: PerformDualDisplayConfigSwitch(configToBeSet); break;
                case 3: PerformTriDisplayConfigSwitch(configToBeSet); break;
                default: break;
            }
        }

        /// <summary>
        /// Function to apply the particular configuration passed in the parameter argDispConfig
        /// </summary>
        /// <param name="argDispConfig">Holds the config to be set</param>

        private void SetConfig(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("Config Applied successfully");
            else
            {
                Log.Fail(false, "Failed to apply Config,Expected config {0}", argDispConfig.GetCurrentConfigStr());
            }
        }

        /// <summary>
        /// function to apply tri-display configuration specified in commandline and perform display switching
        /// </summary>
        /// <param name="argConfigToBeSet">holds config to be set</param>

        private void PerformTriDisplayConfigSwitch(DisplayConfig argConfigToBeSet)
        {
            //list to hold the different possible ways of switching between the displays
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

        /// <summary>
        /// function to apply dual display configuration specified in commandline and perform display switching
        /// </summary>
        /// <param name="argConfigToBeSet">holds config to be set</param>

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
    }
}





