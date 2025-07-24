namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    class DisplayInfoCollection
    {
        private static List<DisplayInfo> _dIList = null;

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
                };
            }
        }

        public static List<DisplayInfo> Collection
        {
            get { return _dIList; }
        }
    }
}
