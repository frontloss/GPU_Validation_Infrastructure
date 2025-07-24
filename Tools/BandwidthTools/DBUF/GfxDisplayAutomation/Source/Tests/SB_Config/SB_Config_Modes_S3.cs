namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading;
    using System.Threading.Tasks;

    class SB_Config_Modes_S3 : SB_Config_Base
    {
        protected List<DisplayModeList> _modeList = null;
        const string S3_Config_File = "S3PowerData.config";

        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.ConfigTypeCount != base.CurrentConfig.DisplayList.Count())
                Log.Abort("This test requires atleast {0} displays , current display count: {1}", base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());
        }
        
        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            ApplyConfigOS(base.CurrentConfig);
        }
        
        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            _modeList = new List<DisplayModeList>();
            _modeList = base.GetMaxModeForConfig(base.CurrentConfig.DisplayList, base.CurrentConfig.ConfigType.GetUnifiedConfig());
            _modeList.ForEach(curDisp =>
            {
                curDisp.supportedModes.ForEach(curMode =>
                {
                    ApplyModeOS(curMode, curMode.display);
                });
            });
        }
        
        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep3()
        {
            //InvokePowerEvent(PowerStates.S3);

            if (VerifyCSSystem())
            {
                CSParam csData = new CSParam();
                int cyc = GetNoOfCycles(S3_Config_File);
                for(int i=0;i<cyc;i++)
                    AccessInterface.SetFeature<bool,CSParam>(Features.ConnectedStandby, Action.SetMethod, csData);
            }
            else
            {
                int cyc = GetNoOfCycles(S3_Config_File);
                for (int i = 0; i < cyc; i++)
                    InvokePowerEvent(PowerStates.S3);
            }
        }

        [Test(Type = TestType.Method, Order = 4)]
        public virtual void TestStep4()
        {
            VerifyConfigOS(base.CurrentConfig);
            /*_modeList.ForEach(curDisp =>
            {
                curDisp.supportedModes.ForEach(curMode =>
                {
                    VerifyModeOS(curMode, curMode.display);
                });
            });*/
        }
        
        protected virtual void InvokePowerEvent(PowerStates argPowerState)
        {
            Log.Message(true, "Invoking power event {0}", argPowerState);
            PowerParams powerParams = new PowerParams() { Delay = 30 };
            powerParams.PowerStates = argPowerState;
            powerParams.Delay = 30;
            base.EventResult(powerParams.PowerStates, base.InvokePowerEvent(powerParams, powerParams.PowerStates));
        }

        protected int GetNoOfCycles(string fileName)
        {
            int cycles = 1;
            if (System.IO.File.Exists(fileName))
            {
                String text = System.IO.File.ReadAllText(fileName);
                if (String.IsNullOrEmpty(text)!=true)
                {
                    cycles = int.Parse(text);
                }
            }
            return cycles;
        }

        private bool VerifyCSSystem()
        {
            Log.Message(true, "Checking CS test pre condition");
            Log.Verbose("checking connected standby system using powercfg.exe /a");
            System.Diagnostics.Process pwrCfgProcess = new System.Diagnostics.Process();
            pwrCfgProcess = CommonExtensions.StartProcess("powercfg.exe", " /a");
            bool testSetup = false;
            while (!pwrCfgProcess.StandardOutput.EndOfStream)
            {
                string line = pwrCfgProcess.StandardOutput.ReadLine();
                if (line == "The following sleep states are not available on this system:")
                    break;
                if (line.Trim().ToLower().Contains("standby (connected)"))
                {
                    Log.Verbose("Connected Standby Setup Ready for execution");
                    testSetup = true;
                }
            }
            if (!testSetup)
            {
                Log.Alert("Connected Standby Setup is not ready for execution");
            }
            pwrCfgProcess.Close();

            return testSetup;
         }
    }
}
