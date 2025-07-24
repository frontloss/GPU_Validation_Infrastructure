namespace Intel.VPG.Display.Automation
{
    using Ranorex.Core.Repository;
    /// <summary>
    /// The class representing the OptionalDisplayInfoRepo element repository.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    [RepositoryFolder("e1fffc0b-3d01-43a8-8d49-0a9b490dbe85")]
    public partial class OptionalDisplayInfoRepo : RepoGenBaseFolder
    {
        static OptionalDisplayInfoRepo instance = new OptionalDisplayInfoRepo();
        OptionalDisplayInfoRepoFolders.IntelRGraphicsControlPanelAppFolder _intelrgraphicscontrolpanel;

        /// <summary>
        /// Gets the singleton class instance representing the OptionalDisplayInfoRepo element repository.
        /// </summary>
        [RepositoryFolder("080251b0-865c-4a60-968d-69da01ad8281")]
        public static OptionalDisplayInfoRepo Instance
        {
            get { return instance; }
        }

        /// <summary>
        /// Repository class constructor.
        /// </summary>
        public OptionalDisplayInfoRepo()
            : base("OptionalDisplayInfoRepo", "", null, 30000, false, "080251b0-865c-4a60-968d-69da01ad8281", ".\\RepositoryImages\\NewRepository080251b0.rximgres")
        {
            _intelrgraphicscontrolpanel = new OptionalDisplayInfoRepoFolders.IntelRGraphicsControlPanelAppFolder(this);
        }

        #region Variables

        #endregion

        /// <summary>
        /// The IntelRGraphicsControlPanel folder.
        /// </summary>
        [RepositoryFolder("c06120f1-3bf2-4950-a7c5-405a9b494029")]
        public virtual OptionalDisplayInfoRepoFolders.IntelRGraphicsControlPanelAppFolder IntelRGraphicsControlPanel
        {
            get { return _intelrgraphicscontrolpanel; }
        }

    }

    /// <summary>
    /// Inner folder classes.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    public partial class OptionalDisplayInfoRepoFolders
    {
        /// <summary>
        /// The IntelRGraphicsControlPanelAppFolder folder.
        /// </summary>
        [RepositoryFolder("c06120f1-3bf2-4950-a7c5-405a9b494029")]
        public partial class IntelRGraphicsControlPanelAppFolder : RepoGenBaseFolder
        {
            RepoItemInfo _selfInfo;
            RepoItemInfo _connectortypeInfo;
            RepoItemInfo _devicetypeInfo;

            /// <summary>
            /// Creates a new IntelRGraphicsControlPanel  folder.
            /// </summary>
            public IntelRGraphicsControlPanelAppFolder(RepoGenBaseFolder parentFolder) :
                base("IntelRGraphicsControlPanel", "/form[@automationid='MainWindow']", parentFolder, 30000, true, "c06120f1-3bf2-4950-a7c5-405a9b494029", "")
            {
                _selfInfo = new RepoItemInfo(this, "Self", "", 0, null, "c06120f1-3bf2-4950-a7c5-405a9b494029");
                _connectortypeInfo = new RepoItemInfo(this, "ConnectorType", "element/element[@classname='InformationTab']/text[@automationid='lbDevConnectorTypeVal']", 30000, null, "94521b80-4d7e-4445-b349-811580f7831c");
                _devicetypeInfo = new RepoItemInfo(this, "DeviceType", "element/element[@classname='InformationTab']/text[@automationid='lbDevDeviceTypeVal']", 30000, null, "62a8f738-5370-46cd-b071-a1eb9dc8feb0");
            }

            /// <summary>
            /// The Self item.
            /// </summary>
            [RepositoryItem("c06120f1-3bf2-4950-a7c5-405a9b494029")]
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
            [RepositoryItemInfo("c06120f1-3bf2-4950-a7c5-405a9b494029")]
            public virtual RepoItemInfo SelfInfo
            {
                get
                {
                    return _selfInfo;
                }
            }

            /// <summary>
            /// The HDMI item.
            /// </summary>
            [RepositoryItem("94521b80-4d7e-4445-b349-811580f7831c")]
            public virtual Ranorex.Text ConnectorType
            {
                get
                {
                    return _connectortypeInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The HDMI item info.
            /// </summary>
            [RepositoryItemInfo("94521b80-4d7e-4445-b349-811580f7831c")]
            public virtual RepoItemInfo ConnectorTypeInfo
            {
                get
                {
                    return _connectortypeInfo;
                }
            }

            /// <summary>
            /// The DigitalTelevision item.
            /// </summary>
            [RepositoryItem("62a8f738-5370-46cd-b071-a1eb9dc8feb0")]
            public virtual Ranorex.Text DeviceType
            {
                get
                {
                    return _devicetypeInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The DigitalTelevision item info.
            /// </summary>
            [RepositoryItemInfo("62a8f738-5370-46cd-b071-a1eb9dc8feb0")]
            public virtual RepoItemInfo DeviceTypeInfo
            {
                get
                {
                    return _devicetypeInfo;
                }
            }
        }

    }
}