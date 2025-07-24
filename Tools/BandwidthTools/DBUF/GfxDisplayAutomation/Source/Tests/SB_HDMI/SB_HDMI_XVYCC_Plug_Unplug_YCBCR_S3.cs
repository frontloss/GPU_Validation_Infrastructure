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
    class SB_HDMI_XVYCC_Plug_Unplug_YCBCR_S3 : SB_HDMI_XVYCC_Basic
    {
        private string edidFileAfterPanelChange = "HDMI_DELL.EDID";
        private PowerStates powerState;
        public SB_HDMI_XVYCC_Plug_Unplug_YCBCR_S3()
            : base()
        {
            base._actionAfterEnable = this.ActionAfterEnable;
            base._actionAfterDisable = this.ActionAfterDisable;
            this.powerState = PowerStates.S3;
        }
        public SB_HDMI_XVYCC_Plug_Unplug_YCBCR_S3(PowerStates argPowerState)
            : this()
        {
            this.powerState = argPowerState;
        }
        private void ActionAfterEnable()
        {
            if (displayInfo.ColorInfo.IsXvYcc)
            {
                Log.Message(true, "Unplug the Panel while in {0}", powerState);
                Log.Verbose("Unplug {0} panel on display {0}", _colorType, displayInfo.DisplayType);

                base.HotUnPlug(displayInfo.DisplayType, true);
                PowerParams powerParams = new PowerParams();
                powerParams.Delay = 40;
                base.InvokePowerEvent(powerParams, powerState);

                Thread.Sleep(1000);
                base.HotPlug(displayInfo.DisplayType, edidFileAfterPanelChange);
                base.CheckConfigChange(_intialConfig);
                //base.CheckCRC();
                Log.Message("Verify registers after Unplug and Plug");
                eventCalled = "YCBCR_DISABLE";
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
            Log.Message(true, "Unplug the panel while in {0}",powerState);
            if (displayInfo.ColorInfo.IsXvYcc)
            {
                base.HotUnPlug(displayInfo.DisplayType, true);
                PowerParams powerParams = new PowerParams();
                powerParams.Delay = 40;
                base.InvokePowerEvent(powerParams, powerState);
         
                base.HotPlug(displayInfo.DisplayType, edidFileAfterPanelChange);
                base.CheckConfigChange(_intialConfig);
                //base.CheckCRC();
                Log.Message("Verify registers after Unplug and Plug");
                eventCalled = "YCBCR_DISABLE";
                base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, eventCalled);
            }
            else
                Log.Message("Cannot plug and unplug {0}", displayInfo.DisplayType);
        }       
    }
}
