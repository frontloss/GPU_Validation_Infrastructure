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
    /// The class representing the SystemInfoRepo element repository.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    [RepositoryFolder("29ec13bc-1bdc-4f80-a196-a6fc3c7f2935")]
    public partial class SystemInfoRepo : RepoGenBaseFolder
    {
        static SystemInfoRepo instance = new SystemInfoRepo();
        SystemInfoRepoFolders.FormIntelLParenRRParen_GraphAppFolder _formintellparenrrparen_graph;

        /// <summary>
        /// Gets the singleton class instance representing the SystemInfoRepo element repository.
        /// </summary>
        [RepositoryFolder("29ec13bc-1bdc-4f80-a196-a6fc3c7f2935")]
        public static SystemInfoRepo Instance
        {
            get { return instance; }
        }

        /// <summary>
        /// Repository class constructor.
        /// </summary>
        public SystemInfoRepo()
            : base("SystemInfoRepo", "", null, 30000, false, "29ec13bc-1bdc-4f80-a196-a6fc3c7f2935", ".\\RepositoryImages\\SystemInfoRepo29ec13bc.rximgres")
        {
            _formintellparenrrparen_graph = new SystemInfoRepoFolders.FormIntelLParenRRParen_GraphAppFolder(this);
        }

        #region Variables

        #endregion

        /// <summary>
        /// The FormIntelLParenRRParen_Graph folder.
        /// </summary>
        [RepositoryFolder("424084ee-70b0-43db-807a-428d02d8dcc6")]
        public virtual SystemInfoRepoFolders.FormIntelLParenRRParen_GraphAppFolder FormIntelLParenRRParen_Graph
        {
            get { return _formintellparenrrparen_graph; }
        }
    }

    /// <summary>
    /// Inner folder classes.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCode("Ranorex", "4.0.2")]
    public partial class SystemInfoRepoFolders
    {
        /// <summary>
        /// The FormIntelLParenRRParen_GraphAppFolder folder.
        /// </summary>
        [RepositoryFolder("424084ee-70b0-43db-807a-428d02d8dcc6")]
        public partial class FormIntelLParenRRParen_GraphAppFolder : RepoGenBaseFolder
        {
            RepoItemInfo _selfInfo;
            RepoItemInfo _reportdateInfo;
            RepoItemInfo _shaderversionInfo;
            RepoItemInfo _driverversionInfo;
            RepoItemInfo _installeddirectxversionInfo;
            RepoItemInfo _defaultlanguageInfo;
            RepoItemInfo _supporteddirectxversionInfo;
            RepoItemInfo _operatingsystemInfo;
            RepoItemInfo _openglversionInfo;
            RepoItemInfo _physicalmemoryInfo;
            RepoItemInfo _processornameInfo;
            RepoItemInfo _deviceidInfo;
            RepoItemInfo _devicerevisionInfo;
            RepoItemInfo _processorspeedInfo;
            RepoItemInfo _vendoridInfo;
            RepoItemInfo _videobiosInfo;
            RepoItemInfo _processorgraphicsInfo;
            RepoItemInfo _currentgraphicsmodeInfo;
            RepoItemInfo _reporttimeInfo;

            /// <summary>
            /// Creates a new FormIntelLParenRRParen_Graph  folder.
            /// </summary>
            public FormIntelLParenRRParen_GraphAppFolder(RepoGenBaseFolder parentFolder) :
                base("FormIntelLParenRRParen_Graph", "/form[@automationid='MainWindow']", parentFolder, 30000, true, "424084ee-70b0-43db-807a-428d02d8dcc6", "")
            {
                _selfInfo = new RepoItemInfo(this, "Self", "", 30000, null, "424084ee-70b0-43db-807a-428d02d8dcc6");
                _reportdateInfo = new RepoItemInfo(this, "ReportDate", "element/element[@classname='InformationTab']/text[@automationid='lbReportDateVal']", 30000, null, "bb83355f-4eb7-4893-8737-2057ac0b2ec6");
                _shaderversionInfo = new RepoItemInfo(this, "ShaderVersion", "element/element[@classname='InformationTab']/text[@automationid='lbCSVersionVal']", 30000, null, "dd94a4a2-426f-47ae-85c9-cd9ad88e0ffa");
                _driverversionInfo = new RepoItemInfo(this, "DriverVersion", "element/element[@classname='InformationTab']/text[@automationid='lbDriverVersionVal']", 30000, null, "6ba189b4-a835-43b3-b359-90b9a62839ae");
                _installeddirectxversionInfo = new RepoItemInfo(this, "InstalledDirectXVersion", "element/element[@classname='InformationTab']/text[@automationid='lbDirectXVersionVal']", 30000, null, "b165dec1-7e4a-4869-ba04-a41a890a970a");
                _defaultlanguageInfo = new RepoItemInfo(this, "DefaultLanguage", "element/element[@classname='InformationTab']//text[@automationid='lbDefaultLanguageVal']", 30000, null, "aa74a122-99e9-46a8-8134-33508cc1b887");
                _supporteddirectxversionInfo = new RepoItemInfo(this, "SupportedDirectXVersion", "element/element[@classname='InformationTab']/text[@automationid='lbDirectXVersionSupVal']", 30000, null, "1043145f-dd6a-49ab-871e-0cffd70a94a5");
                _operatingsystemInfo = new RepoItemInfo(this, "OperatingSystem", "element/element[@classname='InformationTab']//text[@automationid='lbOperatingSystemVal']", 30000, null, "808a4916-1134-4f5a-8b52-765c821c9a7f");
                _openglversionInfo = new RepoItemInfo(this, "OpenGLVersion", "element/element[@classname='InformationTab']/text[@automationid='lbOGLVersionVal']", 30000, null, "2f3ecbb2-17fa-4d7d-823c-87f4015d2ce5");
                _physicalmemoryInfo = new RepoItemInfo(this, "PhysicalMemory", "element/element[@classname='InformationTab']/text[@automationid='lbPhysicalMemoryVal']", 30000, null, "1e56c236-0b12-4bac-a914-d6f018608c9a");
                _processornameInfo = new RepoItemInfo(this, "ProcessorName", "element/element[@classname='InformationTab']//text[@automationid='lbProcessorVal']", 30000, null, "1d74ac0e-76e8-49cf-9486-ce5078192774");
                _deviceidInfo = new RepoItemInfo(this, "DeviceID", "element/element[@classname='InformationTab']/text[@automationid='lbDeviceIdVal']", 30000, null, "a58b4c52-8573-4930-af7d-726e02999d8f");
                _devicerevisionInfo = new RepoItemInfo(this, "DeviceRevision", "element/element[@classname='InformationTab']/text[@automationid='lbDeviceRevVal']", 30000, null, "8c3d73d6-f34d-46f1-917f-1d6e8bff6815");
                _processorspeedInfo = new RepoItemInfo(this, "ProcessorSpeed", "element/element[@classname='InformationTab']/text[@automationid='lbProcessorSpeedVal']", 30000, null, "e6dda72d-0526-4439-adcb-d96dbe33fe15");
                _vendoridInfo = new RepoItemInfo(this, "VendorID", "element/element[@classname='InformationTab']/text[@automationid='lbVendorIdVal']", 30000, null, "85dddf57-8ca8-466c-bc34-91cd3468ce3c");
                _videobiosInfo = new RepoItemInfo(this, "VideoBios", "element/element[@classname='InformationTab']/text[@automationid='lbVideoBiosVal']", 30000, null, "45ef2ac5-08bd-461f-9ca7-5dc7f1e816a0");
                _processorgraphicsInfo = new RepoItemInfo(this, "ProcessorGraphics", "element/element[@classname='InformationTab']/text/text[@automationid='lbAcceleratorUseVal']", 30000, null, "2a6770a8-7c6f-4144-aae1-bff80bf4fecc");
                _currentgraphicsmodeInfo = new RepoItemInfo(this, "CurrentGraphicsMode", "element/element[@classname='InformationTab']/text[@automationid='lbCurrentModeVal']", 30000, null, "13daa786-3351-4835-ba73-d255e0f5229e");
                _reporttimeInfo = new RepoItemInfo(this, "ReportTime", "element/element[@classname='InformationTab']/text[@automationid='lbReportTimeVal']", 30000, null, "4a34c616-27c5-4f40-8c71-859cd9c1551e");
            }

            /// <summary>
            /// The Self item.
            /// </summary>
            [RepositoryItem("424084ee-70b0-43db-807a-428d02d8dcc6")]
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
            [RepositoryItemInfo("424084ee-70b0-43db-807a-428d02d8dcc6")]
            public virtual RepoItemInfo SelfInfo
            {
                get
                {
                    return _selfInfo;
                }
            }

            /// <summary>
            /// The ReportDate item.
            /// </summary>
            [RepositoryItem("bb83355f-4eb7-4893-8737-2057ac0b2ec6")]
            public virtual Ranorex.Text ReportDate
            {
                get
                {
                    return _reportdateInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The ReportDate item info.
            /// </summary>
            [RepositoryItemInfo("bb83355f-4eb7-4893-8737-2057ac0b2ec6")]
            public virtual RepoItemInfo ReportDateInfo
            {
                get
                {
                    return _reportdateInfo;
                }
            }

            /// <summary>
            /// The ShaderVersion item.
            /// </summary>
            [RepositoryItem("dd94a4a2-426f-47ae-85c9-cd9ad88e0ffa")]
            public virtual Ranorex.Text ShaderVersion
            {
                get
                {
                    return _shaderversionInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The ShaderVersion item info.
            /// </summary>
            [RepositoryItemInfo("dd94a4a2-426f-47ae-85c9-cd9ad88e0ffa")]
            public virtual RepoItemInfo ShaderVersionInfo
            {
                get
                {
                    return _shaderversionInfo;
                }
            }

            /// <summary>
            /// The DriverVersion item.
            /// </summary>
            [RepositoryItem("6ba189b4-a835-43b3-b359-90b9a62839ae")]
            public virtual Ranorex.Text DriverVersion
            {
                get
                {
                    return _driverversionInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The DriverVersion item info.
            /// </summary>
            [RepositoryItemInfo("6ba189b4-a835-43b3-b359-90b9a62839ae")]
            public virtual RepoItemInfo DriverVersionInfo
            {
                get
                {
                    return _driverversionInfo;
                }
            }

            /// <summary>
            /// The InstalledDirectXVersion item.
            /// </summary>
            [RepositoryItem("b165dec1-7e4a-4869-ba04-a41a890a970a")]
            public virtual Ranorex.Text InstalledDirectXVersion
            {
                get
                {
                    return _installeddirectxversionInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The InstalledDirectXVersion item info.
            /// </summary>
            [RepositoryItemInfo("b165dec1-7e4a-4869-ba04-a41a890a970a")]
            public virtual RepoItemInfo InstalledDirectXVersionInfo
            {
                get
                {
                    return _installeddirectxversionInfo;
                }
            }

            /// <summary>
            /// The DefaultLanguage item.
            /// </summary>
            [RepositoryItem("aa74a122-99e9-46a8-8134-33508cc1b887")]
            public virtual Ranorex.Text DefaultLanguage
            {
                get
                {
                    return _defaultlanguageInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The DefaultLanguage item info.
            /// </summary>
            [RepositoryItemInfo("aa74a122-99e9-46a8-8134-33508cc1b887")]
            public virtual RepoItemInfo DefaultLanguageInfo
            {
                get
                {
                    return _defaultlanguageInfo;
                }
            }

            /// <summary>
            /// The SupportedDirectXVersion item.
            /// </summary>
            [RepositoryItem("1043145f-dd6a-49ab-871e-0cffd70a94a5")]
            public virtual Ranorex.Text SupportedDirectXVersion
            {
                get
                {
                    return _supporteddirectxversionInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The SupportedDirectXVersion item info.
            /// </summary>
            [RepositoryItemInfo("1043145f-dd6a-49ab-871e-0cffd70a94a5")]
            public virtual RepoItemInfo SupportedDirectXVersionInfo
            {
                get
                {
                    return _supporteddirectxversionInfo;
                }
            }

            /// <summary>
            /// The OperatingSystem item.
            /// </summary>
            [RepositoryItem("808a4916-1134-4f5a-8b52-765c821c9a7f")]
            public virtual Ranorex.Text OperatingSystem
            {
                get
                {
                    return _operatingsystemInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The OperatingSystem item info.
            /// </summary>
            [RepositoryItemInfo("808a4916-1134-4f5a-8b52-765c821c9a7f")]
            public virtual RepoItemInfo OperatingSystemInfo
            {
                get
                {
                    return _operatingsystemInfo;
                }
            }

            /// <summary>
            /// The OpenGLVersion item.
            /// </summary>
            [RepositoryItem("2f3ecbb2-17fa-4d7d-823c-87f4015d2ce5")]
            public virtual Ranorex.Text OpenGLVersion
            {
                get
                {
                    return _openglversionInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The OpenGLVersion item info.
            /// </summary>
            [RepositoryItemInfo("2f3ecbb2-17fa-4d7d-823c-87f4015d2ce5")]
            public virtual RepoItemInfo OpenGLVersionInfo
            {
                get
                {
                    return _openglversionInfo;
                }
            }

            /// <summary>
            /// The PhysicalMemory item.
            /// </summary>
            [RepositoryItem("1e56c236-0b12-4bac-a914-d6f018608c9a")]
            public virtual Ranorex.Text PhysicalMemory
            {
                get
                {
                    return _physicalmemoryInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The PhysicalMemory item info.
            /// </summary>
            [RepositoryItemInfo("1e56c236-0b12-4bac-a914-d6f018608c9a")]
            public virtual RepoItemInfo PhysicalMemoryInfo
            {
                get
                {
                    return _physicalmemoryInfo;
                }
            }

            /// <summary>
            /// The ProcessorName item.
            /// </summary>
            [RepositoryItem("1d74ac0e-76e8-49cf-9486-ce5078192774")]
            public virtual Ranorex.Text ProcessorName
            {
                get
                {
                    return _processornameInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The ProcessorName item info.
            /// </summary>
            [RepositoryItemInfo("1d74ac0e-76e8-49cf-9486-ce5078192774")]
            public virtual RepoItemInfo ProcessorNameInfo
            {
                get
                {
                    return _processornameInfo;
                }
            }

            /// <summary>
            /// The DeviceID item.
            /// </summary>
            [RepositoryItem("a58b4c52-8573-4930-af7d-726e02999d8f")]
            public virtual Ranorex.Text DeviceID
            {
                get
                {
                    return _deviceidInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The DeviceID item info.
            /// </summary>
            [RepositoryItemInfo("a58b4c52-8573-4930-af7d-726e02999d8f")]
            public virtual RepoItemInfo DeviceIDInfo
            {
                get
                {
                    return _deviceidInfo;
                }
            }

            /// <summary>
            /// The DeviceRevision item.
            /// </summary>
            [RepositoryItem("8c3d73d6-f34d-46f1-917f-1d6e8bff6815")]
            public virtual Ranorex.Text DeviceRevision
            {
                get
                {
                    return _devicerevisionInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The DeviceRevision item info.
            /// </summary>
            [RepositoryItemInfo("8c3d73d6-f34d-46f1-917f-1d6e8bff6815")]
            public virtual RepoItemInfo DeviceRevisionInfo
            {
                get
                {
                    return _devicerevisionInfo;
                }
            }

            /// <summary>
            /// The ProcessorSpeed item.
            /// </summary>
            [RepositoryItem("e6dda72d-0526-4439-adcb-d96dbe33fe15")]
            public virtual Ranorex.Text ProcessorSpeed
            {
                get
                {
                    return _processorspeedInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The ProcessorSpeed item info.
            /// </summary>
            [RepositoryItemInfo("e6dda72d-0526-4439-adcb-d96dbe33fe15")]
            public virtual RepoItemInfo ProcessorSpeedInfo
            {
                get
                {
                    return _processorspeedInfo;
                }
            }

            /// <summary>
            /// The VendorID item.
            /// </summary>
            [RepositoryItem("85dddf57-8ca8-466c-bc34-91cd3468ce3c")]
            public virtual Ranorex.Text VendorID
            {
                get
                {
                    return _vendoridInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The VendorID item info.
            /// </summary>
            [RepositoryItemInfo("85dddf57-8ca8-466c-bc34-91cd3468ce3c")]
            public virtual RepoItemInfo VendorIDInfo
            {
                get
                {
                    return _vendoridInfo;
                }
            }

            /// <summary>
            /// The VideoBios item.
            /// </summary>
            [RepositoryItem("45ef2ac5-08bd-461f-9ca7-5dc7f1e816a0")]
            public virtual Ranorex.Text VideoBios
            {
                get
                {
                    return _videobiosInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The VideoBios item info.
            /// </summary>
            [RepositoryItemInfo("45ef2ac5-08bd-461f-9ca7-5dc7f1e816a0")]
            public virtual RepoItemInfo VideoBiosInfo
            {
                get
                {
                    return _videobiosInfo;
                }
            }

            /// <summary>
            /// The ProcessorGraphics item.
            /// </summary>
            [RepositoryItem("2a6770a8-7c6f-4144-aae1-bff80bf4fecc")]
            public virtual Ranorex.Text ProcessorGraphics
            {
                get
                {
                    return _processorgraphicsInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The ProcessorGraphics item info.
            /// </summary>
            [RepositoryItemInfo("2a6770a8-7c6f-4144-aae1-bff80bf4fecc")]
            public virtual RepoItemInfo ProcessorGraphicsInfo
            {
                get
                {
                    return _processorgraphicsInfo;
                }
            }

            /// <summary>
            /// The CurrentGraphicsMode item.
            /// </summary>
            [RepositoryItem("13daa786-3351-4835-ba73-d255e0f5229e")]
            public virtual Ranorex.Text CurrentGraphicsMode
            {
                get
                {
                    return _currentgraphicsmodeInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The CurrentGraphicsMode item info.
            /// </summary>
            [RepositoryItemInfo("13daa786-3351-4835-ba73-d255e0f5229e")]
            public virtual RepoItemInfo CurrentGraphicsModeInfo
            {
                get
                {
                    return _currentgraphicsmodeInfo;
                }
            }

            /// <summary>
            /// The ReportTime item.
            /// </summary>
            [RepositoryItem("4a34c616-27c5-4f40-8c71-859cd9c1551e")]
            public virtual Ranorex.Text ReportTime
            {
                get
                {
                    return _reporttimeInfo.CreateAdapter<Ranorex.Text>(true);
                }
            }

            /// <summary>
            /// The ReportTime item info.
            /// </summary>
            [RepositoryItemInfo("4a34c616-27c5-4f40-8c71-859cd9c1551e")]
            public virtual RepoItemInfo ReportTimeInfo
            {
                get
                {
                    return _reporttimeInfo;
                }
            }
        }

    }
}