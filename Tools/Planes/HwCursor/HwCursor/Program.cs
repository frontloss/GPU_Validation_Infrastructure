using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Diagnostics.Tracing.Session;
using Microsoft.Diagnostics.Tracing;

namespace HardwareCursor
{
    class Program
    {
        static void Main(string[] args)
        {
            MPOOptions Options = new MPOOptions();
            if (0 == args.Length)
            {
                Options.bMPOFlip = true;
            }
            foreach (string option in args)
            {
                String UpperOption = option.ToUpper();
                if (UpperOption.Equals("HELP"))
                {
                    Options.bHelp = true;
                }
                if (UpperOption.Equals("-REG"))
                {
                    Options.bRegistry = true;
                }
                else if (UpperOption.StartsWith("-DDRW"))
                {
                    Options.IsDDRW = true;
                }
                else
                {
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine("Ignoring Unsupported Option {0}", option);
                    Console.ForegroundColor = ConsoleColor.Gray;
                }
            }
            if(Options.bHelp)
            {
                Console.ForegroundColor = ConsoleColor.Blue;
                Console.WriteLine("Help");
                Console.ForegroundColor = ConsoleColor.Gray;
            }
            else
            {
                if (!(TraceEventSession.IsElevated() ?? false))
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("Run the Analyzer in Admin mode");
                    Console.ForegroundColor = ConsoleColor.Gray;
                    return;
                }

                var sessionName = "MPOEvents";
                using (var session = new TraceEventSession(sessionName))
                {
                    MPODataParser mpoDataParser = new MPODataParser();
                    StreamWriter outFile = File.CreateText("MPOTraceLog.txt");
                    Console.CancelKeyPress += delegate(object sender, ConsoleCancelEventArgs e)
                    {
                        session.Dispose();
                        outFile.Close();
                    };

                    mpoDataParser.LogEvents(session.Source, Options, outFile);
                    // At this point we have created a TraceEventSession, hooked it up to a TraceEventSource, and hooked the
                    // TraceEventSource to a TraceEventParser (you can do several of these), and then hooked up callbacks
                    // up to the TraceEventParser (again you can have several).  However we have NOT actually told any
                    // provider (EventSources) to actually send any events to our TraceEventSession.  
                    // We do that now.  

                    // Enable my provider, you can call many of these on the same session to get events from other providers.  
                    // Because this EventSource did not define any keywords, I can only turn on all events or none. 
                    if(!Options.IsDDRW)
                    {
                        var restarted = session.EnableProvider("{6381f857-7661-4b04-9521-288319e75f12}");//"Intel-Gfx-Driver");
                    }
                    else
                    {
                        var restarted = session.EnableProvider("{6F556899-027A-45EC-A3F5-C58E7FB94FF5}");//"Intel-Gfx-Driver-Display");
                    }
                    session.Source.Process();
                    Console.WriteLine();
                    Console.WriteLine("Stopping the collection of events.");

                }  
            }
        }
    }
}
