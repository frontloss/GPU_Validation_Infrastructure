namespace Intel.VPG.Display.Automation
{
    public interface IApplicationSettings
    {
        string DefaultNamespace { get; }
        int ReportLogLevel { get; }
        string DefaultTestName { get; }
        bool EnableCaching { get; }
        bool AlternateLogFile { get; }
        string ProdDriverPath { get; }
        string AlternatePAVEProdDriverPath { get; }
        string CustomDriverPath { get; }
        double RebootFlgTimespanInDays { get; }
        string DisplayToolsPath { get; }
        string ARCSoftSerialKey { get; }
        string CRCGoldenRepoPath { get; }
        string WDTFPath { get; }
        string MPOClipPath { get; }   
        string DataPartitionRef { get; }
        string WIDiAppPath { get; }
        string SwitchableGraphicsDriverPath { get; }
        string DirectX { get; }
        string HDMIGoldenImage { get; }
        string UIAutomationPath { get; }
        string ULTDumpFiles { get; }
        string SmartFrameApp { get; }
        bool UseULTFramework { get; }
        string UseSDKType { get; }
        bool UseDivaFramework { get; }
        bool UseSHEFramework { get; }
        bool CheckCorruption { get; }
        string GoldenCRCPath { get; }
    }
}
