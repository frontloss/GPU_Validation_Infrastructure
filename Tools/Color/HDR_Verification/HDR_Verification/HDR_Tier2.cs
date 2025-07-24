using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

using Microsoft.Diagnostics.Tracing.Session;
using Microsoft.Diagnostics.Tracing;
using Microsoft.Diagnostics.Tracing.Parsers;
using Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriver;

//Extra added DLL
using IgfxExtBridge_DotNet;
using Intel.Display.Automation.Common;
using Intel.Display.Automation.TestsCommon;


namespace HDRVerification
{
    enum HDR_TYPE
    {
        LSPCON_HDR = 1,
        DP_HDR = 2,
        HDMI_HDR = 3
    };

    struct Metadata_struct
    {
        public uint uEOTF;
        public uint HDRType;
        public uint uDisplayPrimariesX0;
        public uint uDisplayPrimariesX1;
        public uint uDisplayPrimariesX2;
        public uint uDisplayPrimariesY0;
        public uint uDisplayPrimariesY1;
        public uint uDisplayPrimariesY2;
        public uint uWhitePtX;
        public uint uWhitePtY;
        public uint uMaxDispLum;
        public uint uMinDispLum;
        public uint uMaxCLL;
        public uint uMaxFALL;

    };

    class Program
    {

        public static RegisterModule reg = new RegisterModule();
        public static uint[] uTrans_Conf = { 0, 0, 0, 0 }; // trans A,trans B,trans C,trans EDP
        public static uint[] uVideo_Dip_Ctrl = { 0, 0, 0, 0 }; // video_dip_A , video_dip_B , video_dip_B , Video_dip_EDP
        public static uint[] uTrans_Ddi_Ctrl = { 0, 0, 0, 0 }; // A,B,C,EDP
        public static uint[] uPlane_Ctrl = { 0, 0, 0 }; // Plane 1,2,3
        public static uint[] uCur_Ctrl = { 0, 0, 0 };
        public static uint[,] uVIdeo_Dip_HDR_data = new uint[4, 9];  // metadata
        public static uint[] uBPC = { 0, 0, 0, 0 };
        public static string[] uCSC = { "Disabled", "Disabled", "Disabled" };
        public static uint[,] uCSCCoeff = { { 0, 0, 0 }, { 0, 0, 0 }, { 0, 0, 0 } };
        public static uint[] uCSCPostOffset = { 0, 0, 0 };
        public static string[] uGamma = { "Disabled", "Disabled", "Disabled" };
        public static uint[,] uVSC_Data = {  { 0x60320, 0x60324, 0x60328, 0x6032C, 0x60330, 0x60334, 0x60338, 0x6033C, 0x60340 },
                                             { 0x61320, 0x61324, 0x61328, 0x6132C, 0x61330, 0x61334, 0x61338, 0x6133C, 0x61340 },
                                             { 0x62320, 0x62324, 0x62328, 0x6232C, 0x62330, 0x62334, 0x62338, 0x6233C, 0x62340 },
                                             { 0x6F320, 0x6F324, 0x6F328, 0x6F32C, 0x6F330, 0x6F334, 0x6F338, 0x6F33C, 0x6F340 }};
        public static uint[,] uGMP_Data = {  { 0x602E0, 0x602E4, 0x602E8, 0x602EC, 0x602F0, 0x602F4, 0x602F8, 0x602FC },
                                             { 0x612E0, 0x612E4, 0x612E8, 0x612EC, 0x612F0, 0x612F4, 0x612F8, 0x612FC },
                                             { 0x622E0, 0x622E4, 0x622E8, 0x622EC, 0x622F0, 0x622F4, 0x622F8, 0x622FC },
                                             { 0x632E0, 0x632E4, 0x632E8, 0x632EC, 0x632F0, 0x632F4, 0x632F8, 0x632FC }};

        public static uint[,] uDRM_Data = { { 0x60440,0x60444,0x60448,0x6044C,0x60450,0x60454,0x60458,0x6045C},
                                            { 0x61440,0x61444,0x61448,0x6144C,0x61450,0x61454,0x61458,0x6145C},
                                            { 0x62440,0x62444,0x62448,0x6244C,0x62450,0x62454,0x62458,0x6245C},
                                          };

