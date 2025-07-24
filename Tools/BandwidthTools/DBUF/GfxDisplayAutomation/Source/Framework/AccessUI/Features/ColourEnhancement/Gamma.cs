namespace Intel.VPG.Display.Automation
{
    using System;

    public class Gamma :FunctionalBase,  ISet, IGet
    {
        SliderHandler SliderHandler = null;

        public Gamma()
        {
		SliderHandler = new SliderHandler(ColorEnhancementNew.Instance.IntelRGraphicsControlPanel.SliderName, Features.Gamma);

          //  ColorEnhancementNew.Instance.IntelRGraphicsControlPanel.SliderName
      //     SliderHandler = new SliderHandler(ColorEnhancementRepo.Instance.FormIntelR_Graphics_and_Medi.SliderGamma, Features.Gamma);
        }
        public object Get
        {
            get { return SliderHandler.GetSliderValue(); }
        }
        public object Set
        {
            set {   SliderHandler.SetSliderValue(double.Parse(value.ToString()));   }
        }
    }
}
