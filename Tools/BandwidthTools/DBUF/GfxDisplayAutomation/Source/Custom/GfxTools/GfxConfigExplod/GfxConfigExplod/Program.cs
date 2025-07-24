namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Collections.Generic;

    class Program
    {
        static void Main(string[] args)
        {
            try
            {
                Console.WriteLine("Arguments passed:: {0}", string.Join(" ", args));
                Console.WriteLine("{0}", Environment.NewLine);
                if (!args.ParseHelpRequest())
                {
                    List<string> displaysList = args.ParseDisplayList();
                    if (null == displaysList || displaysList.Count.Equals(0))
                    {
                        List<DisplayInfo> enumeratedDisplays = WindowsFunctions.GetAllDisplayList();
                        displaysList = enumeratedDisplays.Select(dI => dI.DisplayType).ToList();
                    }
                    if (displaysList.Count > 1)
                    {
                        string outputFileName = args.ParseOutputFile();
                        if (!string.IsNullOrEmpty(outputFileName) && File.Exists(outputFileName))
                            File.Delete(outputFileName);
                        int displaysSupported = args.ParseDisplaysSupported();
                        if (displaysSupported.Equals(0) || !WindowsFunctions.ExplodPatterns.Keys.Contains(displaysSupported) || displaysList.Count.Equals(displaysSupported))
                        {
                            displaysSupported = 2;
                            if (displaysList.Count >= 3)
                                displaysSupported = 3;
                        }
                        Console.WriteLine("Preparing Config Explod list for {0} pipe", displaysSupported);
                        Console.WriteLine("*****************************************");
                        List<string> configExplod = WindowsFunctions.ExplodPatterns[displaysSupported](displaysList);
                        configExplod.ForEach(combo =>
                            {
                                if (!string.IsNullOrEmpty(outputFileName))
                                    File.AppendAllText(outputFileName, string.Format("{0}{1}", combo, Environment.NewLine));
                                Console.WriteLine(combo);
                            });
                    }
                    else
                        Console.WriteLine("Displays enumerated in the system is {0}::{1}. No config patterns prepared!", displaysList.Count, string.Join(",", displaysList.ToArray()));
                }
                else
                    Help();
            }
            catch (Exception ex)
            {
                PrintException(ex, "Exception");
                if (null != ex.InnerException)
                {
                    Console.WriteLine("{0}", Environment.NewLine);
                    PrintException(ex.InnerException, "InnerException");
                }
            }
            Console.WriteLine("{0}", Environment.NewLine);
            Console.WriteLine("Press any key to continue!");
            Console.ReadKey();
        }

        private static void PrintException(Exception argEx, string argContext)
        {
            Console.WriteLine("{0} Msg:: {1}", argContext, argEx.Message);
            Console.WriteLine("{0} StackTrace:: {1}", argContext, argEx.StackTrace);
        }
        private static void Help()
        {
            Console.WriteLine("**************************************************************************");
            Console.WriteLine("1) COMMAND TO OUTPUT THE CONFIG EXPLOD PATTERN TO A FILE");
            Console.WriteLine("{0}", Environment.NewLine);
            Console.WriteLine(@"USAGE:: GfxConfigExplod.exe -fileTo <path:\filename.txt>");
            Console.WriteLine("EXAMPLE:: GfxConfigExplod.exe -fileTo ConfigPatterns.txt");
            Console.WriteLine(@"EXAMPLE:: GfxConfigExplod.exe -fileTo ""\\ba5swts005\common\user\ConfigPatterns.txt""");
            Console.WriteLine(@"EXAMPLE:: GfxConfigExplod.exe -fileTo ""C:\My Documents\ConfigPatterns.txt""");
            Console.WriteLine("{0}{0}", Environment.NewLine);
            Console.WriteLine("2) COMMAND TO SPECIFY THE DESIRED CONFIG EXPLOD PATTERN FOR A 2-PIPE OR 3-PIPE COMBINATION");
            Console.WriteLine("{0}", Environment.NewLine);
            Console.WriteLine("USAGE:: GfxConfigExplod.exe -maxDisp <2 OR 3>");
            Console.WriteLine("EXAMPLE:: GfxConfigExplod.exe -maxDisp 3");
            Console.WriteLine("{0}{0}", Environment.NewLine);
            Console.WriteLine("3) COMMAND TO SPECIFY THE DISPLAY LIST");
            Console.WriteLine("EXAMPLE:: GfxConfigExplod.exe -displays CRT,EDP,HDMI,DP,HDMI_2,DP_2,DP_3,MIPI_A,MIPI_B");
            Console.WriteLine(@"DELIMITER:: , OR - OR +");
            Console.WriteLine(@"DUPLICATE DISPLAY NAME:: APPEND A NUMBER TO EACH DUPLICATE DISPLAY NAME");
            Console.WriteLine("{0}{0}", Environment.NewLine);
            Console.WriteLine("4) POSSIBLE COMMANDS");
            Console.WriteLine("{0}", Environment.NewLine);
            Console.WriteLine("USAGE:: GfxConfigExplod.exe -help");
            Console.WriteLine(@"USAGE:: GfxConfigExplod.exe -fileTo <path\filename> -maxDisp <2 OR 3> -displays <display list>");
            Console.WriteLine("OPTIONAL:: GfxConfigExplod.exe -fileTo OR -maxDisp OR -displays");
            Console.WriteLine("HINT:: WHEN NO ARGUMENTS ARE GIVEN, PATTERN WILL BE LISTED BASED ON ENUMERATED DISPLAYS");
            Console.WriteLine("**************************************************************************");
        }
    }
}