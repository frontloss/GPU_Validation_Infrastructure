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
    class SB_HDMI_XVYCC_S3 : SB_HDMI_XVYCC_Basic
    {
        protected PowerStates powerState;
        PowerParams _powerParams = null;
        public SB_HDMI_XVYCC_S3()
            : base()
        {
            base._actionAfterEnable = this.ActionAfterEnable;
            base._actionAfterDisable = this.ActionAfterDisable;
            this.powerState = PowerStates.S3;
        }
        public SB_HDMI_XVYCC_S3(PowerStates argPowerState)
            : this()
        {
            this.powerState = argPowerState;
        }
        private void ActionAfterEnable()
        {
            Log.Message(true, "Goto {0} and Resume", powerState);
            Thread.Sleep(5000);
            this._powerParams = new PowerParams() { Delay = 30, };
            base.InvokePowerEvent(this._powerParams, this.powerState);
            base.MoveCursorToPrimary(_intialConfig);
            base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, eventCalled);
            //base.CheckCRC();
        }
        private void ActionAfterDisable()
        {
            Log.Message(true, "Goto {0} and Resume", powerState);
            Thread.Sleep(5000);
            this._powerParams = new PowerParams() { Delay = 30, };
            base.InvokePowerEvent(this._powerParams, this.powerState);
            base.MoveCursorToPrimary(_intialConfig);
            base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, eventCalled);
            //base.CheckCRC();
        }       
    }
}
