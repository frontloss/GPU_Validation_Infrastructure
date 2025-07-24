namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;

    class MP_WiGig_ModeSet : MP_WiGig_Base
    {
        // A list created to hold all possible modes
        private List<DisplayModeList> allModeList = new List<DisplayModeList>();
        private string Horizontal_Resolution = "Horizontal_Resolution_Register";
        private string Vertical_Resolution = "Vertical_Resolution_Register";
        /// <summary>
        /// To check the number of displays and apply the configuration specified in the commandline
        /// </summary>
        [Test(Type = TestType.PreCondition, Order = 1)]
        public void ApplyConfiguration()
        {
            base.ApplyConfig();
        }

        /// <summary>
        /// Function to get all possible modes possible & to get each and every supported mode for WigigDisplay and to send the mode for applying 
        /// </summary>
        [Test(Type = TestType.Method, Order = 2)]
        public void CheckAllPossibleModes()
        {
            allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);
            List<DisplayMode> testModes = null;

            if (!allModeList.Count.Equals(0))
            {
                allModeList.ForEach(dML =>
                {
                    if (DisplayExtensions.GetDisplayType(dML.display) == DisplayType.WIGIG_DP)
                    {
                        testModes = this.TestModes(dML.supportedModes);
                        testModes.ForEach(dM => ApplyMode(dM));
                    }
                });
            }
            else
            {
                Log.Fail(false, "No modes returned!");
            }
        }
        private List<DisplayMode> TestModes(List<DisplayMode> displayModeList)
        {
            List<DisplayMode> testModes = new List<DisplayMode>();
            displayModeList.ForEach(dM => 
                {
                if(dM.ScalingOptions.Contains((uint)ScalingOptions.Maintain_Display_Scaling))
                {
                    dM.ScalingOptions.RemoveRange(0,dM.ScalingOptions.Count());
                    dM.ScalingOptions.Add((uint)ScalingOptions.Maintain_Display_Scaling);
                    testModes.Add(dM);
                }
                });
            return testModes;
        }
        
        /// <summary>
        /// Function to apply the mode passed in the parameter argMode
        /// </summary>
        /// <param name="argMode">Holds the mode to be applied</param>
        private void ApplyMode(DisplayMode argMode)
        {
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argMode))
            {
                if (DisplayExtensions.GetDisplayType(argMode.display) == DisplayType.WIGIG_DP)
                {
                    uint VtRz = 0;
                    uint HzRz = 0;
                    VtRz = base.GetRegisterValue(Vertical_Resolution, PIPE.NONE, PLANE.NONE, PORT.NONE);
                    HzRz = base.GetRegisterValue(Horizontal_Resolution, PIPE.NONE, PLANE.NONE, PORT.NONE);

                    DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argMode.display).First();
                    DisplayMode curMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);

                    if ((curMode.HzRes) == (HzRz))
                    {
                        if ((curMode.VtRes) == (VtRz))
                        {
                            Log.Success("Mode Applied Successfully");
                        }
                    }
                    else
                    {
                        Log.Fail("Mode Not applied");
                    }
                }
            }
        }
    }
}

