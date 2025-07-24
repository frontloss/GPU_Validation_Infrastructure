namespace Intel.VPG.Display.Automation
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
                    new DisplayInfo("None", DisplayType.None,false, new ConnectorType() { connectorType = string.Empty, deviceType = string.Empty }),
                    new DisplayInfo("Monitor", DisplayType.CRT,false, new ConnectorType() { connectorType = "VGA", deviceType = "Monitor" }),
                    new DisplayInfo("Digital Display", DisplayType.DP,false, new ConnectorType() { connectorType = "DisplayPort", deviceType = "DisplayPort" }),
                    new DisplayInfo("Digital Display 2", DisplayType.DP_2,false, new ConnectorType() { connectorType = "DisplayPort", deviceType = "DisplayPort" }),
                    new DisplayInfo("Digital Display 3", DisplayType.DP_3,false, new ConnectorType() { connectorType = "DisplayPort", deviceType = "DisplayPort" }),
                    new DisplayInfo("Built-in Display", DisplayType.EDP,false, new ConnectorType() { connectorType = "Embedded DisplayPort", deviceType = "Built-in Display" }),
                    new DisplayInfo("Digital Television", DisplayType.HDMI,true, new ConnectorType() { connectorType = "HDMI", deviceType = "Digital Television" }),
                    new DisplayInfo("Digital Television 2", DisplayType.HDMI_2,true, new ConnectorType() { connectorType = "HDMI", deviceType = "Digital Television" }),
                    new DisplayInfo("Digital Television 3", DisplayType.HDMI_3,true, new ConnectorType() { connectorType = "HDMI", deviceType = "Digital Television" }),
                    new DisplayInfo("Intel® WiDi", DisplayType.WIDI,false, new ConnectorType() { connectorType = "HDMI", deviceType = "Digital Television" }),
                    new DisplayInfo("Digital Display", DisplayType.DVI,false, new ConnectorType() { connectorType = "DisplayPort", deviceType = "Digital Television" }),
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