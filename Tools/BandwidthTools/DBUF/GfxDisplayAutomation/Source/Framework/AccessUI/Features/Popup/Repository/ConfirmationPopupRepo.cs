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
    /// The class representing the ConfirmationPopupRepo element repository.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    [RepositoryFolder("08dad510-532e-4244-ac48-9c4e04234756")]
    public partial class ConfirmationPopupRepo : RepoGenBaseFolder
    {
        static ConfirmationPopupRepo instance = new ConfirmationPopupRepo();
        ConfirmationPopupRepoFolders.Form__IntelR_Graphics_and_MeAppFolder _form__intelr_graphics_and_me;

        /// <summary>
        /// Gets the singleton class instance representing the ConfirmationPopupRepo element repository.
        /// </summary>
        [RepositoryFolder("08dad510-532e-4244-ac48-9c4e04234756")]
        public static ConfirmationPopupRepo Instance
        {
            get { return instance; }
        }

        /// <summary>
        /// Repository class constructor.
        /// </summary>
        public ConfirmationPopupRepo()
            : base("ConfirmationPopupRepo", "", null, 30000, false, "08dad510-532e-4244-ac48-9c4e04234756", ".\\RepositoryImages\\ConfirmationPopupRepo08dad510.rximgres")
        {
            _form__intelr_graphics_and_me = new ConfirmationPopupRepoFolders.Form__IntelR_Graphics_and_MeAppFolder(this);
        }

        #region Variables

        #endregion

        /// <summary>
        /// The Form__IntelR_Graphics_and_Me folder.
        /// </summary>
        [RepositoryFolder("6ae67e1b-4aee-42ea-bbdc-1551fc91bb64")]
        public virtual ConfirmationPopupRepoFolders.Form__IntelR_Graphics_and_MeAppFolder Form__IntelR_Graphics_and_Me
        {
            get { return _form__intelr_graphics_and_me; }
        }
    }

    /// <summary>
    /// Inner folder classes.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    public partial class ConfirmationPopupRepoFolders
    {
        /// <summary>
        /// The Form__IntelR_Graphics_and_MeAppFolder folder.
        /// </summary>
        [RepositoryFolder("6ae67e1b-4aee-42ea-bbdc-1551fc91bb64")]
        public partial class Form__IntelR_Graphics_and_MeAppFolder : RepoGenBaseFolder
        {
            RepoItemInfo _selfInfo;
            RepoItemInfo _buttonyesInfo;
            RepoItemInfo _buttonnoInfo;
            RepoItemInfo _text__intelr_graphics_and_meInfo;
            RepoItemInfo _textthe_new_settings_have_beInfo;

            /// <summary>
            /// Creates a new Form__IntelR_Graphics_and_Me  folder.
            /// </summary>
            public Form__IntelR_Graphics_and_MeAppFolder(RepoGenBaseFolder parentFolder) :
                base("Form__IntelR_Graphics_and_Me", "/form[@name~'^\\ \\ Intel®\\ HD\\ Graphics\\ Cont' or @name~'^\\ \\ Intel®\\ Iris™\\ Graphics\\ C']", parentFolder, 30000, true, "6ae67e1b-4aee-42ea-bbdc-1551fc91bb64", "")
            {
                _selfInfo = new RepoItemInfo(this, "Self", "", 30000, null, "6ae67e1b-4aee-42ea-bbdc-1551fc91bb64");
                _buttonyesInfo = new RepoItemInfo(this, "ButtonOK", "button[@name='Yes']", 30000, null, "fbe2c04f-b24f-4a8d-b5ee-8b69834f41c5");
                _buttonnoInfo = new RepoItemInfo(this, "ButtonCancel", "button[@name='No']", 30000, null, "3e2fece4-23ae-453c-9e7e-486b2e3bb25a");
                _text__intelr_graphics_and_meInfo = new RepoItemInfo(this, "Text__IntelR_Graphics_and_Me", "text[@automationid='MsgBoxTitle']", 30000, null, "650fec7e-9ea2-4c7c-b5c5-f4ed11dd22cd");
                _textthe_new_settings_have_beInfo = new RepoItemInfo(this, "TextThe_new_settings_have_be", "text[@automationid='tbDesc']", 30000, null, "da6ac1bd-b7de-4fa5-9ab2-1b2beb81781d");
            }

            /// <summary>
            /// The Self item.
            /// </summary>
            [RepositoryItem("6ae67e1b-4aee-42ea-bbdc-1551fc91bb64")]
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
            [RepositoryItemInfo("6ae67e1b-4aee-42ea-bbdc-1551fc91bb64")]
            public virtual RepoItemInfo SelfInfo
            {
                get
                {
                    return _selfInfo;
                }
            }

            /// <summary>
            /// The ButtonOK item.
            /// </summary>
            [RepositoryItem("fbe2c04f-b24f-4a8d-b5ee-8b69834f41c5")]
            public virtual Ranorex.Button ButtonYes
            {
                get
                {
                    return _buttonyesInfo.CreateAdapter<Ranorex.Button>(true);
                }
            }

            /// <summary>
            /// The ButtonOK item info.
            /// </summary>
            [RepositoryItemInfo("fbe2c04f-b24f-4a8d-b5ee-8b69834f41c5")]
            public virtual RepoItemInfo ButtonYesInfo
            {
                get
                {
                    return _buttonyesInfo;
                }
            }

            /// <summary>
            /// The ButtonCancel item.
            /// </summary>
            [RepositoryItem("3e2fece4-23ae-453c-9e7e-486b2e3bb25a")]
            public virtual Ranorex.Button ButtonNo
            {
                get
                {
                    return _buttonnoInfo.CreateAdapter<Ranorex.Button>(true);
                }
            }

            /// <summary>
            /// The ButtonCancel item info.
            /// </summary>
            [RepositoryItemInfo("3e2fece4-23ae-453c-9e7e-486b2e3bb25a")]
            public virtual RepoItemInfo ButtonNoInfo
            {
                get
                {
                    return _buttonnoInfo;
                }
            }

            /// <summary>
            /// The Text__IntelR_Graphics_and_Me item.
            /// </summary>
            [RepositoryItem("650fec7e-9ea2-4c7c-b5c5-f4ed11dd22cd")]
            public virtual Ranorex.Text Text__IntelR_Graphics_and_Me
            {
                get
                {
                    return _text__intelr_graphics_and_meInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The Text__IntelR_Graphics_and_Me item info.
            /// </summary>
            [RepositoryItemInfo("650fec7e-9ea2-4c7c-b5c5-f4ed11dd22cd")]
            public virtual RepoItemInfo Text__IntelR_Graphics_and_MeInfo
            {
                get
                {
                    return _text__intelr_graphics_and_meInfo;
                }
            }

            /// <summary>
            /// The TextThe_new_settings_have_be item.
            /// </summary>
            [RepositoryItem("da6ac1bd-b7de-4fa5-9ab2-1b2beb81781d")]
            public virtual Ranorex.Text TextThe_new_settings_have_be
            {
                get
                {
                    return _textthe_new_settings_have_beInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The TextThe_new_settings_have_be item info.
            /// </summary>
            [RepositoryItemInfo("da6ac1bd-b7de-4fa5-9ab2-1b2beb81781d")]
            public virtual RepoItemInfo TextThe_new_settings_have_beInfo
            {
                get
                {
                    return _textthe_new_settings_have_beInfo;
                }
            }
        }

    }
}