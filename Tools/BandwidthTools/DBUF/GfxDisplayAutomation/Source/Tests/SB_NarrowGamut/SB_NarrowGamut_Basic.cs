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
    class SB_NarrowGamut_Basic : SB_NarrowGamut_Base
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
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
            if (base.MachineInfo.PlatformDetails.Platform != Platform.CHV)
            { // csc is always enabled in chv , hence disbale state is not being checked.
                base.NarrowGamutSupportedDisplays.Intersect(base.CurrentConfig.DisplayList).ToList().ForEach(curDisp =>
                {
                    base.SetNarrowGamutStatus(curDisp, NarrowGamutOption.DisbaleNarrowGamut);
                });
            }
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Test clean up- Unplug all displays");
            _pluggableDisplaySim.ForEach(curDisp =>
            {
                base.HotUnPlug(curDisp);
            });
            base.CleanUpHotplugFramework();
            RevertNarrowGamutChanges();
        }
      
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Test Execution Completed");                           
        }             
    }
}
