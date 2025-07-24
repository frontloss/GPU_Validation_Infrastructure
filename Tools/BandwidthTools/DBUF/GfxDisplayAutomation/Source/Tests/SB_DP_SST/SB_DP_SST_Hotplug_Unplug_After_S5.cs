using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_DP_SST_Hotplug_Unplug_After_S5 : SB_DP_SST_Base
    {
        int delay = 30;
        PowerParams _powerParams = new PowerParams();

        //Put System into Connected Stand By state
        [Test(Type = TestType.Method, Order = 1)]
        public void putInS5()
        {
            //Delay can be modified as per requirement
            _powerParams.Delay = delay;

            Log.Message("#### To test S5, we need to devise mechanism to restart device post S5 ####");
            Log.Message("#### Till such mechanism is developed, we will just shut down device #### ");
            //Put system into CS state by invoking power event
            base.InvokePowerEvent(_powerParams, PowerStates.S5);
        }
    }
}
