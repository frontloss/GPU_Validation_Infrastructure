using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;

//Extra added DLL
using IgfxExtBridge_DotNet;
using Intel.Display.Automation.Common;
using Intel.Display.Automation.TestsCommon;


namespace HDRVerification
{
    enum SourcePixelFormat
    {
        Indexed_8bit = 12,
        RGB_32_bit_XR_BIAS101010 = 10,
        YUV_16_bit422 = 0,
        RGB_16_bit565 = 14,
        P010_YUV_420_10bit = 3,
        RGB_32_bit_8888 = 4,
        NV12_YUV_420 = 1,
        RGB_32_2101010 = 2,
        P012_YUV_420_12bit = 5,
        YUV_32_bit_444 = 8,
        RGB_64bit_16161616_UINT = 9,
        RGB_64bit_16161616_float = 6,
        P016_YUV_420_16_bit = 7,
        Invalid_format = 100

    };

    class Program
    {
        [DllImport("Utilities.dll")]
        private static extern UInt32 writeMMIOReg(UInt32 dwOffset, UInt32 dwValue);

        public static RegisterModule reg = new RegisterModule();

        public static uint[] uTrans_Conf = { 0, 0, 0, 0, 0 }; // trans A,trans B,trans C,trans D,trans EDP   
        public static uint uDsiPLL = 0;
        public static uint[] uMIPICtrl = { 0, 0 };
        public static uint[] uMIPIPort = { 0, 0 };
        public static bool edp = false;

        public static uint[,] uPlane_Ctrl = { {0,0,0,0},
                                              {0,0,0,0},
                                              {0,0,0,0},
                                              {0,0,0,0} }; // Plane Ctrl for 1-4 wro Pipe A-D
        public static uint[,] uPlane_Color_Ctrl = { {0,0,0,0},
                                                     {0,0,0,0},
                                                     {0,0,0,0},
                                                     {0,0,0,0} }; // Color ctrl for plane 1-4 wrto Pipe A-D

        public static uint[,] uCSCCoeff = { { 0, 0, 0 }, { 0, 0, 0 }, { 0, 0, 0 } };
        public static uint[] uCSCPostOffset = { 0, 0, 0 };



        static double[,] uBT2020RGBtoYUVCoeff ={ {0.2627,0.6780,0.0593},
                                                  {-0.13963,-0.36036,0.5},
                                                  {0.5 ,-0.45978,-0.04021}
                                                };

        public static uint[] PalPrecIndex = { 0x4A400, 0x4AC00, 0x4B400, 0x4BC00 };
        public static uint[] PalPrecData = { 0x4A404, 0x4AC04, 0x4B404, 0x4BC04 };
        public static uint[] PalGCMax = { 0x4A410, 0x4AC10, 0x4B410, 0x4BC10 };
        public static uint[] PalExtGCMax = { 0x4A420, 0x4AC20, 0x4B420, 0x4BC20 };
        public static uint[] PalExt2GCMax = { 0x4A430, 0x4AC30, 0x4B430, 0x4BC30 };
        public static uint[] PipePreCSCGammaIndex = { 0x4A484, 0x4AC84, 0x4B484, 0x4BC84 };
        public static uint[] PipePreCSCGammaData = { 0x4A488, 0x4AC88, 0x4B488, 0x4BC88 };
        public static uint[,] PlanePreCSCGammaIndex = { {0x701D0,0x702D0,0x703D0,0x704D0},
                                                        {0x711D0,0x712D0,0x713D0,0x714D0},
                                                        {0x721D0,0x722D0,0x723D0,0x724D0},
                                                        {0x731D0,0x732D0,0x733D0,0x734D0}
                                                     }; // PlanePreCSCGammaData will be Index + 4
        public static uint[,] PlanePostCSCGammaIndex = {{0x701D8,0x702D8,0x703D8,0x704D8},
                                                        {0x711D8,0x712D8,0x713D8,0x714D8},
                                                        {0x721D8,0x722D8,0x723D8,0x724D8},
                                                        {0x731D8,0x732D8,0x733D8,0x734D8}
                                                     }; // PlanePostCSCGammaData will be Index + 4

