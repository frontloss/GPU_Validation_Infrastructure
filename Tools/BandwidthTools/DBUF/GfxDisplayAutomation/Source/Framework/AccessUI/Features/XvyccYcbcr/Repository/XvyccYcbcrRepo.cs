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
    [RepositoryFolder("3ebedb54-37d8-402c-a160-caeeb73f7283")]
    public partial class XvyccYcbcrRepo : RepoGenBaseFolder
    {
        static XvyccYcbcrRepo instance = new XvyccYcbcrRepo();
        HotkeyPanelRepoFolders.IntelRHDGraphicsControlPanelAppFolder _intelrhdgraphicscontrolpanel;

        /// <summary>
        /// Gets the singleton class instance representing the HotkeyPanelRepo element repository.
        /// </summary>
        [RepositoryFolder("3ebedb54-37d8-402c-a160-caeeb73f7283")]
        public static XvyccYcbcrRepo Instance
        {
            get { return instance; }
        }

        /// <summary>
        /// Repository class constructor.
        /// </summary>
        public XvyccYcbcrRepo() 
            : base("HotkeyPanelRepo", "", null, 30000, false, "3ebedb54-37d8-402c-a160-caeeb73f7283", ".\\RepositoryImages\\NewRepository3ebedb54.rximgres")
        {
            _intelrhdgraphicscontrolpanel = new HotkeyPanelRepoFolders.IntelRHDGraphicsControlPanelAppFolder(this);
        }

#region Variables

#endregion

        /// <summary>
        /// The IntelRHDGraphicsControlPanel folder.
        /// </summary>
        [RepositoryFolder("fd6a1488-ed3d-486c-b9d4-6c5195e0890c")]
        public virtual HotkeyPanelRepoFolders.IntelRHDGraphicsControlPanelAppFolder IntelRHDGraphicsControlPanel
        {
            get { return _intelrhdgraphicscontrolpanel; }
        }
    }

    /// <summary>
    /// Inner folder classes.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    public partial class HotkeyPanelRepoFolders
    {
        /// <summary>
        /// The IntelRHDGraphicsControlPanelAppFolder folder.
        /// </summary>
        [RepositoryFolder("fd6a1488-ed3d-486c-b9d4-6c5195e0890c")]
        public partial class IntelRHDGraphicsControlPanelAppFolder : RepoGenBaseFolder
        {
            HotkeyPanelRepoFolders.DisplayMainPageFolder _displaymainpage;
            RepoItemInfo _selfInfo;

            /// <summary>
            /// Creates a new IntelRHDGraphicsControlPanel  folder.
            /// </summary>
            public IntelRHDGraphicsControlPanelAppFolder(RepoGenBaseFolder parentFolder) :
                    base("IntelRHDGraphicsControlPanel", "/form[@automationid='MainWindow']", parentFolder, 30000, true, "fd6a1488-ed3d-486c-b9d4-6c5195e0890c", "")
            {
                _displaymainpage = new HotkeyPanelRepoFolders.DisplayMainPageFolder(this);
                _selfInfo = new RepoItemInfo(this, "Self", "", 0, null, "fd6a1488-ed3d-486c-b9d4-6c5195e0890c");
            }

            /// <summary>
            /// The Self item.
            /// </summary>
            [RepositoryItem("fd6a1488-ed3d-486c-b9d4-6c5195e0890c")]
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
            [RepositoryItemInfo("fd6a1488-ed3d-486c-b9d4-6c5195e0890c")]
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
            [RepositoryFolder("df47cc7f-c3b4-4d14-89d5-909348a0b4b9")]
            public virtual HotkeyPanelRepoFolders.DisplayMainPageFolder DisplayMainPage
            {
                get { return _displaymainpage; }
            }
        }

        /// <summary>
        /// The DisplayMainPageFolder folder.
        /// </summary>
        [RepositoryFolder("df47cc7f-c3b4-4d14-89d5-909348a0b4b9")]
        public partial class DisplayMainPageFolder : RepoGenBaseFolder
        {
            RepoItemInfo _selfInfo;
            RepoItemInfo _basicadvoptionsInfo;
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
            RepoItemInfo _colorimetrycontrolInfo;
            RepoItemInfo _horizontallist01Info;
            RepoItemInfo _horizontalscrollbar2Info;
            RepoItemInfo _verticalscrollbar2Info;
            RepoItemInfo _partcontenthost2Info;
            RepoItemInfo _text2Info;
            RepoItemInfo _horizontallist11Info;
            RepoItemInfo _horizontalscrollbar3Info;
            RepoItemInfo _verticalscrollbar3Info;
            RepoItemInfo _partcontenthost3Info;
            RepoItemInfo _text3Info;
            RepoItemInfo _labelandhelpcontrolInfo;
            RepoItemInfo _imageInfo;
            RepoItemInfo _btntooltipInfo;
            RepoItemInfo _xvyccInfo;

            /// <summary>
            /// Creates a new DisplayMainPage  folder.
            /// </summary>
            public DisplayMainPageFolder(RepoGenBaseFolder parentFolder) :
                    base("DisplayMainPage", "element", parentFolder, 30000, true, "df47cc7f-c3b4-4d14-89d5-909348a0b4b9", "")
            {
                _selfInfo = new RepoItemInfo(this, "Self", "", 0, null, "df47cc7f-c3b4-4d14-89d5-909348a0b4b9");
                _basicadvoptionsInfo = new RepoItemInfo(this, "BasicAdvOptions", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='basicAdvOptions']", 30000, null, "0de9eaba-ab69-4af9-99e9-5f287fd28c7c");
                _horizontallist0Info = new RepoItemInfo(this, "HorizontalList0", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='basicAdvOptions']/element[@automationid='HorizontalList_0']", 30000, null, "4d4b20fd-04ad-405a-8fb6-cdfc116cd8d7");
                _horizontalscrollbarInfo = new RepoItemInfo(this, "HorizontalScrollBar", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='basicAdvOptions']/element[@automationid='HorizontalList_0']/text/container/scrollbar[@automationid='HorizontalScrollBar']", 30000, null, "fd337d4b-e231-49b4-8324-0b1fc709d259");
                _verticalscrollbarInfo = new RepoItemInfo(this, "VerticalScrollBar", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='basicAdvOptions']/element[@automationid='HorizontalList_0']/text/container/scrollbar[@automationid='VerticalScrollBar']", 30000, null, "9bd6ebac-2fbd-4204-b610-44d2987adac0");
                _partcontenthostInfo = new RepoItemInfo(this, "PARTContentHost", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='basicAdvOptions']/element[@automationid='HorizontalList_0']/text/container[@automationid='PART_ContentHost']", 30000, null, "bb1dc6d5-b5fb-4f9c-8e8f-c7dad7af97f9");
                _textInfo = new RepoItemInfo(this, "Text", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='basicAdvOptions']/element[@automationid='HorizontalList_0']/text[@automationid='text']", 30000, null, "ce767dd3-49ea-4644-b274-8bf9e6092398");
                _horizontallist1Info = new RepoItemInfo(this, "HorizontalList1", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='basicAdvOptions']/element[@automationid='HorizontalList_1']", 30000, null, "77cf2a28-42dc-4e46-8752-3dfff38b213f");
                _horizontalscrollbar1Info = new RepoItemInfo(this, "HorizontalScrollBar1", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='basicAdvOptions']/element[@automationid='HorizontalList_1']/text/container/scrollbar[@automationid='HorizontalScrollBar']", 30000, null, "1d2b5822-cdd7-4e57-bef0-89339d48c269");
                _verticalscrollbar1Info = new RepoItemInfo(this, "VerticalScrollBar1", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='basicAdvOptions']/element[@automationid='HorizontalList_1']/text/container/scrollbar[@automationid='VerticalScrollBar']", 30000, null, "1c287a3f-427b-4480-b945-fa8b94bed818");
                _partcontenthost1Info = new RepoItemInfo(this, "PARTContentHost1", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='basicAdvOptions']/element[@automationid='HorizontalList_1']/text/container[@automationid='PART_ContentHost']", 30000, null, "676eea21-5ceb-439e-9aef-f35615131f1c");
                _text1Info = new RepoItemInfo(this, "Text1", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='basicAdvOptions']/element[@automationid='HorizontalList_1']/text[@automationid='text']", 30000, null, "26e1c9bc-e085-42e9-82df-b131e61fcf14");
                _colorimetrycontrolInfo = new RepoItemInfo(this, "ColorimetryControl", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='colorimetryControl']", 30000, null, "a249f50c-1f78-473c-a46a-3c9aa799e75e");
                _horizontallist01Info = new RepoItemInfo(this, "HorizontalList01", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='colorimetryControl']/element[@automationid='HorizontalList_0']", 30000, null, "509c93b6-fd2c-4a74-ae49-44ede5c14fed");
                _horizontalscrollbar2Info = new RepoItemInfo(this, "HorizontalScrollBar2", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='colorimetryControl']/element[@automationid='HorizontalList_0']/text/container/scrollbar[@automationid='HorizontalScrollBar']", 30000, null, "47dedee5-ba96-4dda-bda5-62ee5cf425be");
                _verticalscrollbar2Info = new RepoItemInfo(this, "VerticalScrollBar2", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='colorimetryControl']/element[@automationid='HorizontalList_0']/text/container/scrollbar[@automationid='VerticalScrollBar']", 30000, null, "b44d746e-37b3-4dc4-9b3e-c1a68ddd7f80");
                _partcontenthost2Info = new RepoItemInfo(this, "PARTContentHost2", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='colorimetryControl']/element[@automationid='HorizontalList_0']/text/container[@automationid='PART_ContentHost']", 30000, null, "4aff7e4e-fd22-45b6-bb23-4d450f60c7c6");
                _text2Info = new RepoItemInfo(this, "Text2", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='colorimetryControl']/element[@automationid='HorizontalList_0']/text[@automationid='text']", 30000, null, "93ef0f5f-0866-4db2-b125-75c8875d89a9");
                _horizontallist11Info = new RepoItemInfo(this, "HorizontalList11", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='colorimetryControl']/element[@automationid='HorizontalList_1']", 30000, null, "53d41f4e-b3a8-4e73-a798-348b6cfbf130");
                _horizontalscrollbar3Info = new RepoItemInfo(this, "HorizontalScrollBar3", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='colorimetryControl']/element[@automationid='HorizontalList_1']/text/container/scrollbar[@automationid='HorizontalScrollBar']", 30000, null, "9471bae7-5eaa-4ec5-ab8c-83d6bcedf717");
                _verticalscrollbar3Info = new RepoItemInfo(this, "VerticalScrollBar3", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='colorimetryControl']/element[@automationid='HorizontalList_1']/text/container/scrollbar[@automationid='VerticalScrollBar']", 30000, null, "cfe04d0b-6d18-4641-9a99-19a1ba288b56");
                _partcontenthost3Info = new RepoItemInfo(this, "PARTContentHost3", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='colorimetryControl']/element[@automationid='HorizontalList_1']/text/container[@automationid='PART_ContentHost']", 30000, null, "5a0768fe-a0b9-4960-b89c-db8ba08a9c82");
                _text3Info = new RepoItemInfo(this, "Text3", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='colorimetryControl']/element[@automationid='HorizontalList_1']/text[@automationid='text']", 30000, null, "ff7f6e90-c70a-450a-8d3a-6250530d7bb0");
                _labelandhelpcontrolInfo = new RepoItemInfo(this, "LabelAndHelpControl", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='colorimetryControl']/element[@automationid='labelAndHelpControl']", 30000, null, "4c9d497a-dd03-48e1-9f27-1093316a746a");
                _imageInfo = new RepoItemInfo(this, "Image", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='colorimetryControl']/element[@automationid='labelAndHelpControl']/button/picture[@automationid='image']", 30000, null, "d593be5b-46b6-467b-b442-e62f4430fcf0");
                _btntooltipInfo = new RepoItemInfo(this, "BtnTooltip", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='colorimetryControl']/element[@automationid='labelAndHelpControl']/button[@automationid='btnTooltip']", 30000, null, "0c466ec8-9818-4a1a-9733-b5d467d37e1e");
                _xvyccInfo = new RepoItemInfo(this, "XvYCC", "element[@classname='DisplaySettingsWindow']/element[@classname='DisplayColorControl']/element[@automationid='colorimetryControl']/element[@automationid='labelAndHelpControl']/text[@automationid='text']", 30000, null, "5b87a18e-af37-457c-8ff3-0c66ef0eb8c2");
            }

            /// <summary>
            /// The Self item.
            /// </summary>
            [RepositoryItem("df47cc7f-c3b4-4d14-89d5-909348a0b4b9")]
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
            [RepositoryItemInfo("df47cc7f-c3b4-4d14-89d5-909348a0b4b9")]
            public virtual RepoItemInfo SelfInfo
            {
                get
                {
                    return _selfInfo;
                }
            }

            /// <summary>
            /// The BasicAdvOptions item.
            /// </summary>
            [RepositoryItem("0de9eaba-ab69-4af9-99e9-5f287fd28c7c")]
            public virtual Ranorex.Unknown BasicAdvOptions
            {
                get
                {
                    return _basicadvoptionsInfo.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The BasicAdvOptions item info.
            /// </summary>
            [RepositoryItemInfo("0de9eaba-ab69-4af9-99e9-5f287fd28c7c")]
            public virtual RepoItemInfo BasicAdvOptionsInfo
            {
                get
                {
                    return _basicadvoptionsInfo;
                }
            }

            /// <summary>
            /// The HorizontalList0 item.
            /// </summary>
            [RepositoryItem("4d4b20fd-04ad-405a-8fb6-cdfc116cd8d7")]
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
            [RepositoryItemInfo("4d4b20fd-04ad-405a-8fb6-cdfc116cd8d7")]
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
            [RepositoryItem("fd337d4b-e231-49b4-8324-0b1fc709d259")]
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
            [RepositoryItemInfo("fd337d4b-e231-49b4-8324-0b1fc709d259")]
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
            [RepositoryItem("9bd6ebac-2fbd-4204-b610-44d2987adac0")]
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
            [RepositoryItemInfo("9bd6ebac-2fbd-4204-b610-44d2987adac0")]
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
            [RepositoryItem("bb1dc6d5-b5fb-4f9c-8e8f-c7dad7af97f9")]
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
            [RepositoryItemInfo("bb1dc6d5-b5fb-4f9c-8e8f-c7dad7af97f9")]
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
            [RepositoryItem("ce767dd3-49ea-4644-b274-8bf9e6092398")]
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
            [RepositoryItemInfo("ce767dd3-49ea-4644-b274-8bf9e6092398")]
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
            [RepositoryItem("77cf2a28-42dc-4e46-8752-3dfff38b213f")]
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
            [RepositoryItemInfo("77cf2a28-42dc-4e46-8752-3dfff38b213f")]
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
            [RepositoryItem("1d2b5822-cdd7-4e57-bef0-89339d48c269")]
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
            [RepositoryItemInfo("1d2b5822-cdd7-4e57-bef0-89339d48c269")]
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
            [RepositoryItem("1c287a3f-427b-4480-b945-fa8b94bed818")]
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
            [RepositoryItemInfo("1c287a3f-427b-4480-b945-fa8b94bed818")]
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
            [RepositoryItem("676eea21-5ceb-439e-9aef-f35615131f1c")]
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
            [RepositoryItemInfo("676eea21-5ceb-439e-9aef-f35615131f1c")]
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
            [RepositoryItem("26e1c9bc-e085-42e9-82df-b131e61fcf14")]
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
            [RepositoryItemInfo("26e1c9bc-e085-42e9-82df-b131e61fcf14")]
            public virtual RepoItemInfo Text1Info
            {
                get
                {
                    return _text1Info;
                }
            }

            /// <summary>
            /// The ColorimetryControl item.
            /// </summary>
            [RepositoryItem("a249f50c-1f78-473c-a46a-3c9aa799e75e")]
            public virtual Ranorex.Unknown ColorimetryControl
            {
                get
                {
                    try
                    {
                        return _colorimetrycontrolInfo.CreateAdapter<Ranorex.Unknown>(true);
                    }
                    catch
                    {
                        return XvyccYcbcrRepo2.Instance.IntelRGraphics.DisplayMainPage.XvyccControl;
                    }
                }
            }

            /// <summary>
            /// The ColorimetryControl item info.
            /// </summary>
            [RepositoryItemInfo("a249f50c-1f78-473c-a46a-3c9aa799e75e")]
            public virtual RepoItemInfo ColorimetryControlInfo
            {
                get
                {
                    return _colorimetrycontrolInfo;
                }
            }

            /// <summary>
            /// The HorizontalList01 item.
            /// </summary>
            [RepositoryItem("509c93b6-fd2c-4a74-ae49-44ede5c14fed")]
            public virtual Ranorex.Unknown HorizontalList01
            {
                get
                {
                    return _horizontallist01Info.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The HorizontalList01 item info.
            /// </summary>
            [RepositoryItemInfo("509c93b6-fd2c-4a74-ae49-44ede5c14fed")]
            public virtual RepoItemInfo HorizontalList01Info
            {
                get
                {
                    return _horizontallist01Info;
                }
            }

            /// <summary>
            /// The HorizontalScrollBar2 item.
            /// </summary>
            [RepositoryItem("47dedee5-ba96-4dda-bda5-62ee5cf425be")]
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
            [RepositoryItemInfo("47dedee5-ba96-4dda-bda5-62ee5cf425be")]
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
            [RepositoryItem("b44d746e-37b3-4dc4-9b3e-c1a68ddd7f80")]
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
            [RepositoryItemInfo("b44d746e-37b3-4dc4-9b3e-c1a68ddd7f80")]
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
            [RepositoryItem("4aff7e4e-fd22-45b6-bb23-4d450f60c7c6")]
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
            [RepositoryItemInfo("4aff7e4e-fd22-45b6-bb23-4d450f60c7c6")]
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
            [RepositoryItem("93ef0f5f-0866-4db2-b125-75c8875d89a9")]
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
            [RepositoryItemInfo("93ef0f5f-0866-4db2-b125-75c8875d89a9")]
            public virtual RepoItemInfo Text2Info
            {
                get
                {
                    return _text2Info;
                }
            }

            /// <summary>
            /// The HorizontalList11 item.
            /// </summary>
            [RepositoryItem("53d41f4e-b3a8-4e73-a798-348b6cfbf130")]
            public virtual Ranorex.Unknown HorizontalList11
            {
                get
                {
                    return _horizontallist11Info.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The HorizontalList11 item info.
            /// </summary>
            [RepositoryItemInfo("53d41f4e-b3a8-4e73-a798-348b6cfbf130")]
            public virtual RepoItemInfo HorizontalList11Info
            {
                get
                {
                    return _horizontallist11Info;
                }
            }

            /// <summary>
            /// The HorizontalScrollBar3 item.
            /// </summary>
            [RepositoryItem("9471bae7-5eaa-4ec5-ab8c-83d6bcedf717")]
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
            [RepositoryItemInfo("9471bae7-5eaa-4ec5-ab8c-83d6bcedf717")]
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
            [RepositoryItem("cfe04d0b-6d18-4641-9a99-19a1ba288b56")]
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
            [RepositoryItemInfo("cfe04d0b-6d18-4641-9a99-19a1ba288b56")]
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
            [RepositoryItem("5a0768fe-a0b9-4960-b89c-db8ba08a9c82")]
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
            [RepositoryItemInfo("5a0768fe-a0b9-4960-b89c-db8ba08a9c82")]
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
            [RepositoryItem("ff7f6e90-c70a-450a-8d3a-6250530d7bb0")]
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
            [RepositoryItemInfo("ff7f6e90-c70a-450a-8d3a-6250530d7bb0")]
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
            [RepositoryItem("4c9d497a-dd03-48e1-9f27-1093316a746a")]
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
            [RepositoryItemInfo("4c9d497a-dd03-48e1-9f27-1093316a746a")]
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
            [RepositoryItem("d593be5b-46b6-467b-b442-e62f4430fcf0")]
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
            [RepositoryItemInfo("d593be5b-46b6-467b-b442-e62f4430fcf0")]
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
            [RepositoryItem("0c466ec8-9818-4a1a-9733-b5d467d37e1e")]
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
            [RepositoryItemInfo("0c466ec8-9818-4a1a-9733-b5d467d37e1e")]
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
            [RepositoryItem("5b87a18e-af37-457c-8ff3-0c66ef0eb8c2")]
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
            [RepositoryItemInfo("5b87a18e-af37-457c-8ff3-0c66ef0eb8c2")]
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