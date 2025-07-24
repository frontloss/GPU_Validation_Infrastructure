
namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Text;
    using System.Linq;
    using System.Drawing;
    using Ranorex;
    using Ranorex.Core;
    using Ranorex.Core.Repository;
    using Ranorex.Core.Testing;


    /// <summary>
    /// The class representing the New_Repository element repository.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    [RepositoryFolder("800b65e3-5cc1-4528-99a3-651f6e9ec99b")]

    public partial class ADKRepo : RepoGenBaseFolder
    {
        static ADKRepo instance = new ADKRepo();
        New_RepositoryFolders.AssessmentLauncherNewJob4AppFolder _assessmentlaunchernewjob4;

        /// <summary>
        /// Gets the singleton class instance representing the New_Repository element repository.
        /// </summary>
        [RepositoryFolder("800b65e3-5cc1-4528-99a3-651f6e9ec99b")]
        public static ADKRepo Instance
        {
            get { return instance; }
        }

        /// <summary>
        /// Repository class constructor.
        /// </summary>
        public ADKRepo() 
            : base("New_Repository", "", null, 30000, false, "800b65e3-5cc1-4528-99a3-651f6e9ec99b", ".\\RepositoryImages\\NewRepository800b65e3.rximgres")
        {
            _assessmentlaunchernewjob4 = new New_RepositoryFolders.AssessmentLauncherNewJob4AppFolder(this);
        }

#region Variables

#endregion

        /// <summary>
        /// The AssessmentLauncherNewJob4 folder.
        /// </summary>
        [RepositoryFolder("eb24c6f4-9496-4430-80d9-f2e9c5942dd1")]
        public virtual New_RepositoryFolders.AssessmentLauncherNewJob4AppFolder AssessmentLauncherNewJob4
        {
            get { return _assessmentlaunchernewjob4; }
        }
    }

    /// <summary>
    /// Inner folder classes.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    public partial class New_RepositoryFolders
    {
        /// <summary>
        /// The AssessmentLauncherNewJob4AppFolder folder.
        /// </summary>
        [RepositoryFolder("eb24c6f4-9496-4430-80d9-f2e9c5942dd1")]
        public partial class AssessmentLauncherNewJob4AppFolder : RepoGenBaseFolder
        {
            RepoItemInfo _selfInfo;
            RepoItemInfo _runjobonthiscomputerInfo;
            RepoItemInfo _startInfo;

            /// <summary>
            /// Creates a new AssessmentLauncherNewJob4  folder.
            /// </summary>
            public AssessmentLauncherNewJob4AppFolder(RepoGenBaseFolder parentFolder) :
                    base("AssessmentLauncherNewJob4", "/form[@title~'^Assessment\\ Launcher\\ -\\ New']", parentFolder, 45000, true, "eb24c6f4-9496-4430-80d9-f2e9c5942dd1", "")
            {
                _selfInfo = new RepoItemInfo(this, "Self", "", 45000, null, "eb24c6f4-9496-4430-80d9-f2e9c5942dd1");
                _runjobonthiscomputerInfo = new RepoItemInfo(this, "RunJobOnThisComputer", "element/element[@class='WindowsForms10.BUTTON.app.0.2bf8098_r9_ad1']/button[@accessiblename='Run job on this computer']", 30000, null, "9ee20577-4826-47f4-b6bb-02f28ea1a24d");
                _startInfo = new RepoItemInfo(this, "Start", "element/element[@instance='1']/element[@class='WindowsForms10.BUTTON.app.0.2bf8098_r9_ad1' and @instance='0']/button[@accessiblename='Start']", 30000, null, "79554da9-63c0-4925-89a4-b0a0574a3269");
            }

            /// <summary>
            /// The Self item.
            /// </summary>
            [RepositoryItem("eb24c6f4-9496-4430-80d9-f2e9c5942dd1")]
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
            [RepositoryItemInfo("eb24c6f4-9496-4430-80d9-f2e9c5942dd1")]
            public virtual RepoItemInfo SelfInfo
            {
                get
                {
                    return _selfInfo;
                }
            }

            /// <summary>
            /// The RunJobOnThisComputer item.
            /// </summary>
            [RepositoryItem("9ee20577-4826-47f4-b6bb-02f28ea1a24d")]
            public virtual Ranorex.Button RunJobOnThisComputer
            {
                get
                {
                    return _runjobonthiscomputerInfo.CreateAdapter<Ranorex.Button>(true);
                }
            }

            /// <summary>
            /// The RunJobOnThisComputer item info.
            /// </summary>
            [RepositoryItemInfo("9ee20577-4826-47f4-b6bb-02f28ea1a24d")]
            public virtual RepoItemInfo RunJobOnThisComputerInfo
            {
                get
                {
                    return _runjobonthiscomputerInfo;
                }
            }
            /// <summary>
            /// The Start item.
            /// </summary>
            [RepositoryItem("79554da9-63c0-4925-89a4-b0a0574a3269")]
            public virtual Ranorex.Button Start
            {
                get
                {
                    return _startInfo.CreateAdapter<Ranorex.Button>(true);
                }
            }

            /// <summary>
            /// The Start item info.
            /// </summary>
            [RepositoryItemInfo("79554da9-63c0-4925-89a4-b0a0574a3269")]
            public virtual RepoItemInfo StartInfo
            {
                get
                {
                    return _startInfo;
                }
            }
        }

    }
}
