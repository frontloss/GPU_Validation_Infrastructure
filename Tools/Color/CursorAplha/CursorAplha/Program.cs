using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

//Extra added DLL
using IgfxExtBridge_DotNet;
using Intel.Display.Automation.Common;
using Intel.Display.Automation.TestsCommon;

namespace CursorAplha
{
    class Program
    {

        public static RegisterModule reg = new RegisterModule();
        public static uint[] uCURSOR =  { 0, 0, 0 };
        public static string[] uCAB_Status = { "Disable", "Disable", "Disable" };
        public static string[] uCURSOR_Value = { "Disable", "Disable", "Disable" };
        static void Main(string[] args)
        {
            if (args.Length == 1)
            {
                Console.WriteLine(" Delay of 15 second is added to the script");
                CmnDelay.Seconds(15);
            }
            InitializeRegister();
            Console.WriteLine("Cursor Alpha Blending (CAB) \n \n \t \t");

            if (uCURSOR_Value[0] == "Enable")
            {
                Console.WriteLine("CAB on Pipe 1 : " + uCAB_Status[0]);

            }

                if (uCURSOR_Value[1] == "Enable")
                {
                    Console.WriteLine("CAB on Pipe 2 : " + uCAB_Status[1]);
                    
                }

                if (uCURSOR_Value[2] == "Enable")
                {
                    Console.WriteLine("CAB on Pipe 3 : " + uCAB_Status[2]);
                    
                }

            Console.ReadLine();
        }



        public static void InitializeRegister()
        {
            reg.ReadRegister((uint)0x70080, ref uCURSOR[0]);  //Pipe1 Cursor
            reg.ReadRegister((uint)0x71080, ref uCURSOR[1]);  //Pipe2 Cursor
            reg.ReadRegister((uint)0x72080, ref uCURSOR[2]);  //Pipe3 Cursor


            //Get the status about Cursor_Plane
            for (int i = 0; i < 3; i++)
            {
                Console.WriteLine("  Cursor Value for Pipe " + i + " : " + String.Format("0x{0:X}", uCURSOR[i]) + "\n");
               
                if ((uCURSOR[i] & 0x000003F) != 0)
                {
                    uCURSOR_Value[i] = "Enable";
                    
                    if ((uCURSOR[i] & 0x000003F) == 2)
                    {
                        Console.WriteLine(" The Cursor Format : 128x128 32bpp AND/INVERT");
                    }
                    else if ((uCURSOR[i] & 0x000003F) == 3)
                    {
                        Console.WriteLine(" The Cursor Format : 256x256 32bpp AND/INVERT");
                    }
                    else if ((uCURSOR[i] & 0x000003F) == 4)
                    {
                        Console.WriteLine(" The Cursor Format : 64x64 2bpp Indexed 3-color and transparency");
                    }
                    else if ((uCURSOR[i] & 0x000003F) == 5)
                    {
                        Console.WriteLine("  The Cursor Format : 64x64 2bpp Indexed AND/XOR 2-color");
                    }
                    else if ((uCURSOR[i] & 0x000003F) == 6)
                    {
                        Console.WriteLine(" The Cursor Format : 64x64 2bpp Indexed 4-color");
                    }
                    else if ((uCURSOR[i] & 0x000003F) == 7)
                    {
                        Console.WriteLine("  The Cursor Format : 64x64 32bpp AND/INVERT");
                    }
                    else if ((uCURSOR[i] & 0x000003F) == 34)
                    {
                        Console.WriteLine(" The Cursor Format : 128x128 32bpp ARGB (8:8:8:8 MSB-A:R:G:B)");
                    }
                    else if ((uCURSOR[i] & 0x000003F) == 35)
                    {
                        Console.WriteLine(" The Cursor Format : 256x256 32bpp ARGB (8:8:8:8 MSB-A:R:G:B)");
                    }
                    else if ((uCURSOR[i] & 0x000003F) ==36)
                    {
                        Console.WriteLine(" The Cursor Format : 64x64 32bpp AND/XOR");
                    }
                    else if ((uCURSOR[i] & 0x000003F) == 37)
                    {
                        Console.WriteLine(" The Cursor Format : 128x128 32bpp AND/XOR");
                    }
                    else if ((uCURSOR[i] & 0x000003F) == 38)
                    {
                        Console.WriteLine(" The Cursor Format : 256x256 32bpp AND/XOR");
                    }
                    else if ((uCURSOR[i] & 0x000003F) == 39)
                    {
                        Console.WriteLine(" The Cursor Format : 64x64 32bpp ARGB (8:8:8:8 MSB-A:R:G:B)");
                    }
                    else
                    {
                        Console.WriteLine("Incorrect Cursor Format");
                    }
                     
                }
            }

            Console.WriteLine("\n");
                //  Getting  the Status of the Cursor Alpha Blending
                for (int i = 0; i < 3; i++)
                {
                    if (uCURSOR_Value[i] == "Enable")
                    {
                        if ((uCURSOR[i] & 0x00000C00) >> 10 == 1)
                            uCAB_Status[i] = "Enable";
                        else if ((uCURSOR[i] & 0x00000C00) >> 10 == 2)
                            uCAB_Status[i] = "Enable";
                        else if ((uCURSOR[i] & 0x00000F00) >> 8 == 0)
                            uCAB_Status[i] = "Disable";
                        else
                            uCAB_Status[i] = "Undefined";
                    }
                }


        }
    }
}
