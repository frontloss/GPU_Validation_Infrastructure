namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_Deepcolor_DisplayConfig_DPApplet : SB_DeepColor_Base
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            EnableDPApplet();
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            foreach (DisplayType display in base.CurrentConfig.DisplayList)
            {
                DisplayInfo dispInfo = CurrentConfig.EnumeratedDisplays.Find(dp => dp.DisplayType == display);
                PipePlaneParams pipePlane = GetPipePlane(dispInfo);
                CheckDeepColorconditions(dispInfo, pipePlane, DeepColorAppType.DPApplet, true, CurrentConfig, DisplayHierarchy.Display_1);
            }
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            if (null != this._actionAfterEnable)
                this._actionAfterEnable();
        }

        [Test(Type = TestType.Method, Order = 4)]
        public virtual void TestStep4()
        {
            DisableDPApplet();
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            foreach (DisplayType display in base.CurrentConfig.DisplayList)
            {
                DisplayInfo dispInfo = CurrentConfig.EnumeratedDisplays.Find(dp => dp.DisplayType == display);
                PipePlaneParams pipePlane = GetPipePlane(dispInfo);
                CheckDeepColorconditions(dispInfo, pipePlane, DeepColorAppType.DPApplet, false, CurrentConfig, DisplayHierarchy.Display_1);
            }
        }

        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            if (null != this._actionAfterDisable)
                this._actionAfterDisable();
        }

        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            CloseApp(DeepColorAppType.DPApplet);
        }
    }
}
