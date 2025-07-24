namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;

    internal class InitAssemblies : InitEnvironment
    {
        public InitAssemblies(IApplicationManager argManager)
            : base(argManager)
        { }
        public override void DoWork()
        {
            if (IntPtr.Size.Equals(8))
            {
                Log.Verbose("Copying 64 bit assemblies to root");
                CommonExtensions.StartProcess("xcopy", ".\\x64 . /S /E /R /Y");
            }
            else
            {
                Log.Verbose("Copying 32 bit assemblies to root");
                CommonExtensions.StartProcess("xcopy", ".\\x86 . /S /E /R /Y");
            }
        }
    }
}
