using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Diagnostics.Tracing.Session;
using Microsoft.Diagnostics.Tracing;

namespace ImmediateFlips
{
    class Program
    {
        static void Main(string[] args)
        {
            AsyncFlipOptions Options = new AsyncFlipOptions();
            foreach (string option in args)
            {
                String UpperOption = option.ToUpper();
                if (UpperOption.Equals("HELP"))
                {
                    Options.bHelp = true;
                }
                if (UpperOption.StartsWith("-P:"))
                {

                    String Platform = UpperOption.Substring(UpperOption.IndexOf(':') + 1);
                    switch(Platform){
                        case "SKL":
                            Options.Platform = AsyncFlipOptions.Platforms.SKYLAKE;
                            break;
                        case "KBL":
                            Options.Platform = AsyncFlipOptions.Platforms.KABYLAKE;
                            break;
                        case "CFL":
                            Options.Platform = AsyncFlipOptions.Platforms.COFFEELAKE;
                            break;
                        case "WHL":
                            Options.Platform = AsyncFlipOptions.Platforms.WHISKEYLAKE;
                            break;
                        case "AML":
                            Options.Platform = AsyncFlipOptions.Platforms.AMBERLAKE;
                            break;
                        case "CML":
                            Options.Platform = AsyncFlipOptions.Platforms.COMETLAKE;
                            break;
                        case "BXT":
                        case "APL":
                            Options.Platform = AsyncFlipOptions.Platforms.BROXTON;
                            break;
                        case "GLK":
                            Options.Platform = AsyncFlipOptions.Platforms.GEMINILAKE;
                            break;
                        case "CNL":
                            Options.Platform = AsyncFlipOptions.Platforms.CANNONLAKE;
                            break;
                        case "CHV":
                            Options.Platform = AsyncFlipOptions.Platforms.CHERRYVIEW;
                            break;
                        case "ICL":
                            Options.Platform = AsyncFlipOptions.Platforms.ICELAKE;
                            break;
                        case "ICLLP":
                            Options.Platform = AsyncFlipOptions.Platforms.ICELAKELP;
                            break;
                        case "ICLHP":
                            Options.Platform = AsyncFlipOptions.Platforms.ICELAKEHP;
                            break;
                        default:
                            Options.Platform = AsyncFlipOptions.Platforms.UNINITIALIZED;
                            break;
                    }
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
                    ImmediateFlipsParser AsyncFlipParser = new ImmediateFlipsParser();
                    StreamWriter outFile = File.CreateText("MPOTraceLog.txt");
                    Console.CancelKeyPress += delegate(object sender, ConsoleCancelEventArgs e)
                    {
                        session.Dispose();
                        outFile.Close();
                    };

                    AsyncFlipParser.LogEvents(session.Source, Options, outFile);
                    // At this point we have created a TraceEventSession, hooked it up to a TraceEventSource, and hooked the
                    // TraceEventSource to a TraceEventParser (you can do several of these), and then hooked up callbacks
                    // up to the TraceEventParser (again you can have several).  However we have NOT actually told any
                    // provider (EventSources) to actually send any events to our TraceEventSession.  
                    // We do that now.  

                    // Enable my provider, you can call many of these on the same session to get events from other providers.  
                    // Because this EventSource did not define any keywords, I can only turn on all events or none.  
                    if (!Options.IsDDRW)
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
