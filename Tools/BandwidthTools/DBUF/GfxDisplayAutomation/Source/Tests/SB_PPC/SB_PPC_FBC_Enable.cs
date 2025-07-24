namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;

    class SB_PPC_FBC_Enable : SB_PPC_Config_Basic
    {
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            bool current_Status = VerifyRegisters("FBC_REGISTER", PIPE.PIPE_A, PLANE.NONE, PORT.NONE, false);

            if (base.CurrentConfig.ConfigType == DisplayConfigType.SD && base.CurrentConfig.PrimaryDisplay == DisplayType.EDP)
            {
                if (current_Status)
                {
                    Log.Success("FBC Enabled as per expected for {0}", base.CurrentConfig.GetCurrentConfigStr());
                }
                else
                {
                    Log.Fail("FBC Not Enabled for {0}", base.CurrentConfig.GetCurrentConfigStr());
                }
            }
            else
            {
                if (current_Status)
                {
                    Log.Fail("FBC Not Enabled for {0}", base.CurrentConfig.GetCurrentConfigStr());
                }
                else
                {
                    Log.Success("FBC Enabled as per expected for {0}", base.CurrentConfig.GetCurrentConfigStr());
                }
            }
        }
    }
}