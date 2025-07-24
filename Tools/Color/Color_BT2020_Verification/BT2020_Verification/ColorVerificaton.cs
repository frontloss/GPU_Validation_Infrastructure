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


namespace ColorVerification
{

    class Program
    {
        [DllImport("Utilities.dll")]
        private static extern UInt32 writeMMIOReg(UInt32 dwOffset, UInt32 dwValue);

        public static RegisterModule reg = new RegisterModule();

        public static uint[] uTrans_Conf = { 0, 0, 0, 0, 0 }; // trans A,trans B,trans C,trans D,trans EDP 
        public static uint[] uTrans_DDIFunc_Ctrl = { 0, 0, 0, 0 }; // Trans DDI Ctrl A - D
        public static uint[] uPipeBottomColor = { 0, 0, 0, 0 };
        public static uint[] uGammaMode = { 0, 0, 0, 0 };
        public static uint[] uPipeMisc = { 0, 0, 0, 0 };
        public static uint[] uCurCtl = { 0, 0, 0, 0 };
        public static uint[] uCgeCtl = { 0, 0, 0, 0 };
        public static uint[] uCgeLUT = { 0, 0, 0, 0 };

        public static uint uDsiPLL = 0;
        public static uint[] uMIPICtrl = { 0, 0 };
        public static uint[] uMIPIPort = { 0, 0 };
        public static uint[,] uPlane_Ctrl = { { 0, 0, 0, 0 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } }; // Plane Ctrl for 1-4 wro Pipe A-D
        public static uint[,] uPlane_Color_Ctrl = { { 0, 0, 0, 0 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } }; // Color ctrl for plane 1-4 wrto Pipe A-D

        public static string WGStatus = null;
        public static bool edp = false;

        public static uint[,] uCSCCoeff = { { 0, 0, 0 }, { 0, 0, 0 }, { 0, 0, 0 } };
        public static uint[] PalPrecIndex = { 0x4A400, 0x4AC00, 0x4B400, 0x4BC00 };
        public static uint[] PalPrecData = { 0x4A404, 0x4AC04, 0x4B404, 0x4BC04 };



        static void Main(string[] args)
        {
            if (args.Length == 1)
            {
                Console.WriteLine(" Delay of " + args[0] + " second is added to the script");

                CmnDelay.Seconds(Int32.Parse(args[0]));
            }

            InitializeRegister();


            Console.WriteLine("\n ****************** OUTPUT *******************\n ");
            PrintResult();


            Console.ReadLine();
        } // Main_ends

