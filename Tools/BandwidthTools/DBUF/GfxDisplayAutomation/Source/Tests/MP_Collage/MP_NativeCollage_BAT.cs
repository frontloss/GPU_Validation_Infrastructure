namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System.Threading;

    class MP_NativeCollage_BAT : MP_NativeCollage_Base
    {
        protected string setConfigString;

        protected List<DisplayConfigType> _myList = null;
        protected DisplayConfig displayConfig;
        protected DisplayMode currentMode;
        protected DisplayInfo displayInfo;
        protected DisplayConfigType result;
        protected System.Action _performAction = null;
        public MP_NativeCollage_BAT()
            : base()
        {
            _performAction = null;
            _myList = new List<DisplayConfigType>()
            {
                DisplayConfigType.Horizontal,
                DisplayConfigType.Vertical
            };
        }
        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {            
            base.collagepar.option = CollageOption.SetConfig;

            foreach (DisplayConfigType CT in _myList)
            {
                result = CT;
                displayConfig = new DisplayConfig()
                {
                    ConfigType = result,
                    PrimaryDisplay = base.CurrentConfig.PrimaryDisplay,
                    SecondaryDisplay = base.CurrentConfig.SecondaryDisplay,
                    TertiaryDisplay = base.CurrentConfig.TertiaryDisplay,
                    DisplayList = base.CurrentConfig.DisplayList,
                    EnumeratedDisplays = base.CurrentConfig.EnumeratedDisplays

                };
                
                setConfigString = base.GetConfigString(displayConfig);

                collagepar.config = displayConfig;
                collagepar.option = CollageOption.SetConfig;
                if (AccessInterface.SetFeature<bool, CollageParam>(Features.Collage, Action.SetMethod, collagepar))
                {
                    Log.Success("Config set successfully to {0}", setConfigString);
                }
                                
                Log.Message(true, "Verifying {0} configuration is set using Resolutions", displayConfig.ConfigType);
                displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == base.CurrentConfig.PrimaryDisplay).First();
                currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
                if (base.CheckCollageThruResolution(displayConfig.ConfigType, currentMode, base.CurrentConfig.DisplayList.Count))
                    Log.Success("{0} is verified to be successfully set using Resolutions", displayConfig.ConfigType);
                else
                    Log.Fail("{0} is not verified using Resolutions", displayConfig.ConfigType);
                if (null != this._performAction)
                    this._performAction();
            }
        }
        [Test(Type = TestType.PostCondition, Order = 2)]
        public virtual void TestStep2()
        {
            Log.Message(true, "Disable collage, set config to sd Primary display");

            collagepar.option = CollageOption.Disable;

            if (AccessInterface.SetFeature<bool, CollageParam>(Features.Collage, Action.SetMethod, collagepar))
            {
                Log.Success("Config disabled successfully");
            }
            else
            {
                Log.Fail("Collage can't be disabled");
            }

            DisplayConfig displayConfig = new DisplayConfig()
            {
                ConfigType = DisplayConfigType.SD,
                PrimaryDisplay = base.CurrentConfig.PrimaryDisplay
            };
            if(AccessInterface.SetFeature<bool,DisplayConfig>(Features.Config, Action.SetMethod, displayConfig))
            {
                Log.Success("SD Config enabled successfully");
            }
            
        }      
    }
}