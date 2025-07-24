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
    /// The class representing the MultipleDisplaysRepo element repository.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    [RepositoryFolder("b3ef79f8-7c5a-4cf8-a745-23a6d061add9")]
    public partial class MultipleDisplaysRepo : RepoGenBaseFolder
    {
        static MultipleDisplaysRepo instance = new MultipleDisplaysRepo();
        MultipleDisplaysRepoFolders.FormIntelR_Graphics_and_MediAppFolder _formintelr_graphics_and_medi;

        /// <summary>
        /// Gets the singleton class instance representing the MultipleDisplaysRepo element repository.
        /// </summary>
        [RepositoryFolder("b3ef79f8-7c5a-4cf8-a745-23a6d061add9")]
        public static MultipleDisplaysRepo Instance
        {
            get { return instance; }
        }

        /// <summary>
        /// Repository class constructor.
        /// </summary>
        public MultipleDisplaysRepo()
            : base("MultipleDisplaysRepo", "", null, 30000, false, "b3ef79f8-7c5a-4cf8-a745-23a6d061add9", ".\\RepositoryImages\\MultipleDisplaysRepob3ef79f8.rximgres")
        {
            _formintelr_graphics_and_medi = new MultipleDisplaysRepoFolders.FormIntelR_Graphics_and_MediAppFolder(this);
        }

        #region Variables

        #endregion

        /// <summary>
        /// The FormIntelR_Graphics_and_Medi folder.
        /// </summary>
        [RepositoryFolder("4179543e-133d-4b70-b944-eea140cacbfc")]
        public virtual MultipleDisplaysRepoFolders.FormIntelR_Graphics_and_MediAppFolder FormIntelR_Graphics_and_Medi
        {
            get { return _formintelr_graphics_and_medi; }
        }
    }

    /// <summary>
    /// Inner folder classes.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    public partial class MultipleDisplaysRepoFolders
    {
        /// <summary>
        /// The FormIntelR_Graphics_and_MediAppFolder folder.
        /// </summary>
        [RepositoryFolder("4179543e-133d-4b70-b944-eea140cacbfc")]
        public partial class FormIntelR_Graphics_and_MediAppFolder : RepoGenBaseFolder
        {
            RepoItemInfo _selfInfo;
            RepoItemInfo _modeitemlistInfo;
            RepoItemInfo _comboboxcomboboxselectopmodeInfo;

            /// <summary>
            /// Creates a new FormIntelR_Graphics_and_Medi  folder.
            /// </summary>
            public FormIntelR_Graphics_and_MediAppFolder(RepoGenBaseFolder parentFolder) :
                base("FormIntelR_Graphics_and_Medi", "/form[@automationid='MainWindow']", parentFolder, 30000, true, "4179543e-133d-4b70-b944-eea140cacbfc", "")
            {
                _selfInfo = new RepoItemInfo(this, "Self", "", 30000, null, "4179543e-133d-4b70-b944-eea140cacbfc");
                _modeitemlistInfo = new RepoItemInfo(this, "ModeItemList", "element/element[@classname='MultipleDisplays']/element[@automationid='opModeList']", 30000, null, "ba9b1262-c0c4-4c11-9a7a-30bb7d4a8ea6");
                _comboboxcomboboxselectopmodeInfo = new RepoItemInfo(this, "ComboBoxComboBoxSelectOpMode", "element/element[@classname='MultipleDisplays']/combobox[@automationid='comboBoxSelectOpMode']", 30000, null, "0fcb7db3-f376-4439-9484-b41e8a0db5b8");
            }

            /// <summary>
            /// The Self item.
            /// </summary>
            [RepositoryItem("4179543e-133d-4b70-b944-eea140cacbfc")]
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
            [RepositoryItemInfo("4179543e-133d-4b70-b944-eea140cacbfc")]
            public virtual RepoItemInfo SelfInfo
            {
                get
                {
                    return _selfInfo;
                }
            }

            /// <summary>
            /// The ModeItemList item.
            /// </summary>
            [RepositoryItem("ba9b1262-c0c4-4c11-9a7a-30bb7d4a8ea6")]
            public virtual Ranorex.Unknown ModeItemList
            {
                get
                {
                    return _modeitemlistInfo.CreateAdapter<Ranorex.Unknown>(true);
                }
            }

            /// <summary>
            /// The ModeItemList item info.
            /// </summary>
            [RepositoryItemInfo("ba9b1262-c0c4-4c11-9a7a-30bb7d4a8ea6")]
            public virtual RepoItemInfo ModeItemListInfo
            {
                get
                {
                    return _modeitemlistInfo;
                }
            }

            /// <summary>
            /// The ComboBoxComboBoxSelectOpMode item.
            /// </summary>
            [RepositoryItem("0fcb7db3-f376-4439-9484-b41e8a0db5b8")]
            public virtual Ranorex.ComboBox ComboBoxComboBoxSelectOpMode
            {
                get
                {
                    try
                    {
                        return _comboboxcomboboxselectopmodeInfo.CreateAdapter<Ranorex.ComboBox>(true);
                    }
                    catch
                    {
                        return null;
                    }
                }
            }

            /// <summary>
            /// The ComboBoxComboBoxSelectOpMode item info.
            /// </summary>
            [RepositoryItemInfo("0fcb7db3-f376-4439-9484-b41e8a0db5b8")]
            public virtual RepoItemInfo ComboBoxComboBoxSelectOpModeInfo
            {
                get
                {
                    return _comboboxcomboboxselectopmodeInfo;
                }
            }
        }

    }
}