        public static void InitializeRegister()
        {
            reg.ReadRegister((uint)0x70008, ref uTrans_Conf[0]);  // Pipe /Transcoder 
            reg.ReadRegister((uint)0x71008, ref uTrans_Conf[1]);
            reg.ReadRegister((uint)0x72008, ref uTrans_Conf[2]);
            reg.ReadRegister((uint)0x73008, ref uTrans_Conf[3]);
            reg.ReadRegister((uint)0x7F008, ref uTrans_Conf[4]);

            reg.ReadRegister((uint)0x70034, ref uPipeBottomColor[0]);  // Pipe Bottom color 
            reg.ReadRegister((uint)0x71034, ref uPipeBottomColor[1]);
            reg.ReadRegister((uint)0x72034, ref uPipeBottomColor[2]);
            reg.ReadRegister((uint)0x73034, ref uPipeBottomColor[3]);

            reg.ReadRegister((uint)0x70030, ref uPipeMisc[0]);  // Pipe Misc 
            reg.ReadRegister((uint)0x71030, ref uPipeMisc[1]);
            reg.ReadRegister((uint)0x72030, ref uPipeMisc[2]);
            reg.ReadRegister((uint)0x73030, ref uPipeMisc[3]);

            reg.ReadRegister((uint)0x60400, ref uTrans_DDIFunc_Ctrl[0]); // Trans DDI A-D
            reg.ReadRegister((uint)0x61400, ref uTrans_DDIFunc_Ctrl[1]);
            reg.ReadRegister((uint)0x62400, ref uTrans_DDIFunc_Ctrl[2]);
            reg.ReadRegister((uint)0x63400, ref uTrans_DDIFunc_Ctrl[3]);

            reg.ReadRegister((uint)0x70080, ref uCurCtl[0]);  // CUrsor ctrl
            reg.ReadRegister((uint)0x71080, ref uCurCtl[1]);
            reg.ReadRegister((uint)0x72080, ref uCurCtl[2]);
            reg.ReadRegister((uint)0x73080, ref uCurCtl[3]);

            reg.ReadRegister((uint)0x49080, ref uCgeCtl[0]);  // CGE ctrl
            reg.ReadRegister((uint)0x49180, ref uCgeCtl[1]);
            reg.ReadRegister((uint)0x49280, ref uCgeCtl[2]);
            reg.ReadRegister((uint)0x49380, ref uCgeCtl[3]);

            reg.ReadRegister((uint)0x49080, ref uCgeLUT[0]);  // CGE LUT
            reg.ReadRegister((uint)0x49180, ref uCgeLUT[1]);
            reg.ReadRegister((uint)0x49280, ref uCgeLUT[2]);
            reg.ReadRegister((uint)0x49380, ref uCgeLUT[3]);

            reg.ReadRegister((uint)0x4A480, ref uGammaMode[0]);  // Pipe Misc 
            reg.ReadRegister((uint)0x4AC80, ref uGammaMode[1]);
            reg.ReadRegister((uint)0x4B480, ref uGammaMode[2]);
            reg.ReadRegister((uint)0x4BC80, ref uGammaMode[3]);

            reg.ReadRegister((uint)0x70180, ref uPlane_Ctrl[0, 0]); // Plane Ctl  Pipe A
            reg.ReadRegister((uint)0x70280, ref uPlane_Ctrl[0, 1]);
            reg.ReadRegister((uint)0x701CC, ref uPlane_Color_Ctrl[0, 0]); // Plane Color Ctl Pipe A
            reg.ReadRegister((uint)0x702CC, ref uPlane_Color_Ctrl[0, 1]);


            reg.ReadRegister((uint)0x71180, ref uPlane_Ctrl[1, 0]); // Plane  Pipe B
            reg.ReadRegister((uint)0x71280, ref uPlane_Ctrl[1, 1]);
            reg.ReadRegister((uint)0x711CC, ref uPlane_Color_Ctrl[1, 0]); // Plane Color Pipe B
            reg.ReadRegister((uint)0x712CC, ref uPlane_Color_Ctrl[1, 1]);

            reg.ReadRegister((uint)0x72180, ref uPlane_Ctrl[2, 0]); // Plane Pipe C
            reg.ReadRegister((uint)0x72280, ref uPlane_Ctrl[2, 1]);
            reg.ReadRegister((uint)0x721CC, ref uPlane_Color_Ctrl[2, 0]); // Plane Color Pipe C
            reg.ReadRegister((uint)0x722CC, ref uPlane_Color_Ctrl[2, 1]);

            reg.ReadRegister((uint)0x73180, ref uPlane_Ctrl[3, 0]); // Plane 1-4 Pipe D
            reg.ReadRegister((uint)0x73280, ref uPlane_Ctrl[3, 1]);
            reg.ReadRegister((uint)0x731CC, ref uPlane_Color_Ctrl[3, 0]); // Plane Color Pipe D
            reg.ReadRegister((uint)0x732CC, ref uPlane_Color_Ctrl[3, 1]);

            reg.ReadRegister((uint)0x46080, ref uDsiPLL);
            reg.ReadRegister((uint)0x6B104, ref uMIPICtrl[0]);
            reg.ReadRegister((uint)0x6B904, ref uMIPICtrl[1]);
            reg.ReadRegister((uint)0x6B0C0, ref uMIPIPort[0]);
            reg.ReadRegister((uint)0x6B8C0, ref uMIPIPort[1]);

        } // InitializeRegisters_ends