        static double[,] uBT2020RGBtoYUVCoeff ={ {0.2627,0.6780,0.0593},
                                                  {-0.13963,-0.36036,0.5},
                                                  {0.5 ,-0.45978,-0.04021}
                                                };
        public static int hdrType = 0;

        public static Metadata_struct default_metadata = new Metadata_struct();
        public static Metadata_struct curr_metadata = new Metadata_struct();


        public static uint[] uVideo_Dip_VSC_Colorimetry_Data = new uint[4];

        static void Main(string[] args)
        {
            // Args parsing

            if (args.Length < 1)
            {
                Console.WriteLine(" Commandline params missing!! \n Parameter 1 : LSPCON_HDR/DP_HDR/HDMI_HDR \n Parameter 2 : Delay in seconds (optional)");
                return;
            }
            if (args.Length == 1 || args.Length == 2)
            {
                if (string.Equals(args[0], "LSPCON_HDR", StringComparison.OrdinalIgnoreCase))
                    hdrType = (int)HDR_TYPE.LSPCON_HDR;
                else if (string.Equals(args[0], "DP_HDR", StringComparison.OrdinalIgnoreCase))
                    hdrType = (int)HDR_TYPE.DP_HDR;
                else if (string.Equals(args[0], "HDMI_HDR", StringComparison.OrdinalIgnoreCase))
                    hdrType = (int)HDR_TYPE.HDMI_HDR;
                else
                {
                    Console.WriteLine("Wrong input parameter"); return;
                }

            }
            if (args.Length == 2)
            {

                Console.WriteLine(" Delay of " + args[1] + " second is added to the script");

                CmnDelay.Seconds(Int32.Parse(args[1]));
            }

            //Basic register reads

            InitializeRegister();
            StreamWriter outFile = File.CreateText("HDRTraceLog.txt");

            //Check for Admin mode
            if (!(TraceEventSession.IsElevated() ?? false))
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("Run the Analyzer in Admin mode");
                return;
            }

            // Trace session

            var sessionName = "HDREvents";
            using (var session = new TraceEventSession(sessionName))
            {


                LogETLEvents(session.Source, outFile);

                var restarted = session.EnableProvider("{6381f857-7661-4b04-9521-288319e75f12}");//"Intel-Gfx-Driver");
                session.Source.Process();

                Console.CancelKeyPress += delegate (object sender, ConsoleCancelEventArgs e)
                {
                    session.Dispose();
                };

                Console.ForegroundColor = ConsoleColor.Gray;
                Console.WriteLine("Stopping the collection of events.");
            }
        } // Main_ends

        public static void InitializeRegister()
        {
            reg.ReadRegister((uint)0x70008, ref uTrans_Conf[0]);  // Pipe /Transcoder 
            reg.ReadRegister((uint)0x71008, ref uTrans_Conf[1]);
            reg.ReadRegister((uint)0x72008, ref uTrans_Conf[2]);
            reg.ReadRegister((uint)0x7F008, ref uTrans_Conf[3]);

            reg.ReadRegister((uint)0x70180, ref uPlane_Ctrl[0]); // Plane
            reg.ReadRegister((uint)0x71180, ref uPlane_Ctrl[1]);
            reg.ReadRegister((uint)0x72180, ref uPlane_Ctrl[2]);

            reg.ReadRegister((uint)0x70080, ref uCur_Ctrl[0]); // Cursor
            reg.ReadRegister((uint)0x71080, ref uCur_Ctrl[1]);
            reg.ReadRegister((uint)0x72080, ref uCur_Ctrl[2]);


            reg.ReadRegister((uint)0x60400, ref uTrans_Ddi_Ctrl[0]); // Trans DDI
            reg.ReadRegister((uint)0x61400, ref uTrans_Ddi_Ctrl[1]);
            reg.ReadRegister((uint)0x62400, ref uTrans_Ddi_Ctrl[2]);
            reg.ReadRegister((uint)0x6F400, ref uTrans_Ddi_Ctrl[3]);

            reg.ReadRegister((uint)0x60200, ref uVideo_Dip_Ctrl[0]); // Video DIP Ctrl VSC
            reg.ReadRegister((uint)0x61200, ref uVideo_Dip_Ctrl[1]);
            reg.ReadRegister((uint)0x62200, ref uVideo_Dip_Ctrl[2]);
            reg.ReadRegister((uint)0x6F200, ref uVideo_Dip_Ctrl[3]);

            reg.ReadRegister((uint)0x60320, ref uVIdeo_Dip_HDR_data[0, 0]);
            reg.ReadRegister((uint)0x61320, ref uVIdeo_Dip_HDR_data[1, 0]);
            reg.ReadRegister((uint)0x62320, ref uVIdeo_Dip_HDR_data[2, 0]);
            reg.ReadRegister((uint)0x6F320, ref uVIdeo_Dip_HDR_data[3, 0]);


            reg.ReadRegister((uint)0x60334, ref uVideo_Dip_VSC_Colorimetry_Data[0]); // VSC Data 334 - has DB 16,17,18
            reg.ReadRegister((uint)0x61334, ref uVideo_Dip_VSC_Colorimetry_Data[1]);
            reg.ReadRegister((uint)0x62334, ref uVideo_Dip_VSC_Colorimetry_Data[2]);
            reg.ReadRegister((uint)0x6F334, ref uVideo_Dip_VSC_Colorimetry_Data[3]);

        } // InitializeRegisters_ends

