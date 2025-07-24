namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using System;
    using System.Windows.Forms;

    class SB_DisplayCStates_PSR : SB_DisplayCStates_Base
    {
        private bool isEDP = true;
        private bool isBXT = false;
        private bool isIdle = true;
        private uint DMCVersion = 0;
        private bool isVideo = true;
        [Test(Type = TestType.PreCondition, Order = 1)]
        public void TestPreCondition()
        {
            DMCVersion = GetRegisterValue("DMC_VERSION", PIPE.NONE, PLANE.NONE, PORT.NONE);
            Log.Message(true, "DMC Version for {0}", DMCVersion);
            Log.Message(true, "Enable DC Mode");
            PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);

            if (powerState == PowerLineStatus.Online)
            {
                if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                    Log.Success("System is Running in DC Mode");
                else
                    Log.Fail("Fail to set DC Mode");
            }
            else
                Log.Success("System is Running in DC Mode");
            isBXT = this.MachineInfo.PlatformDetails.Platform == Platform.BXT ? true : false;
            Log.Message(true, "Set config SD internal panel");
            if (base.CurrentConfig.CustomDisplayList.Contains(DisplayType.MIPI))
            {
                Log.Abort("PSR test case needs to run on EDP Configuration. MIPI panel connected to the system");
            }
            DisplayConfig displayConfig = new DisplayConfig()
            {
                ConfigType = DisplayConfigType.SD,
                PrimaryDisplay = DisplayType.EDP
            };
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, displayConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void Method()
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
                    Log.Fail("DC6/DC9 state achieved.");
                else
                    if (returnType.Contains(DCStateOutput.DC5))
                        Log.Success("System Enabled upto DC5.");
            }
        }
    } 
}