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
    /// The class representing the ControlPanelRepo element repository.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    [RepositoryFolder("dfebd887-ff03-4c42-8a29-5eece08046bb")]
    public partial class ControlPanelRepo : RepoGenBaseFolder
    {
        static ControlPanelRepo instance = new ControlPanelRepo();
        ControlPanelRepoFolders.ControlPanelAppFolder _controlpanel;
        ControlPanelRepoFolders.ExplorerAppFolder _explorer;

        /// <summary>
        /// Gets the singleton class instance representing the ControlPanelRepo element repository.
        /// </summary>
        [RepositoryFolder("dfebd887-ff03-4c42-8a29-5eece08046bb")]
        public static ControlPanelRepo Instance
        {
            get { return instance; }
        }

        /// <summary>
        /// Repository class constructor.
        /// </summary>
        public ControlPanelRepo()
            : base("ControlPanelRepo", "", null, 30000, false, "dfebd887-ff03-4c42-8a29-5eece08046bb", ".\\RepositoryImages\\ControlPanelRepodfebd887.rximgres")
        {
            _controlpanel = new ControlPanelRepoFolders.ControlPanelAppFolder(this);
            _explorer = new ControlPanelRepoFolders.ExplorerAppFolder(this);
        }

        #region Variables

        #endregion

        /// <summary>
        /// The ControlPanel folder.
        /// </summary>
        [RepositoryFolder("c15a4d86-4bc4-4814-b6bb-1cf44c39278e")]
        public virtual ControlPanelRepoFolders.ControlPanelAppFolder FormControl_Panel
        {
            get { return _controlpanel; }
        }

        /// <summary>
        /// The Explorer folder.
        /// </summary>
        [RepositoryFolder("2df529f8-dabd-475b-8f98-ae3e3595734c")]
        public virtual ControlPanelRepoFolders.ExplorerAppFolder ContextMenuExplorer
        {
            get { return _explorer; }
        }
    }

    /// <summary>
    /// Inner folder classes.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    public partial class ControlPanelRepoFolders
    {
        /// <summary>
        /// The ControlPanelAppFolder folder.
        /// </summary>
        [RepositoryFolder("c15a4d86-4bc4-4814-b6bb-1cf44c39278e")]
        public partial class ControlPanelAppFolder : RepoGenBaseFolder
        {
            RepoItemInfo _selfInfo;
            RepoItemInfo _notificationareaiconsInfo;
            RepoItemInfo _intelrhdgraphicsInfo;
            RepoItemInfo _categoryInfo;
            RepoItemInfo _closeInfo;
            RepoItemInfo _checkboxalwaysshowalliconsandnotifiInfo;

            /// <summary>
            /// Creates a new ControlPanel  folder.
            /// </summary>
            public ControlPanelAppFolder(RepoGenBaseFolder parentFolder) :
                base("ControlPanel", "/form[@title~'Control Panel*' or @title='Notification Area Icons']", parentFolder, 30000, true, "c15a4d86-4bc4-4814-b6bb-1cf44c39278e", "")
            {
                _selfInfo = new RepoItemInfo(this, "Self", "", 30000, null, "c15a4d86-4bc4-4814-b6bb-1cf44c39278e");
                _notificationareaiconsInfo = new RepoItemInfo(this, "NotificationAreaIcons", "element[@class='ShellTabWindowClass']/element[@class='DUIViewWndClassName']/*/container/*/*/link[@accessiblename='Notification Area Icons']", 30000, null, "2e10aa64-49d7-4a61-8666-95215a79cbb4");
                _intelrhdgraphicsInfo = new RepoItemInfo(this, "IntelRHDGraphics", "element[@class='ShellTabWindowClass']/element[@class='DUIViewWndClassName']/*/container/*/*/link[@accessiblename='Intel(R) HD Graphics']", 30000, null, "9208c52f-6a55-4d10-aec5-a4cb154fb484");
                _categoryInfo = new RepoItemInfo(this, "Category", "element[@class='ShellTabWindowClass']/element[@class='DUIViewWndClassName']/container/container/container/container/button", 30000, null, "de31cce3-72c3-46e7-aebf-fd6cbd5717e7");
                if (Environment.OSVersion.Version.Minor.Equals(2))  //Win8  TODO
                    _categoryInfo = new RepoItemInfo(this, "Category", "element[@class='ShellTabWindowClass']/element[@class='DUIViewWndClassName']/container/container/container/container/container/button", 30000, null, "de31cce3-72c3-46e7-aebf-fd6cbd5717e7");
                _closeInfo = new RepoItemInfo(this, "Close", "titlebar/button[@accessiblename='Close']", 30000, null, "a3b7e9b2-07e2-4232-8856-fa56e5ab4d4a");
                _checkboxalwaysshowalliconsandnotifiInfo = new RepoItemInfo(this, "CheckBoxAlwaysShowAllIconsAndNotifi", "element[@class='ShellTabWindowClass']/element[@class='DUIViewWndClassName']/*/element/*/*/element[@class='CtrlNotifySink' and @instance='0']/checkbox", 30000, null, "89ac046b-2260-405f-ac9c-b69de0e3cd56");
            }

            /// <summary>
            /// The Self item.
            /// </summary>
            [RepositoryItem("c15a4d86-4bc4-4814-b6bb-1cf44c39278e")]
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
            [RepositoryItemInfo("c15a4d86-4bc4-4814-b6bb-1cf44c39278e")]
            public virtual RepoItemInfo SelfInfo
            {
                get
                {
                    return _selfInfo;
                }
            }

            /// <summary>
            /// The NotificationAreaIcons item.
            /// </summary>
            [RepositoryItem("2e10aa64-49d7-4a61-8666-95215a79cbb4")]
            public virtual Ranorex.Link LinkNotification_Area_Icons
            {
                get
                {
                    return _notificationareaiconsInfo.CreateAdapter<Ranorex.Link>(true);
                }
            }

            /// <summary>
            /// The NotificationAreaIcons item info.
            /// </summary>
            [RepositoryItemInfo("2e10aa64-49d7-4a61-8666-95215a79cbb4")]
            public virtual RepoItemInfo NotificationAreaIconsInfo
            {
                get
                {
                    return _notificationareaiconsInfo;
                }
            }

            /// <summary>
            /// The IntelRHDGraphics item.
            /// </summary>
            [RepositoryItem("9208c52f-6a55-4d10-aec5-a4cb154fb484")]
            public virtual Ranorex.Link LinkIntelLParenRRParen_Graph
            {
                get
                {
                    return _intelrhdgraphicsInfo.CreateAdapter<Ranorex.Link>(true);
                }
            }

            /// <summary>
            /// The IntelRHDGraphics item info.
            /// </summary>
            [RepositoryItemInfo("9208c52f-6a55-4d10-aec5-a4cb154fb484")]
            public virtual RepoItemInfo IntelRHDGraphicsInfo
            {
                get
                {
                    return _intelrhdgraphicsInfo;
                }
            }

            /// <summary>
            /// The Category item.
            /// </summary>
            [RepositoryItem("de31cce3-72c3-46e7-aebf-fd6cbd5717e7")]
            public virtual Ranorex.Button ButtonDDL
            {
                get
                {
                    //IList<Ranorex.Container> items = this.Self.Find<Ranorex.Container>("element[@class='ShellTabWindowClass']/element[@class='DUIViewWndClassName']/container/container/container/container");
                    //if (null != items && !items.Count.Equals(0))
                    //{
                    //    foreach (Container item in items)
                    //    {
                    //        IList<Ranorex.Button> btn = item.FindChildren<Ranorex.Button>();
                    //        if (null != btn && !btn.Count.Equals(0))
                    //            return btn[0];
                    //    }
                    //}
                    return _categoryInfo.CreateAdapter<Ranorex.Button>(true);
                }
            }

            /// <summary>
            /// The Category item info.
            /// </summary>
            [RepositoryItemInfo("de31cce3-72c3-46e7-aebf-fd6cbd5717e7")]
            public virtual RepoItemInfo CategoryInfo
            {
                get
                {
                    return _categoryInfo;
                }
            }

            /// <summary>
            /// The Close item.
            /// </summary>
            [RepositoryItem("a3b7e9b2-07e2-4232-8856-fa56e5ab4d4a")]
            public virtual Ranorex.Button ButtonClose
            {
                get
                {
                    return _closeInfo.CreateAdapter<Ranorex.Button>(true);
                }
            }

            /// <summary>
            /// The Close item info.
            /// </summary>
            [RepositoryItemInfo("a3b7e9b2-07e2-4232-8856-fa56e5ab4d4a")]
            public virtual RepoItemInfo CloseInfo
            {
                get
                {
                    return _closeInfo;
                }
            }

            /// <summary>
            /// The CheckBoxAlwaysShowAllIconsAndNotifi item.
            /// </summary>
            [RepositoryItem("89ac046b-2260-405f-ac9c-b69de0e3cd56")]
            public virtual Ranorex.CheckBox CheckBoxAlways_show_all_icons_an
            {
                get
                {
                    return _checkboxalwaysshowalliconsandnotifiInfo.CreateAdapter<Ranorex.CheckBox>(true);
                }
            }

            /// <summary>
            /// The CheckBoxAlwaysShowAllIconsAndNotifi item info.
            /// </summary>
            [RepositoryItemInfo("89ac046b-2260-405f-ac9c-b69de0e3cd56")]
            public virtual RepoItemInfo CheckBoxAlwaysShowAllIconsAndNotifiInfo
            {
                get
                {
                    return _checkboxalwaysshowalliconsandnotifiInfo;
                }
            }
        }

        /// <summary>
        /// The ExplorerAppFolder folder.
        /// </summary>
        [RepositoryFolder("2df529f8-dabd-475b-8f98-ae3e3595734c")]
        public partial class ExplorerAppFolder : RepoGenBaseFolder
        {
            RepoItemInfo _selfInfo;
            RepoItemInfo _largeiconsInfo;

            /// <summary>
            /// Creates a new Explorer  folder.
            /// </summary>
            public ExplorerAppFolder(RepoGenBaseFolder parentFolder) :
                base("Explorer", "/contextmenu", parentFolder, 30000, true, "2df529f8-dabd-475b-8f98-ae3e3595734c", "")
            {
                _selfInfo = new RepoItemInfo(this, "Self", "", 30000, null, "2df529f8-dabd-475b-8f98-ae3e3595734c");
                _largeiconsInfo = new RepoItemInfo(this, "LargeIcons", "contextmenu/menuitem[@accessiblename='Large icons']", 30000, null, "e86ccafd-d2bf-4f30-9cff-eafb1a5a24cf");
            }

            /// <summary>
            /// The Self item.
            /// </summary>
            [RepositoryItem("2df529f8-dabd-475b-8f98-ae3e3595734c")]
            public virtual Ranorex.ContextMenu Self
            {
                get
                {
                    return _selfInfo.CreateAdapter<Ranorex.ContextMenu>(true);
                }
            }

            /// <summary>
            /// The Self item info.
            /// </summary>
            [RepositoryItemInfo("2df529f8-dabd-475b-8f98-ae3e3595734c")]
            public virtual RepoItemInfo SelfInfo
            {
                get
                {
                    return _selfInfo;
                }
            }

            /// <summary>
            /// The LargeIcons item.
            /// </summary>
            [RepositoryItem("e86ccafd-d2bf-4f30-9cff-eafb1a5a24cf")]
            public virtual Ranorex.MenuItem MenuItemLarge_icons
            {
                get
                {
                    return _largeiconsInfo.CreateAdapter<Ranorex.MenuItem>(true);
                }
            }

            /// <summary>
            /// The LargeIcons item info.
            /// </summary>
            [RepositoryItemInfo("e86ccafd-d2bf-4f30-9cff-eafb1a5a24cf")]
            public virtual RepoItemInfo LargeIconsInfo
            {
                get
                {
                    return _largeiconsInfo;
                }
            }
        }

    }
}