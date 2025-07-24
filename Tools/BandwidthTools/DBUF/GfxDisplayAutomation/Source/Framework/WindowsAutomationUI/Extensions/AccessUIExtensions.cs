namespace Intel.VPG.Display.Automation
{
    using System.Threading;
    using System.Diagnostics;

    public static class AccessUIExtensions
    {
        public static bool RebootHandler(int argCurrentMethodIndex, RebootReason reason = RebootReason.Unknown)
        {
            int rebootIdx = -1;
            if (!argCurrentMethodIndex.Equals(-1))
                rebootIdx = argCurrentMethodIndex;
            CommonExtensions._rebootAnalysysInfo.rebootReason = reason;
            CommonExtensions.DoSinchorize(rebootIdx);
            if (CommonExtensions.HasDTMProcess())
            {
                Log.Verbose("Initiated Environment.Exit(0) on DTM Infrastructure @ {0}", System.DateTime.Now);
                CommonExtensions.ExitProcess(0);
            }
            Log.Verbose("Initiated S5 @ {0}", System.DateTime.Now);
            Process process = CommonExtensions.StartProcess("shutdown", "/f /r /t 10");
            Thread.Sleep(10000);
            return process.HasExited;
        }
    }
}