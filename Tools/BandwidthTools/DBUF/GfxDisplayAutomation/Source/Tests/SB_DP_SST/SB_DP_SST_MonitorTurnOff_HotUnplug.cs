namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.IO;

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_DP_SST_MonitorTurnOff_HotUnplug : SB_DP_SST_Base
    {
        protected DisplayConfig configAfterPlug, configBeforePlug, configAfterUnPlug;
        public uint uiDPCDOffset = (uint)DPCDRegisters.DPCD_SINK_CONTROL; // Variable to hold DPCD offset

        [Test(Type = TestType.Method, Order = 1)]
        //Function to perform hotplugging of DP display during monitor turn-off
        public void DisplayHotplug()
        {
            configBeforePlug = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);

            // Hotplug external display using DFT
            if (base.CurrentConfig.SecondaryDisplay != DisplayType.None)
            {
                DisplayType Secondary = base.CurrentConfig.SecondaryDisplay;
                if (DisplayExtensions.GetDisplayType(Secondary) == DisplayType.DP)
                {
                    base.HotPlug(Secondary, _defaultEDIDMap[Secondary], false);

                    // Apply/Set SD on secondary Display
                    DisplayConfig sec = new DisplayConfig { ConfigType = DisplayConfigType.SD, PrimaryDisplay = Secondary };
                    ApplyConfigOS(sec);

                    configAfterPlug = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);

                    // Retrieve DisplayID of the external Display1
                    DisplayInfo curDispInfo = base.EnumeratedDisplays.Where(di => di.DisplayType == Secondary).FirstOrDefault();

                    VerifyDPCDRegisterValue(Secondary, uiDPCDOffset, DP_HOTPLUG_BITMAP, DP_HOTPLUG_GOLDENVALUE);
                    VerifyInOS(configBeforePlug, configAfterPlug, DisplayAction.HOTPLUG);
                }
                else
                {
                    Log.Fail("Config doesn't contain DP as Secondary Display");
                }
            }

            //If there is a Tertiary display is connected then execute below code
            if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
            {
                configBeforePlug = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
                DisplayType Tertiary = base.CurrentConfig.TertiaryDisplay;

                if ((DisplayExtensions.GetDisplayType(Tertiary) == DisplayType.DP) || (DisplayExtensions.GetDisplayType(Tertiary) == DisplayType.HDMI))
                {
                    base.HotPlug(Tertiary, _defaultEDIDMap[Tertiary], false);
                    // Apply/Set SD on Tertiary Display
                    DisplayConfig ter = new DisplayConfig { ConfigType = DisplayConfigType.SD, PrimaryDisplay = Tertiary };
                    ApplyConfigOS(ter);

                    configAfterPlug = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);

                    // Retrieve DisplayID of the external Display1
                    DisplayInfo curDispInfo1 = base.EnumeratedDisplays.Where(di => di.DisplayType == Tertiary).FirstOrDefault();

                    if (DisplayExtensions.GetDisplayType(Tertiary) == DisplayType.DP)
                    {
                        // Call VerifyDPCDRegisterValue function to read DPCD register value and compare against golden/expected values
                        VerifyDPCDRegisterValue(Tertiary, uiDPCDOffset, DP_HOTPLUG_BITMAP, DP_HOTPLUG_GOLDENVALUE);
                    }
                    VerifyInOS(configBeforePlug, configAfterPlug, DisplayAction.HOTPLUG);
                }               
            }
        }

        [Test(Type = TestType.Method, Order = 2)]
        //Function to do hotunplug during monitor turn off
        public void DisplayHotUnPlug()
        {
            if (base.CurrentConfig.SecondaryDisplay != DisplayType.None)
            {
                DisplayType Secondary = base.CurrentConfig.SecondaryDisplay;
                if (DisplayExtensions.GetDisplayType(Secondary) == DisplayType.DP)
                {
                    base.HotUnPlug(Secondary, true);
                    Log.Message("{0} display is hot-unplugged successfully", base.CurrentConfig.SecondaryDisplay);
                    MonitorTurnOffOn();
                }
                else
                {
                    Log.Message("Current Config doesn't contain DP as Secondary Display");
                }
            }
            //If there is a Tertiary display is connected then execute below code
            if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
            {
                DisplayType Tertiary = base.CurrentConfig.TertiaryDisplay;
                if ((DisplayExtensions.GetDisplayType(Tertiary) == DisplayType.DP) || (DisplayExtensions.GetDisplayType(Tertiary) == DisplayType.HDMI))
                {
                    base.HotUnPlug(Tertiary, true);
                    Log.Message("{0} display is hot-unplugged successfully", base.CurrentConfig.TertiaryDisplay);
                    MonitorTurnOffOn();
                }
                else
                {
                    Log.Message("Current Config doesn't contain DP as Secondary Display");
                }
            }
        }

        //To perform sleep/resume operation by Monitor TurnOff using display timer
        public void MonitorTurnOffOn()
        {
            Log.Message(true, "Turning Off Monitor for 1 min and resuming back");
            MonitorTurnOffParam monitorOnOffParam = new MonitorTurnOffParam();
            monitorOnOffParam.onOffParam = MonitorOnOff.OffOn;
            // Read monitor turnoff time from the Configuration file. 
            string HandletoFile = Path.Combine(Directory.GetCurrentDirectory(), "SB_DP_SST_MonitorTurnOff_WaitingTime.txt");
            string countStr = File.ReadAllText(HandletoFile);
            int waitingTime = Convert.ToUInt16(countStr.Trim());

            if (AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorOnOffParam))
            {
                Log.Success("Successfully Turn off monitor and resume back after {0} sec", waitingTime);
            }
        }
    }
}
