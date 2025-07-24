using System;
using Microsoft.Win32.SafeHandles;
using System.Threading;
using System.IO;
using System.Management;
using System.Collections.Generic;

namespace DisplayCStates
{
    public class DC_State_Status
    {
        public string sw_dc_state_status;
        public string hw_dc5_status;
        public string hw_dc6_dc9_status;

        public DC_State_Status()
        {
            sw_dc_state_status = "Not Enabled";
            hw_dc5_status = string.Empty;
            hw_dc6_dc9_status = string.Empty;
        }
    }
    class Program
    {
        public static UInt32 DCStateEnable = 0;
        public static UInt32 DCStateSelect = 0;
        public static UInt32 PowerWell2State = 0;
        public static UInt32 DCStateDebug = 0;
        public static UInt32 DCStateEnable1 = 0;
        public static UInt32 DCStateSelect1 = 0;
        public static UInt32 PowerWell2State1 = 0;
        public static UInt32 DePLLEnable = 0;
        public static UInt32 DsiPLLEnable = 0;
        public static bool PanelPWM = false;
        public static bool PSRDisplay = false;
        public static DC_State_Status dc_state_status = new DC_State_Status();

        public enum Platform
        {
            None,
            SKL,
            KBL,
            APL,
            GLK,
            CNL,
            CFL,
            ICL_LP,
            ICL_HP,
        }
        public enum Display
        {
            None,
            EDP,
            MIPI,
        }
        static Platform platform = Platform.None;
        static List<Platform> LP_Platform = new List<Platform>() { Platform.APL, Platform.GLK };
        static bool is_lp_platform = false;

        static Dictionary<Platform, uint> DMC_DC5_Counter_Register = new Dictionary<Platform, uint>
        {
            { Platform.APL,     0x80038 },
            { Platform.GLK,     0x80030},
            { Platform.ICL_HP,  0x101084}
        };

        static Dictionary<Platform, uint> DMC_DC6_Counter_Register = new Dictionary<Platform, uint>
        {
            { Platform.ICL_HP,  0x101088 }
        };

        static void Main(string[] args)
        {
            Display display = Display.None;
            Logger.Clear();
            RegisterInterfaces.Escape_path = false;
            RegisterInterfaces.Diva_driver_status = GetDivaDriverStatus();

            AppDomain.CurrentDomain.UnhandledException += new UnhandledExceptionEventHandler(GlobalExceptionHandler);

            if (args.Length != 2 ||
                (args.Length == 1 && (args[0].Contains("/?") || args[0].Contains("help"))))
            {
                HelpText();
                return;
            }
            if ( (Enum.TryParse(args[0], true, out platform) == false) ||
                (Enum.TryParse(args[1], true, out display) == false))
            {
                HelpText();
                return;
            }

            if (display == Display.MIPI)
            {
                if (false == VerifyCommandModeforMIPIDisplay())
                {
                    Logger.Message("Test should work on MIPI command mode..");
                    return;
                }
            }


            Logger.Message("************************ Display C-States ************************");
            Logger.Message("Platform: {0} display: {1}", platform, display);

            is_lp_platform = LP_Platform.Contains(platform);

            if(true == is_lp_platform)
                Verify_DCStates_LP(display);
            else
                Verify_DCStates_GEN();

            // Verify DC State Result
            Logger.Message("Press the Enter key to check Display C State Acheived");
            Console.ReadLine();



            Logger.Message("======================== DC State Result ===========================");
            Logger.Message("SW DC State Status: {0}", dc_state_status.sw_dc_state_status);

            if(dc_state_status.hw_dc5_status != string.Empty)
                Logger.Message("{0}", dc_state_status.hw_dc5_status);

            if (dc_state_status.hw_dc6_dc9_status != string.Empty)
                Logger.Message("{0}", dc_state_status.hw_dc6_dc9_status);
            Logger.Message("====================================================================");

            Logger.Message("Press the Enter key to exit the program at any time... ");
            Console.ReadLine();

            Logger.Message("****************************** End ******************************");
        }

        public static bool VerifyCommandModeforMIPIDisplay()
        {
            bool cmdMode = true;
            Int32 cmdMode_bitmap = 0xE000;
            UInt32 RegisterValue = 0;

            //0x6B00C MIPI connected in PORTA - bit 13-15 -> 0 command mode not supported. bit  7-10 -> 0 video mode not supported.
            //0x6B80C MIPI connected in PORTC - bit 13-15 -> 0 command mode not supported. bit  7-10 -> 0 video mode not supported.
            RegisterInterfaces.ReadMMIO(0x6B00C, out RegisterValue);
            if ((cmdMode_bitmap & RegisterValue) == 0)
                cmdMode = false;

            if (cmdMode == false)
            {
                RegisterValue = 0;
                RegisterInterfaces.ReadMMIO(0x6B80C, out RegisterValue);
                if ((cmdMode_bitmap & RegisterValue) == 0)
                    cmdMode = false;
            }
            return cmdMode;
        }

