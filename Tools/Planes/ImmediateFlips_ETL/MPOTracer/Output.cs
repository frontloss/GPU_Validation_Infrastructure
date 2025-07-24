using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using ImmediateFlips;

namespace PlaneStatus
{
    public class RegisterOutput
    {
        const uint SURFACETILEMASK = 0x00001c00;
        const uint ENABLEMASK = 0x80000000;
        const uint RCMASK = 0x00008000;
        const uint PIPECSCMASK = 0x00800000;
        const uint PLANECSCMASK = 0x00080000;
        const uint HWROTATIONMASK = 0x00000003;

        const uint DEG_0_ROTATION = 0x00000000;
        const uint DEG_90_ROTATION = 0x00000001;
        const uint DEG_180_ROTATION = 0x00000002;
        const uint DEG_270_ROTATION = 0x00000003;

        const uint TILELINEAR = 0x00000000;
        const uint TILEXMEM = 0x00000400;
        const uint TILEYMEM = 0x00001000;
        const uint TILEYFMEM = 0x00001400;
        
        public enum SkyLakeColor : uint
        {
            COLORFORMATMASK = 0x0F000000,
            COLORYUV16 = 0x00000000,
            COLORNV12 = 0x01000000,
            COLORRGB32 = 0x02000000,
            COLORRGB328 = 0x04000000,
            COLORRGB64 = 0x06000000,
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
        }

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
        public void RegOutput(ImmediateFlips.AsyncFlipOptions Options, StreamWriter outFile)
        {
            int piIndex = 0, plIndex = 0;
            uint[][] RegisterOffset = GetOffSetforPlatform(Options.Platform);
            String[][] RegisterLabel = GetOffSetNameforPlatform(Options.Platform);

            for (piIndex = 0; piIndex < RegisterOffset.GetLength(0); piIndex++)
            {
                int planeCount = 0;
                for (plIndex = 0; plIndex < RegisterOffset[piIndex].Length; plIndex++)
                {
                    uint RegValue = 0;
                    if (RegisterInterface.Instance.ReadWriteRegister(RegisterInterface.RegisterOperation.READ, RegisterOffset[piIndex][plIndex], out RegValue, Options.IsDDRW))
                    {
                        if (IsPlaneEnabled(RegValue))
                        {
                            Console.ForegroundColor = ConsoleColor.Green;
                            Console.Write(RegisterLabel[piIndex][plIndex] + /*String.Format(" 0x{0:X}", RegisterOffset[piIndex][plIndex]) +*/ ": " + String.Format("0x{0:X}", RegValue) + "::");
                            outFile.Write(RegisterLabel[piIndex][plIndex] + /*String.Format(" 0x{0:X}", RegisterOffset[piIndex][plIndex]) +*/ ": " + String.Format("0x{0:X}", RegValue) + "::");

                            Console.Write("PixelFormat > " + GetColorFormat(Options.Platform, RegValue) + "; ");
                            outFile.Write("PixelFormat > " + GetColorFormat(Options.Platform, RegValue) + "; ");

                            if (Options.Platform >= AsyncFlipOptions.Platforms.SKYLAKE)
                            {
                                Console.Write("HW Rotation > " + GetHwRotation(RegValue) + "; ");
                                outFile.Write("HW Rotation > " + GetHwRotation(RegValue) + "; ");

                                Console.Write("Tiling > " + GetTileFormat(RegValue) + ";");
                                outFile.Write("Tiling > " + GetTileFormat(RegValue) + ";");
                            }

                            //Console.Write("Plane CSC >" + IsPlaneCSCEnabled(RegValue) + "; ");
                            //outFile.Write("Plane CSC > " + IsPlaneCSCEnabled(RegValue) + "; ");
                            //Console.WriteLine("PIPE CSC >" + IsPipeCSCEnabled(RegValue));
                            //sw.WriteLine("PIPE CSC > " + IsPipeCSCEnabled(RegValue));

                            //Console.WriteLine("RC > " + IsRCEnabled(RegValue));
                            //outFile.WriteLine("RC > " + IsRCEnabled(RegValue));

                            Console.WriteLine();
                            outFile.WriteLine();
                            
                            planeCount++;
                        }
                    }
                    //Console.Write(String.Format("0x{0:X}", Offset[piIndex][plIndex]) + ' ');
                }
                
                if(planeCount != 0)
                { 
                    Console.WriteLine("MultiPlane Overlay is enabled on PIPE " + ((char)(piIndex + 65)));
                    outFile.WriteLine("MultiPlane Overlay is enabled on PIPE " + ((char)(piIndex + 65)));
                }
                //else if (planeCount == 1)
                //{
                //    Console.WriteLine("MultiPlane Overlay is disabled on PIPE " + ((char)(piIndex + 65)));
                //    sw.WriteLine("MultiPlane Overlay is disabled on PIPE " + ((char)(piIndex + 65)));
                //}
                if (planeCount != 0)
                {
                    Console.WriteLine("------------------------------------------------------------");
                    outFile.WriteLine("------------------------------------------------------------");
                }
            }
            Console.WriteLine("************************************************************");
            outFile.WriteLine("************************************************************");
            Console.ForegroundColor = ConsoleColor.White;
        }



