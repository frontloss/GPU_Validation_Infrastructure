using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_MBO_Rotation : SB_MBO_Basic
    {
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            DisplayMode mode = base.GetAppliedMode(DisplayType.EDP);
            UpdateRotationAngle(mode);
            base.StopVideo();
            base.CleanUpHotplugFramework();
        }
        private void UpdateRotationAngle(DisplayMode argDispMode)
        {
            Log.Message(true, "Applying rotation to {0}", argDispMode.display);
            this.ApplyRotationAngles(argDispMode);
            argDispMode.Angle = 90;
            this.ApplyRotationAngles(argDispMode);
            argDispMode.Angle = 180;
            this.ApplyRotationAngles(argDispMode);
            argDispMode.Angle = 270;
            this.ApplyRotationAngles(argDispMode);
            argDispMode.Angle = 0;
            this.ApplyRotationAngles(argDispMode);
        }
        private void ApplyRotationAngles(DisplayMode argDisplayMode)
        {
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argDisplayMode))
            {
                Log.Success("Angle: {0} applied successfully to {1}", argDisplayMode.Angle, argDisplayMode.GetCurrentModeStr(true));
                DisplayInfo curDispInfo = base.CurrentConfig.EnumeratedDisplays.Where(di => di.DisplayType == argDisplayMode.display).FirstOrDefault();
                DisplayMode curDispMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Rotation, Action.GetMethod, Source.AccessAPI, curDispInfo);
                curDispMode.VerifyOrientation();
                base.VerifyMBOEnable();
            }
            else
            {
                Log.Fail("Failed to rotate {0} by {1}", argDisplayMode.GetCurrentModeStr(false), argDisplayMode.Angle);
            }
        }
    }
}