        public static void Verify_DCStates_GEN()
        {
            uint DC5_Counter_Register = 0x80030;
            uint DC6_Counter_Register = 0x8002c;
            uint DC5CounterInitial = 0, DC5CounterFinal = 0, DC6CounterInitial = 0, DC6CounterFinal = 0;

            if (Platform.ICL_HP == platform)
            {
                DMC_DC5_Counter_Register.TryGetValue(platform, out DC5_Counter_Register);
                DMC_DC6_Counter_Register.TryGetValue(platform, out DC6_Counter_Register);
            }
            RegisterInterfaces.ReadMMIO(DC5_Counter_Register, out DC5CounterInitial);
            RegisterInterfaces.ReadMMIO(DC6_Counter_Register, out DC6CounterInitial);

            //Verify SW DC State{
            Display_C_State_for_EDP(is_lp_platform, true);

            var startTime = DateTime.UtcNow;
            while (DateTime.UtcNow - startTime < TimeSpan.FromSeconds(120))
            {
                Display_C_State_for_EDP(is_lp_platform, false);
                Thread.Sleep(4000);
            }
            
            // Verify HW DC5 Status
            RegisterInterfaces.ReadMMIO(DC5_Counter_Register, out DC5CounterFinal);
            if ((DC5CounterInitial != DC5CounterFinal) && (DC5CounterFinal - DC5CounterInitial != 0xffffffff))
            {
                Logger.Message("Change in DC3_DC5_Counter Values :- Initial {0}, Final {1}", DC5CounterInitial, DC5CounterFinal);
                dc_state_status.hw_dc5_status = "HW DC 5";
            }

            // Verify HW DC6 Status
            RegisterInterfaces.ReadMMIO(DC6_Counter_Register, out DC6CounterFinal);

            if ((DC6CounterInitial != DC6CounterFinal) && (DC6CounterFinal - DC6CounterInitial != 0xffffffff))
            {
                Logger.Message("Change in DC5_DC6_Counter Values :- Initial {0}, Final {1}", DC6CounterInitial, DC6CounterFinal);
                dc_state_status.hw_dc6_dc9_status = "HW DC 6";
            }
        }
        public static void Verify_DCStates_LP(Display display)
        {
            uint DC5_Counter_Register = 0;
            uint DC5CounterInitial = 0, DC5CounterFinal = 0;
            DMC_DC5_Counter_Register.TryGetValue(platform, out DC5_Counter_Register);

            RegisterInterfaces.ReadMMIO(DC5_Counter_Register, out DC5CounterInitial);

            //Verify SW DC State
            Display_C_State_for_EDP(true, true);

            //Pollling MMIO read for verifying HW DC State
            var startTime = DateTime.UtcNow;
            while (DateTime.UtcNow - startTime < TimeSpan.FromSeconds(120))
            {
                Display_C_State_for_EDP(true, false); 
                Thread.Sleep(4000);
            }

            //Verify HW DC5
            RegisterInterfaces.ReadMMIO(DC5_Counter_Register, out DC5CounterFinal);
            if ((DC5CounterInitial != DC5CounterFinal) && (DC5CounterFinal - DC5CounterInitial != 0xffffffff))
            {
                Logger.Message("Change in DC3_DC5_Counter Values :- Initial {0}, Final {1}", DC5CounterInitial, DC5CounterFinal);
                dc_state_status.hw_dc5_status = "HW DC 5";
            }

            //Verify HW DC9
            if (dc_state_status.hw_dc6_dc9_status != String.Empty)
            {
                dc_state_status.hw_dc6_dc9_status = "HW DC 9";
            }
        }
        private static void Display_C_State_for_EDP(bool islowPowerPlatform, bool sw_dc_state)
        {
            Int32 bitmap = 0x00000003;
            int value = 2;
            if (islowPowerPlatform)
            {
                bitmap = 0x00000001;
                value = 1;
            }
            RegisterInterfaces.ReadMMIO(0x45404, out PowerWell2State1);
            RegisterInterfaces.ReadMMIO(0x45500, out DCStateSelect);
            RegisterInterfaces.ReadMMIO(0x45504, out DCStateEnable);
            Logger.Message("DC_States Register Value at" + DateTime.Now.ToString() + " PowerWell2 " + String.Format("0x{0:X}", PowerWell2State) +  " DC_State_Select " + String.Format("0x{0:X}", DCStateSelect) + " DC_State_Enable " + String.Format("0x{0:X}", DCStateEnable));
            if ((true == sw_dc_state) && ((DCStateEnable & bitmap) == value))
            {
                dc_state_status.sw_dc_state_status = "Enabled";
            }
            else
            {
                if (DCStateEnable == 0xffffffff)
                {
                    if (islowPowerPlatform)
                        dc_state_status.hw_dc6_dc9_status = "HW DC 9";
                    else
                        dc_state_status.hw_dc6_dc9_status = "HW DC 6";

                }
            }
        }

        private static void HelpText()
        {
            string platformString = string.Empty;
            string display = string.Empty;

            foreach (string name in Enum.GetNames(typeof(Platform)))
            {
                platformString += name + " ";
            }
            foreach (string name in Enum.GetNames(typeof(Display)))
            {
                display += name + " ";
            }
            Logger.Message("###################################################################");
            Logger.Message("# ..\\>DisplayCStates.exe <platform> <internal display>");
            Logger.Message("# Supported platforms are {0}:", platformString);
            Logger.Message("# Supported internal displays are {0}", display);
            Logger.Message("###################################################################");
        }

        private static void GlobalExceptionHandler(object sender, UnhandledExceptionEventArgs e)
        {
            Logger.Message("Exception Message");
            Exception exception = e.ExceptionObject as Exception;
            Logger.Message("{0}", exception.StackTrace);
            Logger.Message(exception.Message);
        }

        private static bool GetDivaDriverStatus()
        {
            bool status = false;
            string divaSearchQuery = "select * from Win32_SystemDriver where Name = 'DivaKmd'";
            ManagementObjectSearcher searcher = new ManagementObjectSearcher(divaSearchQuery);
            var drivers = searcher.Get();

            if (drivers.Count >= 1)
            {
                string divaDriverState = default(string);
                foreach (ManagementObject mo in drivers)
                {
                    if (mo["State"] != null)
                    {
                        divaDriverState = mo["State"].ToString();
                        Logger.Message("DivaDriver State: {0}", divaDriverState);
                    }

                    if (divaDriverState == "Running")
                    {
                        status = true;
                    }
                }
            }
            return status;
        }
    }
}
