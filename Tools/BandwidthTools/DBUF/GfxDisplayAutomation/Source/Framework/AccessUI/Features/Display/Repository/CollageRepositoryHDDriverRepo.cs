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
    /// The class representing the ColorEnhacementReposHD element repository.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    [RepositoryFolder("53c0a7d5-08ee-4931-8afe-17776abaf70b")]
    public partial class ColorEnhacementReposHD : RepoGenBaseFolder
    {
        static ColorEnhacementReposHD instance = new ColorEnhacementReposHD();
        ColorEnhacementReposHDFolders.IntelRHDGraphicsControlPanelAppFolder _intelrhdgraphicscontrolpanel;

        /// <summary>
        /// Gets the singleton class instance representing the ColorEnhacementReposHD element repository.
        /// </summary>
        [RepositoryFolder("53c0a7d5-08ee-4931-8afe-17776abaf70b")]
        public static ColorEnhacementReposHD Instance
        {
            get { return instance; }
        }

        /// <summary>
        /// Repository class constructor.
        /// </summary>
        public ColorEnhacementReposHD() 
            : base("ColorEnhacementReposHD", "", null, 30000, false, "53c0a7d5-08ee-4931-8afe-17776abaf70b", ".\\RepositoryImages\\CollageRepositoryHDDriver53c0a7d5.rximgres")
        {
            _intelrhdgraphicscontrolpanel = new ColorEnhacementReposHDFolders.IntelRHDGraphicsControlPanelAppFolder(this);
        }

#region Variables

#endregion

        /// <summary>
        /// The IntelRHDGraphicsControlPanel folder.
        /// </summary>
        [RepositoryFolder("6bbe6182-c9ba-489e-9f85-f98efaf03a4f")]
        public virtual ColorEnhacementReposHDFolders.IntelRHDGraphicsControlPanelAppFolder IntelRHDGraphicsControlPanel
        {
            get { return _intelrhdgraphicscontrolpanel; }
        }
    }

    /// <summary>
    /// Inner folder classes.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    public partial class ColorEnhacementReposHDFolders
    {
        /// <summary>
        /// The IntelRHDGraphicsControlPanelAppFolder folder.
        /// </summary>
        [RepositoryFolder("6bbe6182-c9ba-489e-9f85-f98efaf03a4f")]
        public partial class IntelRHDGraphicsControlPanelAppFolder : RepoGenBaseFolder
        {
            ColorEnhacementReposHDFolders.DisplayMainPageFolder _displaymainpage;
            RepoItemInfo _selfInfo;

            /// <summary>
            /// Creates a new IntelRHDGraphicsControlPanel  folder.
            /// </summary>
            public IntelRHDGraphicsControlPanelAppFolder(RepoGenBaseFolder parentFolder) :
                    base("IntelRHDGraphicsControlPanel", "/form[@automationid='MainWindow']", parentFolder, 30000, true, "6bbe6182-c9ba-489e-9f85-f98efaf03a4f", "")
            {
                _displaymainpage = new ColorEnhacementReposHDFolders.DisplayMainPageFolder(this);
                _selfInfo = new RepoItemInfo(this, "Self", "", 0, null, "6bbe6182-c9ba-489e-9f85-f98efaf03a4f");
            }

            /// <summary>
            /// The Self item.
            /// </summary>
            [RepositoryItem("6bbe6182-c9ba-489e-9f85-f98efaf03a4f")]
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
            [RepositoryItemInfo("6bbe6182-c9ba-489e-9f85-f98efaf03a4f")]
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
            [RepositoryFolder("c0418726-5cb6-4552-b61b-da2254d07732")]
            public virtual ColorEnhacementReposHDFolders.DisplayMainPageFolder DisplayMainPage
            {
                get { return _displaymainpage; }
            }
        }

        /// <summary>
        /// The DisplayMainPageFolder folder.
        /// </summary>
        [RepositoryFolder("c0418726-5cb6-4552-b61b-da2254d07732")]
        public partial class DisplayMainPageFolder : RepoGenBaseFolder
        {
            RepoItemInfo _selfInfo;
            RepoItemInfo _enablecollagecontrolInfo;
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
            RepoItemInfo _comboboxselectcollagestatusInfo;
            RepoItemInfo _disable1Info;
            RepoItemInfo _disableInfo;
            RepoItemInfo _enable1Info;
            RepoItemInfo _enableInfo;

            /// <summary>
            /// Creates a new DisplayMainPage  folder.
            /// </summary>
            public DisplayMainPageFolder(RepoGenBaseFolder parentFolder) :
                    base("DisplayMainPage", "element", parentFolder, 30000, true, "c0418726-5cb6-4552-b61b-da2254d07732", "")
            {
                _selfInfo = new RepoItemInfo(this, "Self", "", 0, null, "c0418726-5cb6-4552-b61b-da2254d07732");
                _enablecollagecontrolInfo = new RepoItemInfo(this, "EnableCollageControl", "element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']", 30000, null, "0935a17a-fe2f-40ee-876e-f3499b0cd0cf");
                _verticallist0Info = new RepoItemInfo(this, "VerticalList0", "element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='VerticalList_0']", 30000, null, "f70e19b5-ced0-41cd-988a-b4884f50ef08");
                _horizontalscrollbarInfo = new RepoItemInfo(this, "HorizontalScrollBar", "element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='VerticalList_0']/text/container/scrollbar[@automationid='HorizontalScrollBar']", 30000, null, "eb5eec53-8acf-466c-83f7-39f73a1553a2");
                _verticalscrollbarInfo = new RepoItemInfo(this, "VerticalScrollBar", "element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='VerticalList_0']/text/container/scrollbar[@automationid='VerticalScrollBar']", 30000, null, "9f53a4c5-39b8-4a05-8ed5-40fba4615614");
                _partcontenthostInfo = new RepoItemInfo(this, "PARTContentHost", "element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='VerticalList_0']/text/container[@automationid='PART_ContentHost']", 30000, null, "d5957e25-6dd4-414f-bf04-9e2c64ce088d");
                _textInfo = new RepoItemInfo(this, "Text", "element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='VerticalList_0']/text[@automationid='text']", 30000, null, "95a1fb3d-6221-4acd-835b-bc97e4eb5fc8");
                _verticallist1Info = new RepoItemInfo(this, "VerticalList1", "element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='VerticalList_1']", 30000, null, "c378b6ba-0904-4db2-b5ee-84b4fba0a8ae");
                _horizontalscrollbar1Info = new RepoItemInfo(this, "HorizontalScrollBar1", "element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='VerticalList_1']/text/container/scrollbar[@automationid='HorizontalScrollBar']", 30000, null, "880eba31-593d-4a5a-94f1-8d64a08e5d56");
                _verticalscrollbar1Info = new RepoItemInfo(this, "VerticalScrollBar1", "element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='VerticalList_1']/text/container/scrollbar[@automationid='VerticalScrollBar']", 30000, null, "16f01f9c-7026-4304-930c-99574d9990ca");
                _partcontenthost1Info = new RepoItemInfo(this, "PARTContentHost1", "element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='VerticalList_1']/text/container[@automationid='PART_ContentHost']", 30000, null, "35b1b7cc-38bb-4c39-8ceb-0438b9fe76f0");
                _text1Info = new RepoItemInfo(this, "Text1", "element[@classname='MultipleDisplays']/element[@automationid='enableCollageControl']/element[@automationid='VerticalList_1']/text[@automationid='text']", 30000, null, "b37231c7-53e0-4e61-8228-a6af0c1e90d9");
                _comboboxselectcollagestatusInfo = new RepoItemInfo(this, "ComboBoxSelectCollageStatus", "element[@classname='MultipleDisplays']/combobox[@automationid='comboBoxSelectCollageStatus']", 30000, null, "34b54211-5a5c-4bd9-8f62-ce2a138e2810");
                _disable1Info = new RepoItemInfo(this, "Disable1", "element[@classname='MultipleDisplays']/combobox[@automationid='comboBoxSelectCollageStatus']/listitem[@name='Disable']", 30000, null, "df4dcad0-eff6-4b18-b60c-541d9030e34c");
                _disableInfo = new RepoItemInfo(this, "Disable", "element[@classname='MultipleDisplays']/combobox[@automationid='comboBoxSelectCollageStatus']/listitem[@name='Disable']/text[@name='Disable']", 30000, null, "2eaf8b56-98db-466d-8ad4-34f43790a10a");
                _enable1Info = new RepoItemInfo(this, "Enable1", "element[@classname='MultipleDisplays']/combobox[@automationid='comboBoxSelectCollageStatus']/listitem[@name='Enable']", 30000, null, "8fd74d0d-9911-42f4-9650-7d12f223995b");
                _enableInfo = new RepoItemInfo(this, "Enable", "element[@classname='MultipleDisplays']/combobox[@automationid='comboBoxSelectCollageStatus']/listitem[@name='Enable']/text[@name='Enable']", 30000, null, "92ec8387-3e53-4a86-acea-35de1e1d17e7");
            }

            /// <summary>
            /// The Self item.
            /// </summary>
            [RepositoryItem("c0418726-5cb6-4552-b61b-da2254d07732")]
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
            [RepositoryItemInfo("c0418726-5cb6-4552-b61b-da2254d07732")]
            public virtual RepoItemInfo SelfInfo
            {
                get
                {
                    return _selfInfo;
                }
            }

            /// <summary>
            /// The EnableCollageControl item.
            /// </summary>
            [RepositoryItem("0935a17a-fe2f-40ee-876e-f3499b0cd0cf")]
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
            [RepositoryItemInfo("0935a17a-fe2f-40ee-876e-f3499b0cd0cf")]
            public virtual RepoItemInfo EnableCollageControlInfo
            {
                get
                {
                    return _enablecollagecontrolInfo;
                }
            }

            /// <summary>
            /// The VerticalList0 item.
            /// </summary>
            [RepositoryItem("f70e19b5-ced0-41cd-988a-b4884f50ef08")]
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
            [RepositoryItemInfo("f70e19b5-ced0-41cd-988a-b4884f50ef08")]
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
            [RepositoryItem("eb5eec53-8acf-466c-83f7-39f73a1553a2")]
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
            [RepositoryItemInfo("eb5eec53-8acf-466c-83f7-39f73a1553a2")]
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
            [RepositoryItem("9f53a4c5-39b8-4a05-8ed5-40fba4615614")]
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
            [RepositoryItemInfo("9f53a4c5-39b8-4a05-8ed5-40fba4615614")]
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
            [RepositoryItem("d5957e25-6dd4-414f-bf04-9e2c64ce088d")]
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
            [RepositoryItemInfo("d5957e25-6dd4-414f-bf04-9e2c64ce088d")]
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
            [RepositoryItem("95a1fb3d-6221-4acd-835b-bc97e4eb5fc8")]
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
            [RepositoryItemInfo("95a1fb3d-6221-4acd-835b-bc97e4eb5fc8")]
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
            [RepositoryItem("c378b6ba-0904-4db2-b5ee-84b4fba0a8ae")]
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
            [RepositoryItemInfo("c378b6ba-0904-4db2-b5ee-84b4fba0a8ae")]
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
            [RepositoryItem("880eba31-593d-4a5a-94f1-8d64a08e5d56")]
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
            [RepositoryItemInfo("880eba31-593d-4a5a-94f1-8d64a08e5d56")]
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
            [RepositoryItem("16f01f9c-7026-4304-930c-99574d9990ca")]
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
            [RepositoryItemInfo("16f01f9c-7026-4304-930c-99574d9990ca")]
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
            [RepositoryItem("35b1b7cc-38bb-4c39-8ceb-0438b9fe76f0")]
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
            [RepositoryItemInfo("35b1b7cc-38bb-4c39-8ceb-0438b9fe76f0")]
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
            [RepositoryItem("b37231c7-53e0-4e61-8228-a6af0c1e90d9")]
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
            [RepositoryItemInfo("b37231c7-53e0-4e61-8228-a6af0c1e90d9")]
            public virtual RepoItemInfo Text1Info
            {
                get
                {
                    return _text1Info;
                }
            }

            /// <summary>
            /// The ComboBoxSelectCollageStatus item.
            /// </summary>
            [RepositoryItem("34b54211-5a5c-4bd9-8f62-ce2a138e2810")]
            public virtual Ranorex.ComboBox ComboBoxSelectCollageStatus
            {
                get
                {
                    try
                    {
                        return _comboboxselectcollagestatusInfo.CreateAdapter<Ranorex.ComboBox>(true);
                    }
                    catch
                    {
                        return null;
                    }
                }
            }

            /// <summary>
            /// The ComboBoxSelectCollageStatus item info.
            /// </summary>
            [RepositoryItemInfo("34b54211-5a5c-4bd9-8f62-ce2a138e2810")]
            public virtual RepoItemInfo ComboBoxSelectCollageStatusInfo
            {
                get
                {
                    return _comboboxselectcollagestatusInfo;
                }
            }

            /// <summary>
            /// The Disable1 item.
            /// </summary>
            [RepositoryItem("df4dcad0-eff6-4b18-b60c-541d9030e34c")]
            public virtual Ranorex.ListItem Disable1
            {
                get
                {
                    return _disable1Info.CreateAdapter<Ranorex.ListItem>(true);
                }
            }

            /// <summary>
            /// The Disable1 item info.
            /// </summary>
            [RepositoryItemInfo("df4dcad0-eff6-4b18-b60c-541d9030e34c")]
            public virtual RepoItemInfo Disable1Info
            {
                get
                {
                    return _disable1Info;
                }
            }

            /// <summary>
            /// The Disable item.
            /// </summary>
            [RepositoryItem("2eaf8b56-98db-466d-8ad4-34f43790a10a")]
            public virtual Ranorex.Text Disable
            {
                get
                {
                    return _disableInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The Disable item info.
            /// </summary>
            [RepositoryItemInfo("2eaf8b56-98db-466d-8ad4-34f43790a10a")]
            public virtual RepoItemInfo DisableInfo
            {
                get
                {
                    return _disableInfo;
                }
            }

            /// <summary>
            /// The Enable1 item.
            /// </summary>
            [RepositoryItem("8fd74d0d-9911-42f4-9650-7d12f223995b")]
            public virtual Ranorex.ListItem Enable1
            {
                get
                {
                    return _enable1Info.CreateAdapter<Ranorex.ListItem>(true);
                }
            }

            /// <summary>
            /// The Enable1 item info.
            /// </summary>
            [RepositoryItemInfo("8fd74d0d-9911-42f4-9650-7d12f223995b")]
            public virtual RepoItemInfo Enable1Info
            {
                get
                {
                    return _enable1Info;
                }
            }

            /// <summary>
            /// The Enable item.
            /// </summary>
            [RepositoryItem("92ec8387-3e53-4a86-acea-35de1e1d17e7")]
            public virtual Ranorex.Text Enable
            {
                get
                {
                    return _enableInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The Enable item info.
            /// </summary>
            [RepositoryItemInfo("92ec8387-3e53-4a86-acea-35de1e1d17e7")]
            public virtual RepoItemInfo EnableInfo
            {
                get
                {
                    return _enableInfo;
                }
            }
        }

    }
}