        public static void VerifyResult(StreamWriter outFile)
        {
            Console.WriteLine("Entered Verify result");
            string plane_status = "";
            string cur_status = "";
            string hdr_status = "Disabled";
            string csc_status = "Disabled";
            uint pixel_format = 0;
            for (uint i = 0; i < 3; i++)
            {
                if (GetValue(uPlane_Ctrl[i], 31, 31) == 1) // Plane enable check
                {
                    switch (i)
                    {
                        case 0:
                            plane_status = "Plane 1A Enabled"; break;
                        case 1:
                            plane_status = "Plane 1B Enabled"; break;
                        case 2:
                            plane_status = "Plane 1C Enabled"; break;
                    }
                    pixel_format = GetValue(uPlane_Ctrl[i], 24, 27);
                    uint value = GetValue(uTrans_Ddi_Ctrl[i], 20, 22); // BPC
                    switch (value)
                    {
                        case 0:
                            uBPC[i] = 8; break;
                        case 1:
                            uBPC[i] = 10; break;
                        case 2:
                            uBPC[i] = 6; break;
                        case 3:
                            uBPC[i] = 12; break;
                        default:
                            uBPC[i] = 0; break;
                    }
                    if (GetValue(uVideo_Dip_Ctrl[i], 20, 20) == 1 || (GetValue(uVideo_Dip_Ctrl[i], 4, 4) == 1))// VSC/GMP Packet check
                        hdr_status = "Enabled";
                    if (GetValue(uPlane_Ctrl[i], 23, 23) == 1) // Pipe CSC check
                        csc_status = "Enabled";

                    if (GetValue(uCur_Ctrl[i], 0, 5) == 0)
                        cur_status = " HW Cursor - Disabled";
                    else
                        cur_status = "HW Cursor - Enabled";


                    Console.ForegroundColor = ConsoleColor.Gray;
                    Console.WriteLine(plane_status + " Pixel Format : " + pixel_format + " ;BPC:" + uBPC[i] + ";CSC status" + csc_status + " ;" + cur_status + ";HDR Status :" + hdr_status);
                    outFile.WriteLine(plane_status + " Pixel Format : " + pixel_format + " ;BPC:" + uBPC[i] + ";CSC status" + csc_status + " ;" + cur_status + ";HDR Status :" + hdr_status);

                    if (GetValue(uVideo_Dip_Ctrl[i], 20, 20) == 1 || (GetValue(uVideo_Dip_Ctrl[i], 4, 4) == 1)) // VSC/GMP Packet check
                    {
                        FetchMetadata(i, outFile);

                    }


                }
            }
        } // VerifyResult_ends

