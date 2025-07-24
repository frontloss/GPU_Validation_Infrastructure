using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Diagnostics.Tracing;
using Microsoft.Diagnostics.Tracing.Parsers;
using Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriver;
using Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriverDisplay;
using PlaneStatus;

namespace MPOTracer
{
    public class MPOOptions
    {
        public const int FLIPREGPRINT = 150;
        public enum Platforms
        {
            UNINITIALIZED = 0,
            CHERRYVIEW,
            SKYLAKE,
            KABYLAKE,
            COFFEELAKE,
            WHISKEYLAKE,
            AMBERLAKE,
            COMETLAKE,
            BROXTON,
            GEMINILAKE,
            CANONLAKE,
            ICELAKE,
            ICELAKELP,
            ICELAKEHP
        }
        public MPOOptions()
        {  }
        public bool bHelp = false;
        public bool bMPOFlip = false;
        public bool bColor = false;
        public bool b48Hz = false;
        public bool bSize = false;
        public bool bCSC = false;
        public bool bRotation = false;
        public bool bRegistry = false;
        public bool IsDDRW = false;
        public Platforms Platform = Platforms.UNINITIALIZED;
    }
    class MPODataParser
    {
        static bool CheckMPOStatus = false;
        static bool MPOFlips = false;
        static bool MMIOFlips = false;

        static int MPOFlipCount = 0;
        static int TotalFlipCount = 0;

        public MPODataParser()
        { }


