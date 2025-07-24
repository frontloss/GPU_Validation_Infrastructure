namespace Intel.VPG.Display.Automation
{
    using System.IO;
    using System.Linq;

    class InitVerifyDriverStatus : InitEnvironment
    {
        IApplicationSettings _appSettings = null;
        private TestBase _context = null;
        public InitVerifyDriverStatus(IApplicationManager argManager)
            : base(argManager)
        {
            this._appSettings = argManager.ApplicationSettings;
            _context = _context.Load(base.Manager.ParamInfo[ArgumentType.TestName] as string);  
            
        }
        public override void DoWork()
        {
            if (_context == null)
                return;
            if (!CommonExtensions._rebootAnalysysInfo.IsBasicDisplayAdapter)
            {
                //If test is install uninstall tests and driver is not instal, then installing driver
                if (!CommonExtensions.IntelDriverStringList.Any(str => base.MachineInfo.Driver.Name.ToLower().Contains(str)))
                {
                    InstallUnInstallParams param = new InstallUnInstallParams();
                    param.ProdPath = this._appSettings.ProdDriverPath;
                    if (!AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.InstallDriver, Action.SetMethod, param))
                    {
                        Log.Verbose("Installing Driver through UI method");
                        AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.InstallDriver, Action.SetMethod, Source.WindowsAutomationUI, param);
                    }
                }

                if (!CommonExtensions.IntelDriverStringList.Any(str => base.MachineInfo.Driver.Name.ToLower().Contains(str)))
                {
                    Log.Abort("Driver not installed!");
                }

                if (_context.ToString().ToLower().Contains("mp_") && 
                    (string.IsNullOrEmpty(base.MachineInfo.Driver.Status) || !base.MachineInfo.Driver.Status.ToLower().Contains(DriverState.Running.ToString().ToLower())) )
                {
                    Log.Verbose("Trying to enable IGD");
                    AccessInterface.SetFeature<bool, DriverAdapterType>(Features.EnableDriver, Action.SetMethod, DriverAdapterType.Intel);
                }

                if (string.IsNullOrEmpty(base.MachineInfo.Driver.Status) || !base.MachineInfo.Driver.Status.ToLower().Contains(DriverState.Running.ToString().ToLower()))
                {
                    base.MachineInfo.Driver.PrintBasicDetails();
                    Log.Abort("IGD not Enabled!");
                }

                //    Log.Sporadic(false, "Driver not installed!");
                //    InstallUnInstallParams param = new InstallUnInstallParams();
                //    param.ProdPath = this._appSettings.ProdDriverPath;
                //    if (!AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.InstallDriver, Action.SetMethod, param))
                //    {
                //        Log.Verbose("Installing Driver through UI method");
                //        AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.InstallDriver, Action.SetMethod, Source.AccessUI, param);
                //    }
                //}
                //else if(Directory.Exists(this._appSettings.ProdDriverPath))
                //{
                //    string[] infFilePath = Directory.GetFiles(string.Concat(this._appSettings.ProdDriverPath, @"\Graphics"), CommonExtensions.IdentifyDriverFile());
                //    if (base.MachineInfo.Driver.Version != DisplayExtensions.GetDriverVesion(infFilePath.First()).Trim().Split(',').Last() && !_context.HasAttribute(TestType.HasUpgrade))
                //    {
                //        Log.Sporadic(false, "Driver Version not accurate. reinstalling Production driver");
                //        InstallUnInstallParams param = new InstallUnInstallParams();
                //        param.ProdPath = this._appSettings.ProdDriverPath;
                //        if (!AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.InstallDriver, Action.SetMethod, param))
                //        {
                //            Log.Verbose("Installing Driver through UI method");
                //            AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.InstallDriver, Action.SetMethod, Source.AccessUI, param);
                //        }
                //    }
                //}
                //if (string.IsNullOrEmpty(base.MachineInfo.Driver.Status) || base.MachineInfo.Driver.Status.ToLower().Contains(DriverState.Disabled.ToString().ToLower()))
                //{
                //    Log.Sporadic(false, "Enable Driver & verify!");
                //    if (AccessInterface.SetFeature<bool, DriverAdapterType>(Features.EnableDriver, Action.SetMethod, DriverAdapterType.Intel) &&
                //        base.MachineInfo.Driver.Status.ToLower().Contains(DriverState.Running.ToString().ToLower()))
                //    {
                //        Log.Success("IGD Enabled & running");
                //    }
                //    else
                //    {
                //        base.MachineInfo.Driver.PrintBasicDetails();
                //        Log.Abort("IGD not Enabled!");
                //    }
                //}

            }
        }
    }
}