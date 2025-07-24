using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Threading;
using Microsoft.Diagnostics.Tracing.Session;

namespace EtlCapturer
{
    public static class EtlTracer
    {
        public static readonly int MAX_NUM_PROVIDERS = 6;
        public static readonly string INTEL_GFX_DRIVER = "{6381f857-7661-4b04-9521-288319e75f12}";
        public static readonly string INTEL_GFX_DRIVER_DISPLAY = "{6F556899-027A-45EC-A3F5-C58E7FB94FF5}";
        public static readonly string INTEL_HD_GRAPHICS_KRNL = "{DBBF40DD-5E4F-4528-8A43-BBF62DB6E401}";
        public static readonly string INTEL_GFX_DRIVER_PERF_ANALYSIS = "{90F8AFC2-3F92-4DA3-A4C1-C933A74D2AEC}";
        public static readonly string INTEL_MEDIA = "{4e1c52c9-1d1e-4470-a110-25a9f3ebe1a5}";
        public static readonly string INTEL_GFX_D3D10 = "{AD367E62-97EF-4B20-8235-E8AB49DB0C23}";
        static readonly string etlFolderpath = System.IO.Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), "GfxEvents");
        static TraceEventSession session = null;
        public static string getEventProviderNameStrings(string provider)
        {
            string providerNameString = null;
            switch (provider)
            {
                case "{6381f857-7661-4b04-9521-288319e75f12}":
                    providerNameString = "INTEL_GFX_DRIVER";
                    break;
                case "{6F556899-027A-45EC-A3F5-C58E7FB94FF5}":
                    providerNameString = "INTEL_GFX_DRIVER_DISPLAY";
                    break;
                case "{DBBF40DD-5E4F-4528-8A43-BBF62DB6E401}":
                    providerNameString = "INTEL_HD_GRAPHICS_KRNL";
                    break;
                case "{90F8AFC2-3F92-4DA3-A4C1-C933A74D2AEC}":
                    providerNameString = "INTEL_GFX_DRIVER_PERF_ANALYSIS";
                    break;
                case "{4e1c52c9-1d1e-4470-a110-25a9f3ebe1a5}":
                    providerNameString = "INTEL_MEDIA";
                    break;
                case "{AD367E62-97EF-4B20-8235-E8AB49DB0C23}":
                    providerNameString = "INTEL_GFX_D3D10";
                    break;
                default:
                    providerNameString = "Invalid";
                    break;
            }
            return providerNameString;
        }
        public static string getEventProviderClassId(int providers)
        {
            string provider = null;
            if (providers > EtlTracer.MAX_NUM_PROVIDERS)
            {
                Program.consoleMesage("Invalid Events Provider argument(Provider number)= " + providers + " Max Allowed Event Provider Number= " + EtlTracer.MAX_NUM_PROVIDERS, ConsoleColor.DarkRed, ConsoleColor.Yellow);
                Program.consoleMesage("Continuing with default INTEL_GFX_DRIVER and INTEL_GFX_DRIVER_DISPLAY Events capture", ConsoleColor.Blue);
            }
            else
            {
                switch (providers)
                {
                    case 1:
                        provider = EtlTracer.INTEL_GFX_DRIVER;
                        break;
                    case 2:
                        provider = EtlTracer.INTEL_GFX_DRIVER_DISPLAY;
                        break;
                    case 3:
                        provider = EtlTracer.INTEL_HD_GRAPHICS_KRNL;
                        break;
                    case 4:
                        provider = EtlTracer.INTEL_GFX_DRIVER_PERF_ANALYSIS;
                        break;
                    case 5:
                        provider = EtlTracer.INTEL_MEDIA;
                        break;
                    case 6:
                        provider = EtlTracer.INTEL_GFX_D3D10;
                        break;
                    default:
                        provider = "Invalid";
                        break;
                }
            }
            return provider;
        }
        public static bool startEtlTracing(APP_CONFIG appCfg)
        {
            string etlFilePathWithFileName = System.IO.Path.Combine(Environment.CurrentDirectory, appCfg.EtlFIleName);
            if (File.Exists(etlFilePathWithFileName))
            {
                File.Delete(etlFilePathWithFileName);
            }
            string timeStamp = DateTime.Now.ToString("yyyy-MM-dd-HHmmssffff");
            if (!(TraceEventSession.IsElevated() ?? false))
            {
                Program.consoleMesage("!!!ERROR!!! Make sure command prompt is launched with ADMIN privilages", ConsoleColor.DarkRed, ConsoleColor.Yellow);
                return false;
            }
            try
            {
                session = new TraceEventSession("CustomEtlTraceEvent", etlFilePathWithFileName);
                session.BufferSizeMB = 16;
                foreach (string provider in appCfg.EventsProviders)
                {
                    session.EnableProvider(provider);
                    Program.consoleMesage("Enabled Event Tracing: " + getEventProviderNameStrings(provider), ConsoleColor.Green);
                }
            }
            catch (Exception e)
            {
                Program.consoleMesage("!!!Exception!!! While starting ETL tracing session", ConsoleColor.DarkRed, ConsoleColor.Yellow);
                return false;
            }
            Program.consoleMesage("!!!Started ETL Capture!!!\n", ConsoleColor.Green);
            return true;
        }
        public static bool stopEtlTracing(APP_CONFIG appCfg)
        {
            if (null == session)
            {
                Program.consoleMesage("!!!Error!!! ETL Session is NULL", ConsoleColor.DarkRed, ConsoleColor.Yellow);
                return false;
            }
            try
            {
                bool? status = session?.Stop();
            }
            catch (Exception e)
            {
                Program.consoleMesage("!!!Exception!!! While stopping ETL tracing. Exception Message: " + e.Message, ConsoleColor.DarkRed, ConsoleColor.Yellow);
                return false;
            }
            if (appCfg.DoMerge)
            {
                //mergeETL function to have pass fail messages 
                Program.consoleMesage("!!!ETL Captured Successfully!!!\nETL file info: " + Path.Combine(Environment.CurrentDirectory, appCfg.EtlFIleName) + "\nDuration of Capture in Seconds: " + appCfg.DurationOfCaptureInSeconds, ConsoleColor.Green);
                mergeEtl_Using_Xperf(appCfg.EtlFIleName);
                //mergeETL_UsingGfxEvents_Merge_BatchFile(appCfg.EtlFIleName);
            }
            else
            {
                //if merge not requested, print ETL capture message
                Program.consoleMesage("!!!ETL Captured Successfully!!!\nETL file info: " + Path.Combine(Environment.CurrentDirectory, appCfg.EtlFIleName) + "\nDuration of Capture in Seconds: " + appCfg.DurationOfCaptureInSeconds, ConsoleColor.Green);
            }
            return true;
        }
        private static bool mergeEtl_Using_Xperf(string etlFileName)
        {
            bool isMergeOkay = true;
            string status = null;
            string etlFileNameWithPathInGfxEventsFolder = System.IO.Path.Combine(Environment.CurrentDirectory, etlFileName);
            string xperfFolderPath = Path.Combine(Environment.CurrentDirectory, "xperf\\amd64");
            try
            {
                runProgramOnThread(xperfFolderPath, "xperf.exe", ref status, "-merge " + etlFileNameWithPathInGfxEventsFolder + " " + @Path.Combine(Environment.CurrentDirectory, "Merged_" + etlFileName));
                if (status.Contains("Merged"))  //pass case
                {
                    Program.consoleMesage("!!!ETL Merged Succesfully!!!\nMerged ETL File info: " + Path.Combine(Environment.CurrentDirectory, "Merged_" + etlFileName), ConsoleColor.Green);
                }
                else        //fail case
                {
                    isMergeOkay = false;
                    Program.consoleMesage("!!!ETL Merge FAILED!!!\n xperf.exe output: " + status, ConsoleColor.DarkRed, ConsoleColor.Yellow);
                    Console.WriteLine();
                }
            }
            catch (Exception e)
            {
                Program.consoleMesage("!!!Exception!!! while merging the ETL, Exception Message= " + e.Message, ConsoleColor.DarkRed, ConsoleColor.Yellow);
                return false;
            }
            return isMergeOkay;
        }
        //not using below function for now, using the xperf method to merge the ETL 
        private static bool mergeETL_UsingGfxEvents_Merge_BatchFile(string etlFileName)
        {
            string etlFileNameWithPathInGfxEventsFolder = System.IO.Path.Combine(Environment.CurrentDirectory, etlFileName);
            try
            {
                if (Directory.Exists(etlFolderpath))    //Move saved etl file from VQA tool log folder to GfxEvents folder for the merge 
                {
                    string status = null;
                    runProgramOnThread(etlFolderpath, "Merge.bat", ref status, etlFileNameWithPathInGfxEventsFolder);
                    if (status.Contains("Merged"))
                    {

                        //move the file in app binary folder from GfxEvents
                        string newMergedEtlFileNameWithAppRootPath = Path.Combine(Environment.CurrentDirectory, "Merged_" + etlFileName);

                        if (File.Exists(newMergedEtlFileNameWithAppRootPath))
                            File.Delete(newMergedEtlFileNameWithAppRootPath);   //delete existing merged etl if it is there 
                        File.Move(etlFolderpath + "\\MergedGfxTrace_" + etlFileName, newMergedEtlFileNameWithAppRootPath);
                        Console.WriteLine("!!!ETL Merged Succesfully!!!\nMerged ETL File info: " + newMergedEtlFileNameWithAppRootPath);
                        //we can delete the non merged etl file to save space 
                        //non merged file wont be deleted if merge is not successful 
                        string notMergedEtlFileWithAppRootPath = Path.Combine(Environment.CurrentDirectory, etlFileName);
                        if (File.Exists(notMergedEtlFileWithAppRootPath))
                        {
                            File.Delete(notMergedEtlFileWithAppRootPath);
                            Console.WriteLine("Deleted unmerged ETL file: " + notMergedEtlFileWithAppRootPath);
                        }
                        return true;
                    }
                    else
                    {
                        Console.WriteLine("!!!ETL Merge FAILED!!!\n Merge.bat output: " + status);
                        return false;
                    }
                }
                else
                {
                    Console.WriteLine("!!!Merge FAIL!!! Couldn't Locate \"GfxEvents\" folder with all reuired ETL tracing file on Desktop");
                    return false;
                }
            }
            catch (Exception e)
            {
                Console.WriteLine("!!!Exception while Merging ETL: Exception Message= " + e.Message);
                return false;
            }
        }
        private static void runProgramOnThread(string workingDirectory, string programToRunFileName, ref string _status, string arg1 = null)
        {
            try
            {
                ProcessStartInfo processInfo;
                Process process = null;
                string bathFilePath = System.IO.Path.Combine(workingDirectory, programToRunFileName);
                processInfo = new ProcessStartInfo(bathFilePath);
                processInfo.WorkingDirectory = workingDirectory;
                processInfo.CreateNoWindow = true;
                processInfo.UseShellExecute = false;
                processInfo.Verb = "runas";
                processInfo.Arguments = @arg1;
                //redirect the output 
                processInfo.RedirectStandardOutput = true;
                processInfo.RedirectStandardError = true;
                Thread beginProcess = new Thread(() => process = Process.Start(processInfo));
                beginProcess.Start();
                while (true)
                {
                    System.Threading.ThreadState threadStatus = beginProcess.ThreadState;
                    if (threadStatus == System.Threading.ThreadState.Stopped)
                        break;
                }
                _status = process.StandardError.ReadToEnd();
                Program.consoleMesage("<INFO> Merger output=" + _status, ConsoleColor.Gray);
            }

            catch (Exception e)
            {
                Program.consoleMesage("Exception while merging: Check Xperf Folder Presence...\nMessage= " + e.Message, ConsoleColor.Red);
            }
        }
    }
}
