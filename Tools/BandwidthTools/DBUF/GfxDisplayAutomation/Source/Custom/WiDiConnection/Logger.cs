namespace WiDiConnection
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;
    using System.Text;
    internal static class Logger
    {
        static string widiLogPath = "WiDiConnectionLogs.log";

        public static string WidiLogPath
        {
            get { return Logger.widiLogPath; }
            set { Logger.widiLogPath = value; }
        }
        public static void WriteLog(string printData)
        {
            Console.WriteLine(printData);
            StreamWriter writer = File.AppendText(widiLogPath);
			writer.WriteLine(printData);
			writer.Close(); 
        }
    }
}
