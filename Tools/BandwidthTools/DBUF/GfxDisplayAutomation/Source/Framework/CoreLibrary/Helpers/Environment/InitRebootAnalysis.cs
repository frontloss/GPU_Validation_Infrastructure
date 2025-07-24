namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Net;
    using System.Xml;
    using System.Xml.Serialization;
    class InitRebootAnalysis : InitEnvironment
    {
        IApplicationSettings _appSettings = null;
        private TestBase _context = null;
        public InitRebootAnalysis(IApplicationManager argManager)
            : base(argManager)
        {
            this._appSettings = argManager.ApplicationSettings;
        }
        public override void DoWork()
        {
            _context = _context.Load(base.Manager.ParamInfo[ArgumentType.TestName] as string);

            if (!File.Exists(CommonExtensions._mpBSODAnalysisPath))
                CommonExtensions.RebootLogSerialize();
            if (CommonExtensions._rebootReason.jobID != CommonExtensions._rebootAnalysysInfo.rebootJobID &&
                CommonExtensions._rebootReason.identifier == CommonExtensions._rebootAnalysysInfo.identifier)
            {
                DateTime getCreationTime = Directory.GetCreationTime(@"C:\Windows\System32");
                if (getCreationTime != CommonExtensions._rebootReason.osCreationTime)
                {
                    Log.Alert("OS flashed has occured due to BSOD");
                    CommonExtensions.Exit(0);
                }
                if (CommonExtensions._rebootReason.count == 0)
                {
                    CommonExtensions._rebootReason.count += 1;
                    CommonExtensions.RebootLogSerialize();
                }
                else
                {
                    CommonExtensions._rebootReason.count += 1;
                    CommonExtensions.RebootLogSerialize();
                    if (CommonExtensions._rebootReason.count > 1 && false == System.Diagnostics.Debugger.IsAttached)
                    {
                        Log.Fail("{0} time abnormal reboot observed", (--CommonExtensions._rebootReason.count));
                        CommonExtensions.Exit(0);
                    }
                }
            }
        }
    }
}
