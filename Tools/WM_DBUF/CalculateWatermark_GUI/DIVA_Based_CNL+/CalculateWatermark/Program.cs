using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using System.Diagnostics;

namespace CalculateWatermark
{
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            InstallIgfxBridge();
            Application.Run(new CalculateWM());
        }

        static private void InstallIgfxBridge()
        {
            string filePath = "";
            string dllName = "IgfxExtBridge.dll";
            string osVersion = Environment.GetEnvironmentVariable("PROCESSOR_ARCHITECTURE");
            if (osVersion == "x86")
                filePath = Directory.GetCurrentDirectory() + "\\32_Bit_Libs\\" + dllName;
            else
                filePath = Directory.GetCurrentDirectory() + "\\64_Bit_Libs\\" + dllName;

            Process regIgfxExtBridge = new Process();
            regIgfxExtBridge.StartInfo.FileName = "regsvr32.exe";
            regIgfxExtBridge.StartInfo.Arguments = "/s" + filePath;
            regIgfxExtBridge.Start();
            System.Threading.Thread.Sleep(1000);
        }
    }
}
