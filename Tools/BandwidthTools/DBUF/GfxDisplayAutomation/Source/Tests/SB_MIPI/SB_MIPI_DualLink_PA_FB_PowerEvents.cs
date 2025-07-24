using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_MIPI_DualLink_PA_FB_PowerEvents : SB_MIPI_Base
    {
        protected bool IsMipiVideoMode = false;
        Dual_Link_Mode dualLinkMode;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPrerequisite()
        {
            if (!base.CurrentConfig.CustomDisplayList.Contains(DisplayType.MIPI))
                Log.Abort("This test requires MIPI display as active panel.");

            dualLinkMode = GetMIPIDualLinkMode();
            if (!(dualLinkMode == Dual_Link_Mode.Dual_Link_Front_Back_Mode || dualLinkMode == Dual_Link_Mode.Dual_Link_Pixel_Alternative_Mode))
                Log.Abort("Should plan this test with Dual Link MIPI panel/VBT.");

            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("{0} Applied successfully", base.CurrentConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", base.CurrentConfig.GetCurrentConfigStr());
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            DisplayInfo displayInfo = this.CurrentConfig.EnumeratedDisplays.Find(dispInfo => dispInfo.DisplayType == DisplayType.MIPI);

            StartMouseMovement();

            IsMipiVideoMode = IsMipiVideoModePanel(displayInfo.Port);

            if (IsMipiVideoMode)
                StopMouseMovement();
            
            base.CurrentConfig.CustomDisplayList.ForEach(disp =>
                      {
                          ApplyNativeMode(disp);
                      });

            VerifyRegisters(displayInfo.Port);

            base.CurrentConfig.CustomDisplayList.ForEach(disp =>
            {
                ApplyNonNativeMode(disp);
            });

            VerifyRegisters(displayInfo.Port);
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            DisplayInfo displayInfo = this.CurrentConfig.EnumeratedDisplays.Find(dispInfo => dispInfo.DisplayType == DisplayType.MIPI);

           PowerEvent(PowerStates.S3);

            VerifyRegisters(displayInfo.Port);

            PowerEvent(PowerStates.S4);

            VerifyRegisters(displayInfo.Port);

            PowerEvent(PowerStates.S5);
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            DisplayInfo displayInfo = this.CurrentConfig.EnumeratedDisplays.Find(dispInfo => dispInfo.DisplayType == DisplayType.MIPI);

            StartMouseMovement();

            IsMipiVideoMode = IsMipiVideoModePanel(displayInfo.Port);

            if (IsMipiVideoMode)
                StopMouseMovement();

            VerifyRegisters(displayInfo.Port);

            if (!IsMipiVideoMode)
                StopMouseMovement();
        }
        private void PowerEvent(PowerStates powerState)
        {
            Log.Verbose("Putting the system into {0} state & resume ", powerState);
            PowerParams powerParams = new PowerParams();
            powerParams.Delay = 30;
            base.InvokePowerEvent(powerParams, powerState);
            Log.Success("Put the system into {0} state & resumed ", powerState);
        }
        protected void VerifyRegisters(PORT port)
        {
            List<PORT> availablePorts = new List<PORT> { PORT.PORTA, PORT.PORTC };

            bool isDualLinkEnabled = VerifyRegisters(MIPI_DUAL_LINK_MODE, PIPE.NONE, PLANE.NONE, port, false);
            if (isDualLinkEnabled)
            {
                Log.Success("Data is driven in Dual Link mode");
            }
            else
            {
                Log.Fail("Dual Link is not enabled.");
            }

            dualLinkMode = GetMIPIDualLinkMode();
            string st = Enum.GetName(typeof(Dual_Link_Mode), dualLinkMode);
            availablePorts.ForEach(eachPort =>
            {
                bool status = VerifyRegisters(st, PIPE.NONE, PLANE.NONE, eachPort, false);
                if (status)
                {
                    Log.Success("Data is driven in {0} for port:{1}", st, eachPort);
                }
                else
                {
                    Log.Fail("Data is not driver in {0} for port:{1}.", st, eachPort);
                }
            });
        }
    }
}
