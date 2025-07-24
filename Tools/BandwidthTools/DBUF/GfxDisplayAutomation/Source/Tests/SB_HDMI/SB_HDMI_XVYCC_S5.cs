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
    [Test(Type = TestType.HasReboot)]
    class SB_HDMI_XVYCC_S5 : SB_HDMI_XVYCC_Basic
    {
        private PowerStates powerState = PowerStates.S5;
        private PowerParams _powerParams = null;  
        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            Log.Message(true, "Reboot the machine.");
            this._powerParams = new PowerParams();
            this._powerParams.Delay = 5;
            base.InvokePowerEvent(this._powerParams, PowerStates.S5);
        }
        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
        {
            base.CheckConfigChange(base.CurrentConfig);
            Log.Message(true, "Check {0} is Enabled after {1}", _colorType, powerState);
            foreach (DisplayType display in base.CurrentConfig.DisplayList)
            {
                DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
                DisplayHierarchy dh = base.GetDispHierarchy(base.CurrentConfig.CustomDisplayList, display);
                if (displayInfo.ColorInfo.IsXvYcc)
                {
                    Log.Message("{0} is supported on {1}", _colorType, displayInfo.DisplayType);
                    Log.Message(true, "Verify {0} enabled on {1} using Registers and CUI", _colorType, displayInfo.DisplayType);
                    base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, enableEvent);
                }
                if (!displayInfo.ColorInfo.IsXvYcc && !displayInfo.ColorInfo.IsYcBcr)
                {
                    Log.Message("{0} is not supported on {1}", _colorType, displayInfo.DisplayType);
                    base.RegisterCheck(display, displayInfo, displayHierarchy, nonHDMIPanelEvent);
                    //base.CheckCRC();
                }
            }
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            base.TestStep3();
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
                DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
                DisplayHierarchy dh = base.GetDispHierarchy(base.CurrentConfig.CustomDisplayList, display);
                if (displayInfo.ColorInfo.IsXvYcc)
                {
                    Log.Message("{0} is supported on {1}", _colorType, displayInfo.DisplayType);
                    Log.Message(true, "Verify {0} disabled on {1} using Registers and CUI", _colorType, displayInfo.DisplayType);
                    base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, disableEvent);

                }
                if (!displayInfo.ColorInfo.IsXvYcc && !displayInfo.ColorInfo.IsYcBcr)
                {
                    Log.Message("{0} is not supported on {1}", _colorType, displayInfo.DisplayType);
                    base.RegisterCheck(display, displayInfo, displayHierarchy, nonHDMIPanelEvent);
                    //base.CheckCRC();
                }
            }
        }
        [Test(Type = TestType.Method, Order = 8)]
        public void TestStep8()
        {
            base.Hotplug(FunctionName.OPEN, DisplayType.HDMI, DVMU_PORT.PORTA);

            Log.Message(true, "Unplug all displays connnected");
            base.CurrentConfig.DisplayList.Intersect(_defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                base.HotUnPlug(curDisp);
            });
        }
    }
}
