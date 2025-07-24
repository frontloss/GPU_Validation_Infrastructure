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
    /// The class representing the AppBarRepo element repository.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    [RepositoryFolder("194294a7-82a2-4dcd-9644-32dbde1d90fa")]
    public partial class AppBarRepo : RepoGenBaseFolder
    {
        static AppBarRepo instance = new AppBarRepo();
        AppBarRepoFolders.FormIntelR_Graphics_and_MediAppFolder _formintelr_graphics_and_medi;

        /// <summary>
        /// Gets the singleton class instance representing the AppBarRepo element repository.
        /// </summary>
        [RepositoryFolder("194294a7-82a2-4dcd-9644-32dbde1d90fa")]
        public static AppBarRepo Instance
        {
            get { return instance; }
        }

        /// <summary>
        /// Repository class constructor.
        /// </summary>
        public AppBarRepo()
            : base("AppBarRepo", "", null, 30000, false, "194294a7-82a2-4dcd-9644-32dbde1d90fa", ".\\RepositoryImages\\AppBarRepo194294a7.rximgres")
        {
            _formintelr_graphics_and_medi = new AppBarRepoFolders.FormIntelR_Graphics_and_MediAppFolder(this);
        }

        #region Variables

        #endregion

        /// <summary>
        /// The FormIntelR_Graphics_and_Medi folder.
        /// </summary>
        [RepositoryFolder("390031ee-553c-4a63-9881-d56dae9c43e1")]
        public virtual AppBarRepoFolders.FormIntelR_Graphics_and_MediAppFolder FormIntelR_Graphics_and_Medi
        {
            get { return _formintelr_graphics_and_medi; }
        }
    }

    /// <summary>
    /// Inner folder classes.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    public partial class AppBarRepoFolders
    {
        /// <summary>
        /// The FormIntelR_Graphics_and_MediAppFolder folder.
        /// </summary>
        [RepositoryFolder("390031ee-553c-4a63-9881-d56dae9c43e1")]
        public partial class FormIntelR_Graphics_and_MediAppFolder : RepoGenBaseFolder
        {
            RepoItemInfo _selfInfo;
            RepoItemInfo _appbarlistInfo;
            RepoItemInfo _buttonrestore_defaultsInfo;
            RepoItemInfo _buttoncancelInfo;
            RepoItemInfo _buttonapplyInfo;
            RepoItemInfo _save_profileInfo;
            RepoItemInfo _rename_profileInfo;
            RepoItemInfo _delete_profileInfo;
            RepoItemInfo _saveInfo;

            /// <summary>
            /// Creates a new FormIntelR_Graphics_and_Medi  folder.
            /// </summary>
            public FormIntelR_Graphics_and_MediAppFolder(RepoGenBaseFolder parentFolder) :
                base("FormIntelR_Graphics_and_Medi", "/form[@automationid='MainWindow']", parentFolder, 30000, true, "390031ee-553c-4a63-9881-d56dae9c43e1", "")
            {
                _selfInfo = new RepoItemInfo(this, "Self", "", 30000, null, "390031ee-553c-4a63-9881-d56dae9c43e1");
                _appbarlistInfo = new RepoItemInfo(this, "AppBarList", "element/element[@automationid='appBar']", 30000, null, "012a63d6-800e-402b-9ab1-510de2c5d8b0");
                _buttonrestore_defaultsInfo = new RepoItemInfo(this, "ButtonRestore_Defaults", "element/element[@automationid='appBar']/*/button[@automationid='AppBarButton_Restore_Defaults']", 30000, null, "bd60fa1d-cb75-48c4-8f5e-8d8ac8bdaf0d");
                _buttoncancelInfo = new RepoItemInfo(this, "ButtonCancel", "element/element[@automationid='appBar']/*/button[@automationid='AppBarButton_Cancel']", 30000, null, "15dc387d-7388-451a-a2fc-7a1c0900753c");
                _buttonapplyInfo = new RepoItemInfo(this, "ButtonApply", "element/element[@automationid='appBar']/*/button[@automationid='AppBarButton_Apply']", 30000, null, "cb26e037-6adb-410b-b337-269299499500");
                _save_profileInfo = new RepoItemInfo(this, "Save_Profile", "element/element[@automationid='appBar']/*/button[@automationid='AppBarButton_Save']", 30000, null, "a126117b-7e83-4ac4-a5fe-76899895a6d9");
                _rename_profileInfo = new RepoItemInfo(this, "Rename_Profile", "element/element[@automationid='appBar']/*/button[@automationid='AppBarButton_Rename']", 30000, null, "d3ec8191-6955-4967-8820-c97740553341");
                _delete_profileInfo = new RepoItemInfo(this, "Delete_Profile", "element/element[@automationid='appBar']/*/button[@automationid='AppBarButton_Delete']", 30000, null, "a3457d16-0785-477e-9033-2c6b3342d81d");
                _saveInfo = new RepoItemInfo(this, "Save", "element/element[@automationid='appBar']/element/button[@automationid='AppBarButton_Save_Report']", 30000, null, "df2e75c8-84f1-4ca7-a8ac-312584dc5cfb");
            }

            /// <summary>
            /// The Self item.
            /// </summary>
            [RepositoryItem("390031ee-553c-4a63-9881-d56dae9c43e1")]
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
            [RepositoryItemInfo("390031ee-553c-4a63-9881-d56dae9c43e1")]
            public virtual RepoItemInfo SelfInfo
            {
                get
                {
                    return _selfInfo;
                }
            }

            /// <summary>
            /// The AppBarList item.
            /// </summary>
            [RepositoryItem("012a63d6-800e-402b-9ab1-510de2c5d8b0")]
            public virtual Ranorex.Unknown AppBarList
            {
                get
                {
                    return _appbarlistInfo.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The AppBarList item info.
            /// </summary>
            [RepositoryItemInfo("012a63d6-800e-402b-9ab1-510de2c5d8b0")]
            public virtual RepoItemInfo AppBarListInfo
            {
                get
                {
                    return _appbarlistInfo;
                }
            }

            /// <summary>
            /// The ButtonRestore_Defaults item.
            /// </summary>
            [RepositoryItem("bd60fa1d-cb75-48c4-8f5e-8d8ac8bdaf0d")]
            public virtual Ranorex.Button ButtonRestore_Defaults
            {
                get
                {
                    return _buttonrestore_defaultsInfo.CreateAdapter<Ranorex.Button>(true);
                }
            }

            /// <summary>
            /// The ButtonRestore_Defaults item info.
            /// </summary>
            [RepositoryItemInfo("bd60fa1d-cb75-48c4-8f5e-8d8ac8bdaf0d")]
            public virtual RepoItemInfo ButtonRestore_DefaultsInfo
            {
                get
                {
                    return _buttonrestore_defaultsInfo;
                }
            }

            /// <summary>
            /// The ButtonCancel item.
            /// </summary>
            [RepositoryItem("15dc387d-7388-451a-a2fc-7a1c0900753c")]
            public virtual Ranorex.Button ButtonCancel
            {
                get
                {
                    return _buttoncancelInfo.CreateAdapter<Ranorex.Button>(true);
                }
            }

            /// <summary>
            /// The ButtonCancel item info.
            /// </summary>
            [RepositoryItemInfo("15dc387d-7388-451a-a2fc-7a1c0900753c")]
            public virtual RepoItemInfo ButtonCancelInfo
            {
                get
                {
                    return _buttoncancelInfo;
                }
            }

            /// <summary>
            /// The ButtonApply item.
            /// </summary>
            [RepositoryItem("cb26e037-6adb-410b-b337-269299499500")]
            public virtual Ranorex.Button ButtonApply
            {
                get
                {
                    return _buttonapplyInfo.CreateAdapter<Ranorex.Button>(true);
                }
            }

            /// <summary>
            /// The ButtonApply item info.
            /// </summary>
            [RepositoryItemInfo("cb26e037-6adb-410b-b337-269299499500")]
            public virtual RepoItemInfo ButtonApplyInfo
            {
                get
                {
                    return _buttonapplyInfo;
                }
            }

            /// <summary>
            /// The Save_Profile item.
            /// </summary>
            [RepositoryItem("a126117b-7e83-4ac4-a5fe-76899895a6d9")]
            public virtual Ranorex.Button Save_Profile
            {
                get
                {
                    return _save_profileInfo.CreateAdapter<Ranorex.Button>(true);
                }
            }

            /// <summary>
            /// The Save_Profile item info.
            /// </summary>
            [RepositoryItemInfo("a126117b-7e83-4ac4-a5fe-76899895a6d9")]
            public virtual RepoItemInfo Save_ProfileInfo
            {
                get
                {
                    return _save_profileInfo;
                }
            }

            /// <summary>
            /// The Rename_Profile item.
            /// </summary>
            [RepositoryItem("d3ec8191-6955-4967-8820-c97740553341")]
            public virtual Ranorex.Button Rename_Profile
            {
                get
                {
                    return _rename_profileInfo.CreateAdapter<Ranorex.Button>(true);
                }
            }

            /// <summary>
            /// The Rename_Profile item info.
            /// </summary>
            [RepositoryItemInfo("d3ec8191-6955-4967-8820-c97740553341")]
            public virtual RepoItemInfo Rename_ProfileInfo
            {
                get
                {
                    return _rename_profileInfo;
                }
            }

            /// <summary>
            /// The Delete_Profile item.
            /// </summary>
            [RepositoryItem("a3457d16-0785-477e-9033-2c6b3342d81d")]
            public virtual Ranorex.Button Delete_Profile
            {
                get
                {
                    return _delete_profileInfo.CreateAdapter<Ranorex.Button>(true);
                }
            }

            /// <summary>
            /// The Delete_Profile item info.
            /// </summary>
            [RepositoryItemInfo("a3457d16-0785-477e-9033-2c6b3342d81d")]
            public virtual RepoItemInfo Delete_ProfileInfo
            {
                get
                {
                    return _delete_profileInfo;
                }
            }
            /// <summary>
            /// The Save item.
            /// </summary>
            [RepositoryItem("df2e75c8-84f1-4ca7-a8ac-312584dc5cfb")]
            public virtual Ranorex.Button Save
            {
                get
                {
                    return _saveInfo.CreateAdapter<Ranorex.Button>(true);
                }
            }
        }

    }
}