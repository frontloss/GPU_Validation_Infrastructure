using System;
using System.Runtime.InteropServices;

namespace StartStopProfiling
{
    class Program
    {
        [DllImport("PerfProfile.dll", CallingConvention = CallingConvention.StdCall)]
        internal static extern bool GfxStartProfiling(EVENT_NAME_PROFILING eventName, bool bUseAppDependencyData, IntPtr dependencyData);
        [DllImport("PerfProfile.dll", CallingConvention = CallingConvention.StdCall)]
        internal static extern bool GfxStopProfiling(EVENT_NAME_PROFILING eventName, IntPtr filePointer);

        static void Main(string[] args)
        {
            ChronometerParams cParam = new ChronometerParams();
            foreach (string arg in args)
            {
                if (arg.Trim().ToLower() == "start")
                    cParam.profilingType = PROFILING_TYPE.START_PROFILING;
                else if (arg.Trim().ToUpper() == "EVENT_RESUME_FROM_CONNECTED_STANDBY")
                    cParam.eventNameProfiling = EVENT_NAME_PROFILING.EVENT_RESUME_FROM_SLEEP;
                else if (arg.Trim().ToUpper() == "EVENT_RESUME_FROM_SLEEP")
                    cParam.eventNameProfiling = EVENT_NAME_PROFILING.EVENT_RESUME_FROM_SLEEP;
                else if (arg.Trim().ToLower() == "stop")
                    cParam.profilingType = PROFILING_TYPE.STOP_PROFILING;
                else
                    Environment.Exit(0);
            }
            switch (cParam.profilingType)
            {
                case PROFILING_TYPE.START_PROFILING:
                    StartProfiling(cParam.eventNameProfiling);
                    break;
                case PROFILING_TYPE.STOP_PROFILING:
                    StopProfiling(cParam.eventNameProfiling);
                    break;
            }
        }

        private static void StartProfiling(EVENT_NAME_PROFILING eventName)
        {
            GfxStartProfiling(eventName, false, IntPtr.Zero);
        }
        private static void StopProfiling(EVENT_NAME_PROFILING eventName)
        {
            GfxStopProfiling(eventName, IntPtr.Zero);
        }
    }
}
