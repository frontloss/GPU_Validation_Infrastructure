using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;

namespace PlaneScaler
{
    class MPOPlaneScaler
    {
        public enum Platforms
        {
            UNINITIALIZED = 0,
            CHERRYVIEW,
            SKYLAKE,
            KABYLAKE,
            COFFEELAKE,
            BROXTON,
            GEMINILAKE,
            CANNONLAKE,
            ICELAKE,
            ICELAKELP,
            ICELAKEHP
        }
        public static Platforms PlatformID = Platforms.UNINITIALIZED;
        public static bool IsDDRW = false;

        const uint GENENABLEMASK = 0x80000000;
        const uint CHVENABLEMASK = 0x00000001;
        const uint PIPECSCMASK = 0x00800000;
        const uint PLANECSCMASK = 0x00080000;

        static void Main(string[] args)
        {
            //MPOPlaneScaler mpoPlaneScaler = new MPOPlaneScaler();
            StreamWriter sw = File.CreateText("PlaneScaler_Log.txt");
            int duration = 1;
            int interval = 3;
            int timeCount = 0;
            int piIndex = 0, plIndex = 0;

            if (0 == args.Length)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("Unsupported platform !!!");
                Console.ForegroundColor = ConsoleColor.White;
                Console.ReadLine();
                return;
            }

            foreach (string option in args)
            {
                String UpperOption = option.ToUpper();
                if (UpperOption.Equals("HELP"))
                {
                    PrintHelp();
                    return;
                }
                else if (UpperOption.StartsWith("-P:"))
                {
                    String Platform = UpperOption.Substring(UpperOption.IndexOf(':') + 1);
                    switch (Platform)
                    {
                        case "CHV":
                            PlatformID = Platforms.CHERRYVIEW;
                            break;
                        case "KBL":
                        case "CFL":
                            PlatformID = Platforms.KABYLAKE;
                            break;
                        case "SKL":
                            PlatformID = Platforms.SKYLAKE;
                            break;
                        case "BXT":
                            PlatformID = Platforms.BROXTON;
                            break;
                        case "GLK":
                            PlatformID = Platforms.GEMINILAKE;
                            break;
                        case "CNL":
                            PlatformID = Platforms.CANNONLAKE;
                            break;
                        case "ICL":
                            PlatformID = Platforms.ICELAKE;
                            break;
                        case "ICLLP":
                            PlatformID = Platforms.ICELAKELP;
                            break;
                        case "ICLHP":
                            PlatformID = Platforms.ICELAKEHP;
                            break;
                        default:
                            PlatformID = Platforms.UNINITIALIZED;
                            break;
                    }
                }
                else if (UpperOption.StartsWith("-D:"))
                {
                    String durationStr = UpperOption.Substring(UpperOption.IndexOf(':') + 1);
                    if (!int.TryParse(durationStr, out duration))
                    {
                        Console.ForegroundColor = ConsoleColor.Red;
                        Console.WriteLine("Incorrect Duration !!!");
                        Console.ForegroundColor = ConsoleColor.White;
                        Console.ReadLine();
                    }
                }
                else if (UpperOption.StartsWith("-I:"))
                {
                    String intervalStr = UpperOption.Substring(UpperOption.IndexOf(':') + 1);
                    if (!int.TryParse(intervalStr, out interval))
                    {
                        Console.ForegroundColor = ConsoleColor.Red;
                        Console.WriteLine("Incorrect Interval !!!");
                        Console.ForegroundColor = ConsoleColor.White;
                        Console.ReadLine();
                    }
                }
                else if(UpperOption.StartsWith("-DDRW"))
                {
                    IsDDRW = true;
                }
                else
                {
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine("Ignoring Unsupported Option {0}", option);
                    Console.ForegroundColor = ConsoleColor.Gray;
                    return;
                }
            }

