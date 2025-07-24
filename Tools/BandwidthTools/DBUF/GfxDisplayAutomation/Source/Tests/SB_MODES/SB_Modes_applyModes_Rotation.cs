namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    class SB_Modes_applyModes_Rotation : SB_MODES_Base
    {
        protected List<DisplayMode> _modesList = null;
        Dictionary<DisplayUnifiedConfig, System.Action> _rotateConfig = null;
        public SB_Modes_applyModes_Rotation()
        {
            _rotateConfig = new Dictionary<DisplayUnifiedConfig, System.Action>();
            _rotateConfig.Add(DisplayUnifiedConfig.Single, RotatePrimary);
            _rotateConfig.Add(DisplayUnifiedConfig.Clone, RotatePrimary);
            _rotateConfig.Add(DisplayUnifiedConfig.Extended, RotateAllDisplay);
        }
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.ConfigTypeCount > base.CurrentConfig.DisplayList.Count())
                Log.Abort("{0} requires atleast {1} Displays to be enumerated, current Display count: {2}", base.CurrentConfig.ConfigType, base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("{0} Applied successfully", base.CurrentConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", base.CurrentConfig.GetCurrentConfigStr());
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            _modesList = GetMinMode();
            PerformRotation();
            _modesList = GetMaxMode();
            PerformRotation();
        }
        private void PerformRotation()
        {
            _modesList.ForEach(curDisp =>
            {
                base.ApplyModeOS(curDisp, curDisp.display);
            });
            _rotateConfig[base.CurrentConfig.ConfigType.GetUnifiedConfig()]();
        }
        private void RotatePrimary()
        {
            DisplayMode primaryMode = _modesList.First();
            UpdateRotationAngle(primaryMode);
        }
        private void RotateAllDisplay()
        {
            _modesList.ForEach(curMode =>
            {
                UpdateRotationAngle(curMode);
            });
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
            }
            else
            {
                Log.Fail("Failed to rotate {0} by {1}", argDisplayMode.GetCurrentModeStr(false), argDisplayMode.Angle);
            }
        }
        private List<DisplayMode> GetMinMode()
        {
            List<DisplayMode> modesList = new List<DisplayMode>();
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);
            allModeList.ForEach(curDisp =>
            {
                modesList.Add(curDisp.supportedModes.First());
            });
            return modesList;
        }
        private List<DisplayMode> GetMaxMode()
        {
            List<DisplayMode> modesList = new List<DisplayMode>();
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);
            allModeList.ForEach(curDisp =>
            {
                modesList.Add(curDisp.supportedModes.Last());
            });
            return modesList;
        }
    }
}
