using System;
using System.Linq;
using System.Runtime.InteropServices;

namespace ACPISwitching
{
    class Program
    {
        [DllImport("inpout32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        private static extern short Inp32(short PortAddress);

        [DllImport("inpout32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        private static extern void Out32(short PortAddress, short data);

        const int KB_DISABLE = 0xAD;
        const int KB_ENABLE = 0xAE;
        const int C3_CODE = 0xC3;
        const int KeyStatus = 0x64;
        const int KeyData = 0x60;
        const int OBFULL = 0x01;
        const int IBFULL = 0x02;

        enum ScanCodes
        {
            F1 = 0x3b,
            F2 = 0x3c,
            F3 = 0x3d,
            F4 = 0x3e,
            F8 = 0x42
        }

        static void Main(string[] args)
        {
            ScanCodes scanCodes;
            if (args.Length.Equals(0) || args.Length > 1)
                Console.WriteLine("Possible ScanCode argument --> F1 | F2 | F3 | F4 | F8");
            else
            {
                if (Enum.TryParse(args.First(), true, out scanCodes))
                {
                    if (SwitchUsingAcpiKeys(scanCodes))
                        Console.WriteLine("Switching succeeded through {0}", scanCodes);
                    else
                        Console.WriteLine("Switching not succeeded through {0}", scanCodes);
                }
                else
                {
                    Console.WriteLine("Invalid ScanCode passed --> {0}", args.First());
                    Console.WriteLine("Possible ScanCode argument --> F1 | F2 | F3 | F4 | F8");
                }
            }
        }

        static void SendCommand(int key)
        {
            int StatusFlag = 0x00;

            // Output to the keyboard command port
            Out32((short)KeyStatus, (short)key);

            // Check whether the write is complete
            StatusFlag = Inp32((short)KeyStatus);

            while (Convert.ToBoolean(StatusFlag & OBFULL))
            {
                StatusFlag = Inp32((short)KeyStatus);
            }
        }

        static void SendKey(int key)
        {
            int StatusFlag = 0x00;
            // Check to verfiy whether the port is ready
            StatusFlag = Inp32((short)KeyStatus);

            while (Convert.ToBoolean(StatusFlag & IBFULL))
            {
                StatusFlag = Inp32((short)KeyStatus);
            }

            // Output to the keyboard command port
            Out32((short)KeyData, (short)key);

            // Check whether the write is complete
            StatusFlag = Inp32((short)KeyStatus);

            while (Convert.ToBoolean(StatusFlag & OBFULL))
            {
                StatusFlag = Inp32((short)KeyStatus);
            }
        }

        static bool SwitchUsingAcpiKeys(ScanCodes funcKey)
        {
            try
            {
                SendCommand(KB_DISABLE);	// Disable the Keyboard
                SendCommand(C3_CODE);	// Send C3 command (custom for HK testing)
                SendKey((int)funcKey);		// Send the hot key scan code
                SendCommand(KB_ENABLE);	// Enable the Keyboard
                return true;
            }
            catch (Exception e)
            {
                Console.WriteLine("Error in switching using ACPI HotKeys:{0}", e.ToString());
                return false;
            }

        }
    }
}
