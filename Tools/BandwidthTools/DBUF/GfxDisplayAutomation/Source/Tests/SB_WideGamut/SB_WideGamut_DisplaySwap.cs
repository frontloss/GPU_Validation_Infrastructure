namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.HasINFModify)]
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_WideGamut_DisplaySwap:SB_WideGamut_Base
    {
        protected Dictionary<int, System.Action> _configSwap = null;
        public SB_WideGamut_DisplaySwap()
        {
            _configSwap = new Dictionary<int, System.Action>() {{2,PerformDualSwap},
            {3,PerformTriSwap}};
            base._wideGamutLevel = WideGamutLevel.LEVEL2;
        }
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.ConfigType == DisplayConfigType.SD)
                Log.Abort("Display Swap does not support SD ");

            //Log.Message(true, "Disabling Driver Signature Enforcement");
            //SetBCDEditOptions("-set loadoptions DDISABLE_INTEGRITY_CHECKS", "-set TESTSIGNING ON"); 
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            //Log.Message("Verify Disabling Driver Signature Enforcement");
            //CheckBCDEditOptions("loadoptions DDISABLE_INTEGRITY_CHECKS", "testSigning Yes");
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            base.WideGamutDriver(7);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            base.InitializeHotplugFramework();
            base.CurrentConfig.PluggableDisplayList.ForEach(curDisp =>
            {
                HotPlug(curDisp, _defaultEDIDMap[curDisp]);
                _pluggableDisplaySim.Add(curDisp);
            });

            base.ApplyConfigOS(base.CurrentConfig);
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                base.ApplyWideGamutToDisplay(curDisp, base._wideGamutLevel);
            });
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            _configSwap[base.CurrentConfig.ConfigType.GetDisplaysCount()]();

            Log.Message(true, "Test clean up- Unplug all displays");
            _pluggableDisplaySim.ForEach(curDisp =>
            {
                base.HotUnPlug(curDisp);
            });
            base.CleanUpHotplugFramework();
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            base.WideGamutDriver(0);
        }
        protected void PerformDualSwap()
        {
                    DisplayConfig swap1 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay };
                    base.ApplyConfigOS(swap1);
                    Verify_WG_Val(swap1);

                    base.ApplyConfigOS(base.CurrentConfig);
                    Verify_WG_Val(base.CurrentConfig);
        }
        protected void PerformTriSwap()
        {
            DisplayConfig swap1 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay, TertiaryDisplay = base.CurrentConfig.PrimaryDisplay };
            base.ApplyConfigOS(swap1);
            Verify_WG_Val(swap1);

            DisplayConfig swap2 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
            base.ApplyConfigOS(swap2);
            Verify_WG_Val(swap2);
                    
            base.ApplyConfigOS(base.CurrentConfig);
            Verify_WG_Val(base.CurrentConfig);
        }
        protected void Verify_WG_Val(DisplayConfig customConfig) 
        {
            customConfig.DisplayList.ForEach(curDisp =>
            {
                VerifyWideGamutValue(curDisp, base._wideGamutLevel);
            });
        }
    }
}
