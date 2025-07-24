namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Xml.Linq;
    using System.Collections.Generic;

    class MP_ACPI_Base : TestBase
    {
        protected Dictionary<string, List<DisplayConfig>> _acpiToggle = null;
        private Dictionary<PORT, List<DisplayType>> _portDisplayMapping = null;
        protected void ReadACPIDataFromFile()
        {
            _acpiToggle = new Dictionary<string, List<DisplayConfig>>();
            _portDisplayMapping = new Dictionary<PORT, List<DisplayType>>();

            _portDisplayMapping.Add(PORT.PORTB, new List<DisplayType> { DisplayType.DP });
            _portDisplayMapping.Add(PORT.PORTC, new List<DisplayType> { DisplayType.HDMI });
            _portDisplayMapping.Add(PORT.PORTX, new List<DisplayType> { DisplayType.EDP, DisplayType.MIPI });
            _portDisplayMapping.Add(PORT.PORTY, new List<DisplayType> { DisplayType.CRT });
            
            string fileName = string.Concat(Directory.GetCurrentDirectory(), "\\Mapper\\ACPIConfig.map");
            if (!File.Exists(fileName))
                Log.Abort("File {0} not found", fileName);
            XDocument doc = XDocument.Load(fileName);
            var platform = from plt in doc.Descendants("Platform")
                           where plt.Attribute("id").Value.ToString().Contains(base.MachineInfo.PlatformDetails.Platform.ToString())
                           select new
                           {
                               platformId = plt.Attribute("id").Value,
                               key = plt.Descendants("Key")
                           };
            foreach (var currentKey in platform.First().key)
            {
                List<DisplayConfig> DispConfigList = new List<DisplayConfig>();
                var toggleSequence = currentKey.Descendants("ToggleSequence");

                var toggleList = from toggle in toggleSequence.Descendants("Toggle")
                                 select new
                                 {
                                     config = toggle.Attribute("config").Value,
                                     portList = toggle.Descendants("Port")
                                 };
                foreach (var currentToggle in toggleList)
                {
                    DisplayConfig currentDispConfig = new DisplayConfig();
                    currentDispConfig.DisplayList = new List<DisplayType>();

                    bool validDisplays = true;
                    DisplayConfigType dispconfigType;
                    Enum.TryParse<DisplayConfigType>(currentToggle.config.ToString(), true, out dispconfigType);
                    currentDispConfig.ConfigType = dispconfigType;
                    foreach (var currentPort in currentToggle.portList)
                    {
                        PORT port; DisplayType currentDispType;
                        Enum.TryParse<PORT>(currentPort.Value.ToString(), true, out port);
                        List<DisplayType> dispList = _portDisplayMapping[port];
                        if (dispList.Count() == 1)
                        {
                            currentDispType = dispList.First();
                        }
                        else
                        {
                            currentDispType = base.CurrentConfig.EnumeratedDisplays.Where(dI => dispList.Contains(dI.DisplayType)).Select(dI => dI.DisplayType).FirstOrDefault();
                        }
                        if (currentDispType != DisplayType.None)
                            currentDispType = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentDispType).Select(dI => dI.DisplayType).FirstOrDefault();
                        if (currentDispType != DisplayType.None)
                            currentDispConfig.DisplayList.Add(currentDispType);
                        else
                        {
                            validDisplays = false;
                            break;
                        }
                    }
                    if (validDisplays)
                        DispConfigList.Add(currentDispConfig);
                }
                if (DispConfigList.Count > 0)
                {
                    DispConfigList.Add(DispConfigList.First());//append the first entry
                    _acpiToggle.Add(currentKey.Attribute("id").Value.ToString(), DispConfigList);
                }
            }            
        }
        protected void SetConfig(DisplayConfig argDisplayConfig)
        {
            argDisplayConfig.PrimaryDisplay = argDisplayConfig.DisplayList.GetDisplay(DisplayHierarchy.Display_1);
            argDisplayConfig.SecondaryDisplay = argDisplayConfig.DisplayList.GetDisplay(DisplayHierarchy.Display_2);
            argDisplayConfig.TertiaryDisplay = argDisplayConfig.DisplayList.GetDisplay(DisplayHierarchy.Display_3);

            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDisplayConfig))
                Log.Success("Config applied successfully");
            else
                Log.Fail(false, "Failed to apply config");
        }
    }
}

