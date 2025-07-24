using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
namespace Intel.VPG.Display.Automation
{
    class SB_DeepColor_Plug_NonDeepcolor_S3_DPApplet : SB_Deepcolor_DisplayConfig_DPApplet
    {
        protected PowerStates powerState;
        public SB_DeepColor_Plug_NonDeepcolor_S3_DPApplet()
            : base()
        {
            this.powerState = PowerStates.S3;
            base._actionAfterEnable = this.ActionAfterEnable;
        }
        public SB_DeepColor_Plug_NonDeepcolor_S3_DPApplet(PowerStates argPowerState)
            : this()
        {
            this.powerState = argPowerState;
        }
        private void ActionAfterEnable()
        {
            base.CurrentConfig.PluggableDisplayList.Intersect(_nonDeepColorEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                Log.Message("UnPlugging {0} Deepcolor supported panel in low power state.", curDisp);
                base.HotUnPlug(curDisp, true);

                Log.Message("Hotplug {0} Non Deepcolor supported panel in low power state.", curDisp);

                DisplayInfo displayInfo = base.EnumeratedDisplays.Where(item => item.DisplayType == curDisp).FirstOrDefault();
                base.HotPlug(curDisp, true, displayInfo.WindowsMonitorID, base._nonDeepColorEDIDMap[curDisp], true);
            });

            GotoPowerState();

            AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig);

            base.TestStep2();

            base.CurrentConfig.PluggableDisplayList.Intersect(_nonDeepColorEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                base.HotUnPlug(curDisp);

                Log.Message("Hotplug {0} Non Deepcolor supported panel.", curDisp);
                base.HotPlug(curDisp, _defaultEDIDMap[curDisp]);
            });
        }

        private void GotoPowerState()
        {
            Log.Message("Putting the system into {0} state & resume", this.powerState);
            PowerParams powerParams = new PowerParams();
            powerParams.Delay = 15;
            base.InvokePowerEvent(powerParams, this.powerState);
            Log.Success("Put the system into {0} state & resumed", this.powerState);
        }
    }
}
