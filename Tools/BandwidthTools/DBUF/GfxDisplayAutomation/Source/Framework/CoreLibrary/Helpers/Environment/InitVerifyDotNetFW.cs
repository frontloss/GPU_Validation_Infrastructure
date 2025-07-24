namespace Intel.VPG.Display.Automation
{
    using Microsoft.Win32;

    class InitVerifyDotNetFW : InitEnvironment
    {
        public InitVerifyDotNetFW(IApplicationManager argManager)
            : base(argManager)
        { }
        public override void DoWork()
        {
            using (RegistryKey ndpKey = RegistryKey.OpenBaseKey(RegistryHive.LocalMachine, RegistryView.Registry64).OpenSubKey(@"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full\"))
                if (null == ndpKey.GetValue("Release"))
                    Log.Abort(".Net 4.5 Framework is required on this system");
        }
    }
}