        private static string GetHwRotation(uint RegValue)
        {
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

        private static string GetColorFormat(AsyncFlipOptions.Platforms PlatformID, uint RegValue)
        {
            String ColorFormat = "";
            #region SKYLAKE
            if (PlatformID == AsyncFlipOptions.Platforms.SKYLAKE || PlatformID == AsyncFlipOptions.Platforms.KABYLAKE || PlatformID == AsyncFlipOptions.Platforms.BROXTON || PlatformID == AsyncFlipOptions.Platforms.GEMINILAKE || PlatformID == AsyncFlipOptions.Platforms.CANNONLAKE || PlatformID == AsyncFlipOptions.Platforms.COFFEELAKE || PlatformID == AsyncFlipOptions.Platforms.WHISKEYLAKE || PlatformID == AsyncFlipOptions.Platforms.AMBERLAKE || PlatformID == AsyncFlipOptions.Platforms.COMETLAKE)
            {
                switch (RegValue & (uint)SkyLakeColor.COLORFORMATMASK)
                {
                    case (uint)SkyLakeColor.COLORYUV16:
                        ColorFormat = "YUV 16-bit";
                        break;
                    case (uint)SkyLakeColor.COLORNV12:
                        ColorFormat = "NV12 YUV";
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
                }
            }
            #endregion

            #region CHERRYVIEW
            if (PlatformID == AsyncFlipOptions.Platforms.CHERRYVIEW)
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
            if (PlatformID == AsyncFlipOptions.Platforms.ICELAKE || PlatformID == AsyncFlipOptions.Platforms.ICELAKELP || PlatformID == AsyncFlipOptions.Platforms.ICELAKEHP)
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

        private static uint[][] GetOffSetforPlatform(AsyncFlipOptions.Platforms platform)
        {
            uint[][] offset = null;
            switch (platform)
            {   
                case AsyncFlipOptions.Platforms.SKYLAKE:
                case AsyncFlipOptions.Platforms.KABYLAKE:
                case AsyncFlipOptions.Platforms.COFFEELAKE:
                case AsyncFlipOptions.Platforms.WHISKEYLAKE:
                case AsyncFlipOptions.Platforms.AMBERLAKE:
                case AsyncFlipOptions.Platforms.COMETLAKE:
                    offset = new uint[3][] { new uint[] { 0x70180, 0x70280, 0x70380 }, 
                                             new uint[] { 0x71180, 0x71280, 0x71380 }, 
                                             new uint[] { 0x72180, 0x72280, 0x72380 } };
                    break;
                case AsyncFlipOptions.Platforms.BROXTON:
                    offset = new uint[3][] { new uint[] { 0x70180, 0x70280, 0x70380, 0x70480 }, 
                                             new uint[] { 0x71180, 0x71280, 0x71380, 0x71480 }, 
                                             new uint[] { 0x72180, 0x72280, 0x72380 } };
                    break;
                case AsyncFlipOptions.Platforms.GEMINILAKE:
                case AsyncFlipOptions.Platforms.CANNONLAKE:
                    offset = new uint[3][] { new uint[] { 0x70180, 0x70280, 0x70380, 0x70480 },
                                             new uint[] { 0x71180, 0x71280, 0x71380, 0x71480 },
                                             new uint[] { 0x72180, 0x72280, 0x72380, 0x72480 } };
                    break;
                case AsyncFlipOptions.Platforms.CHERRYVIEW:
                     offset = new uint[3][] { new uint[] { 0x1F0180, 0x1F2180, 0x1F2280 }, 
                                             new uint[] { 0x1F1180, 0x1F2380, 0x1F2480 },
                                             new uint[] { 0x1F4180, 0x1F2580, 0x1F2680 }};
                    break;
                case AsyncFlipOptions.Platforms.ICELAKE:
                case AsyncFlipOptions.Platforms.ICELAKELP:
                    offset = new uint[3][] { new uint[] { 0x70180, 0x70280, 0x70380, 0x70480, 0x70580 },
                                             new uint[] { 0x71180, 0x71280, 0x71380, 0x71480, 0x71580 },
                                             new uint[] { 0x72180, 0x72280, 0x72380, 0x72480, 0x72580 } };
                    break;
                case AsyncFlipOptions.Platforms.ICELAKEHP:
                    offset = new uint[4][] { new uint[] { 0x70180, 0x70280, 0x70380, 0x70480, 0x70580 },
                                             new uint[] { 0x71180, 0x71280, 0x71380, 0x71480, 0x71580 },
                                             new uint[] { 0x72180, 0x72280, 0x72380, 0x72480, 0x72580 },
                                             new uint[] { 0x73180, 0x73280, 0x73380, 0x73480, 0x73580 } };
                    break;
            }
            return offset;
        }
        private static String[][] GetOffSetNameforPlatform(AsyncFlipOptions.Platforms platform)
        {
            String[][] offsetLabel = null;
            switch (platform)
            {
                case AsyncFlipOptions.Platforms.SKYLAKE:
                case AsyncFlipOptions.Platforms.KABYLAKE:
                case AsyncFlipOptions.Platforms.COFFEELAKE:
                case AsyncFlipOptions.Platforms.WHISKEYLAKE:
                case AsyncFlipOptions.Platforms.AMBERLAKE:
                case AsyncFlipOptions.Platforms.COMETLAKE:
                    offsetLabel = new string[3][] { new string[] { "Plane A-1", "Plane A-2", "Plane A-3" }, 
                                                    new string[] { "Plane B-1", "Plane B-2", "Plane B-3" }, 
                                                    new string[] { "Plane C-1", "Plane C-2", "Plane C-3" } };
                    break;
                case AsyncFlipOptions.Platforms.BROXTON:
                    offsetLabel = new string[3][] { new string[] { "Plane A-1", "Plane A-2", "Plane A-3", "Plane A-4" }, 
                                                    new string[] { "Plane B-1", "Plane B-2", "Plane B-3", "Plane B-4" }, 
                                                    new string[] { "Plane C-1", "Plane C-2", "Plane C-3" } };
                    break;
                case AsyncFlipOptions.Platforms.CHERRYVIEW:
                    offsetLabel = new string[3][] { new string[] { "Display Plane A-1", "Sprite A-1", "Sprite A-2" }, 
                                                    new string[] { "Display Plane B-1", "Sprite B-1", "Sprite A-2" },
                                                    new string[] { "Display Plane C-1", "Sprite C-1", "Sprite A-2" }};
                    break;
                case AsyncFlipOptions.Platforms.GEMINILAKE:
                case AsyncFlipOptions.Platforms.CANNONLAKE:
                    offsetLabel = new string[3][] { new string[] { "Plane A-1", "Plane A-2", "Plane A-3", "Plane A-4" },
                                                    new string[] { "Plane B-1", "Plane B-2", "Plane B-3", "Plane B-4" },
                                                    new string[] { "Plane C-1", "Plane C-2", "Plane C-3", "Plane C-4" } };
                    break;
                case AsyncFlipOptions.Platforms.ICELAKE:
                case AsyncFlipOptions.Platforms.ICELAKELP:
                    offsetLabel = new string[3][] { new string[] { "Plane A-1", "Plane A-2", "Plane A-3", "Plane A-4", "Plane A-5" },
                                                    new string[] { "Plane B-1", "Plane B-2", "Plane B-3", "Plane B-4", "Plane B-5" },
                                                    new string[] { "Plane C-1", "Plane C-2", "Plane C-3", "Plane C-4", "Plane C-5" }};
                    break;
                case AsyncFlipOptions.Platforms.ICELAKEHP:
                    offsetLabel = new string[4][] { new string[] { "Plane A-1", "Plane A-2", "Plane A-3", "Plane A-4", "Plane A-5" },
                                                    new string[] { "Plane B-1", "Plane B-2", "Plane B-3", "Plane B-4", "Plane B-5" },
                                                    new string[] { "Plane C-1", "Plane C-2", "Plane C-3", "Plane C-4", "Plane C-5" },
                                                    new string[] { "Plane D-1", "Plane D-2", "Plane D-3", "Plane D-4", "Plane D-5" }};
                    break;
            }
            return offsetLabel;
        }
        
    }
}