            uint[][] RegisterOffset = GetRegisterOffSetforPlatform(PlatformID);
            String[][] RegisterLabel = GetRegisterLabelforPlatform(PlatformID);
            while (true)
            {
                for (piIndex = 0; piIndex < RegisterOffset.GetLength(0); piIndex++)
                {
                    int planeScalerCount = 0;
                    for (plIndex = 0; plIndex < RegisterOffset[piIndex].Length; plIndex++)
                    {
                        uint RegValue = 0;
                        if (RegisterInterface.Instance.ReadWriteRegister(RegisterInterface.RegisterOperation.READ, RegisterOffset[piIndex][plIndex], out RegValue))
                        {
                            if (IsPlaneScalerEnabled(RegValue))
                            {
                                                               
                                Console.Write(RegisterLabel[piIndex][plIndex] + String.Format(" 0x{0:X}", RegisterOffset[piIndex][plIndex]) + ": " + String.Format("0x{0:X}", RegValue) + "::");
                                sw.Write(RegisterLabel[piIndex][plIndex] + String.Format(" 0x{0:X}", RegisterOffset[piIndex][plIndex]) + ": " + String.Format("0x{0:X}", RegValue) + "::");
                                if (PlatformID >= Platforms.SKYLAKE)
                                {
                                    Console.Write("Scaler Mode >" + GetScalerMode(RegValue) + "; ");
                                    sw.Write("Scaler Mode > " + GetScalerMode(RegValue) + "; ");

                                    Console.Write("Scaler Bind >" + GetScalerBind(RegValue) + "; ");
                                    sw.Write("Scaler Bind > " + GetScalerBind(RegValue) + "; ");
                                }
                                

                                //if (PlatformID >= Platforms.SKYLAKE)
                                //{
                                    

                                //    Console.Write("Plane CSC >" + IsPlaneCSCEnabled(RegValue) + "; ");
                                //    sw.Write("Plane CSC > " + IsPlaneCSCEnabled(RegValue) + "; ");

                                //    Console.WriteLine("PIPE CSC >" + IsPipeCSCEnabled(RegValue));
                                //    sw.WriteLine("PIPE CSC > " + IsPipeCSCEnabled(RegValue));
                                //}
                                
                                Console.WriteLine();
                                sw.WriteLine();

                                planeScalerCount++;
                            }
                        }
                        //Console.Write(String.Format("0x{0:X}", Offset[piIndex][plIndex]) + ' ');
                    }
                    if (planeScalerCount != 0)
                    {
                        Console.WriteLine("------------------------------------------------------------");
                        sw.WriteLine("------------------------------------------------------------");
                    }
                }
                Console.WriteLine("************************************************************");
                sw.WriteLine("************************************************************");
                Thread.Sleep(interval * 1000 - 100);
                timeCount += interval;
                if (timeCount >= duration * 60)
                    break;
            }
            /*uint RegValue = 0;
            uint offset = 0x70180;
            if (RegisterInterface.Instance.ReadWriteRegister(RegisterInterface.RegisterOperation.READ, offset, out RegValue))
            {
                Console.WriteLine("Value: "+ String.Format("0x{0:X}", RegValue));
                Console.ReadKey();
            }*/
            sw.Close();
        }

        private static string GetScalerBind(uint RegValue)
        {
            const uint SCALERBINDMASK = 0x0E000000;
            const uint PIPESCALER = 0x00000000;
            const uint PL1SCALER = 0x02000000;
            const uint PL2SCALER = 0x04000000;
            const uint PL3SCALER = 0x06000000;
            const uint PL4SCALER = 0x08000000;
            const uint PL5SCALER = 0x0A000000;
            const uint PL6SCALER = 0x0C000000;
            const uint PL7SCALER = 0x0E000000;
            String ScalerBind = "";

            switch (RegValue & SCALERBINDMASK)
            {
                case PIPESCALER:
                    ScalerBind = "Pipe";
                    break;
                case PL1SCALER:
                    ScalerBind = "Plane 1";
                    break;
                case PL2SCALER:
                    ScalerBind = "Plane 2";
                    break;
                case PL3SCALER:
                    ScalerBind = "Plane 3";
                    break;
                case PL4SCALER:
                    ScalerBind = "Plane 4";
                    break;
                case PL5SCALER:
                    ScalerBind = "Plane 5";
                    break;
                case PL6SCALER:
                    ScalerBind = "Plane 6";
                    break;
                case PL7SCALER:
                    ScalerBind = "Plane 7";
                    break;
            }
            return ScalerBind;
        }

        private static string GetScalerMode(uint RegValue)
        {
            const uint SCALERMODEMASK = 0x30000000;
            const uint DYNMODE = 0x00000000;
            const uint _75MODE = 0x10000000;
            const uint NV12MODE = 0x20000000;

            String ScalerMode = "";

            switch (RegValue & SCALERMODEMASK)
            {
                case DYNMODE:
                    ScalerMode = "Dynamic";
                    break;
                case _75MODE:
                    ScalerMode = "7 x 5 Filter";
                    break;
                case NV12MODE:
                    ScalerMode = "NV12 Scaler";
                    break;
            }
            return ScalerMode;
        }

        

        private static void PrintHelp()
        {
            throw new NotImplementedException();
        }

        private static string IsPipeCSCEnabled(uint RegValue)
        {
            if ((RegValue & PIPECSCMASK) > 0)
                return "Enabled";
            return "Disabled";
        }

