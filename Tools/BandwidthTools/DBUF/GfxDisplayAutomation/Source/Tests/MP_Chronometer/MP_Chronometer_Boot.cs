namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;

    public class MP_Chronometer_Boot : MP_ChronometerBase
    {
        protected ChronometerParams cParam;
        List<ChronometerResult> profileData = new List<ChronometerResult>();
        protected string _logfilePath;
        protected PowerStates pStates;
        private double TimeTakenForEvent = 0;
        public MP_Chronometer_Boot()
        {
            _logfilePath = "EVENT_BOOT";
            cParam = new ChronometerParams();
            cParam.eventNameProfiling = EVENT_NAME_PROFILING.EVENT_BOOT;
            IsResumeTimeTest = true;
            Log.CustomLogPath = ChronometerParams.logFilePath.Split(Path.DirectorySeparatorChar).Last();
            File.Delete(_logfilePath);
            this._powerParams = new PowerParams();
            this._powerParams.Delay = 5;
            pStates = PowerStates.S5;
        }

        #region Test
        [Test(Type = TestType.Method, Order = 1)]
        public void SetConfigMethod()
        {
            Log.Verbose(true, "Set display Config using Windows API");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Message("Config applied successfully");
            else
            {
                Log.Abort("Config not applied!");
            }
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void StartStopProfiling()
        {
            Log.Message(true, "Event under test is {0}", _logfilePath);
            if (Directory.Exists(ChronometerParams.logFilePath))
                Directory.Delete(ChronometerParams.logFilePath, true);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void Iteration1()
        {
            Log.Message(true, "{0}---- Cycle 1", _logfilePath);

            cParam.profilingType = PROFILING_TYPE.START_PROFILING;
            AccessInterface.SetFeature<bool, ChronometerParams>(Features.Chronometer, Action.SetMethod, cParam);

            base.InvokePowerEvent(this._powerParams, pStates);
            Log.Message("{0} completed..", _powerParams.PowerStates);
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void Iteration2()
        {
            cParam.profilingType = PROFILING_TYPE.STOP_PROFILING;
            AccessInterface.SetFeature<bool, ChronometerParams>(Features.Chronometer, Action.SetMethod, cParam);

            profileData = new List<ChronometerResult>();
            ChronometerResult data = new ChronometerResult();
            data.cycle = 1;
            data.EventName = Convert.ToString(cParam.eventNameProfiling);
            profileData = AccessInterface.GetFeature<List<ChronometerResult>, ChronometerResult>(Features.Chronometer, Action.GetMethod, Source.AccessAPI, data);
            if (profileData.First().benchMarkValue == 0)
            {
                Log.Abort("Benchmark value for running platform is 0 platform ID not mapped, hence exiting from test execution");
            }
            if (profileData.First().chronometerStatus)
                Log.Message("Resumr time from CS as expected, Benchmark value {0}ms, Actual: {1}ms", data.benchMarkValue, Math.Round((data.actualValue) / 1000));
            else
                Log.Alert("Resumr time from CS exceed the expectation, Benchmark Value: {0}ms, Actual: {1}ms", data.benchMarkValue, Math.Round((data.actualValue) / 1000));
            TimeTakenForEvent += Math.Round((profileData.First().actualValue) / 1000);

            Log.Message(true, "{0}---- Cycle 2", _logfilePath);

            cParam.profilingType = PROFILING_TYPE.START_PROFILING;
            AccessInterface.SetFeature<bool, ChronometerParams>(Features.Chronometer, Action.SetMethod, cParam);

            base.InvokePowerEvent(this._powerParams, pStates);
            Log.Message("{0} completed..", _powerParams.PowerStates);      
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void Iteration3()
        {
            cParam.profilingType = PROFILING_TYPE.STOP_PROFILING;
            AccessInterface.SetFeature<bool, ChronometerParams>(Features.Chronometer, Action.SetMethod, cParam);

            profileData = new List<ChronometerResult>();
            ChronometerResult data = new ChronometerResult();
            data.cycle = 2;
            data.EventName = Convert.ToString(cParam.eventNameProfiling);
            profileData = AccessInterface.GetFeature<List<ChronometerResult>, ChronometerResult>(Features.Chronometer, Action.GetMethod, Source.AccessAPI, data);
            if (profileData.First().benchMarkValue == 0)
            {
                Log.Abort("Benchmark value for running platform is 0 platform ID not mapped, hence exiting from test execution");
            }
            if (profileData.First().chronometerStatus)
                Log.Message("Resumr time from CS as expected, Benchmark value {0}ms, Actual: {1}ms", data.benchMarkValue, Math.Round((data.actualValue) / 1000));
            else
                Log.Alert("Resumr time from CS exceed the expectation, Benchmark Value: {0}ms, Actual: {1}ms", data.benchMarkValue, Math.Round((data.actualValue) / 1000));
            TimeTakenForEvent += Math.Round((profileData.First().actualValue) / 1000);

            Log.Message(true, "{0}---- Cycle 3", _logfilePath);

            cParam.profilingType = PROFILING_TYPE.START_PROFILING;
            AccessInterface.SetFeature<bool, ChronometerParams>(Features.Chronometer, Action.SetMethod, cParam);

            base.InvokePowerEvent(this._powerParams, pStates);
            Log.Message("{0} completed..", _powerParams.PowerStates);
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void Iteration4()
        {
            cParam.profilingType = PROFILING_TYPE.STOP_PROFILING;
            AccessInterface.SetFeature<bool, ChronometerParams>(Features.Chronometer, Action.SetMethod, cParam);

            profileData = new List<ChronometerResult>();
            ChronometerResult data = new ChronometerResult();
            data.cycle = 3;
            data.EventName = Convert.ToString(cParam.eventNameProfiling);
            profileData = AccessInterface.GetFeature<List<ChronometerResult>, ChronometerResult>(Features.Chronometer, Action.GetMethod, Source.AccessAPI, data);
            if (profileData.First().benchMarkValue == 0)
            {
                Log.Abort("Benchmark value for running platform is 0 platform ID not mapped, hence exiting from test execution");
            }
            if (profileData.First().chronometerStatus)
                Log.Message("Resumr time from CS as expected, Benchmark value {0}ms, Actual: {1}ms", data.benchMarkValue, Math.Round((data.actualValue) / 1000));
            else
                Log.Alert("Resumr time from CS exceed the expectation, Benchmark Value: {0}ms, Actual: {1}ms", data.benchMarkValue, Math.Round((data.actualValue) / 1000));
            TimeTakenForEvent += Math.Round((profileData.First().actualValue) / 1000);

            Log.Message(true, "{0}---- Cycle 4", _logfilePath);

            cParam.profilingType = PROFILING_TYPE.START_PROFILING;
            AccessInterface.SetFeature<bool, ChronometerParams>(Features.Chronometer, Action.SetMethod, cParam);

            base.InvokePowerEvent(this._powerParams, pStates);
            Log.Message("{0} completed..", _powerParams.PowerStates);
        }

        [Test(Type = TestType.Method, Order = 6)]
        public void Iteration5()
        {
            cParam.profilingType = PROFILING_TYPE.STOP_PROFILING;
            AccessInterface.SetFeature<bool, ChronometerParams>(Features.Chronometer, Action.SetMethod, cParam);

            profileData = new List<ChronometerResult>();
            ChronometerResult data = new ChronometerResult();
            data.cycle = 4;
            data.EventName = Convert.ToString(cParam.eventNameProfiling);
            profileData = AccessInterface.GetFeature<List<ChronometerResult>, ChronometerResult>(Features.Chronometer, Action.GetMethod, Source.AccessAPI, data);
            if (profileData.First().benchMarkValue == 0)
            {
                Log.Abort("Benchmark value for running platform is 0 platform ID not mapped, hence exiting from test execution");
            }
            if (profileData.First().chronometerStatus)
                Log.Message("Resumr time from CS as expected, Benchmark value {0}ms, Actual: {1}ms", data.benchMarkValue, Math.Round((data.actualValue) / 1000));
            else
                Log.Alert("Resumr time from CS exceed the expectation, Benchmark Value: {0}ms, Actual: {1}ms", data.benchMarkValue, Math.Round((data.actualValue) / 1000));
            TimeTakenForEvent += Math.Round((profileData.First().actualValue) / 1000);

            Log.Message(true, "{0}---- Cycle 5", _logfilePath);

            cParam.profilingType = PROFILING_TYPE.START_PROFILING;
            AccessInterface.SetFeature<bool, ChronometerParams>(Features.Chronometer, Action.SetMethod, cParam);

            base.InvokePowerEvent(this._powerParams, pStates);
            Log.Message("{0} completed..", _powerParams.PowerStates);
        }
        [Test(Type = TestType.Method, Order = 7)]
        public void Iteration6()
        {
            cParam.profilingType = PROFILING_TYPE.STOP_PROFILING;
            AccessInterface.SetFeature<bool, ChronometerParams>(Features.Chronometer, Action.SetMethod, cParam);

            profileData = new List<ChronometerResult>();
            ChronometerResult data = new ChronometerResult();
            data.cycle = 5;
            data.EventName = Convert.ToString(cParam.eventNameProfiling);
            profileData = AccessInterface.GetFeature<List<ChronometerResult>, ChronometerResult>(Features.Chronometer, Action.GetMethod, Source.AccessAPI, data);
            if (profileData.First().benchMarkValue == 0)
            {
                Log.Abort("Benchmark value for running platform is 0 platform ID not mapped, hence exiting from test execution");
            }
            if (profileData.First().chronometerStatus)
                Log.Message("Resumr time from CS as expected, Benchmark value {0}ms, Actual: {1}ms", data.benchMarkValue, Math.Round((data.actualValue) / 1000));
            else
                Log.Alert("Resumr time from CS exceed the expectation, Benchmark Value: {0}ms, Actual: {1}ms", data.benchMarkValue, Math.Round((data.actualValue) / 1000));
            TimeTakenForEvent += Math.Round((profileData.First().actualValue) / 1000);

            Log.Message(true, "{0}---- Cycle 6", _logfilePath);

            cParam.profilingType = PROFILING_TYPE.START_PROFILING;
            AccessInterface.SetFeature<bool, ChronometerParams>(Features.Chronometer, Action.SetMethod, cParam);

            base.InvokePowerEvent(this._powerParams, pStates);
            Log.Message("{0} completed..", _powerParams.PowerStates);
        }

        [Test(Type = TestType.Method, Order = 8)]
        public void Iteration7()
        {
            cParam.profilingType = PROFILING_TYPE.STOP_PROFILING;
            AccessInterface.SetFeature<bool, ChronometerParams>(Features.Chronometer, Action.SetMethod, cParam);

            profileData = new List<ChronometerResult>();
            ChronometerResult data = new ChronometerResult();
            data.cycle = 6;
            data.EventName = Convert.ToString(cParam.eventNameProfiling);
            profileData = AccessInterface.GetFeature<List<ChronometerResult>, ChronometerResult>(Features.Chronometer, Action.GetMethod, Source.AccessAPI, data);
            if (profileData.First().benchMarkValue == 0)
            {
                Log.Abort("Benchmark value for running platform is 0 platform ID not mapped, hence exiting from test execution");
            }
            if (profileData.First().chronometerStatus)
                Log.Message("Resumr time from CS as expected, Benchmark value {0}ms, Actual: {1}ms", data.benchMarkValue, Math.Round((data.actualValue) / 1000));
            else
                Log.Alert("Resumr time from CS exceed the expectation, Benchmark Value: {0}ms, Actual: {1}ms", data.benchMarkValue, Math.Round((data.actualValue) / 1000));
            TimeTakenForEvent += Math.Round((profileData.First().actualValue) / 1000);

            TimeTakenForEvent /= 6;
            if (Math.Round(TimeTakenForEvent, 2) > profileData.First().benchMarkValue)
                Log.Fail(true, "Average time taken for " + profileData.First().EventName + " for 6 cycle(s): " + Math.Round(TimeTakenForEvent, 2).ToString() + " ms");
            else
                Log.Success("Average time taken for " + profileData.First().EventName + " for 6 cycle(s): " + Math.Round(TimeTakenForEvent, 2).ToString() + " ms");
            File.Copy(Directory.GetCurrentDirectory() + "\\" + _logfilePath, ChronometerParams.logFilePath + "\\" + _logfilePath, true);
            File.Delete(Directory.GetCurrentDirectory() + "\\" + _logfilePath);
            
        }

        #endregion
    }
}