        public static uint[] PlanePreCSCGammaData = { 0x4A488, 0x4AC88, 0x4B488, 0x4BC88 };

        static void Main(string[] args)
        {
            string stepping = "B0";

            if (args.Length == 1)
            {
                Console.WriteLine(" Delay of " + args[0] + " second is added to the script");

                CmnDelay.Seconds(Int32.Parse(args[0]));
            }

            if (args.Length == 2)
            {
                stepping = args[1];
                Console.WriteLine(" Stepping :" + stepping);

                Console.WriteLine(" Delay of " + args[0] + " second is added to the script");

                CmnDelay.Seconds(Int32.Parse(args[0]));

            }
            InitializeRegister();
            System.IO.Directory.CreateDirectory(@"C:\Intel\BT2020");
            FileStream writerOutput = new FileStream(@"C:\Intel\BT2020\Output.txt", FileMode.Create, FileAccess.Write);
            StreamWriter writer = new StreamWriter(writerOutput);
            Console.SetOut(writer);

            Console.WriteLine("\n ****************** OUTPUT *******************\n ");
            if (String.Compare(stepping, "A0", true) == 0)
                VerifyResultColor();
            else
                VerifyResultBT2020();

            writer.Close();
            writerOutput.Close();

            Console.ReadLine();
        } // Main_ends

        public static void InitializeRegister()
        {
            reg.ReadRegister((uint)0x70008, ref uTrans_Conf[0]);  // Pipe /Transcoder 
            reg.ReadRegister((uint)0x71008, ref uTrans_Conf[1]);
            reg.ReadRegister((uint)0x72008, ref uTrans_Conf[2]);
            reg.ReadRegister((uint)0x73008, ref uTrans_Conf[3]);
            reg.ReadRegister((uint)0x7F008, ref uTrans_Conf[4]);

            reg.ReadRegister((uint)0x70180, ref uPlane_Ctrl[0, 0]); // Plane 1-4 Pipe A
            reg.ReadRegister((uint)0x70280, ref uPlane_Ctrl[0, 1]);
            reg.ReadRegister((uint)0x70380, ref uPlane_Ctrl[0, 2]);
            reg.ReadRegister((uint)0x70480, ref uPlane_Ctrl[0, 3]);

            reg.ReadRegister((uint)0x71180, ref uPlane_Ctrl[1, 0]); // Plane 1-4 Pipe B
            reg.ReadRegister((uint)0x71280, ref uPlane_Ctrl[1, 1]);
            reg.ReadRegister((uint)0x71380, ref uPlane_Ctrl[1, 2]);
            reg.ReadRegister((uint)0x71480, ref uPlane_Ctrl[1, 3]);


            reg.ReadRegister((uint)0x72180, ref uPlane_Ctrl[2, 0]); // Plane 1-4 Pipe C
            reg.ReadRegister((uint)0x72280, ref uPlane_Ctrl[2, 1]);
            reg.ReadRegister((uint)0x72380, ref uPlane_Ctrl[2, 2]);
            reg.ReadRegister((uint)0x72480, ref uPlane_Ctrl[2, 3]);


            reg.ReadRegister((uint)0x73180, ref uPlane_Ctrl[3, 0]); // Plane 1-4 Pipe D
            reg.ReadRegister((uint)0x73280, ref uPlane_Ctrl[3, 1]);
            reg.ReadRegister((uint)0x73380, ref uPlane_Ctrl[3, 2]);
            reg.ReadRegister((uint)0x73480, ref uPlane_Ctrl[3, 3]);

            reg.ReadRegister((uint)0x701CC, ref uPlane_Color_Ctrl[0, 0]); // Plane 1-4 Pipe A
            reg.ReadRegister((uint)0x702CC, ref uPlane_Color_Ctrl[0, 1]);
            reg.ReadRegister((uint)0x703CC, ref uPlane_Color_Ctrl[0, 2]);
            reg.ReadRegister((uint)0x704CC, ref uPlane_Color_Ctrl[0, 3]);

            reg.ReadRegister((uint)0x711CC, ref uPlane_Color_Ctrl[1, 0]); // Plane 1-4 Pipe B
            reg.ReadRegister((uint)0x712CC, ref uPlane_Color_Ctrl[1, 1]);
            reg.ReadRegister((uint)0x713CC, ref uPlane_Color_Ctrl[1, 2]);
            reg.ReadRegister((uint)0x714CC, ref uPlane_Color_Ctrl[1, 3]);

            reg.ReadRegister((uint)0x721CC, ref uPlane_Color_Ctrl[2, 0]); // Plane 1-4 Pipe C
            reg.ReadRegister((uint)0x722CC, ref uPlane_Color_Ctrl[2, 1]);
            reg.ReadRegister((uint)0x723CC, ref uPlane_Color_Ctrl[2, 2]);
            reg.ReadRegister((uint)0x724CC, ref uPlane_Color_Ctrl[2, 3]);

            reg.ReadRegister((uint)0x731CC, ref uPlane_Color_Ctrl[3, 0]); // Plane 1-4 Pipe D
            reg.ReadRegister((uint)0x732CC, ref uPlane_Color_Ctrl[3, 1]);
            reg.ReadRegister((uint)0x733CC, ref uPlane_Color_Ctrl[3, 2]);
            reg.ReadRegister((uint)0x734CC, ref uPlane_Color_Ctrl[3, 3]);

            reg.ReadRegister((uint)0x46080, ref uDsiPLL);
            reg.ReadRegister((uint)0x6B104, ref uMIPICtrl[0]);
            reg.ReadRegister((uint)0x6B904, ref uMIPICtrl[1]);
            reg.ReadRegister((uint)0x6B0C0, ref uMIPIPort[0]);
            reg.ReadRegister((uint)0x6B8C0, ref uMIPIPort[1]);

        } // InitializeRegisters_ends

