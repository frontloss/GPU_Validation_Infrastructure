using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
namespace Intel.VPG.Display.Automation
{
    class MP_Rotation_Basic : TestBase
    {
        protected Dictionary<DisplayUnifiedConfig, System.Action> _rotate = null;
        protected List<uint> _angle = null;
        protected DisplayConfig curAppliedConfig = null;
        protected List<DisplayMode> curAppliedMode = new List<DisplayMode>();

        public MP_Rotation_Basic()
        {
            _rotate = new Dictionary<DisplayUnifiedConfig, System.Action>() { { DisplayUnifiedConfig.Clone, RotatePrimary }, { DisplayUnifiedConfig.Extended, RotateAll }, { DisplayUnifiedConfig.Single, RotateAll } };
            _angle = new List<uint>();
        }
        protected void RotatePrimary()
        {
            //DisplayType primary = curAppliedConfig.PrimaryDisplay;
            //DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == primary).First();
            //DisplayMode mode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            //DisplayMode mode = base.EnumeratedDisplays.Where(dI => dI.DisplayType == curAppliedConfig.PrimaryDisplay).Select(dI => dI.DisplayMode).FirstOrDefault();

            Log.Message("Scaling out is {0}", curAppliedMode.First().ScalingOptions.Count());
            RotateNVerify(curAppliedMode.First(), _angle.First());
        }
        protected void RotateAll()
        {
            for (int i = 0; i < _angle.Count; i++)
            {
                DisplayType disp = curAppliedConfig.DisplayList.ElementAt(i);
                DisplayMode mode = curAppliedMode.ElementAt(i);
                RotateNVerify(mode, _angle.ElementAt(i));
            }
        }
        protected void ApplyConfig(DisplayConfig argDispConfig)
        {
            Log.Message(true, "Applying config {0}", argDispConfig.GetCurrentConfigStr());
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("Config applied successfully");
            else
                Log.Abort("Failed to apply config, The Displays are {0}", argDispConfig.GetCurrentConfigStr());

            curAppliedMode = new List<DisplayMode>();
            if (argDispConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone || argDispConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Single)
            {
                DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDispConfig.PrimaryDisplay).First();
                DisplayMode mode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
                curAppliedMode.Add(mode);
            }
            else
            {
                argDispConfig.DisplayList.ForEach(curDisp =>
                {
                    DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).First();
                    DisplayMode mode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
                    curAppliedMode.Add(mode);
                    // base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();
                });
            }
        }
        protected void ApplyMode(DisplayMode argDispMode)
        {
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argDispMode))
                Log.Success("Mode applied Successfully");
            else
                Log.Fail("Fail to apply Mode");
        }
        public void ApplyNonNative()
        {
            //    //Log.Message("Apply non native resolution");
            //    //List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, curAppliedConfig.DisplayList);
            //    if (curAppliedConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone || curAppliedConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Single)
            //    {
            //        DisplayType primary = curAppliedConfig.PrimaryDisplay;
            //       // List<DisplayMode> modeList = allModeList.Where(dI => dI.display == primary).Select(dI => dI.supportedModes).FirstOrDefault();
            //       // uint nativeX = modeList.Last().HzRes;
            //       // uint nativeY = modeList.Last().VtRes;

            //       // DisplayMode mode = modeList.Where(dI => dI.HzRes != nativeX && dI.VtRes != nativeY).Select(dI => dI).FirstOrDefault();
            //       //ApplyMode(mode);

            //        curAppliedMode = new List<DisplayMode>();
            //        DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == primary).First();
            //       DisplayMode mode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            //        curAppliedMode.Add(mode);

            //    }
            //    else
            //    {
            //        curAppliedMode = new List<DisplayMode>();
            //        curAppliedConfig.DisplayList.ForEach(curDisp =>
            //        {
            //            //List<DisplayMode> modeList = allModeList.Where(dI => dI.display == curDisp).Select(dI => dI.supportedModes).FirstOrDefault();
            //            //uint nativeX = modeList.Last().HzRes;
            //            //uint nativeY = modeList.Last().VtRes;

            //            //DisplayMode mode = modeList.Where(dI => dI.HzRes != nativeX && dI.VtRes != nativeY).Select(dI => dI).FirstOrDefault();
            //            //ApplyMode(mode);

            //            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).First();
            //            DisplayMode mode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            //            curAppliedMode.Add(mode);
            //            // base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();
            //        });
            //    }
        }

        private void RotateNVerify(DisplayMode argMode, uint argAngle)
        {
            DisplayMode actualMode;
            argMode.Angle = argAngle;
            Log.Message(true, "Rotating the display {0} through OS call to {1}, {2} Deg", argMode.display, argMode.GetCurrentModeStr(true), argAngle);
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argMode))
            {
                actualMode = VerifyRotation(argMode.display);
                if (actualMode.Angle != argMode.Angle)
                {
                    Log.Fail(false, "Mode set failed for display {0}: SetMode - {1}, CurrentMode - {2}", actualMode.display, argMode.GetCurrentModeStr(false), actualMode.GetCurrentModeStr(false));
                }
                else
                    Log.Success("Mode is set Successfully for display {0}: {1}", actualMode.display, actualMode.GetCurrentModeStr(false));
            }
            else
                Log.Fail(false, "Desired mode is not set !!!");
        }
        protected DisplayMode VerifyRotation(DisplayType argDisplay)
        {
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplay).First();
            DisplayMode currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            if (currentMode.CanFlip())
            {
                uint temp = currentMode.HzRes;
                currentMode.HzRes = currentMode.VtRes;
                currentMode.VtRes = temp;
            }
            return currentMode;
        }
        protected void PlayAndMoveVideo(DisplayHierarchy displayHierarchy, DisplayConfig displayConfig)
        {
            base.OverlayOperations(displayHierarchy, displayConfig, OverlayPlaybackOptions.MovePlayer);
        }
        protected void StopVideo()
        {
            base.OverlayOperations(DisplayHierarchy.Unsupported, base.CurrentConfig, OverlayPlaybackOptions.ClosePlayer);
        }
        protected void FullScreen(DisplayHierarchy displayHierarchy, DisplayConfig displayConfig)
        {
            base.OverlayOperations(displayHierarchy, displayConfig, OverlayPlaybackOptions.FullScreen);
        }
    }
}
