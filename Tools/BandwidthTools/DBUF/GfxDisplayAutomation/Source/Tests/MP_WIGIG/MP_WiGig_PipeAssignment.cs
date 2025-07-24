// This test verifies whether WiGig can be enabled on all the Display Pipes A, B and C

namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;

    class MP_WiGig_PipeAssignment : MP_WiGig_Base
    {

        /// <summary>
        /// function to check if required number of displays are present to perform the config given in commandline
        /// </summary>
        
        [Test(Type = TestType.PreCondition, Order = 1)]
        public void TestPreCondition()
        {
            base.ApplyConfig();
        }

        /// <summary>
        /// Function to call appropriate display config switch function based on the number of displays
        /// </summary>
        
        [Test(Type = TestType.Method, Order = 2)]
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

        /// <summary>
        /// This function is used to assign the current mode details to a variable of WIGIGPARAMS type which checks on which pipe the Wigig Display is present
        /// </summary>
        /// <param name="argDispConfig">Holds the config for which pipe has to be checked</param>

        private void Pipe_Check(DisplayConfig argDispConfig)
        {
            List<DisplayType> displist = base.CurrentConfig.DisplayList.ToList();
            foreach (DisplayType display in displist)
            {
                if (DisplayExtensions.GetDisplayType(display) == DisplayType.WIGIG_DP)
                {
                    Log.Message("WiGig Pipe Assignment test started ....");
                    WiGigParams inputParam = new WiGigParams();
                    inputParam.wigigSyncInput = WIGIG_SYNC.WiGigDisplayPipe;
                    inputParam.wigigDisplay = display;
                    base.Pipe_Assignment(inputParam);
                }
            }
        }

        /// <summary>
        /// Function to apply the particular configuration passed in the parameter argDispConfig
        /// </summary>
        /// <param name="argDispConfig">Holds the config to be set</param>
        
        private void SetConfig(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
            {
                Log.Success("Config Applied successfully");
            }
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
                {new List<int>(){1,2,0}},
                {new List<int>(){2,0,1}},
            };
            foreach (List<int> currentList in triDisplaySwitch)
            {
                argConfigToBeSet.PrimaryDisplay = base.CurrentConfig.DisplayList.ElementAt(currentList.ElementAt(0));
                argConfigToBeSet.SecondaryDisplay = base.CurrentConfig.DisplayList.ElementAt(currentList.ElementAt(1));
                argConfigToBeSet.TertiaryDisplay = base.CurrentConfig.DisplayList.ElementAt(currentList.ElementAt(2));
                
                // Apply tri-display configuration
                SetConfig(argConfigToBeSet);
                
                // Verify Pipe assignment 
                Pipe_Check(argConfigToBeSet);
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
            Pipe_Check(argConfigToBeSet);

            argConfigToBeSet.PrimaryDisplay = secondaryDisplay;
            argConfigToBeSet.SecondaryDisplay = primaryDisplay;
            SetConfig(argConfigToBeSet);
            Pipe_Check(argConfigToBeSet);
        }

        /// <summary>
        /// function to apply single display configuration passed in the parameter argConfigToBeSet
        /// </summary>
        /// <param name="argConfigToBeSet">holds config to be set</param>
        
        private void PerformSingleDisplayConfigSwitch(DisplayConfig argConfigToBeSet)
        {
            foreach (DisplayType currentDispType in base.CurrentConfig.DisplayList)
            {
                argConfigToBeSet.PrimaryDisplay = currentDispType;
                SetConfig(argConfigToBeSet);
                Pipe_Check(argConfigToBeSet);
            }
        }
    }
}
