namespace Intel.VPG.Display.Automation
{
    using System.IO;
    class InitCloneDriver : InitEnvironment
    {
        IApplicationSettings _appSettings = null;
        private TestBase _context = null;
        private string driverPath = string.Empty;
        private string driverVersion = string.Empty;
        private string driverDesc = string.Empty;
        private string identifier = string.Empty;
        public InitCloneDriver(IApplicationManager argManager)
            : base(argManager)
        {
            this._appSettings = argManager.ApplicationSettings;
        }
        public override void DoWork()
        {
            driverVersion = base.MachineInfo.Driver.Version;
            driverDesc = base.MachineInfo.Driver.DriverDescription;
            identifier = driverVersion + driverDesc;
            _context = _context.Load(base.Manager.ParamInfo[ArgumentType.TestName] as string);
            if (_context == null)
                return;
            driverPath = _appSettings.AlternatePAVEProdDriverPath + "\\" + identifier + ".txt";

            if (false == VerifyDriverCopy() && CommonExtensions.IsPAVEEnvironment())
            {
                if (Directory.Exists(_appSettings.AlternatePAVEProdDriverPath))
                {
                    Directory.Delete(_appSettings.AlternatePAVEProdDriverPath, true);
                }
                Directory.CreateDirectory(_appSettings.AlternatePAVEProdDriverPath);
                Log.Verbose("Copying gfx driver from {0} to {1}", _appSettings.ProdDriverPath, _appSettings.AlternatePAVEProdDriverPath);
                CommonExtensions.CopyRecursive(_appSettings.ProdDriverPath, _appSettings.AlternatePAVEProdDriverPath);
                Log.Verbose("Successfully copy driver package to {0}", _appSettings.AlternatePAVEProdDriverPath);
                File.WriteAllText(driverPath, string.Empty);
            }
        }

        private bool VerifyDriverCopy()
        {
            if (!Directory.Exists(_appSettings.AlternatePAVEProdDriverPath))
                return false;
            else if (!File.Exists(driverPath))
                return false;
            else if ((Path.GetFileNameWithoutExtension(driverPath) != identifier) && false == _context.HasAttribute(TestType.HasUpgrade))
                return false;
            else
            {
                Log.Verbose("Copy of Gfx Driver is present in {0}", _appSettings.AlternatePAVEProdDriverPath);
                CommonExtensions._cloneDriverCopyStatus = true;
                return true;
            }
        }
    }

}
