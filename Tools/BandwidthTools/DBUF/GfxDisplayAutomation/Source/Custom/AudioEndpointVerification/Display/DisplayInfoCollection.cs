namespace AudioEndpointVerification
{
    using System.Collections.Generic;
    public static class DisplayInfoCollection
    {
        private static List<DisplayInfo> _dIList = null;
        private static List<string> _triOptions = null;

        static DisplayInfoCollection()
        {
            if (null == _dIList)
            {
                _dIList = new List<DisplayInfo>()
                {
                    new DisplayInfo("None", DisplayType.None),
                    new DisplayInfo("Monitor", DisplayType.CRT),
                    new DisplayInfo("Digital Display", DisplayType.DP),
                    new DisplayInfo("Digital Display 2", DisplayType.DP_2),
                    new DisplayInfo("Digital Display 3", DisplayType.DP_3),
                    new DisplayInfo("Built-in Display", DisplayType.EDP),
                    new DisplayInfo("Digital Television", DisplayType.HDMI),
                    new DisplayInfo("Digital Television 2", DisplayType.HDMI_2),
                    new DisplayInfo("Digital Television 3", DisplayType.HDMI_3),
                    new DisplayInfo("Intel® WiDi", DisplayType.WIDI)
                };
            }
            if (null == _triOptions)
            {
                _triOptions = new List<string>() { "Clone Displays 3", "Extended Desktop 3" };
            }
        }

        public static List<DisplayInfo> Collection
        {
            get { return _dIList; }
        }
        public static List<string> TriConfigReference
        {
            get { return _triOptions; }
        }
    }
}