namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    using System.Windows.Forms;

    class MP_Stress_AC_DC : MP_Stress_Base
    {
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep1()
        {
           Log.Message(true, "Running AC-DC Stress Test for {0}", StressCycle);

           for (int i = 0; i < StressCycle; i++)
           {
               Log.Message(true, "Cycle --- {0} ", i);
               Log.Message(true, "Enable AC Mode");
               PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);

               if (powerState == PowerLineStatus.Offline)
               {
                   if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                       Log.Success("System is Running in AC Mode");
                   else
                       Log.Fail("Fail to set AC mode");
               }
               else
                   Log.Success("System is Running in AC Mode");

               Log.Message(true, "Enable DC Mode");
               powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);

               if (powerState == PowerLineStatus.Online)
               {
                   if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                       Log.Success("System is Running in DC Mode");
                   else
                       Log.Fail("Fail to set DC Mode");
               }
               else
                   Log.Success("System is Running in DC Mode");

           }
        }
    }
}
