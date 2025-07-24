using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class MP_Rotation_Basic_SD_DDC_TDC : MP_Rotation_Basic_DisableEnable
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public override void TestPreCondition()
        {
            curAppliedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay };
            base.ApplyConfig(curAppliedConfig);

            base._angle = new List<uint>() { 90 };
            base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

            base._angle = new List<uint>() { 180 };
            base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();
        }
        [Test(Type = TestType.Method, Order = 1)]
        public override void TestStep1()
        {
            if (base.CurrentConfig.SecondaryDisplay != DisplayType.None)
            {
                curAppliedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
                base.ApplyConfig(curAppliedConfig);

                base._angle = new List<uint>() { 270, 90 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                base._angle = new List<uint>() { 180, 270 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                base._angle = new List<uint>() { 90, 180 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public override void TestStep2()
        {
            if (base.CurrentConfig.SecondaryDisplay != DisplayType.None)
            {
                curAppliedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay };
                base.ApplyConfig(curAppliedConfig);

                base._angle = new List<uint>() { 270, 90 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                curAppliedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay };
                base.ApplyConfig(curAppliedConfig);

                base._angle = new List<uint>() { 180, 90 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();
            }
        }

        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
            {
                curAppliedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
                base.ApplyConfig(curAppliedConfig);

                base._angle = new List<uint>() { 180, 90, 180 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();
            }
        }
        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
        {
            curAppliedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay };
            base.ApplyConfig(curAppliedConfig);

            base._angle = new List<uint>() { 0 };
            base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();
        }
    }
}
