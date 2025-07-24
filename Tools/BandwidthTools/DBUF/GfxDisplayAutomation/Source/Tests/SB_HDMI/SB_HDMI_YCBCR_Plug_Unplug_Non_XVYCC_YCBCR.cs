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
    class SB_HDMI_YCBCR_Plug_Unplug_Non_XVYCC_YCBCR : SB_HDMI_YCBCR_Basic
    {
        private string edidFileAfterPanelChange = "HDMI_3011_xvycc_Remove_RGB.EDID";
        public SB_HDMI_YCBCR_Plug_Unplug_Non_XVYCC_YCBCR()
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
                //Log.Message("Check if the xvycc/ycbcr option is not coming in CUI");
                //base.VerifyNonXvyccYcvcrPanel(displayInfo.DisplayType);
                Log.Message("Verify registers for Non-Xvycc/Ycbcr panel");
                base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, nonHDMIPanelEvent);
                Log.Message(true, "Plug back the original panel");
                Log.Verbose("Unplug {0} panel on display {0}", _colorType, displayInfo.DisplayType);
                base.HotUnPlug(displayInfo.DisplayType);
                //base.CheckCRC();
                Log.Verbose("Plug back {0} panel on display {1}", _colorType, displayInfo.DisplayType);
                base.HotPlug(displayInfo.DisplayType, edidFile);
                //base.CheckCRC();
                base.CheckConfigChange(_intialConfig);
            }
            else
                Log.Message("Cannot plug and unplug {0}", displayInfo.DisplayType);

        }
        private void ActionAfterDisable()
        {
            Log.Message(true, "Unplug and Plug Panel");
            if (displayInfo.DvmuPort != DVMU_PORT.None && displayInfo.ColorInfo.IsYcBcr)
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
                base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, nonHDMIPanelEvent);
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
        //        //Log.Message("Check if the xvycc/ycbcr option is not coming in CUI");
        //        //base.VerifyNonXvyccYcvcrPanel(displayInfo.DisplayType);
        //        Log.Message("Verify registers for Non-Xvycc/Ycbcr panel");
        //        base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, nonHDMIPanelEvent);
        //        Log.Message(true, "Plug back the original panel");
        //        Log.Verbose("Unplug {0} panel on display {0}", _colorType, displayInfo.DisplayType);
        //        base.Hotplug(FunctionName.UNPLUG, displayInfo.DisplayType, displayInfo.DvmuPort);
        //        //base.CheckCRC();
        //        Log.Verbose("Plug back {0} panel on display {1}", _colorType, displayInfo.DisplayType);
        //        base.Hotplug(FunctionName.PLUG, displayInfo.DisplayType, displayInfo.DvmuPort, edidFile);
        //        //base.CheckCRC();
        //        base.CheckConfigChange(_intialConfig);
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
        //        //Log.Message("Check if the xvycc/ycbcr option is not coming in CUI");
        //        //base.VerifyNonXvyccYcvcrPanel(displayInfo.DisplayType);
        //        Log.Message("Verify registers for Non-Xvycc/Ycbcr panel");
        //        base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, nonHDMIPanelEvent);
        //        //base.CheckCRC();
        //    }
        //    else
        //        Log.Message("Cannot plug and unplug {0}", displayInfo.DisplayType);   
        //}       
    }
}
