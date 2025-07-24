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

namespace ImmediateFlips
{
    public class AsyncFlipOptions
    {
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
            CANNONLAKE,
            ICELAKE,
            ICELAKELP,
            ICELAKEHP
        }
        public AsyncFlipOptions()
        {  }
        public bool bHelp = false;
        public bool IsDDRW = false;
        public Platforms Platform = Platforms.UNINITIALIZED;
    }
    class ImmediateFlipsParser
    {
        static bool ASYNCFlips = false;

        public ImmediateFlipsParser()
        { }


        public void LogEvents(TraceEventSource EventSource, AsyncFlipOptions Options, StreamWriter outFile)
        {
            RegisterOutput RegOut = new RegisterOutput();
            if (Options.IsDDRW)
            {
                IntelGfxDriverDisplayTraceEventParser GfxParser = new IntelGfxDriverDisplayTraceEventParser(EventSource);

                GfxParser.FlipAsync += delegate (FlipAddress_t FlipData)
                {
                    //Console.WriteLine("MMIO Async Flips initiated");
                    if (ASYNCFlips == false)
                    {
                        Console.ForegroundColor = ConsoleColor.Green;
                        Console.WriteLine("MMIO Async Flips initiated");
                        outFile.WriteLine("MMIO Async Flips initiated");
                        ASYNCFlips = true;
                        Console.ForegroundColor = ConsoleColor.White;
                    }
                };

                GfxParser.FlipSync += delegate (FlipAddress_t FlipData)
                {
                    //Console.WriteLine("MMIO Sync Flips initiated");
                    if (ASYNCFlips == true)
                    {
                        Console.ForegroundColor = ConsoleColor.Red;
                        Console.WriteLine("MMIO Async Flips Exited");
                        outFile.WriteLine("MMIO Async Flips Exited");
                        ASYNCFlips = false;
                        Console.ForegroundColor = ConsoleColor.White;
                    }
                };
            }
            else
            {
                IntelGfxDriverTraceEventParser GfxParser = new IntelGfxDriverTraceEventParser(EventSource);

                GfxParser.ReportPresentIDFlipDone += delegate (t_PresentID PresentIDData)
                {
                    if (ASYNCFlips == false)
                    {
                        Console.ForegroundColor = ConsoleColor.Green;
                        Console.WriteLine("MMIO Async Flips initiated");
                        outFile.WriteLine("MMIO Async Flips initiated");
                        ASYNCFlips = true;
                        Console.ForegroundColor = ConsoleColor.White;
                    }
                };

                GfxParser.ReportPresentIDVBI += delegate (t_PresentID PresentIDData)
                {
                    if (ASYNCFlips == true)
                    {
                        Console.ForegroundColor = ConsoleColor.Red;
                        Console.WriteLine("MMIO Async Flips Exited");
                        outFile.WriteLine("MMIO Async Flips Exited");
                        ASYNCFlips = false;
                        Console.ForegroundColor = ConsoleColor.White;
                    }
                };
            }
                //GfxParser.CSLBASE_SetDisplayStart +=delegate(t_CSLBASE_SetDisplayStartEntry MMIOFlipData)
                //{
                //    if (MMIOFlipData.bIsASynchMMIOFlip == true && ASYNCFlips == false)
                //    {
                //        Console.ForegroundColor = ConsoleColor.Green;
                //        Console.WriteLine("MMIO Async Flips initiated");
                //        outFile.WriteLine("MMIO Async Flips initiated");
                //        ASYNCFlips = true;
                //        Console.ForegroundColor = ConsoleColor.White;
                //    }
                //    else if (MMIOFlipData.bIsASynchMMIOFlip == false && ASYNCFlips == true)
                //    {
                //        Console.ForegroundColor = ConsoleColor.Red;
                //        Console.WriteLine("MMIO Async Flips Exited");
                //        outFile.WriteLine("MMIO Async Flips Exited");
                //        ASYNCFlips = true;
                //        Console.ForegroundColor = ConsoleColor.White;
                //    }
                //};

                //GfxParser.SetDisplayStart += delegate(t_SetDisplayStart DisplayFlipArgs)
                //{
                //    if (DisplayFlipArgs.IsAsync == true && ASYNCFlips == false)
                //    {
                //        Console.ForegroundColor = ConsoleColor.Green;
                //        Console.WriteLine("MMIO Async Flips initiated");
                //        outFile.WriteLine("MMIO Async Flips initiated");
                //        ASYNCFlips = true;
                //        Console.ForegroundColor = ConsoleColor.White;
                //    }
                //    else if (DisplayFlipArgs.IsAsync == false && ASYNCFlips == true)
                //    {
                //        Console.ForegroundColor = ConsoleColor.Red;
                //        Console.WriteLine("MMIO Async Flips Exited");
                //        outFile.WriteLine("MMIO Async Flips Exited");
                //        ASYNCFlips = true;
                //        Console.ForegroundColor = ConsoleColor.White;
                //    }
                //};

        }
    }
}
