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


namespace LUT_3DVerification
{

    class Program
    {
        [DllImport("Utilities.dll")]
        private static extern UInt32 writeMMIOReg(UInt32 dwOffset, UInt32 dwValue);

        public static RegisterModule reg = new RegisterModule();

        public static uint uTrans_Conf = 0;
        public static uint uTrans_Ddi_Func = 0;
        public static uint uLUT_3D_Ctrl = 0;
        public static uint uLUT_3D_Index = 0;
        public static uint uLUT_3D_Data = 0;

        public static uint uDsiPLL = 0;
        public static uint[] uMIPICtrl = { 0, 0 };
        public static uint[] uMIPIPort = { 0, 0 };
        public static bool pipeA = false;



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

            reg.ReadRegister((uint)0x7F008, ref uTrans_Conf);
            reg.ReadRegister((uint)0x6F400, ref uTrans_Ddi_Func);

            reg.ReadRegister((uint)0x490A4, ref uLUT_3D_Ctrl);  // Pipe Bottom color 
            reg.ReadRegister((uint)0x490A8, ref uLUT_3D_Index);
            reg.ReadRegister((uint)0x490AC, ref uLUT_3D_Data);


            reg.ReadRegister((uint)0x46080, ref uDsiPLL);
            reg.ReadRegister((uint)0x6B104, ref uMIPICtrl[0]);
            reg.ReadRegister((uint)0x6B904, ref uMIPICtrl[1]);
            reg.ReadRegister((uint)0x6B0C0, ref uMIPIPort[0]);
            reg.ReadRegister((uint)0x6B8C0, ref uMIPIPort[1]);

        } // InitializeRegisters_ends

        public static void PrintResult()
        {

            if (GetValue(uTrans_Conf, 31, 31) == 1)
            {
                if (GetValue(uTrans_Ddi_Func, 12, 14) == 0)
                {
                    Console.WriteLine("  Pipe A EDP  :Enabled ");
                    pipeA = true;
                }
                else
                    Console.WriteLine("  EDP  :Enabled  on non Pipe A");

            }
            else if (GetValue(uDsiPLL, 31, 31) == 1)
            {
                if (GetValue(uMIPIPort[0], 31, 31) == 1)
                {
                    if (GetValue(uMIPICtrl[0], 7, 9) == 0)
                    {
                        Console.WriteLine("Pipe A MIPI_A : Enabled");
                        pipeA = true;
                    }
                    else
                        Console.WriteLine("  MIPI A :Enabled  on non Pipe A");
                }
                else if (GetValue(uMIPIPort[1], 31, 31) == 1)
                {
                    if (GetValue(uMIPICtrl[1], 7, 9) == 0)
                    {
                        Console.WriteLine("Pipe A MIPI_C : Enabled");
                        pipeA = true;
                    }
                    else
                        Console.WriteLine("  MIPI C :Enabled  on non Pipe A");

                }

            }
            else
            {
                Console.WriteLine("Internal displays (eDp/MIPI ) not Active");

            }

            if (pipeA == true)
            {
                if (GetValue(uLUT_3D_Ctrl, 31, 31) == 1)
                {

                    Console.WriteLine("HW 3D LUT is enabled on Pipe A");
                    Dump3DLUT();

                    if (GetValue(uLUT_3D_Ctrl, 30, 30) == 0)
                        Console.WriteLine("HW finshed loading the LUT buffer in to internal working RAM");
                    else
                        Console.WriteLine("HW didn't load the LUT buffer in to internal working RAM yet");
                }
                else
                    Console.WriteLine("HW 3D LUT is Disabled on Pipe A");
            }

        } // PrintResult_ends  

        public static void Dump3DLUT()
        {
            FileStream fs = new FileStream("3DLUT.txt", FileMode.OpenOrCreate, FileAccess.Write);
            StreamWriter writer = new StreamWriter(fs);
            uint u3DLUTData = 0;

            for (int startIndex = 0; startIndex < 4913; startIndex++)
            {

                reg.ReadRegister(uLUT_3D_Data, ref u3DLUTData);

                writer.WriteLine("Index :" + startIndex + " Data : 0x" + uLUT_3D_Data.ToString("X"));

            }
            writer.Close();

        }

        public static uint GetValue(uint value, int start, int end)
        {
            uint retvalue = value << (31 - end);
            retvalue >>= (31 - end + start);
            return retvalue;
        }






    } // class_end

} // namespace_end


