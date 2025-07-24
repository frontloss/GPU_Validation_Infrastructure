namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;

    [Test(Type = TestType.WiDi)]
    class MP_WIDI_Rotation : MP_WIDIBase
    {
        int[,] _rotationSequence = new int[3, 4] { { 90, 180, 270, 0}, 
                                                    { 90, 180, 270, 0}, 
                                                    { 90, 180, 270, 0 } };
        [Test(Type = TestType.Method, Order = 1)]
        public void SetConfigMethod()
        {
            this.SetNValidateConfig(this.CurrentConfig);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void RotationMethod()
        {
            List<DisplayModeList> displayModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);
            if (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Extended)
                this.RotationOnExtendedDisplay(displayModeList);
            else
                this.RotationOnPrimaryDisplay(displayModeList);
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void CleanUp()
        {
            this.SetNValidateConfig(this.CurrentConfig);
        }
        private void RotationOnPrimaryDisplay(List<DisplayModeList> displayModeList)
        {
            List<DisplayMode> filteredModes = TestModes(base.FilterModeLists(displayModeList.First().supportedModes));
            foreach (DisplayMode eachSingleMode in filteredModes)
                for (int eachAngle = 0; eachAngle < _rotationSequence.GetLength(1); eachAngle++)
                    this.RotateNVerify(eachSingleMode, (uint)_rotationSequence[1, eachAngle]);
        }
        private void RotationOnExtendedDisplay(List<DisplayModeList> displayModeList)
        {
            List<DisplayMode> primaryFilteredModes = TestModes(displayModeList.First().supportedModes);
            List<DisplayMode> SecondaryFilteredModes = TestModes(displayModeList.Skip(1).First().supportedModes);
            List<DisplayMode> thirdFilteredModes = null;
            if (base.CurrentConfig.ConfigType.GetDisplaysCount().Equals(3))
                thirdFilteredModes = TestModes(displayModeList.Last().supportedModes);
            for (int modeIndex = 0; modeIndex < primaryFilteredModes.Count; modeIndex++)
            {
                for (int eachAngle = 0; eachAngle < _rotationSequence.GetLength(1); eachAngle++)
                {
                    this.RotateNVerify(primaryFilteredModes[modeIndex], (uint)_rotationSequence[0, eachAngle]);
                    this.RotateNVerify(SecondaryFilteredModes[modeIndex], (uint)_rotationSequence[1, eachAngle]);
                    if (null != thirdFilteredModes)
                        this.RotateNVerify(thirdFilteredModes[modeIndex], (uint)_rotationSequence[2, eachAngle]);
                }
            }
        }
    }
}
