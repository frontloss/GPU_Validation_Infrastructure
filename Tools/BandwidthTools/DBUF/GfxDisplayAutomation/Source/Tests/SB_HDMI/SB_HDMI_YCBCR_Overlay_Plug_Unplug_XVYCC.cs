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
    class SB_HDMI_YCBCR_Overlay_Plug_Unplug_XVYCC : SB_HDMI_YCBCR_Overlay_Basic
    {
        private string edidFileAfterPanelChange = "HDMI_DELL_U2711_XVYCC.EDID";
        public SB_HDMI_YCBCR_Overlay_Plug_Unplug_XVYCC() 
            : base()
        {
            base._actionAfterEnable = this.ActionAfterEnable;
            base._actionAfterDisable = this.ActionAfterDisable;
        }

        private void ActionAfterEnable()
        {
            Log.Message(true, "Unplug and Plug Panel");
            if (displayInfo.ColorInfo.IsYcBcr)
            {
                Log.Verbose("Unplug {0} panel on display {0}", _colorType, displayInfo.DisplayType);
                base.HotUnPlug(displayInfo.DisplayType);
                //base.CheckCRC();
                Log.Verbose("Plug back {0} panel on display {1}", _colorType, displayInfo.DisplayType);
                base.HotPlug(displayInfo.DisplayType, edidFileAfterPanelChange);
                base.CheckConfigChange(_intialConfig);
                //base.CheckCRC();
                base.StopVideo(dh, base.CurrentConfig);
                base.PlayAndMoveVideo(dh, base.CurrentConfig);
                Log.Message("Verify registers after Unplug and Plug");
                if ((dh != DisplayHierarchy.Display_1) && (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
                    eventCalled = "XVYCC_DISABLED_CLONE_SPRITE_DISABLED";
                else
                    eventCalled = "XVYCC_DISABLED_SPRITE_ENABLED";
                base.RegisterCheck(displayInfo.DisplayType, displayInfo, dh, eventCalled);
                Log.Message(true, "Plug back the original panel");
                Log.Verbose("Unplug {0} panel on display {1}", _colorType, displayInfo.DisplayType);
                base.HotUnPlug(displayInfo.DisplayType);
                //base.CheckCRC();
                Log.Verbose("Plug panel on display {0}", displayInfo.DisplayType);
                base.HotPlug(displayInfo.DisplayType, edidFile);
                base.CheckConfigChange(_intialConfig);
                base.StopVideo(dh, base.CurrentConfig);
                //base.CheckCRC();
            }
            else
                Log.Message("Cannot plug and unplug {0}", displayInfo.DisplayType);
        }
        private void ActionAfterDisable()
        {
            Log.Message(true, "Unplug and Plug Panel");
            if (displayInfo.ColorInfo.IsYcBcr)
            {
                Log.Verbose("Unplug {0} panel on display {0}", _colorType, displayInfo.DisplayType);
                base.HotUnPlug(displayInfo.DisplayType);
                //base.CheckCRC();
                Log.Verbose("Plug back {0} panel on display {1}", _colorType, displayInfo.DisplayType);
                base.HotPlug(displayInfo.DisplayType, edidFileAfterPanelChange);
                base.CheckConfigChange(_intialConfig);
                //base.CheckCRC();
                base.StopVideo(dh, base.CurrentConfig);
                base.PlayAndMoveVideo(dh, base.CurrentConfig);
                Log.Message("Verify registers after Unplug and Plug");
                if ((dh != DisplayHierarchy.Display_1) && (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
                    eventCalled = "XVYCC_DISABLED_CLONE_SPRITE_DISABLED";
                else
                    eventCalled = "XVYCC_DISABLED_SPRITE_ENABLED";
                base.RegisterCheck(displayInfo.DisplayType, displayInfo, dh, eventCalled);
                base.StopVideo(dh, base.CurrentConfig);
                //base.CheckCRC();
            }
            else
                Log.Message("Cannot plug and unplug {0}", displayInfo.DisplayType);
        }

        //private void ActionAfterEnable()
        //{
        //    Log.Message(true, "Unplug and Plug Panel");
        //    if (displayInfo.DvmuPort != DVMU_PORT.None && displayInfo.ColorInfo.IsYcBcr)
        //    {
        //        Log.Verbose("Unplug {0} panel on display {0}", _colorType, displayInfo.DisplayType);
        //        base.Hotplug(FunctionName.UNPLUG, displayInfo.DisplayType, displayInfo.DvmuPort);
        //        //base.CheckCRC();
        //        Log.Verbose("Plug back {0} panel on display {1}", _colorType, displayInfo.DisplayType);
        //        base.Hotplug(FunctionName.PLUG, displayInfo.DisplayType, displayInfo.DvmuPort, edidFileAfterPanelChange);
        //        base.CheckConfigChange(_intialConfig);
        //        //base.CheckCRC();
        //        Thread.Sleep(5000);
        //        base.StopVideo(dh, base.CurrentConfig);
        //        base.PlayAndMoveVideo(dh, base.CurrentConfig);
        //        Thread.Sleep(5000);
        //        Log.Message("Verify registers after Unplug and Plug");
        //        if ((dh != DisplayHierarchy.Display_1) && (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
        //            eventCalled = "XVYCC_DISABLED_CLONE_SPRITE_DISABLED";
        //        else
        //            eventCalled = "XVYCC_DISABLED_SPRITE_ENABLED";
        //        base.RegisterCheck(displayInfo.DisplayType, displayInfo, dh, eventCalled);
        //        Log.Message(true, "Plug back the original panel");
        //        Log.Verbose("Unplug {0} panel on display {1}", _colorType, displayInfo.DisplayType);
        //        base.Hotplug(FunctionName.UNPLUG, displayInfo.DisplayType, displayInfo.DvmuPort);
        //        //base.CheckCRC();
        //        Log.Verbose("Plug panel on display {0}", displayInfo.DisplayType);
        //        base.Hotplug(FunctionName.PLUG, displayInfo.DisplayType, displayInfo.DvmuPort, edidFile);
        //        base.CheckConfigChange(_intialConfig);
        //        //base.CheckCRC();
        //    }
        //    else
        //        Log.Message("Cannot plug and unplug {0}", displayInfo.DisplayType);
        //}
        //private void ActionAfterDisable()
        //{
        //    Log.Message(true, "Unplug and Plug Panel");
        //    if (displayInfo.DvmuPort != DVMU_PORT.None && displayInfo.ColorInfo.IsYcBcr)
        //    {
        //        Log.Verbose("Unplug {0} panel on display {0}", _colorType, displayInfo.DisplayType);
        //        base.Hotplug(FunctionName.UNPLUG, displayInfo.DisplayType, displayInfo.DvmuPort);
        //        //base.CheckCRC();
        //        Log.Verbose("Plug back {0} panel on display {1}", _colorType, displayInfo.DisplayType);
        //        base.Hotplug(FunctionName.PLUG, displayInfo.DisplayType, displayInfo.DvmuPort, edidFileAfterPanelChange);
        //        base.CheckConfigChange(_intialConfig);
        //        //base.CheckCRC();
        //        Thread.Sleep(5000);
        //        base.StopVideo(dh, base.CurrentConfig);
        //        base.PlayAndMoveVideo(dh, base.CurrentConfig);
        //        Thread.Sleep(5000);
        //        Log.Message("Verify registers after Unplug and Plug");
        //        if ((dh != DisplayHierarchy.Display_1) && (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
        //            eventCalled = "XVYCC_DISABLED_CLONE_SPRITE_DISABLED";
        //        else
        //            eventCalled = "XVYCC_DISABLED_SPRITE_ENABLED";
        //        base.RegisterCheck(displayInfo.DisplayType, displayInfo, dh, eventCalled);
        //        //base.CheckCRC();
        //    }
        //    else
        //        Log.Message("Cannot plug and unplug {0}", displayInfo.DisplayType);
        //}       
    }
}
