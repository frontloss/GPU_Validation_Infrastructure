using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using System.Windows.Forms;
namespace Intel.VPG.Display.Automation
{
     [Test(Type = TestType.HasReboot)]
     [Test(Type = TestType.HasINFModify)]
     [Test(Type = TestType.HasPlugUnPlug)]
    class SB_WideGamut_MonitorTurnOff:SB_WideGamut_Base
    {
        public SB_WideGamut_MonitorTurnOff()
        {
            base._wideGamutLevel = WideGamutLevel.LEVEL3;
        }
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.WideGamutDriver(7);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            base.PlugDisplays();
            base.ApplyConfigOS(base.CurrentConfig);
        }    
         [Test(Type = TestType.Method, Order = 3)]
         public virtual void TestStep3()
         {             
             base.CurrentConfig.DisplayList.ForEach(curDisp =>
             {
                 SendKeys.SendWait("{ESC}");
                 base.ApplyWideGamutToDisplay(curDisp, base._wideGamutLevel);
                 base.VerifyWideGamutValue(curDisp, _wideGamutLevel);
             });
         }
         [Test(Type = TestType.Method, Order = 4)]
         public virtual void TestStep4()
         {
             Log.Message(true, "Turn off the monitor for 1 min");
             MonitorTurnOffParam monitorTurnOffOnObject = new MonitorTurnOffParam()
             {
                 onOffParam = MonitorOnOff.Off,
                 waitingTime = 10
             };
             if (AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorTurnOffOnObject))
                 Log.Success("Monitor turn On and Off successful");
             else
                 Log.Fail("Monitor Turn On and Off Operation Fail");

             _pluggableDisplaySim.ForEach(curDisp =>
             {
                 base.HotUnPlug(curDisp);
             });
             _pluggableDisplaySim.Clear();
             
             base.PlugDisplays();

             
             monitorTurnOffOnObject = new MonitorTurnOffParam()
             {
                 onOffParam = MonitorOnOff.On,
                 waitingTime = 10
             };
             if (AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorTurnOffOnObject))
                 Log.Success("Monitor turn on successful");    
             else
                 Log.Fail("Failed to resume from monitor turn off");
         }
         [Test(Type = TestType.Method, Order = 5)]
         public virtual void TestStep5()
         {
             SendKeys.SendWait("{ESC}");
             DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
             if (currentConfig.GetCurrentConfigStr().Equals(base.CurrentConfig.GetCurrentConfigStr()))
                 Log.Success("{0} retained",base.CurrentConfig.GetCurrentConfigStr());
             else
                 Log.Fail("Expected:{0} , current: {1}",base.CurrentConfig.GetCurrentConfigStr() , currentConfig.GetCurrentConfigStr());
             base.CurrentConfig.DisplayList.ForEach(curDisp =>
             {
                 VerifyWideGamutValue(curDisp, base._wideGamutLevel);
             });
             Log.Message(true, "Test clean up- Unplug all displays");
             base.UnPlugDisplays();
         }
         [Test(Type = TestType.Method, Order = 6)]
         public virtual void TestStep6()
         {
             base.WideGamutDriver(0);
         }
         [Test(Type = TestType.Method, Order = 7)]
         public virtual void TestStep7()
         {
             Log.Message(true, "Test Execution completed");
         }
    }
}
