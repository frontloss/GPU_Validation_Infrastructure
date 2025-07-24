namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System.Windows.Forms;
    using System;

    class MP_NativeCollage_Rotation : MP_NativeCollage_BAT
    {
        bool status_set;
        public MP_NativeCollage_Rotation()
        {
            base._performAction = this.PerformAction;
        }
        private void PerformAction()
        {
            Log.Message(true, "Apply all possible Rotation angles");
            DisplayMode dm = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            DisplayMode targetMode;
            List<string> angleList = Enum.GetNames(typeof(ScreenOrientation)).ToList();
            angleList.Add(angleList.First());
            angleList.Remove(angleList.First());
            angleList.ForEach(angle =>
            {
                Log.Message(true, "Setting rotation {0} for {1}", angle, displayInfo.DisplayType);
                dm.Angle = Convert.ToUInt32(angle.Replace("Angle", string.Empty));
                status_set = AccessInterface.SetFeature<bool, DisplayMode>(Features.Rotation, Action.SetMethod, dm);
                targetMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Rotation, Action.GetMethod, Source.AccessAPI, displayInfo);
                if (status_set && targetMode.Angle.Equals(dm.Angle))
                {
                    Log.Success("Rotation {0} successfully set for {1}", targetMode.Angle, displayInfo.DisplayType);
                    Log.Success("Rotation verified using AccessAPI");
                    
                    //this.VerifyCollagePersistence(setConfigString, 0, targetMode.Angle);
                    base.VerifyCollagePersistence(setConfigString, 0);

                    if ((currentMode.Angle == (uint)180) || (currentMode.Angle == (uint)0))
                    {
                        if (base.CheckCollageThruResolution(displayConfig.ConfigType, currentMode, base.CurrentConfig.DisplayList.Count))
                            Log.Success("{0} is verified to be successfully set using Resolutions after re-enabling driver", displayConfig.ConfigType);
                        else
                            Log.Fail("{0} is not verified using Resolutions after re-enabling driver", displayConfig.ConfigType);
                    }
                    else
                    {
                        if (base.CheckCollageThruResolution90And270(displayConfig.ConfigType, currentMode, base.CurrentConfig.DisplayList.Count))
                            Log.Success("{0} is verified to be successfully set using Resolutions after re-enabling driver", displayConfig.ConfigType);
                        else
                            Log.Fail("{0} is not verified using Resolutions after re-enabling driver", displayConfig.ConfigType);
                    }
                }
                else
                    Log.Fail("Unable to set rotation {0} for {1}", angle, displayInfo.DisplayType);
            });
        }
        private void VerifyCollagePersistence(string argSetConfigString, int argSporadic, uint argCurrentAngle)
        {
            collagepar.option = CollageOption.GetConfig;
            CollageParam collageStatus = AccessInterface.GetFeature<CollageParam, CollageParam>(Features.Collage, Action.GetMethod, Source.AccessAPI, collagepar);
            string currentConfigString = this.GetConfigString(collageStatus.config);
            if ((argCurrentAngle == (uint)180) || (argCurrentAngle == (uint)0))
            {
                if (argSetConfigString.Equals(currentConfigString))
                    Log.Success("Config {0} persistant ", currentConfigString);
                else
                    if (argSporadic == 1)
                        Log.Sporadic("Config persistance failed, Actual config is  {0}. Current config is {1}", argSetConfigString, currentConfigString);
                    else
                        Log.Fail("Config persistance failed, Actual config is  {0}. Current config is {1}", argSetConfigString, currentConfigString);
            }
            else
            {
                if (argSetConfigString.Equals(currentConfigString))
                    Log.Fail("Config persistance failed, Actual config is  {0}. Current config is {1}", argSetConfigString, currentConfigString);
            }
        }
    }
}