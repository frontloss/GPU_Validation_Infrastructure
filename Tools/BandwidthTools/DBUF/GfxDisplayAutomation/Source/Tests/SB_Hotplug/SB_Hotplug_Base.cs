namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System.Text.RegularExpressions;
    class SB_Hotplug_Base : TestBase
    {
        protected Dictionary<DisplayType, string> _defaultEDIDMap = null;
        protected Dictionary<DisplayType, string> _changeEdid = null;
        protected List<DisplayType> _semiAutomatedDispList = null;
        public SB_Hotplug_Base()
        {
            _defaultEDIDMap = new Dictionary<DisplayType, string>();
            _changeEdid = new Dictionary<DisplayType, string>();
            _semiAutomatedDispList = new List<DisplayType>();
            _semiAutomatedDispList.Add(DisplayType.CRT);

           
        }
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
                _defaultEDIDMap.Add(DisplayType.HDMI, "HDMI_DELL.EDID");
                _changeEdid.Add(DisplayType.HDMI, "HDMI_DELL_U2711_XVYCC.EDID");
                _defaultEDIDMap.Add(DisplayType.HDMI_2, "HDMI_Dell_3011.EDID");
                _changeEdid.Add(DisplayType.HDMI_2, "HDMI_HP.EDID");

                if (ApplicationManager.ApplicationSettings.UseDivaFramework || ApplicationManager.ApplicationSettings.UseULTFramework || ApplicationManager.ApplicationSettings.UseSHEFramework) 
            {
                _defaultEDIDMap.Add(DisplayType.DP, "DP_3011.EDID");
                _changeEdid.Add(DisplayType.DP, "DP_HP_ZR2240W.EDID");
                _defaultEDIDMap.Add(DisplayType.DP_2, "DP_HP_ZR2240W.EDID");
                _changeEdid.Add(DisplayType.DP_2, "DP_3011.EDID");
            }

            if (base.CurrentConfig.ConfigTypeCount > base.CurrentConfig.DisplayList.Count())
                Log.Abort("{0} requires atleast {1} Displays to be enumerated, current Display count: {2}", base.CurrentConfig.ConfigType, base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());

            if (base.CurrentConfig.DisplayList.Intersect(_defaultEDIDMap.Keys).Count() == 0)
                Log.Abort("Hotplug test needs atleast 1 pluggable display");
        }
        
        protected string GetTrimmedDisplayName(string completeDisplayName)
        {
            string dispName = Regex.Replace(completeDisplayName, "Digital Television 2", " ");
            dispName = Regex.Replace(dispName, "Digital Television", " ");
            if (dispName.Length == completeDisplayName.Length)
            {
                dispName = Regex.Replace(dispName, "Digital Display 2", " ");
                dispName = Regex.Replace(dispName, "Digital Display", " ");
            }
            return dispName.Trim();
        }

        protected void ApplyConfigOS(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());
        }
        protected void VerifyConfigOS(DisplayConfig argDisplayConfig)
        {
            Log.Message(true, "Verifying config {0} via OS", argDisplayConfig.GetCurrentConfigStr());
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            if (currentConfig.GetCurrentConfigStr().Equals(argDisplayConfig.GetCurrentConfigStr()))
                Log.Success("{0} is verified by OS", argDisplayConfig.GetCurrentConfigStr());
            else
                Log.Fail("Config {0} does not match with current config {1}", argDisplayConfig.GetCurrentConfigStr(), currentConfig.GetCurrentConfigStr());
        }
        protected void InvokePowerEvent(PowerStates argPowerState)
        {
            Log.Message(true, "Invoking power event {0}", argPowerState);
            PowerParams powerParams = new PowerParams() { Delay = 30 };
            powerParams.PowerStates = argPowerState;
            base.EventResult(powerParams.PowerStates, base.InvokePowerEvent(powerParams, powerParams.PowerStates));
        }
        protected void PerformSemiautomated(string argSemiautomatedDisp)
        {
            Log.Message(true, "{0} semi automated", argSemiautomatedDisp);
            AccessInterface.SetFeature<bool, string>(Features.PromptMessage, Action.SetMethod, argSemiautomatedDisp);
        }
    }
}

