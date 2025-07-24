// This test gets list of all graphics modes enumerated for the WiGig Display by the Graphics driver. Then
// it will scan through each mode to check whether it is POR mode or not.

namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;

    class MP_WiGig_ModeEnumeration: MP_WiGig_Base
    {
        // A list created to hold all possible modes
        private List<DisplayModeList> allModeList = new List<DisplayModeList>();
        protected Dictionary<Platform, DisplayMode> _myDictionary = null;
       
        /// <summary>
        /// To apply the configuration specified in the commandline
        /// </summary>
        [Test(Type = TestType.Method, Order = 1)]
        public void applyConfig()
        {
            base.ApplyConfig();
        }

        /// <summary>
        /// Function to get all possible modes possible & to get each and every supported mode for WigigDisplay and call the Resolution Checking function for each mode
        /// </summary>
        [Test(Type = TestType.Method, Order = 2)]
        public void checkAllPossibleModes()
        {
            allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);
            
            if (!allModeList.Count.Equals(0))
            {
                allModeList.ForEach(dML =>
                {
                    if ((DisplayExtensions.GetDisplayType(dML.display) == DisplayType.WIGIG_DP))
                    {
                        dML.supportedModes.ForEach(dM => ApplyNVerify_GraphicsMode(dM));
                    }
                });
            }
            else
            {
                Log.Fail(false, "No modes returned!");
            }
        }
           
        private Dictionary<Platform, DisplayMode> SwitchPatternList
        {
            get
            {
                if (null == this._myDictionary)
                {
                    DisplayMode argMode= new DisplayMode();
                    argMode.HzRes=2560;
                    argMode.VtRes=1600;
                    this._myDictionary = new Dictionary<Platform, DisplayMode>();
                    this._myDictionary.Add(Platform.BXT, argMode);
                    this._myDictionary.Add(Platform.SKL, argMode);
                }
                return this._myDictionary;
            }
        }
        /// <summary>
        /// This function is used to assign the current mode details to a variable of WIGIGPARAMS type which checks the resolution of WIGIG display is within specified limits or not.
        /// </summary>
        private void ApplyNVerify_GraphicsMode(DisplayMode dispmode)
        {
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, dispmode))
            {
                if (DisplayExtensions.GetDisplayType(dispmode.display) == DisplayType.WIGIG_DP)
                {
                    Log.Message(true, "Verify the selected mode got applied for {0}", dispmode.display);
                    DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == dispmode.display).First();
                    DisplayMode curMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
                    DisplayMode modeCheck;
                    _myDictionary.TryGetValue(base.MachineInfo.PlatformEnum,out modeCheck);
                    //For SKL and BXT, maximum resolution supported on WiGig display is 2560x1600
                    if ((curMode.HzRes <= modeCheck.HzRes) && (curMode.VtRes <= modeCheck.VtRes))
                    {
                        Log.Message("Mode checked is {0}x{1} @ {2}", curMode.HzRes, curMode.VtRes, curMode.RR);
                        Log.Success("Enumerated mode is POR");
                    }
                    else
                    {
                        Log.Fail("Graphics mode {0}x{1} is not a POR", curMode.HzRes, curMode.VtRes);
                    }
                }
            }
            else
            {
                Log.Message("Mode not applied...");
            }
        }
   }
}
