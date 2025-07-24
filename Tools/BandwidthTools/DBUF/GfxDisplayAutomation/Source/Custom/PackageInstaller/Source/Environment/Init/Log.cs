using System;
using System.IO;

namespace PackageInstaller
{
    public static class Log
    {
        static string logFile;
        public static void Init()
        {
            logFile = string.Concat(Parser.ServiceType.ToString() , ".txt");
            if(CommonRoutine.IsSystemRebooted() == false)
                File.Delete(logFile);
            using (StreamWriter sw = File.CreateText(logFile))
            {
                Console.ForegroundColor = ConsoleColor.White;
                Console.WriteLine("====================================================================");
                sw.WriteLine("====================================================================");
                Console.ResetColor();

                Console.ForegroundColor = ConsoleColor.Blue;
                Console.WriteLine("                   Service Type {0}                   ", Parser.ServiceType);
                sw.WriteLine("                   Service Type {0}                   ", Parser.ServiceType);
                Console.ResetColor();

                Console.ForegroundColor = ConsoleColor.White;
                Console.WriteLine("====================================================================\n");
                sw.WriteLine("====================================================================\n");
                Console.ResetColor();
            }

        }
        public static void Messege(string argData, params object[] args)
        {
            File.AppendAllText(logFile, string.Format("Messege:: " + argData, args) + Environment.NewLine);
            Console.ForegroundColor = ConsoleColor.Gray;
            Console.WriteLine(string.Format(argData, args));
            Console.ResetColor();
        }
        public static void Success(string argData, params object[] args)
        {
            File.AppendAllText(logFile, string.Format("Success:: " + argData, args) + Environment.NewLine);
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine(string.Format(argData, args));
            Console.ResetColor();
        }
        public static void Fail(string argData, params object[] args)
        {
            File.AppendAllText(logFile, string.Format("Fail:: " + argData, args) + Environment.NewLine);
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine(string.Format(argData, args));
            Console.ResetColor();
        }

    }
}