        public static void VerifyResultBT2020()
        {


            for (uint i = 0; i < 4; i++) // Pipe set - A/B/C/D
            {
                Console.WriteLine("\n***********Pipe " + (i + 1) + "************\n");
                if (GetValue(uTrans_Conf[i], 31, 31) == 1)
                    Console.WriteLine("Pipe " + (i + 1) + "\t\t\t : Enabled");
                else if (GetValue(uTrans_Conf[4], 31, 31) == 1 && edp != true)
                {
                    Console.WriteLine(" Pipe EDP \t\t\t : Enabled");
                    edp = true;
                }
                else if (GetValue(uDsiPLL, 31, 31) == 1)
                {
                    if (GetValue(uMIPIPort[0], 31, 31) == 1 && GetValue(uMIPICtrl[0], 7, 9) == i)
                        Console.WriteLine("MIPI A \t\t\t: Enabled");
                    else if (GetValue(uMIPIPort[1], 31, 31) == 1 && GetValue(uMIPICtrl[1], 7, 9) == i)
                        Console.WriteLine("MIPI C \t\t\t: Enabled");
                }
                else
                {
                    Console.WriteLine("Pipe " + (i + 1) + "\t\t\t : Disabled");
                    continue;
                }

                for (uint j = 0; j < 4; j++) // Plane -> 1-4
                {
                    if (GetValue(uPlane_Ctrl[i, j], 31, 31) == 1) // Plane enable check
                    {
                        Console.WriteLine("Plane " + (j + 1) + " \t\t : Enabled");

                        Console.WriteLine("Plane source pixel format : " + GetPlaneFormat(GetValue(uPlane_Ctrl[i, j], 24, 27)));

                        if (GetValue(uPlane_Color_Ctrl[i, j], 14, 14) == 1) // Plane pre CSC gamma
                        {
                            Console.WriteLine("Plane pre CSC gamma\t : Enabled");
                            ReadPlanePreCSCGammaData(i, j);
                        }
                        else
                            Console.WriteLine("Plane pre CSC gamma\t : Disabled");

                        if (GetValue(uPlane_Color_Ctrl[i, j], 28, 28) == 0) // YUV Range Correction
                        {
                            Console.WriteLine("YUV Range correction\t : Enabled");
                        }
                        else
                            Console.WriteLine("YUV Range correction\t : Disabled");

                        switch (GetValue(uPlane_Color_Ctrl[i, j], 17, 19)) // Plane CSC
                        {
                            case 0: Console.WriteLine("Plane CSC mode\t\t : Bypass"); break;
                            case 1: Console.WriteLine("Plane CSC mode\t\t : YUV601 -> RGB709"); break;
                            case 2: Console.WriteLine("Plane CSC mode\t\t : YUV709 -> RGB709"); break;
                            case 3: Console.WriteLine("Plane CSC mode\t\t : YUV2020 -> RGB2020"); break;
                            case 4: Console.WriteLine("Plane CSC mode\t\t : RGB709 -> RGB2020"); break;
                        }

                        if (GetValue(uPlane_Color_Ctrl[i, j], 13, 13) == 0) // Plane gamma
                        {
                            Console.WriteLine("Plane gamma\t\t : Enabled");
                            ReadPlanePostCSCGammaData(i, j);
                        }
                        else
                            Console.WriteLine("Plane gamma\t\t : Disabled");

                        if (GetValue(uPlane_Color_Ctrl[i, j], 30, 30) == 1)
                        {// Pipe gamma
                            Console.WriteLine("Pipe gamma\t\t : Enabled");
                            ReadPallettePrecisionData(i);
                            ReadGcMaxRegisters(i);
                        }
                        else
                        {
                            Console.WriteLine("Pipe gamma\t\t : Disabled");
                            ReadPipePreCSCGammaData(i);
                        }

                        if (GetValue(uPlane_Color_Ctrl[i, j], 23, 23) == 1) // Pipe CSC
                        {
                            Console.WriteLine("Pipe CSC\t\t : Enabled");
                            GetCSCCoeff(i);
                        }
                        else
                            Console.WriteLine("Pipe CSC\t\t : Disabled");

                    }
                }

            }


        } // VerifyResult_ends  

