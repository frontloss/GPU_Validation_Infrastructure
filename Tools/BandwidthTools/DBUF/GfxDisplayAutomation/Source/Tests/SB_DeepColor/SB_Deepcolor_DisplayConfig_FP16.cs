namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_Deepcolor_DisplayConfig_FP16 : SB_DeepColor_Base
    {
         Boolean _isExtendedMode;
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            //check if the mode is extended mode.
            _isExtendedMode = base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Extended ? true : false;
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            EnableFP16();
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            foreach (DisplayType display in base.CurrentConfig.DisplayList)
            {
                DisplayInfo dispInfo = CurrentConfig.EnumeratedDisplays.Find(dp => dp.DisplayType == display);
                PipePlaneParams pipePlane = GetPipePlane(dispInfo);
                CheckDeepColorconditions(dispInfo, pipePlane, DeepColorAppType.FP16, true, CurrentConfig, DisplayHierarchy.Display_1);
            }
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            DisableFP16();
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            foreach (DisplayType display in base.CurrentConfig.DisplayList)
            {
                DisplayInfo dispInfo = CurrentConfig.EnumeratedDisplays.Find(dp => dp.DisplayType == display);
                PipePlaneParams pipePlane = GetPipePlane(dispInfo);
                CheckDeepColorconditions(dispInfo, pipePlane, DeepColorAppType.FP16, false, CurrentConfig, DisplayHierarchy.Display_1);
            }
        }

        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            if (_isExtendedMode)
            {
                MoveFP16(DisplayHierarchy.Display_2);
                EnableFP16();
                foreach (DisplayType display in base.CurrentConfig.DisplayList)
                {
                    DisplayInfo dispInfo = CurrentConfig.EnumeratedDisplays.Find(dp => dp.DisplayType == display);
                    PipePlaneParams pipePlane = GetPipePlane(dispInfo);
                    CheckDeepColorconditions(dispInfo, pipePlane, DeepColorAppType.FP16, true, CurrentConfig, DisplayHierarchy.Display_2);
                   // CheckDitheringBPC(dispInfo, pipePlane);
                }
            }
        }

        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            if (_isExtendedMode)
            {
                DisableFP16();

                foreach (DisplayType display in base.CurrentConfig.DisplayList)
                {
                    DisplayInfo dispInfo = CurrentConfig.EnumeratedDisplays.Find(dp => dp.DisplayType == display);
                    PipePlaneParams pipePlane = GetPipePlane(dispInfo);
                    CheckDeepColorconditions(dispInfo, pipePlane, DeepColorAppType.FP16, false, CurrentConfig, DisplayHierarchy.Display_2);
                }
            }
        }

        [Test(Type = TestType.Method, Order = 8)]
        public void TestStep8()
        {
            if (CurrentConfig.ConfigType == DisplayConfigType.TED)
            {
                MoveFP16(DisplayHierarchy.Display_3);
                EnableFP16();

                foreach (DisplayType display in base.CurrentConfig.DisplayList)
                {
                    DisplayInfo dispInfo = CurrentConfig.EnumeratedDisplays.Find(dp => dp.DisplayType == display);
                    PipePlaneParams pipePlane = GetPipePlane(dispInfo);
                    CheckDeepColorconditions(dispInfo, pipePlane, DeepColorAppType.FP16, true, CurrentConfig, DisplayHierarchy.Display_3);
                }
            }
        }

        [Test(Type = TestType.Method, Order = 9)]
        public void TestStep9()
        {
            if (CurrentConfig.ConfigType == DisplayConfigType.TED)
            {
                DisableFP16();
              

                foreach (DisplayType display in base.CurrentConfig.DisplayList)
                {
                    DisplayInfo dispInfo = CurrentConfig.EnumeratedDisplays.Find(dp => dp.DisplayType == display);
                    PipePlaneParams pipePlane = GetPipePlane(dispInfo);
                    CheckDeepColorconditions(dispInfo, pipePlane, DeepColorAppType.FP16, false, CurrentConfig, DisplayHierarchy.Display_3);
                }
            }
        }

        [Test(Type = TestType.Method, Order = 10)]
        public void TestStep10()
        {
            CloseApp(DeepColorAppType.FP16);
        }

    }
}
