
namespace Intel.VPG.Display.Automation
{
    using System.IO;
    using System.Xml;
    using System.Threading;

    class MP_NonCS_SocWatch_SysInfo : MP_S0ixBase
    {
        CSParam csParam = new CSParam();
        public MP_NonCS_SocWatch_SysInfo()
        {
            nonCS_PackageC8PlushState = true;
            NonCSInputOption = NonCSPowerOption.Idle;
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            powerParam = new CSParam();
            Log.Message(true, "Verify Socwatch Share dBinary Exists");
            if (!Directory.Exists(System.String.Concat(base.ApplicationManager.ApplicationSettings.DisplayToolsPath, "\\SocWatch")))
            {
                Log.Abort("Coun't find {0} SB to run the test", base.ApplicationManager.ApplicationSettings.DisplayToolsPath);
            }
            string[] csvFiles = Directory.GetFiles(Directory.GetCurrentDirectory(), "*.csv*");
            foreach (string file in csvFiles)
            {
                File.Delete(file);
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            csParam.Command = GetSysCommand();
            Log.Message(true, "Run SocWatch {0}",csParam.Command);
            if (AccessInterface.SetFeature<bool, CSParam>(Features.SocWatch, Action.SetMethod, csParam))
                Log.Success("socwatch applied successfully");
            switch (NonCSInputOption)
            {
                case NonCSPowerOption.MonitorOff:
                    Log.Message(true, "TurnOFF state and Resume the system from Monitor TurnOFF after {0} seconds", powerParam.Delay);
                    MonitorTurnOffParam monitorOnOffParam = new MonitorTurnOffParam();
                    monitorOnOffParam.waitingTime = 45;
                    monitorOnOffParam.onOffParam = MonitorOnOff.OffOn;
                    AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorOnOffParam);
                    break;

                case NonCSPowerOption.Sleep:
                    PowerParams powerParams = new PowerParams() { PowerStates = PowerStates.S3, Delay = 45 };
                    Log.Message("Put the system into {1} state & resume after {1} sec", powerParams.PowerStates, powerParams.Delay);
                    AccessInterface.SetFeature<bool, PowerParams>(Features.PowerEvent, Action.SetMethod, powerParams);
                    break;

                case NonCSPowerOption.Idle:
                    Log.Message("Wait for ideal desktop for 2 minute");
                    Thread.Sleep(120000); //wait for 
                    break;

                default:
                    Log.Fail("Non CS power option not specified");
                    break;

            }
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "SocWatch Output Log File");
            string[] csvFiles = Directory.GetFiles(Directory.GetCurrentDirectory(), "*.csv*");
            foreach (string file in csvFiles)
            {
                Log.Success("Log Generated at {0}", file);
            }
        }
        private string GetSysCommand()
        {
            string commandLineArg = string.Empty;
            XmlDocument benchmarkValue = new XmlDocument();
            benchmarkValue.Load("Mapper\\S0ixdata.map");
            XmlNode eventBenchmarkRoot = benchmarkValue.SelectSingleNode("/Data/ConnectedStandby");
            eventBenchmarkRoot = benchmarkValue.SelectSingleNode("/Data/SocWatch/System");
            commandLineArg = eventBenchmarkRoot.Attributes["cmd"].Value.Trim();       
            return commandLineArg;
        }
    }
}
