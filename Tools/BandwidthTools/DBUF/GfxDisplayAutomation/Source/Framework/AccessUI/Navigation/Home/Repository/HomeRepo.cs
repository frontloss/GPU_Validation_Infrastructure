namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;
    using System.Text;
    using System.Drawing;
    using Ranorex;
    using Ranorex.Core;
    using Ranorex.Core.Repository;
    using Ranorex.Core.Testing;

    /// <summary>
    /// The class representing the HomeRepo element repository.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    [RepositoryFolder("30d5c4e4-58eb-4142-a011-70eea16725e2")]
    public partial class HomeRepo : RepoGenBaseFolder
    {
        static HomeRepo instance = new HomeRepo();
        HomeRepoFolders.FormIntelLParenRRParen_GraphAppFolder _formintellparenrrparen_graph;

        /// <summary>
        /// Gets the singleton class instance representing the HomeRepo element repository.
        /// </summary>
        [RepositoryFolder("30d5c4e4-58eb-4142-a011-70eea16725e2")]
        public static HomeRepo Instance
        {
            get { return instance; }
        }

        /// <summary>
        /// Repository class constructor.
        /// </summary>
        public HomeRepo()
            : base("HomeRepo", "", null, 30000, false, "30d5c4e4-58eb-4142-a011-70eea16725e2", ".\\RepositoryImages\\HomeRepo30d5c4e4.rximgres")
        {
            _formintellparenrrparen_graph = new HomeRepoFolders.FormIntelLParenRRParen_GraphAppFolder(this);
        }

        #region Variables

        #endregion

        /// <summary>
        /// The FormIntelLParenRRParen_Graph folder.
        /// </summary>
        [RepositoryFolder("d1c445d1-4b14-4333-a883-8975a59f0b8a")]
        public virtual HomeRepoFolders.FormIntelLParenRRParen_GraphAppFolder FormIntelLParenRRParen_Graph
        {
            get { return _formintellparenrrparen_graph; }
        }
    }

    /// <summary>
    /// Inner folder classes.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    public partial class HomeRepoFolders
    {
        /// <summary>
        /// The FormIntelLParenRRParen_GraphAppFolder folder.
        /// </summary>
        [RepositoryFolder("d1c445d1-4b14-4333-a883-8975a59f0b8a")]
        public partial class FormIntelLParenRRParen_GraphAppFolder : RepoGenBaseFolder
        {
            RepoItemInfo _selfInfo;
            RepoItemInfo _backbuttonitemInfo;

            /// <summary>
            /// Creates a new FormIntelLParenRRParen_Graph  folder.
            /// </summary>
            public FormIntelLParenRRParen_GraphAppFolder(RepoGenBaseFolder parentFolder) :
                base("FormIntelLParenRRParen_Graph", "/form[@automationid='MainWindow']", parentFolder, 30000, true, "d1c445d1-4b14-4333-a883-8975a59f0b8a", "")
            {
                _selfInfo = new RepoItemInfo(this, "Self", "", 30000, null, "d1c445d1-4b14-4333-a883-8975a59f0b8a");
                _backbuttonitemInfo = new RepoItemInfo(this, "MainMenuItem", "element/element[@automationid='headergrid']/button[@automationid='HomeButton']", 30000, null, "c018a432-53e6-4a86-a827-a0f8a83c7a53");
            }

            /// <summary>
            /// The Self item.
            /// </summary>
            [RepositoryItem("d1c445d1-4b14-4333-a883-8975a59f0b8a")]
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
            [RepositoryItemInfo("d1c445d1-4b14-4333-a883-8975a59f0b8a")]
            public virtual RepoItemInfo SelfInfo
            {
                get
                {
                    return _selfInfo;
                }
            }

            /// <summary>
            /// The MainMenuItem item.
            /// </summary>
            [RepositoryItem("c018a432-53e6-4a86-a827-a0f8a83c7a53")]
            public virtual Ranorex.Button BackButtonItem
            {
                get
                {
                    return _backbuttonitemInfo.CreateAdapter<Ranorex.Button>(true);
                }
            }
        }

    }
}