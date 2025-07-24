using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Win32;
namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    [Test(Type = TestType.HasINFModify)]
    class SB_NarrowGamut_DisplaySwap : SB_NarrowGamut_Base
    {
        public Dictionary<int, System.Action> DisplaySwap
        {
            get { Dictionary<int, System.Action> dispSwap = new Dictionary<int, System.Action>() { { 2, PerformDualSwap }, { 3, PerformTriSwap }}; return dispSwap; }
        }
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.DisplayList.Count < 2)
                Log.Abort("please provide atleast 2 displays");
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.NarrowGamutDriver(NarrowGamutOption.EnableINF);                        
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            base.VerifyInfChanges(NarrowGamutOption.VerifyINF);
            base.InitializeHotplugFramework();
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                if (base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).Select(dI => dI.DisplayType).FirstOrDefault() == DisplayType.None)
                {
                    base.HotPlug(curDisp, _defaultEDIDMap[curDisp]);
                    _pluggableDisplaySim.Add(curDisp);
                }
            });
            base.ApplyConfig(base.CurrentConfig);
            base.NarrowGamutSupportedDisplays.Intersect(base.CurrentConfig.DisplayList).ToList().ForEach(curDisp =>
            {
                base.SetNarrowGamutStatus(curDisp, NarrowGamutOption.EnableNarrowGamut);
            });
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            DisplaySwap[base.CurrentConfig.ConfigTypeCount]();            
        }
        [Test(Type = TestType.Method, Order = 4)]
        public virtual void TestStep4()
        {
            if (base.MachineInfo.PlatformDetails.Platform != Platform.CHV)
            { // csc is always enabled in chv , hence disbale state is not being checked.
                base.NarrowGamutSupportedDisplays.Intersect(base.CurrentConfig.DisplayList).ToList().ForEach(curDisp =>
                {
                    base.SetNarrowGamutStatus(curDisp, NarrowGamutOption.DisbaleNarrowGamut);
                });
            }
        }
        [Test(Type = TestType.Method, Order = 5)]
        public virtual void TestStep5()
        {
            Log.Message(true, "Test clean up- Unplug all displays");
            _pluggableDisplaySim.ForEach(curDisp =>
            {
                base.HotUnPlug(curDisp);
            });
            base.CleanUpHotplugFramework();
            base.RevertNarrowGamutChanges();
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            Log.Message(true, "Test Execution Completed");            
        }
       
        private void PerformDualSwap()
        {
            DisplayConfig swap = new DisplayConfig()
            {
                ConfigType = base.CurrentConfig.ConfigType,
                PrimaryDisplay = base.CurrentConfig.SecondaryDisplay,
                SecondaryDisplay = base.CurrentConfig.PrimaryDisplay
            };
            base.ApplyConfig(swap);
            base.NarrowGamutSupportedDisplays.Intersect(swap.DisplayList).ToList().ForEach(curDisp =>
            {
                base.CheckNarrowGamutRegister(curDisp, NarrowGamutOption.EnableNarrowGamut);
            });

            base.ApplyConfig(base.CurrentConfig);
            base.NarrowGamutSupportedDisplays.Intersect(base.CurrentConfig.DisplayList).ToList().ForEach(curDisp =>
            {
                base.CheckNarrowGamutRegister(curDisp, NarrowGamutOption.EnableNarrowGamut);
            });            
        }

        private void PerformTriSwap()
        {
            DisplayConfig swap = new DisplayConfig()
            {
                ConfigType = base.CurrentConfig.ConfigType,
                PrimaryDisplay = base.CurrentConfig.SecondaryDisplay,
                SecondaryDisplay = base.CurrentConfig.TertiaryDisplay,
                TertiaryDisplay = base.CurrentConfig.PrimaryDisplay
            };
            base.ApplyConfig(swap);
            base.NarrowGamutSupportedDisplays.Intersect(swap.DisplayList).ToList().ForEach(curDisp =>
            {
                base.CheckNarrowGamutRegister(curDisp, NarrowGamutOption.EnableNarrowGamut);
            });

            swap = new DisplayConfig()
            {
                ConfigType = base.CurrentConfig.ConfigType,
                PrimaryDisplay = base.CurrentConfig.TertiaryDisplay,
                SecondaryDisplay = base.CurrentConfig.PrimaryDisplay,
                TertiaryDisplay = base.CurrentConfig.SecondaryDisplay
            };
            base.ApplyConfig(swap);
            base.NarrowGamutSupportedDisplays.Intersect(swap.DisplayList).ToList().ForEach(curDisp =>
            {
                base.CheckNarrowGamutRegister(curDisp, NarrowGamutOption.EnableNarrowGamut);
            });

            base.ApplyConfig(base.CurrentConfig);
            base.NarrowGamutSupportedDisplays.Intersect(base.CurrentConfig.DisplayList).ToList().ForEach(curDisp =>
            {
                base.CheckNarrowGamutRegister(curDisp, NarrowGamutOption.EnableNarrowGamut);
            });            
        }
    }
}