        public static void VerifyResultColor()
        {
            for (uint i = 0; i < 4; i++) // Pipe set - A/B/C/D
            {
                Console.WriteLine("\n***********Pipe " + (i + 1) + "************\n");
                if (GetValue(uTrans_Conf[i], 31, 31) == 1)
                    Console.WriteLine("Pipe " + (i + 1) + "\t\t\t : Enabled");
                else if (GetValue(uTrans_Conf[4], 31, 31) == 1)
                    Console.WriteLine(" Pipe EDP \t\t\t : Enabled");
                else
                    Console.WriteLine("Pipe " + (i + 1) + "\t\t\t : Disabled");

                for (uint j = 0; j < 4; j++) // Plane -> 1-4
                {
                    if (GetValue(uPlane_Ctrl[i, j], 31, 31) == 1) // Plane enable check
                    {
                        Console.WriteLine("Plane " + (j + 1) + " \t\t : Enabled");

                        Console.WriteLine("Plane source pixel format : " + GetPlaneFormat(GetValue(uPlane_Ctrl[i, j], 24, 27)));


                        if (GetValue(uPlane_Ctrl[i, j], 13, 13) == 0) // Plane gamma
                            Console.WriteLine("Plane gamma\t\t : Enabled");
                        else
                            Console.WriteLine("Plane gamma\t\t : Disabled");

                        if (GetValue(uPlane_Ctrl[i, j], 30, 30) == 1) // Pipe gamma
                            Console.WriteLine("Pipe gamma\t\t : Enabled");
                        else
                            Console.WriteLine("Pipe gamma\t\t : Disabled");

                        if (GetValue(uPlane_Ctrl[i, j], 23, 23) == 1) // Pipe CSC
                        {
                            Console.WriteLine("Pipe CSC\t\t : Enabled");
                            GetCSCCoeff(i);
                        }
                        else
                            Console.WriteLine("Pipe CSC\t\t : Disabled");

                    }
                }

            }
        }

