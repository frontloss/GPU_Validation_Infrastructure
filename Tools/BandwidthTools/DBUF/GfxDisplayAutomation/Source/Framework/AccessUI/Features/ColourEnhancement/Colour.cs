namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;

    public class Colour :FunctionalBase, ISet, IGet
    {
        private List<Ranorex.Picture> _colorsList = null;

        public Colour()
        {
             AntiAliasingRepo.Instance.IntelRGraphicsControlPanel.DisplayMainPage.ColorSettings1.FocusEnter();
    //        DisplayTabsRepo.Instance.IntelRHDGraphicsControlPanel.Color.FocusEnter();
            if (null == this._colorsList)
            {
                this._colorsList = new List<Ranorex.Picture>();
                this._colorsList.Add(ColorEnhancementRepo.Instance.FormIntelR_Graphics_and_Medi.PictureImgAllColors);
                this._colorsList.Add(ColorEnhancementRepo.Instance.FormIntelR_Graphics_and_Medi.PictureImgRed);
                this._colorsList.Add(ColorEnhancementRepo.Instance.FormIntelR_Graphics_and_Medi.PictureImgGreen);
                this._colorsList.Add(ColorEnhancementRepo.Instance.FormIntelR_Graphics_and_Medi.PictureImgBlue);
            }
        }
     
        public object Get
        {
            get { return Enum.Parse(typeof(ColorOptions), ColorEnhancementRepo.Instance.FormIntelR_Graphics_and_Medi.TextColor.TextValue.Replace("Colors", string.Empty).Trim()); }
        }
        public object Set
        {
            set
            {
                this._colorsList[(int)Enum.Parse(typeof(ColorOptions), value.ToString())].Click();
            }
        }
    }
}
