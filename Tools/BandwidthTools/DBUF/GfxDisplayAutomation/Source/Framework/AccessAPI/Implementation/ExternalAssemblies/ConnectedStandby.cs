namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Xml;
    using System.Diagnostics;

    internal class ConnectedStandby : FunctionalBase, ISetMethod, ISet
    {
        private NetParam netParam;
        public void VerifyWDTF()
        {
            if (CommonExtensions.VerifyWDTFStatus())
            {
                Log.Verbose("WDTF framework installed successfully");
            }
            else
            {
                InstallWDTF();
            }
        }

        private void InstallWDTF()
        {
            Log.Verbose("Installing WDTF framework");
            string cmd = "";
            if (base.MachineInfo.OS.Architecture.Contains("32"))
                cmd = "/i \"Windows Driver Testing Framework (WDTF) Runtime Libraries-x86_en-us.msi\" /l* WDTFInstall.log WDTFDir=c:\\WDTF WDTF_SKIP_MACHINE_CONFIG=1";
            else
                cmd = "/i \"Windows Driver Testing Framework (WDTF) Runtime Libraries-x64_en-us.msi\" /l* WDTFInstall.log WDTFDir=c:\\WDTF WDTF_SKIP_MACHINE_CONFIG=1";
            CommonExtensions.StartProcess("msiexec", cmd, 20, base.AppSettings.WDTFPath + @"\WDTF_8.1").WaitForExit();
            if (false == CommonExtensions.VerifyWDTFStatus())
                Log.Abort("Installation failed");
        }

        private void UnInstallWDTF()
        {
            Log.Verbose("UnInstalling WDTF framework");
            string cmd = "";
            if (base.MachineInfo.OS.Architecture.Contains("32"))
                cmd = "/q /x \"Windows Driver Testing Framework (WDTF) Runtime Libraries-x86_en-us.msi\" WDTF_SKIP_MACHINE_CONFIG=1";
            else
                cmd = "/q /x \"Windows Driver Testing Framework (WDTF) Runtime Libraries-x64_en-us.msi\" WDTF_SKIP_MACHINE_CONFIG=1";
            CommonExtensions.StartProcess("msiexec", cmd, 5, base.AppSettings.WDTFPath + @"\WDTF_8.1").WaitForExit();
        }

        public bool SetMethod(object argMessage)
        {
            CSParam powerEvent = argMessage as CSParam;
            VerifyWDTF();
            return PerformPowerEvent(powerEvent);
        }

        private bool PerformPowerEvent(CSParam powerEvent)
        {
            string sleepArg = string.Format("/cs /c:1 /p:{0}", powerEvent.Delay);
            Log.Verbose("Initiated {0} @ {1} for {2}", powerEvent.PowerStates, DateTime.Now, sleepArg);
            CommonExtensions.StartProcess("pwrtest.exe", sleepArg).WaitForExit();
            Log.Verbose("Resumed from {0} @ {1}", powerEvent.PowerStates, DateTime.Now);
            if (base.AppManager.HotplugUnplugCntx.PlugUnplugInLowPower == true)
            {
                PlugUnPlugEnumeration plugUnPlugEnum = base.CreateInstance<PlugUnPlugEnumeration>(new PlugUnPlugEnumeration());
                foreach (HotPlugUnplug HT in base.AppManager.HotplugUnplugCntx.HotPlugUnPlugInfo)
                {
                    plugUnPlugEnum.SetMethod(HT);
                }
            }
            return true;
        }

        public object Set
        {
            set { VerifyWDTF(); }
        }
    }
}
