namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Xml.Linq;

    [Test(Type = TestType.WiDi)]
    class MP_WIDI_ACPI_HK : MP_WIDIBase
    {
        protected Dictionary<string, List<DisplayConfig>> _acpiToggle = null;
        private Dictionary<PORT, List<DisplayType>> _portDisplayMapping = null;
        [Test(Type = TestType.PreCondition, Order = 1)]
        public void ACPITestPreCondition()
        {
            ReadACPIDataFromFile();
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep1()
        {
            PerformTest(base.MachineInfo.PlatformDetails.Platform.ToString(), "F1");
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep2()
        {
            PerformTest(base.MachineInfo.PlatformDetails.Platform.ToString(), "F2");
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep3()
        {
            PerformTest(base.MachineInfo.PlatformDetails.Platform.ToString(), "F3");
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep4()
        {
            PerformTest(base.MachineInfo.PlatformDetails.Platform.ToString(), "F4");
        }
        private void ReadACPIDataFromFile()
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

        private void SetInitialConfig(DisplayConfig argDisplayConfig)
        {
            argDisplayConfig.PrimaryDisplay = argDisplayConfig.DisplayList.GetDisplay(DisplayHierarchy.Display_1);
            argDisplayConfig.SecondaryDisplay = argDisplayConfig.DisplayList.GetDisplay(DisplayHierarchy.Display_2);
            argDisplayConfig.TertiaryDisplay = argDisplayConfig.DisplayList.GetDisplay(DisplayHierarchy.Display_3);
            base.SetNValidateConfig(argDisplayConfig);
        }

        private void PerformTest(string argPlatform, string argKey)
        {
            Log.Message(true, "Performing acpi default switch for key {0} in {1}", argKey, argPlatform);
            List<DisplayConfig> toggleSequence = new List<DisplayConfig>();
            if (_acpiToggle.ContainsKey(argKey))
            {
                toggleSequence = _acpiToggle[argKey];
                DisplayConfig initialConfig = toggleSequence.First();
                SetInitialConfig(initialConfig);

                toggleSequence.RemoveAt(0);
                foreach (DisplayConfig currentDispConfig in toggleSequence)
                {
                    AccessInterface.SetFeature<bool, string>(Features.ACPIFunctions, Action.SetMethod, argKey);
                    Thread.Sleep(5000);
                    DisplayConfig osConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
                    Log.Verbose(osConfig.GetCurrentConfigStr());
                    if (osConfig.ConfigType != currentDispConfig.ConfigType ||
                        osConfig.CustomDisplayList.Except(currentDispConfig.DisplayList).Count() != 0 &&
                        osConfig.CustomDisplayList.Contains(DisplayType.WIDI))
                    {
                        Log.Fail(false, "Mismatch in config in key {0} Expected Configuration:{1} Current Configuration:{2}", argKey, currentDispConfig.GetCurrentConfigStr(), osConfig.GetCurrentConfigStr());
                        break;
                    }
                    else
                    {
                        Log.Message("WiDi display is not enumerated, as expected");
                        Log.Success("ACPI switch configutaion {0} match the expected sequence for Key: {1}", osConfig.GetCurrentConfigStr(), argKey);
                    }
                }
            }
            else
                Log.Message("Toggle sequence eliminated for key {0}", argKey);
        }
    }
}
