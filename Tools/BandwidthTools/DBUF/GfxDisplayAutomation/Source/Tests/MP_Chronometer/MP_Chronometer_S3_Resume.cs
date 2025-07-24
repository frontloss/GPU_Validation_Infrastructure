namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;

    public class MP_Chronometer_S3_Resume : MP_ChronometerBase
    {
        protected ChronometerParams cParam = new ChronometerParams();
        // cParam.eventNameProfiling = EVENT_NAME_PROFILING.EVENT_RESUME_FROM_SLEEP;
        List<ChronometerResult> profileData = new List<ChronometerResult>();
        protected string _logfilePath;
        protected PowerStates pStates;
        List<double> chronometerValues = new List<double>();
        public MP_Chronometer_S3_Resume()
        {
            _logfilePath = "EVENT_RESUME_FROM_SLEEP";
            cParam = new ChronometerParams();
            cParam.eventNameProfiling = EVENT_NAME_PROFILING.EVENT_RESUME_FROM_SLEEP;
            IsResumeTimeTest = true;
            Log.CustomLogPath = ChronometerParams.logFilePath.Split(Path.DirectorySeparatorChar).Last();
            File.Delete(_logfilePath);
            this._powerParams = new PowerParams();
            this._powerParams.Delay = 5;
            pStates = PowerStates.S3;
        }

        #region Test
        [Test(Type = TestType.Method, Order = 1)]
        public void SetConfigMethod()
        {
        //    base.LoadDLL();
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

            double TimeTakenForEvent = 0;
            try
            {
                for (int eachCycle = 1; eachCycle <= 6; eachCycle++)
                {
                    Log.Message(true, "{0}---- Cycle {1}",_logfilePath, eachCycle);

                    cParam.profilingType = PROFILING_TYPE.START_PROFILING;
                    AccessInterface.SetFeature<bool, ChronometerParams>(Features.Chronometer, Action.SetMethod, cParam);

                    base.InvokePowerEvent(this._powerParams, pStates);
                    Log.Message("{0} completed..", _powerParams.PowerStates);
                    cParam.profilingType = PROFILING_TYPE.STOP_PROFILING;
                    AccessInterface.SetFeature<bool, ChronometerParams>(Features.Chronometer, Action.SetMethod, cParam);

                    profileData = new List<ChronometerResult>();
                    ChronometerResult data = new ChronometerResult();
                    data.cycle = eachCycle;
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
                    chronometerValues.Add(Math.Round((profileData.First().actualValue) / 1000));
                }
            }
            catch
            {
                return;
            }
            chronometerValues.Sort();
            chronometerValues.RemoveAt(5);
            chronometerValues.RemoveAt(0) ;
            foreach (double d in chronometerValues)
                TimeTakenForEvent += d;


            TimeTakenForEvent /= 4;
            if(Math.Round(TimeTakenForEvent, 2) > profileData.First().benchMarkValue)
                Log.Fail(true,"Average time taken for " + profileData.First().EventName + " for 6 cycle(s): " + Math.Round(TimeTakenForEvent, 2).ToString() + " ms");
            else
                Log.Success("Average time taken for " + profileData.First().EventName + " for 6 cycle(s): " + Math.Round(TimeTakenForEvent, 2).ToString() + " ms");
        }
        #endregion
    }
}
