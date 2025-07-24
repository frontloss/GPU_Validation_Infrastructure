namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Configuration;
    using Ranorex.Core;
    using Ranorex;
    using System.Collections.Generic;
    using System.Linq;
    using System.Xml.Linq;
    using System.IO;
    public class SliderHandler
    {
        Ranorex.Slider _Slider = null;        
        public SliderHandler(Ranorex.Slider Slider, Features Feature)
        {
            _Slider = Slider;
        }
        public void SetSliderValue(double Value)
        {
            _Slider.Value = Value;
        }
        public double GetSliderValue()
        {
            return Math.Round(_Slider.Value, 2);
        }
    }
}
