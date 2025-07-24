using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;

namespace PlaneStatus
{
    class MPOPlaneStatus
    {
        public enum Platforms
        {
            UNINITIALIZED = 0,
            CHERRYVIEW,
            SKYLAKE,
            KABYLAKE,
            BROXTON,
            GEMINILAKE,
            CANNONLAKE,
            ICELAKE,
            ICELAKELP,
            ICELAKEHP
        }
        public static Platforms PlatformID = Platforms.UNINITIALIZED;
        public static bool IsDDRW = false;

        public enum SkyLakeColor : uint
        {
            COLORFORMATMASK = 0x0F000000,
            COLORYUV16 = 0x00000000,
            COLORNV12 = 0x01000000,
            COLORRGB32 = 0x02000000,
            COLORP010 = 0x03000000,
            COLORRGB328 = 0x04000000,
            COLORP012 = 0x05000000,
            COLORRGB64 = 0x06000000,
            COLORP016 = 0x07000000,
            COLORYUV32 = 0x08000000,
            COLORRGB32X = 0x0A000000,
            COLORINDX8 = 0x0C000000,
            COLORRGB16 = 0x0E000000
        };

        public enum LPColor : uint
        {
            COLORFORMATMASK = 0x3C000000,
            COLORYUV422 = 0x00000000,
            COLORINDX8 = 0x0C000000,
            COLOR16BGRX = 0x14000000,
            COLOR32BGRX8 = 0x18000000,
            COLOR32BGRA8 = 0x1C000000,
            COLOR32RGBX10 = 0x20000000,
            COLOR32RGBA10 = 0x24000000,
            COLOR32RGBX8 = 0x38000000,
            COLOR32RGBA8 = 0x3C000000
        };

        public enum IceLakeColor : uint
        {
            COLORFORMATMASK = 0x0F800000,
            COLORYUV16 = 0x00000000,
            COLORY210 = 0x0800000,
            COLORNV12 = 0x01000000,
            COLORY212 = 0x01800000,
            COLORRGB32 = 0x02000000,
            COLORY216 = 0x02800000,
            COLORP010 = 0x03000000,
            COLORY410 = 0x03800000,
            COLORRGB328 = 0x04000000,
            COLORY412 = 0x04800000,
            COLORP012 = 0x05000000,
            COLORY416 = 0x05800000,
            COLORRGB64 = 0x06000000,
            COLORP016 = 0x07000000,
            COLORYUV32 = 0x08000000,
            COLORRGB64UINT = 0x09000000,
            COLORRGB32X = 0x0A000000,
            COLORINDX8 = 0x0C000000,
            COLORRGB16 = 0x0E000000
        };
        const uint SURFACETILEMASK = 0x00001c00;
        const uint TILELINEAR = 0x00000000;
        const uint TILEXMEM = 0x00000400;
        const uint TILEYMEM = 0x00001000;
        const uint TILEYFMEM = 0x00001400;

        const uint ENABLEMASK = 0x80000000;
        const uint RCMASK = 0x00008000;
        const uint PIPECSCMASK = 0x00800000;
        const uint PLANECSCMASK = 0x00080000;

