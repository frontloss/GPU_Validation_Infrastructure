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
    class SB_HDMI_XVYCC_Plug_Unplug_Non_XVYCC_YCBCR_S3 : SB_HDMI_XVYCC_Basic
    {
        private string edidFileAfterPanelChange = "HDMI_3011_xvycc_Remove_RGB.EDID";
        private PowerStates powerState;
        public SB_HDMI_XVYCC_Plug_Unplug_Non_XVYCC_YCBCR_S3()
            : base()
        {
            base._actionAfterEnable = this.ActionAfterEnable;
            base._actionAfterDisable = this.ActionAfterDisable;
            this.powerState = PowerStates.S3;
        }
        public SB_HDMI_XVYCC_Plug_Unplug_Non_XVYCC_YCBCR_S3(PowerStates argPowerState)
            : this()
        {
            this.powerState = argPowerState;
        }
        private void ActionAfterEnable()
        {
            Log.Message(true, "Unplug the Panel while in {0}", powerState);
            if (displayInfo.ColorInfo.IsXvYcc)
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
                base.CheckConfigChange(base.CurrentConfig);
                //base.CheckCRC();
                //List<DisplayInfo> enumeratedDisplay = AccessInterface.GetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);
                //DisplayInfo displayInfoAfterPlug = enumeratedDisplay.Where(dI => dI.DisplayType == displayInfo.DisplayType).First();
                //Log.Message("Check if the xvycc/ycbcr option is not coming in CUI");
                //base.VerifyNonXvyccYcvcrPanel(displayInfo.DisplayType);
                Log.Message("Verify registers for Non-Xvycc/Ycbcr panel");
                base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, nonHDMIPanelEvent);
                Log.Message(true, "Plug back the original panel");
                Log.Verbose("Unplug {0} panel on display {0}", _colorType, displayInfo.DisplayType);
                base.HotUnPlug(displayInfo.DisplayType);
                //base.CheckCRC();
                Log.Verbose("Plug back {0} panel on display {1}", _colorType, displayInfo.DisplayType);
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
            if (displayInfo.ColorInfo.IsXvYcc)
            {
                base.HotUnPlug(displayInfo.DisplayType, true);

                Log.Message("Putting the system into {0} state", powerState);
                PowerParams powerParams = new PowerParams();
                powerParams.Delay = 40;
                base.InvokePowerEvent(powerParams, powerState);

                base.HotPlug(displayInfo.DisplayType, edidFileAfterPanelChange);
                //base.CheckCRC();
                base.CheckConfigChange(base.CurrentConfig);
                //DisplayInfo displayInfoAfterPlug = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == displayInfo.DisplayType).First();
                ////Log.Message("Check if the xvycc/ycbcr option is not coming in CUI");
                ////base.VerifyNonXvyccYcvcrPanel(displayInfo.DisplayType);
                Log.Message("Verify registers for Non-Xvycc/Ycbcr panel");
                base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, nonHDMIPanelEvent);
                //base.CheckCRC();
            }
            else
                Log.Message("Cannot plug and unplug {0}", displayInfo.DisplayType);
        }       
    }
}
