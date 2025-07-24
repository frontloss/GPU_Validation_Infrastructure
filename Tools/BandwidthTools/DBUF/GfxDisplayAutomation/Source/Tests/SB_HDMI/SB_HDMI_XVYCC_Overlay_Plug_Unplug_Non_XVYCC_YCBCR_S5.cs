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
    class SB_HDMI_XVYCC_Overlay_Plug_Unplug_Non_XVYCC_YCBCR_S5 : SB_HDMI_XVYCC_Overlay_Plug_Unplug_YCBCR_S5
    {
        private string edidFileAfterS5 = "HDMI_3011_xvycc_Remove_RGB.EDID";

        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
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
                if (displayInfo.DvmuPort != DVMU_PORT.None)
                {
                    //Log.Message("Check if the xvycc/ycbcr option is not coming in CUI");
                    //base.VerifyNonXvyccYcvcrPanel(displayInfo.DisplayType);
                    Log.Message("Verify registers for Non-Xvycc/Ycbcr panel");
                    if ((dh != DisplayHierarchy.Display_1) && (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
                        eventCalled = base.cloneModeSecondaryOverlay;
                    else
                        eventCalled = nonHDMIPanelEventSprite;
                    Thread.Sleep(5000);
                    base.PlayAndMoveVideo(dh, base.CurrentConfig);
                    base.RegisterCheck(display, displayInfo, dh, eventCalled);
                }
            }
            read.Close();
        }
        [Test(Type = TestType.Method, Order = 5)]
        public override void TestStep5()
        {
            foreach (DisplayType display in base.CurrentConfig.DisplayList)
            {
                DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
                DisplayHierarchy dh = base.GetDispHierarchy(base.CurrentConfig.CustomDisplayList, display);
                if (displayInfo.DvmuPort != DVMU_PORT.None)
                {
                    Log.Message(true, "Plug back {0} panel for the test to continue", _colorType);
                    Log.Verbose("Unplug {0} panel on display {1}", _colorType, displayInfo.DisplayType);
                    base.Hotplug(FunctionName.UNPLUG, displayInfo.DisplayType, displayInfo.DvmuPort);
                    Log.Verbose("Plug panel on display {0}", displayInfo.DisplayType);
                    base.Hotplug(FunctionName.PLUG, displayInfo.DisplayType, displayInfo.DvmuPort, edidFile);
                }
            }
        }
        [Test(Type = TestType.Method, Order = 8)]
        public override void TestStep8()
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
                if (displayInfo.DvmuPort != DVMU_PORT.None)
                {
                    //Log.Message("Check if the xvycc/ycbcr option is not coming in CUI");
                    //base.VerifyNonXvyccYcvcrPanel(displayInfo.DisplayType);
                    Log.Message("Verify registers for Non-Xvycc/Ycbcr panel");
                    if ((dh != DisplayHierarchy.Display_1) && (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
                        eventCalled = base.cloneModeSecondaryOverlay;
                    else
                        eventCalled = nonHDMIPanelEventSprite;
                    Thread.Sleep(5000);
                    base.PlayAndMoveVideo(dh, base.CurrentConfig);
                    base.RegisterCheck(display, displayInfo, dh, eventCalled);
                }
            }
        }
    }
}
