namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;

    class SB_PPC_LPSP : SB_PPC_Config_Basic
    {
        protected const string LPSP_REGISTER_EVENT = "LPSP_ENABLE";
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            bool isLPSPEnable=false;
            if (base.CurrentConfig.ConfigType == DisplayConfigType.SD)
            {
                isLPSPEnable = true;
            }

            LPSPRegisterVerify(isLPSPEnable);
        }

        protected void LPSPRegisterVerify(bool pEnable)
        {
            if (VerifyRegisters(LPSP_REGISTER_EVENT, PIPE.NONE, PLANE.NONE, PORT.PORTA,false))
            {
                if (pEnable)
                    Log.Success("LPSP is Enable");
                else
                    Log.Fail("LPSP is Enable");
            }
            else
            {
                if (!pEnable)
                    Log.Success("LPSP is Disable");
                else
                    Log.Fail("LPSP is Disable");
            }
        }
    }
}