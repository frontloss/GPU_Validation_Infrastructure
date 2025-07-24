using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace EtlCapturer
{
    public class APP_CONFIG
    {
        public string EtlFIleName;
        public int StartEtlCaptureAfterSeconds;
        public int DurationOfCaptureInSeconds;
        public List<string> EventsProviders;
        public bool DoMerge;
        public bool GenerateFlipPatternCsvFileOnline;
        public bool GenerateFlipPatternCsvFileOffline;
    };
    public static class Program
    {        
        //entry point 
        static void Main(string[] args)
        {
            APP_CONFIG appCfg = parseCommandLineArguments(args);
            captureEtl(appCfg);
        }
        private static void printUsage()
        {
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("\n******************************************Usage******************************************\nEtlCapturer.exe -o <\"etl filename with/without extension and without space in name\"> " +
                    "-d <integer value of duration of etl capture in seconds(1-900)> -e <all/3-6/3,4,5,6:additional events if needed alogn with GFX and DISPLAY events> " +
                    "-s <integer value for seconds, ETL capture will start after specified number of seconds>" +
                    "-m <no options:add just -m if needed to merge else this argument need not be entered>\n" + //\nNote: Copy the driver \"GfxEvents\" folder on desktop for merging\n"
                    "Example 1: EtlCapturer.exe -o test_example -d 5 \n" +
                    "Example 2: EtlCapturer.exe -o test_example.etl -d 5 -s 3\n" +
                    "Example 3: EtlCapturer.exe -o test_example -d 5 -s 4 -e 4\n" +
                    "Example 4: EtlCapturer.exe -o test_example.etl -d 5 -e all\n" +
                    "Example 5: EtlCapturer.exe -o test_example -d 5 -e 3,5 -m \n");
            Console.Write("******************************************Arguments inforamtion******************************************\n" +
                "---------------------------------------------------------------------------------------------------\n" +
                "-o: output ETL file name --------> (Mandatory)\n" +
                "---------------------------------------------------------------------------------------------------\n" +
                "-d: duration of ETL events capture --------> (Optional) 10 Seconds default capture time\n" +
                "---------------------------------------------------------------------------------------------------\n" +
                "-s: ETL events capture to begin after the specified number of seconds --------> (Optional)\n" +
                "---------------------------------------------------------------------------------------------------\n" +
                "-e: additional events capture along with GFX and DISPLAY events --------> (Optional)\nAdditioanl Events Supported:\n" +
                "1. INTEL_GFX_DRIVER: {6381f857-7661-4b04-9521-288319e75f12} ---------> Default Enabled\n" +
                "2. INTEL_GFX_DRIVER_DISPLAY: {6F556899-027A-45EC-A3F5-C58E7FB94FF5} ---------> Default Enabled\n" +
                "3. INTEL_HD_GRAPHICS_KRNL: {DBBF40DD-5E4F-4528-8A43-BBF62DB6E401}\n" +
                "4. INTEL_GFX_DRIVER_PERF_ANALYSIS: {90F8AFC2-3F92-4DA3-A4C1-C933A74D2AEC}\n" +
                "5. INTEL_MEDIA: {4e1c52c9-1d1e-4470-a110-25a9f3ebe1a5}\n" +
                "6. INTEL_GFX_D3D10: {AD367E62-97EF-4B20-8235-E8AB49DB0C23}\n" +
                "Enter the number of event as command line argument: Allowed options: \nall: for all the events capture \n<1-4>: Single event entry alogn with GFX and DISPLAY events(GFX and DISPLAY components will be captured by default)" +
                "\n<1,2,3,4>:Multiple events entry along with GFX and DISPLAY\n" +
                "---------------------------------------------------------------------------------------------------\n" +
                "-m: Merge ETL --------> (Optional)\n" +
                "---------------------------------------------------------------------------------------------------\n" +
                "-genFlipPat: generate the flip pattern with newly captured ETL --------> (Optional)\n" +
                "---------------------------------------------------------------------------------------------------\n" );
           Console.ResetColor();
        }
        public static void consoleMesage(string message, ConsoleColor textColor, ConsoleColor textBackgroundColor = ConsoleColor.Black)
        {
            Console.ForegroundColor = textColor;
            Console.BackgroundColor = textBackgroundColor;
            Console.WriteLine(message);
            Console.ResetColor();
        }
        public static APP_CONFIG parseCommandLineArguments(string[] argc)
        {
            if(argc.Length < 3)
            {
                consoleMesage("!!!ERROR!!! Insufficient Arguments", ConsoleColor.DarkRed, ConsoleColor.Yellow);
                printUsage();
                Environment.Exit(0);
            }
            APP_CONFIG appCfg = new APP_CONFIG();
            try
            {
                appCfg.EventsProviders = new List<string>();
                //default event providers initialization 
                appCfg.DurationOfCaptureInSeconds = 10;             //default capture of 10 seconds 
                appCfg.EventsProviders.Add(EtlTracer.getEventProviderClassId(1));    //GFX
                appCfg.EventsProviders.Add(EtlTracer.getEventProviderClassId(2));    //DISPLAY
                appCfg.StartEtlCaptureAfterSeconds = 0;             //Default start immediate 
                bool mandatoryArgument_etlOutputFIle = false;
                bool isOfflineOnlyFlipPatternCsvGeneration = true;  //only if need to dump flip pattern from etl : this will be set false if -s -d are set as these args are set only if new etl to be generated
                for (int i = 0; i < argc.Length; i++)
                {
                    if (argc[i] == "-s")
                    {
                        i++;
                        if (i >= argc.Length)
                        {
                            consoleMesage("Error Processing Command line argument: -s, do re-check usage of -s arguments", ConsoleColor.DarkRed, ConsoleColor.Yellow);
                            Environment.Exit(0);
                        }
                        else
                        {
                            appCfg.StartEtlCaptureAfterSeconds = Convert.ToInt32(argc[i]);
                        }
                    }
                    else if (argc[i] == "-o")
                    {
                        i++;
                        if (i >= argc.Length)
                        {
                            consoleMesage("Error Processing Command line argument: -o, do re-check usage of -o arguments", ConsoleColor.DarkRed, ConsoleColor.Yellow);
                            Environment.Exit(0);
                        }
                        else
                        {
                            if (argc[i].Contains(".etl"))   //check if etl ext is given in command line arg
                                appCfg.EtlFIleName = argc[i];
                            else
                                appCfg.EtlFIleName = argc[i] + ".etl";  //add etl ext if not given in command line argument 
                            mandatoryArgument_etlOutputFIle = true;
                        }
                    }
                    else if (argc[i] == "-d")
                    {
                        i++;
                        isOfflineOnlyFlipPatternCsvGeneration = false;   //dump freshly
                        if (i >= argc.Length)
                        {
                            consoleMesage("Error Processing Command line argument: -d, do re-check usage of -d arguments", ConsoleColor.DarkRed, ConsoleColor.Yellow);
                            Environment.Exit(0);
                        }
                        else
                        {
                            if (Convert.ToInt32(argc[i]) > 0 && Convert.ToInt32(argc[i]) <= 900) //1 sec to 15 mins 
                            {
                                appCfg.DurationOfCaptureInSeconds = Convert.ToInt32(argc[i]);
                            }
                            else
                            {
                                appCfg.DurationOfCaptureInSeconds = 10;
                                consoleMesage("!!!Warning!!! -d Argument: allowed number between 1-900\n setting default duration of 10 seconds", ConsoleColor.Yellow);
                            }
                        }
                    }
                    else if(argc[i] == "-e")
                    {
                        i++;
                        if (i >= argc.Length)
                        {
                            consoleMesage("Error Processing Command line argument: -e, do re-check usage of -e arguments", ConsoleColor.DarkRed, ConsoleColor.Yellow);
                            Environment.Exit(0);
                        }
                        else
                        {
                            if (argc[i] == "all")
                            {
                                for (int j = 3; j <= EtlTracer.MAX_NUM_PROVIDERS; j++)
                                    appCfg.EventsProviders.Add(EtlTracer.getEventProviderClassId(j));    //add all from 2-5 index: 0 and 1 added by default 
                            }
                            else if (!argc[i].Contains(","))     //single entry passed by user 
                            {
                                if (Convert.ToInt32(argc[i]) != 1 && Convert.ToInt32(argc[i]) != 2)       //ignore 1 GFX and 2 DISPLAY providers as they are added by default 
                                {
                                    string provider = EtlTracer.getEventProviderClassId(Convert.ToInt32(argc[i]));
                                    if (provider != null)   //check for invalid null 
                                        appCfg.EventsProviders.Add(provider);    //single try always 
                                }
                            }
                            else if (argc[i].Contains(","))     //multiple entry passed by user 
                            {
                                string[] argumentsEvents = argc[i].Split(',');
                                for (int j = 0; j < argumentsEvents.Length; j++)
                                {
                                    if (Convert.ToInt32(argumentsEvents[j]) != 1 && Convert.ToInt32(argumentsEvents[j]) != 2)       //ignore 1 GFX and 2 DISPLAY providers as they are added by default 
                                    {
                                        string provider = EtlTracer.getEventProviderClassId(Convert.ToInt32(argumentsEvents[j]));
                                        if (provider != null)    //check for invlid null entry for argument more than max num of providers, 
                                            appCfg.EventsProviders.Add(provider);
                                    }
                                }
                            }
                        }
                    }
                    else if (argc[i] == "-m")   //for this GfxEvents folder should be on Desktop with all required custom driver files 
                    {
                        appCfg.DoMerge = true;
                    }
                    else if(argc[i] == "-genFlipPat")
                    {
                        if(isOfflineOnlyFlipPatternCsvGeneration == true)
                        {
                            appCfg.GenerateFlipPatternCsvFileOffline = true;
                            appCfg.GenerateFlipPatternCsvFileOnline = false;
                        }
                        else
                        {
                            appCfg.GenerateFlipPatternCsvFileOnline = true;
                            appCfg.GenerateFlipPatternCsvFileOffline = false;
                        }
                    }
                }
                if(!mandatoryArgument_etlOutputFIle)
                {
                    consoleMesage("!!!Error!!! while processing mandatory arguments, do re-check mandatory arguments", ConsoleColor.DarkRed, ConsoleColor.Yellow);
                    printUsage();
                    Environment.Exit(0);
                }
            }
            catch(Exception e)
            {
                printUsage();
                consoleMesage("!!!Exception!!! while processing command line arguments, do re-check usage, Exception Message: " + e.Message, ConsoleColor.DarkRed, ConsoleColor.Yellow);
                Environment.Exit(0);
            }
            return appCfg;
        }
       
        public static void captureEtl(APP_CONFIG appCfg)
        {
            if (appCfg.GenerateFlipPatternCsvFileOnline)
            {
                consoleMesage("Starting ETL capture after " + appCfg.StartEtlCaptureAfterSeconds + " seconds", ConsoleColor.Green);
                Thread.Sleep(appCfg.StartEtlCaptureAfterSeconds * 1000);
                EtlTracer.startEtlTracing(appCfg);
                Thread.Sleep(appCfg.DurationOfCaptureInSeconds * 1000); // multiply by 1000 for seconds count 
                EtlTracer.stopEtlTracing(appCfg);
                FlipDataJsonParser flipDataJsonParser = new FlipDataJsonParser();
                flipDataJsonParser.dumpFlipPatternToCsv(appCfg.EtlFIleName);
            }
            else if(appCfg.GenerateFlipPatternCsvFileOffline)
            {
                FlipDataJsonParser flipDataJsonParser = new FlipDataJsonParser();
                flipDataJsonParser.dumpFlipPatternToCsv(appCfg.EtlFIleName);
            }
            else        //no need to generate flip pattern case 
            {
                consoleMesage("Starting ETL capture after " + appCfg.StartEtlCaptureAfterSeconds + " seconds", ConsoleColor.Green);
                Thread.Sleep(appCfg.StartEtlCaptureAfterSeconds * 1000);
                EtlTracer.startEtlTracing(appCfg);
                Thread.Sleep(appCfg.DurationOfCaptureInSeconds * 1000); // multiply by 1000 for seconds count 
                EtlTracer.stopEtlTracing(appCfg);
            }
        }
    }
}