        public static SourcePixelFormat GetPlaneFormat(uint value)
        {

            switch (value)
            {
                case 0: return SourcePixelFormat.YUV_16_bit422; break;
                case 1: return SourcePixelFormat.NV12_YUV_420; break;
                case 2: return SourcePixelFormat.RGB_32_2101010; break;
                case 3: return SourcePixelFormat.P010_YUV_420_10bit; break;
                case 4: return SourcePixelFormat.RGB_32_bit_8888; break;
                case 5: return SourcePixelFormat.P012_YUV_420_12bit; break;
                case 6: return SourcePixelFormat.RGB_64bit_16161616_float; break;
                case 7: return SourcePixelFormat.P016_YUV_420_16_bit; break;
                case 8: return SourcePixelFormat.YUV_32_bit_444; break;
                case 9: return SourcePixelFormat.RGB_64bit_16161616_UINT; break;
                case 10: return SourcePixelFormat.RGB_32_bit_XR_BIAS101010; break;
                case 12: return SourcePixelFormat.Indexed_8bit; break;
                default: return SourcePixelFormat.Invalid_format; break;
            };

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

            string path = System.IO.Path.Combine(@"c:\Intel\BT2020\CSCCoeff_" + i + ".txt");
            System.IO.StreamWriter file = new System.IO.StreamWriter(path);

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
                    file.WriteLine("CSC offset[" + x + "][" + y + "] -->  From H/W reg :" + outVal);
                }
            }

            file.WriteLine("CSC PostOffset Coefficients -->  From H/W reg : {" + uCSCPostOffset[0] + "," + uCSCPostOffset[1] + "," + uCSCPostOffset[2] + "}");

