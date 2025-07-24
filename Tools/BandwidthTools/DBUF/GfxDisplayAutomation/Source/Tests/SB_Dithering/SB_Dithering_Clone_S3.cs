using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_Dithering_Clone_S3:SB_Dithering_Base
    {
        public SB_Dithering_Clone_S3()
        {
            _powerState = PowerStates.S3;
        }
      protected  DisplayConfig _config = null;
       protected Dictionary<int, DisplayConfig> _configList=null;
       protected PowerStates _powerState;
        [Test(Type = TestType.Method, Order = 0)]
        public void TestPreCondition()
        {
            if (base.CurrentConfig.DisplayList.Count<2)
                Log.Abort("The test needs atleast 2 displays"); // applies only DDC or TDC

            _configList = new Dictionary<int, DisplayConfig>() {{2,new DisplayConfig(){ConfigType=DisplayConfigType.DDC,PrimaryDisplay=base.CurrentConfig.PrimaryDisplay , SecondaryDisplay=base.CurrentConfig.SecondaryDisplay}},
            {3, new DisplayConfig(){ConfigType=DisplayConfigType.TDC , PrimaryDisplay=base.CurrentConfig.PrimaryDisplay , SecondaryDisplay=base.CurrentConfig.SecondaryDisplay , TertiaryDisplay=base.CurrentConfig.TertiaryDisplay}}};
           
            base.InstallDirectX();            
            base.EnumeratedDisplays.ForEach(curDisp =>
            {
                Log.Message("{0}: {1}", curDisp.DisplayType, curDisp.ColorInfo.MaxDeepColorValue);
            });            
        }
        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            if (_configList.Keys.ToList().Contains(base.CurrentConfig.DisplayList.Count))
            {
                _config = _configList[base.CurrentConfig.DisplayList.Count];
                base.ApplyConfigOS(_config);
                Enable10BitScanner(8);
                _config.CustomDisplayList.ForEach(curDisp =>
                    {
                        base.CheckDithering(curDisp, DeepColorAppType.None);
                    });              
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            base.InvokePowerEvent(_powerState);
            base.Disable10BitScanner();
            base.CloseApp();
        }
        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep3()
        {
            _config.CustomDisplayList.ForEach(curDisp =>
            {
                base.CheckDithering(curDisp, DeepColorAppType.None);
            }); 
        }
        [Test(Type = TestType.Method, Order = 4)]
        public virtual void TestStep4()
        {
            base.EnableFP16();
            _config.CustomDisplayList.ForEach(curDisp =>
            {
                base.CheckDithering(curDisp, DeepColorAppType.FP16);
            });
        }
        [Test(Type = TestType.Method, Order = 5)]
        public virtual void TestStep5()
        {
            base.InvokePowerEvent(_powerState);
        }
        [Test(Type = TestType.Method, Order = 6)]
        public virtual void TestStep6()
        {
            _config.CustomDisplayList.ForEach(curDisp =>
            {
                base.CheckDithering(curDisp, DeepColorAppType.None);
            });
            base.DisableFP16();
            base.CloseApp();
        }
    }
}
