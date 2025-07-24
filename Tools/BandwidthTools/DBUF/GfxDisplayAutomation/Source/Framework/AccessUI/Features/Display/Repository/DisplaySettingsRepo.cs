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
    /// The class representing the DisplaySettingsRepo element repository.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    [RepositoryFolder("6fa66863-212a-4add-949c-bd2f145cd845")]
    public partial class DisplaySettingsRepo : RepoGenBaseFolder
    {
        static DisplaySettingsRepo instance = new DisplaySettingsRepo();
        DisplaySettingsRepoFolders.FormIntelR_Graphics_and_MediAppFolder _formintelr_graphics_and_medi;

        /// <summary>
        /// Gets the singleton class instance representing the DisplaySettingsRepo element repository.
        /// </summary>
        [RepositoryFolder("6fa66863-212a-4add-949c-bd2f145cd845")]
        public static DisplaySettingsRepo Instance
        {
            get { return instance; }
        }

        /// <summary>
        /// Repository class constructor.
        /// </summary>
        public DisplaySettingsRepo()
            : base("DisplaySettingsRepo", "", null, 30000, false, "6fa66863-212a-4add-949c-bd2f145cd845", ".\\RepositoryImages\\DisplaySettingsRepo6fa66863.rximgres")
        {
            _formintelr_graphics_and_medi = new DisplaySettingsRepoFolders.FormIntelR_Graphics_and_MediAppFolder(this);
        }

        #region Variables

        #endregion

        /// <summary>
        /// The FormIntelR_Graphics_and_Medi folder.
        /// </summary>
        [RepositoryFolder("fd086c63-1ce8-4f6e-815b-d6665747de01")]
        public virtual DisplaySettingsRepoFolders.FormIntelR_Graphics_and_MediAppFolder FormIntelR_Graphics_and_Medi
        {
            get { return _formintelr_graphics_and_medi; }
        }
    }

    /// <summary>
    /// Inner folder classes.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    public partial class DisplaySettingsRepoFolders
    {
        /// <summary>
        /// The FormIntelR_Graphics_and_MediAppFolder folder.
        /// </summary>
        [RepositoryFolder("fd086c63-1ce8-4f6e-815b-d6665747de01")]
        public partial class FormIntelR_Graphics_and_MediAppFolder : RepoGenBaseFolder
        {
            RepoItemInfo _selfInfo;
            RepoItemInfo _comboboxcomboresolutionInfo;
            RepoItemInfo _comboboxcomborefreshrateInfo;
            RepoItemInfo _rotation0textInfo;
            RepoItemInfo _rotation0Info;
            RepoItemInfo _rotation90textInfo;
            RepoItemInfo _rotation90Info;
            RepoItemInfo _rotation180textInfo;
            RepoItemInfo _rotation180Info;
            RepoItemInfo _rotation270textInfo;
            RepoItemInfo _rotation270Info;
            RepoItemInfo _textcenter_image_scalingInfo;
            RepoItemInfo _tickcenterimagescalingInfo;
            RepoItemInfo _textscalefullscreen_scalingInfo;
            RepoItemInfo _tickscalefullscreenscalingInfo;
            RepoItemInfo _textmaintain_aspect_ratio_scalingInfo;
            RepoItemInfo _tickmaintain_aspect_ratioscalingInfo;
            RepoItemInfo _textmaintain_display_scalingInfo;
            RepoItemInfo _tickmaintaindisplayscalingInfo;
            RepoItemInfo _textcustomize_aspect_ratioInfo;
            RepoItemInfo _tickcustomaspectratioInfo;
            RepoItemInfo _scalingcontrolInfo;
            RepoItemInfo _rotationcontrolInfo;
            RepoItemInfo _slidervtsliderInfo;
            RepoItemInfo _sliderhzsliderInfo;
            RepoItemInfo _comboboxcomboboxchoosedisplayInfo;
			RepoItemInfo _colorDepthcontrolInfo;
			
            /// <summary>
            /// Creates a new FormIntelR_Graphics_and_Medi  folder.
            /// </summary>
            public FormIntelR_Graphics_and_MediAppFolder(RepoGenBaseFolder parentFolder) :
                base("FormIntelR_Graphics_and_Medi", "/form[@automationid='MainWindow']", parentFolder, 30000, true, "fd086c63-1ce8-4f6e-815b-d6665747de01", "")
            {
                _selfInfo = new RepoItemInfo(this, "Self", "", 30000, null, "fd086c63-1ce8-4f6e-815b-d6665747de01");
                _comboboxcomboresolutionInfo = new RepoItemInfo(this, "ComboBoxComboResolution", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/element[@automationid='resolutionControl']/combobox", 30000, null, "b9e35c37-b998-470d-b745-21c3606877d6");
                _comboboxcomborefreshrateInfo = new RepoItemInfo(this, "ComboBoxComboRefreshRate", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/element[@automationid='refreshRateControl']/combobox", 30000, null, "6415e02f-621a-49e5-b744-e0b201d3ee62");
                _rotation0textInfo = new RepoItemInfo(this, "Rotation0Text", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/element[@automationid='rotationControl']/element[@automationid='HorizontalList_0']/text[@automationid='text']", 30000, null, "66e19011-0176-409d-8d06-9ef9de86e01f");
                _rotation0Info = new RepoItemInfo(this, "Rotation0", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/element[@automationid='rotationControl']/element[@automationid='HorizontalList_0']", 30000, null, "a3dc7bb5-7756-4a3c-8a7f-dc21a4cb0d0b");
                _rotation90textInfo = new RepoItemInfo(this, "Rotation90Text", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/element[@automationid='rotationControl']/element[@automationid='HorizontalList_1']/text[@automationid='text']", 30000, null, "80a8d487-6df1-46b4-9f47-34f736a73778");
                _rotation90Info = new RepoItemInfo(this, "Rotation90", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/element[@automationid='rotationControl']/element[@automationid='HorizontalList_1']", 30000, null, "fabab179-0b0a-4552-911e-97bd388626ef");
                _rotation180textInfo = new RepoItemInfo(this, "Rotation180Text", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/element[@automationid='rotationControl']/element[@automationid='HorizontalList_2']/text[@automationid='text']", 30000, null, "2d0276f7-dc8c-42e4-a3cf-922b3c98c4bc");
                _rotation180Info = new RepoItemInfo(this, "Rotation180", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/element[@automationid='rotationControl']/element[@automationid='HorizontalList_2']", 30000, null, "edf49e94-8652-4a59-b4de-08b033cb015d");
                _rotation270textInfo = new RepoItemInfo(this, "Rotation270Text", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/element[@automationid='rotationControl']/element[@automationid='HorizontalList_3']/text[@automationid='text']", 30000, null, "992ff5e4-89f4-482e-a50b-4c13d1efdea8");
                _rotation270Info = new RepoItemInfo(this, "Rotation270", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/element[@automationid='rotationControl']/element[@automationid='HorizontalList_3']", 30000, null, "e814945a-029a-4fa6-9e60-d6a53e673e16");
                _textcenter_image_scalingInfo = new RepoItemInfo(this, "TextCenter_Image_Scaling", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/element[@automationid='scalingControl']/element[@automationid='VerticalList_0']/text[@automationid='text']", 30000, null, "c98930e5-42de-430c-9865-32afcc4b6690");
                _tickcenterimagescalingInfo = new RepoItemInfo(this, "TickCenterImageScaling", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/element[@automationid='scalingControl']/element[@automationid='VerticalList_0']", 30000, null, "385fbb93-73ef-4cdf-833a-0c775d283a8b");
                _textscalefullscreen_scalingInfo = new RepoItemInfo(this, "TextScaleFullScreen_Scaling", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/element[@automationid='scalingControl']/element[@automationid='VerticalList_1']/text[@automationid='text']", 30000, null, "49fd63a5-2df8-40bb-9c7a-d6b9e3a19185");
                _tickscalefullscreenscalingInfo = new RepoItemInfo(this, "TickScaleFullScreenScaling", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/element[@automationid='scalingControl']/element[@automationid='VerticalList_1']", 30000, null, "6f97c400-89ea-430d-9e28-30a26a22c015");
                _textmaintain_aspect_ratio_scalingInfo = new RepoItemInfo(this, "TextMaintain_Aspect_Ratio_Scaling", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/element[@automationid='scalingControl']/element[@automationid='VerticalList_2']/text[@automationid='text']", 30000, null, "747cf7e8-5f0c-46e8-a231-f8666fa836e2");
                _tickmaintain_aspect_ratioscalingInfo = new RepoItemInfo(this, "TickMaintain_Aspect_RatioScaling", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/element[@automationid='scalingControl']/element[@automationid='VerticalList_2']", 30000, null, "712f6d63-131e-4194-b748-d1fb04187f2d");
                _textmaintain_display_scalingInfo = new RepoItemInfo(this, "TextMaintain_Display_Scaling", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/element[@automationid='scalingControl']/element[@automationid='VerticalList_3']/text[@automationid='text']", 30000, null, "036713b3-a41a-496a-b788-9428cc7ad6a8");
                _tickmaintaindisplayscalingInfo = new RepoItemInfo(this, "TickMaintainDisplayScaling", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/element[@automationid='scalingControl']/element[@automationid='VerticalList_3']", 30000, null, "edb98c74-ae11-46a2-afa6-b25a17370633");
                _textcustomize_aspect_ratioInfo = new RepoItemInfo(this, "TextCustomize_Aspect_Ratio", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/element[@automationid='scalingControl']/element[@automationid='VerticalList_4']/text[@automationid='text']", 30000, null, "05ac2d7b-5ff6-4a2d-81cf-d325cc2743e5");
                _tickcustomaspectratioInfo = new RepoItemInfo(this, "TickCustomAspectRatio", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/element[@automationid='scalingControl']/element[@automationid='VerticalList_4']", 30000, null, "f3247477-5a7e-4588-85f0-6801dc8c17bf");
                _scalingcontrolInfo = new RepoItemInfo(this, "ScalingControl", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/element[@automationid='scalingControl']", 30000, null, "da9c1b35-f4ce-42bf-be43-26eef1a9d684");
                _rotationcontrolInfo = new RepoItemInfo(this, "RotationControl", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/element[@automationid='rotationControl']", 30000, null, "da9c1b35-f4ce-42bf-be43-26eef1a9d684");
                _slidervtsliderInfo = new RepoItemInfo(this, "SliderVtSlider", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/slider[@automationid='vtSlider']", 30000, null, "32f3c5ef-fefe-4a74-871b-0150daf80b78");
                _sliderhzsliderInfo = new RepoItemInfo(this, "SliderHzSlider", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayGeneralSettingsControl']/slider[@automationid='hzSlider']", 30000, null, "92acbb6a-dbec-4309-bdd5-013fccccae6c");
                _comboboxcomboboxchoosedisplayInfo = new RepoItemInfo(this, "ComboBoxComboBoxChooseDisplay", "element/element[@classname='DisplaySettingsWindow']/combobox[@automationid='comboBoxChooseDisplay']", 30000, null, "676ada0a-c3bb-4a90-9a3f-040b7483a2a2");
				_colorDepthcontrolInfo = new RepoItemInfo(this, "ColorDepthControl", "element/element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='colorDepthControl']", 30000, null, "da9c1b35-f4ce-42bf-be43-26eef1a9d684");
            }

            /// <summary>
            /// The Self item.
            /// </summary>
            [RepositoryItem("fd086c63-1ce8-4f6e-815b-d6665747de01")]
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
            [RepositoryItemInfo("fd086c63-1ce8-4f6e-815b-d6665747de01")]
            public virtual RepoItemInfo SelfInfo
            {
                get
                {
                    return _selfInfo;
                }
            }

            /// <summary>
            /// The ComboBoxComboResolution item.
            /// </summary>
            [RepositoryItem("b9e35c37-b998-470d-b745-21c3606877d6")]
            public virtual Ranorex.ComboBox ComboBoxComboResolution
            {
                get
                {
                    return _comboboxcomboresolutionInfo.CreateAdapter<Ranorex.ComboBox>(true);
                }
            }

            /// <summary>
            /// The ComboBoxComboResolution item info.
            /// </summary>
            [RepositoryItemInfo("b9e35c37-b998-470d-b745-21c3606877d6")]
            public virtual RepoItemInfo ComboBoxComboResolutionInfo
            {
                get
                {
                    return _comboboxcomboresolutionInfo;
                }
            }

            /// <summary>
            /// The ComboBoxComboRefreshRate item.
            /// </summary>
            [RepositoryItem("6415e02f-621a-49e5-b744-e0b201d3ee62")]
            public virtual Ranorex.ComboBox ComboBoxComboRefreshRate
            {
                get
                {
                    return _comboboxcomborefreshrateInfo.CreateAdapter<Ranorex.ComboBox>(true);
                }
            }

            /// <summary>
            /// The ComboBoxComboRefreshRate item info.
            /// </summary>
            [RepositoryItemInfo("6415e02f-621a-49e5-b744-e0b201d3ee62")]
            public virtual RepoItemInfo ComboBoxComboRefreshRateInfo
            {
                get
                {
                    return _comboboxcomborefreshrateInfo;
                }
            }

            /// <summary>
            /// The Rotation0Text item.
            /// </summary>
            [RepositoryItem("66e19011-0176-409d-8d06-9ef9de86e01f")]
            public virtual Ranorex.Text Rotation0Text
            {
                get
                {
                    return _rotation0textInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The Rotation0Text item info.
            /// </summary>
            [RepositoryItemInfo("66e19011-0176-409d-8d06-9ef9de86e01f")]
            public virtual RepoItemInfo Rotation0TextInfo
            {
                get
                {
                    return _rotation0textInfo;
                }
            }

            /// <summary>
            /// The Rotation0 item.
            /// </summary>
            [RepositoryItem("a3dc7bb5-7756-4a3c-8a7f-dc21a4cb0d0b")]
            public virtual Ranorex.Unknown Rotation0
            {
                get
                {
                    return _rotation0Info.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The Rotation0 item info.
            /// </summary>
            [RepositoryItemInfo("a3dc7bb5-7756-4a3c-8a7f-dc21a4cb0d0b")]
            public virtual RepoItemInfo Rotation0Info
            {
                get
                {
                    return _rotation0Info;
                }
            }

            /// <summary>
            /// The Rotation90Text item.
            /// </summary>
            [RepositoryItem("80a8d487-6df1-46b4-9f47-34f736a73778")]
            public virtual Ranorex.Text Rotation90Text
            {
                get
                {
                    return _rotation90textInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The Rotation90Text item info.
            /// </summary>
            [RepositoryItemInfo("80a8d487-6df1-46b4-9f47-34f736a73778")]
            public virtual RepoItemInfo Rotation90TextInfo
            {
                get
                {
                    return _rotation90textInfo;
                }
            }

            /// <summary>
            /// The Rotation90 item.
            /// </summary>
            [RepositoryItem("fabab179-0b0a-4552-911e-97bd388626ef")]
            public virtual Ranorex.Unknown Rotation90
            {
                get
                {
                    return _rotation90Info.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The Rotation90 item info.
            /// </summary>
            [RepositoryItemInfo("fabab179-0b0a-4552-911e-97bd388626ef")]
            public virtual RepoItemInfo Rotation90Info
            {
                get
                {
                    return _rotation90Info;
                }
            }

            /// <summary>
            /// The Rotation180Text item.
            /// </summary>
            [RepositoryItem("2d0276f7-dc8c-42e4-a3cf-922b3c98c4bc")]
            public virtual Ranorex.Text Rotation180Text
            {
                get
                {
                    return _rotation180textInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The Rotation180Text item info.
            /// </summary>
            [RepositoryItemInfo("2d0276f7-dc8c-42e4-a3cf-922b3c98c4bc")]
            public virtual RepoItemInfo Rotation180TextInfo
            {
                get
                {
                    return _rotation180textInfo;
                }
            }

            /// <summary>
            /// The Rotation180 item.
            /// </summary>
            [RepositoryItem("edf49e94-8652-4a59-b4de-08b033cb015d")]
            public virtual Ranorex.Unknown Rotation180
            {
                get
                {
                    return _rotation180Info.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The Rotation180 item info.
            /// </summary>
            [RepositoryItemInfo("edf49e94-8652-4a59-b4de-08b033cb015d")]
            public virtual RepoItemInfo Rotation180Info
            {
                get
                {
                    return _rotation180Info;
                }
            }

            /// <summary>
            /// The Rotation270Text item.
            /// </summary>
            [RepositoryItem("992ff5e4-89f4-482e-a50b-4c13d1efdea8")]
            public virtual Ranorex.Text Rotation270Text
            {
                get
                {
                    return _rotation270textInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The Rotation270Text item info.
            /// </summary>
            [RepositoryItemInfo("992ff5e4-89f4-482e-a50b-4c13d1efdea8")]
            public virtual RepoItemInfo Rotation270TextInfo
            {
                get
                {
                    return _rotation270textInfo;
                }
            }

            /// <summary>
            /// The Rotation270 item.
            /// </summary>
            [RepositoryItem("e814945a-029a-4fa6-9e60-d6a53e673e16")]
            public virtual Ranorex.Unknown Rotation270
            {
                get
                {
                    return _rotation270Info.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The Rotation270 item info.
            /// </summary>
            [RepositoryItemInfo("e814945a-029a-4fa6-9e60-d6a53e673e16")]
            public virtual RepoItemInfo Rotation270Info
            {
                get
                {
                    return _rotation270Info;
                }
            }

            /// <summary>
            /// The TextCenter_Image_Scaling item.
            /// </summary>
            [RepositoryItem("c98930e5-42de-430c-9865-32afcc4b6690")]
            public virtual Ranorex.Text TextCenter_Image_Scaling
            {
                get
                {
                    return _textcenter_image_scalingInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The TextCenter_Image_Scaling item info.
            /// </summary>
            [RepositoryItemInfo("c98930e5-42de-430c-9865-32afcc4b6690")]
            public virtual RepoItemInfo TextCenter_Image_ScalingInfo
            {
                get
                {
                    return _textcenter_image_scalingInfo;
                }
            }

            /// <summary>
            /// The TickCenterImageScaling item.
            /// </summary>
            [RepositoryItem("385fbb93-73ef-4cdf-833a-0c775d283a8b")]
            public virtual Ranorex.Unknown TickCenterImageScaling
            {
                get
                {
                    return _tickcenterimagescalingInfo.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The TickCenterImageScaling item info.
            /// </summary>
            [RepositoryItemInfo("385fbb93-73ef-4cdf-833a-0c775d283a8b")]
            public virtual RepoItemInfo TickCenterImageScalingInfo
            {
                get
                {
                    return _tickcenterimagescalingInfo;
                }
            }

            /// <summary>
            /// The TextScaleFullScreen_Scaling item.
            /// </summary>
            [RepositoryItem("49fd63a5-2df8-40bb-9c7a-d6b9e3a19185")]
            public virtual Ranorex.Text TextScaleFullScreen_Scaling
            {
                get
                {
                    return _textscalefullscreen_scalingInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The TextScaleFullScreen_Scaling item info.
            /// </summary>
            [RepositoryItemInfo("49fd63a5-2df8-40bb-9c7a-d6b9e3a19185")]
            public virtual RepoItemInfo TextScaleFullScreen_ScalingInfo
            {
                get
                {
                    return _textscalefullscreen_scalingInfo;
                }
            }

            /// <summary>
            /// The TickScaleFullScreenScaling item.
            /// </summary>
            [RepositoryItem("6f97c400-89ea-430d-9e28-30a26a22c015")]
            public virtual Ranorex.Unknown TickScaleFullScreenScaling
            {
                get
                {
                    return _tickscalefullscreenscalingInfo.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The TickScaleFullScreenScaling item info.
            /// </summary>
            [RepositoryItemInfo("6f97c400-89ea-430d-9e28-30a26a22c015")]
            public virtual RepoItemInfo TickScaleFullScreenScalingInfo
            {
                get
                {
                    return _tickscalefullscreenscalingInfo;
                }
            }

            /// <summary>
            /// The TextMaintain_Aspect_Ratio_Scaling item.
            /// </summary>
            [RepositoryItem("747cf7e8-5f0c-46e8-a231-f8666fa836e2")]
            public virtual Ranorex.Text TextMaintain_Aspect_Ratio_Scaling
            {
                get
                {
                    return _textmaintain_aspect_ratio_scalingInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The TextMaintain_Aspect_Ratio_Scaling item info.
            /// </summary>
            [RepositoryItemInfo("747cf7e8-5f0c-46e8-a231-f8666fa836e2")]
            public virtual RepoItemInfo TextMaintain_Aspect_Ratio_ScalingInfo
            {
                get
                {
                    return _textmaintain_aspect_ratio_scalingInfo;
                }
            }

            /// <summary>
            /// The TickMaintain_Aspect_RatioScaling item.
            /// </summary>
            [RepositoryItem("712f6d63-131e-4194-b748-d1fb04187f2d")]
            public virtual Ranorex.Unknown TickMaintain_Aspect_RatioScaling
            {
                get
                {
                    return _tickmaintain_aspect_ratioscalingInfo.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The TickMaintain_Aspect_RatioScaling item info.
            /// </summary>
            [RepositoryItemInfo("712f6d63-131e-4194-b748-d1fb04187f2d")]
            public virtual RepoItemInfo TickMaintain_Aspect_RatioScalingInfo
            {
                get
                {
                    return _tickmaintain_aspect_ratioscalingInfo;
                }
            }

            /// <summary>
            /// The TextMaintain_Display_Scaling item.
            /// </summary>
            [RepositoryItem("036713b3-a41a-496a-b788-9428cc7ad6a8")]
            public virtual Ranorex.Text TextMaintain_Display_Scaling
            {
                get
                {
                    return _textmaintain_display_scalingInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The TextMaintain_Display_Scaling item info.
            /// </summary>
            [RepositoryItemInfo("036713b3-a41a-496a-b788-9428cc7ad6a8")]
            public virtual RepoItemInfo TextMaintain_Display_ScalingInfo
            {
                get
                {
                    return _textmaintain_display_scalingInfo;
                }
            }

            /// <summary>
            /// The TickMaintainDisplayScaling item.
            /// </summary>
            [RepositoryItem("edb98c74-ae11-46a2-afa6-b25a17370633")]
            public virtual Ranorex.Unknown TickMaintainDisplayScaling
            {
                get
                {
                    return _tickmaintaindisplayscalingInfo.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The TickMaintainDisplayScaling item info.
            /// </summary>
            [RepositoryItemInfo("edb98c74-ae11-46a2-afa6-b25a17370633")]
            public virtual RepoItemInfo TickMaintainDisplayScalingInfo
            {
                get
                {
                    return _tickmaintaindisplayscalingInfo;
                }
            }

            /// <summary>
            /// The TextCustomize_Aspect_Ratio item.
            /// </summary>
            [RepositoryItem("05ac2d7b-5ff6-4a2d-81cf-d325cc2743e5")]
            public virtual Ranorex.Text TextCustomize_Aspect_Ratio
            {
                get
                {
                    return _textcustomize_aspect_ratioInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The TextCustomize_Aspect_Ratio item info.
            /// </summary>
            [RepositoryItemInfo("05ac2d7b-5ff6-4a2d-81cf-d325cc2743e5")]
            public virtual RepoItemInfo TextCustomize_Aspect_RatioInfo
            {
                get
                {
                    return _textcustomize_aspect_ratioInfo;
                }
            }

            /// <summary>
            /// The TickCustomAspectRatio item.
            /// </summary>
            [RepositoryItem("f3247477-5a7e-4588-85f0-6801dc8c17bf")]
            public virtual Ranorex.Unknown TickCustomAspectRatio
            {
                get
                {
                    return _tickcustomaspectratioInfo.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The TickCustomAspectRatio item info.
            /// </summary>
            [RepositoryItemInfo("f3247477-5a7e-4588-85f0-6801dc8c17bf")]
            public virtual RepoItemInfo TickCustomAspectRatioInfo
            {
                get
                {
                    return _tickcustomaspectratioInfo;
                }
            }

            /// <summary>
            /// The ScalingControl item.
            /// </summary>
            [RepositoryItem("da9c1b35-f4ce-42bf-be43-26eef1a9d684")]
            public virtual Ranorex.Unknown ScalingControl
            {
                get
                {
                    return _scalingcontrolInfo.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The RotationControl item.
            /// </summary>
            [RepositoryItem("da9c1b35-f4ce-42bf-be43-26eef1a9d684")]
            public virtual Ranorex.Unknown RotationControl
            {
                get
                {
                    return _rotationcontrolInfo.CreateAdapter<Ranorex.Unknown>(true);
                }
            }
            /// <summary>
            /// The ScalingControl item info.
            /// </summary>
            [RepositoryItemInfo("da9c1b35-f4ce-42bf-be43-26eef1a9d684")]
            public virtual RepoItemInfo ScalingControlInfo
            {
                get
                {
                    return _scalingcontrolInfo;
                }
            }

            /// <summary>
            /// The SliderVtSlider item.
            /// </summary>
            [RepositoryItem("32f3c5ef-fefe-4a74-871b-0150daf80b78")]
            public virtual Ranorex.Slider SliderVtSlider
            {
                get
                {
                    return _slidervtsliderInfo.CreateAdapter<Ranorex.Slider>(true);
                }
            }

            /// <summary>
            /// The SliderVtSlider item info.
            /// </summary>
            [RepositoryItemInfo("32f3c5ef-fefe-4a74-871b-0150daf80b78")]
            public virtual RepoItemInfo SliderVtSliderInfo
            {
                get
                {
                    return _slidervtsliderInfo;
                }
            }

            /// <summary>
            /// The SliderHzSlider item.
            /// </summary>
            [RepositoryItem("92acbb6a-dbec-4309-bdd5-013fccccae6c")]
            public virtual Ranorex.Slider SliderHzSlider
            {
                get
                {
                    return _sliderhzsliderInfo.CreateAdapter<Ranorex.Slider>(true);
                }
            }

            /// <summary>
            /// The SliderHzSlider item info.
            /// </summary>
            [RepositoryItemInfo("92acbb6a-dbec-4309-bdd5-013fccccae6c")]
            public virtual RepoItemInfo SliderHzSliderInfo
            {
                get
                {
                    return _sliderhzsliderInfo;
                }
            }
            /// <summary>
            /// The ComboBoxComboBoxChooseDisplay item.
            /// </summary>
            [RepositoryItem("676ada0a-c3bb-4a90-9a3f-040b7483a2a2")]
            public virtual Ranorex.ComboBox ComboBoxComboBoxChooseDisplay
            {
                get
                {
                    return _comboboxcomboboxchoosedisplayInfo.CreateAdapter<Ranorex.ComboBox>(true);
                }
            }
			
			 /// <summary>
            /// The ColorDepthControl item.
            /// </summary>
            [RepositoryItem("da9c1b35-f4ce-42bf-be43-26eef1a9d684")]
            public virtual Ranorex.Unknown ColorDepthControl
            {
                get
                {
                    return _colorDepthcontrolInfo.CreateAdapter<Ranorex.Unknown>(true);
                }
            }
        }

    }
}