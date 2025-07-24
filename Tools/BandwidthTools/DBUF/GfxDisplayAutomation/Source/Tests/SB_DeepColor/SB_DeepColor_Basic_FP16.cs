namespace Intel.VPG.Display.Automation
{
    using System;

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_DeepColor_Basic_FP16 : SB_DeepColor_Base
    {
        DisplayInfo _DiplayInfo;
        DeepColorAppType _AppType;

        public SB_DeepColor_Basic_FP16()
            : base()
        {
            this._AppType = DeepColorAppType.FP16;
        }

        public SB_DeepColor_Basic_FP16(DeepColorAppType AppType)
            : this()
        {
            this._AppType = AppType;
        }

        [Test(Type = TestType.PreCondition, Order = 0)]
        public override void TestPreCondition()
        {
            if (DisplayConfigType.SD != CurrentConfig.ConfigType)
                Log.Abort("Only SD Mode Supported by Basic Test");

            base.TestPreCondition();

            _DiplayInfo = CurrentConfig.EnumeratedDisplays.Find(dp => dp.DisplayType == CurrentConfig.PrimaryDisplay);
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
          base.EnableDeepColor(_AppType);
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            PipePlaneParams pipePlane = GetPipePlane(_DiplayInfo);
            CheckDeepColorconditions(_DiplayInfo, pipePlane, DeepColorAppType.FP16, true, CurrentConfig, DisplayHierarchy.Display_1);
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            DisableDeepColor(_AppType);
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            PipePlaneParams pipePlane = GetPipePlane(_DiplayInfo);
            CheckDeepColorconditions(_DiplayInfo, pipePlane, _AppType, false, CurrentConfig, DisplayHierarchy.Display_1);
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            CloseApp(_AppType);
        }
    }
}