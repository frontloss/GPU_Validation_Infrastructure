namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Collections.Generic;
    using System.Diagnostics;

    public static class Log
    {
        private static LogList _logList = null;
        private static LogManager _logManager = null;

        static Log()
        {
            _logManager = new LogManager();
        }
        public static void Init(string argTestName)
        {
            Init(argTestName, (int)LogType.Verbose);
        }
        public static void Init(string argTestName, int argLogLevel)
        {
            Init(argTestName, argLogLevel, false, false, false, false);
        }
        public static void Init(string argTestName, int argLogLevel, bool argPrintVerboseOnConsole)
        {
            Init(argTestName, argLogLevel, argPrintVerboseOnConsole, false, false, false);
        }
        public static void Init(string argTestName, int argLogLevel, bool argPrintVerboseOnConsole, bool argAlternateLogFile)
        {
            Init(argTestName, argLogLevel, argPrintVerboseOnConsole, false, false, false);
        }
        public static void Init(string argTestName, int argLogLevel, bool argPrintVerboseOnConsole, bool argPostReboot, bool argGenerateDisplayTestLog, bool argAlternateLogFile)
        {
            _logManager.TestName = argTestName;
            _logManager.LogLevel = argLogLevel;
            _logManager.PostReboot = argPostReboot;
            _logManager.PrintVerboseOnConsole = argPrintVerboseOnConsole;
            _logManager.GenerateDisplayTestLogFile = argGenerateDisplayTestLog;
            _logManager.IsAlternateLogFile = argAlternateLogFile;
            if (argGenerateDisplayTestLog)
                _logManager.GenerateDisplayTestLog();
            _logList = new LogList(_logManager);
        }
        public static string NewLine
        {
            get { return "<br />"; }
        }
        public static string XmlLogDocPath
        {
            get { return _logManager.XmlLogDocPath; }
        }
        public static string LogReportText
        {
            get { return _logManager.LogReportText; }
        }
        public static string CustomLogPath
        {
            set { _logManager.CustomPathName = value; }
        }
        /// <summary>
        /// <para> Attach a method that can capture the screen and return the path to the image </para>
        /// <para> Example:: </para>
        /// <para>Log.CaptureScreenOnError = () => string:fnBitmapPrintScreen();</para>
        /// </summary>
        public static Func<string> CaptureScreenOnError
        {
            set { _logManager.CaptureScreenMethod = value; }
        }
        public static void GenerateHTMLReport()
        {
            _logManager.GenerateReport();
        }
        public static void Message(string argData, params object[] args)
        {
            Message(false, argData, args);
        }
        public static void Message(bool argIsParent, string argData, params object[] args)
        {
            _logList.Record(LogType.Message, string.Format(argData, args), argIsParent);
        }
        public static void Verbose(string argData, params object[] args)
        {
            Verbose(false, argData, args);
        }
        public static void Verbose(bool argCaptureScreenshot, string argData, params object[] args)
        {
            _logList.Record(LogType.Verbose, string.Format(argData, args), argCaptureScreenshot, false);
        }
        public static void Alert(string argData, params object[] args)
        {
            Alert(false, argData, args);
        }
        public static void Alert(bool argCaptureScreenshot, string argData, params object[] args)
        {
            _logList.Record(LogType.Alert, string.Format(argData, args), argCaptureScreenshot, false);
        }
        public static void Sporadic(string argData, params object[] args)
        {
            Sporadic(true, argData, args);
        }
        public static void Sporadic(bool argCaptureScreenshot, string argData, params object[] args)
        {
            _logManager.TestResults.Add(TestResult.Sporadic);
            _logList.Record(LogType.Sporadic, string.Format(argData, args), argCaptureScreenshot, false);
        }
        public static void Success(string argData, params object[] args)
        {
            _logManager.TestResults.Add(TestResult.Passed);
            _logList.Record(LogType.Success, string.Format(argData, args));
        }
        public static void Fail(string argData, params object[] args)
        {
            Fail(true, argData, args);
        }
        public static void Fail(bool argCaptureScreenshot, string argData, params object[] args)
        {
            _logManager.TestResults.Add(TestResult.Failed);
            _logList.Record(LogType.Fail, string.Format(argData, args), argCaptureScreenshot, false);
        }
        public static void Abort(string argData, params object[] args)
        {
            Abort(null, argData, args);
        }
        public static void Abort(Exception argOriginalEx, string argData, params object[] args)
        {
            throw new Exception(string.Format(argData, args), argOriginalEx);
        }

        public static void GetDispDiagDump()
        {
            Log.Verbose("Capturing DispDiag Dump data");
            string commandPath = System.IO.Path.Combine(Environment.SystemDirectory, "dispdiag.exe");
            System.Diagnostics.ProcessStartInfo psInfo = new System.Diagnostics.ProcessStartInfo(commandPath);
            psInfo.UseShellExecute = true;
            psInfo.UseShellExecute = false;
            psInfo.CreateNoWindow = false;
            psInfo.WindowStyle = ProcessWindowStyle.Hidden;

            System.Diagnostics.Process p = System.Diagnostics.Process.Start(psInfo);
            p.WaitForExit();
        }
    }
}