        static void Main(string[] args)
        {
            //MPOPlaneStatus mpoPlaneStatus = new MPOPlaneStatus();
            StreamWriter sw = File.CreateText("PlaneStatus_Log.txt");
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
                else if (UpperOption.StartsWith("-DDRW"))
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
            uint[][] SourceSize = GetSourceSizeOffset(PlatformID);
            while (true)
            {
                for (piIndex = 0; piIndex < RegisterOffset.GetLength(0); piIndex++)
                {
                    int planeCount = 0;
                    for (plIndex = 0; plIndex < RegisterOffset[piIndex].Length; plIndex++)
                    {
                        uint RegValue = 0;
                        if (RegisterInterface.Instance.ReadWriteRegister(RegisterInterface.RegisterOperation.READ, RegisterOffset[piIndex][plIndex], out RegValue))
                        {
                            if (IsPlaneEnabled(RegValue))
                            {
                                                               
                                Console.Write(RegisterLabel[piIndex][plIndex] + String.Format(" 0x{0:X}", RegisterOffset[piIndex][plIndex]) + ": " + String.Format("0x{0:X}", RegValue) + "::");
                                sw.Write(RegisterLabel[piIndex][plIndex] + String.Format(" 0x{0:X}", RegisterOffset[piIndex][plIndex]) + ": " + String.Format("0x{0:X}", RegValue) + "::");
                               
                                Console.Write("ColorFormat > " + GetColorFormat(RegValue) + "; ");
                                sw.Write("ColorFormat > " + GetColorFormat(RegValue) + "; ");

                                if (PlatformID >= Platforms.SKYLAKE)
                                {
                                    Console.Write("Plane CSC >" + IsPlaneCSCEnabled(RegValue) + "; ");
                                    sw.Write("Plane CSC > " + IsPlaneCSCEnabled(RegValue) + "; ");

                                    Console.WriteLine("PIPE CSC >" + IsPipeCSCEnabled(RegValue));
                                    sw.WriteLine("PIPE CSC > " + IsPipeCSCEnabled(RegValue));
                                }

                                Console.WriteLine();
                                sw.WriteLine();

                                planeCount++;
                            }
                        }
                        //Console.Write(String.Format("0x{0:X}", Offset[piIndex][plIndex]) + ' ');
                    }
                    if (planeCount > 1)
                    {
                        Console.WriteLine("MultiPlane Overlay is enabled on PIPE " + ((char)(piIndex + 65)));
                        sw.WriteLine("MultiPlane Overlay is enabled on PIPE " + ((char)(piIndex + 65)));
                    }
                    else if (planeCount == 1)
                    {
                        Console.WriteLine("MultiPlane Overlay is disabled on PIPE " + ((char)(piIndex + 65)));
                        sw.WriteLine("MultiPlane Overlay is disabled on PIPE " + ((char)(piIndex + 65)));
                    }
                    if (planeCount != 0)
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

        private static string GetSourceSizeX(uint RegValue1)
        {
            uint reg = 0;

            reg = RegValue1 & 0xFFFF;

            return reg.ToString();
        }

        private static object GetSourceSizeY(uint RegValue1)
        {
            uint reg = 0;

            reg = (RegValue1 >> 16) & 0xFFFF;

            return reg.ToString();
        }

        private static uint[][] GetSourceSizeOffset(Platforms PlatformID)
        {
            uint[][] offset = null;
            switch (PlatformID)
            {
                case MPOPlaneStatus.Platforms.SKYLAKE:
                case MPOPlaneStatus.Platforms.KABYLAKE:
                    offset = new uint[3][] { new uint[] { 0x70190, 0x70290, 0x70390 }, 
                                             new uint[] { 0x71190, 0x71290, 0x71390 }, 
                                             new uint[] { 0x72190, 0x72290, 0x72390 } };
                    break;
                case MPOPlaneStatus.Platforms.GEMINILAKE:
                case MPOPlaneStatus.Platforms.CANNONLAKE:
                    offset = new uint[3][] { new uint[] { 0x70190, 0x70290, 0x70390 },
                                             new uint[] { 0x71190, 0x71290, 0x71390 },
                                             new uint[] { 0x72190, 0x72290, 0x72390 } };
                    break;
                case MPOPlaneStatus.Platforms.ICELAKE:
                case MPOPlaneStatus.Platforms.ICELAKELP:
                    offset = new uint[3][] { new uint[] { 0x70190, 0x70290, 0x70390, 0x70490, 0x70590, 0x70690, 0x70790},
                                             new uint[] { 0x71190, 0x71290, 0x71390, 0x71490, 0x71590, 0x71690, 0x71790},
                                             new uint[] { 0x72190, 0x72290, 0x72390, 0x72490, 0x72590, 0x72690, 0x72790} };
                    break;
                case MPOPlaneStatus.Platforms.ICELAKEHP:
                    offset = new uint[4][] { new uint[] { 0x70190, 0x70290, 0x70390, 0x70490, 0x70590, 0x70690, 0x70790},
                                             new uint[] { 0x71190, 0x71290, 0x71390, 0x71490, 0x71590, 0x71690, 0x71790},
                                             new uint[] { 0x72190, 0x72290, 0x72390, 0x72490, 0x72590, 0x72690, 0x72790},
                                             new uint[] { 0x73190, 0x73290, 0x73390, 0x73490, 0x73590, 0x73690, 0x73790} };
                    break;
            }
            return offset;
        }

        

        private static void PrintHelp()
        {
            throw new NotImplementedException();
        }

        private static string GetHwRotation(uint RegValue)
        {
            const uint HWROTATIONMASK = 0x00000003;

            const uint DEG_0_ROTATION = 0x00000000;
            const uint DEG_90_ROTATION = 0x00000001;
            const uint DEG_180_ROTATION = 0x00000002;
            const uint DEG_270_ROTATION = 0x00000003;

            String HwRotation = "Disabled";
            switch(RegValue & HWROTATIONMASK)
            {
                case DEG_0_ROTATION:
                    HwRotation = "Disabled";
                    break;
                case DEG_90_ROTATION:
                    HwRotation = "HW 90 Deg Rotation";
                    break;
                case DEG_180_ROTATION:
                    HwRotation = "HW 180 Deg Rotation";
                    break;
                case DEG_270_ROTATION:
                    HwRotation = "HW 270 Deg Rotation";
                    break;
                    
            }
            return HwRotation;
        }

        private static string IsPlaneCSCEnabled(uint RegValue)
        {
            if ((RegValue & PLANECSCMASK) == 0)
                return "Enabled";
            return "Disabled";
        }

        private static string IsPipeCSCEnabled(uint RegValue)
        {
            if ((RegValue & PIPECSCMASK) > 0)
                return "Enabled";
            return "Disabled";
        }

        private static string IsRCEnabled(uint RegValue)
        {
            if ((RegValue & RCMASK) > 0)
                return "Enabled";
            return "Disabled";
        }

        private static string GetTileFormat(uint RegValue)
        {
            String TileFormat = "";
            switch (RegValue & SURFACETILEMASK) 
            {
                case TILELINEAR:
                    TileFormat = "LINEAR";
                    break;
                case TILEXMEM:
                    TileFormat = "X-Tiling";
                    break;
                case TILEYMEM:
                    TileFormat = "Y-Tiling";
                    break;
                case TILEYFMEM:
                    TileFormat = "YF-Tiling";
                    break;
            }
            return TileFormat;
        }

        private static string GetColorFormat(uint RegValue)
        {
            String ColorFormat = "";
            #region SKYLAKE
            if (PlatformID == Platforms.SKYLAKE || PlatformID == Platforms.KABYLAKE || PlatformID == Platforms.BROXTON ||PlatformID == Platforms.GEMINILAKE)
            {
                switch (RegValue & (uint)SkyLakeColor.COLORFORMATMASK)
                {
                    case (uint)SkyLakeColor.COLORYUV16:
                        ColorFormat = "YUV 16-bit";
                        break;
                    case (uint)SkyLakeColor.COLORNV12:
                        ColorFormat = "NV12 YUV 4:2:0 8-bit";
                        break;
                    case (uint)SkyLakeColor.COLORRGB32:
                        ColorFormat = "RGB 32-bit 2:10:10:10";
                        break;
                    case (uint)SkyLakeColor.COLORRGB328:
                        ColorFormat = "RGB 32-bit 8:8:8:8";
                        break;
                    case (uint)SkyLakeColor.COLORRGB64:
                        ColorFormat = "RGB 64-bit";
                        break;
                    case (uint)SkyLakeColor.COLORYUV32:
                        ColorFormat = "YUV 32-bit";
                        break;
                    case (uint)SkyLakeColor.COLORRGB32X:
                        ColorFormat = "RGB 32-bit Ext";
                        break;
                    case (uint)SkyLakeColor.COLORINDX8:
                        ColorFormat = "Indexed 8-bit";
                        break;
                    case (uint)SkyLakeColor.COLORRGB16:
                        ColorFormat = "RGB 16-bit";
                        break;
                    case (uint)SkyLakeColor.COLORP010:
                        ColorFormat = "P010 YUV 4:2:0 10 bit";
                        break;
                    case (uint)SkyLakeColor.COLORP012:
                        ColorFormat = "P012 YUV 4:2:0 12 bit";
                        break;
                    case (uint)SkyLakeColor.COLORP016:
                        ColorFormat = "P016 YUV 4:2:0 16 bit";
                        break;
                }
            }
            #endregion

            #region CHERRYVIEW
            if (PlatformID == Platforms.CHERRYVIEW)
            {
                switch (RegValue & (uint)LPColor.COLORFORMATMASK)
                {
                    case (uint)LPColor.COLORYUV422:
                        ColorFormat = "YUY2";
                        break;
                    case (uint)LPColor.COLOR32BGRX8:
                        ColorFormat = "32-BGRX 8:8:8:8";
                        break;
                    case (uint)LPColor.COLOR16BGRX:
                        ColorFormat = "16-BGRX 5:6:5:0";
                        break;
                    case (uint)LPColor.COLOR32BGRA8:
                        ColorFormat = "32-BGRA 8:8:8:8";
                        break;
                    case (uint)LPColor.COLOR32RGBA10:
                        ColorFormat = "32-BGRA 10:10:10:2";
                        break;
                    case (uint)LPColor.COLOR32RGBA8:
                        ColorFormat = "32-RGBA 8:8:8:8";
                        break;
                    case (uint)LPColor.COLOR32RGBX10:
                        ColorFormat = "32-BGRX 10:10:10:2";
                        break;
                    case (uint)LPColor.COLORINDX8:
                        ColorFormat = "Indexed 8-bit";
                        break;
                }
            }
            #endregion

            #region ICELAKE
            if (PlatformID == MPOOptions.Platforms.ICELAKE || PlatformID == MPOOptions.Platforms.ICELAKELP || PlatformID == MPOOptions.Platforms.ICELAKEHP)
            {
                switch (RegValue & (uint)IceLakeColor.COLORFORMATMASK)
                {
                    case (uint)IceLakeColor.COLORYUV16:
                        ColorFormat = "YUV 16-bit";
                        break;
                    case (uint)IceLakeColor.COLORY210:
                        ColorFormat = "YUV 16-bit Y210";
                        break;
                    case (uint)IceLakeColor.COLORNV12:
                        ColorFormat = "NV12 YUV 4:2:0 8-bit";
                        break;
                    case (uint)IceLakeColor.COLORY212:
                        ColorFormat = "YUV 16-bit Y212";
                        break;
                    case (uint)IceLakeColor.COLORRGB32:
                        ColorFormat = "RGB 32-bit 2:10:10:10";
                        break;
                    case (uint)IceLakeColor.COLORY216:
                        ColorFormat = "YUV 16-bit Y216";
                        break;
                    case (uint)IceLakeColor.COLORP010:
                        ColorFormat = "P010 YUV 4:2:0 10 bit";
                        break;
                    case (uint)IceLakeColor.COLORY410:
                        ColorFormat = "YUV 32-bit Y410";
                        break;
                    case (uint)IceLakeColor.COLORRGB328:
                        ColorFormat = "RGB 32-bit 8:8:8:8";
                        break;
                    case (uint)IceLakeColor.COLORY412:
                        ColorFormat = "YUV 32-bit Y412";
                        break;
                    case (uint)IceLakeColor.COLORP012:
                        ColorFormat = "P012 YUV 4:2:0 12 bit";
                        break;
                    case (uint)IceLakeColor.COLORY416:
                        ColorFormat = "YUV 32-bit Y416";
                        break;
                    case (uint)IceLakeColor.COLORRGB64:
                        ColorFormat = "RGB 64-bit";
                        break;
                    case (uint)IceLakeColor.COLORP016:
                        ColorFormat = "P016 YUV 4:2:0 16 bit";
                        break;
                    case (uint)IceLakeColor.COLORYUV32:
                        ColorFormat = "YUV 32-bit";
                        break;
                    case (uint)IceLakeColor.COLORRGB64UINT:
                        ColorFormat = "RGB 64-bit UINT";
                        break;
                    case (uint)IceLakeColor.COLORRGB32X:
                        ColorFormat = "RGB 32-bit Ext";
                        break;
                    case (uint)IceLakeColor.COLORINDX8:
                        ColorFormat = "Indexed 8-bit";
                        break;
                    case (uint)IceLakeColor.COLORRGB16:
                        ColorFormat = "RGB 16-bit";
                        break;
                }
            }
            #endregion

            return ColorFormat;
        }

        private static bool IsPlaneEnabled(uint RegValue)
        {
            if ((RegValue & ENABLEMASK) > 0)
                return true;
            return false;
        }
        private static string[][] GetRegisterLabelforPlatform(Platforms PlatformID)
        {
            String[][] offsetLabel = null;
            switch (PlatformID)
            {
                case MPOPlaneStatus.Platforms.SKYLAKE:
                case MPOPlaneStatus.Platforms.KABYLAKE:
                    offsetLabel = new string[3][] { new string[] { "Plane A-1", "Plane A-2", "Plane A-3" }, 
                                                    new string[] { "Plane B-1", "Plane B-2", "Plane B-3" }, 
                                                    new string[] { "Plane C-1", "Plane C-2", "Plane C-3" } };
                    break;
                case MPOPlaneStatus.Platforms.BROXTON:
                    offsetLabel = new string[3][] { new string[] { "Plane A-1", "Plane A-2", "Plane A-3", "Plane A-4" }, 
                                                    new string[] { "Plane B-1", "Plane B-2", "Plane B-3", "Plane B-4" }, 
                                                    new string[] { "Plane C-1", "Plane C-2", "Plane C-3" } };
                    break;
                case MPOPlaneStatus.Platforms.GEMINILAKE:
                    offsetLabel = new string[3][] { new string[] { "Plane A-1", "Plane A-2", "Plane A-3", "Plane A-4" }, 
                                                    new string[] { "Plane B-1", "Plane B-2", "Plane B-3", "Plane B-4" }, 
                                                    new string[] { "Plane C-1", "Plane C-2", "Plane C-3", "Plane C-4" } };
                    break;
                case MPOPlaneStatus.Platforms.ICELAKE:
                case MPOPlaneStatus.Platforms.ICELAKELP:
                    offsetLabel = new string[3][] { new string[] { "Plane A-1", "Plane A-2", "Plane A-3", "Plane A-4", "Plane A-5" },
                                                    new string[] { "Plane B-1", "Plane B-2", "Plane B-3", "Plane B-4", "Plane B-5" },
                                                    new string[] { "Plane C-1", "Plane C-2", "Plane C-3", "Plane C-4", "Plane C-5" }};
                    break;
                case MPOPlaneStatus.Platforms.ICELAKEHP:
                    offsetLabel = new string[4][] { new string[] { "Plane A-1", "Plane A-2", "Plane A-3", "Plane A-4", "Plane A-5" },
                                                    new string[] { "Plane B-1", "Plane B-2", "Plane B-3", "Plane B-4", "Plane B-5" },
                                                    new string[] { "Plane C-1", "Plane C-2", "Plane C-3", "Plane C-4", "Plane C-5" },
                                                    new string[] { "Plane D-1", "Plane D-2", "Plane D-3", "Plane D-4", "Plane D-5" }};
                    break;
                case MPOPlaneStatus.Platforms.CHERRYVIEW:
                    offsetLabel = new string[3][] { new string[] { "Plane A-1", "Sprite A-1", "Sprite A-2" }, 
                                                    new string[] { "Plane B-1", "Sprite B-1", "Sprite A-2" },
                                                    new string[] { "Plane C-1", "Sprite C-1", "Sprite A-2" }};
                    break;
            }
            return offsetLabel;
        }
        private static uint[][] GetRegisterOffSetforPlatform(MPOPlaneStatus.Platforms PlatformID)
        {
            uint[][] offset = null;
            switch (PlatformID)
            {   
                case MPOPlaneStatus.Platforms.SKYLAKE:
                case MPOPlaneStatus.Platforms.KABYLAKE:
                    offset = new uint[3][] { new uint[] { 0x70180, 0x70280, 0x70380 }, 
                                             new uint[] { 0x71180, 0x71280, 0x71380 }, 
                                             new uint[] { 0x72180, 0x72280, 0x72380 } };
                    break;
                case MPOPlaneStatus.Platforms.BROXTON:
                    offset = new uint[3][] { new uint[] { 0x70180, 0x70280, 0x70380, 0x70480 }, 
                                             new uint[] { 0x71180, 0x71280, 0x71380, 0x71480 }, 
                                             new uint[] { 0x72180, 0x72280, 0x72380 } };
                    break;
                case MPOPlaneStatus.Platforms.GEMINILAKE:
                case MPOPlaneStatus.Platforms.CANNONLAKE:
                    offset = new uint[3][] { new uint[] { 0x70180, 0x70280, 0x70380, 0x70480 }, 
                                             new uint[] { 0x71180, 0x71280, 0x71380, 0x71480 }, 
                                             new uint[] { 0x72180, 0x72280, 0x72380, 0x72480 } };
                    break;
                
                case MPOPlaneStatus.Platforms.CHERRYVIEW:
                    offset = new uint[3][] { new uint[] { 0x1F0180, 0x1F2180, 0x1F2280 }, 
                                             new uint[] { 0x1F1180, 0x1F2380, 0x1F2480 },
                                             new uint[] { 0x1F2180, 0x1F2580, 0x1F2680 }};
                    break;
                case MPOPlaneStatus.Platforms.ICELAKE:
                case MPOPlaneStatus.Platforms.ICELAKELP:
                    offset = new uint[3][] { new uint[] { 0x70180, 0x70280, 0x70380, 0x70480, 0x70580 },
                                             new uint[] { 0x71180, 0x71280, 0x71380, 0x71480, 0x71580 },
                                             new uint[] { 0x72180, 0x72280, 0x72380, 0x72480, 0x72580 } };
                    break;
                case MPOPlaneStatus.Platforms.ICELAKEHP:
                    offset = new uint[4][] { new uint[] { 0x70180, 0x70280, 0x70380, 0x70480, 0x70580 },
                                             new uint[] { 0x71180, 0x71280, 0x71380, 0x71480, 0x71580 },
                                             new uint[] { 0x72180, 0x72280, 0x72380, 0x72480, 0x72580 },
                                             new uint[] { 0x73180, 0x73280, 0x73380, 0x73480, 0x73580 } };
                    break;
            }
            return offset;
        }

        
    }
}
