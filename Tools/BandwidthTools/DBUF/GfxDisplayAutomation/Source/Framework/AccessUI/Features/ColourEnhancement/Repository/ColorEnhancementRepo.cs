namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Text;
    using System.Drawing;
    using Ranorex;
    using Ranorex.Core;
    using Ranorex.Core.Repository;
    using Ranorex.Core.Testing;
    /// <summary>
    /// The class representing the ColorEnhancementRepo element repository.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    [RepositoryFolder("973cdc88-6e76-47a6-bd22-fa2bbfbb2713")]
    public partial class ColorEnhancementRepo : RepoGenBaseFolder
    {
        static ColorEnhancementRepo instance = new ColorEnhancementRepo();
        ColorEnhancementRepoFolders.FormIntelR_Graphics_and_MediAppFolder _formintelr_graphics_and_medi;

        /// <summary>
        /// Gets the singleton class instance representing the ColorEnhancementRepo element repository.
        /// </summary>
        [RepositoryFolder("973cdc88-6e76-47a6-bd22-fa2bbfbb2713")]
        public static ColorEnhancementRepo Instance
        {
            get { return instance; }
        }

        /// <summary>
        /// Repository class constructor.
        /// </summary>
        public ColorEnhancementRepo()
            : base("ColorEnhancementRepo", "", null, 30000, false, "973cdc88-6e76-47a6-bd22-fa2bbfbb2713", ".\\RepositoryImages\\ColorEnhancementRepo973cdc88.rximgres")
        {
            _formintelr_graphics_and_medi = new ColorEnhancementRepoFolders.FormIntelR_Graphics_and_MediAppFolder(this);
        }

        #region Variables

        #endregion

        /// <summary>
        /// The FormIntelR_Graphics_and_Medi folder.
        /// </summary>
        [RepositoryFolder("b0fa5a54-72da-4c29-9b70-3547fd97a701")]
        public virtual ColorEnhancementRepoFolders.FormIntelR_Graphics_and_MediAppFolder FormIntelR_Graphics_and_Medi
        {
            get { return _formintelr_graphics_and_medi; }
        }
    }

    /// <summary>
    /// Inner folder classes.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    public partial class ColorEnhancementRepoFolders
    {
        /// <summary>
        /// The FormIntelR_Graphics_and_MediAppFolder folder.
        /// </summary>
        [RepositoryFolder("b0fa5a54-72da-4c29-9b70-3547fd97a701")]
        public partial class FormIntelR_Graphics_and_MediAppFolder : RepoGenBaseFolder
        {
            RepoItemInfo _selfInfo;
            RepoItemInfo _pictureimgallcolorsInfo;
            RepoItemInfo _pictureimgredInfo;
            RepoItemInfo _pictureimggreenInfo;
            RepoItemInfo _pictureimgblueInfo;
            RepoItemInfo _textcolorInfo;
            RepoItemInfo _sliderbrightnessInfo;
            RepoItemInfo _slidercontrastInfo;
            RepoItemInfo _slidergammaInfo;

            /// <summary>
            /// Creates a new FormIntelR_Graphics_and_Medi  folder.
            /// </summary>
            public FormIntelR_Graphics_and_MediAppFolder(RepoGenBaseFolder parentFolder) :
                base("FormIntelR_Graphics_and_Medi", "/form[@automationid='MainWindow']", parentFolder, 30000, true, "b0fa5a54-72da-4c29-9b70-3547fd97a701", "")
            {
                _selfInfo = new RepoItemInfo(this, "Self", "", 30000, null, "b0fa5a54-72da-4c29-9b70-3547fd97a701");
                _pictureimgallcolorsInfo = new RepoItemInfo(this, "PictureImgAllColors", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/picture[@automationid='imgAllColors']", 30000, null, "646005ff-61c6-4ff6-a88a-e66cfee53a26");
                _pictureimgredInfo = new RepoItemInfo(this, "PictureImgRed", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/picture[@automationid='imgRed']", 30000, null, "f2b0ef49-31e3-4d10-a627-e6955e792232");
                _pictureimggreenInfo = new RepoItemInfo(this, "PictureImgGreen", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/picture[@automationid='imgGreen']", 30000, null, "de642314-4b12-4af6-ac0c-5f114fb39a5e");
                _pictureimgblueInfo = new RepoItemInfo(this, "PictureImgBlue", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/picture[@automationid='imgBlue']", 30000, null, "3c41dacb-6e8d-4e40-821b-2224dc3f5c16");
                _textcolorInfo = new RepoItemInfo(this, "TextColor", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/container[@automationid='BasicColorFeatutes']/text[@automationid='lblRGB']", 30000, null, "d9abf09f-ccb3-4491-980b-a03d305a5e67");
                _sliderbrightnessInfo = new RepoItemInfo(this, "SliderBrightness", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/container[@automationid='BasicColorFeatutes']/element[@automationid='sliderBrightness']/slider[@automationid='sliderName']", 30000, null, "503ca3ac-aae1-4586-be0e-5758cfa1a3d0");
                _slidercontrastInfo = new RepoItemInfo(this, "SliderContrast", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/container[@automationid='BasicColorFeatutes']/element[@automationid='sliderContrast']/slider[@automationid='sliderName']", 30000, null, "98ce0b2d-279d-4ce5-b2b1-3f95819cef34");
                _slidergammaInfo = new RepoItemInfo(this, "SliderGamma", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/container[@automationid='BasicColorFeatutes']/element[@automationid='sliderGamma']/slider[@automationid='sliderName']", 5000, null, "a494cecf-524a-4e28-9728-d3149d1d3582");
            }

            /// <summary>
            /// The Self item.
            /// </summary>
            [RepositoryItem("b0fa5a54-72da-4c29-9b70-3547fd97a701")]
            public virtual Ranorex.Form Self
            {
                get
                {
                    return _selfInfo.CreateAdapter<Ranorex.Form>(true);
                }
            }

            /// <summary>
            /// The Self item info.
            /// </summary>
            [RepositoryItemInfo("b0fa5a54-72da-4c29-9b70-3547fd97a701")]
            public virtual RepoItemInfo SelfInfo
            {
                get
                {
                    return _selfInfo;
                }
            }

            /// <summary>
            /// The PictureImgAllColors item.
            /// </summary>
            [RepositoryItem("646005ff-61c6-4ff6-a88a-e66cfee53a26")]
            public virtual Ranorex.Picture PictureImgAllColors
            {
                get
                {
                    return _pictureimgallcolorsInfo.CreateAdapter<Ranorex.Picture>(true);
                }
            }

            /// <summary>
            /// The PictureImgAllColors item info.
            /// </summary>
            [RepositoryItemInfo("646005ff-61c6-4ff6-a88a-e66cfee53a26")]
            public virtual RepoItemInfo PictureImgAllColorsInfo
            {
                get
                {
                    return _pictureimgallcolorsInfo;
                }
            }

            /// <summary>
            /// The PictureImgRed item.
            /// </summary>
            [RepositoryItem("f2b0ef49-31e3-4d10-a627-e6955e792232")]
            public virtual Ranorex.Picture PictureImgRed
            {
                get
                {
                    return _pictureimgredInfo.CreateAdapter<Ranorex.Picture>(true);
                }
            }

            /// <summary>
            /// The PictureImgRed item info.
            /// </summary>
            [RepositoryItemInfo("f2b0ef49-31e3-4d10-a627-e6955e792232")]
            public virtual RepoItemInfo PictureImgRedInfo
            {
                get
                {
                    return _pictureimgredInfo;
                }
            }

            /// <summary>
            /// The PictureImgGreen item.
            /// </summary>
            [RepositoryItem("de642314-4b12-4af6-ac0c-5f114fb39a5e")]
            public virtual Ranorex.Picture PictureImgGreen
            {
                get
                {
                    return _pictureimggreenInfo.CreateAdapter<Ranorex.Picture>(true);
                }
            }

            /// <summary>
            /// The PictureImgGreen item info.
            /// </summary>
            [RepositoryItemInfo("de642314-4b12-4af6-ac0c-5f114fb39a5e")]
            public virtual RepoItemInfo PictureImgGreenInfo
            {
                get
                {
                    return _pictureimggreenInfo;
                }
            }

            /// <summary>
            /// The PictureImgBlue item.
            /// </summary>
            [RepositoryItem("3c41dacb-6e8d-4e40-821b-2224dc3f5c16")]
            public virtual Ranorex.Picture PictureImgBlue
            {
                get
                {
                    return _pictureimgblueInfo.CreateAdapter<Ranorex.Picture>(true);
                }
            }

            /// <summary>
            /// The PictureImgBlue item info.
            /// </summary>
            [RepositoryItemInfo("3c41dacb-6e8d-4e40-821b-2224dc3f5c16")]
            public virtual RepoItemInfo PictureImgBlueInfo
            {
                get
                {
                    return _pictureimgblueInfo;
                }
            }

            /// <summary>
            /// The TextColor item.
            /// </summary>
            [RepositoryItem("d9abf09f-ccb3-4491-980b-a03d305a5e67")]
            public virtual Ranorex.Text TextColor
            {
                get
                {
                    return _textcolorInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The TextColor item info.
            /// </summary>
            [RepositoryItemInfo("d9abf09f-ccb3-4491-980b-a03d305a5e67")]
            public virtual RepoItemInfo TextColorInfo
            {
                get
                {
                    return _textcolorInfo;
                }
            }

            /// <summary>
            /// The SliderBrightness item.
            /// </summary>
            [RepositoryItem("503ca3ac-aae1-4586-be0e-5758cfa1a3d0")]
            public virtual Ranorex.Slider SliderBrightness
            {
                get
                {
                    return _sliderbrightnessInfo.CreateAdapter<Ranorex.Slider>(true);
                }
            }

            /// <summary>
            /// The SliderBrightness item info.
            /// </summary>
            [RepositoryItemInfo("503ca3ac-aae1-4586-be0e-5758cfa1a3d0")]
            public virtual RepoItemInfo SliderBrightnessInfo
            {
                get
                {
                    return _sliderbrightnessInfo;
                }
            }

            /// <summary>
            /// The SliderContrast item.
            /// </summary>
            [RepositoryItem("98ce0b2d-279d-4ce5-b2b1-3f95819cef34")]
            public virtual Ranorex.Slider SliderContrast
            {
                get
                {
                    return _slidercontrastInfo.CreateAdapter<Ranorex.Slider>(true);
                }
            }

            /// <summary>
            /// The SliderContrast item info.
            /// </summary>
            [RepositoryItemInfo("98ce0b2d-279d-4ce5-b2b1-3f95819cef34")]
            public virtual RepoItemInfo SliderContrastInfo
            {
                get
                {
                    return _slidercontrastInfo;
                }
            }

            /// <summary>
            /// The SliderGamma item.
            /// </summary>
            [RepositoryItem("a494cecf-524a-4e28-9728-d3149d1d3582")]
            public virtual Ranorex.Slider SliderGamma
            {
                get
                {
                    //try
                    //{
                        return _slidergammaInfo.CreateAdapter<Ranorex.Slider>(true);
                    //}
                    //catch
                    //{
                    //    return ColorEnhancementNew.Instance.IntelRGraphicsControlPanel.SliderName;
                    //}

                }
            }

            /// <summary>
            /// The SliderGamma item info.
            /// </summary>
            [RepositoryItemInfo("a494cecf-524a-4e28-9728-d3149d1d3582")]
            public virtual RepoItemInfo SliderGammaInfo
            {
                get
                {
                    return _slidergammaInfo;
                }
            }
        }

    }
}