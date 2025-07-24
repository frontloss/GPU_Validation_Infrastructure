using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class MP_Rotation_Basic_Scaling : MP_Rotation_Basic_DisableEnable
    {
        public override void TestPreCondition()
        {


        }
        [Test(Type = TestType.Method, Order = 1)]
        public override void TestStep1()
        {
            curAppliedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay };
            base.ApplyConfig(curAppliedConfig);
            ApplyNonNative();

            //curAppliedMode = new List<DisplayMode>();
            //DisplayType primary = curAppliedConfig.PrimaryDisplay;
            //DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == primary).First();
            //DisplayMode mode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            //curAppliedMode.Add(mode);

            base._angle = new List<uint>() { 180 };
            base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

            base._angle = new List<uint>() { 270 };
            base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

            base._angle = new List<uint>() { 90 };
            base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

            base._angle = new List<uint>() { 0 };
            base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

            if (base.CurrentConfig.SecondaryDisplay != DisplayType.None)
            {
                curAppliedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
                base.ApplyConfig(curAppliedConfig);
                ApplyNonNative();

                // curAppliedMode = new List<DisplayMode>();
                //primary = curAppliedConfig.PrimaryDisplay;
                //displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == primary).First();
                // mode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
                // curAppliedMode.Add(mode);

                base._angle = new List<uint>() { 270, 90 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                base._angle = new List<uint>() { 180, 270 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                base._angle = new List<uint>() { 90, 180 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                base._angle = new List<uint>() { 0, 0 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public override void TestStep2()
        {
            if (base.CurrentConfig.SecondaryDisplay != DisplayType.None)
            {
                curAppliedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
                base.ApplyConfig(curAppliedConfig);
                ApplyNonNative();

                //curAppliedMode = new List<DisplayMode>();
                //DisplayType primary = curAppliedConfig.PrimaryDisplay;
                //DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == primary).First();
                //DisplayMode mode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
                //curAppliedMode.Add(mode);

                //DisplayType secondary = curAppliedConfig.SecondaryDisplay;
                //displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == secondary).First();
                //mode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
                //curAppliedMode.Add(mode);

                base._angle = new List<uint>() { 270, 90 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                base._angle = new List<uint>() { 180, 270 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                base._angle = new List<uint>() { 90, 180 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                base._angle = new List<uint>() { 0, 0 };
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
                ApplyNonNative();

                //curAppliedMode = new List<DisplayMode>();
                //DisplayType primary = curAppliedConfig.PrimaryDisplay;
                //DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == primary).First();
                //DisplayMode mode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
                //curAppliedMode.Add(mode);              

                base._angle = new List<uint>() { 90, 270, 90 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                base._angle = new List<uint>() { 270, 180, 180 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                base._angle = new List<uint>() { 180, 90, 180 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                base._angle = new List<uint>() { 0, 0, 0 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();
            }
        }
        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
        {
            if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
            {
                curAppliedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
                base.ApplyConfig(curAppliedConfig);
                ApplyNonNative();

                base._angle = new List<uint>() { 90, 270, 90 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                base._angle = new List<uint>() { 270, 180, 180 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                base._angle = new List<uint>() { 180, 90, 180 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                base._angle = new List<uint>() { 0, 0, 0 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();
            }
        }
    }
}
