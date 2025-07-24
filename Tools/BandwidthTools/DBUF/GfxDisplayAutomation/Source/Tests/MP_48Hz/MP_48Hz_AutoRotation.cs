namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Windows.Forms;
    using System.Threading;   
    using System.IO;
    using System.Diagnostics;
    using System.Collections.Generic;

    class MP_48Hz_AutoRotation : MP_48Hz_Basic
    {
        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            bool status_set = false;
            DisplayInfo displayInfo = null;
            uint angle = 180; // 48Hz can kick-in only in 0 & 180 rotation in landscape panels as we can do FS video playback in this only.
            DisplayMode targetMode;
            DisplayMode currentMode;
            base.TestStep5();
            displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == DisplayType.EDP).First();
            currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);

            Log.Message(true, "Setting rotation {0} for eDP", angle);
            currentMode.Angle = 180;
            status_set = AccessInterface.SetFeature<bool, DisplayMode>(Features.Rotation, Action.SetMethod, currentMode);
            targetMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Rotation, Action.GetMethod, Source.AccessAPI, displayInfo);
            if (status_set && targetMode.Angle.Equals(currentMode.Angle))
            {
                Log.Success("Rotation {0} successfully set for eDP", targetMode.Angle);
                Log.Message("Check for change in RR while clip is playing in the rotation angle {0}", targetMode.Angle);
                base.TestStep6();
            }
            else
            {
                Log.Fail("Unable to set rotation {0} for eDP", angle);
                Log.Message("Skipping RR change check as rotation for the angel {0} failed", targetMode.Angle);
            }
            
        }
    }
}
