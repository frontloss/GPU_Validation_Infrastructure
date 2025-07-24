namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using IgfxExtBridge_DotNet;
    using System.Xml.Linq;
    using System.IO;
    using System.Text;
    using System;
    using System.Threading;

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_HDMI_YCBCR_Overlay_Plug_Unplug_XVYCC_S3 : SB_HDMI_YCBCR_Overlay_Basic
    {
        protected PowerStates powerState;
        private string edidFileAfterPanelChange = "HDMI_DELL_U2711_XVYCC.EDID";
        public SB_HDMI_YCBCR_Overlay_Plug_Unplug_XVYCC_S3() 
            : base()
        {
            base._actionAfterEnable = this.ActionAfterEnable;
            base._actionAfterDisable = this.ActionAfterDisable;
            this.powerState = PowerStates.S3;
        }

        public SB_HDMI_YCBCR_Overlay_Plug_Unplug_XVYCC_S3(PowerStates argPowerState)
            : this()
        {
            this.powerState = argPowerState;
        }

        private void ActionAfterEnable()
        {
            Log.Message(true, "Unplug and Plug Panel");
            if (displayInfo.ColorInfo.IsYcBcr)
            {
                Log.Verbose("Unplug {0} panel on display {0}", _colorType, displayInfo.DisplayType);
                base.HotUnPlug(displayInfo.DisplayType, true);

                Log.Message("Putting the system into {0} state", powerState);
                PowerParams powerParams = new PowerParams();
                powerParams.Delay = 40;
                base.InvokePowerEvent(powerParams, powerState);
                Thread.Sleep(1000);

                Log.Message(true, "After {0}, plug an YCBCR Panel and check YCBCR is enabled", powerState);
                base.HotPlug(displayInfo.DisplayType, edidFileAfterPanelChange);
                //base.CheckCRC();
                base.MoveCursorToPrimary(base.CurrentConfig);
                base.StopVideo(dh, base.CurrentConfig);
                base.PlayAndMoveVideo(dh, base.CurrentConfig);
                Log.Message("Verify registers after Unplug and Plug");
                if ((dh != DisplayHierarchy.Display_1) && (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
                    eventCalled = "XVYCC_DISABLED_CLONE_SPRITE_DISABLED";
                else
                    eventCalled = "XVYCC_DISABLED_SPRITE_ENABLED";
                base.RegisterCheck(displayInfo.DisplayType, displayInfo, dh, eventCalled);
                Log.Message(true, "Plug back the original panel");
                Log.Verbose("Unplug {0} panel on display {1}", _colorType, displayInfo.DisplayType);
                base.HotUnPlug(displayInfo.DisplayType);
                //base.CheckCRC();
                Log.Verbose("Plug panel on display {0}", displayInfo.DisplayType);
                base.HotPlug(displayInfo.DisplayType, edidFile);
                base.StopVideo(dh, base.CurrentConfig);
                base.CheckConfigChange(_intialConfig);
                //base.CheckCRC();
            }
            else
                Log.Message("Cannot plug and unplug {0}", displayInfo.DisplayType); ;
        }
        private void ActionAfterDisable()
        {
            Log.Message(true, "Unplug and Plug Panel");
            if (displayInfo.ColorInfo.IsYcBcr)
            {
                Log.Message(true, "Unplug the panel while in {0}", powerState);
                base.HotUnPlug(displayInfo.DisplayType, true);

                Log.Message("Putting the system into {0} state", powerState);
                PowerParams powerParams = new PowerParams();
                powerParams.Delay = 40;
                base.InvokePowerEvent(powerParams, powerState);
                
                base.HotPlug(displayInfo.DisplayType, edidFileAfterPanelChange);
                //base.CheckCRC();
                base.CheckConfigChange(_intialConfig);
                base.MoveCursorToPrimary(base.CurrentConfig);
                base.StopVideo(dh, base.CurrentConfig);
                base.PlayAndMoveVideo(dh, base.CurrentConfig);
                Log.Message("Verify registers after Unplug and Plug");
                if ((dh != DisplayHierarchy.Display_1) && (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
                    eventCalled = "XVYCC_DISABLED_CLONE_SPRITE_DISABLED";
                else
                    eventCalled = "XVYCC_DISABLED_SPRITE_ENABLED";
                base.RegisterCheck(displayInfo.DisplayType, displayInfo, dh, eventCalled);
                base.StopVideo(dh, base.CurrentConfig);
                //base.CheckCRC();
            }
            else
                Log.Message("Cannot plug and unplug {0}", displayInfo.DisplayType);
        }       

        //private void ActionAfterEnable()
        //{
        //    Log.Message(true, "Unplug and Plug Panel");
        //    if (displayInfo.DvmuPort != DVMU_PORT.None && displayInfo.ColorInfo.IsYcBcr)
        //    {
        //        Log.Verbose("Unplug {0} panel on display {0}", _colorType, displayInfo.DisplayType);
        //        HotPlugUnplug hotPlugUnplug = new HotPlugUnplug(FunctionName.UNPLUG, displayInfo.DisplayType, displayInfo.DvmuPort);
        //        hotPlugUnplug.Delay = 20;
        //        if (AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, hotPlugUnplug))
        //            Log.Success("{0}  will be HotPlugged in 10 Seconds after system go to S3", displayInfo.DisplayType);
        //        else
        //            Log.Fail("{0} HotPlug Fail", displayInfo.DisplayType);
        //        Log.Message("Putting the system into {0} state", PowerStates.S3);
        //        PowerParams powerParams = new PowerParams();
        //        powerParams.Delay = 40;
        //        base.InvokePowerEvent(powerParams, PowerStates.S3);
        //        Thread.Sleep(1000);
        //        Log.Message(true, "After S3, plug an YCBCR Panel and check YCBCR is enabled");
        //        base.Hotplug(FunctionName.UnplugEnumerate, displayInfo.DisplayType, displayInfo.DvmuPort);
        //        base.Hotplug(FunctionName.PLUG, displayInfo.DisplayType, displayInfo.DvmuPort, edidFileAfterPanelChange);
        //        //base.CheckCRC();
        //        Thread.Sleep(5000);
        //        base.MoveCursorToPrimary(base.CurrentConfig);
        //        base.StopVideo(dh, base.CurrentConfig);
        //        base.PlayAndMoveVideo(dh, base.CurrentConfig);
        //        Thread.Sleep(5000);
        //        Log.Message("Verify registers after Unplug and Plug");
        //        if ((dh != DisplayHierarchy.Display_1) && (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
        //            eventCalled = "XVYCC_DISABLED_CLONE_SPRITE_DISABLED";
        //        else
        //            eventCalled = "XVYCC_DISABLED_SPRITE_ENABLED";
        //        base.RegisterCheck(displayInfo.DisplayType, displayInfo, dh, eventCalled);
        //        Log.Message(true, "Plug back the original panel");
        //        Log.Verbose("Unplug {0} panel on display {1}", _colorType, displayInfo.DisplayType);
        //        base.Hotplug(FunctionName.UNPLUG, displayInfo.DisplayType, displayInfo.DvmuPort);
        //        //base.CheckCRC();
        //        Log.Verbose("Plug panel on display {0}", displayInfo.DisplayType);
        //        base.Hotplug(FunctionName.PLUG, displayInfo.DisplayType, displayInfo.DvmuPort, edidFile);
        //        base.CheckConfigChange(_intialConfig);
        //        //base.CheckCRC();
        //    }
        //    else
        //        Log.Message("Cannot plug and unplug {0}", displayInfo.DisplayType); ;
        //}
        //private void ActionAfterDisable()
        //{
        //    Log.Message(true, "Unplug and Plug Panel");
        //    if (displayInfo.DvmuPort != DVMU_PORT.None && displayInfo.ColorInfo.IsYcBcr)
        //    {
        //        Log.Message(true, "Unplug the panel while in S3");
        //        HotPlugUnplug hotPlugUnplug = new HotPlugUnplug(FunctionName.UNPLUG, displayInfo.DisplayType, displayInfo.DvmuPort);
        //        hotPlugUnplug.Delay = 10;
        //        if (AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, hotPlugUnplug))
        //            Log.Success("{0}  will be HotPlugged in 10 Seconds after system go to S3", displayInfo.DisplayType);
        //        else
        //            Log.Fail("{0} HotPlug Fail", displayInfo.DisplayType);
        //        Log.Message("Putting the system into {0} state", PowerStates.S3);
        //        PowerParams powerParams = new PowerParams();
        //        powerParams.Delay = 40;
        //        base.InvokePowerEvent(powerParams, PowerStates.S3);
        //        base.Hotplug(FunctionName.UnplugEnumerate, displayInfo.DisplayType, displayInfo.DvmuPort);
        //        base.Hotplug(FunctionName.PLUG, displayInfo.DisplayType, displayInfo.DvmuPort, edidFileAfterPanelChange);
        //        //base.CheckCRC();
        //        base.CheckConfigChange(_intialConfig);
        //        Thread.Sleep(5000);
        //        base.MoveCursorToPrimary(base.CurrentConfig);
        //        base.StopVideo(dh, base.CurrentConfig);
        //        base.PlayAndMoveVideo(dh, base.CurrentConfig);
        //        Thread.Sleep(5000);
        //        Log.Message("Verify registers after Unplug and Plug");
        //        if ((dh != DisplayHierarchy.Display_1) && (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
        //            eventCalled = "XVYCC_DISABLED_CLONE_SPRITE_DISABLED";
        //        else
        //            eventCalled = "XVYCC_DISABLED_SPRITE_ENABLED";
        //        base.RegisterCheck(displayInfo.DisplayType, displayInfo, dh, eventCalled);
        //        //base.CheckCRC();
        //    }
        //    else
        //        Log.Message("Cannot plug and unplug {0}", displayInfo.DisplayType);
        //}       
    }
}
