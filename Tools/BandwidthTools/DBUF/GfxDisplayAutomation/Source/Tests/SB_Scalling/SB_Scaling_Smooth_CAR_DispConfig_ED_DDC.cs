using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_Scaling_Smooth_CAR_DispConfig_ED_DDC : SB_Scaling_Smooth_CAR_Lock_S3_S4_Reboot
    {
        List<uint> _prixList = null;
        List<uint> _priyList = null;

        List<uint> _secxList = null;
        List<uint> _secyList = null;
        PowerParams powerParam = new PowerParams();

        DisplayScaling _priScalingApplied = null;
        DisplayMode _priModeApplied = new DisplayMode();

        DisplayScaling _secScalingApplied = null;
        DisplayMode _secModeApplied = new DisplayMode();
        [Test(Type = TestType.Method, Order = 1)]
        public override void TestStep1()
        {
            base.ApplyConfig(base.CurrentConfig);

            AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
            if (!AccessInterface.SetFeature<bool, DecisionActions>(Features.LaunchCUI, Action.SetMethod, DecisionActions.No))
                Log.Fail(false, "Unable to launch CUI!");

            _prixList = new List<uint>() { 50 };
            _priyList = new List<uint>() { 50 };
            GetModeForScaling(ScalingOptions.Customize_Aspect_Ratio, base.CurrentConfig.PrimaryDisplay, _prixList, _priyList);

            _secxList = new List<uint>() { 100 };
            _secyList = new List<uint>() { 50 };
            GetModeForScaling(ScalingOptions.Customize_Aspect_Ratio, base.CurrentConfig.SecondaryDisplay, _secxList, _secyList);

           
        }
        [Test(Type = TestType.Method, Order = 2)]
        public override void TestStep2()
        {
            DisplaySwap(base.CurrentConfig.SecondaryDisplay, base.CurrentConfig.PrimaryDisplay);
            base.VerifyPersistance(base.CurrentConfig.PrimaryDisplay,_priScalingApplied,_priModeApplied);
            base.VerifyPersistance(base.CurrentConfig.SecondaryDisplay, _secScalingApplied, _secModeApplied);
        }

        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            GetModeForScaling(ScalingOptions.Maintain_Display_Scaling, base.CurrentConfig.PrimaryDisplay);
            base.CheckRegister(base.CurrentConfig.SecondaryDisplay, ScalingOptions.Customize_Aspect_Ratio);
        }

        [Test(Type = TestType.Method, Order = 4)]
        public virtual void TestStep4()
        {
            DisplaySwap(base.CurrentConfig.PrimaryDisplay,base.CurrentConfig.SecondaryDisplay);
            base.VerifyPersistance(base.CurrentConfig.PrimaryDisplay, _priScalingApplied, _priModeApplied);
            base.VerifyPersistance(base.CurrentConfig.SecondaryDisplay, _secScalingApplied, _secModeApplied);
        }
        [Test(Type = TestType.Method, Order = 5)]
        public  void TestStep5()
        {
            GetModeForScaling(ScalingOptions.Maintain_Display_Scaling, base.CurrentConfig.SecondaryDisplay);
            base.CheckRegister(base.CurrentConfig.PrimaryDisplay, ScalingOptions.Maintain_Display_Scaling);

            AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
        }
        public void DisplaySwap(DisplayType argDispPri, DisplayType argDispSec)
        {
            Log.Message(true,"Swap the display set pri:{0} and sec:{1}",argDispPri,argDispSec);
            _priScalingApplied = AccessInterface.GetFeature<DisplayScaling, DisplayType>(Features.Scaling, Action.GetMethod, Source.AccessAPI, base.CurrentConfig.PrimaryDisplay);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == base.CurrentConfig.PrimaryDisplay).First();
            _priModeApplied = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);

            _secScalingApplied = AccessInterface.GetFeature<DisplayScaling, DisplayType>(Features.Scaling, Action.GetMethod, Source.AccessAPI, base.CurrentConfig.SecondaryDisplay);
             displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == base.CurrentConfig.SecondaryDisplay).First();
            _secModeApplied = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);

            DisplayConfig currentConfig = new DisplayConfig();
            currentConfig.ConfigType = base.CurrentConfig.ConfigType;

            currentConfig.PrimaryDisplay = argDispPri;
            currentConfig.SecondaryDisplay = argDispSec;
            

            AccessInterface.Navigate(Features.Config);
            AccessInterface.SetFeature<DisplayConfig>(Features.Config, Action.Set, Source.AccessUI, currentConfig);
            if (AccessInterface.SetFeature<bool, AppBarOptions>(Features.AppBar, Action.SetMethod, AppBarOptions.Apply))
                AccessInterface.SetFeature(Features.ConfirmationPopup, Action.Set, DecisionActions.Yes);
        }
    }
}
