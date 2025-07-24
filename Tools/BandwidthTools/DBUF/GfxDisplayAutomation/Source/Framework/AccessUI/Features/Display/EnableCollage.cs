namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;

    using Ranorex;

    class EnableCollage : FunctionalBase, IGet, ISet
    {
        private ComboBox _collageComboBox = null;
        private List<Ranorex.Unknown> _horizontalVertical = null;
        public EnableCollage()
        {
            Config configObject = new Config();
            configObject.SetConfigType(DisplayUnifiedConfig.Collage);
        }
        public object Get
        {
            get
            {
                this._collageComboBox = ColorEnhacementReposHD.Instance.IntelRHDGraphicsControlPanel.DisplayMainPage.ComboBoxSelectCollageStatus;
                int collageValue =0;
                if (null != this._collageComboBox && _collageComboBox.Visible)
                    collageValue =(int)CollageOptions.Enable - ColorEnhacementReposHD.Instance.IntelRHDGraphicsControlPanel.DisplayMainPage.ComboBoxSelectCollageStatus.SelectedItemIndex;
                else
                {
                    this._horizontalVertical = ChooseActiveDisplaysRepo.Instance.FormIntelR_Graphics_and_Medi.EnableCollageControl.FindChildren<Ranorex.Unknown>().ToList();
                    for (int idx = 0; idx < this._horizontalVertical.Count; idx++)
                    {
                        if (null != this._horizontalVertical[idx].Element.GetAttributeValue("ItemStatus"))
                            collageValue= (_horizontalVertical.Count - idx);
                    }
                }
                return (CollageOptions)(collageValue);
            }
        }
        public object Set
        {
            set
            {
                CollageOptions collageOption = (CollageOptions)value ;
                this._collageComboBox = ColorEnhacementReposHD.Instance.IntelRHDGraphicsControlPanel.DisplayMainPage.ComboBoxSelectCollageStatus;
                if (null != this._collageComboBox && _collageComboBox.Visible)
                    ColorEnhacementReposHD.Instance.IntelRHDGraphicsControlPanel.DisplayMainPage.ComboBoxSelectCollageStatus.SelectedItemIndex = (int)collageOption % (int)CollageOptions.Enable;
                else
                {
                    this._horizontalVertical = ChooseActiveDisplaysRepo.Instance.FormIntelR_Graphics_and_Medi.EnableCollageControl.FindChildren<Ranorex.Unknown>().ToList();
                    this._horizontalVertical[_horizontalVertical.Count - (int)collageOption].FocusEnter();
               //     ChooseActiveDisplaysRepo.Instance.FormIntelR_Graphics_and_Medi.EnableCollageControl.Children[val].FocusEnter();
                }
            }
        }
    }
}