        public static void FetchMetadata(uint i, StreamWriter outFile)
        {
            if (hdrType == (int)HDR_TYPE.LSPCON_HDR)
            {
                for (int num = 0; num < 9; num++)
                    reg.ReadRegister(uVSC_Data[i, num], ref uVIdeo_Dip_HDR_data[i, num]);
            }
            else if (hdrType == (int)HDR_TYPE.DP_HDR)
            {
                for (int num = 0; num < 8; num++)
                    reg.ReadRegister(uGMP_Data[i, num], ref uVIdeo_Dip_HDR_data[i, num]);
            }

            Metadata_struct metadata = new Metadata_struct();

            metadata.uEOTF = GetValue(uVIdeo_Dip_HDR_data[i, 1], 16, 17);

            metadata.uDisplayPrimariesX0 = GetValue(uVIdeo_Dip_HDR_data[i, 2], 0, 15);

            metadata.uDisplayPrimariesY0 = GetValue(uVIdeo_Dip_HDR_data[i, 2], 16, 31);

            metadata.uDisplayPrimariesX1 = GetValue(uVIdeo_Dip_HDR_data[i, 3], 0, 15);

            metadata.uDisplayPrimariesY1 = GetValue(uVIdeo_Dip_HDR_data[i, 3], 16, 31);

            metadata.uDisplayPrimariesX2 = GetValue(uVIdeo_Dip_HDR_data[i, 4], 0, 15);

            metadata.uDisplayPrimariesY2 = GetValue(uVIdeo_Dip_HDR_data[i, 4], 16, 31);

            metadata.uWhitePtX = GetValue(uVIdeo_Dip_HDR_data[i, 5], 0, 15);

            metadata.uWhitePtY = GetValue(uVIdeo_Dip_HDR_data[i, 5], 16, 31);

            metadata.uMaxDispLum = GetValue(uVIdeo_Dip_HDR_data[i, 6], 0, 15);

            metadata.uMinDispLum = GetValue(uVIdeo_Dip_HDR_data[i, 6], 16, 31);

            metadata.uMaxCLL = GetValue(uVIdeo_Dip_HDR_data[i, 7], 0, 15);

            metadata.uMaxFALL = GetValue(uVIdeo_Dip_HDR_data[i, 7], 16, 31);


            PrintMetadata(metadata, outFile);

            Console.WriteLine("----------------------------------------------------------------------------------------------------------------------");


        } //FetchMetadata_ends



        public static void PrintMetadata(Metadata_struct metadata, StreamWriter outFile, bool ETL = false)
        {
            if (ETL == true)
            {
                Console.ForegroundColor = ConsoleColor.DarkYellow;
                Console.WriteLine("ETL Trace :");
                outFile.WriteLine("ETL Trace :");
                Console.WriteLine("HDRType : " + metadata.HDRType.ToString("x"));
                outFile.WriteLine("HDRType : " + metadata.HDRType.ToString("x"));
            }
            else
            {
                Console.ForegroundColor = ConsoleColor.DarkGreen;
                Console.WriteLine("Register values :");
                outFile.WriteLine("Register values :");
                Console.WriteLine("EOTF : " + metadata.uEOTF.ToString("x"));
                outFile.WriteLine("EOTF : " + metadata.uEOTF.ToString("x"));
            }
            Console.WriteLine(" DisplayPrimariesX[0] : " + metadata.uDisplayPrimariesX0.ToString("x") + " DisplayPrimariesY[0] : " + metadata.uDisplayPrimariesY0.ToString("x") +
                " DisplayPrimariesX[1] : " + metadata.uDisplayPrimariesX1.ToString("x") + " DisplayPrimariesY[1] : " + metadata.uDisplayPrimariesY1.ToString("x") +
                " DisplayPrimariesX[2] : " + metadata.uDisplayPrimariesX2.ToString("x") + " DisplayPrimariesY[2] : " + metadata.uDisplayPrimariesY2.ToString("x") +
                " WhitepointX: " + metadata.uWhitePtX.ToString("x") + " WhitepointY : " + metadata.uWhitePtY.ToString("x") +
                " MaxLuminance : " + metadata.uMaxDispLum.ToString("x") + " MinLuminance : " + metadata.uMinDispLum.ToString("x") +
                " MaxCLL : " + metadata.uMaxCLL.ToString("x") + " MaxFALL : " + metadata.uMaxFALL.ToString("x")
                );

            outFile.WriteLine(" DisplayPrimariesX[0] : " + metadata.uDisplayPrimariesX0.ToString("x") + " DisplayPrimariesY[0] : " + metadata.uDisplayPrimariesY0.ToString("x") +
                " DisplayPrimariesX[1] : " + metadata.uDisplayPrimariesX1.ToString("x") + " DisplayPrimariesY[1] : " + metadata.uDisplayPrimariesY1.ToString("x") +
                " DisplayPrimariesX[2] : " + metadata.uDisplayPrimariesX2.ToString("x") + " DisplayPrimariesY[2] : " + metadata.uDisplayPrimariesY2.ToString("x") +
                " WhitepointX : " + metadata.uWhitePtX.ToString("x") + " WhitepointY : " + metadata.uWhitePtY.ToString("x") +
                " MaxLuminance : " + metadata.uMaxDispLum.ToString("x") + " MinLuminance : " + metadata.uMinDispLum.ToString("x") +
                " MaxCLL : " + metadata.uMaxCLL.ToString("x") + " MaxFALL : " + metadata.uMaxFALL.ToString("x")
                );

            Console.ForegroundColor = ConsoleColor.Gray;

        }


