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
    /// The class representing the TilesRepo element repository.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    [RepositoryFolder("3a1c1270-e7c3-45cb-99a2-dae72e9ba606")]
    public partial class TilesRepo : RepoGenBaseFolder
    {
        static TilesRepo instance = new TilesRepo();
        TilesRepoFolders.FormIntelLParenRRParen_GraphAppFolder _formintellparenrrparen_graph;

        /// <summary>
        /// Gets the singleton class instance representing the TilesRepo element repository.
        /// </summary>
        [RepositoryFolder("3a1c1270-e7c3-45cb-99a2-dae72e9ba606")]
        public static TilesRepo Instance
        {
            get { return instance; }
        }

        /// <summary>
        /// Repository class constructor.
        /// </summary>
        public TilesRepo()
            : base("TilesRepo", "", null, 30000, false, "3a1c1270-e7c3-45cb-99a2-dae72e9ba606", ".\\RepositoryImages\\TilesRepo3a1c1270.rximgres")
        {
            _formintellparenrrparen_graph = new TilesRepoFolders.FormIntelLParenRRParen_GraphAppFolder(this);
        }

        #region Variables

        #endregion

        /// <summary>
        /// The FormIntelLParenRRParen_Graph folder.
        /// </summary>
        [RepositoryFolder("1e0de70c-ea53-4f52-bc30-dc410146e807")]
        public virtual TilesRepoFolders.FormIntelLParenRRParen_GraphAppFolder FormIntelLParenRRParen_Graph
        {
            get { return _formintellparenrrparen_graph; }
        }
    }

    /// <summary>
    /// Inner folder classes.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    public partial class TilesRepoFolders
    {
        /// <summary>
        /// The FormIntelLParenRRParen_GraphAppFolder folder.
        /// </summary>
        [RepositoryFolder("1e0de70c-ea53-4f52-bc30-dc410146e807")]
        public partial class FormIntelLParenRRParen_GraphAppFolder : RepoGenBaseFolder
        {
            RepoItemInfo _selfInfo;
            RepoItemInfo _displayInfo;
            RepoItemInfo _videoInfo;
            RepoItemInfo _threedInfo;
            RepoItemInfo _powerInfo;
            RepoItemInfo _optionsInfo;
            RepoItemInfo _supportInfo;

            /// <summary>
            /// Creates a new FormIntelLParenRRParen_Graph  folder.
            /// </summary>
            public FormIntelLParenRRParen_GraphAppFolder(RepoGenBaseFolder parentFolder) :
                base("FormIntelLParenRRParen_Graph", "/form[@automationid='MainWindow']", parentFolder, 30000, true, "1e0de70c-ea53-4f52-bc30-dc410146e807", "")
            {
                _selfInfo = new RepoItemInfo(this, "Self", "", 30000, null, "1e0de70c-ea53-4f52-bc30-dc410146e807");
                _displayInfo = new RepoItemInfo(this, "Display", "element/element[@automationid='IntelTilesContainer']/element[@automationid='Tile_0']/button[@classname='Button']", 30000, null, "8af15951-3f45-4e28-b6e6-e62fde1b9a9c");
                _videoInfo = new RepoItemInfo(this, "Video", "element/element[@automationid='IntelTilesContainer']/element[@automationid='Tile_1']/button[@classname='Button']", 30000, null, "d5b02375-df7f-4368-81b6-8f980133812d");
                _threedInfo = new RepoItemInfo(this, "ThreeD", "element/element[@automationid='IntelTilesContainer']/element[@automationid='Tile_2']/button[@classname='Button']", 30000, null, "c5bf6abf-c749-4711-b36a-71af210ce7c0");
                _powerInfo = new RepoItemInfo(this, "Power", "element/element[@automationid='IntelTilesContainer']/element[@automationid='Tile_3']/button[@classname='Button']", 30000, null, "0fd30881-8ff8-4128-ae0e-8a937da71a9e");
                _optionsInfo = new RepoItemInfo(this, "Options", "element/element[@automationid='IntelTilesContainer']/element[@automationid='Tile_4']/button[@classname='Button']", 30000, null, "0bde26ff-5def-4b4e-859e-ae4dfa0ab1a7");
                _supportInfo = new RepoItemInfo(this, "Support", "element/element[@automationid='IntelTilesContainer']/element[@automationid='Tile_5']/button[@classname='Button']", 30000, null, "02026a23-8706-4b67-bb31-edd9756fc566");
            }

            /// <summary>
            /// The Self item.
            /// </summary>
            [RepositoryItem("1e0de70c-ea53-4f52-bc30-dc410146e807")]
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
            [RepositoryItemInfo("1e0de70c-ea53-4f52-bc30-dc410146e807")]
            public virtual RepoItemInfo SelfInfo
            {
                get
                {
                    return _selfInfo;
                }
            }

            /// <summary>
            /// The Display item.
            /// </summary>
            [RepositoryItem("8af15951-3f45-4e28-b6e6-e62fde1b9a9c")]
            public virtual Ranorex.Button Display
            {
                get
                {
                    return _displayInfo.CreateAdapter<Ranorex.Button>(true);
                }
            }

            /// <summary>
            /// The Display item info.
            /// </summary>
            [RepositoryItemInfo("8af15951-3f45-4e28-b6e6-e62fde1b9a9c")]
            public virtual RepoItemInfo DisplayInfo
            {
                get
                {
                    return _displayInfo;
                }
            }

            /// <summary>
            /// The Video item.
            /// </summary>
            [RepositoryItem("d5b02375-df7f-4368-81b6-8f980133812d")]
            public virtual Ranorex.Button Video
            {
                get
                {
                    return _videoInfo.CreateAdapter<Ranorex.Button>(true);
                }
            }

            /// <summary>
            /// The Video item info.
            /// </summary>
            [RepositoryItemInfo("d5b02375-df7f-4368-81b6-8f980133812d")]
            public virtual RepoItemInfo VideoInfo
            {
                get
                {
                    return _videoInfo;
                }
            }

            /// <summary>
            /// The ThreeD item.
            /// </summary>
            [RepositoryItem("c5bf6abf-c749-4711-b36a-71af210ce7c0")]
            public virtual Ranorex.Button ThreeD
            {
                get
                {
                    return _threedInfo.CreateAdapter<Ranorex.Button>(true);
                }
            }

            /// <summary>
            /// The ThreeD item info.
            /// </summary>
            [RepositoryItemInfo("c5bf6abf-c749-4711-b36a-71af210ce7c0")]
            public virtual RepoItemInfo ThreeDInfo
            {
                get
                {
                    return _threedInfo;
                }
            }

            /// <summary>
            /// The Power item.
            /// </summary>
            [RepositoryItem("0fd30881-8ff8-4128-ae0e-8a937da71a9e")]
            public virtual Ranorex.Button Power
            {
                get
                {
                    return _powerInfo.CreateAdapter<Ranorex.Button>(true);
                }
            }

            /// <summary>
            /// The Power item info.
            /// </summary>
            [RepositoryItemInfo("0fd30881-8ff8-4128-ae0e-8a937da71a9e")]
            public virtual RepoItemInfo PowerInfo
            {
                get
                {
                    return _powerInfo;
                }
            }

            /// <summary>
            /// The Options item.
            /// </summary>
            [RepositoryItem("0bde26ff-5def-4b4e-859e-ae4dfa0ab1a7")]
            public virtual Ranorex.Button Options
            {
                get
                {
                    return _optionsInfo.CreateAdapter<Ranorex.Button>(true);
                }
            }

            /// <summary>
            /// The Options item info.
            /// </summary>
            [RepositoryItemInfo("0bde26ff-5def-4b4e-859e-ae4dfa0ab1a7")]
            public virtual RepoItemInfo OptionsInfo
            {
                get
                {
                    return _optionsInfo;
                }
            }

            /// <summary>
            /// The Support item.
            /// </summary>
            [RepositoryItem("02026a23-8706-4b67-bb31-edd9756fc566")]
            public virtual Ranorex.Button Support
            {
                get
                {
                    return _supportInfo.CreateAdapter<Ranorex.Button>(true);
                }
            }

            /// <summary>
            /// The Support item info.
            /// </summary>
            [RepositoryItemInfo("02026a23-8706-4b67-bb31-edd9756fc566")]
            public virtual RepoItemInfo SupportInfo
            {
                get
                {
                    return _supportInfo;
                }
            }
        }

    }
}