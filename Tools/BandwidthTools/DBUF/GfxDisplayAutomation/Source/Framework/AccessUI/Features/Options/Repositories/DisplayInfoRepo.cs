namespace Intel.VPG.Display.Automation
{
    using Ranorex.Core.Repository;

    /// <summary>
    /// The class representing the New_Repository element repository.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    [RepositoryFolder("e1fffc0b-3d01-43a8-8d49-0a9b490dbe85")]
    public partial class DisplayInfoRepo : RepoGenBaseFolder
    {
        static DisplayInfoRepo instance = new DisplayInfoRepo();
        DisplayInfoRepoFolders.IntelRGraphicsAppFolder _intelrgraphics;

        /// <summary>
        /// Gets the singleton class instance representing the New_Repository element repository.
        /// </summary>
        [RepositoryFolder("e1fffc0b-3d01-43a8-8d49-0a9b490dbe85")]
        public static DisplayInfoRepo Instance
        {
            get { return instance; }
        }

        /// <summary>
        /// Repository class constructor.
        /// </summary>
        public DisplayInfoRepo()
            : base("DisplayInfoRepo", "", null, 30000, false, "e1fffc0b-3d01-43a8-8d49-0a9b490dbe85", ".\\RepositoryImages\\SelectDisplayInfofffc0b.rximgres")
        {
            _intelrgraphics = new DisplayInfoRepoFolders.IntelRGraphicsAppFolder(this);
        }

        #region Variables

        #endregion

        /// <summary>
        /// The IntelRGraphics folder.
        /// </summary>
        [RepositoryFolder("9516ce46-fd4a-46fb-826a-bb668d446eb1")]
        public virtual DisplayInfoRepoFolders.IntelRGraphicsAppFolder IntelRGraphics
        {
            get { return _intelrgraphics; }
        }
    }

    /// <summary>
    /// Inner folder classes.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    public partial class DisplayInfoRepoFolders
    {
        /// <summary>
        /// The IntelRGraphicsAppFolder folder.
        /// </summary>
        [RepositoryFolder("9516ce46-fd4a-46fb-826a-bb668d446eb1")]
        public partial class IntelRGraphicsAppFolder : RepoGenBaseFolder
        {
            RepoItemInfo _selfInfo;
            RepoItemInfo _comboinfoInfo;

            /// <summary>
            /// Creates a new IntelRGraphics  folder.
            /// </summary>
            public IntelRGraphicsAppFolder(RepoGenBaseFolder parentFolder) :
                base("IntelRGraphics", "/form[@automationid='MainWindow']", parentFolder, 30000, true, "9516ce46-fd4a-46fb-826a-bb668d446eb1", "")
            {
                _selfInfo = new RepoItemInfo(this, "Self", "", 0, null, "9516ce46-fd4a-46fb-826a-bb668d446eb1");
                _comboinfoInfo = new RepoItemInfo(this, "ComboOption", "element/element[@classname='InformationTab']/combobox[@automationid='comboOption']", 30000, null, "bfda3c6f-0c1c-4272-ba15-f2cf8fdd0b88");
            }

            /// <summary>
            /// The Self item.
            /// </summary>
            [RepositoryItem("9516ce46-fd4a-46fb-826a-bb668d446eb1")]
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
            [RepositoryItemInfo("9516ce46-fd4a-46fb-826a-bb668d446eb1")]
            public virtual RepoItemInfo SelfInfo
            {
                get
                {
                    return _selfInfo;
                }
            }

            /// <summary>
            /// The ComboInfo item.
            /// </summary>
            [RepositoryItem("f75d680e-6398-4976-813a-815581a410ed")]
            public virtual Ranorex.ComboBox ComboInfo
            {
                get
                {
                    return _comboinfoInfo.CreateAdapter<Ranorex.ComboBox>(true);
                }
            }

            /// <summary>
            /// The ComboInfo item info.
            /// </summary>
            [RepositoryItemInfo("f75d680e-6398-4976-813a-815581a410ed")]
            public virtual RepoItemInfo ComboInfoInfo
            {
                get
                {
                    return _comboinfoInfo;
                }
            }
        }

    }
}