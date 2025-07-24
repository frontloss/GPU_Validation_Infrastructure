namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;

    internal static partial class WindowsFunctions
    {
        private static Dictionary<DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY, string> _displayTypeMap = null;
        private static Dictionary<int, Func<List<string>, List<string>>> _explodPatterns = null;

        internal static List<DisplayInfo> GetAllDisplayList()
        {
            List<DisplayInfo> displaysList = new List<DisplayInfo>();
            UInt32 numPathArrayElements = 0, numModeInfoArrayElements = 0;
            int returnVal = Interop.GetDisplayConfigBufferSizes((uint)QDCFlags.QDC_ALL_PATHS, ref numPathArrayElements, ref numModeInfoArrayElements);
            DISPLAYCONFIG_PATH_INFO[] pathInfo = new DISPLAYCONFIG_PATH_INFO[numPathArrayElements];
            DISPLAYCONFIG_MODE_INFO[] modeInfo = new DISPLAYCONFIG_MODE_INFO[numModeInfoArrayElements];
            DISPLAYCONFIG_TOPOLOGY_ID topologyId = DISPLAYCONFIG_TOPOLOGY_ID.DISPLAYCONFIG_TOPOLOGY_NULL;
            returnVal = Interop.QueryDisplayConfig((UInt32)QDCFlags.QDC_ALL_PATHS, ref numPathArrayElements, pathInfo, ref numModeInfoArrayElements, modeInfo, topologyId);
            if (!Convert.ToBoolean(returnVal))
            {
                foreach (DISPLAYCONFIG_PATH_INFO eachPath in pathInfo)
                    if (!eachPath.targetInfo.id.Equals(0) && eachPath.targetInfo.targetAvailable)
                        if (DisplayTypeMap.ContainsKey(eachPath.targetInfo.outputTechnology) && !displaysList.Any(dI => dI.WindowsMonitorID == eachPath.targetInfo.id))
                            AddDisplay(eachPath.targetInfo.id, DisplayTypeMap[eachPath.targetInfo.outputTechnology], displaysList, eachPath.flags);
            }
            else
                Console.WriteLine("GetAllDisplayList::QDC Call Error! Return value {0}", returnVal);
            return displaysList;
        }
        internal static Dictionary<int, Func<List<string>, List<string>>> ExplodPatterns
        {
            get
            {
                if (null == _explodPatterns)
                {
                    _explodPatterns = new Dictionary<int, Func<List<string>, List<string>>>();
                    _explodPatterns.Add(2, Get2PipeExplodPattern);
                    _explodPatterns.Add(3, Get3PipeExplodPattern);
                }
                return _explodPatterns;
            }
        }

        private static void AddDisplay(uint argWinMonID, string argDisplayType, List<DisplayInfo> argDisplaysList, uint argIsActive)
        {
            int count = argDisplaysList.Count(dI => dI.DisplayType.StartsWith(argDisplayType));
            DisplayInfo displayInfo = new DisplayInfo() { DisplayType = argDisplayType, WindowsMonitorID = argWinMonID, IsActive = Convert.ToBoolean(argIsActive) };
            if (!count.Equals(0))
                displayInfo.DisplayType += string.Concat("_", count + 1);
            argDisplaysList.Add(displayInfo);
        }
        private static Dictionary<DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY, string> DisplayTypeMap
        {
            get
            {
                if (null == _displayTypeMap)
                {
                    _displayTypeMap = new Dictionary<DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY, string>();
                    _displayTypeMap.Add(DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_HD15, "CRT");
                    _displayTypeMap.Add(DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_INTERNAL, "EDP");
                    _displayTypeMap.Add(DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_HDMI, "HDMI");
                    _displayTypeMap.Add(DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_DISPLAYPORT_EXTERNAL, "DP");
                }
                return _displayTypeMap;
            }
        }
        private static List<string> Get2PipeExplodPattern(List<string> argDisplayList)
        {
            List<string> combo = null;
            foreach (string primaryDisplay in argDisplayList)
            {
                foreach (string secondaryDisplay in argDisplayList)
                {
                    if (primaryDisplay != secondaryDisplay)
                    {
                        if (null == combo)
                            combo = new List<string>();
                        combo.Add(string.Format("{0}+{1}", primaryDisplay, secondaryDisplay));
                    }
                }
            }
            return combo;
        }
        private static List<string> Get3PipeExplodPattern(List<string> argDisplayList)
        {
            List<string> combo = null;
            foreach (string primaryDisplay in argDisplayList)
            {
                foreach (string secondaryDisplay in argDisplayList)
                {
                    if (primaryDisplay != secondaryDisplay)
                    {
                        foreach (string thirdDisplay in argDisplayList)
                        {
                            if (secondaryDisplay != thirdDisplay && primaryDisplay != thirdDisplay)
                            {
                                if (null == combo)
                                    combo = new List<string>();
                                combo.Add(string.Format("{0}+{1}+{2}", primaryDisplay, secondaryDisplay, thirdDisplay));
                            }
                        }
                    }
                }
            }
            return combo;
        }
    }
}