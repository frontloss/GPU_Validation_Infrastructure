using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EtlCapturer
{
    public class FlipDataJsonParser
    {
        public static class EtlParsedJsonFileNames
        {
            public const string CommonData = @".\EtlParser\commonData.json";
            public const string DebugMessages = @".\EtlParser\dbgMsgData.json";
            public const string DisplayDetectData = @"DisplayDetectData.json";
            public const string DisplayDiagnosticsData = @"displayDiagnosticsData.json";
            public const string DcpdData = @".\EtlParser\dpcdData.json";
            public const string DpstData = @".\EtlParser\dpstData.json";
            public const string FlipData = @".\EtlParser\flipData.json";
            public const string FunctionData = @".\EtlParser\functionData.json";
            public const string I2cData = @".\EtlParser\I2cData.json";
            public const string InterruptData = @".\EtlParser\interruptData.json";
            public const string MmioData = @".\EtlParser\mmioData.json";
            public const string PsrData = @".\EtlParser\psrData.json";
            public const string VbiData = @".\EtlParser\vbiData.json";
        };
        public List<FlipData> getFlipDataFromEtl(string etlFilePath)
        {
            dumpEtlDataIntoJson(etlFilePath);
            List<FlipData> flipData = new List<FlipData>();
            try
            {                
                using (StreamReader r = new StreamReader(EtlParsedJsonFileNames.FlipData))
                {
                    string json = r.ReadToEnd();
                    flipData = JsonConvert.DeserializeObject<List<FlipData>>(json);
                    return flipData;
                }
            }
            catch(Exception e)
            {
                return flipData;
            }
        }
        public void dumpFlipPatternToCsv(string fileName)
        {
            List<FlipData> flipData = getFlipDataFromEtl(fileName);
            List<int> uniqueThradIds = getUniqueThreadIdOfMpoFlip_Start(flipData);
            //need to fetch flip pattern per thread ID
            if (flipData.Count > 0)
            {
                for (int threadIdCounter = 0; threadIdCounter < uniqueThradIds.Count; threadIdCounter++)
                {
                    List<double> timeStamps = new List<double>();
                    for (int i = 0; i < flipData.Count; i++)
                    {
                        if (flipData[i].TaskName == "Mpo3Flip" && flipData[i].Opcode == "Start")
                        {
                            if(flipData[i].ThreadId == uniqueThradIds[threadIdCounter])
                                timeStamps.Add(flipData[i].TimeStamp);
                        }
                    }
                    List<double> flipPattern = new List<double>();
                    for (int i = 0; i < timeStamps.Count - 1; i++)
                    {
                        flipPattern.Add(timeStamps[i + 1] - timeStamps[i]);
                    }
                    if (flipPattern.Count > 1)   //write to file only if the flippattern count is more than 1                     
                        writeToCsv("TID_" + uniqueThradIds[threadIdCounter] + "_" + fileName, flipPattern);                       
                }
            }
            else
            {
                Program.consoleMesage("Did not find any valid flip pattern from ETL, ETL data returned NULL(ETL data fetch from: Display->Mpo3Flip->Start)", ConsoleColor.Red);
            }
        }
        public List<int> getUniqueThreadIdOfMpoFlip_Start(List<FlipData> flipData)
        {
            List<int> AllThreadIdList = new List<int>();
            for (int i = 0; i < flipData.Count; i++)
            {
                if (flipData[i].TaskName == "Mpo3Flip" && flipData[i].Opcode == "Start")
                {
                    AllThreadIdList.Add(flipData[i].ThreadId);
                }
            }
            List<int> uniqueThreadIds = AllThreadIdList.Distinct().ToList();

            return uniqueThreadIds;
        }
        private void writeToCsv(string fileName, List<double> flipPattern)
        {
            string[] file = fileName.Split('.');
            fileName = "FlipPattern_" + file[0] + ".csv";
            //delete file if exists 
            if (File.Exists(fileName))
            {
                File.Delete(fileName);
            }
            try
            {
                using (var w = new StreamWriter(fileName))
                {
                    for (int i = 0; i < flipPattern.Count; i++)
                    {
                        w.WriteLine(flipPattern[i]);
                    }
                    w.Flush();
                    w.Close();
                    w.Dispose();
                    Program.consoleMesage("Flip Pattern dumped in " + fileName, ConsoleColor.Green);
                }
            }
            catch(Exception ex)
            {
                Program.consoleMesage("Exception while writing Flip Pattern To CSV File: " + fileName + "\nMessage= " + ex.Message, ConsoleColor.Red);
            }
        }
        private void dumpEtlDataIntoJson(string etlFilePath)
        {
            try
            {
                string filePath = Path.Combine(Directory.GetCurrentDirectory(), etlFilePath);
                ProcessStartInfo processInfo;
                Process process;
                processInfo = new ProcessStartInfo(@"EtlParser.exe");
                processInfo.WorkingDirectory = @".\EtlParser";
                processInfo.Arguments = @filePath;
                processInfo.CreateNoWindow = true;
                process = Process.Start(processInfo);
                process.WaitForExit();
                process.Dispose();
                Program.consoleMesage("Dumped ETL data into respective JSON files", ConsoleColor.Green);
            }
            catch(Exception e)
            {
                Program.consoleMesage("Exception while using EtlParser.exe to dump etl data into JSON files...\nMessage= " + e.Message, ConsoleColor.Red);
            }
        }
    }
    public class FlipData
    {
        public int SourceId { get; set; }
        public int PlaneCount { get; set; }
        public long Duration { get; set; }
        public float SoftwareOverhead { get; set; }
        public float FlipDoneTime { get; set; }
        public bool IsAllParam { get; set; }
        public bool IsAddressOnly { get; set; }
        public string Pipe { get; set; }
        public int InputFlags { get; set; }
        public int OutputFlags { get; set; }
        public Planeinfolist[] PlaneInfoList { get; set; }
        public Planedetailslist[] PlaneDetailsList { get; set; }
        public Flipallparamlist[] FlipAllParamList { get; set; }
        public Flipaddresslist[] FlipAddressList { get; set; }
        public object[] NotifyVSyncInfoList { get; set; }
        public Notifyvsynclayerlist[] NotifyVSyncLayerList { get; set; }
        public Mmiodatalist[] MmioDataList { get; set; }
        public float TimeStamp { get; set; }
        public string Level { get; set; }
        public string TaskName { get; set; }
        public string Opcode { get; set; }
        public int ThreadId { get; set; }
    }

    public class Planeinfolist
    {
        public int LayerIndex { get; set; }
        public object Flags { get; set; }
        public int PresentId { get; set; }
        public long Reserved { get; set; }
        public float TimeStamp { get; set; }
        public string Level { get; set; }
        public string TaskName { get; set; }
        public int Opcode { get; set; }
        public int ThreadId { get; set; }
    }

    public class Planedetailslist
    {
        public long MaxImmFlipLine { get; set; }
        public int PlaneAttribFlag { get; set; }
        public int Blend { get; set; }
        public int ClrSpace { get; set; }
        public int Rotation { get; set; }
        public int StretchQuality { get; set; }
        public int SDRWhiteLevel { get; set; }
        public int SrcLeft { get; set; }
        public int SrcTop { get; set; }
        public int SrcRight { get; set; }
        public int SrcBottom { get; set; }
        public int DestLeft { get; set; }
        public int DestTop { get; set; }
        public int DestRight { get; set; }
        public int DestBottom { get; set; }
        public int ClipLeft { get; set; }
        public int ClipTop { get; set; }
        public int ClipRight { get; set; }
        public int ClipBottom { get; set; }
        public int DirtyRectLeft { get; set; }
        public int DirtyRectTop { get; set; }
        public int DirtyRectRight { get; set; }
        public int DirtyRectBottom { get; set; }
        public float TimeStamp { get; set; }
        public string Level { get; set; }
        public string TaskName { get; set; }
        public int Opcode { get; set; }
        public int ThreadId { get; set; }
    }

    public class Flipallparamlist
    {
        public string Pipe { get; set; }
        public int PlaneID { get; set; }
        public int Enabled { get; set; }
        public string PixelFmt { get; set; }
        public int SurfMemType { get; set; }
        public int ScanX { get; set; }
        public int ScanY { get; set; }
        public int Orientation { get; set; }
        public int PosX { get; set; }
        public int PosY { get; set; }
        public long Address { get; set; }
        public int Rsvd { get; set; }
        public string FeatureFlags { get; set; }
        public int ScanLineCount { get; set; }
        public int FrameCount { get; set; }
        public float TimeStamp { get; set; }
        public string Level { get; set; }
        public string TaskName { get; set; }
        public int Opcode { get; set; }
        public int ThreadId { get; set; }
    }

    public class Flipaddresslist
    {
        public string Pipe { get; set; }
        public int PlaneID { get; set; }
        public bool Async { get; set; }
        public int Address { get; set; }
        public int ScanLineCount { get; set; }
        public int FrameCount { get; set; }
        public long DisplayTime { get; set; }
        public int PresentationDelay { get; set; }
        public int AddressUv { get; set; }
        public bool IsSwFlipQ { get; set; }
        public float TimeStamp { get; set; }
        public string Level { get; set; }
        public string TaskName { get; set; }
        public int Opcode { get; set; }
        public int ThreadId { get; set; }
    }

    public class Notifyvsynclayerlist
    {
        public int LayerIndex { get; set; }
        public int PresentID { get; set; }
        public int Flags { get; set; }
        public float TimeStamp { get; set; }
        public string Level { get; set; }
        public string TaskName { get; set; }
        public int Opcode { get; set; }
        public int ThreadId { get; set; }
    }

    public class Mmiodatalist
    {
        public float TimeStamp { get; set; }
        public string Level { get; set; }
        public string TaskName { get; set; }
        public int Opcode { get; set; }
        public int ThreadId { get; set; }
        public bool IsWrite { get; set; }
        public int Offset { get; set; }
        public long Data { get; set; }
    }
}
