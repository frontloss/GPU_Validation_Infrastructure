using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_ColorConversion_RGB_YUV_Overlay_S3:SB_ColorConversion_RGB_YUV_Overlay
    {
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true,"Invoke Power event S3");
            PowerParams powerParams = new PowerParams();
            powerParams.Delay=30;
            powerParams.PowerStates = PowerStates.S3;
            base.InvokePowerEvent(powerParams,PowerStates.S3);
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            base.TestStep2();
        }
    }
}
