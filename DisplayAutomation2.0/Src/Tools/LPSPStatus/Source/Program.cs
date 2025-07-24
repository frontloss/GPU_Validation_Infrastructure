using System;
using System.Management;

namespace LPSPStatus
{
    class Program
    {
        public enum Platform
        {
            None,
            HSW,
            BDW,
            SKL,
            KBL,
            APL,
            GLK,
            CNL,
            CFL,
            ICL,
        }

        static Platform platform = Platform.None;
        static void Main(string[] args)
        {
            
            Logger.Clear();
            AppDomain.CurrentDomain.UnhandledException += new UnhandledExceptionEventHandler(GlobalExceptionHandler);

            RegisterInterfaces.Escape_path = false;
            RegisterInterfaces.Diva_driver_status = GetDivaDriverStatus();

            /* Command line parameter verification */
            if (args.Length != 1 ||
                ((args[0].Contains("/?")) || (args[0].Contains("h")) || (args[0].Contains("help"))))
            {
                HelpText();
                return;
            }
            if ((Enum.TryParse(args[0], true, out platform) == false))
            {
                HelpText();
                return;
            }

            while (true)
            {
                Logger.Message(string.Empty);
                if (VerifyLPSP())
                        Logger.Message("LPSP IS ENABLED");
                else
                    Logger.Message("LPSP IS DISABLED");
                Logger.Message("Verify LPSP Status again y/n ?");
                ConsoleKeyInfo key = Console.ReadKey(true);
                if (key.Key == ConsoleKey.N)
                    break;
            }
            Logger.Message("Press any key to exit.");
            Console.ReadLine();
        }
        private static bool VerifyLPSP()
        {
            bool status = false;
            UInt32 power_well1_register = 0x45400;
            UInt32 power_well2_register = 0x45404;
            UInt32 power_well2_status = 0;
            UInt32 power_well1_status = 0;
            RegisterInterfaces.ReadMMIO(power_well2_register, out power_well2_status);
            Logger.Message("Power_Well_2 Offset {0} - Value {1}", String.Format("0x{0:X}", power_well2_register), String.Format("0x{0:X}", power_well2_status));
            if (platform >= Platform.ICL)
            {
                /* Verify PWR_WELL_CTL2 register (0x45404) - > 0th bit specify Power_well_1 status. 1 -> Enable, 0 -> Disable */
                if ((Convert.ToInt64(power_well2_status) & 0xFFFFFFFF) == 1) status = true;
            }
            else
            {
                /* Upto CFL there are only two power well.*/
                /* Verify PWR_WELL_CTL1 register (0x45400) - > 30th bit specify Power_well_1 status. 1 -> Enable, 0 -> Disable */
                /* Verify PWR_WELL_CTL2 register (0x45404)- > 30 and 31th bit specify Power well 2 status. 1 -> Enable 0 -> Disable */
                RegisterInterfaces.ReadMMIO(power_well1_register, out power_well1_status);
                Logger.Message("Power_Well_1 Offset {0} - Value {1}", String.Format("0x{0:X}", power_well1_register), String.Format("0x{0:X}", power_well1_status));
                if (((Convert.ToInt64(power_well2_status) & 0xC0000000) == 0) &&
                    ((Convert.ToInt64(power_well1_status) & 0x40000000) == 0x1)) status = true;
            }
            return status;
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
        private static void HelpText()
        {
            string platformString = string.Empty;

            foreach (string name in Enum.GetNames(typeof(Platform)))
            {
                platformString += name + " ";
            }
            Logger.Message("###################################################################");
            Logger.Message("# ..\\>LPSPStatus.exe <platform>");
            Logger.Message("# Supported platforms are {0}:", platformString);
            Logger.Message("###################################################################");
        }

        private static void GlobalExceptionHandler(object sender, UnhandledExceptionEventArgs e)
        {
            Logger.Message("Exception Message");
            Exception exception = e.ExceptionObject as Exception;
            Logger.Message("{0}", exception.StackTrace);
            Logger.Message(exception.Message);
        }

    }
}
