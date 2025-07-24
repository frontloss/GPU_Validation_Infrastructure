namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Configuration;
    using System.Threading.Tasks;

    public class ApplicationSettings : ConfigurationSection, IApplicationSettings
    {
        private static ApplicationSettings _self = null;
        private ApplicationSettings()
        { }

        public static ApplicationSettings Instance
        {
            get { if (null == _self) _self = ConfigurationManager.GetSection("applicationSettings") as ApplicationSettings; return _self; }
        }
        [ConfigurationProperty("DefaultNamespace", DefaultValue = "Intel.VPG.Display.Automation")]
        public string DefaultNamespace
        {
            get { return base["DefaultNamespace"].ToString(); }
        }
        [ConfigurationProperty("ReportLogLevel", DefaultValue = 5)]
        public int ReportLogLevel
        {
            get { return Convert.ToInt32(base["ReportLogLevel"]); }
        }
        [ConfigurationProperty("DefaultTestName", DefaultValue = "Automation_Test")]
        public string DefaultTestName
        {
            get { return base["DefaultTestName"].ToString(); }
        }
        [ConfigurationProperty("EnableCaching", DefaultValue = true)]
        public bool EnableCaching
        {
            get { return Convert.ToBoolean(base["EnableCaching"]); }
        }
        [ConfigurationProperty("AlternateLogFile", DefaultValue = true)]
        public bool AlternateLogFile
        {
            get { return Convert.ToBoolean(base["AlternateLogFile"]); }
        }

        [ConfigurationProperty("ProdDriverPath")]
        public string ProdDriverPath
        {
            get { return this.CloneProdDriverForPAVE(base["ProdDriverPath"].ToString()); }
        }
        [ConfigurationProperty("CustomDriverPath")]
        public string CustomDriverPath
        {
            get { return string.Format("{0}\\{1}bit", this.GetPath("CustomDriverPath"), IntPtr.Size.Equals(8) ? "64" : "32"); }
        }
        [ConfigurationProperty("SwitchableGraphicsDriverPath")]
        public string SwitchableGraphicsDriverPath
        {
            get { return string.Format("{0}", this.GetPath("SwitchableGraphicsDriverPath")); }
        }
        [ConfigurationProperty("RebootFlgTimespanInDays")]
        public double RebootFlgTimespanInDays
        {
            get { return Convert.ToDouble(base["RebootFlgTimespanInDays"]); }
        }
        [ConfigurationProperty("SmartFrameApp")]
        public string SmartFrameApp
        {
            get { return this.GetPath("SmartFrameApp"); }
        }
        [ConfigurationProperty("DisplayToolsPath")]
        public string DisplayToolsPath
        {
            get { return this.GetPath("DisplayToolsPath"); }
        }
        [ConfigurationProperty("ARCSoftSerialKey")]
        public string ARCSoftSerialKey
        {
            get { return base["ARCSoftSerialKey"].ToString(); }
        }
        [ConfigurationProperty("CRCGoldenRepoPath")]
        public string CRCGoldenRepoPath
        {
            get { return this.GetPath("CRCGoldenRepoPath"); }
        }
        [ConfigurationProperty("ULTDumpFiles")]
        public string ULTDumpFiles
        {
            get { return this.GetPath("ULTDumpFiles"); }
        }
        [ConfigurationProperty("WDTFPath")]
        public string WDTFPath
        {
            get { return this.GetPath("WDTFPath"); }
        }
        [ConfigurationProperty("MPOClipPath")]
        public string MPOClipPath
        {
            get { return this.GetPath("MPOClipPath"); }
        }
        [ConfigurationProperty("WIDiAppPath")]
        public string WIDiAppPath
        {
            get { return this.GetPath("WIDiAppPath"); }
        }
        [ConfigurationProperty("AlternatePAVEProdDriverPath")]
        public string AlternatePAVEProdDriverPath
        {
            get { return string.Format(base["AlternatePAVEProdDriverPath"].ToString(), CommonExtensions.GetCurrentDirectoryDrive()); }
        }
        [ConfigurationProperty("DataPartitionRef")]
        public string DataPartitionRef
        {
            get { return base["DataPartitionRef"].ToString(); }
        }

        private string GetPath(string argKey)
        {
            string paths = base[argKey].ToString();
            return string.Format(paths, CommonExtensions.GetCurrentDirectoryDrive());
        }
        [ConfigurationProperty("DirectX")]
        public string DirectX
        {
            get { return this.GetPath("DirectX"); }
        }
        [ConfigurationProperty("HDMIGoldenImage")]
        public string HDMIGoldenImage
        {
            get { return this.GetPath("HDMIGoldenImage"); }
        }
        [ConfigurationProperty("UIAutomationPath")]
        public string UIAutomationPath
        {
            get { return base["UIAutomationPath"].ToString(); }
        }
        [ConfigurationProperty("UseULTFramework", DefaultValue = false)]
        public bool UseULTFramework
        {
            get { return Convert.ToBoolean(base["UseULTFramework"]); }
        }
        [ConfigurationProperty("UseDivaFramework", DefaultValue = false)]
        public bool UseDivaFramework
        {
            get { return Convert.ToBoolean(base["UseDivaFramework"]); }
        }
        [ConfigurationProperty("UseSHEFramework", DefaultValue = false)]
        public bool UseSHEFramework
        {
            get { return Convert.ToBoolean(base["UseSHEFramework"]); }
        }
        [ConfigurationProperty("CheckCorruption", DefaultValue = false)]
        public bool CheckCorruption
        {
            get { return Convert.ToBoolean(base["CheckCorruption"]); }
        }
        [ConfigurationProperty("GoldenCRCPath")]
        public string GoldenCRCPath
        {
            get { return this.GetPath("GoldenCRCPath"); }
        }
        [ConfigurationProperty("UseSDKType")]
        public string UseSDKType
        {
            get { return base["UseSDKType"].ToString(); }
        }
        private string CloneProdDriverForPAVE(string argOriginalPath)
        {
            if (CommonExtensions._cloneDriverCopyStatus)
                return AlternatePAVEProdDriverPath;
            else
            {
                if(Directory.Exists(argOriginalPath))
                    return argOriginalPath;
                else
                    return @"C:\Driver\Gfxdriver"; //this is release internal driver path
            }
        }
    }
}