            file.Close();
        }




        public static void ReadPallettePrecisionData(uint pipeIndex)
        {

            uint ulValue = 0;
            uint uGammaValue_even = 0;
            uint uGammaValue_odd = 0;
            uint uGammaIndex = 0;
            uint rValue, gValue, bValue = 0;

            string path = System.IO.Path.Combine(@"c:\Intel\BT2020\PipeGamma_" + pipeIndex + ".txt");
            System.IO.StreamWriter file = new System.IO.StreamWriter(path);

            // auto increment Bit 15
            reg.ReadRegister(PalPrecIndex[pipeIndex], ref ulValue);
            ulValue = ulValue | 0x00008000;
            reg.WriteRegister(PalPrecIndex[pipeIndex], ulValue);
            Console.WriteLine(" Register write :" + PalPrecIndex[pipeIndex] + "   Data :" + ulValue);

            //16bit value
            //Lower 6 bits in even idexes (Bit 4:9)
            //Upper 10 bits in odd indexes
            for (int startIndex = 0; startIndex < 512; startIndex++)
            {
                reg.ReadRegister(PalPrecIndex[pipeIndex], ref uGammaIndex);
                reg.ReadRegister(PalPrecData[pipeIndex], ref uGammaValue_even);
                reg.ReadRegister(PalPrecData[pipeIndex], ref uGammaValue_odd);

                rValue = ((GetValue(uGammaValue_odd, 20, 29) & ((uint)0x3FF)) << 6) + GetValue(uGammaValue_even, 24, 29);
                gValue = ((GetValue(uGammaValue_odd, 10, 19) & ((uint)0x3FF)) << 6) + GetValue(uGammaValue_even, 14, 19);
                bValue = ((GetValue(uGammaValue_odd, 0, 9) & ((uint)0x3FF)) << 6) + GetValue(uGammaValue_even, 4, 9);

                file.WriteLine("Index :" + startIndex + " R :" + rValue + "G :" + gValue + "B :" + bValue);
            }

            file.Close();

        }


        public static void ReadGcMaxRegisters(uint pipeIndex)
        {
            string path = System.IO.Path.Combine(@"c:\Intel\BT2020\PipeGamma_" + pipeIndex + ".txt");
            FileStream fsAppend = new FileStream(path, FileMode.Append);
            StreamWriter swAppend = new StreamWriter(fsAppend);
            uint ulValue = 0;
            // GC_Max 0.16 format

            swAppend.WriteLine(" GC_MAX registers");
            reg.ReadRegister(PalGCMax[pipeIndex], ref ulValue);
            swAppend.WriteLine("R :" + GetValue(ulValue, 0, 16));
            reg.ReadRegister(PalGCMax[pipeIndex] + 4, ref ulValue);
            swAppend.WriteLine("G :" + GetValue(ulValue, 0, 16));
            reg.ReadRegister(PalGCMax[pipeIndex] + 8, ref ulValue);
            swAppend.WriteLine("B :" + GetValue(ulValue, 0, 16));


            // EXT_GC_MAX 3.16 format
            swAppend.WriteLine(" EXT_GC_MAX registers");

            reg.ReadRegister(PalExtGCMax[pipeIndex], ref ulValue);
            swAppend.WriteLine("R :" + GetValue(ulValue, 0, 18));
            reg.ReadRegister(PalExtGCMax[pipeIndex] + 4, ref ulValue);
            swAppend.WriteLine("R :" + GetValue(ulValue, 0, 18));
            reg.ReadRegister(PalExtGCMax[pipeIndex] + 8, ref ulValue);
            swAppend.WriteLine("R :" + GetValue(ulValue, 0, 18));

            // EXT2_GC_MAX 3.16 format
            swAppend.WriteLine(" EXT2_GC_MAX registers");

            reg.ReadRegister(PalExt2GCMax[pipeIndex], ref ulValue);
            swAppend.WriteLine("R :" + GetValue(ulValue, 0, 18));
            reg.ReadRegister(PalExt2GCMax[pipeIndex] + 4, ref ulValue);
            swAppend.WriteLine("R :" + GetValue(ulValue, 0, 18));
            reg.ReadRegister(PalExt2GCMax[pipeIndex] + 8, ref ulValue);
            swAppend.WriteLine("R :" + GetValue(ulValue, 0, 18));

            swAppend.Close();
            fsAppend.Close();

        }

        public static void ReadPipePreCSCGammaData(uint pipeIndex)
        {
            uint ulValue = 0;
            uint uGammaValue = 0;
            uint uGammaIndex = 0;


            string path = System.IO.Path.Combine(@"c:\Intel\BT2020\PipePreCSCGamma_" + pipeIndex + ".txt");
            System.IO.StreamWriter file = new System.IO.StreamWriter(path);

            // auto increment Bit 10
            reg.ReadRegister(PalPrecIndex[pipeIndex], ref ulValue);
            ulValue = ulValue | 0x00000400;
            reg.WriteRegister(PalPrecIndex[pipeIndex], ulValue);

            for (int startIndex = 0; startIndex < 34; startIndex++)
            {
                reg.ReadRegister(PipePreCSCGammaIndex[pipeIndex], ref uGammaIndex);
                reg.ReadRegister(PipePreCSCGammaData[pipeIndex], ref uGammaValue);

                file.WriteLine("Index :" + startIndex + " Value : " + GetValue(uGammaValue, 0, 18));
            }
            file.Close();
        }


        public static void ReadPlanePreCSCGammaData(uint pipeIndex, uint planeIndex)
        {
            uint ulValue = 0;
            uint uGammaValue = 0;
            uint uGammaIndex = 0;


            string path = System.IO.Path.Combine(@"c:\Intel\BT2020\PlanePreCSCGamma_" + pipeIndex + ".txt");
            System.IO.StreamWriter file = new System.IO.StreamWriter(path);

            // auto increment Bit 10
            reg.ReadRegister(PlanePreCSCGammaIndex[pipeIndex, planeIndex], ref ulValue);
            ulValue = ulValue | 0x00000400;
            reg.WriteRegister(PlanePreCSCGammaIndex[pipeIndex, planeIndex], ulValue);

            for (int startIndex = 0; startIndex < 34; startIndex++)
            {
                reg.ReadRegister(PlanePreCSCGammaIndex[pipeIndex, planeIndex], ref uGammaIndex);
                reg.ReadRegister(PlanePreCSCGammaIndex[pipeIndex, planeIndex] + 4, ref uGammaValue);

                file.WriteLine("Index :" + startIndex + " Value : " + GetValue(uGammaValue, 0, 18));
            }
            file.Close();
        }

        public static void ReadPlanePostCSCGammaData(uint pipeIndex, uint planeIndex)
        {
            uint ulValue = 0;
            uint uGammaValue = 0;
            uint uGammaIndex = 0;


            string path = System.IO.Path.Combine(@"c:\Intel\BT2020\PlanePostCSCGamma_" + pipeIndex + ".txt");
            System.IO.StreamWriter file = new System.IO.StreamWriter(path);

            // auto increment Bit 10
            reg.ReadRegister(PlanePostCSCGammaIndex[pipeIndex, planeIndex], ref ulValue);
            ulValue = ulValue | 0x00000400;
            reg.WriteRegister(PlanePostCSCGammaIndex[pipeIndex, planeIndex], ulValue);

            for (int startIndex = 0; startIndex < 34; startIndex++)
            {
                reg.ReadRegister(PlanePostCSCGammaIndex[pipeIndex, planeIndex], ref uGammaIndex);
                reg.ReadRegister(PlanePostCSCGammaIndex[pipeIndex, planeIndex] + 4, ref uGammaValue);

                file.WriteLine("Index :" + startIndex + " Value : " + GetValue(uGammaValue, 0, 18));
            }
            file.Close();
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

            scale_factor = Math.Pow(2, positionOfPointFromRight);

            outVal = (double)mantissa / scale_factor;

            if (sign == 1)
                outVal = outVal * -1;

            return outVal;
        }

        public static uint Convert_CSC_Coeff_to_RegFormat(double coeff)
        {
            uint outVal = 0;

            uint sign = 0, exponent = 0, shift_factor = 0;
            int mantissa;

            if (coeff < 0)
                sign = 1;

            // range check
            if (coeff > 3.99)
                coeff = 3.9921875; // 11.1111111b -> 511/128 
            if (coeff < -4.00)
                coeff = -3.9921875;

            coeff = Math.Abs(coeff);

            if (coeff < 0.125)    //0.000bbbbbbbbb 
            {
                exponent = 3;
                shift_factor = 12;
            }
            else if (coeff < 0.25) //0.00bbbbbbbbb
            {
                exponent = 2;
                shift_factor = 11;
            }
            else if (coeff < 0.5)  //0.0bbbbbbbbb
            {
                exponent = 1;
                shift_factor = 10;
            }
            else if (coeff < 1.0)   // 0.bbbbbbbbb
            {
                exponent = 0;
                shift_factor = 9;
            }
            else if (coeff < 2.0)    //b.bbbbbbbb
            {
                exponent = 7;
                shift_factor = 8;
            }
            else if (coeff >= 2.0)
            {
                exponent = 6;
                shift_factor = 7;
            }


            mantissa = (int)Math.Round(coeff * (1 << (int)shift_factor));

            outVal = sign << 15;
            outVal = outVal | (exponent << 12);
            outVal = outVal | (uint)(mantissa << 3);

            return outVal;
        }

        //public static void GetExpectedCSCCoeffValue(uint id)
        //{

        //    double[,] CSCMatrix = new double[3, 3];

        //    double mul_factorY = 0.0, mul_factorUV = 0.0;

        //    uint CSCPostOffY = 0;

        //    if (uBPC[id] == 8)
        //    { mul_factorY = 219.0 / 255.0; mul_factorUV = 224.0 / 255.0; CSCPostOffY = 16; }
        //    else if (uBPC[id] == 10)
        //    { mul_factorY = 876.0 / 1023.0; mul_factorUV = 896.0 / 1023.0; CSCPostOffY = 64; }
        //    else if (uBPC[id] == 12)
        //    { mul_factorY = 2904.0 / 4095.0; mul_factorUV = 3584.0 / 4096.0; CSCPostOffY = 256; }

        //    //Console.WriteLine("Expected CSC Coeff");
        //    for (int i = 0; i < 3; i++)
        //    {
        //        for (int j = 0; j < 3; j++)
        //        {
        //            if (i == 0)
        //                CSCMatrix[i, j] = uBT2020RGBtoYUVCoeff[i, j] * mul_factorY;
        //            else
        //                CSCMatrix[i, j] = uBT2020RGBtoYUVCoeff[i, j] * mul_factorUV;

        //            Convert_CSC_Coeff_to_RegFormat(CSCMatrix[i, j]);

        //            //Console.WriteLine(CSCMatrix[i,j]);
        //        }
        //    }

        //}

    } // class_end

} // namespace_end


