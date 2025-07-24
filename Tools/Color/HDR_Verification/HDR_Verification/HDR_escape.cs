using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

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
        public unsafe fixed uint uDisplayPrimariesX[3];
        public unsafe fixed uint uDisplayPrimariesY[3];
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

        public static uint[] uVideo_Dip_VSC_Colorimetry_Data = new uint[4];

        static void Main(string[] args)
        {
            if (args.Length < 1)
            {
                Console.WriteLine(" Commandline params missing!! \n Parameter 1 : LSPCON_HDR/DP_HDR/HDMI_HDR \n Parameter 2 : Delay in seconds (optional)");
            }
            if (args.Length == 1 || args.Length == 2)
            {
                if (string.Equals(args[0], "LSPCON_HDR", StringComparison.OrdinalIgnoreCase))
                    hdrType = (int)HDR_TYPE.LSPCON_HDR;
                else if (string.Equals(args[0], "DP_HDR", StringComparison.OrdinalIgnoreCase))
                    hdrType = (int)HDR_TYPE.DP_HDR;
                else if (string.Equals(args[0], "HDMI_HDR", StringComparison.OrdinalIgnoreCase))
                    hdrType = (int)HDR_TYPE.HDMI_HDR;
                Console.WriteLine("Entered!!");
            }
            if (args.Length == 2)
            {

                Console.WriteLine(" Delay of " + args[1] + " second is added to the script");

                CmnDelay.Seconds(Int32.Parse(args[1]));
            }
            InitializeRegister();

            FileStream writerOutput = new FileStream("C:\\Intel\\out.txt", FileMode.Create, FileAccess.Write);
            StreamWriter writer = new StreamWriter(writerOutput);
            Console.SetOut(writer);

            Console.WriteLine("\n ****************** OUTPUT *******************\n ");

            VerifyResult();

            writer.Close();
            writerOutput.Close();



            Console.ReadLine();
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



        public static void VerifyResult()
        {
            for (uint i = 0; i < 3; i++)
            {
                Console.WriteLine(" \n ");

                if (GetValue(uPlane_Ctrl[i], 31, 31) == 1) // Plane enable check
                {
                    Console.WriteLine(" Plane " + (i + 1) + " : Enabled");

                    if (GetValue(uTrans_Conf[i], 31, 31) == 1) // transcoder enable check
                    {
                        Console.WriteLine(" Pipe " + (i + 1) + " : Enabled");

                        uint value = GetValue(uTrans_Ddi_Ctrl[i], 20, 22); // BPC

                        switch (value)
                        {
                            case 0:
                                uBPC[i] = 8; break;
                            case 1:
                                uBPC[i] = 10; break;
                            case 3:
                                uBPC[i] = 12; break;
                            default:
                                uBPC[i] = 0; break;
                        }

                        Console.WriteLine(" Bits per Color : " + uBPC[i]);

                        if (GetValue(uPlane_Ctrl[i], 23, 23) == 1) // Pipe CSC check
                        {
                            uCSC[i] = "Enabled";
                            GetCSCCoeff(i);
                        }

                        GetCSCCoeff(i);

                        if (GetValue(uPlane_Ctrl[i], 30, 30) == 1) // Pipe Gamma check
                        {
                            uGamma[i] = "Enabled";
                        }

                        Console.WriteLine(" Pipe " + (i + 1) + " CSC : " + uCSC[i]);
                        Console.WriteLine(" Pipe " + (i + 1) + " Gamma : " + uGamma[i]);

                        uVideo_Dip_Ctrl[i] = 0x100000; //dummy
                        if (hdrType == (int)HDR_TYPE.LSPCON_HDR)
                        {
                            if (GetValue(uVideo_Dip_Ctrl[i], 20, 20) == 1) // VSC Packet check
                            {
                                Console.WriteLine(" ********* VSC packet Data *********** ");
                                FetchMetadata(i);
                                PrintMetadata(i);
                            }
                        }
                        else if (hdrType == (int)HDR_TYPE.DP_HDR)
                        {
                            if (GetValue(uVideo_Dip_Ctrl[i], 4, 4) == 1) // GMP Packet check
                            {
                                Console.WriteLine(" ********* GMP packet Data *********** ");
                                FetchMetadata(i);
                                PrintMetadata(i);
                            }
                            if (GetValue(uTrans_Ddi_Ctrl[i], 6, 6) == 1)
                            {
                                if (GetValue(uVideo_Dip_Ctrl[i], 20, 20) == 1) // VSC Packet check
                                {
                                    Console.WriteLine(" ********* VSC packet Colorimetry Data *********** ");
                                    FetchColorimetrydata(i);
                                }
                            }
                        }
                        else if (hdrType == (int)HDR_TYPE.HDMI_HDR)
                        {
                            Console.WriteLine(" ********* DRM DIP packet Colorimetry Data *********** ");
                            FetchMetadata(i);

                            PrintMetadata(i);
                        }

                    }

                    else if (GetValue(uTrans_Conf[3], 31, 31) == 1)
                    {
                        Console.WriteLine(" Pipe " + (i + 1) + " : Enabled");

                        uint value = GetValue(uTrans_Ddi_Ctrl[3], 20, 22); // BPC


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

                        Console.WriteLine(" Bits per Color : " + uBPC[i]);



                        if (GetValue(uPlane_Ctrl[i], 23, 23) == 1) // Pipe CSC check
                        {
                            uCSC[i] = "Enabled";
                            GetCSCCoeff(i);

                            // GetExpectedCSCCoeffValue(i);
                        }
                        GetCSCCoeff(i);

                        if (GetValue(uPlane_Ctrl[i], 30, 30) == 1) // Pipe Gamma check
                        {
                            uGamma[i] = "Enabled";
                        }

                        Console.WriteLine(" Pipe " + (i + 1) + " CSC : " + uCSC[i]);
                        Console.WriteLine(" Pipe " + (i + 1) + " Gamma : " + uGamma[i]);

                        uVideo_Dip_Ctrl[3] = 0x100000; //dummy

                        if (GetValue(uVideo_Dip_Ctrl[3], 20, 20) == 1) // VSC Packet check
                        {
                            Console.WriteLine(" ********* VSC packet Data *********** ");

                            FetchMetadata(3);

                            PrintMetadata(3);
                        }
                        else
                        {
                            if (GetValue(uVideo_Dip_Ctrl[3], 4, 4) == 1) // GMP Packet check
                            {
                                Console.WriteLine(" ********* GMP packet Data *********** ");

                                FetchMetadata(3);

                                PrintMetadata(3);
                            }
                            if (GetValue(uTrans_Ddi_Ctrl[3], 6, 6) == 1)
                            {
                                if (GetValue(uVideo_Dip_Ctrl[3], 20, 20) == 1) // VSC Packet check
                                {
                                    Console.WriteLine(" ********* VSC packet Colorimetry Data *********** ");

                                    FetchColorimetrydata(3);


                                }
                            }
                        }
                    }


                }
            } // for_end

        } // VerifyResult_ends

        public static void FetchMetadata(uint id)
        {
            if (hdrType == (int)HDR_TYPE.LSPCON_HDR)
            {
                reg.ReadRegister(uVSC_Data[id, 0], ref uVIdeo_Dip_HDR_data[id, 0]);
                reg.ReadRegister(uVSC_Data[id, 1], ref uVIdeo_Dip_HDR_data[id, 1]);
                reg.ReadRegister(uVSC_Data[id, 2], ref uVIdeo_Dip_HDR_data[id, 2]);
                reg.ReadRegister(uVSC_Data[id, 3], ref uVIdeo_Dip_HDR_data[id, 3]);
                reg.ReadRegister(uVSC_Data[id, 4], ref uVIdeo_Dip_HDR_data[id, 4]);
                reg.ReadRegister(uVSC_Data[id, 5], ref uVIdeo_Dip_HDR_data[id, 5]);
                reg.ReadRegister(uVSC_Data[id, 6], ref uVIdeo_Dip_HDR_data[id, 6]);
                reg.ReadRegister(uVSC_Data[id, 7], ref uVIdeo_Dip_HDR_data[id, 7]);
                reg.ReadRegister(uVSC_Data[id, 8], ref uVIdeo_Dip_HDR_data[id, 8]);
            }
            else if (hdrType == (int)HDR_TYPE.DP_HDR)
            {
                reg.ReadRegister(uGMP_Data[id, 0], ref uVIdeo_Dip_HDR_data[id, 0]);
                reg.ReadRegister(uGMP_Data[id, 1], ref uVIdeo_Dip_HDR_data[id, 1]);
                reg.ReadRegister(uGMP_Data[id, 2], ref uVIdeo_Dip_HDR_data[id, 2]);
                reg.ReadRegister(uGMP_Data[id, 3], ref uVIdeo_Dip_HDR_data[id, 3]);
                reg.ReadRegister(uGMP_Data[id, 4], ref uVIdeo_Dip_HDR_data[id, 4]);
                reg.ReadRegister(uGMP_Data[id, 5], ref uVIdeo_Dip_HDR_data[id, 5]);
                reg.ReadRegister(uGMP_Data[id, 6], ref uVIdeo_Dip_HDR_data[id, 6]);
                reg.ReadRegister(uGMP_Data[id, 7], ref uVIdeo_Dip_HDR_data[id, 7]);


            }

            else if (hdrType == (int)HDR_TYPE.HDMI_HDR)
            {
                reg.ReadRegister(uDRM_Data[id, 0], ref uVIdeo_Dip_HDR_data[id, 0]);
                reg.ReadRegister(uDRM_Data[id, 1], ref uVIdeo_Dip_HDR_data[id, 1]);
                reg.ReadRegister(uDRM_Data[id, 2], ref uVIdeo_Dip_HDR_data[id, 2]);
                reg.ReadRegister(uDRM_Data[id, 3], ref uVIdeo_Dip_HDR_data[id, 3]);
                reg.ReadRegister(uDRM_Data[id, 4], ref uVIdeo_Dip_HDR_data[id, 4]);
                reg.ReadRegister(uDRM_Data[id, 5], ref uVIdeo_Dip_HDR_data[id, 5]);
                reg.ReadRegister(uDRM_Data[id, 6], ref uVIdeo_Dip_HDR_data[id, 6]);
                reg.ReadRegister(uDRM_Data[id, 7], ref uVIdeo_Dip_HDR_data[id, 7]);


            }


        } //FetchMetadata_ends


        unsafe public static void PrintMetadata(uint i)
        {
            Metadata_struct metadata = new Metadata_struct();

            metadata.uEOTF = ((uVIdeo_Dip_HDR_data[i, 1] & 0x00030000) >> 16);
            metadata.uEOTF = GetValue(uVIdeo_Dip_HDR_data[i, 1], 16, 17);
            Console.WriteLine("EOTF : " + metadata.uEOTF.ToString("x"));

            metadata.uDisplayPrimariesX[0] = (uVIdeo_Dip_HDR_data[i, 2] & 0x0000FFFF);
            metadata.uDisplayPrimariesX[0] = GetValue(uVIdeo_Dip_HDR_data[i, 2], 0, 15);
            Console.WriteLine(" DisplayPrimariesX[0] : " + metadata.uDisplayPrimariesX[0].ToString("x"));

            metadata.uDisplayPrimariesY[0] = ((uVIdeo_Dip_HDR_data[i, 2] & 0xFFFF0000) >> 16);
            metadata.uDisplayPrimariesY[0] = GetValue(uVIdeo_Dip_HDR_data[i, 2], 16, 31);
            Console.WriteLine(" DisplayPrimariesY[0] : " + metadata.uDisplayPrimariesY[0].ToString("x"));

            metadata.uDisplayPrimariesX[1] = (uVIdeo_Dip_HDR_data[i, 3] & 0x0000FFFF);
            metadata.uDisplayPrimariesX[1] = GetValue(uVIdeo_Dip_HDR_data[i, 3], 0, 15);
            Console.WriteLine(" DisplayPrimariesX[1] : " + metadata.uDisplayPrimariesX[1].ToString("x"));

            metadata.uDisplayPrimariesY[1] = ((uVIdeo_Dip_HDR_data[i, 3] & 0xFFFF0000) >> 16);
            metadata.uDisplayPrimariesY[1] = GetValue(uVIdeo_Dip_HDR_data[i, 3], 16, 31);
            Console.WriteLine(" DisplayPrimariesY[1] : " + metadata.uDisplayPrimariesY[1].ToString("x"));

            metadata.uDisplayPrimariesX[2] = (uVIdeo_Dip_HDR_data[i, 4] & 0x0000FFFF);
            metadata.uDisplayPrimariesX[2] = GetValue(uVIdeo_Dip_HDR_data[i, 4], 0, 15);
            Console.WriteLine(" DisplayPrimariesX[2] : " + metadata.uDisplayPrimariesX[2].ToString("x"));

            metadata.uDisplayPrimariesY[2] = ((uVIdeo_Dip_HDR_data[i, 4] & 0xFFFF0000) >> 16);
            metadata.uDisplayPrimariesY[2] = GetValue(uVIdeo_Dip_HDR_data[i, 4], 16, 31);
            Console.WriteLine(" DisplayPrimariesY[2] : " + metadata.uDisplayPrimariesY[2].ToString("x"));

            metadata.uWhitePtX = (uVIdeo_Dip_HDR_data[i, 5] & 0x0000FFFF);
            metadata.uWhitePtX = GetValue(uVIdeo_Dip_HDR_data[i, 5], 0, 15);
            Console.WriteLine(" WhitepointX[1] : " + metadata.uWhitePtX.ToString("x"));

            metadata.uWhitePtY = ((uVIdeo_Dip_HDR_data[i, 5] & 0xFFFF0000) >> 16);
            metadata.uWhitePtY = GetValue(uVIdeo_Dip_HDR_data[i, 5], 16, 31);
            Console.WriteLine(" WhitepointY[2] : " + metadata.uWhitePtY.ToString("x"));

            metadata.uMaxDispLum = GetValue(uVIdeo_Dip_HDR_data[i, 6], 0, 15);
            Console.WriteLine(" MaxLuminance : " + metadata.uMaxDispLum.ToString("x"));

            metadata.uMinDispLum = GetValue(uVIdeo_Dip_HDR_data[i, 6], 16, 31);
            Console.WriteLine(" MinLuminance : " + metadata.uMinDispLum.ToString("x"));

            metadata.uMaxCLL = GetValue(uVIdeo_Dip_HDR_data[i, 7], 0, 15);
            Console.WriteLine(" MaxCLL : " + metadata.uMaxCLL.ToString("x"));

            metadata.uMaxFALL = GetValue(uVIdeo_Dip_HDR_data[i, 7], 16, 31);
            Console.WriteLine(" MaxFALL : " + metadata.uMaxFALL.ToString("x"));

        }

        public static void FetchColorimetrydata(uint pipeIndex)
        {
            uint pixel_encoding = GetValue(uVideo_Dip_VSC_Colorimetry_Data[pipeIndex], 4, 7);
            switch (pixel_encoding)
            {
                case 0: Console.WriteLine(" Pixel Encoding : RGB"); break;
                case 1: Console.WriteLine(" Pixel Encoding : YUV444"); break;
                case 2: Console.WriteLine(" Pixel Encoding : YUV422"); break;
                case 3: Console.WriteLine(" Pixel Encoding : YUV420"); break;
                case 4: Console.WriteLine(" Pixel Encoding : Y only"); break;
                case 5: Console.WriteLine(" Pixel Encoding : Raw"); break;
                default: break;

            }
            if (pixel_encoding == 1 || pixel_encoding == 3)
            {
                switch (GetValue(uVideo_Dip_VSC_Colorimetry_Data[pipeIndex], 0, 3))
                {

                    case 0: Console.WriteLine("Colorimetry : ITU-R BT601"); break;
                    case 1: Console.WriteLine("Colorimetry : ITU-R BT709"); break;
                    case 2: Console.WriteLine("Colorimetry : xvYCC601"); break;
                    case 3: Console.WriteLine("Colorimetry : xvYCC709"); break;
                    case 4: Console.WriteLine("Colorimetry : sYCC 601"); break;
                    case 5: Console.WriteLine("Colorimetry : Adobe YCC601"); break;
                    case 6: Console.WriteLine("Colorimetry : ITU-R BT2020 Y'CC'BCC'RC"); break;
                    case 7: Console.WriteLine("Colorimetry : ITU-R BT2020 Y'C'BC'R"); break;
                }
            }
            else
            {
                switch (GetValue(uVideo_Dip_VSC_Colorimetry_Data[pipeIndex], 0, 3))
                {

                    case 0: Console.WriteLine("Colorimetry : sRGB"); break;
                    case 1: Console.WriteLine("Colorimetry : Widegamut_FixedPoint"); break;
                    case 2: Console.WriteLine("Colorimetry : Widegamut_FloatingPoint"); break;
                    case 3: Console.WriteLine("Colorimetry : Adobe"); break;
                    case 4: Console.WriteLine("Colorimetry : DCIP3"); break;
                    case 5: Console.WriteLine("Colorimetry : CustomColorProfile"); break;
                    case 6: Console.WriteLine("Colorimetry : ITU-R BT2020 RGB"); break;

                }
            }


            switch (GetValue(uVideo_Dip_VSC_Colorimetry_Data[pipeIndex], 8, 10))
            {
                case 1: Console.WriteLine("BitDepth : 8bit"); break;
                case 2: Console.WriteLine("BitDepth : 10bit"); break;
                case 3: Console.WriteLine("Bitdepth : 12bit"); break;
                case 4: Console.WriteLine("BitDepth : 16bit"); break;
            }

        }

        public static uint GetValue(uint value, int start, int end)
        {
            uint retvalue = value << (31 - end);
            retvalue >>= (31 - end + start);
            return retvalue;
        }

        public static void GetCSCCoeff(uint i)
        {
            uint temp = 0;
            uint registerCSC = 0;
            uint registerCSCPostoff = 0;
            double outVal;

            if (i == 0)
            { registerCSC = (uint)0x49010; registerCSCPostoff = (uint)0x49040; }
            else if (i == 1)
            { registerCSC = (uint)0x49110; registerCSCPostoff = (uint)0x49140; }
            else if (i == 2)
            { registerCSC = (uint)0x49210; registerCSCPostoff = (uint)0x49240; }
            else if (i == 3)
            { registerCSC = (uint)0x49310; registerCSCPostoff = (uint)0x49240; }

            reg.ReadRegister(registerCSC, ref temp);
            uCSCCoeff[0, 0] = GetValue(temp, 16, 31);
            uCSCCoeff[0, 1] = GetValue(temp, 0, 15);

            reg.ReadRegister((registerCSC + 4), ref temp);
            uCSCCoeff[0, 2] = GetValue(temp, 16, 31);

            reg.ReadRegister((registerCSC + 8), ref temp);
            uCSCCoeff[1, 0] = GetValue(temp, 16, 31);
            uCSCCoeff[1, 1] = GetValue(temp, 0, 15);

            uint x1 = (registerCSC + (uint)0xC);

            reg.ReadRegister((uint)0x4901C, ref temp);
            uCSCCoeff[1, 2] = GetValue(temp, 16, 31);

            reg.ReadRegister((registerCSC + (uint)0x10), ref temp);
            uCSCCoeff[2, 0] = GetValue(temp, 16, 31);
            uCSCCoeff[2, 1] = GetValue(temp, 0, 15);

            reg.ReadRegister((registerCSC + 0x14), ref temp);
            uCSCCoeff[2, 2] = GetValue(temp, 16, 31);

            reg.ReadRegister((registerCSCPostoff), ref temp);
            uCSCPostOffset[0] = GetValue(temp, 0, 12);

            reg.ReadRegister((registerCSCPostoff + 4), ref temp);
            uCSCPostOffset[1] = GetValue(temp, 0, 12);

            reg.ReadRegister((registerCSCPostoff + 8), ref temp);
            uCSCPostOffset[2] = GetValue(temp, 0, 12);



            for (uint x = 0; x < 3; x++)
            {
                for (uint y = 0; y < 3; y++)
                {
                    outVal = Convert_CSC_RegFormat_to_Coeff(uCSCCoeff[x, y]);
                    Console.WriteLine("CSC offset[" + x + "][" + y + "] -->  From H/W reg :" + outVal);
                }
            }

            Console.WriteLine("CSC PostOffset Coefficients -->  From H/W reg : {" + uCSCPostOffset[0] + "," + uCSCPostOffset[1] + "," + uCSCPostOffset[2] + "}");


        }

        public static double Convert_CSC_RegFormat_to_Coeff(uint cscCoeff)
        {
            double outVal = 0.0, scale_factor = 0.0;

            uint sign, exponent;
            int mantissa;

            uint positionOfPointFromRight = 0;


            sign = GetValue(cscCoeff, 15, 15);
            exponent = GetValue(cscCoeff, 12, 14);
            mantissa = (int)GetValue(cscCoeff, 3, 11);

            switch (exponent)
            {
                case 6:
                    positionOfPointFromRight = 7; break;
                case 7:
                    positionOfPointFromRight = 8; break;
                case 0:
                    positionOfPointFromRight = 9; break;
                case 1:
                    positionOfPointFromRight = 10; break;
                case 2:
                    positionOfPointFromRight = 11; break;
                case 3:
                    positionOfPointFromRight = 12; break;

            }

            scale_factor = Math.Pow(2, (double)positionOfPointFromRight);

            outVal = (double)mantissa / scale_factor;

            if (sign == 1)
                outVal = outVal * -1;

            return outVal;
        }





    } // class_end



} // namespace_end

