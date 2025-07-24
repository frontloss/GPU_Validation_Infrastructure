namespace Intel.VPG.Display.Automation
{
    using System.Threading;
    using System.Diagnostics;

    using Ranorex;

    public static class AccessUIExtensions
    {
        public static void FocusEnter(this Ranorex.Adapter argContext)
        {
            argContext.Focus();
            Keyboard.Press("{Enter}");
            Delay.Seconds(2);
        }
        public static void FocusEnter(this Ranorex.Core.Element argContext)
        {
            argContext.Focus();
            Keyboard.Press("{Enter}");
            Delay.Seconds(2);
        }
        public static bool RebootHandler(int argCurrentMethodIndex, RebootReason reason = RebootReason.Unknown)
        {
            int rebootIdx = -1;
            if (!argCurrentMethodIndex.Equals(-1))
                rebootIdx = argCurrentMethodIndex;
            CommonExtensions.RebootAnalysysInfo.rebootReason = reason;
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
        public static void Retry(this Ranorex.MenuItem argContext, System.Action argMainMenuNav, Text argTitleBlock)
        {
            if (!argTitleBlock.TextValue.Equals(argTitleBlock.FlavorName))
            {
                if (!argContext.Text.Equals(argTitleBlock.TextValue))
                {
                    Log.Sporadic(true, "{0} navigation failed, remains at {1}. Trying again!", argContext.Text, argTitleBlock.TextValue);
                    argMainMenuNav();
                    Log.Verbose("Selecting {0} menu item", argContext.Text);
                    argContext.FocusEnter();
                }
            }
        }
    }
}