        public static void PrintResult()
        {


            for (uint i = 0; i < 3; i++) // Pipe set - A/B/C/D
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

                for (uint j = 0; j < 2; j++) 
                {
                    if (GetValue(uPlane_Ctrl[i, j], 31, 31) == 1) // Plane enable check
                    {
                        if (j == 0)
                            Console.WriteLine("----------Plane  A : Enabled---------------");
                        else
                            Console.WriteLine("-------------Sprite Plane: Enabled---------------");

                        if (GetValue(uPlane_Color_Ctrl[i, j], 30, 30) == 1)
                            Console.WriteLine("Pipe gamma\t\t : Enabled");
                        else
                            Console.WriteLine("Pipe gamma\t\t : Disabled");

                        if (GetValue(uPlane_Color_Ctrl[i, j], 23, 23) == 1) // Pipe CSC
                        {
                            Console.WriteLine("Plane is using Pipe CSC\t\t ");
                            if (GetValue(uCgeCtl[i], 31, 31) != 1)
                                WGStatus = "WG slider is at Natural";
                        }
                        else
                        {
                            Console.WriteLine("Plane is not using Pipe CSC");
                            WGStatus = "WG slider is at Vivid";
                        }

                        if (GetValue(uPlane_Color_Ctrl[i, j], 17, 19) == 1 || GetValue(uPlane_Color_Ctrl[i, j], 17, 19) == 2 || GetValue(uPlane_Color_Ctrl[i, j], 17, 19) == 3) // Pipe CSC
                            Console.WriteLine("Plane is using YUV->RGB color conversion logic\t\t ");
                        else
                            Console.WriteLine("Plane is not using YUV->RGB color conversion logic");


                    }
                } // Plane loop ends

                // Pipe o/p color space

                if (GetValue(uPipeMisc[i], 11, 11) == 1)
                    Console.WriteLine("Pipe output color space is YUV");
                else
                    Console.WriteLine("Pipe output color space is RGB");
                //Bottom CSC

                if (GetValue(uPipeBottomColor[i], 30, 30) == 1) // Pipe CSC
                    Console.WriteLine("Pipe Bottom CSC\t\t : Enabled");
                else
                    Console.WriteLine("Pipe Bottom CSC\t\t : Disabled");

                // Cursor and Cursor CSC status
                if (GetValue(uCurCtl[i], 0, 5) != 0)
                {
                    if (GetValue(uCurCtl[i], 24, 24) == 1)
                        Console.WriteLine("Cursor is Enabled and using Cursor CSC");
                    else
                        Console.WriteLine("Cursor is Enabled and  not using Cursor CSC");
                }

                else
                    Console.WriteLine("Cursor: Disabled");

                // BPC

                switch (GetValue(uTrans_DDIFunc_Ctrl[i], 20, 22))
                {
                    case 0: Console.WriteLine(" Color Format/BPC : 8 "); break;
                    case 1: Console.WriteLine(" Color Format/BPC: 10 \n Deep Color Enabled"); break;
                    case 2: Console.WriteLine(" Color Format/BPC : 6 "); break;
                    case 3: Console.WriteLine(" Color Format/BPC : 12 \n Deep Color Enabled"); break;
                }

                //Gamma mode

                switch (GetValue(uGammaMode[i],0,1))
                {
                    case 0: Console.WriteLine(" Gamma Mode : 8 bit "); break;
                    case 1: Console.WriteLine(" Gamma Mode : 10 bit"); break;
                    case 2: Console.WriteLine(" Gamma MOde : 12 bit "); break;
                    
                }


                // Dithering

                if (GetValue(uPipeMisc[i], 4, 4) == 1)
                {
                    Console.WriteLine("Dithering : Enabled");
                    switch (GetValue(uPipeMisc[i], 2, 3))
                    {
                        case 0: Console.WriteLine(" Dithering Type : Spatial"); break;
                        case 1: Console.WriteLine(" Dithering Type : Spatio - Temporal 1 "); break;
                        case 2: Console.WriteLine(" Dithering Type : Spatio - Temporal 2 "); break;
                        case 3: Console.WriteLine(" Dithering Type : Temporal"); break;
                    }
                }
                else
                    Console.WriteLine("DIthering : Disabled");

                // Widegamut Status
                Console.WriteLine(" WG - Status");

                if (GetValue(uCgeCtl[i], 31, 31) == 1)
                {
                    uint regValLUT_0 = GetValue(uCgeLUT[i], 0, 31);
                    uint regValLUT_1 = GetValue(uCgeLUT[i], 0, 31);
                    uint regValLUT_2 = GetValue(uCgeLUT[i], 0, 31);
                    uint regValLUT_3 = GetValue(uCgeLUT[i], 0, 31);
                    uint regValLUT_4 = GetValue(uCgeLUT[i], 0, 31);

                    if ((10 == GetValue(regValLUT_0, 0, 5)) && (10 == GetValue(regValLUT_0, 8, 13)) && (10 == GetValue(regValLUT_0, 16, 21)) && (10 == GetValue(regValLUT_0, 24, 29)) && (10 == GetValue(regValLUT_1, 0, 5)) && (10 == GetValue(regValLUT_1, 8, 13)) && (14 == GetValue(regValLUT_1, 16, 21)) && (19 == GetValue(regValLUT_1, 24, 29)) && (24 == GetValue(regValLUT_2, 0, 5)) && (29 == GetValue(regValLUT_2, 8, 13)) && (32 == GetValue(regValLUT_2, 16, 21)) && (32 == GetValue(regValLUT_2, 24, 29)) && (32 == GetValue(regValLUT_3, 0, 5)) && (32 == GetValue(regValLUT_3, 8, 13)) && (32 == GetValue(regValLUT_3, 16, 21)) && (32 == GetValue(regValLUT_3, 24, 29)) && (32 == GetValue(regValLUT_4, 0, 5)))
                        WGStatus = "WG Slider at LEVEL 4 \n";
                    else if ((0 == GetValue(regValLUT_0, 0, 5)) && (0 == GetValue(regValLUT_0, 8, 13)) && (0 == GetValue(regValLUT_0, 16, 21)) && (0 == GetValue(regValLUT_0, 24, 29)) && (0 == GetValue(regValLUT_1, 0, 5)) && (0 == GetValue(regValLUT_1, 8, 13)) && (6 == GetValue(regValLUT_1, 16, 21)) && (13 == GetValue(regValLUT_1, 24, 29)) && (19 == GetValue(regValLUT_2, 0, 5)) && (26 == GetValue(regValLUT_2, 8, 13)) && (32 == GetValue(regValLUT_2, 16, 21)) && (32 == GetValue(regValLUT_2, 24, 29)) && (32 == GetValue(regValLUT_3, 0, 5)) && (32 == GetValue(regValLUT_3, 8, 13)) && (32 == GetValue(regValLUT_3, 16, 21)) && (32 == GetValue(regValLUT_3, 24, 29)) && (32 == GetValue(regValLUT_4, 0, 5)))
                        WGStatus = "WG Slider at LEVEL 3 \n";
                    else if ((0 == GetValue(regValLUT_0, 0, 5)) && (0 == GetValue(regValLUT_0, 8, 13)) && (0 == GetValue(regValLUT_0, 16, 21)) && (0 == GetValue(regValLUT_0, 24, 29)) && (0 == GetValue(regValLUT_1, 0, 5)) && (0 == GetValue(regValLUT_1, 8, 13)) && (3 == GetValue(regValLUT_1, 16, 21)) && (6 == GetValue(regValLUT_1, 24, 29)) && (10 == GetValue(regValLUT_2, 0, 5)) && (13 == GetValue(regValLUT_2, 8, 13)) && (16 == GetValue(regValLUT_2, 16, 21)) && (19 == GetValue(regValLUT_2, 24, 29)) && (22 == GetValue(regValLUT_3, 0, 5)) && (26 == GetValue(regValLUT_3, 8, 13)) && (29 == GetValue(regValLUT_3, 16, 21)) && (32 == GetValue(regValLUT_3, 24, 29)) && (32 == GetValue(regValLUT_4, 0, 5)))
                        WGStatus = "WG Slider at LEVEL 2 \n";
                }

                Console.WriteLine(WGStatus);



            } // Pipe loop ends


        } // PrintResult_ends  



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
            double outVal;

            string path = System.IO.Path.Combine(@"c:\Intel\BT2020\CSCCoeff_" + i + ".txt");
            System.IO.StreamWriter file = new System.IO.StreamWriter(path);


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





            for (uint x = 0; x < 3; x++)
            {
                for (uint y = 0; y < 3; y++)
                {
                    outVal = Convert_CSC_RegFormat_to_Coeff(uCSCCoeff[x, y]);
                    file.WriteLine("CSC offset[" + x + "][" + y + "] -->  From H/W reg :" + outVal);
                }
            }

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




    } // class_end

} // namespace_end


