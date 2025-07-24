namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;

    class SB_PPC_Cursor : SB_PPC_Config_Basic
    {
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            MoveCursorToPrimary(base.CurrentConfig);

            if (!VerifyRegisters("CURSOR_STATUS", PIPE.PIPE_A, PLANE.PLANE_A, PORT.NONE, false))
            {
                Log.Success("Cursor Enabled as per expected");
            }
            else
            {
                Log.Fail("Cursor Not Enabled");
            }
        }

        protected void MoveCursorToPrimary(DisplayConfig currentConfig)
        {
            MoveCursorPos moveToPri = new MoveCursorPos()
            {
                displayType = currentConfig.PrimaryDisplay,
                displayHierarchy = DisplayHierarchy.Display_1,
                currentConfig = currentConfig
            };
            AccessInterface.SetFeature<MoveCursorPos>(Features.MoveCursor, Action.Set, moveToPri);
        }
    }
}