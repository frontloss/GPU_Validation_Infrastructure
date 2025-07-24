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
    class SB_HDMI_XVYCC_Overlay_Plug_Unplug_Non_XVYCC_YCBCR : SB_HDMI_XVYCC_Overlay_Basic
    {
        private string edidFileAfterPanelChange = "HDMI_3011_xvycc_Remove_RGB.EDID";
        public SB_HDMI_XVYCC_Overlay_Plug_Unplug_Non_XVYCC_YCBCR()
            : base()
        {
            base._actionAfterEnable = this.ActionAfterEnable;
            base._actionAfterDisable = this.ActionAfterDisable;
        }
        private void ActionAfterEnable()
        {
            Log.Message(true, "Unplug and Plug Panel");
            if (displayInfo.ColorInfo.IsXvYcc)
            {
                Log.Verbose("Unplug {0} panel on display {0}", _colorType, displayInfo.DisplayType);
                base.HotUnPlug(displayInfo.DisplayType);
                //base.CheckCRC();
                Log.Verbose("Plug back {0} panel on display {1}", _colorType, displayInfo.DisplayType);
               
                base.HotPlug(displayInfo.DisplayType, edidFileAfterPanelChange);
                base.CheckConfigChange(_intialConfig);
                //base.CheckCRC();
                //Log.Message("Check if the xvycc/ycbcr option is not coming in CUI");
                //base.VerifyNonXvyccYcvcrPanel(displayInfo.DisplayType);
                Log.Message("Verify registers for Non-Xvycc/Ycbcr panel");
                Thread.Sleep(5000);
                base.MoveCursorToPrimary(base.CurrentConfig);
                base.StopVideo(dh, base.CurrentConfig);
                base.PlayAndMoveVideo(dh, base.CurrentConfig);
                Thread.Sleep(5000);
                if ((dh != DisplayHierarchy.Display_1) && (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
                    eventCalled = base.cloneModeSecondaryOverlay;
                else
                    eventCalled = nonHDMIPanelEventSprite;
                base.RegisterCheck(displayInfo.DisplayType, displayInfo, dh, eventCalled);
                Log.Message(true, "Plug back the original panel");
                Log.Verbose("Unplug {0} panel on display {0}", _colorType, displayInfo.DisplayType);
                base.HotUnPlug(displayInfo.DisplayType);
                //base.CheckCRC();
                Log.Verbose("Plug back {0} panel on display {1}", _colorType, displayInfo.DisplayType);
                base.HotPlug(displayInfo.DisplayType, edidFile);
                base.CheckConfigChange(_intialConfig);
                //base.CheckCRC();
            }
            else
                Log.Message("Cannot plug and unplug {0}", displayInfo.DisplayType);
            
        }
        private void ActionAfterDisable()
        {
            Log.Message(true, "Unplug and Plug Panel");
            if (displayInfo.ColorInfo.IsXvYcc)
            {
                Log.Verbose("Unplug {0} panel on display {0}", _colorType, displayInfo.DisplayType);
                base.HotUnPlug(displayInfo.DisplayType);
                //base.CheckCRC();
                Log.Verbose("Plug back {0} panel on display {1}", _colorType, displayInfo.DisplayType);
              
                base.HotPlug(displayInfo.DisplayType, edidFileAfterPanelChange);
                base.CheckConfigChange(_intialConfig);
                //base.CheckCRC();
                //Log.Message("Check if the xvycc/ycbcr option is not coming in CUI");
                //base.VerifyNonXvyccYcvcrPanel(displayInfo.DisplayType);
                Log.Message("Verify registers for Non-Xvycc/Ycbcr panel");
                Thread.Sleep(5000);
                base.MoveCursorToPrimary(base.CurrentConfig);
                base.StopVideo(dh, base.CurrentConfig);
                base.PlayAndMoveVideo(dh, base.CurrentConfig);
                Thread.Sleep(5000);
                if ((dh != DisplayHierarchy.Display_1) && (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
                    eventCalled = base.cloneModeSecondaryOverlay;
                else
                    eventCalled = nonHDMIPanelEventSprite;
                base.RegisterCheck(displayInfo.DisplayType, displayInfo, dh, eventCalled);
                //base.CheckCRC();
            }
            else
                Log.Message("Cannot plug and unplug {0}", displayInfo.DisplayType);
        }       
    }
}
