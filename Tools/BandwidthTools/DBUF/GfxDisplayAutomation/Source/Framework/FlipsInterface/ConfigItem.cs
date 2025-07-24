using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Configuration;
using System.Runtime.InteropServices;
using System.IO;

namespace Intel.VPG.Display.FlipsInterface
{
    public class ConfigItem
    {
        [DllImport("User32.dll")]
        static extern IntPtr GetDC(IntPtr hwnd);

        [DllImport("User32.dll")]
        static extern int ReleaseDC(IntPtr hwnd, IntPtr dc);

        [DllImport("gdi32.dll")]
        static extern IntPtr DeleteDC(IntPtr hDc);

        [DllImport("gdi32.dll")]
        static extern int GetDeviceCaps(IntPtr hdc, int nIndex);


        //private static readonly ILog logger = LogManager.GetLogger(typeof(Intel.VPG.Display.FlickerTestSuite.ConfigItem));
        private static Dim currentMode = null;

        public static Dim CurrentMode
        {
            get
            {
                if (ConfigItem.currentMode == null)
                {
                    IntPtr primary = GetDC(IntPtr.Zero);
                    int DESKTOPVERTRES = 117;
                    int DESKTOPHORZRES = 118;
                    int actualPixelsX = GetDeviceCaps(primary, DESKTOPHORZRES);
                    int actualPixelsY = GetDeviceCaps(primary, DESKTOPVERTRES);
                    ReleaseDC(IntPtr.Zero, primary);
                    DeleteDC(primary);

                    currentMode = new Dim();
                    currentMode.Width = (uint)actualPixelsX;
                    currentMode.Height = (uint)actualPixelsY;
                }
                return ConfigItem.currentMode;
            }
        }



        public static string GetStringValue(string keyName)
        {
            string retValue = string.Empty;
            try
            {
                retValue = ConfigurationManager.AppSettings[keyName];
            }
            catch
            {
                //logger.ErrorFormat("Error: fetching keyname {0}", keyName);
            }
            return retValue;
        }


        private static int GetValue(string keyName, int default_value = 0)
        {
            int retValue = 0;
            try
            {
                string strValue = ConfigurationManager.AppSettings[keyName];
                Int32.TryParse(strValue, out retValue);
            }
            catch
            {
                retValue = default_value;
            }
            return retValue;
        }

        public static int FlipDelay()
        {
            return GetValue("FLIP_DELAY");
        }

        public static string VariationDefaultPath()
        {
            string path = Directory.GetCurrentDirectory();
            path = System.IO.Path.Combine(path, "Variations");

            return path;
        }

        public static uint EdpMonitor_ID()
        {
            uint id = 1;
            string monitorid = ConfigurationManager.AppSettings["EDP"];
            UInt32.TryParse(monitorid, out id);
            return id;
        }

        public static bool UnderRunCheck()
        {
            return (GetValue("UNDER-RUN_CHECK") > 0) ? true : false;
        }

        public static bool UnderRunExit()
        {
            return (GetValue("UNDERRUN_EXIT") > 0) ? true : false;
        }


        public static int BreakAfterIteration()
        {
            return GetValue("BREAK_AFTER_ITERATION");
        }

        public static bool DumpRegister()
        {
            return (GetValue("DUMP_REGISTER") > 0) ? true : false;
        }

        public static bool DumpVariation()
        {
            return (GetValue("DUMP_VARIATION") > 0) ? true : false;
        }

        public static int IterationLimit()
        {
            return GetValue("ITERATION_LIMIT", 250);
        }

        public static int StartDelay()
        {
            return GetValue("START_DELAY", 1);
        }

        public static bool Interrupt()
        {
            return (GetValue("INTERRUPT",1) > 0) ? true : false;            
        }

        //public static bool isBaseLayer(uint zorder)
        //{
        //    if (zorder == (TestVector.getInstance().Count - 1))
        //    {
        //        return true;
        //    }
        //    return false;
        //}
    }
}
