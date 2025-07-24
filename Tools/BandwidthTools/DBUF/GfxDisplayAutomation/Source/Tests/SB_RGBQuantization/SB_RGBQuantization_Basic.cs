namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System;
    using System.IO;

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_RGBQuantization_Basic : SB_RGBQuantization_Base
    {
        protected ColorType _colorType = ColorType.XvYCC;
        protected string edidFile = "rgb_quantization_samsung.EDID";

        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.ConfigTypeCount > base.CurrentConfig.DisplayList.Count())
                Log.Abort("{0} requires atleast {1} Displays to be enumerated, current Display count: {2}", base.CurrentConfig.ConfigType, base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());

            Log.Message(true, "Checking Preconditions and Plugging in {0} supported panel", _colorType);
            if (!base.CurrentConfig.DisplayList.Contains(DisplayType.HDMI))
                Log.Abort("HDMI not passed in command line...Aborting the test");
            base.Hotplug(FunctionName.OPEN, DisplayType.HDMI, DVMU_PORT.PORTA);
            base.Hotplug(FunctionName.UNPLUG, DisplayType.HDMI, DVMU_PORT.PORTA);
            base.Hotplug(FunctionName.UNPLUG, DisplayType.HDMI_2, DVMU_PORT.PORTB);
            if (!(base.CurrentConfig.EnumeratedDisplays.Any(dI => dI.DisplayType == DisplayType.HDMI)))
            {
                Log.Message("HDMI is not enumerated..Plugging it through DVMU");
                Log.Message("Hotplug {0} supported HDMI panel & switch the display to it", _colorType);
                base.Hotplug(FunctionName.PLUG, DisplayType.HDMI, DVMU_PORT.PORTA, edidFile);
            }
            if (base.CurrentConfig.DisplayList.Contains(DisplayType.HDMI_2) && (!(base.CurrentConfig.EnumeratedDisplays.Any(dI => dI.DisplayType == DisplayType.HDMI_2))))
            {
                Log.Message("HDMI_2 is not enumerated..Plugging it through DVMU");
                Log.Message("Hotplug {0} supported HDMI panel & switch the display to it", _colorType);
                base.Hotplug(FunctionName.PLUG, DisplayType.HDMI_2, DVMU_PORT.PORTB, edidFile);
            }
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Set the configuration");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }

        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            base.ApplyResolution(DisplayType.HDMI, true);
            SetQuantizationRange(DisplayType.HDMI, RGB_QUANTIZATION_RANGE.DEFAULT);

            base.CurrentConfig.CustomDisplayList.ForEach(item =>
                {
                    if (item == DisplayType.HDMI)
                    {
                        PerformTest(item, ImageColors.Black, RGB_QUANTIZATION_RANGE.DEFAULT,true);

                        PerformTest(item, ImageColors.White, RGB_QUANTIZATION_RANGE.DEFAULT,true);

                        base.ApplyResolution(DisplayType.HDMI, false);

                        PerformTest(item, ImageColors.Black, RGB_QUANTIZATION_RANGE.DEFAULT,false);

                        PerformTest(item, ImageColors.White, RGB_QUANTIZATION_RANGE.DEFAULT,false);

                    }
                });
        }

        private void PerformTest(DisplayType item, ImageColors imageColor, RGB_QUANTIZATION_RANGE quantRange, bool IsCEAmode)
        {
            PrepareBackground(true, imageColor);
            if (VerifyColorValue(ImageColors.Black, quantRange, true))
            {
                Log.Success("Color values as per expected");
            }
            else
            {
                Log.Fail("Invalid color format");
            }

            RGB_QUANTIZATION_RANGE currentQuantRange = GetQuantizationRange(item);

            if (currentQuantRange == RGB_QUANTIZATION_RANGE.DEFAULT)
            {
                Log.Message("Super. As expected");
            }
            else
                Log.Fail("Issue");

        }
    }
}