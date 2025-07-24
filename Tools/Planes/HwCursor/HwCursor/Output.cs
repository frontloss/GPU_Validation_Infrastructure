using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using HardwareCursor;

namespace PlaneStatus
{
    public class RegisterOutput
    {
        const uint HWCURSORPMASK = 0x00000027;

        public void RegOutput(HardwareCursor.MPOOptions Options, StreamWriter outFile)
        {
            int piIndex = 0, plIndex = 0;
            uint[][] RegisterOffset = GetOffSet();
            String[][] RegisterLabel = GetOffSetName();

            for (piIndex = 0; piIndex < RegisterOffset.GetLength(0); piIndex++)
            {
                int planeCount = 0;
                for (plIndex = 0; plIndex < RegisterOffset[piIndex].Length; plIndex++)
                {
                    uint RegValue = 0;
                    if (RegisterInterface.Instance.ReadWriteRegister(RegisterInterface.RegisterOperation.READ, RegisterOffset[piIndex][plIndex], out RegValue, Options.IsDDRW))
                    {
                        Console.ForegroundColor = ConsoleColor.Green;
                        Console.Write(RegisterLabel[piIndex][plIndex] + /*String.Format(" 0x{0:X}", RegisterOffset[piIndex][plIndex]) +*/ ": " + String.Format("0x{0:X}", RegValue) + "::");
                        outFile.Write(RegisterLabel[piIndex][plIndex] + /*String.Format(" 0x{0:X}", RegisterOffset[piIndex][plIndex]) +*/ ": " + String.Format("0x{0:X}", RegValue) + "::");

                        Console.Write("HWcursor > " + IsHWcursorEnabled(RegValue) + "; ");
                        outFile.Write("HWcursor > " + IsHWcursorEnabled(RegValue) + "; ");

                        Console.WriteLine();
                        outFile.WriteLine();
                            
                        planeCount++;
                    }
                }
                
                if(planeCount != 0)
                { 
                    Console.WriteLine("MultiPlane Overlay is enabled on PIPE " + ((char)(piIndex + 65)));
                    outFile.WriteLine("MultiPlane Overlay is enabled on PIPE " + ((char)(piIndex + 65)));
                }
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

        private static string IsHWcursorEnabled(uint RegValue)
        {
            if ((RegValue & HWCURSORPMASK) > 0)
                return "Enabled";
            return "Disabled";
        }

        private static uint[][] GetOffSet()
        {
            uint[][] offset = null;
            offset = new uint[3][] { new uint[] { 0x70080},
                                         new uint[] { 0x71080},
                                         new uint[] { 0x72080} };

            return offset;
        }

        private static String[][] GetOffSetName()
        {
            String[][] offsetLabel = null;
            offsetLabel = new string[3][] { new string[] { "Cursor Control A"},
                                            new string[] { "Cursor Control B "},
                                            new string[] { "Cursor Control C" } };

            return offsetLabel;
        }

    }
}
