namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    using System.Text.RegularExpressions;
    using System.IO;
    using System.Xml.Linq;
    using System.Xml.Serialization;
    using System.Xml;
    using System.Threading;
    using System.Runtime.InteropServices;

    public class SB_ULT_SymmetricScalar_FourPlane_Cursor : SB_ULT_SymmetricScalar_FourPlane
    {
        public SB_ULT_SymmetricScalar_FourPlane_Cursor()
        {
            DisableCursor = false;
        }

        [Test(Type = TestType.Method, Order = 7)]
        public override void TestStep7()
        {
            base.TestStep7();

            MoveCursorToPrimary(base.CurrentConfig);

            if (VerifyRegisters("CURSOR_STATUS", PIPE.PIPE_A, PLANE.NONE, PORT.NONE, true))
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




