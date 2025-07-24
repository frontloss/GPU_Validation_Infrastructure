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
    class SB_HDMI_YCBCR_Plug_Unplug : SB_HDMI_YCBCR_Basic
    {
        public SB_HDMI_YCBCR_Plug_Unplug()
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
                base.HotPlug(displayInfo.DisplayType, _defaultEDIDMap[displayInfo.DisplayType]);
                //base.CheckCRC();
                base.CheckConfigChange(_intialConfig);
                Log.Message("Verify registers after Unplug and Plug");
                base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, eventCalled);
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
                base.HotPlug(displayInfo.DisplayType, _defaultEDIDMap[displayInfo.DisplayType]);
                //base.CheckCRC();
                base.CheckConfigChange(_intialConfig);
                Log.Message("Verify registers after Unplug and Plug");
                base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, eventCalled);
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
        //        base.Hotplug(FunctionName.PLUG, displayInfo.DisplayType, displayInfo.DvmuPort, edidFile);
        //        //base.CheckCRC();
        //        base.CheckConfigChange(_intialConfig);
        //        Log.Message("Verify registers after Unplug and Plug");
        //        base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, eventCalled);
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
        //        base.Hotplug(FunctionName.PLUG, displayInfo.DisplayType, displayInfo.DvmuPort, edidFile);
        //        //base.CheckCRC();
        //        base.CheckConfigChange(_intialConfig);
        //        Log.Message("Verify registers after Unplug and Plug");
        //        base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, eventCalled);
        //    }
        //    else
        //        Log.Message("Cannot plug and unplug {0}", displayInfo.DisplayType);        
        //}       
    }
}
