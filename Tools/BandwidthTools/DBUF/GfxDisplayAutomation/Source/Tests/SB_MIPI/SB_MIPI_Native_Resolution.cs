using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_MIPI_Native_Resolution: SB_MIPI_Base
    {
        protected bool IsMipiVideoMode = false;
        protected List<PORT> availablePorts = new List<PORT> { PORT.PORTA, PORT.PORTC };

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPrerequisite()
        {
            if (!base.CurrentConfig.CustomDisplayList.Contains(DisplayType.MIPI))
                Log.Abort("This test requires MIPI display as active panel.");

            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("{0} Applied successfully", base.CurrentConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", base.CurrentConfig.GetCurrentConfigStr());
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            DisplayInfo displayInfo = this.CurrentConfig.EnumeratedDisplays.Find(dispInfo => dispInfo.DisplayType == DisplayType.MIPI);

            base.CurrentConfig.CustomDisplayList.ForEach(disp =>
                      {
                          ApplyNativeMode(disp);
                      });

            StartMouseMovement();

            IsMipiVideoMode = IsMipiVideoModePanel(displayInfo.Port);

            if (IsMipiVideoMode)
                StopMouseMovement();

            bool isDualLinkEnabled = VerifyRegisters(MIPI_DUAL_LINK_MODE, PIPE.NONE, PLANE.NONE, displayInfo.Port, false);
            if (isDualLinkEnabled)
            {
                Log.Message("Data is driven in Dual Link mode");
            }
            else
            {
                availablePorts.Clear();
                availablePorts.Add(displayInfo.Port);
            }

            VerifyRegisters();

            if (!IsMipiVideoMode)
                StopMouseMovement();
        }
        protected virtual void VerifyRegisters()
        {
           
        }

        protected void VerifyRegisters(string eventName, PORT port)
        {
            bool isfeatureEnabled = VerifyRegisters(eventName, PIPE.NONE, PLANE.NONE, port, false);

            if (isfeatureEnabled)
                Log.Success("{0} is enabled with Port:{1}", eventName, port);
            else
                Log.Fail("{0} not enabled with Port:{1}", eventName, port);
        }
    }
}
