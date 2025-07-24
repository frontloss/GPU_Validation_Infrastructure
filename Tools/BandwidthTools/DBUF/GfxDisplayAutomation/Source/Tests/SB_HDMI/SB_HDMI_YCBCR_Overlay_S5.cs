namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using IgfxExtBridge_DotNet;
    using System.Xml.Linq;
    using System.IO;
    using System.Text;
    using System;
    using System.Threading;

    [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_HDMI_YCBCR_Overlay_S5 : SB_HDMI_Base
    {
        protected PowerStates powerState = PowerStates.S5;
        PowerParams _powerParams = null;
        protected string overlayCloneSecondaryYcbcrEnabled = "YCBCR_ENABLED_CLONE_SPRITE_DISABLED";
        protected string overlayCloneSecondaryXvyccDisabled = "XVYCC_DISABLED_CLONE_SPRITE_DISABLED";
        protected string overlayWithYcbcrEnabled = "YCBCR_ENABLED_SPRITE_ENABLED";
        protected string overlaywithXvyccDisabled = "XVYCC_DISABLED_SPRITE_ENABLED_YCBCR";
        protected DisplayHierarchy dh;
        protected string eventName = "";

        protected ColorType _colorType = ColorType.YCbCr;
        protected XvYccYcbXr xvyccObject = null;
        protected DisplayConfig _intialConfig = null;
        protected DisplayInfo displayInfo;
        protected DisplayHierarchy displayHierarchy;
        protected string eventCalled = "";
        protected string enableEvent = "YCBCR_ENABLE";
        protected string disableEvent = "YCBCR_DISABLE";
        protected string edidFile = "HDMI_DELL.EDID";
        
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {
            Log.Message(true, "Checking Preconditions and Plugging in {0} supported panel", _colorType);
            if (!base.CurrentConfig.DisplayList.Contains(DisplayType.HDMI))
                Log.Abort("HDMI not passed in command line...Aborting the test");
            base.Hotplug(FunctionName.OPEN, DisplayType.HDMI, DVMU_PORT.PORTA);
            base.Hotplug(FunctionName.UNPLUG, DisplayType.HDMI, DVMU_PORT.PORTA);
            base.Hotplug(FunctionName.UNPLUG, DisplayType.HDMI_2, DVMU_PORT.PORTB);
            if (!(base.CurrentConfig.EnumeratedDisplays.Any(dI => dI.DisplayType == DisplayType.HDMI)))
            {
                Log.Message("HDMI is not enumerated..Plugging it through DVMU");
                Log.Message("Hotplug {0} supported HDMI panel & switch the display to it", _colorType);
                base.Hotplug(FunctionName.PLUG, DisplayType.HDMI, DVMU_PORT.PORTA, edidFile);
            }
            if (base.CurrentConfig.DisplayList.Contains(DisplayType.HDMI_2) && (!(base.CurrentConfig.EnumeratedDisplays.Any(dI => dI.DisplayType == DisplayType.HDMI_2))))
            {
                Log.Message("HDMI_2 is not enumerated..Plugging it through DVMU");
                Log.Message("Hotplug {0} supported HDMI panel & switch the display to it", _colorType);
                base.Hotplug(FunctionName.PLUG, DisplayType.HDMI_2, DVMU_PORT.PORTB, edidFile);
            }
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Set the configuration");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
            _intialConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Enable {0}  and check if Enabled", _colorType);
            foreach (DisplayType display in base.CurrentConfig.DisplayList)
            {
                base.MoveCursorToPrimary(base.CurrentConfig);
                displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
                dh = base.GetDispHierarchy(base.CurrentConfig.CustomDisplayList, display);
                //if ((int)dh <= (int)DisplayHierarchy.Display_2)
                //{
                    if (displayInfo.ColorInfo.IsYcBcr)
                    {
                        Log.Message("{0} is supported on {1}", _colorType, displayInfo.DisplayType);
                        XvYccYcbXr xvyccObj = new XvYccYcbXr()
                        {
                            displayType = displayInfo.DisplayType,
                            currentConfig = base.CurrentConfig,
                            colorType = _colorType,
                            isEnabled = 1
                        };
                        if (AccessInterface.SetFeature<bool, XvYccYcbXr>(Features.YCbCr, Action.SetMethod, xvyccObj))
                        {
                            Log.Message("{0} is enabled", _colorType);
                            Log.Message(true, "Verify the registers for {0} supported display with overlay and {0} set to on", _colorType, _colorType);
                            if ((dh != DisplayHierarchy.Display_1) && (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
                                eventCalled = overlayCloneSecondaryYcbcrEnabled;
                            else
                                eventCalled = overlayWithYcbcrEnabled;
                            base.StopVideo(dh, base.CurrentConfig);
                            base.PlayAndMoveVideo(dh, base.CurrentConfig);
                            Log.Message(true, "Verify {0} enabled on {1} using Registers and CUI", _colorType, displayInfo.DisplayType);
                            base.RegisterCheck(displayInfo.DisplayType, displayInfo, dh, eventCalled);
                            base.StopVideo(dh, base.CurrentConfig);
                        }
                    }
                    if (!displayInfo.ColorInfo.IsXvYcc && !displayInfo.ColorInfo.IsYcBcr)
                    {
                        Log.Message("{0} is not supported on {1}", _colorType, displayInfo.DisplayType);
                        Log.Message("Check is sprite is enabled");
                        if ((dh != DisplayHierarchy.Display_1) && (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
                            eventCalled = base.cloneModeSecondaryOverlay;
                        else
                            eventCalled = nonHDMIPanelEventSprite;
                        Thread.Sleep(5000);
                        base.StopVideo(dh, base.CurrentConfig);
                        base.PlayAndMoveVideo(dh, base.CurrentConfig);
                        base.RegisterCheck(display, displayInfo, dh, eventCalled);
                        //base.CheckCRC();
                        base.StopVideo(dh, base.CurrentConfig);
                    }
                //}
            }
        }


        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Reboot the machine.");
            this._powerParams = new PowerParams();
            this._powerParams.Delay = 5;
            base.InvokePowerEvent(this._powerParams, PowerStates.S5);
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Check {0} is Enabled after {1}", _colorType, powerState);
            foreach (DisplayType display in base.CurrentConfig.DisplayList)
            {
                DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
                DisplayHierarchy dh = base.GetDispHierarchy(base.CurrentConfig.CustomDisplayList, display);
                //if ((int)dh <= (int)DisplayHierarchy.Display_2)
                //{
                    if (displayInfo.ColorInfo.IsYcBcr)
                    {
                        Log.Message("{0} is supported on {1}", _colorType, displayInfo.DisplayType);
                        if ((dh != DisplayHierarchy.Display_1) && (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
                            eventCalled = overlayCloneSecondaryYcbcrEnabled;
                        else
                            eventCalled = overlayWithYcbcrEnabled;
                        base.StopVideo(dh, base.CurrentConfig);
                        base.PlayAndMoveVideo(dh, base.CurrentConfig);
                        Thread.Sleep(5000);
                        Log.Message(true, "Verify {0} enabled on {1} using Registers and CUI", _colorType, displayInfo.DisplayType);
                        base.RegisterCheck(displayInfo.DisplayType, displayInfo, dh, eventCalled);
                    }
                    if (!displayInfo.ColorInfo.IsXvYcc && !displayInfo.ColorInfo.IsYcBcr)
                    {
                        Log.Message("{0} is not supported on {1}", _colorType, displayInfo.DisplayType);
                        Log.Message("Check is sprite is enabled");
                        if ((dh != DisplayHierarchy.Display_1) && (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
                            eventCalled = base.cloneModeSecondaryOverlay;
                        else
                            eventCalled = nonHDMIPanelEventSprite;
                        Thread.Sleep(5000);
                        base.StopVideo(dh, base.CurrentConfig);
                        base.PlayAndMoveVideo(dh, base.CurrentConfig);
                        Thread.Sleep(5000);
                        base.RegisterCheck(display, displayInfo, dh, eventCalled);
                        //base.CheckCRC();
                    }
                //}
            }
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Disable {0}  and check if Disabled", _colorType);
            foreach (DisplayType display in base.CurrentConfig.DisplayList)
            {
                base.MoveCursorToPrimary(base.CurrentConfig);
                displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
                dh = base.GetDispHierarchy(base.CurrentConfig.CustomDisplayList, display);
                //if ((int)dh <= (int)DisplayHierarchy.Display_2)
                //{
                    if (displayInfo.ColorInfo.IsYcBcr)
                    {
                        Log.Message("{0} is supported on {1}", _colorType, displayInfo.DisplayType);
                        XvYccYcbXr xvyccObj = new XvYccYcbXr()
                        {
                            displayType = displayInfo.DisplayType,
                            currentConfig = base.CurrentConfig,
                            colorType = _colorType,
                            isEnabled = 0
                        };
                        if (AccessInterface.SetFeature<bool, XvYccYcbXr>(Features.YCbCr, Action.SetMethod, xvyccObj))
                        {
                            Log.Message("{0} is disabled", _colorType);
                            Log.Message(true, "Verify the registers for {0} supported display with overlay and {0} set to OFF", _colorType, _colorType);
                            Log.Message("Verify the registers for {0} supported display with overlay and {0} set to on", _colorType, _colorType);
                            if ((dh != DisplayHierarchy.Display_1) && (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
                                eventCalled = overlayCloneSecondaryXvyccDisabled;
                            else
                                eventCalled = overlaywithXvyccDisabled;
                            base.StopVideo(dh, base.CurrentConfig);
                            base.PlayAndMoveVideo(dh, base.CurrentConfig);
                            Thread.Sleep(5000);
                            Log.Message(true, "Verify {0} disabled on {1} using Registers and CUI", _colorType, displayInfo.DisplayType);
                            base.RegisterCheck(displayInfo.DisplayType, displayInfo, dh, eventCalled);
                            base.StopVideo(dh, base.CurrentConfig);
                        }
                    }
                    if (!displayInfo.ColorInfo.IsXvYcc && !displayInfo.ColorInfo.IsYcBcr)
                    {
                        Log.Message("{0} is not supported on {1}", _colorType, displayInfo.DisplayType);
                        Log.Message("Check is sprite is enabled");
                        if ((dh != DisplayHierarchy.Display_1) && (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
                            eventCalled = base.cloneModeSecondaryOverlay;
                        else
                            eventCalled = nonHDMIPanelEventSprite;
                        Thread.Sleep(5000);
                        base.StopVideo(dh, base.CurrentConfig);
                        base.PlayAndMoveVideo(dh, base.CurrentConfig);
                        Thread.Sleep(5000);
                        base.RegisterCheck(display, displayInfo, dh, eventCalled);
                        //base.CheckCRC();
                        base.StopVideo(dh, base.CurrentConfig);
                    }
                //}
            }
        }

        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            Log.Message(true, "Reboot the machine.");
            this._powerParams = new PowerParams();
            this._powerParams.Delay = 5;
            base.InvokePowerEvent(this._powerParams, PowerStates.S5);
        }
        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            base.CheckConfigChange(base.CurrentConfig);
            Log.Message(true, "Check {0} is Disabled after {1}", _colorType, powerState);
            foreach (DisplayType display in base.CurrentConfig.DisplayList)
            {
                base.MoveCursorToPrimary(base.CurrentConfig);
                DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
                DisplayHierarchy dh = base.GetDispHierarchy(base.CurrentConfig.CustomDisplayList, display);
                //if ((int)dh <= (int)DisplayHierarchy.Display_2)
                //{
                    if (displayInfo.ColorInfo.IsYcBcr)
                    {
                        Log.Message("{0} is supported on {1}", _colorType, displayInfo.DisplayType);
                        Log.Message(true, "Verify the registers for {0} supported display with overlay and {0} set to OFF", _colorType, _colorType);
                        Log.Message("Verify the registers for {0} supported display with overlay and {0} set to on", _colorType, _colorType);
                        if ((dh != DisplayHierarchy.Display_1) && (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
                            eventCalled = overlayCloneSecondaryXvyccDisabled;
                        else
                            eventCalled = overlaywithXvyccDisabled;
                        base.StopVideo(dh, base.CurrentConfig);
                        base.PlayAndMoveVideo(dh, base.CurrentConfig);
                        Thread.Sleep(5000);
                        Log.Message(true, "Verify {0} disabled on {1} using Registers and CUI", _colorType, displayInfo.DisplayType);
                        base.RegisterCheck(displayInfo.DisplayType, displayInfo, dh, eventCalled);
                        base.StopVideo(dh, base.CurrentConfig);
                    }
                    if (!displayInfo.ColorInfo.IsXvYcc && !displayInfo.ColorInfo.IsYcBcr)
                    {
                        Log.Message("{0} is not supported on {1}", _colorType, displayInfo.DisplayType);
                        Log.Message("Check is sprite is enabled");
                        if ((dh != DisplayHierarchy.Display_1) && (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
                            eventCalled = base.cloneModeSecondaryOverlay;
                        else
                            eventCalled = nonHDMIPanelEventSprite;
                        Thread.Sleep(5000);
                        base.StopVideo(dh, base.CurrentConfig);
                        base.PlayAndMoveVideo(dh, base.CurrentConfig);
                        Thread.Sleep(5000);
                        base.RegisterCheck(display, displayInfo, dh, eventCalled);
                        base.StopVideo(dh, base.CurrentConfig);
                        //base.CheckCRC();
                    }
                //}
            }
        }
        [Test(Type = TestType.Method, Order = 8)]
        public void TestStep8()
        {
            Log.Message(true, "Unplug all displays connnected");
            base.Hotplug(FunctionName.OPEN, DisplayType.HDMI, DVMU_PORT.PORTA);
            
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
