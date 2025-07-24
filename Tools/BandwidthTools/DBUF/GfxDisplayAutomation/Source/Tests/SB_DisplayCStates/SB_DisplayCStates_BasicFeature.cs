namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using System;

    class SB_DisplayCStates_BasicFeature : SB_DisplayCStates_Base
    {
        protected bool isEDP = true;
        protected bool isBXT = false;
        protected bool isIdle = false;
        protected bool isVideo = true;
        private uint DMCVersion = 0;
        [Test(Type = TestType.PreCondition, Order = 1)]
        public virtual void TestPreCondition()
        {
            DMCVersion = GetRegisterValue("DMC_VERSION", PIPE.NONE, PLANE.NONE, PORT.NONE);
            Log.Message(true, "DMC Version for {0}", DMCVersion);  
            isBXT = this.MachineInfo.PlatformDetails.Platform == Platform.BXT ? true : false;
            Log.Message(true, "Set config SD internal panel");
            DisplayConfig displayConfig = new DisplayConfig()
            {
                ConfigType = DisplayConfigType.SD,
                PrimaryDisplay = DisplayType.EDP
            };
            if (base.CurrentConfig.CustomDisplayList.Contains(DisplayType.MIPI))
            {
                displayConfig.PrimaryDisplay = DisplayType.MIPI;
                isEDP = false;
            }
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, displayConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public virtual void Method()
        {
            Log.Message(true, "Verify DC-State with system in Monitor Turn Off for 2 minutes.");
            List<DCStateOutput> returnType = new List<DCStateOutput>();
            if (isEDP)
                returnType = base.DisplayCStateEDP(isBXT,isIdle);
            else
                returnType = base.DisplayCStateMIPI(isVideo,isIdle);
            if (returnType.Count == 0)
            {
                Log.Fail("Display C State not switched");
            }
            else
            {
                if (returnType.Contains(DCStateOutput.DC9) || returnType.Contains(DCStateOutput.DC6))
                    Log.Success("DC6/DC9 state achieved");
                else
                    if (returnType.Contains(DCStateOutput.DC5))
                        Log.Fail("System Enabled upto DC5 only");
            }
        }
    } 
}