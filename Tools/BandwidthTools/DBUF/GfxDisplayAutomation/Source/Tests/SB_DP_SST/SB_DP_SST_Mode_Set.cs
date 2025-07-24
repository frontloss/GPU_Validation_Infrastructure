using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_DP_SST_Mode_Set : SB_DP_SST_Base
    {
        private List<DisplayModeList> _DisplayModeList = new List<DisplayModeList>();
        protected DisplayInfo displayInfo;
        
        /*
         * This needs to be un commented in case of register verification
        // Constants to store Bitmap and golden value
        uint uiDPCDOffset = (uint)DPCDRegisters.DPCD_SINK_CONTROL;
        private const uint DP_HOTPLUG_BITMAP = 1;
        private const uint DP_HOTPLUG_GOLDENVALUE = 1;
        private const uint DP_HOTUNPLUG_GOLDENVALUE = 0;


        [Test(Type = TestType.Method, Order = 0)]
        public void checkConfig()
        {
            if (base.CurrentConfig.PrimaryDisplay == DisplayType.DP || base.CurrentConfig.SecondaryDisplay == DisplayType.DP || base.CurrentConfig.TertiaryDisplay == DisplayType.DP)
            {
                base.VerifyDPCDRegisterValue(DisplayType.DP, uiDPCDOffset, DP_HOTPLUG_BITMAP, DP_HOTPLUG_GOLDENVALUE);
            }
            if (base.CurrentConfig.PrimaryDisplay == DisplayType.DP_2 || base.CurrentConfig.SecondaryDisplay == DisplayType.DP_2 || base.CurrentConfig.TertiaryDisplay == DisplayType.DP_2)
            {
                base.VerifyDPCDRegisterValue(DisplayType.DP_2, uiDPCDOffset, DP_HOTPLUG_BITMAP, DP_HOTPLUG_GOLDENVALUE);
            }
        }
        */

        [Test(Type = TestType.Method, Order = 1)]
        public void ApplyModesAllConfig()
        {
            // Based on config-type we fetch mode list.
            // For clone we take modes which are intersection of modes of individual display
            // For extended we apply modes to each display based on supported modes for display
           _DisplayModeList = GetAllModes(base.CurrentConfig.CustomDisplayList);

           Log.Message(true, "Apply all Resolutions with Refresh Rate and Scaling");
           List<DisplayMode> ModeList = null;

          _DisplayModeList.ForEach(dML =>
            {
                    Log.Message("Configtype:-" + base.CurrentConfig.ConfigType.GetUnifiedConfig());
                    Log.Message("DisplayType\n" + dML.display + "\nMode List:-" + dML.supportedModes.ToList());
            
                    // If we wish to prune certain modes(i.e apply only few modes rather than applying)
                    // before applying we can do it in Testmodes.
                    // At present we are applying all modes.
                    ModeList = GetFinalModesList(dML.supportedModes.ToList());

                   //Apply and verify mode set
                    ModeList.ForEach(dM =>
                    {
                        this.ApplyNVerifyModeOS(dM, dM.display);

                        //Needed if we wish to do register verification
                        //DisplayInfo displayInfos = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == dML.display).First();

                        //Do CRC check here. Blocked on Chandru
                    });
            });
        }
         
        // Applied mode using AccessInterface and verifies whether mode set is succesful
        private void ApplyNVerifyModeOS(DisplayMode argSelectedMode, DisplayType argDisplayType)
        {
            //Apply Mode
            Log.Message(true, "Set supported mode {0} for {1}", argSelectedMode.GetCurrentModeStr(false), argDisplayType);
            argSelectedMode.display = argDisplayType;
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argSelectedMode))
                Log.Success("Mode applied Successfully");
            else
                Log.Fail("Fail to apply Mode");
            Log.Message("Verify the selected mode got applied for {0}", argDisplayType);
            //Verify the applied Mode
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplayType).First();
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            if (actualMode.GetCurrentModeStr(true).Equals(argSelectedMode.GetCurrentModeStr(true)))
                Log.Success("Mode {0} is applied for {1}", actualMode.GetCurrentModeStr(false), argDisplayType);
            else
                Log.Fail("Mode chosen {0} is not applied for {1}! Actual is {2}", argSelectedMode.GetCurrentModeStr(false), argDisplayType, actualMode.GetCurrentModeStr(false));
        }
  
        //Get all modes supported by DP panel planned in cofig
        private List<DisplayModeList> GetAllModes(List<DisplayType> argCustomDisplayList)
        {
            List<DisplayModeList> listDisplayMode = new List<DisplayModeList>();

            // Get the mode list for Single and Extended for both Dual and Tri configuration using CUISDK API
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, argCustomDisplayList);
            List<DisplayMode> commonModes = null;
            List<DisplayMode> tempCommonModes = null;
            List<DisplayModeList> tempModes = null;

            // For clone config, get common modes supported by all displays
            if (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
            {
                commonModes = allModeList.Where(dML => dML.display == base.CurrentConfig.PrimaryDisplay).Select(dML => dML.supportedModes).FirstOrDefault();
                tempModes = allModeList.Skip(1).ToList();

                for (int i = 0; i < tempModes.Count(); i++)
                {
                    tempCommonModes = tempModes[i].supportedModes.ToList();
                    commonModes = ModesRefreshRates(commonModes, tempCommonModes);
                }
                if (commonModes.Count() > 0)
                        listDisplayMode.Add(new DisplayModeList() { display = base.CurrentConfig.PrimaryDisplay, supportedModes = commonModes });
            }
            else
                listDisplayMode = allModeList;
            return listDisplayMode;
        }
      
        //Allows to apply all modes (exhaustive testcases) or particular modes (first, last and one random intermediate)
        //Currently we are doing exhaustive way
        private List<DisplayMode> GetFinalModesList(List<DisplayMode> displayModeList)
        {
            List<DisplayMode> testModes = new List<DisplayMode>();
            List<DisplayMode> ModesToBeApplied = new List<DisplayMode>();
            
            // TODO: Currently no pruning of modes done. In future, if required pruning should be added in function
            for (int i = 0; i < displayModeList.Count; i++)
            {
                testModes.Add(displayModeList[i]);
            }

            ModesToBeApplied = ModesRefreshRates(testModes, displayModeList);
            return ModesToBeApplied;
        }
        //Enables to do mode comparison for 2 set of modes. Useful for clone configuration
        private List<DisplayMode> ModesRefreshRates(List<DisplayMode> testMode, List<DisplayMode> entireModeList)
        {
            List<DisplayMode> modeRefreshRate = new List<DisplayMode>();
            for (int i = 0; i < testMode.Count; i++)
            {
                for (int j = 0; j < entireModeList.Count; j++)
                {
                    if ((testMode[i].HzRes == entireModeList[j].HzRes) && (testMode[i].VtRes == entireModeList[j].VtRes) && (testMode[i].RR == entireModeList[j].RR))
                        modeRefreshRate.Add(entireModeList[j]);
                }
            }
            return modeRefreshRate;
        }
    }
}
