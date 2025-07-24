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
    /// The class representing the MenuRepo element repository.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    [RepositoryFolder("30d5c4e4-58eb-4142-a011-70eea16725e2")]
    public partial class MenuRepo : RepoGenBaseFolder
    {
        static MenuRepo instance = new MenuRepo();
        MenuRepoFolders.FormIntelLParenRRParen_GraphAppFolder _formintellparenrrparen_graph;

        /// <summary>
        /// Gets the singleton class instance representing the MenuRepo element repository.
        /// </summary>
        [RepositoryFolder("30d5c4e4-58eb-4142-a011-70eea16725e2")]
        public static MenuRepo Instance
        {
            get { return instance; }
        }

        /// <summary>
        /// Repository class constructor.
        /// </summary>
        public MenuRepo()
            : base("MenuRepo", "", null, 30000, false, "30d5c4e4-58eb-4142-a011-70eea16725e2", ".\\RepositoryImages\\MenuRepo30d5c4e4.rximgres")
        {
            _formintellparenrrparen_graph = new MenuRepoFolders.FormIntelLParenRRParen_GraphAppFolder(this);
        }

        #region Variables

        #endregion

        /// <summary>
        /// The FormIntelLParenRRParen_Graph folder.
        /// </summary>
        [RepositoryFolder("d1c445d1-4b14-4333-a883-8975a59f0b8a")]
        public virtual MenuRepoFolders.FormIntelLParenRRParen_GraphAppFolder FormIntelLParenRRParen_Graph
        {
            get { return _formintellparenrrparen_graph; }
        }
    }

    /// <summary>
    /// Inner folder classes.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    public partial class MenuRepoFolders
    {
        /// <summary>
        /// The FormIntelLParenRRParen_GraphAppFolder folder.
        /// </summary>
        [RepositoryFolder("d1c445d1-4b14-4333-a883-8975a59f0b8a")]
        public partial class FormIntelLParenRRParen_GraphAppFolder : RepoGenBaseFolder
        {
            RepoItemInfo _selfInfo;
            RepoItemInfo _mainmenuitemInfo;
            RepoItemInfo _menuitemdisplay_settingsInfo;
            RepoItemInfo _menuitemmultiple_displaysInfo;
            RepoItemInfo _menuItemColor_enhancementInfo;
            RepoItemInfo _menuitemimage_enhancementInfo;
            RepoItemInfo _menuitemgamut_mappingInfo;
            RepoItemInfo _menuitemimage_scalingInfo;
            RepoItemInfo _menuitempreferencesInfo;
            RepoItemInfo _menuitemhot_key_managerInfo;
            RepoItemInfo _menuiteminformation_centerInfo;
            RepoItemInfo _titleBlock;

            /// <summary>
            /// Creates a new FormIntelLParenRRParen_Graph  folder.
            /// </summary>
            public FormIntelLParenRRParen_GraphAppFolder(RepoGenBaseFolder parentFolder) :
                base("FormIntelLParenRRParen_Graph", "/form[@automationid='MainWindow']", parentFolder, 30000, true, "d1c445d1-4b14-4333-a883-8975a59f0b8a", "")
            {
                _selfInfo = new RepoItemInfo(this, "Self", "", 30000, null, "d1c445d1-4b14-4333-a883-8975a59f0b8a");
                _mainmenuitemInfo = new RepoItemInfo(this, "MainMenuItem", "element/element[@automationid='headergrid']/contextmenu/menuitem[@automationid='MenuItem']", 30000, null, "c018a432-53e6-4a86-a827-a0f8a83c7a53");
                _menuitemdisplay_settingsInfo = new RepoItemInfo(this, "MenuItemDisplay_Settings", "form/menuitem[@automationid='MenuItem_0']", 30000, null, "059f168d-2d5f-485a-86d9-71b064138955");
                _menuitemmultiple_displaysInfo = new RepoItemInfo(this, "MenuItemMultiple_Displays", "form/menuitem[@automationid='MenuItem_1']", 30000, null, "fcd329af-7b84-4599-bdd2-d7fd3dac1e3c");
                _menuItemColor_enhancementInfo = new RepoItemInfo(this, "MenuItemColor_Enhancement", "form/menuitem[@automationid='MenuItem_0']", 30000, null, "fcd329af-7b84-4599-bdd2-d7fd3dac1e3c");
                _menuitemimage_enhancementInfo = new RepoItemInfo(this, "MenuItemImage_Enhancement", "form/menuitem[@automationid='MenuItem_1']", 30000, null, "e4c94ac1-f9af-45f5-b3f7-e5aa0197940a");
                _menuitemimage_scalingInfo = new RepoItemInfo(this, "MenuItemImage_Scaling", "form/menuitem[@automationid='MenuItem_2']", 30000, null, "1797696a-6a8f-4ed1-a087-f741919cbf6d");
                _menuitemgamut_mappingInfo = new RepoItemInfo(this, "MenuItemGamut_Mapping", "form/menuitem[@automationid='MenuItem_3']", 30000, null, "e9411f9d-1ee1-48b1-98ec-42d5f07ff28d");
                _menuitemhot_key_managerInfo = new RepoItemInfo(this, "MenuItemHot_Key_Manager", "form/menuitem[@automationid='MenuItem_0']", 30000, null, "7542497b-885f-4cfe-9feb-4bbe5470b62e");
                _menuiteminformation_centerInfo = new RepoItemInfo(this, "MenuItemInformation_Center", "form/menuitem[@automationid='MenuItem_1']", 30000, null, "7542497b-885f-4cfe-9feb-4bbe5470b62e");
                _menuitempreferencesInfo = new RepoItemInfo(this, "MenuItemPreferences", "form/menuitem[@automationid='MenuItem_2']", 30000, null, "7542497b-885f-4cfe-9feb-4bbe5470b62e");
                _titleBlock = new RepoItemInfo(this, "TitleBlock", "element/element[@automationid='headergrid']/text[@automationid='TitleBlock']", 30000, null, "3b50c3da-c593-4a43-8ca8-540f6d301169");


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
            public virtual Ranorex.MenuItem MainMenuItem
            {
                get
                {
                    return _mainmenuitemInfo.CreateAdapter<Ranorex.MenuItem>(true);
                }
            }
            /// <summary>
            /// The TitleBlock item.
            /// </summary>
            [RepositoryItem("c018a432-53e6-4a86-a827-a0f8a83c7a53")]
            public virtual Ranorex.Text TitleBlock
            {
                get
                {
                    return _titleBlock.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The MainMenuItem item info.
            /// </summary>
            [RepositoryItemInfo("c018a432-53e6-4a86-a827-a0f8a83c7a53")]
            public virtual RepoItemInfo MainMenuItemInfo
            {
                get
                {
                    return _mainmenuitemInfo;
                }
            }

            /// <summary>
            /// The MenuItemDisplay_Settings item.
            /// </summary>
            [RepositoryItem("059f168d-2d5f-485a-86d9-71b064138955")]
            public virtual Ranorex.MenuItem MenuItemDisplay_Settings
            {
                get
                {
                    return _menuitemdisplay_settingsInfo.CreateAdapter<Ranorex.MenuItem>(true);
                }
            }

            /// <summary>
            /// The MenuItemDisplay_Settings item info.
            /// </summary>
            [RepositoryItemInfo("059f168d-2d5f-485a-86d9-71b064138955")]
            public virtual RepoItemInfo MenuItemDisplay_SettingsInfo
            {
                get
                {
                    return _menuitemdisplay_settingsInfo;
                }
            }

            /// <summary>
            /// The MenuItemMultiple_Displays item.
            /// </summary>
            [RepositoryItem("fcd329af-7b84-4599-bdd2-d7fd3dac1e3c")]
            public virtual Ranorex.MenuItem MenuItemMultiple_Displays
            {
                get
                {
                    return _menuitemmultiple_displaysInfo.CreateAdapter<Ranorex.MenuItem>(true);
                }
            }

            /// <summary>
            /// The MenuItemMultiple_Displays item info.
            /// </summary>
            [RepositoryItemInfo("fcd329af-7b84-4599-bdd2-d7fd3dac1e3c")]
            public virtual RepoItemInfo MenuItemMultiple_DisplaysInfo
            {
                get
                {
                    return _menuitemmultiple_displaysInfo;
                }
            }
            /// <summary>
            /// The MenuItemMultiple_Displays item.
            /// </summary>
            [RepositoryItem("fcd329af-7b84-4599-bdd2-d7fd3dac1e3c")]
            public virtual Ranorex.MenuItem MenuItemColor_Enhancement
            {
                get
                {
                    return _menuItemColor_enhancementInfo.CreateAdapter<Ranorex.MenuItem>(true);
                }
            }

            /// <summary>
            /// The MenuItemMultiple_Displays item info.
            /// </summary>
            [RepositoryItemInfo("fcd329af-7b84-4599-bdd2-d7fd3dac1e3c")]
            public virtual RepoItemInfo MenuItemColor_EnhancementInfo
            {
                get
                {
                    return _menuItemColor_enhancementInfo;
                }
            }
            /// <summary>
            /// The MenuItemImage_Enhancement item.
            /// </summary>
            [RepositoryItem("e4c94ac1-f9af-45f5-b3f7-e5aa0197940a")]
            public virtual Ranorex.MenuItem MenuItemImage_Enhancement
            {
                get
                {
                    return _menuitemimage_enhancementInfo.CreateAdapter<Ranorex.MenuItem>(true);
                }
            }

            /// <summary>
            /// The MenuItemImage_Enhancement item info.
            /// </summary>
            [RepositoryItemInfo("e4c94ac1-f9af-45f5-b3f7-e5aa0197940a")]
            public virtual RepoItemInfo MenuItemImage_EnhancementInfo
            {
                get
                {
                    return _menuitemimage_enhancementInfo;
                }
            }

            /// <summary>
            /// The MenuItemGamut_Mapping item.
            /// </summary>
            [RepositoryItem("e9411f9d-1ee1-48b1-98ec-42d5f07ff28d")]
            public virtual Ranorex.MenuItem MenuItemGamut_Mapping
            {
                get
                {
                    return _menuitemgamut_mappingInfo.CreateAdapter<Ranorex.MenuItem>(true);
                }
            }

            /// <summary>
            /// The MenuItemGamut_Mapping item info.
            /// </summary>
            [RepositoryItemInfo("e9411f9d-1ee1-48b1-98ec-42d5f07ff28d")]
            public virtual RepoItemInfo MenuItemGamut_MappingInfo
            {
                get
                {
                    return _menuitemgamut_mappingInfo;
                }
            }

            /// <summary>
            /// The MenuItemImage_Scaling item.
            /// </summary>
            [RepositoryItem("1797696a-6a8f-4ed1-a087-f741919cbf6d")]
            public virtual Ranorex.MenuItem MenuItemImage_Scaling
            {
                get
                {
                    return _menuitemimage_scalingInfo.CreateAdapter<Ranorex.MenuItem>(true);
                }
            }

            /// <summary>
            /// The MenuItemImage_Scaling item info.
            /// </summary>
            [RepositoryItemInfo("1797696a-6a8f-4ed1-a087-f741919cbf6d")]
            public virtual RepoItemInfo MenuItemImage_ScalingInfo
            {
                get
                {
                    return _menuitemimage_scalingInfo;
                }
            }

            /// <summary>
            /// The MenuItemPreferences item.
            /// </summary>
            [RepositoryItem("7542497b-885f-4cfe-9feb-4bbe5470b62e")]
            public virtual Ranorex.MenuItem MenuItemPreferences
            {
                get
                {
                    return _menuitempreferencesInfo.CreateAdapter<Ranorex.MenuItem>(true);
                }
            }

            /// <summary>
            /// The MenuItemPreferences item info.
            /// </summary>
            [RepositoryItemInfo("7542497b-885f-4cfe-9feb-4bbe5470b62e")]
            public virtual RepoItemInfo MenuItemPreferencesInfo
            {
                get
                {
                    return _menuitempreferencesInfo;
                }
            }

            /// <summary>
            /// The MenuItemHot_Key_Manager item.
            /// </summary>
            [RepositoryItem("fdb7fe1a-1e8d-4a5a-82b7-e01089f4e27e")]
            public virtual Ranorex.MenuItem MenuItemHot_Key_Manager
            {
                get
                {
                    return _menuitemhot_key_managerInfo.CreateAdapter<Ranorex.MenuItem>(true);
                }
            }

            /// <summary>
            /// The MenuItemHot_Key_Manager item info.
            /// </summary>
            [RepositoryItemInfo("fdb7fe1a-1e8d-4a5a-82b7-e01089f4e27e")]
            public virtual RepoItemInfo MenuItemHot_Key_ManagerInfo
            {
                get
                {
                    return _menuitemhot_key_managerInfo;
                }
            }

            /// <summary>
            /// The MenuItemInformation_Center item.
            /// </summary>
            [RepositoryItem("5e335e06-2b86-4407-a9c3-00c79314a72a")]
            public virtual Ranorex.MenuItem MenuItemInformation_Center
            {
                get
                {
                    return _menuiteminformation_centerInfo.CreateAdapter<Ranorex.MenuItem>(true);
                }
            }

            /// <summary>
            /// The MenuItemInformation_Center item info.
            /// </summary>
            [RepositoryItemInfo("5e335e06-2b86-4407-a9c3-00c79314a72a")]
            public virtual RepoItemInfo MenuItemInformation_CenterInfo
            {
                get
                {
                    return _menuiteminformation_centerInfo;
                }
            }
            public virtual bool MenuItemGamut_Mapping_Visible
            {
                get
                {
                    return this.MenuItem_Visible("Gamut Mapping");
                }
            }
            public virtual bool MenuItem_Visible(string argMenuItem)
            {

                IList<Element> mainMenuItem = MenuRepo.Instance.FormIntelLParenRRParen_Graph.Self.Find(@"element/element[@automationid='headergrid']/contextmenu/*/menuitem");

                return (null != mainMenuItem.Where(e => (null != e) && e.ToString().Contains(argMenuItem)).FirstOrDefault());
            }
        }

    }
}