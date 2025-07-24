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

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_HDMI_XVYCC_Overlay_Basic : SB_HDMI_XVYCC_Basic
    {
        protected string overlayWithXvyccEnabled = "XVYCC_ENABLED_SPRITE_ENABLED";
        protected string overlaywithXvyccDisabled = "XVYCC_DISABLED_SPRITE_ENABLED";
        protected string overlayCloneSecondaryXvyccEnabled = "XVYCC_ENABLED_CLONE_SPRITE_DISABLED";
        protected string overlayCloneSecondaryXvyccDisabled = "XVYCC_DISABLED_CLONE_SPRITE_DISABLED";
        protected DisplayHierarchy dh;
        protected string eventName = "";

        public SB_HDMI_XVYCC_Overlay_Basic()
            : base()
        {
            _actionAfterEnable = null;
            _actionAfterDisable = null;
        }
        [Test(Type = TestType.Method, Order = 2)]
        public override void TestStep2()
        {
            Log.Message(true, "Enable {0}  and check if Enabled", _colorType);
            foreach (DisplayType display in base.CurrentConfig.DisplayList)
            {
                base.MoveCursorToPrimary(base.CurrentConfig);
                displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
                dh = base.GetDispHierarchy(base.CurrentConfig.CustomDisplayList, display);
                if ((int)dh <= (int)DisplayHierarchy.Display_2)
                {
                    if (displayInfo.ColorInfo.IsXvYcc)
                    {
                        Log.Message("{0} is supported on {1}", _colorType, displayInfo.DisplayType);
                        XvYccYcbXr xvyccObj = new XvYccYcbXr()
                        {
                            displayType = displayInfo.DisplayType,
                            currentConfig = base.CurrentConfig,
                            colorType = _colorType,
                            isEnabled = 1
                        };
                        if (AccessInterface.SetFeature<bool, XvYccYcbXr>(Features.XvYcc, Action.SetMethod, xvyccObj))
                        {
                            Log.Message("{0} is enabled", _colorType);
                            Log.Message(true, "Verify the registers for {0} supported display with overlay and {0} set to on", _colorType, _colorType);
                            if ((dh != DisplayHierarchy.Display_1) && (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
                                eventCalled = overlayCloneSecondaryXvyccEnabled;
                            else
                                eventCalled = overlayWithXvyccEnabled;
                            base.StopVideo(dh, base.CurrentConfig);

                            base.PlayAndMoveVideo(dh, base.CurrentConfig);
                            Thread.Sleep(5000);
                            Log.Message(true, "Verify {0} enabled on {1} using Registers and CUI", _colorType, displayInfo.DisplayType);
                            base.RegisterCheck(displayInfo.DisplayType, displayInfo, dh, eventCalled);
                            if (null != this._actionAfterEnable)
                                this._actionAfterEnable();
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
                        if (null != this._actionAfterEnable)
                            this._actionAfterEnable();
                    }
                }
                base.StopVideo(dh, base.CurrentConfig);
            }
        }
        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            Log.Message(true, "Disable {0}  and check if Disabled", _colorType);

            foreach (DisplayType display in base.CurrentConfig.DisplayList)
            {
                base.MoveCursorToPrimary(base.CurrentConfig);
                displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
                dh = base.GetDispHierarchy(base.CurrentConfig.CustomDisplayList, display);
                if ((int)dh <= (int)DisplayHierarchy.Display_2)
                {
                    if (displayInfo.ColorInfo.IsXvYcc)
                    {
                        Log.Message("{0} is supported on {1}", _colorType, displayInfo.DisplayType);
                        XvYccYcbXr xvyccObj = new XvYccYcbXr()
                        {
                            displayType = displayInfo.DisplayType,
                            currentConfig = base.CurrentConfig,
                            colorType = _colorType,
                            isEnabled = 0
                        };
                        if (AccessInterface.SetFeature<bool, XvYccYcbXr>(Features.XvYcc, Action.SetMethod, xvyccObj))
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
                            if (null != this._actionAfterDisable)
                                this._actionAfterDisable();
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
                        if (null != this._actionAfterEnable)
                            this._actionAfterEnable();
                    }
                }
                base.StopVideo(dh, base.CurrentConfig);
            }
        }
    }
}
