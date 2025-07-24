using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_Scaling_Smooth_CAR_Tri_Display_Config : SB_Scaling_Smooth_CAR_Lock_S3_S4_Reboot
    {

        List<uint> _prixList = null;
        List<uint> _priyList = null;

        List<uint> _secxList = null;
        List<uint> _secyList = null;

        List<uint> _trixList = null;
        List<uint> _triyList = null;

        [Test(Type = TestType.Method, Order = 1)]
        public override void TestStep1()
        {
            if (base.CurrentConfig.DisplayList.Contains(DisplayType.EDP))
                Log.Abort("this test is applicable only to dp and hdmi");

            base.ApplyConfig(base.CurrentConfig);

            _prixList = new List<uint>() { 50 };
            _priyList = new List<uint>() { 50 };
            GetModeForScaling(ScalingOptions.Customize_Aspect_Ratio, base.CurrentConfig.PrimaryDisplay, _prixList, _priyList);

            _secxList = new List<uint>() { 100 };
            _secyList = new List<uint>() { 50 };
            GetModeForScaling(ScalingOptions.Customize_Aspect_Ratio, base.CurrentConfig.SecondaryDisplay, _secxList, _secyList);

            if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
            {
                _trixList = new List<uint>() { 100 };
                _triyList = new List<uint>() { 50 };
                GetModeForScaling(ScalingOptions.Customize_Aspect_Ratio, base.CurrentConfig.TertiaryDisplay, _trixList, _triyList);
            }

        }
        [Test(Type = TestType.Method, Order = 2)]
        public override void TestStep2()
        {
            base.CheckRegister(base.CurrentConfig.PrimaryDisplay, ScalingOptions.Customize_Aspect_Ratio);
            base.CheckRegister(base.CurrentConfig.SecondaryDisplay, ScalingOptions.Customize_Aspect_Ratio);
            if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
            {
                base.CheckRegister(base.CurrentConfig.TertiaryDisplay, ScalingOptions.Customize_Aspect_Ratio);
            }
        }
        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            //skip the parent class Test3
        }
    }
}