        public static void LogETLEvents(TraceEventSource EventSource, StreamWriter outFile)
        {
            IntelGfxDriverTraceEventParser GfxParser = new IntelGfxDriverTraceEventParser(EventSource);
            int count = 0; int count1 = 0; int count_nextflip = 0;
            bool track_nextflip = false;

            GfxParser.DxgkDdiSetVidPnSourceAddressWithMultiPlaneOverlay3HDR_OS_METADATA += delegate (t_HDROSMetadata HDROSData)
             {
                 Console.WriteLine("Entered SSA3 OS Metadata ETL");
                 outFile.WriteLine("Entered SSA3 OS Metadata ETL");
                 curr_metadata.HDRType = (uint)HDROSData.MetadataType;
                 // When Metadata type is NONE and no metadata is sent from OS and  if the current Metadata != default metadata ,  verify  driver reprogramming
                 if (HDROSData.MetadataType == 0 && HDROSData.MaxMasteringLuminance == 0)
                 {
                     if (!curr_metadata.Equals(default_metadata))
                     {
                         curr_metadata = default_metadata;
                         track_nextflip = true;
                     }
                 }
                 //When Metadata type is HDR10 and OS metadata is sent , verify with driver programming
                 else if (HDROSData.MetadataType == 1)
                 {
                     if (HDROSData.MaxMasteringLuminance != 0) // the meatdata is not null
                     {
                         curr_metadata.uDisplayPrimariesX0 = (uint)HDROSData.GreenPrimaryX;
                         curr_metadata.uDisplayPrimariesY0 = (uint)HDROSData.GreenPrimaryY;
                         curr_metadata.uDisplayPrimariesX1 = (uint)HDROSData.BluePrimaryX;
                         curr_metadata.uDisplayPrimariesY1 = (uint)HDROSData.BluePrimaryY;
                         curr_metadata.uDisplayPrimariesX2 = (uint)HDROSData.RedPrimaryX;
                         curr_metadata.uDisplayPrimariesY2 = (uint)HDROSData.RedPrimaryY;
                         curr_metadata.uMaxDispLum = (uint)HDROSData.MaxMasteringLuminance;
                         curr_metadata.uMinDispLum = (uint)HDROSData.MinMasteringLuminance;
                         curr_metadata.uMaxCLL = (uint)HDROSData.MaxContentLightLevel;
                         curr_metadata.uMaxFALL = (uint)HDROSData.MaxFrameAverageLightLevel;

                         track_nextflip = true;

                         //  PrintMetadata(curr_metadata, outFile, true);
                         // VerifyResult(outFile);
                     }
                 }

                 PrintMetadata(curr_metadata, outFile, true);
                 VerifyResult(outFile);
             };

            GfxParser.DxgkDdiSetTargetAdjustedColorimetryStart += delegate (t_DxgkDdiSetTargetAdjustedColorimetry_Entry DefaultColorimetry)
            {
                Console.WriteLine("Entered Adjust colorimetry start ETL");
                outFile.WriteLine("Entered Adjust colorimetry start ETL");
                default_metadata.uDisplayPrimariesX0 = (uint)DefaultColorimetry.ColorimetryGreenPointcx;
                default_metadata.uDisplayPrimariesY0 = (uint)DefaultColorimetry.ColorimetryGreenPointcy;
                default_metadata.uDisplayPrimariesX1 = (uint)DefaultColorimetry.ColorimetryBluePointcx;
                default_metadata.uDisplayPrimariesY1 = (uint)DefaultColorimetry.ColorimetryBluePointcy;
                default_metadata.uDisplayPrimariesX2 = (uint)DefaultColorimetry.ColorimetryRedPointcx;
                default_metadata.uDisplayPrimariesY2 = (uint)DefaultColorimetry.ColorimetryRedPointcy;
            };

            GfxParser.DxgkDdiSetTargetAdjustedColorimetryLuminance_Data += delegate (t_LuminanceData DefaultLuminance)
            {
                Console.WriteLine("Entered Adjust colorimetry Luminance ETL");
                outFile.WriteLine("Entered Adjust colorimetry Luminance ETL");
                default_metadata.uMaxDispLum = (uint)DefaultLuminance.MaxLuminance;
                default_metadata.uMinDispLum = (uint)DefaultLuminance.MinLuminance;
                default_metadata.uMaxFALL = (uint)DefaultLuminance.MaxFullFrameLuminance;

                curr_metadata = default_metadata;

                PrintMetadata(curr_metadata, outFile, true);
                VerifyResult(outFile);
                track_nextflip = true;
            };
            GfxParser.SetHDRMetaData += delegate (t_SetHDRMetaData EscapeMetadata)
            {
                Console.WriteLine("Escape HDR ETL");
                outFile.WriteLine("Escape HDR ETL");
                curr_metadata.uEOTF = (uint)EscapeMetadata.EOTF;
                curr_metadata.uDisplayPrimariesX0 = (uint)EscapeMetadata.DisplayPrimariesX0;
                curr_metadata.uDisplayPrimariesX1 = (uint)EscapeMetadata.DisplayPrimariesX1;
                curr_metadata.uDisplayPrimariesX2 = (uint)EscapeMetadata.DisplayPrimariesX2;
                curr_metadata.uDisplayPrimariesY0 = (uint)EscapeMetadata.DisplayPrimariesY0 & 0xffff;
                curr_metadata.uDisplayPrimariesY1 = (uint)EscapeMetadata.DisplayPrimariesY1 & 0xffff;
                curr_metadata.uDisplayPrimariesY2 = (uint)EscapeMetadata.DisplayPrimariesY2 & 0xffff;
                curr_metadata.uWhitePtX = (uint)EscapeMetadata.WhitePointX;
                curr_metadata.uWhitePtX = (uint)EscapeMetadata.WhitePointY;
                curr_metadata.uMaxDispLum = (uint)EscapeMetadata.MaxDisplayMasteringLuminance;
                curr_metadata.uMinDispLum = (uint)EscapeMetadata.MinDisplayMasteringLuminance;
                curr_metadata.uMaxCLL = (uint)EscapeMetadata.MaxCLL;
                curr_metadata.uMaxFALL = (uint)EscapeMetadata.MaxFALL;

                count1++;

                if (count1 % 20 == 0)
                {
                    PrintMetadata(curr_metadata, outFile, true);
                    VerifyResult(outFile);
                }
            };

            GfxParser.DxgkDdiSetVidPnSourceAddressWithMultiPlaneOverlay3Plane += delegate (t_DxgkDdiSetVidPnSourceAddressWithMultiPlaneOverlay3Info entry)
            {
                count++;

                if (track_nextflip == true)
                {
                    count_nextflip++;
                    Console.WriteLine(" Flips after metadata change !!");
                    outFile.WriteLine(" Flips after metadata change!!");

                    VerifyResult(outFile);

                    if (count_nextflip % 5 == 0)
                    { track_nextflip = false; count_nextflip = 0; }
                }
                if (count % 100 == 0 || track_nextflip == true)
                {
                    Console.WriteLine(" SSA3 Flip!!");
                    Console.WriteLine("Colorspace Type : " + entry.eColorSpace1);
                    outFile.WriteLine(" SSA3 Flip!!");
                    VerifyResult(outFile);
                }

            };

            GfxParser.DxgkDdiCheckMultiPlaneOverlaySupport3Stop += delegate (t_DxgkDdiCheckMultiPlaneOverlaySupport3 exit)
            {
                Console.WriteLine("CheckMPO Exit !!  Supported : " + exit.Supported);
            };
        }
        public static uint GetValue(uint value, int start, int end)
        {
            uint retvalue = value << (31 - end);
            retvalue >>= (31 - end + start);
            return retvalue;
        }

    } // class_end
} // namespace_end