        public void LogEvents(TraceEventSource EventSource, MPOOptions Options, StreamWriter outFile)
        {
            RegisterOutput RegOut = new RegisterOutput();
            if (Options.IsDDRW)
            {
                IntelGfxDriverDisplayTraceEventParser GfxDisplayParser = new IntelGfxDriverDisplayTraceEventParser(EventSource);

                GfxDisplayParser.Mpo3FlipStart += delegate (Mpo3FlipIn_t FlipData)
                {
                    if (MPOFlips == false)
                    {
                        MPOFlips = true;    //MPO flips started
                        Console.ForegroundColor = ConsoleColor.Green;
                        Console.WriteLine();
                        Console.WriteLine();
                        Console.WriteLine("***MPO Flips intiated");
                        Console.WriteLine();
                        Console.WriteLine();
                        Console.ForegroundColor = ConsoleColor.White;
                        outFile.WriteLine("***MPO Flips intiated");
                        outFile.WriteLine();
                        outFile.WriteLine();
                        MPOFlipCount = 1;
                        MMIOFlips = false;
                    }
                    else if (MPOFlips == true)
                    {
                        MPOFlipCount++;
                    }
                    TotalFlipCount++;
                    if (Options.bRegistry && TotalFlipCount % MPOOptions.FLIPREGPRINT == 0 && Options.Platform != MPOOptions.Platforms.UNINITIALIZED)
                    {
                        RegOut.RegOutput(Options, outFile);
                    }
                };

            }
            else
            {

                IntelGfxDriverTraceEventParser GfxParser = new IntelGfxDriverTraceEventParser(EventSource);
                
                GfxParser.DxgkDdiSetVidPnSourceAddressStart += delegate (t_SetVidpnSourceAddressEntry FlipData)
                {
                    if (!MMIOFlips)
                    {
                        MMIOFlips = true;   //MMIO flips have started
                        MPOFlips = false;   //MPO Flips cant exist with MMIO flips
                        MPOFlipCount = 0;           //re-initialize MPOFlipCount to 0
                        Console.ForegroundColor = ConsoleColor.Yellow;
                        Console.WriteLine("********************MMIO Flips started*********************");
                        Console.WriteLine();
                        Console.WriteLine();
                        Console.ForegroundColor = ConsoleColor.White;
                        outFile.WriteLine("********************MMIO Flips started*********************");
                        outFile.WriteLine();
                        outFile.WriteLine();
                    }
                    TotalFlipCount++;
                };
                GfxParser.DxgkDdiSetVidPnSourceAddressStop += delegate (EmptyTraceData Data)
                {

                };
                GfxParser.DxgkDdiSetVidPnSourceAddressWithMultiPlaneOverlayStart += delegate (t_DxgkDdiSetVidPnSourceAddressWithMultiPlaneOverlayEntry MPOFlipData)
                {

                    if (MPOFlips == false)
                    {
                        MPOFlips = true;    //MPO flips started
                        Console.ForegroundColor = ConsoleColor.Green;
                        Console.WriteLine();
                        Console.WriteLine();
                        Console.WriteLine("***MPO Flips intiated for SourceID:" + MPOFlipData.SourceID + " with " + MPOFlipData.PlaneCount + " planes***");
                        Console.WriteLine();
                        Console.WriteLine();
                        Console.ForegroundColor = ConsoleColor.White;
                        outFile.WriteLine("***MPO Flips intiated for SourceID:" + MPOFlipData.SourceID + " with " + MPOFlipData.PlaneCount + " planes***");
                        outFile.WriteLine();
                        outFile.WriteLine();
                        MPOFlipCount = 1;
                        MMIOFlips = false;
                    }
                    else if (MPOFlips == true)
                    {
                        MPOFlipCount++;
                    }
                    TotalFlipCount++;
                    if (Options.bRegistry && TotalFlipCount % MPOOptions.FLIPREGPRINT == 0 && Options.Platform != MPOOptions.Platforms.UNINITIALIZED)
                    {
                        RegOut.RegOutput(Options, outFile);
                    }
                };

                GfxParser.DxgkDdiSetVidPnSourceAddressWithMultiPlaneOverlay3Start += delegate (EmptyTraceData Data)
                {
                    if (MPOFlips == false)
                    {
                        MPOFlips = true;    //MPO flips started
                        Console.ForegroundColor = ConsoleColor.Green;
                        Console.WriteLine();
                        Console.WriteLine();
                        Console.WriteLine("***MPO Flips intiated");
                        Console.WriteLine();
                        Console.WriteLine();
                        Console.ForegroundColor = ConsoleColor.White;
                        outFile.WriteLine("***MPO Flips intiated");
                        outFile.WriteLine();
                        outFile.WriteLine();
                        MPOFlipCount = 1;
                        MMIOFlips = false;
                    }
                    else if (MPOFlips == true)
                    {
                        MPOFlipCount++;
                    }
                    TotalFlipCount++;
                    if (Options.bRegistry && TotalFlipCount % MPOOptions.FLIPREGPRINT == 0 && Options.Platform != MPOOptions.Platforms.UNINITIALIZED)
                    {
                        RegOut.RegOutput(Options, outFile);
                    }
                };

                GfxParser.DxgkDdiSetVidPnSourceAddressWithMultiPlaneOverlay3Plane += delegate (t_DxgkDdiSetVidPnSourceAddressWithMultiPlaneOverlay3Info PlaneInfo)
                {

                };

                GfxParser.DxgkDdiSetVidPnSourceAddressWithMultiPlaneOverlayStop += delegate (EmptyTraceData Data)
                {

                };
                GfxParser.DxgkDdiCheckMultiPlaneOverlaySupportStart += delegate (t_DxgkDdiCheckMultiPlaneOverlaySupportEntry CheckMPOData)
                {

                };
                GfxParser.DxgkDdiCheckMultiPlaneOverlaySupportStop += delegate (t_DxgkDdiCheckMultiPlaneOverlaySupportExit CheckMPOData)
                {
                    //Console.ForegroundColor = ConsoleColor.Magenta;
                    //Console.WriteLine("Check MPO {0}", CheckMPOData.Supported);
                    if (CheckMPOData.Supported == true)
                    {
                        CheckMPOStatus = true;      //CheckMPO passed
                                                    //MMIOFlips = false;          //MMIO flips should stop, when CheckMPO has passed
                                                    //Console.ForegroundColor = ConsoleColor.Green;
                                                    //Console.WriteLine("CheckMPO PASSED");
                                                    //Console.ForegroundColor = ConsoleColor.White;
                                                    //outFile.WriteLine("WARNING: MPO capability check Failed");

                    }
                    else
                    {
                        Console.ForegroundColor = ConsoleColor.Yellow;
                        Console.WriteLine("WARNING: MPO capability check Failed");
                        Console.ForegroundColor = ConsoleColor.White;
                        outFile.WriteLine("WARNING: MPO capability check Failed");
                        CheckMPOStatus = false;     // CheckMPO Failed
                        MPOFlips = false;           // MPO flips cant start when CheckMPO failed
                        MPOFlipCount = 0;           //re-initialize MPOFlipCount to 0
                    }
                };

                GfxParser.DxgkDdiCheckMultiPlaneOverlaySupport3Stop += delegate (t_DxgkDdiCheckMultiPlaneOverlaySupport3 CheckMPOData)
                {
                    if (CheckMPOData.Supported == true)
                    {

                        CheckMPOStatus = true;      //CheckMPO passed
                        //MMIOFlips = false;          //MMIO flips should stop, when CheckMPO has passed
                        //Console.ForegroundColor = ConsoleColor.Green;
                        //Console.WriteLine("CheckMPO PASSED");
                        //Console.ForegroundColor = ConsoleColor.White;
                        //outFile.WriteLine("WARNING: MPO capability check Failed");

                    }
                    else
                    {
                        Console.ForegroundColor = ConsoleColor.Yellow;
                        Console.WriteLine("WARNING: MPO capability check Failed");
                        Console.ForegroundColor = ConsoleColor.White;
                        outFile.WriteLine("WARNING: MPO capability check Failed");
                        CheckMPOStatus = false;     // CheckMPO Failed
                        MPOFlips = false;           // MPO flips cant start when CheckMPO failed
                        MPOFlipCount = 0;           //re-initialize MPOFlipCount to 0
                    }
                };
            }
        }
    }
}
