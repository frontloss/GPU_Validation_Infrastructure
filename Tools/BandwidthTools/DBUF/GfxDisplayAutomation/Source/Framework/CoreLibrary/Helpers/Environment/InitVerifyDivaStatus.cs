namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Management;

    class InitVerifyDivaStatus : InitEnvironment
    {
        public InitVerifyDivaStatus(IApplicationManager argManager)
            : base(argManager)
        { }

        public override void DoWork()
        {
            if (base.Manager.ApplicationSettings.UseDivaFramework || base.Manager.ApplicationSettings.UseSHEFramework)    //SHE
            {
                string msvcrPath=Path.Combine(Environment.SystemDirectory, "msvcr120.dll");
                string msvcpPath=Path.Combine(Environment.SystemDirectory, "msvcp120.dll");

                if (!(File.Exists(msvcrPath) && File.Exists(msvcpPath)))
                    Log.Abort("Install VC++ 2013 redistributables.");

                string divaSearchQuery = "select * from Win32_SystemDriver where Name = 'DivaKmd'";
                ManagementObjectSearcher searcher = new ManagementObjectSearcher(divaSearchQuery);
                var drivers = searcher.Get();

                if (drivers.Count >= 1)
                {
                    string divaDriverState = default(string);
                    foreach(ManagementObject mo in drivers)
                    {
                        if(mo["State"]!=null)
                        {
                            divaDriverState = mo["State"].ToString();
                            Log.Verbose("DivaDriver State: {0}", divaDriverState);
                        }

                        if(divaDriverState != "Running")
                        {
                            Log.Abort("DIVA Driver wasn't installed.");
                        }
                    }

                }
                else
                    Log.Abort("DIVA Driver wasn't installed.");
            }
        }
    }
}