        private static bool IsPlaneScalerEnabled(uint RegValue)
        {
            switch (PlatformID)
            {
                case Platforms.CHERRYVIEW:
                    if ((RegValue & CHVENABLEMASK) > 0)
                        return true;
                    break;
                default:
                    if ((RegValue & GENENABLEMASK) > 0)
                        return true;
                    break;
            }
            return false;
        }

        private static string[][] GetRegisterLabelforPlatform(Platforms PlatformID)
        {
            String[][] offsetLabel = null;
            switch (PlatformID)
            {
                case MPOPlaneScaler.Platforms.SKYLAKE:
                case MPOPlaneScaler.Platforms.KABYLAKE:
                    offsetLabel = new string[3][] { new string[] { "Scaler A-1", "Scaler A-2" }, 
                                                    new string[] { "Scaler B-1", "Scaler B-2" }, 
                                                    new string[] { "Scaler C-1" } };
                    break;
                case MPOPlaneScaler.Platforms.BROXTON:
                    offsetLabel = new string[3][] { new string[] { "Scaler A-1", "Scaler A-2" }, 
                                                    new string[] { "Scaler B-1", "Scaler B-2" }, 
                                                    new string[] { "Scaler C-1", "Scaler C-2" } };
                    break;
                case MPOPlaneScaler.Platforms.GEMINILAKE:
                case MPOPlaneScaler.Platforms.CANNONLAKE:
                    offsetLabel = new string[3][] { new string[] { "Scaler A-1", "Scaler A-2" }, 
                                                    new string[] { "Scaler B-1", "Scaler B-2" }, 
                                                    new string[] { "Scaler C-1", "Scaler C-2" } };
                    break;
                case MPOPlaneScaler.Platforms.CHERRYVIEW:
                    offsetLabel = new string[1][] { new string[] { "Scaler B-1" }};
                    break;
                case MPOPlaneScaler.Platforms.ICELAKE:
                case MPOPlaneScaler.Platforms.ICELAKELP:
                    offsetLabel = new string[3][] { new string[] { "Scaler A-1", "Scaler A-2" },
                                                    new string[] { "Scaler B-1", "Scaler B-2" },
                                                    new string[] { "Scaler C-1", "Scaler C-2" } };
                    break;
                case MPOPlaneScaler.Platforms.ICELAKEHP:
                    offsetLabel = new string[4][] { new string[] { "Scaler A-1", "Scaler A-2" },
                                                    new string[] { "Scaler B-1", "Scaler B-2" },
                                                    new string[] { "Scaler C-1", "Scaler C-2" },
                                                    new string[] { "Scaler D-1", "Scaler D-2" }};
                    break;
            }
            return offsetLabel;
        }
        private static uint[][] GetRegisterOffSetforPlatform(MPOPlaneScaler.Platforms PlatformID)
        {
            uint[][] offset = null;
            switch (PlatformID)
            {   
                case MPOPlaneScaler.Platforms.SKYLAKE:
                case MPOPlaneScaler.Platforms.KABYLAKE:
                    offset = new uint[3][] { new uint[] { 0x68180, 0x68280 }, 
                                             new uint[] { 0x68980, 0x68A80 }, 
                                             new uint[] { 0x69180 } };
                    break;
                case MPOPlaneScaler.Platforms.BROXTON:
                    offset = new uint[3][] { new uint[] { 0x68180, 0x68280 }, 
                                             new uint[] { 0x68980, 0x68A80 }, 
                                             new uint[] { 0x69180, 0x69280 } };
                    break;
                case MPOPlaneScaler.Platforms.GEMINILAKE:
                case MPOPlaneScaler.Platforms.CANNONLAKE:
                    offset = new uint[3][] { new uint[] { 0x68180, 0x68280 }, 
                                             new uint[] { 0x68980, 0x68A80 }, 
                                             new uint[] { 0x69180, 0x69280 } };
                    break;
                case MPOPlaneScaler.Platforms.CHERRYVIEW:
                    offset = new uint[1][] { new uint[] { 0x1ED000 }};
                    break;
                case MPOPlaneScaler.Platforms.ICELAKE:
                case MPOPlaneScaler.Platforms.ICELAKELP:
                    offset = new uint[3][] { new uint[] { 0x68180, 0x68280 },
                                             new uint[] { 0x68980, 0x68A80 },
                                             new uint[] { 0x69180, 0x69280 } };
                    break;
                case MPOPlaneScaler.Platforms.ICELAKEHP:
                    offset = new uint[4][] { new uint[] { 0x68180, 0x68280 },
                                             new uint[] { 0x68980, 0x68A80 },
                                             new uint[] { 0x69180, 0x69280 },
                                             new uint[] { 0x69980, 0x69A80 }};
                    break;
            }
            return offset;
        }

        
    }
}
