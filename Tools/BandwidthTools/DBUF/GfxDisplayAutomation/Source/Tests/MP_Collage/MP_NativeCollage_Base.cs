namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System.Text;

    class MP_NativeCollage_Base : TestBase
    {
        internal CollageParam collagepar = null;
        public MP_NativeCollage_Base()
        {
            collagepar = new CollageParam();
        }

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {
            CollageParam collagepar = new CollageParam();
            collagepar.option = CollageOption.Enable;
            collagepar.config = null;
            if (base.CurrentConfig.CustomDisplayList.Count < 2)
                Log.Abort("The Collage configuration requires atleast 2 displays");
            if (base.MachineInfo.OS.Type == OSType.WINTHRESHOLD)
            {
                if (base.CurrentConfig.DisplayList.Contains(DisplayType.EDP))
                    Log.Abort("Collage can't applyed with EDP config");
            }
            if (AccessInterface.SetFeature<bool, CollageParam>(Features.Collage, Action.SetMethod, collagepar))
            {
                Log.Success("Config enabled successfully");
            }
            else
            {
                Log.Abort("Collage can't be enabled");
            }
        }
        protected string GetConfigString(DisplayConfig argConfig)
        {
            StringBuilder sb = new StringBuilder(argConfig.ConfigType.ToString()).Append(" ");
            sb.Append(argConfig.PrimaryDisplay.ToString()).Append(" ");
            if (argConfig.SecondaryDisplay != DisplayType.None)
                sb.Append(argConfig.SecondaryDisplay.ToString()).Append(" ");
            if (argConfig.TertiaryDisplay != DisplayType.None)
                sb.Append(argConfig.TertiaryDisplay.ToString()).Append(" ");
            return sb.ToString();
        }

        protected string GetDisplayListString(List<DisplayType> argDisplayList)
        {
            StringBuilder sb = new StringBuilder();
            foreach (DisplayType DT in argDisplayList)
            {
                sb.Append(DT.ToString()).Append(" ");
            }
            return sb.ToString();
        }

        protected List<DisplayType> GetDisplayList(DisplayConfig argConfig)
        {
            List<DisplayType> dispList = new List<DisplayType>();
            dispList.Add(argConfig.PrimaryDisplay);
            if (argConfig.SecondaryDisplay != DisplayType.None)
                dispList.Add(argConfig.SecondaryDisplay);
            if (argConfig.TertiaryDisplay != DisplayType.None)
                dispList.Add(argConfig.TertiaryDisplay);
            return dispList;
        }
        protected bool CheckCollageThruResolution(DisplayConfigType argConfigType, DisplayMode argDisplayMode, int argDisplayCount)
        {
            if (argConfigType == DisplayConfigType.Horizontal)
                return (argDisplayMode.HzRes % argDisplayCount == 0);
            else
                return (argDisplayMode.VtRes % argDisplayCount == 0);
        }
        protected bool CheckCollageThruResolution90And270(DisplayConfigType argConfigType, DisplayMode argDisplayMode, int argDisplayCount)
        {
            if (argConfigType == DisplayConfigType.Vertical)
                return (argDisplayMode.HzRes % argDisplayCount == 0);
            else
                return (argDisplayMode.VtRes % argDisplayCount == 0);
        }
        protected void VerifyCollagePersistence(string argSetConfigString, int argSporadic)
        {
            collagepar.option = CollageOption.GetConfig;

            CollageParam collageStatus = AccessInterface.GetFeature<CollageParam, CollageParam>(Features.Collage, Action.GetMethod, Source.AccessAPI, collagepar);
            string currentConfigString = this.GetConfigString(collageStatus.config);
            if (argSetConfigString.Equals(currentConfigString))
                Log.Success("Config {0} persistant ", currentConfigString);
            else
                if (argSporadic == 1)
                    Log.Sporadic("Config persistance failed, Actual config is  {0}. Current config is {1}", argSetConfigString, currentConfigString);
                else
                    Log.Fail("Config persistance failed, Actual config is  {0}. Current config is {1}", argSetConfigString, currentConfigString);

        }
    }
}