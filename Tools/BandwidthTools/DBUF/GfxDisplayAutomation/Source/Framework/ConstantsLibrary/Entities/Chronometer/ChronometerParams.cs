namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    public class ChronometerParams
    {
        public EVENT_NAME_PROFILING eventNameProfiling { get; set; }
        public PROFILING_TYPE profilingType { get; set; }
        public static string logFilePath { get; set;}

        public ChronometerParams()
        {
            logFilePath = Directory.GetCurrentDirectory() + @"\ChronometerLogs";
        }
    }
}
