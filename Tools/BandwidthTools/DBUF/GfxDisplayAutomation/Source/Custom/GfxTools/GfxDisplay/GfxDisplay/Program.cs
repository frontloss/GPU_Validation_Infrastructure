namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;

    class Program
    {
        static int Main(string[] args)
        {
            try
            {
                Console.WriteLine("Arguments passed:: {0}", string.Join(" ", args));
                Console.WriteLine("{0}", Environment.NewLine);
                if (args.Length.Equals(0))
                    Help();
                {
                    List<DisplayInfo> enumeratedDisplays = Bootstrap.EnumerateDisplaysAndModes();
                    Action<object[]> actionCommand = args.ParseArgs();
                    if (null != actionCommand)
                        actionCommand(new object[] { enumeratedDisplays, args.Skip(1).ToArray() });
                    else
                        Help();
                }
            }
            catch (Exception ex)
            {
                PrintException(ex, "Exception");
                if (null != ex.InnerException)
                {
                    Console.WriteLine("{0}", Environment.NewLine);
                    PrintException(ex.InnerException, "InnerException");
                }
                return -1;
            }
            return 0;
            //Console.WriteLine("{0}", Environment.NewLine);
            //Console.WriteLine("Press any key to continue!");
            //Console.ReadKey();
        }

        private static void PrintException(Exception argEx, string argContext)
        {
            Console.WriteLine("{0} Msg:: {1}", argContext, argEx.Message);
            Console.WriteLine("{0} StackTrace:: {1}", argContext, argEx.StackTrace);
        }
        private static void Help()
        {
            Console.WriteLine("{0}", Environment.NewLine);
            Console.WriteLine("**************************************************************************");
            Console.WriteLine("1) COMMAND TO LIST ALL CONNECTED DISPLAYS ON A MACHINE");
            Console.WriteLine("EXAMPLE:: GfxDisplay.exe -listmonitors");
            Console.WriteLine("{0}{0}", Environment.NewLine);
            Console.WriteLine("2) COMMAND TO LIST ALL SUPPORTED MODES FOR A DISPLAY TYPE");
            Console.WriteLine("USAGE:: GfxDisplay.exe -supportedmodes -<DisplayType>");
            Console.WriteLine("EXAMPLE:: GfxDisplay.exe -supportedmodes crt");
            Console.WriteLine("{0}{0}", Environment.NewLine);
            Console.WriteLine("3) COMMAND TO SET A MODE FOR A DISPLAY TYPE");
            Console.WriteLine("USAGE:: GfxDisplay.exe -set -display <DisplayType> -res <XxY> -rr <RefreshRate><p or i> -angle <0|90|180|270> -scaling <center|stretch|maintain>");
            Console.WriteLine("OPTIONAL (ANY ONE IS REQUIRED):: -display|-res|-rr|-angle|-scaling");
            Console.WriteLine("EXAMPLE:: GfxDisplay.exe -set -display crt -res 1024x768 -rr 60p -angle 180 -scaling stretch");
            Console.WriteLine("**************************************************************************");
        }
    }
}