namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    using System.Threading;
    [Test(Type = TestType.HasPlugUnPlug)]
    public class SB_Modes_Hotplug_Unplug_S3 : SB_modes_Hotplug_Unplug_Basic
    {
        protected PowerParams _powerParams = null;
        protected override void PerformHotplugUnplug()
        {
            base.CurrentConfig.DisplayList.Intersect(_pluggableDisplay).ToList().ForEach(curDisp =>
            {
                Log.Message(true, "Unplugging {0} and will be plugged back", curDisp);
                int displaysCountBeforePlug = base.EnumeratedDisplays.Count;
                HotUnPlug(curDisp);
                Thread.Sleep(3000);
                HotPlug(curDisp, base._defaultEDIDMap[curDisp], true);
                InvokePowerEvent();
                
                if (displaysCountBeforePlug  == base.EnumeratedDisplays.Count)
                {
                    Log.Success("{0} UnPlug and plug Successful in power event", curDisp);                 
                }
                else
                {
                    Log.Fail("Unable to UnPlugand plug {0} in power event", curDisp);
                }
                base.CurrentConfig.DisplayList.ForEach(disp => CheckWatermark(disp));
            });

        }
        protected virtual void InvokePowerEvent()
        {
            Log.Message(true, "Invoking power event S3");
            this._powerParams = new PowerParams() { Delay = 30 };
            _powerParams.PowerStates = PowerStates.S3;
            _powerParams.Delay = 30;
            base.EventResult(_powerParams.PowerStates, base.InvokePowerEvent(_powerParams, _powerParams.PowerStates));
        }
    }
}
