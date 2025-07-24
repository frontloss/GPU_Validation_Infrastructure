namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Text;
    using System.Drawing;
    using Ranorex;
    using System.Linq;
    using Ranorex.Core;
    using Ranorex.Core.Repository;
    using Ranorex.Core.Testing;

    /// <summary>
    /// The class representing the DTCMRepo element repository.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    [RepositoryFolder("c19c68d0-7776-4654-8645-ae05488fdb60")]
    public partial class DTCMRepo : RepoGenBaseFolder
    {
        static DTCMRepo instance = new DTCMRepo();
        DTCMRepoFolders.MenuBarExplorerAppFolder _menuBarexplorer;
        DTCMRepoFolders.ContextMenuExplorerAppFolder _contextmenuexplorer;

        /// <summary>
        /// Gets the singleton class instance representing the DTCMRepo element repository.
        /// </summary>
        [RepositoryFolder("c19c68d0-7776-4654-8645-ae05488fdb60")]
        public static DTCMRepo Instance
        {
            get { return instance; }
        }

        /// <summary>
        /// Repository class constructor.
        /// </summary>
        public DTCMRepo()
            : base("DTCMRepo", "", null, 30000, false, "c19c68d0-7776-4654-8645-ae05488fdb60", ".\\RepositoryImages\\DTCMRepoc19c68d0.rximgres")
        {
            _menuBarexplorer = new DTCMRepoFolders.MenuBarExplorerAppFolder(this);
            _contextmenuexplorer = new DTCMRepoFolders.ContextMenuExplorerAppFolder(this);
        }

        #region Variables

        #endregion

        /// <summary>
        /// The Explorer folder.
        /// </summary>
        [RepositoryFolder("b6c35f64-01f9-4a59-a1ab-25dd5b7a64eb")]
        public virtual DTCMRepoFolders.MenuBarExplorerAppFolder MenuBarexplorer
        {
            get { return _menuBarexplorer; }
        }

        /// <summary>
        /// The ContextMenuHash32768 folder.
        /// </summary>
        [RepositoryFolder("62b46c9e-5576-45fb-b994-9d4d21aaa17d")]
        public virtual DTCMRepoFolders.ContextMenuExplorerAppFolder ContextMenuExplorer
        {
            get { return _contextmenuexplorer; }
        }
    }

    /// <summary>
    /// Inner folder classes.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    public partial class DTCMRepoFolders
    {
        /// <summary>
        /// The ExplorerAppFolder folder.
        /// </summary>
        [RepositoryFolder("b6c35f64-01f9-4a59-a1ab-25dd5b7a64eb")]
        public partial class MenuBarExplorerAppFolder : RepoGenBaseFolder
        {
            RepoItemInfo _selfInfo;
            RepoItemInfo _explorerInfo;
            RepoItemInfo _button1502Info;

            /// <summary>
            /// Creates a new Explorer  folder.
            /// </summary>
            public MenuBarExplorerAppFolder(RepoGenBaseFolder parentFolder) :
                base("MenuBarExplorer", "/menubar[@processname='explorer' and @class='Shell_TrayWnd']", parentFolder, 30000, true, "b6c35f64-01f9-4a59-a1ab-25dd5b7a64eb", "")
            {
                _selfInfo = new RepoItemInfo(this, "Self", "", 30000, null, "b6c35f64-01f9-4a59-a1ab-25dd5b7a64eb");
                _explorerInfo = new RepoItemInfo(this, "Explorer", "", 30000, null, "040b74dc-754b-4b88-a2f2-0d0eebaeeba4");
                _button1502Info = new RepoItemInfo(this, "Button1502", "container/button[@text='']", 30000, null, "0873144c-9005-453d-80e7-100b9048f0e9");
            }

            /// <summary>
            /// The Self item.
            /// </summary>
            [RepositoryItem("b6c35f64-01f9-4a59-a1ab-25dd5b7a64eb")]
            public virtual Ranorex.MenuBar Self
            {
                get
                {
                    return _selfInfo.CreateAdapter<Ranorex.MenuBar>(true);
                }
            }

            /// <summary>
            /// The ButtonIntelLParenRRParen_HD_Gr item.
            /// </summary>
            public virtual Ranorex.Button ButtonIntelLParenRRParen_HD_Gr
            {
                get
                {
                    //Button trayBtn = null;
                    //IList<Button> trayBtns = this.Self.FindSingle<ToolBar>("./container/container/toolbar").Buttons;
                    //Console.WriteLine("*********DTCMRepo***********");
                    //trayBtns.ToList().ForEach(b =>
                    //    {
                    //        Console.WriteLine(b.Text);
                    //        if (b.Text.Equals("Intel(R) HD Graphics") || b.Text.Equals("Intel(R) Iris(TM) Graphics") || b.Text.Equals("Intel® HD Graphics"))
                    //            trayBtn = b;
                    //    });
                    //Console.WriteLine("*********DTCMRepo***********");
                    //return trayBtn;
                    return this.Self.FindSingle<ToolBar>("./container/container/toolbar").Buttons
                        .Where(b => b.Text.Equals("Intel(R) HD Graphics") || b.Text.Equals("Intel(R) Iris(TM) Graphics") || b.Text.Equals("Intel® HD Graphics"))
                        .FirstOrDefault();
                }
            }

            /// <summary>
            /// The Button1502 item.
            /// </summary>
            [RepositoryItem("0873144c-9005-453d-80e7-100b9048f0e9")]
            public virtual Ranorex.Button Button1502
            {
                get
                {
                    return _button1502Info.CreateAdapter<Ranorex.Button>(true);
                }
            }
        }

        /// <summary>
        /// The ContextMenuHash32768AppFolder folder.
        /// </summary>
        [RepositoryFolder("62b46c9e-5576-45fb-b994-9d4d21aaa17d")]
        public partial class ContextMenuExplorerAppFolder : RepoGenBaseFolder
        {
            RepoItemInfo _selfInfo;
            //RepoItemInfo _contextmenuhash32768Info;
            //RepoItemInfo _contextInfo;

            /// <summary>
            /// Creates a new ContextMenuHash32768  folder.
            /// </summary>
            public ContextMenuExplorerAppFolder(RepoGenBaseFolder parentFolder) :
                base("ContextMenuExplorer", "/contextmenu[@processname='explorer' or @processname='igfxtray' or @processname='igfxTray']", parentFolder, 30000, true, "62b46c9e-5576-45fb-b994-9d4d21aaa17d", "")
            {
                _selfInfo = new RepoItemInfo(this, "Self", "", 0, null, "62b46c9e-5576-45fb-b994-9d4d21aaa17d");
                //_contextmenuhash32768Info = new RepoItemInfo(this, "ContextMenuHash32768", "", 5000, null, "8cad0e89-1591-45de-b0de-ea1bef74ff18");
                //_contextInfo = new RepoItemInfo(this, "Context", "contextmenu", 5000, null, "384f0f16-4f9b-4661-b79b-46c682eaa1d0");
            }

            /// <summary>
            /// The Self item.
            /// </summary>
            [RepositoryItem("62b46c9e-5576-45fb-b994-9d4d21aaa17d")]
            public virtual Ranorex.ContextMenu Self
            {
                get
                {
                    return _selfInfo.CreateAdapter<Ranorex.ContextMenu>(true);
                }
            }

        }
    }
}