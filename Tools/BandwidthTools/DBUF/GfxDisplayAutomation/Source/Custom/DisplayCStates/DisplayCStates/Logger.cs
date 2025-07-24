using System;
using System.IO;

namespace DisplayCStates
{
    public static class Logger
    {
        private static string lof_file = "DisplayCStateLogger.txt";

        public static void Clear()
        {
            File.Delete(lof_file);
        }
        public static void Message(string msg, params object[] args)
        {
            using (System.IO.StreamWriter file =
            new System.IO.StreamWriter(lof_file, true))
            {
                file.WriteLine(string.Format(msg, args));
                Console.WriteLine(string.Format(msg, args));
            }
        }
    }
}
