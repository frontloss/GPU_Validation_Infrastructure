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
    class SB_HDMI_YCBCR_Plug_Unplug_XVYCC_S3 : SB_HDMI_YCBCR_Basic
    {
        private string edidFileAfterPanelChange = "HDMI_DELL_U2711_XVYCC.EDID";
        private PowerStates powerState;
        public SB_HDMI_YCBCR_Plug_Unplug_XVYCC_S3()
            : base()
        {
            base._actionAfterEnable = this.ActionAfterEnable;
            base._actionAfterDisable = this.ActionAfterDisable;
            this.powerState = PowerStates.S3;
        }
        public SB_HDMI_YCBCR_Plug_Unplug_XVYCC_S3(PowerStates argPowerState)
            : this()
        {
            this.powerState = argPowerState;
        }

        private void ActionAfterEnable()
        {
            Log.Message(true, "Unplug the Panel while in {0}", powerState);
            if (displayInfo.ColorInfo.IsYcBcr)
            {
                Log.Message(true, "Unplug the Panel while in {0}", powerState);
                base.HotUnPlug(displayInfo.DisplayType, true);

                Log.Message("Putting the system into {0} state", powerState);
                PowerParams powerParams = new PowerParams();
                powerParams.Delay = 40;
                base.InvokePowerEvent(powerParams, powerState);
                Thread.Sleep(1000);
                
                Log.Message(true, "After {0}, plug an XVYCC Panel and check XVYCC is disabled", powerState);
                base.HotPlug(displayInfo.DisplayType, edidFileAfterPanelChange);
                base.CheckConfigChange(base.CurrentConfig);
                //base.CheckCRC();
                Log.Message("Verify registers after Unplug and Plug");
                eventCalled = "XVYCC_DISABLE";
                base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, eventCalled);
                Log.Message(true, "Plug back the original panel");
                Log.Verbose("Unplug {0} panel on display {1}", _colorType, displayInfo.DisplayType);
                base.HotUnPlug(displayInfo.DisplayType);
                //base.CheckCRC();
                Log.Verbose("Plug panel on display {0}", displayInfo.DisplayType);
                base.HotPlug(displayInfo.DisplayType, edidFile);
                base.CheckConfigChange(base.CurrentConfig);
                //base.CheckCRC();
            }
            else
                Log.Message("Cannot plug and unplug {0}", displayInfo.DisplayType);

        }
        private void ActionAfterDisable()
        {
            Log.Message(true, "Unplug the panel while in {0}", powerState);
            if (displayInfo.ColorInfo.IsYcBcr)
            {
                base.HotUnPlug(displayInfo.DisplayType, true);

                Log.Message("Putting the system into {0} state", powerState);
                PowerParams powerParams = new PowerParams();
                powerParams.Delay = 40;
                base.InvokePowerEvent(powerParams, powerState);
                
                base.HotPlug(displayInfo.DisplayType, edidFileAfterPanelChange);
                base.CheckConfigChange(base.CurrentConfig);
                //base.CheckCRC();
                Log.Message("Verify registers after Unplug and Plug");
                eventCalled = "XVYCC_DISABLE";
                base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, eventCalled);
                //base.CheckCRC();
            }
            else
                Log.Message("Cannot plug and unplug {0}", displayInfo.DisplayType);
        }

        //private void ActionAfterEnable()
        //{
        //    Log.Message(true, "Unplug the Panel while in {0}",powerState);
        //    if (displayInfo.DvmuPort != DVMU_PORT.None && displayInfo.ColorInfo.IsYcBcr)
        //    {
        //        Log.Message(true, "Unplug the Panel while in {0}", powerState);
        //        Log.Verbose("Unplug {0} panel on display {0}", _colorType, displayInfo.DisplayType);
        //        HotPlugUnplug hotPlugUnplug = new HotPlugUnplug(FunctionName.UNPLUG, displayInfo.DisplayType, displayInfo.DvmuPort);
        //        hotPlugUnplug.Delay = 20;
        //        if (AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, hotPlugUnplug))
        //            Log.Success("{0}  will be HotPlugged in 10 Seconds after system go to {1}", displayInfo.DisplayType, powerState);
        //        else
        //            Log.Fail("{0} HotPlug Fail", displayInfo.DisplayType);
        //        Log.Message("Putting the system into {0} state", powerState);
        //        PowerParams powerParams = new PowerParams();
        //        powerParams.Delay = 40;
        //        base.InvokePowerEvent(powerParams, powerState);
        //        Thread.Sleep(1000);
        //        Log.Message(true, "After {0}, plug an YCBCR Panel and check YCBCR is enabled", powerState);
        //        base.Hotplug(FunctionName.UnplugEnumerate, displayInfo.DisplayType, displayInfo.DvmuPort);
        //        base.Hotplug(FunctionName.PLUG, displayInfo.DisplayType, displayInfo.DvmuPort, edidFileAfterPanelChange);
        //        base.CheckConfigChange(base.CurrentConfig);
        //        //base.CheckCRC();
        //        Log.Message("Verify registers after Unplug and Plug");
        //        eventCalled = "XVYCC_ENABLE";
        //        base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, eventCalled);
        //        Log.Message(true, "Plug back the original panel");
        //        Log.Verbose("Unplug {0} panel on display {1}", _colorType, displayInfo.DisplayType);
        //        base.Hotplug(FunctionName.UNPLUG, displayInfo.DisplayType, displayInfo.DvmuPort);
        //        //base.CheckCRC();
        //        Log.Verbose("Plug panel on display {0}", displayInfo.DisplayType);
        //        base.Hotplug(FunctionName.PLUG, displayInfo.DisplayType, displayInfo.DvmuPort, edidFile);
        //        base.CheckConfigChange(base.CurrentConfig);
        //        //base.CheckCRC();
        //    }
        //    else
        //        Log.Message("Cannot plug and unplug {0}", displayInfo.DisplayType);
           
        //}
        //private void ActionAfterDisable()
        //{
        //    Log.Message(true, "Unplug the panel while in {0}",powerState);
        //    if (displayInfo.DvmuPort != DVMU_PORT.None && displayInfo.ColorInfo.IsYcBcr)
        //    {
        //        HotPlugUnplug hotPlugUnplug = new HotPlugUnplug(FunctionName.UNPLUG, displayInfo.DisplayType, displayInfo.DvmuPort);
        //        hotPlugUnplug.Delay = 10;
        //        if (AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, hotPlugUnplug))
        //            Log.Success("{0}  will be HotPlugged in 10 Seconds after system go to S3", displayInfo.DisplayType);
        //        else
        //            Log.Fail("{0} HotPlug Fail", displayInfo.DisplayType);
        //        Log.Message("Putting the system into {0} state", powerState);
        //        PowerParams powerParams = new PowerParams();
        //        powerParams.Delay = 40;
        //        base.InvokePowerEvent(powerParams, powerState);
        //        base.Hotplug(FunctionName.UnplugEnumerate, displayInfo.DisplayType, displayInfo.DvmuPort);
        //        base.Hotplug(FunctionName.PLUG, displayInfo.DisplayType, displayInfo.DvmuPort, edidFileAfterPanelChange);
        //        base.CheckConfigChange(base.CurrentConfig);
        //        //base.CheckCRC();
        //        Log.Message("Verify registers after Unplug and Plug");
        //        eventCalled = "XVYCC_DISABLE";
        //        base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, eventCalled);
        //        //base.CheckCRC();
        //    }
        //    else
        //        Log.Message("Cannot plug and unplug {0}", displayInfo.DisplayType);
        //}       
    }
}
