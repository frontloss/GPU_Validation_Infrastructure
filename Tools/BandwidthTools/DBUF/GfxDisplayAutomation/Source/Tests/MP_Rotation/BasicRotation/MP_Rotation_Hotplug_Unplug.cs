namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    [Test(Type=TestType.HasPlugUnPlug)]
    class MP_Rotation_Hotplug_Unplug : TestBase
    {
        List<List<uint>> _extendedDisplayAngle = null;
        List<uint> _cloneDisplayAngle = null;
        List<uint> _data = null;
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {         
            Log.Message(true, "Test Pre Condition");
            if (base.CurrentConfig.DisplayList.Count < 2)
                Log.Abort("Minimum two display required to run the test");
            foreach (DisplayType DT in base.CurrentConfig.PluggableDisplayList)
            {
                Log.Message("{0} is not enumerated..Plugging it", DT);
                if (base.HotPlug(DT))
                {
                    Log.Success("Display {0} is plugged successfully", DT);
                }
                else
                    Log.Fail("Unable to hot plug display {0}", DT);
            }
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            _extendedDisplayAngle = new List<List<uint>>();
            _extendedDisplayAngle.Add(_data = new List<uint> { 90, 180, 270 });
            _extendedDisplayAngle.Add(_data = new List<uint> { 180, 270, 0 });
            _extendedDisplayAngle.Add(_data = new List<uint> { 0, 90, 270 });

            _cloneDisplayAngle = new List<uint>();
            _cloneDisplayAngle.Add(90);
            _cloneDisplayAngle.Add(180);
            _cloneDisplayAngle.Add(270);           

            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
                Log.Abort("Failed to apply config, The Displays are {0}",base.CurrentConfig.GetCurrentConfigStr());
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            if (DisplayExtensions.GetUnifiedConfig(base.CurrentConfig.ConfigType) == DisplayUnifiedConfig.Clone)
            {
                foreach (uint rotationAngle in _cloneDisplayAngle)
                {
                    Log.Message(true, "Setting {0} to Angle {1}", base.CurrentConfig.PrimaryDisplay.ToString(), rotationAngle);
                    RotateDisplay(base.CurrentConfig.PrimaryDisplay, rotationAngle);
                    PlugUnplugDisplay();
                }
            }
            else if (DisplayExtensions.GetUnifiedConfig(base.CurrentConfig.ConfigType) == DisplayUnifiedConfig.Extended)
            {
                foreach (List<uint> rotationAngleList in _extendedDisplayAngle)
                {
                    string displayStr="Setting: ";
                    for ( int index=0;index<base.CurrentConfig.CustomDisplayList.Count();index++)
                    { 
                        displayStr = string.Concat(displayStr, string.Format("Display {0} to Angle {1} ", base.CurrentConfig.CustomDisplayList.ElementAt(index).ToString(), rotationAngleList.ElementAt(index)));
                    }
                    Log.Message(true, displayStr);
                    for (int i   = 0; i < base.CurrentConfig.CustomDisplayList.Count(); i++)
                        RotateDisplay(base.CurrentConfig.CustomDisplayList.ElementAt(i), rotationAngleList.ElementAt(i));
                    PlugUnplugDisplay();
                }
            }
        }

        private void RotateDisplay(DisplayType argDisplayType, uint argRotationAngle)
        {            
            DisplayInfo currentDisplayInfo = null;
            DisplayMode currentDisplayMode = new DisplayMode();
            currentDisplayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplayType).FirstOrDefault();
            currentDisplayMode.Copy(currentDisplayInfo.DisplayMode);
            currentDisplayMode.Angle = argRotationAngle;
            bool status_set = AccessInterface.SetFeature<bool, DisplayMode>(Features.Rotation, Action.SetMethod, currentDisplayMode);
            DisplayMode targetMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Rotation, Action.GetMethod, Source.AccessAPI, currentDisplayInfo);
            if (status_set && targetMode.Angle.Equals(currentDisplayMode.Angle))
                Log.Success("Rotation {0} successfully set for {1}", targetMode.Angle, argDisplayType);
            else
                Log.Fail(false, "Unable to set rotation {0} for {1}", argRotationAngle, argDisplayType);
        }

        private void PlugUnplugDisplay()
        {
            foreach (DisplayType DT in DisplayExtensions.pluggedDisplayList.Reverse<DisplayType>())
            {
                if (base.HotUnPlug(DT))
                {
                    Log.Success("Successfully able to hot unplug display {0}", DT);
                }
                else
                    Log.Fail("Unable to hot unplug display {0}", DT);
                DisplayCurrentConfigMode();
                if (base.HotPlug(DT))
                {
                    Log.Success("Display {0} is plugged successfully", DT);
                }
                else
                    Log.Fail("Unable to hot plug display {0}", DT);
                DisplayCurrentConfigMode();
            }
        }
        private void DisplayCurrentConfigMode()
        {
            Log.Message("The Displays Details:");
            foreach (DisplayInfo currentDisplayInfo in base.CurrentConfig.EnumeratedDisplays)
            {
                DisplayMode currentDisplayMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Rotation, Action.GetMethod, Source.AccessAPI, currentDisplayInfo);
                Log.Message("Display {0} {1}",currentDisplayInfo.DisplayType.ToString(),currentDisplayMode.GetCurrentModeStr(false));
            }
        }
    }
}

