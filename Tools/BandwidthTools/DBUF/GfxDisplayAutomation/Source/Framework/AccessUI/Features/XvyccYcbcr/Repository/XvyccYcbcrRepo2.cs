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
    /// The class representing the HotkeyPanelRepo element repository.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    [RepositoryFolder("a7853685-effa-49ea-bc94-cb5304f2e6e4")]
    public partial class XvyccYcbcrRepo2 : RepoGenBaseFolder
    {
        static XvyccYcbcrRepo2 instance = new XvyccYcbcrRepo2();
        HotkeyPanelRepoFolder.IntelRGraphicsAppFolder _intelrgraphics;

        /// <summary>
        /// Gets the singleton class instance representing the HotkeyPanelRepo element repository.
        /// </summary>
        [RepositoryFolder("a7853685-effa-49ea-bc94-cb5304f2e6e4")]
        public static XvyccYcbcrRepo2 Instance
        {
            get { return instance; }
        }

        /// <summary>
        /// Repository class constructor.
        /// </summary>
        public XvyccYcbcrRepo2() 
            : base("HotkeyPanelRepo", "", null, 30000, false, "a7853685-effa-49ea-bc94-cb5304f2e6e4", ".\\RepositoryImages\\XvyccYcbcrRepo2a7853685.rximgres")
        {
            _intelrgraphics = new HotkeyPanelRepoFolder.IntelRGraphicsAppFolder(this);
        }

#region Variables

#endregion

        /// <summary>
        /// The IntelRGraphics folder.
        /// </summary>
        [RepositoryFolder("d81135fd-1bd3-40ea-9aa5-628cc485e8a7")]
        public virtual HotkeyPanelRepoFolder.IntelRGraphicsAppFolder IntelRGraphics
        {
            get { return _intelrgraphics; }
        }
    }

    /// <summary>
    /// Inner folder classes.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    public partial class HotkeyPanelRepoFolder
    {
        /// <summary>
        /// The IntelRGraphicsAppFolder folder.
        /// </summary>
        [RepositoryFolder("d81135fd-1bd3-40ea-9aa5-628cc485e8a7")]
        public partial class IntelRGraphicsAppFolder : RepoGenBaseFolder
        {
            HotkeyPanelRepoFolder.DisplayMainPageFolder _displaymainpage;
            RepoItemInfo _selfInfo;

            /// <summary>
            /// Creates a new IntelRGraphics  folder.
            /// </summary>
            public IntelRGraphicsAppFolder(RepoGenBaseFolder parentFolder) :
                    base("IntelRGraphics", "/form[@automationid='MainWindow']", parentFolder, 30000, true, "d81135fd-1bd3-40ea-9aa5-628cc485e8a7", "")
            {
                _displaymainpage = new HotkeyPanelRepoFolder.DisplayMainPageFolder(this);
                _selfInfo = new RepoItemInfo(this, "Self", "", 0, null, "d81135fd-1bd3-40ea-9aa5-628cc485e8a7");
            }

            /// <summary>
            /// The Self item.
            /// </summary>
            [RepositoryItem("d81135fd-1bd3-40ea-9aa5-628cc485e8a7")]
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
            [RepositoryItemInfo("d81135fd-1bd3-40ea-9aa5-628cc485e8a7")]
            public virtual RepoItemInfo SelfInfo
            {
                get
                {
                    return _selfInfo;
                }
            }

            /// <summary>
            /// The DisplayMainPage folder.
            /// </summary>
            [RepositoryFolder("149da1b3-3ecf-4017-952e-8ad350581a3d")]
            public virtual HotkeyPanelRepoFolder.DisplayMainPageFolder DisplayMainPage
            {
                get { return _displaymainpage; }
            }
        }

        /// <summary>
        /// The DisplayMainPageFolder folder.
        /// </summary>
        [RepositoryFolder("149da1b3-3ecf-4017-952e-8ad350581a3d")]
        public partial class DisplayMainPageFolder : RepoGenBaseFolder
        {
            RepoItemInfo _selfInfo;
            RepoItemInfo _xvycccontrolInfo;
            RepoItemInfo _horizontallist0Info;
            RepoItemInfo _horizontalscrollbarInfo;
            RepoItemInfo _verticalscrollbarInfo;
            RepoItemInfo _partcontenthostInfo;
            RepoItemInfo _textInfo;
            RepoItemInfo _horizontallist1Info;
            RepoItemInfo _horizontalscrollbar1Info;
            RepoItemInfo _verticalscrollbar1Info;
            RepoItemInfo _partcontenthost1Info;
            RepoItemInfo _text1Info;
            RepoItemInfo _labelandhelpcontrolInfo;
            RepoItemInfo _imageInfo;
            RepoItemInfo _btntooltipInfo;
            RepoItemInfo _xvyccInfo;

            /// <summary>
            /// Creates a new DisplayMainPage  folder.
            /// </summary>
            public DisplayMainPageFolder(RepoGenBaseFolder parentFolder) :
                    base("DisplayMainPage", "element", parentFolder, 30000, true, "149da1b3-3ecf-4017-952e-8ad350581a3d", "")
            {
                _selfInfo = new RepoItemInfo(this, "Self", "", 0, null, "149da1b3-3ecf-4017-952e-8ad350581a3d");
                _xvycccontrolInfo = new RepoItemInfo(this, "XvyccControl", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='xvyccControl']", 30000, null, "fc135963-198a-4628-baf4-9fdd6cdf7ff7");
                _horizontallist0Info = new RepoItemInfo(this, "HorizontalList0", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='xvyccControl']/element[@automationid='HorizontalList_0']", 30000, null, "7ab5f56a-4d67-4aae-b748-2583eaaea980");
                _horizontalscrollbarInfo = new RepoItemInfo(this, "HorizontalScrollBar", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='xvyccControl']/element[@automationid='HorizontalList_0']/text/container/scrollbar[@automationid='HorizontalScrollBar']", 30000, null, "930cbd14-6a0c-4723-8e41-465dd398578a");
                _verticalscrollbarInfo = new RepoItemInfo(this, "VerticalScrollBar", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='xvyccControl']/element[@automationid='HorizontalList_0']/text/container/scrollbar[@automationid='VerticalScrollBar']", 30000, null, "f5786cda-b4ba-469b-b27e-6ae667046942");
                _partcontenthostInfo = new RepoItemInfo(this, "PARTContentHost", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='xvyccControl']/element[@automationid='HorizontalList_0']/text/container[@automationid='PART_ContentHost']", 30000, null, "63588218-e44b-4dc8-8892-adc51a6a6332");
                _textInfo = new RepoItemInfo(this, "Text", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='xvyccControl']/element[@automationid='HorizontalList_0']/text[@automationid='text']", 30000, null, "3cc190b0-02b4-4518-8d56-cca4581dc2fe");
                _horizontallist1Info = new RepoItemInfo(this, "HorizontalList1", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='xvyccControl']/element[@automationid='HorizontalList_1']", 30000, null, "55e6b9fa-7246-4c90-bc3a-519ce3311e00");
                _horizontalscrollbar1Info = new RepoItemInfo(this, "HorizontalScrollBar1", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='xvyccControl']/element[@automationid='HorizontalList_1']/text/container/scrollbar[@automationid='HorizontalScrollBar']", 30000, null, "a9815c7a-7f6a-4960-88c2-09a35eebeb61");
                _verticalscrollbar1Info = new RepoItemInfo(this, "VerticalScrollBar1", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='xvyccControl']/element[@automationid='HorizontalList_1']/text/container/scrollbar[@automationid='VerticalScrollBar']", 30000, null, "7debc68b-69d9-448b-b20b-ef6595bf3341");
                _partcontenthost1Info = new RepoItemInfo(this, "PARTContentHost1", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='xvyccControl']/element[@automationid='HorizontalList_1']/text/container[@automationid='PART_ContentHost']", 30000, null, "9a0e92bb-10e3-4c71-ac05-2c04bc315577");
                _text1Info = new RepoItemInfo(this, "Text1", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='xvyccControl']/element[@automationid='HorizontalList_1']/text[@automationid='text']", 30000, null, "39222f28-2a0d-4484-84b1-491141b5bf21");
                _labelandhelpcontrolInfo = new RepoItemInfo(this, "LabelAndHelpControl", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='xvyccControl']/element[@automationid='labelAndHelpControl']", 30000, null, "9d3de99a-09c7-424d-8cd2-f97448feb37c");
                _imageInfo = new RepoItemInfo(this, "Image", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='xvyccControl']/element[@automationid='labelAndHelpControl']/button/picture[@automationid='image']", 30000, null, "84ebf0fc-e5aa-4667-8708-5e49564f9483");
                _btntooltipInfo = new RepoItemInfo(this, "BtnTooltip", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='xvyccControl']/element[@automationid='labelAndHelpControl']/button[@automationid='btnTooltip']", 30000, null, "22e94bbe-1d31-4bb0-83aa-5e0d2d92f69b");
                _xvyccInfo = new RepoItemInfo(this, "XvYCC", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='xvyccControl']/element[@automationid='labelAndHelpControl']/text[@automationid='text']", 30000, null, "3eae653c-3f91-4a7b-9875-0766b2c14188");
            }

            /// <summary>
            /// The Self item.
            /// </summary>
            [RepositoryItem("149da1b3-3ecf-4017-952e-8ad350581a3d")]
            public virtual Ranorex.Unknown Self
            {
                get
                {
                    return _selfInfo.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The Self item info.
            /// </summary>
            [RepositoryItemInfo("149da1b3-3ecf-4017-952e-8ad350581a3d")]
            public virtual RepoItemInfo SelfInfo
            {
                get
                {
                    return _selfInfo;
                }
            }

            /// <summary>
            /// The XvyccControl item.
            /// </summary>
            [RepositoryItem("fc135963-198a-4628-baf4-9fdd6cdf7ff7")]
            public virtual Ranorex.Unknown XvyccControl
            {
                get
                {
                    return _xvycccontrolInfo.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The XvyccControl item info.
            /// </summary>
            [RepositoryItemInfo("fc135963-198a-4628-baf4-9fdd6cdf7ff7")]
            public virtual RepoItemInfo XvyccControlInfo
            {
                get
                {
                    return _xvycccontrolInfo;
                }
            }

            /// <summary>
            /// The HorizontalList0 item.
            /// </summary>
            [RepositoryItem("7ab5f56a-4d67-4aae-b748-2583eaaea980")]
            public virtual Ranorex.Unknown HorizontalList0
            {
                get
                {
                    return _horizontallist0Info.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The HorizontalList0 item info.
            /// </summary>
            [RepositoryItemInfo("7ab5f56a-4d67-4aae-b748-2583eaaea980")]
            public virtual RepoItemInfo HorizontalList0Info
            {
                get
                {
                    return _horizontallist0Info;
                }
            }

            /// <summary>
            /// The HorizontalScrollBar item.
            /// </summary>
            [RepositoryItem("930cbd14-6a0c-4723-8e41-465dd398578a")]
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
            [RepositoryItemInfo("930cbd14-6a0c-4723-8e41-465dd398578a")]
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
            [RepositoryItem("f5786cda-b4ba-469b-b27e-6ae667046942")]
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
            [RepositoryItemInfo("f5786cda-b4ba-469b-b27e-6ae667046942")]
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
            [RepositoryItem("63588218-e44b-4dc8-8892-adc51a6a6332")]
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
            [RepositoryItemInfo("63588218-e44b-4dc8-8892-adc51a6a6332")]
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
            [RepositoryItem("3cc190b0-02b4-4518-8d56-cca4581dc2fe")]
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
            [RepositoryItemInfo("3cc190b0-02b4-4518-8d56-cca4581dc2fe")]
            public virtual RepoItemInfo TextInfo
            {
                get
                {
                    return _textInfo;
                }
            }

            /// <summary>
            /// The HorizontalList1 item.
            /// </summary>
            [RepositoryItem("55e6b9fa-7246-4c90-bc3a-519ce3311e00")]
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
            [RepositoryItemInfo("55e6b9fa-7246-4c90-bc3a-519ce3311e00")]
            public virtual RepoItemInfo HorizontalList1Info
            {
                get
                {
                    return _horizontallist1Info;
                }
            }

            /// <summary>
            /// The HorizontalScrollBar1 item.
            /// </summary>
            [RepositoryItem("a9815c7a-7f6a-4960-88c2-09a35eebeb61")]
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
            [RepositoryItemInfo("a9815c7a-7f6a-4960-88c2-09a35eebeb61")]
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
            [RepositoryItem("7debc68b-69d9-448b-b20b-ef6595bf3341")]
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
            [RepositoryItemInfo("7debc68b-69d9-448b-b20b-ef6595bf3341")]
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
            [RepositoryItem("9a0e92bb-10e3-4c71-ac05-2c04bc315577")]
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
            [RepositoryItemInfo("9a0e92bb-10e3-4c71-ac05-2c04bc315577")]
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
            [RepositoryItem("39222f28-2a0d-4484-84b1-491141b5bf21")]
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
            [RepositoryItemInfo("39222f28-2a0d-4484-84b1-491141b5bf21")]
            public virtual RepoItemInfo Text1Info
            {
                get
                {
                    return _text1Info;
                }
            }

            /// <summary>
            /// The LabelAndHelpControl item.
            /// </summary>
            [RepositoryItem("9d3de99a-09c7-424d-8cd2-f97448feb37c")]
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
            [RepositoryItemInfo("9d3de99a-09c7-424d-8cd2-f97448feb37c")]
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
            [RepositoryItem("84ebf0fc-e5aa-4667-8708-5e49564f9483")]
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
            [RepositoryItemInfo("84ebf0fc-e5aa-4667-8708-5e49564f9483")]
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
            [RepositoryItem("22e94bbe-1d31-4bb0-83aa-5e0d2d92f69b")]
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
            [RepositoryItemInfo("22e94bbe-1d31-4bb0-83aa-5e0d2d92f69b")]
            public virtual RepoItemInfo BtnTooltipInfo
            {
                get
                {
                    return _btntooltipInfo;
                }
            }

            /// <summary>
            /// The XvYCC item.
            /// </summary>
            [RepositoryItem("3eae653c-3f91-4a7b-9875-0766b2c14188")]
            public virtual Ranorex.Text XvYCC
            {
                get
                {
                    return _xvyccInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The XvYCC item info.
            /// </summary>
            [RepositoryItemInfo("3eae653c-3f91-4a7b-9875-0766b2c14188")]
            public virtual RepoItemInfo XvYCCInfo
            {
                get
                {
                    return _xvyccInfo;
                }
            }
        }

    }
}