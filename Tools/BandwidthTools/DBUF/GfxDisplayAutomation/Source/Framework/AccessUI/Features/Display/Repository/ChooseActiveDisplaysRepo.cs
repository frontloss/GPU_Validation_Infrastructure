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
    using System.Linq;

    /// <summary>
    /// The class representing the ChooseActiveDisplaysRepo element repository.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    [RepositoryFolder("4482f5d6-e006-4584-8a7f-292cf1b46bc6")]
    public partial class ChooseActiveDisplaysRepo : RepoGenBaseFolder
    {
        static ChooseActiveDisplaysRepo instance = new ChooseActiveDisplaysRepo();
        ChooseActiveDisplaysRepoFolders.FormIntelR_Graphics_and_MediAppFolder _formintelr_graphics_and_medi;

        /// <summary>
        /// Gets the singleton class instance representing the ChooseActiveDisplaysRepo element repository.
        /// </summary>
        [RepositoryFolder("4482f5d6-e006-4584-8a7f-292cf1b46bc6")]
        public static ChooseActiveDisplaysRepo Instance
        {
            get { return instance; }
        }

        /// <summary>
        /// Repository class constructor.
        /// </summary>
        public ChooseActiveDisplaysRepo()
            : base("ChooseActiveDisplaysRepo", "", null, 30000, false, "4482f5d6-e006-4584-8a7f-292cf1b46bc6", ".\\RepositoryImages\\SelectActiveDisplays4482f5d6.rximgres")
        {
            _formintelr_graphics_and_medi = new ChooseActiveDisplaysRepoFolders.FormIntelR_Graphics_and_MediAppFolder(this);
        }

        #region Variables

        #endregion

        /// <summary>
        /// The FormIntelR_Graphics_and_Medi folder.
        /// </summary>
        [RepositoryFolder("d9494110-62f8-4a20-83ef-d0c82d9d1147")]
        public virtual ChooseActiveDisplaysRepoFolders.FormIntelR_Graphics_and_MediAppFolder FormIntelR_Graphics_and_Medi
        {
            get { return _formintelr_graphics_and_medi; }
        }
    }

    /// <summary>
    /// Inner folder classes.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    public partial class ChooseActiveDisplaysRepoFolders
    {
        /// <summary>
        /// The FormIntelR_Graphics_and_MediAppFolder folder.
        /// </summary>
        [RepositoryFolder("d9494110-62f8-4a20-83ef-d0c82d9d1147")]
        public partial class FormIntelR_Graphics_and_MediAppFolder : RepoGenBaseFolder
        {
            RepoItemInfo _selfInfo;
            RepoItemInfo _textprimary_displayInfo;
            RepoItemInfo _comboboxcomboboxprimaryInfo;
            RepoItemInfo _comboboxcomboboxsecondaryInfo;
            RepoItemInfo _comboboxcomboboxthirdInfo;
            RepoItemInfo _collageselectdisplayorientationInfo;
            RepoItemInfo _verticallist0Info;
            RepoItemInfo _horizontalscrollbarInfo;
            RepoItemInfo _verticalscrollbarInfo;
            RepoItemInfo _partcontenthostInfo;
            RepoItemInfo _textInfo;
            RepoItemInfo _verticallist1Info;
            RepoItemInfo _horizontalscrollbar1Info;
            RepoItemInfo _verticalscrollbar1Info;
            RepoItemInfo _partcontenthost1Info;
            RepoItemInfo _text1Info;
            RepoItemInfo _enablecollagecontrolInfo;
            RepoItemInfo _horizontallist0Info;
            RepoItemInfo _horizontalscrollbar2Info;
            RepoItemInfo _verticalscrollbar2Info;
            RepoItemInfo _partcontenthost2Info;
            RepoItemInfo _text2Info;
            RepoItemInfo _horizontallist1Info;
            RepoItemInfo _horizontalscrollbar3Info;
            RepoItemInfo _verticalscrollbar3Info;
            RepoItemInfo _partcontenthost3Info;
            RepoItemInfo _text3Info;
            RepoItemInfo _labelandhelpcontrolInfo;
            RepoItemInfo _imageInfo;
            RepoItemInfo _btntooltipInfo;
            RepoItemInfo _enablecollageInfo;

            /// <summary>
            /// Creates a new FormIntelR_Graphics_and_Medi  folder.
            /// </summary>
            public FormIntelR_Graphics_and_MediAppFolder(RepoGenBaseFolder parentFolder) :
                base("FormIntelR_Graphics_and_Medi", "/form[@automationid='MainWindow']", parentFolder, 30000, true, "d9494110-62f8-4a20-83ef-d0c82d9d1147", "")
            {
                _selfInfo = new RepoItemInfo(this, "Self", "", 30000, null, "d9494110-62f8-4a20-83ef-d0c82d9d1147");
                _textprimary_displayInfo = new RepoItemInfo(this, "TextPrimary_Display", "element/element[@classname='MultipleDisplays']/text[@automationid='lblPrimaryDisplay']", 30000, null, "16414173-f7e4-4ed1-bc2e-a9f80c844cc7");
                _comboboxcomboboxprimaryInfo = new RepoItemInfo(this, "ComboBoxComboBoxPrimary", "element/element[@classname='MultipleDisplays']/combobox[@automationid='comboBoxPrimary']", 30000, null, "aa026142-d639-4354-9d47-39103ebcb5cc");
                _comboboxcomboboxsecondaryInfo = new RepoItemInfo(this, "ComboBoxComboBoxSecondary", "element/element[@classname='MultipleDisplays']/combobox[@automationid='comboBoxSecondary']", 30000, null, "9ef2b381-76b0-4b2f-880d-3cb1b9726456");
                _comboboxcomboboxthirdInfo = new RepoItemInfo(this, "ComboBoxComboBoxThird", "element/element[@classname='MultipleDisplays']/combobox[@automationid='comboBoxThird']", 30000, null, "bcf8ad13-1f77-4c26-9bce-f46bd5fceb01");
                //_selfInfo = new RepoItemInfo(this, "Self", "", 0, null, "3704cbed-d0ae-40e8-829f-c34115409ac5");
                _collageselectdisplayorientationInfo = new RepoItemInfo(this, "CollageSelectDisplayOrientation", "element/element[@classname='MultipleDisplays']/element[@automationid='collageSelectDisplayOrientation']", 30000, null, "695c5bfe-17ab-4f42-9aed-c2fef7a4e81b");
                _verticallist0Info = new RepoItemInfo(this, "VerticalList0", "element/element[@classname='MultipleDisplays']/element[@automationid='collageSelectDisplayOrientation']/element[@automationid='VerticalList_0']", 30000, null, "9f6ec47f-e4cc-4db3-9e09-4c059720ac97");
                _horizontalscrollbarInfo = new RepoItemInfo(this, "HorizontalScrollBar", "element/element[@classname='MultipleDisplays']/element[@automationid='collageSelectDisplayOrientation']/element[@automationid='VerticalList_0']/text/container/scrollbar[@automationid='HorizontalScrollBar']", 30000, null, "2454a1db-3846-487d-9fff-03b46f254e8a");
                _verticalscrollbarInfo = new RepoItemInfo(this, "VerticalScrollBar", "element/element[@classname='MultipleDisplays']/element[@automationid='collageSelectDisplayOrientation']/element[@automationid='VerticalList_0']/text/container/scrollbar[@automationid='VerticalScrollBar']", 30000, null, "9ef36c3c-3788-4cf8-998b-b44e0f161202");
                _partcontenthostInfo = new RepoItemInfo(this, "PARTContentHost", "element/element[@classname='MultipleDisplays']/element[@automationid='collageSelectDisplayOrientation']/element[@automationid='VerticalList_0']/text/container[@automationid='PART_ContentHost']", 30000, null, "7c34909a-9a6c-4c6f-82e0-c8f414f0069e");
                _textInfo = new RepoItemInfo(this, "Text", "element/element[@classname='MultipleDisplays']/element[@automationid='collageSelectDisplayOrientation']/element[@automationid='VerticalList_0']/text[@automationid='text']", 30000, null, "cb150a78-07e0-46c3-960f-16fc9e603011");
                _verticallist1Info = new RepoItemInfo(this, "VerticalList1", "element/element[@classname='MultipleDisplays']/element[@automationid='collageSelectDisplayOrientation']/element[@automationid='VerticalList_1']", 30000, null, "7b012968-1709-4eb7-8701-24a4360fcfbe");
                _horizontalscrollbar1Info = new RepoItemInfo(this, "HorizontalScrollBar1", "element/element[@classname='MultipleDisplays']/element[@automationid='collageSelectDisplayOrientation']/element[@automationid='VerticalList_1']/text/container/scrollbar[@automationid='HorizontalScrollBar']", 30000, null, "93f34dba-eea0-4c93-9848-fc01a4767360");
                _verticalscrollbar1Info = new RepoItemInfo(this, "VerticalScrollBar1", "element/element[@classname='MultipleDisplays']/element[@automationid='collageSelectDisplayOrientation']/element[@automationid='VerticalList_1']/text/container/scrollbar[@automationid='VerticalScrollBar']", 30000, null, "a0c34cc4-1551-46ea-9c49-3533c58f2019");
                _partcontenthost1Info = new RepoItemInfo(this, "PARTContentHost1", "element/element[@classname='MultipleDisplays']/element[@automationid='collageSelectDisplayOrientation']/element[@automationid='VerticalList_1']/text/container[@automationid='PART_ContentHost']", 30000, null, "1e7f4176-d1fb-4962-ac82-1dcbe328a3eb");
                _text1Info = new RepoItemInfo(this, "Text1", "element/element[@classname='MultipleDisplays']/element[@automationid='collageSelectDisplayOrientation']/element[@automationid='VerticalList_1']/text[@automationid='text']", 30000, null, "70e25396-f70c-4e3c-9c4f-7a9ac53ef0a1");
                _enablecollagecontrolInfo = new RepoItemInfo(this, "EnableCollageControl", "element/element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']", 30000, null, "dad49f4f-232f-4d30-bbf5-c034880a6c93");
                _horizontallist0Info = new RepoItemInfo(this, "HorizontalList0", "element/element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='HorizontalList_0']", 30000, null, "a1252663-8c59-4e1c-acd9-ce9885a9d33c");
                _horizontalscrollbar2Info = new RepoItemInfo(this, "HorizontalScrollBar2", "element/element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='HorizontalList_0']/text/container/scrollbar[@automationid='HorizontalScrollBar']", 30000, null, "ebdfdcc9-5a9e-4d0f-9075-67d8698760b0");
                _verticalscrollbar2Info = new RepoItemInfo(this, "VerticalScrollBar2", "element/element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='HorizontalList_0']/text/container/scrollbar[@automationid='VerticalScrollBar']", 30000, null, "c6d98058-383e-4031-8cdc-24edfb012b89");
                _partcontenthost2Info = new RepoItemInfo(this, "PARTContentHost2", "element/element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='HorizontalList_0']/text/container[@automationid='PART_ContentHost']", 30000, null, "996f9e0d-ea9e-4e56-906a-6dfd6b8d6332");
                _text2Info = new RepoItemInfo(this, "Text2", "element/element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='HorizontalList_0']/text[@automationid='text']", 30000, null, "86de3d93-f998-4fd5-8e31-05ae0197c452");
                _horizontallist1Info = new RepoItemInfo(this, "HorizontalList1", "element/element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='HorizontalList_1']", 30000, null, "d73ee3b4-f0c8-4168-b3fa-435f58fc0756");
                _horizontalscrollbar3Info = new RepoItemInfo(this, "HorizontalScrollBar3", "element/element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='HorizontalList_1']/text/container/scrollbar[@automationid='HorizontalScrollBar']", 30000, null, "782372fa-e1d6-402e-9a83-e41ca747edd2");
                _verticalscrollbar3Info = new RepoItemInfo(this, "VerticalScrollBar3", "element/element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='HorizontalList_1']/text/container/scrollbar[@automationid='VerticalScrollBar']", 30000, null, "9189df60-78d2-4f4b-b4ec-d049a09d7c60");
                _partcontenthost3Info = new RepoItemInfo(this, "PARTContentHost3", "element/element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='HorizontalList_1']/text/container[@automationid='PART_ContentHost']", 30000, null, "4faaeb2c-ce4d-4a22-9455-59b00b7f00f6");
                _text3Info = new RepoItemInfo(this, "Text3", "element/element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='HorizontalList_1']/text[@automationid='text']", 30000, null, "38981121-103b-4eaf-9212-2fb5e4bdf2b2");
                _labelandhelpcontrolInfo = new RepoItemInfo(this, "LabelAndHelpControl", "element/element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='labelAndHelpControl']", 30000, null, "d9b6545b-f0e5-4c44-93e2-21efba615fa8");
                _imageInfo = new RepoItemInfo(this, "Image", "element/element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='labelAndHelpControl']/button/picture[@automationid='image']", 30000, null, "bf0a27c8-a087-4631-bacb-b7809f4c4039");
                _btntooltipInfo = new RepoItemInfo(this, "BtnTooltip", "element/element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='labelAndHelpControl']/button[@automationid='btnTooltip']", 30000, null, "5f8142e5-b072-4e1d-9027-c82b53a40514");
                _enablecollageInfo = new RepoItemInfo(this, "EnableCollage", "element/element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='labelAndHelpControl']/text[@automationid='text']", 30000, null, "6f962b28-0a39-4394-8eb8-ad65c2bf2c77");
            }

            /// <summary>
            /// The Self item.
            /// </summary>
            [RepositoryItem("d9494110-62f8-4a20-83ef-d0c82d9d1147")]
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
            [RepositoryItemInfo("d9494110-62f8-4a20-83ef-d0c82d9d1147")]
            public virtual RepoItemInfo SelfInfo
            {
                get
                {
                    return _selfInfo;
                }
            }

            /// <summary>
            /// The TextPrimary_Display item.
            /// </summary>
            [RepositoryItem("16414173-f7e4-4ed1-bc2e-a9f80c844cc7")]
            public virtual Ranorex.Text TextPrimary_Display
            {
                get
                {
                    return _textprimary_displayInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The TextPrimary_Display item info.
            /// </summary>
            [RepositoryItemInfo("16414173-f7e4-4ed1-bc2e-a9f80c844cc7")]
            public virtual RepoItemInfo TextPrimary_DisplayInfo
            {
                get
                {
                    return _textprimary_displayInfo;
                }
            }

            /// <summary>
            /// The ComboBoxComboBoxPrimary item.
            /// </summary>
            [RepositoryItem("aa026142-d639-4354-9d47-39103ebcb5cc")]
            public virtual Ranorex.ComboBox ComboBoxComboBoxPrimary
            {
                get
                {
                    return _comboboxcomboboxprimaryInfo.CreateAdapter<Ranorex.ComboBox>(true);
                }
            }

            /// <summary>
            /// The ComboBoxComboBoxPrimary item info.
            /// </summary>
            [RepositoryItemInfo("aa026142-d639-4354-9d47-39103ebcb5cc")]
            public virtual RepoItemInfo ComboBoxComboBoxPrimaryInfo
            {
                get
                {
                    return _comboboxcomboboxprimaryInfo;
                }
            }

            /// <summary>
            /// The ComboBoxComboBoxSecondary item.
            /// </summary>
            [RepositoryItem("9ef2b381-76b0-4b2f-880d-3cb1b9726456")]
            public virtual Ranorex.ComboBox ComboBoxComboBoxSecondary
            {
                get
                {
                    return _comboboxcomboboxsecondaryInfo.CreateAdapter<Ranorex.ComboBox>(true);
                }
            }

            /// <summary>
            /// The ComboBoxComboBoxSecondary item info.
            /// </summary>
            [RepositoryItemInfo("9ef2b381-76b0-4b2f-880d-3cb1b9726456")]
            public virtual RepoItemInfo ComboBoxComboBoxSecondaryInfo
            {
                get
                {
                    return _comboboxcomboboxsecondaryInfo;
                }
            }

            /// <summary>
            /// The ComboBoxComboBoxThird item.
            /// </summary>
            [RepositoryItem("bcf8ad13-1f77-4c26-9bce-f46bd5fceb01")]
            public virtual Ranorex.ComboBox ComboBoxComboBoxThird
            {
                get
                {
                    return _comboboxcomboboxthirdInfo.CreateAdapter<Ranorex.ComboBox>(true);
                }
            }

            /// <summary>
            /// The ComboBoxComboBoxThird item info.
            /// </summary>
            [RepositoryItemInfo("bcf8ad13-1f77-4c26-9bce-f46bd5fceb01")]
            public virtual RepoItemInfo ComboBoxComboBoxThirdInfo
            {
                get
                {
                    return _comboboxcomboboxthirdInfo;
                }
            }

            /// <summary>
            /// The CollageSelectDisplayOrientation item.
            /// </summary>
            [RepositoryItem("695c5bfe-17ab-4f42-9aed-c2fef7a4e81b")]
            public virtual Ranorex.Unknown CollageSelectDisplayOrientation
            {
                get
                {
                    return _collageselectdisplayorientationInfo.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The CollageSelectDisplayOrientation item info.
            /// </summary>
            [RepositoryItemInfo("695c5bfe-17ab-4f42-9aed-c2fef7a4e81b")]
            public virtual RepoItemInfo CollageSelectDisplayOrientationInfo
            {
                get
                {
                    return _collageselectdisplayorientationInfo;
                }
            }

            /// <summary>
            /// The VerticalList0 item.
            /// </summary>
            [RepositoryItem("9f6ec47f-e4cc-4db3-9e09-4c059720ac97")]
            public virtual Ranorex.Unknown VerticalList0
            {
                get
                {
                    return _verticallist0Info.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The VerticalList0 item info.
            /// </summary>
            [RepositoryItemInfo("9f6ec47f-e4cc-4db3-9e09-4c059720ac97")]
            public virtual RepoItemInfo VerticalList0Info
            {
                get
                {
                    return _verticallist0Info;
                }
            }

            /// <summary>
            /// The HorizontalScrollBar item.
            /// </summary>
            [RepositoryItem("2454a1db-3846-487d-9fff-03b46f254e8a")]
            public virtual Ranorex.ScrollBar HorizontalScrollBar
            {
                get
                {
                    return _horizontalscrollbarInfo.CreateAdapter<Ranorex.ScrollBar>(true);
                }
            }

            /// <summary>
            /// The HorizontalScrollBar item info.
            /// </summary>
            [RepositoryItemInfo("2454a1db-3846-487d-9fff-03b46f254e8a")]
            public virtual RepoItemInfo HorizontalScrollBarInfo
            {
                get
                {
                    return _horizontalscrollbarInfo;
                }
            }

            /// <summary>
            /// The VerticalScrollBar item.
            /// </summary>
            [RepositoryItem("9ef36c3c-3788-4cf8-998b-b44e0f161202")]
            public virtual Ranorex.ScrollBar VerticalScrollBar
            {
                get
                {
                    return _verticalscrollbarInfo.CreateAdapter<Ranorex.ScrollBar>(true);
                }
            }

            /// <summary>
            /// The VerticalScrollBar item info.
            /// </summary>
            [RepositoryItemInfo("9ef36c3c-3788-4cf8-998b-b44e0f161202")]
            public virtual RepoItemInfo VerticalScrollBarInfo
            {
                get
                {
                    return _verticalscrollbarInfo;
                }
            }

            /// <summary>
            /// The PARTContentHost item.
            /// </summary>
            [RepositoryItem("7c34909a-9a6c-4c6f-82e0-c8f414f0069e")]
            public virtual Ranorex.Container PARTContentHost
            {
                get
                {
                    return _partcontenthostInfo.CreateAdapter<Ranorex.Container>(true);
                }
            }

            /// <summary>
            /// The PARTContentHost item info.
            /// </summary>
            [RepositoryItemInfo("7c34909a-9a6c-4c6f-82e0-c8f414f0069e")]
            public virtual RepoItemInfo PARTContentHostInfo
            {
                get
                {
                    return _partcontenthostInfo;
                }
            }

            /// <summary>
            /// The Text item.
            /// </summary>
            [RepositoryItem("cb150a78-07e0-46c3-960f-16fc9e603011")]
            public virtual Ranorex.Text Text
            {
                get
                {
                    return _textInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The Text item info.
            /// </summary>
            [RepositoryItemInfo("cb150a78-07e0-46c3-960f-16fc9e603011")]
            public virtual RepoItemInfo TextInfo
            {
                get
                {
                    return _textInfo;
                }
            }

            /// <summary>
            /// The VerticalList1 item.
            /// </summary>
            [RepositoryItem("7b012968-1709-4eb7-8701-24a4360fcfbe")]
            public virtual Ranorex.Unknown VerticalList1
            {
                get
                {
                    return _verticallist1Info.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The VerticalList1 item info.
            /// </summary>
            [RepositoryItemInfo("7b012968-1709-4eb7-8701-24a4360fcfbe")]
            public virtual RepoItemInfo VerticalList1Info
            {
                get
                {
                    return _verticallist1Info;
                }
            }

            /// <summary>
            /// The HorizontalScrollBar1 item.
            /// </summary>
            [RepositoryItem("93f34dba-eea0-4c93-9848-fc01a4767360")]
            public virtual Ranorex.ScrollBar HorizontalScrollBar1
            {
                get
                {
                    return _horizontalscrollbar1Info.CreateAdapter<Ranorex.ScrollBar>(true);
                }
            }

            /// <summary>
            /// The HorizontalScrollBar1 item info.
            /// </summary>
            [RepositoryItemInfo("93f34dba-eea0-4c93-9848-fc01a4767360")]
            public virtual RepoItemInfo HorizontalScrollBar1Info
            {
                get
                {
                    return _horizontalscrollbar1Info;
                }
            }

            /// <summary>
            /// The VerticalScrollBar1 item.
            /// </summary>
            [RepositoryItem("a0c34cc4-1551-46ea-9c49-3533c58f2019")]
            public virtual Ranorex.ScrollBar VerticalScrollBar1
            {
                get
                {
                    return _verticalscrollbar1Info.CreateAdapter<Ranorex.ScrollBar>(true);
                }
            }

            /// <summary>
            /// The VerticalScrollBar1 item info.
            /// </summary>
            [RepositoryItemInfo("a0c34cc4-1551-46ea-9c49-3533c58f2019")]
            public virtual RepoItemInfo VerticalScrollBar1Info
            {
                get
                {
                    return _verticalscrollbar1Info;
                }
            }

            /// <summary>
            /// The PARTContentHost1 item.
            /// </summary>
            [RepositoryItem("1e7f4176-d1fb-4962-ac82-1dcbe328a3eb")]
            public virtual Ranorex.Container PARTContentHost1
            {
                get
                {
                    return _partcontenthost1Info.CreateAdapter<Ranorex.Container>(true);
                }
            }

            /// <summary>
            /// The PARTContentHost1 item info.
            /// </summary>
            [RepositoryItemInfo("1e7f4176-d1fb-4962-ac82-1dcbe328a3eb")]
            public virtual RepoItemInfo PARTContentHost1Info
            {
                get
                {
                    return _partcontenthost1Info;
                }
            }

            /// <summary>
            /// The Text1 item.
            /// </summary>
            [RepositoryItem("70e25396-f70c-4e3c-9c4f-7a9ac53ef0a1")]
            public virtual Ranorex.Text Text1
            {
                get
                {
                    return _text1Info.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The Text1 item info.
            /// </summary>
            [RepositoryItemInfo("70e25396-f70c-4e3c-9c4f-7a9ac53ef0a1")]
            public virtual RepoItemInfo Text1Info
            {
                get
                {
                    return _text1Info;
                }
            }

            /// <summary>
            /// The EnableCollageControl item.
            /// </summary>
            [RepositoryItem("dad49f4f-232f-4d30-bbf5-c034880a6c93")]
            public virtual Ranorex.Unknown EnableCollageControl
            {
                get
                {
                    return _enablecollagecontrolInfo.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The EnableCollageControl item info.
            /// </summary>
            [RepositoryItemInfo("dad49f4f-232f-4d30-bbf5-c034880a6c93")]
            public virtual RepoItemInfo EnableCollageControlInfo
            {
                get
                {
                    return _enablecollagecontrolInfo;
                }
            }

            /// <summary>
            /// The HorizontalList0 item.
            /// </summary>
            [RepositoryItem("a1252663-8c59-4e1c-acd9-ce9885a9d33c")]
            public virtual Ranorex.Unknown HorizontalList0
            {
                get
                {
                    try
                    {
                        return _horizontallist0Info.CreateAdapter<Ranorex.Unknown>(true);
                    }
                    catch
                    {
                        return ColorEnhacementReposHD.Instance.IntelRHDGraphicsControlPanel.DisplayMainPage.VerticalList0;
                    }
                }
            }

            /// <summary>
            /// The HorizontalList0 item info.
            /// </summary>
            [RepositoryItemInfo("a1252663-8c59-4e1c-acd9-ce9885a9d33c")]
            public virtual RepoItemInfo HorizontalList0Info
            {
                get
                {
                    return _horizontallist0Info;
                }
            }

            /// <summary>
            /// The HorizontalScrollBar2 item.
            /// </summary>
            [RepositoryItem("ebdfdcc9-5a9e-4d0f-9075-67d8698760b0")]
            public virtual Ranorex.ScrollBar HorizontalScrollBar2
            {
                get
                {
                    return _horizontalscrollbar2Info.CreateAdapter<Ranorex.ScrollBar>(true);
                }
            }

            /// <summary>
            /// The HorizontalScrollBar2 item info.
            /// </summary>
            [RepositoryItemInfo("ebdfdcc9-5a9e-4d0f-9075-67d8698760b0")]
            public virtual RepoItemInfo HorizontalScrollBar2Info
            {
                get
                {
                    return _horizontalscrollbar2Info;
                }
            }

            /// <summary>
            /// The VerticalScrollBar2 item.
            /// </summary>
            [RepositoryItem("c6d98058-383e-4031-8cdc-24edfb012b89")]
            public virtual Ranorex.ScrollBar VerticalScrollBar2
            {
                get
                {
                    return _verticalscrollbar2Info.CreateAdapter<Ranorex.ScrollBar>(true);
                }
            }

            /// <summary>
            /// The VerticalScrollBar2 item info.
            /// </summary>
            [RepositoryItemInfo("c6d98058-383e-4031-8cdc-24edfb012b89")]
            public virtual RepoItemInfo VerticalScrollBar2Info
            {
                get
                {
                    return _verticalscrollbar2Info;
                }
            }

            /// <summary>
            /// The PARTContentHost2 item.
            /// </summary>
            [RepositoryItem("996f9e0d-ea9e-4e56-906a-6dfd6b8d6332")]
            public virtual Ranorex.Container PARTContentHost2
            {
                get
                {
                    return _partcontenthost2Info.CreateAdapter<Ranorex.Container>(true);
                }
            }

            /// <summary>
            /// The PARTContentHost2 item info.
            /// </summary>
            [RepositoryItemInfo("996f9e0d-ea9e-4e56-906a-6dfd6b8d6332")]
            public virtual RepoItemInfo PARTContentHost2Info
            {
                get
                {
                    return _partcontenthost2Info;
                }
            }

            /// <summary>
            /// The Text2 item.
            /// </summary>
            [RepositoryItem("86de3d93-f998-4fd5-8e31-05ae0197c452")]
            public virtual Ranorex.Text Text2
            {
                get
                {
                    return _text2Info.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The Text2 item info.
            /// </summary>
            [RepositoryItemInfo("86de3d93-f998-4fd5-8e31-05ae0197c452")]
            public virtual RepoItemInfo Text2Info
            {
                get
                {
                    return _text2Info;
                }
            }

            /// <summary>
            /// The HorizontalList1 item.
            /// </summary>
            [RepositoryItem("d73ee3b4-f0c8-4168-b3fa-435f58fc0756")]
            public virtual Ranorex.Unknown HorizontalList1
            {
                get
                {
                    return _horizontallist1Info.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The HorizontalList1 item info.
            /// </summary>
            [RepositoryItemInfo("d73ee3b4-f0c8-4168-b3fa-435f58fc0756")]
            public virtual RepoItemInfo HorizontalList1Info
            {
                get
                {
                    return _horizontallist1Info;
                }
            }

            /// <summary>
            /// The HorizontalScrollBar3 item.
            /// </summary>
            [RepositoryItem("782372fa-e1d6-402e-9a83-e41ca747edd2")]
            public virtual Ranorex.ScrollBar HorizontalScrollBar3
            {
                get
                {
                    return _horizontalscrollbar3Info.CreateAdapter<Ranorex.ScrollBar>(true);
                }
            }

            /// <summary>
            /// The HorizontalScrollBar3 item info.
            /// </summary>
            [RepositoryItemInfo("782372fa-e1d6-402e-9a83-e41ca747edd2")]
            public virtual RepoItemInfo HorizontalScrollBar3Info
            {
                get
                {
                    return _horizontalscrollbar3Info;
                }
            }

            /// <summary>
            /// The VerticalScrollBar3 item.
            /// </summary>
            [RepositoryItem("9189df60-78d2-4f4b-b4ec-d049a09d7c60")]
            public virtual Ranorex.ScrollBar VerticalScrollBar3
            {
                get
                {
                    return _verticalscrollbar3Info.CreateAdapter<Ranorex.ScrollBar>(true);
                }
            }

            /// <summary>
            /// The VerticalScrollBar3 item info.
            /// </summary>
            [RepositoryItemInfo("9189df60-78d2-4f4b-b4ec-d049a09d7c60")]
            public virtual RepoItemInfo VerticalScrollBar3Info
            {
                get
                {
                    return _verticalscrollbar3Info;
                }
            }

            /// <summary>
            /// The PARTContentHost3 item.
            /// </summary>
            [RepositoryItem("4faaeb2c-ce4d-4a22-9455-59b00b7f00f6")]
            public virtual Ranorex.Container PARTContentHost3
            {
                get
                {
                    return _partcontenthost3Info.CreateAdapter<Ranorex.Container>(true);
                }
            }

            /// <summary>
            /// The PARTContentHost3 item info.
            /// </summary>
            [RepositoryItemInfo("4faaeb2c-ce4d-4a22-9455-59b00b7f00f6")]
            public virtual RepoItemInfo PARTContentHost3Info
            {
                get
                {
                    return _partcontenthost3Info;
                }
            }

            /// <summary>
            /// The Text3 item.
            /// </summary>
            [RepositoryItem("38981121-103b-4eaf-9212-2fb5e4bdf2b2")]
            public virtual Ranorex.Text Text3
            {
                get
                {
                    return _text3Info.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The Text3 item info.
            /// </summary>
            [RepositoryItemInfo("38981121-103b-4eaf-9212-2fb5e4bdf2b2")]
            public virtual RepoItemInfo Text3Info
            {
                get
                {
                    return _text3Info;
                }
            }

            /// <summary>
            /// The LabelAndHelpControl item.
            /// </summary>
            [RepositoryItem("d9b6545b-f0e5-4c44-93e2-21efba615fa8")]
            public virtual Ranorex.Unknown LabelAndHelpControl
            {
                get
                {
                    return _labelandhelpcontrolInfo.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The LabelAndHelpControl item info.
            /// </summary>
            [RepositoryItemInfo("d9b6545b-f0e5-4c44-93e2-21efba615fa8")]
            public virtual RepoItemInfo LabelAndHelpControlInfo
            {
                get
                {
                    return _labelandhelpcontrolInfo;
                }
            }

            /// <summary>
            /// The Image item.
            /// </summary>
            [RepositoryItem("bf0a27c8-a087-4631-bacb-b7809f4c4039")]
            public virtual Ranorex.Picture Image
            {
                get
                {
                    return _imageInfo.CreateAdapter<Ranorex.Picture>(true);
                }
            }

            /// <summary>
            /// The Image item info.
            /// </summary>
            [RepositoryItemInfo("bf0a27c8-a087-4631-bacb-b7809f4c4039")]
            public virtual RepoItemInfo ImageInfo
            {
                get
                {
                    return _imageInfo;
                }
            }

            /// <summary>
            /// The BtnTooltip item.
            /// </summary>
            [RepositoryItem("5f8142e5-b072-4e1d-9027-c82b53a40514")]
            public virtual Ranorex.Button BtnTooltip
            {
                get
                {
                    return _btntooltipInfo.CreateAdapter<Ranorex.Button>(true);
                }
            }

            /// <summary>
            /// The BtnTooltip item info.
            /// </summary>
            [RepositoryItemInfo("5f8142e5-b072-4e1d-9027-c82b53a40514")]
            public virtual RepoItemInfo BtnTooltipInfo
            {
                get
                {
                    return _btntooltipInfo;
                }
            }

            /// <summary>
            /// The EnableCollage item.
            /// </summary>
            [RepositoryItem("6f962b28-0a39-4394-8eb8-ad65c2bf2c77")]
            public virtual Ranorex.Text EnableCollage
            {
                get
                {
                    return _enablecollageInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The EnableCollage item info.
            /// </summary>
            [RepositoryItemInfo("6f962b28-0a39-4394-8eb8-ad65c2bf2c77")]
            public virtual RepoItemInfo EnableCollageInfo
            {
                get
                {
                    return _enablecollageInfo;
                }
            }

        }

    }
}