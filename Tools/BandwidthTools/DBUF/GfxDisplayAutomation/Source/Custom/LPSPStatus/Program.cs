using System;
using System.Threading;

namespace LPSPStatus
{
    class Program
    {
        static void Main(string[] args)
        {
            UInt32 value = 0;
            Logger.Clear();
            while(true)
            {
                Logger.Message(string.Empty);
                if (RegisterInterfaces.ReadMMIO(0x45404, out value))
                {
                    if ((Convert.ToInt64(value) & 0xC0000000) == 0)
                        Logger.Message("LPSP IS ENABLED");
                    else
                        Logger.Message("LPSP IS DISABLED");
                }
                Logger.Message("Verify LPSP Status again y/n ?");
                ConsoleKeyInfo key = Console.ReadKey(true);
                if (key.Key == ConsoleKey.N)
                    break;
            }
            Logger.Message("Press any key to exit.");
            Console.ReadLine();
        }
    }
}
