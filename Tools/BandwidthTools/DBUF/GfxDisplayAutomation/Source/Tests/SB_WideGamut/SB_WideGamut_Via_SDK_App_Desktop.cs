using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
namespace Intel.VPG.Display.Automation
{
    class SB_WideGamut_Via_SDK_App_Desktop:SB_WideGamut_Base
    {
       Dictionary<DisplayConfigType, List<DisplayConfig>> _displayConfigList = null;
          public virtual void TestStep0()
        {
            Log.Message(true, "Disabling Driver Signature Enforcement");
            SetBCDEditOptions("-set loadoptions DDISABLE_INTEGRITY_CHECKS", "-set TESTSIGNING ON");          
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message("Verify Disabling Driver Signature Enforcement");
            CheckBCDEditOptions("loadoptions DDISABLE_INTEGRITY_CHECKS", "testSigning Yes");
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            base.WideGamutDriver(7);
            _displayConfigList = new Dictionary<DisplayConfigType, List<DisplayConfig>>();
            
            List<DisplayConfig> sdList = new List<DisplayConfig>();
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
                {
                    DisplayConfig curConfig = new DisplayConfig();
                    curConfig.ConfigType = DisplayConfigType.SD;
                    curConfig.PrimaryDisplay = curDisp;
                    sdList.Add(curConfig);
                });
            _displayConfigList.Add(DisplayConfigType.SD, sdList);

            List<DisplayConfig> ddcList = new List<DisplayConfig>();
            DisplayConfig config = new DisplayConfig();
            config.ConfigType = DisplayConfigType.ED;
            config.PrimaryDisplay = base.CurrentConfig.PrimaryDisplay;
            config.SecondaryDisplay = base.CurrentConfig.SecondaryDisplay;

            ddcList.Add(base.CurrentConfig);
            ddcList.Add(config);
            _displayConfigList.Add(DisplayConfigType.DDC, ddcList);

            List<DisplayConfig> edList = new List<DisplayConfig>();
             config = new DisplayConfig();
            config.ConfigType = DisplayConfigType.DDC;
            config.PrimaryDisplay = base.CurrentConfig.PrimaryDisplay;
            config.SecondaryDisplay = base.CurrentConfig.SecondaryDisplay;

            edList.Add(base.CurrentConfig);
            edList.Add(config);
            _displayConfigList.Add(DisplayConfigType.ED, edList);

            List<DisplayConfig> tdcList = new List<DisplayConfig>();
            config = new DisplayConfig();
            config.ConfigType = DisplayConfigType.TED;
            config.PrimaryDisplay = base.CurrentConfig.PrimaryDisplay;
            config.SecondaryDisplay = base.CurrentConfig.SecondaryDisplay;
            config.TertiaryDisplay = base.CurrentConfig.TertiaryDisplay;

            tdcList.Add(base.CurrentConfig);
            tdcList.Add(config);
            _displayConfigList.Add(DisplayConfigType.TDC, tdcList);

            List<DisplayConfig> tedList = new List<DisplayConfig>();
            config = new DisplayConfig();
            config.ConfigType = DisplayConfigType.TDC;
            config.PrimaryDisplay = base.CurrentConfig.PrimaryDisplay;
            config.SecondaryDisplay = base.CurrentConfig.SecondaryDisplay;
            config.TertiaryDisplay = base.CurrentConfig.TertiaryDisplay;

            tedList.Add(base.CurrentConfig);
            tedList.Add(config);
            _displayConfigList.Add(DisplayConfigType.TED, tedList);

        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            if (_displayConfigList.Keys.Contains(base.CurrentConfig.ConfigType))
            {
                List<DisplayConfig> configList = _displayConfigList[base.CurrentConfig.ConfigType];
                configList.ForEach(curConfig =>
                {
                    base.ApplyConfigOS(curConfig);
                    curConfig.CustomDisplayList.ForEach(curDisp =>
                    {
                        base.ApplyWideGamutToDisplay(curDisp, base._wideGamutLevel);
                        Thread.Sleep(5000);
                        base.VerifyWideGamutValue(curDisp, base._wideGamutLevel);
                    });
                   
                    base.InvokePowerEvent(PowerStates.S3);
                    Thread.Sleep(5000);
                    curConfig.CustomDisplayList.ForEach(curDisp =>
                    {
                        base.VerifyWideGamutValue(curDisp, base._wideGamutLevel);
                    });     
                });
                
                //update script as per QC
            }
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            base.WideGamutDriver(0);
        }
       
    }
}
