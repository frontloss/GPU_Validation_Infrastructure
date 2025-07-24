namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;

    internal class InitMetroSkip : InitEnvironment
    {
        public InitMetroSkip(IApplicationManager argManager)
            : base(argManager)
        { }
        public override void DoWork()
        {
            string currUserStartMenu = string.Concat(Environment.ExpandEnvironmentVariables("%UserProfile%"), @"\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\", "SkipMetro.scf");
            if (CommonExtensions.HasDTMProcess() && !File.Exists(currUserStartMenu))
            {
                Log.Verbose("Copying SkipMetro.scf to StartMenu");
                File.Copy("SkipMetro.scf", currUserStartMenu, true);
                Log.Verbose("Launching AutoIt Notepad to skip metro!");
                CommonExtensions.StartProcess("AutoIt3.exe", "GoToDesktop.au3");
            }
        }
    }
}
