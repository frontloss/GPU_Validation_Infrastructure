namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using IgfxExtBridge_DotNet;
    using System.Xml.Linq;
    using System.IO;
    using System.Text;
    using System;
    using System.Diagnostics;
    using System.Threading;

    [Test(Type = TestType.HasPlugUnPlug)]
    [Test(Type = TestType.HasReboot)]
    class SB_HDMI_YCBCR_Plug_Unplug_XVYCC_S5 : SB_HDMI_Base
    {
        protected ColorType _colorType = ColorType.YCbCr;
        protected XvYccYcbXr xvyccObject = null;
        protected string enableEvent = "YCBCR_ENABLE";
        protected string disableEvent = "YCBCR_DISABLE";
        protected string edidFile = "HDMI_DELL.EDID";
        private string edidFileAfterS5 = "HDMI_DELL_U2711_XVYCC.EDID";
        protected string displayInfoFile = string.Format(@"{0}\PluggedDisplaysInfo.txt", Directory.GetCurrentDirectory());
        protected PowerStates powerState = PowerStates.S5;
        PowerParams _powerParams = null;
        
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            Log.Message(true, "Checking Preconditions and Plugging in {0} supported panel", _colorType);
            if (!base.CurrentConfig.DisplayList.Contains(DisplayType.HDMI))
                Log.Abort("HDMI not passed in command line...Aborting the test");
            base.Hotplug(FunctionName.OPEN, DisplayType.HDMI, DVMU_PORT.PORTA);
            if (!(base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == DisplayType.HDMI).Select(dI => dI.DisplayType).FirstOrDefault() == DisplayType.HDMI))
            {
                Log.Message("HDMI is not enumerated..Plugging it through DVMU");
                Log.Message("Hotplug {0} supported HDMI panel & switch the display to it", _colorType);
                base.Hotplug(FunctionName.PLUG, DisplayType.HDMI, DVMU_PORT.PORTA, edidFile);
            }
            if (base.CurrentConfig.DisplayList.Contains(DisplayType.HDMI_2) && (!(base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == DisplayType.HDMI_2).Select(dI => dI.DisplayType).FirstOrDefault() == DisplayType.HDMI_2)))
            {
                Log.Message("HDMI_2 is not enumerated..Plugging it through DVMU");
                Log.Message("Hotplug {0} supported HDMI panel & switch the display to it", _colorType);
                base.Hotplug(FunctionName.PLUG, DisplayType.HDMI_2, DVMU_PORT.PORTB, edidFile);
            }
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Verbose(true, "Set the configuration");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            System.IO.StreamWriter file = new System.IO.StreamWriter(displayInfoFile);
                             
             Log.Message(true, "Enable {0}  and check if Enabled", _colorType);
            foreach (DisplayType display in base.CurrentConfig.DisplayList)
            {
                DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
                DisplayHierarchy displayHierarchy = base.GetDispHierarchy(base.CurrentConfig.CustomDisplayList, display);
                if (displayInfo.ColorInfo.IsYcBcr)
                {
                    string toBeWritten = string.Concat(displayInfo.DisplayType.ToString(), ",", displayInfo.DvmuPort.ToString());
                    file.WriteLine(toBeWritten);
                    Log.Message("{0} is supported on {1}", _colorType, displayInfo.DisplayType);
                    xvyccObject = new XvYccYcbXr()
                    {
                        displayType = displayInfo.DisplayType,
                        currentConfig = base.CurrentConfig,
                        colorType = _colorType,
                        isEnabled = 1
                    };
                    if (AccessInterface.SetFeature<bool, XvYccYcbXr>(Features.YCbCr, Action.SetMethod, xvyccObject))
                    {
                        Log.Success("{0} is enabled on {1}", _colorType, displayInfo.DisplayType);
                        Log.Message(true, "Verify {0} enabled on {1} using Registers and CUI", _colorType, displayInfo.DisplayType);
                        base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, enableEvent);
                    }
                    else
                        Log.Fail("{0} is not enabled on {1}", _colorType, displayInfo.DisplayType);
                }
                if (!displayInfo.ColorInfo.IsXvYcc && !displayInfo.ColorInfo.IsYcBcr)
                {
                    Log.Message("{0} is not supported on {1}", _colorType, displayInfo.DisplayType);
                    base.RegisterCheck(display, displayInfo, displayHierarchy, nonHDMIPanelEvent);
                }
            }
            file.Close();
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            if (!(AccessInterface.SetFeature<bool, string>(Features.PromptMessage, Action.SetMethod, "Unplug panel during S5")))
                Log.Abort("User Rejected Semi Automated Request");
            Log.Message(true, "Reboot the machine.");
            this._powerParams = new PowerParams();
            this._powerParams.Delay = 5;
            base.InvokePowerEvent(this._powerParams, PowerStates.S5);
        }
        [Test(Type = TestType.Method, Order = 4)]
        public virtual void TestStep4()
        {
            Log.Message(true, "Check {0} is Enabled after {1}", _colorType, powerState);
            base.Hotplug(FunctionName.OPEN, DisplayType.HDMI, DVMU_PORT.PORTA);
            StreamReader read = new StreamReader(displayInfoFile);
            string line;
            string[] displayArray;
            DisplayType displays;
            DVMU_PORT port;
            while ((line = read.ReadLine()) != null)
            {
                displayArray = line.Split(',');
                Enum.TryParse(displayArray[0], true, out displays);
                Enum.TryParse(displayArray[1], true, out port);
                base.Hotplug(FunctionName.PLUG, displays, port, edidFileAfterS5);         
            }
            base.CheckConfigChange(base.CurrentConfig);
            foreach (DisplayType display in base.CurrentConfig.DisplayList)
            {
                DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
                DisplayHierarchy dh = base.GetDispHierarchy(base.CurrentConfig.CustomDisplayList, display);
                if (displayInfo.ColorInfo.IsXvYcc)
                {
                    Log.Message("{0} is supported on {1}", _colorType, displayInfo.DisplayType);
                    Log.Message(true, "Verify {0} enabled on {1} using Registers and CUI", _colorType, displayInfo.DisplayType);
                    string eventCalled = "XVYCC_DISABLE";
                    base.RegisterCheck(displayInfo.DisplayType, displayInfo, dh, eventCalled);
                }
                if (!displayInfo.ColorInfo.IsXvYcc && !displayInfo.ColorInfo.IsYcBcr)
                {
                    Log.Message("{0} is not supported on {1}", _colorType, displayInfo.DisplayType);
                    base.RegisterCheck(display, displayInfo, dh, nonHDMIPanelEvent);
                }
            }
            read.Close();
        }
        [Test(Type = TestType.Method, Order = 5)]
        public virtual void TestStep5()
        {
            foreach (DisplayType display in base.CurrentConfig.DisplayList)
            {
                DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
                DisplayHierarchy dh = base.GetDispHierarchy(base.CurrentConfig.CustomDisplayList, display);
                if (displayInfo.ColorInfo.IsXvYcc)
                {
                    Log.Message(true, "Plug back {0} panel for the test to continue", _colorType);
                    Log.Verbose("Unplug {0} panel on display {1}", _colorType, displayInfo.DisplayType);
                    base.Hotplug(FunctionName.UNPLUG, displayInfo.DisplayType, displayInfo.DvmuPort);
                    Log.Verbose("Plug panel on display {0}", displayInfo.DisplayType);
                    base.Hotplug(FunctionName.PLUG, displayInfo.DisplayType, displayInfo.DvmuPort, edidFile);
                }
            }
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            base.CheckConfigChange(base.CurrentConfig);
            displayInfoFile = string.Format(@"{0}\PluggedDisplaysInfo.txt", Directory.GetCurrentDirectory());
            System.IO.StreamWriter file = new System.IO.StreamWriter(displayInfoFile);
            Log.Message(true, "Disable {0}  and check if Disabled", _colorType);
            foreach (DisplayType display in base.CurrentConfig.DisplayList)
            {
                DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
                DisplayHierarchy displayHierarchy = base.GetDispHierarchy(base.CurrentConfig.CustomDisplayList, display);
                if (displayInfo.ColorInfo.IsYcBcr)
                {
                    string toBeWritten = string.Concat(displayInfo.DisplayType.ToString(), ",", displayInfo.DvmuPort.ToString());
                    file.WriteLine(toBeWritten);
                    Log.Message("{0} is supported on {1}", _colorType, displayInfo.DisplayType);
                    xvyccObject = new XvYccYcbXr()
                    {
                        displayType = displayInfo.DisplayType,
                        currentConfig = base.CurrentConfig,
                        colorType = _colorType,
                        isEnabled = 0
                    };
                    if (AccessInterface.SetFeature<bool, XvYccYcbXr>(Features.YCbCr, Action.SetMethod, xvyccObject))
                    {
                        Log.Success("{0} is disabled on {1}", _colorType, displayInfo.DisplayType);
                        Log.Message(true, "Verify {0} disabled on {1} using Registers and CUI", _colorType, displayInfo.DisplayType);
                        base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, disableEvent);
                    }
                    else
                        Log.Fail("{0} is not disabled on {1}", _colorType, displayInfo.DisplayType);
                }
                if (!displayInfo.ColorInfo.IsXvYcc && !displayInfo.ColorInfo.IsYcBcr)
                {
                    Log.Message("{0} is not supported on {1}", _colorType, displayInfo.DisplayType);
                    base.RegisterCheck(display, displayInfo, displayHierarchy, nonHDMIPanelEvent);
                }
            }
            file.Close();
        }
        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            if (!(AccessInterface.SetFeature<bool, string>(Features.PromptMessage, Action.SetMethod, "Unplug panel during S5")))
                Log.Abort("User Rejected Semi Automated Request");
            Log.Message(true, "Reboot the machine.");
            this._powerParams = new PowerParams();
            this._powerParams.Delay = 5;
            base.InvokePowerEvent(this._powerParams, PowerStates.S5);
        }
        [Test(Type = TestType.Method, Order = 8)]
        public virtual void TestStep8()
        {
            Log.Message(true, "Check {0} is Disabled after {1}", _colorType, powerState);
            base.Hotplug(FunctionName.OPEN, DisplayType.HDMI, DVMU_PORT.PORTA);
            StreamReader read = new StreamReader(displayInfoFile);
            string line;
            string[] displayArray;
            DisplayType displays;
            DVMU_PORT port;
            while ((line = read.ReadLine()) != null)
            {
                displayArray = line.Split(',');
                Enum.TryParse(displayArray[0], true, out displays);
                Enum.TryParse(displayArray[1], true, out port);
                base.Hotplug(FunctionName.PLUG, displays, port, edidFileAfterS5);
            }
            base.CheckConfigChange(base.CurrentConfig);
            foreach (DisplayType display in base.CurrentConfig.DisplayList)
            {
                DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
                DisplayHierarchy dh = base.GetDispHierarchy(base.CurrentConfig.CustomDisplayList, display);
                if (displayInfo.ColorInfo.IsXvYcc)
                {
                    Log.Message("{0} is supported on {1}", _colorType, displayInfo.DisplayType);
                    Log.Message(true, "Verify {0} enabled on {1} using Registers and CUI", _colorType, displayInfo.DisplayType);
                    string eventCalled = "XVYCC_DISABLE";
                    base.RegisterCheck(displayInfo.DisplayType, displayInfo, dh, eventCalled);
                }
                if (!displayInfo.ColorInfo.IsXvYcc && !displayInfo.ColorInfo.IsYcBcr)
                {
                    Log.Message("{0} is not supported on {1}", _colorType, displayInfo.DisplayType);
                    base.RegisterCheck(display, displayInfo, dh, nonHDMIPanelEvent);
                }
            }
        }
        [Test(Type = TestType.Method, Order = 9)]
        public void TestStep9()
        {
            Log.Message(true, "Unplug all displays");
            base.CurrentConfig.CustomDisplayList.Reverse(0, base.CurrentConfig.CustomDisplayList.Count);
            List<DisplayType> sortedDisplayList = base.CurrentConfig.CustomDisplayList;
            sortedDisplayList.ForEach(display =>
            {
                DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
                if (!(displayInfo.DvmuPort == DVMU_PORT.None))
                    base.Hotplug(FunctionName.UNPLUG, displayInfo.DisplayType, displayInfo.DvmuPort);
            });         
        }
    }
}
