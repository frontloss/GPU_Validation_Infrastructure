using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;
using IntelWiDiLib;
using System.Runtime.InteropServices;
using System.Xml;
using System.IO;
using System.Diagnostics;
using System.Threading;

namespace WiDiConnectionApp
{
    static class Program
    {
        static WiDiExtensionsClass WiDi;
        [DllImport("user32.dll", CallingConvention = CallingConvention.Cdecl)]
        public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);

        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new Form1());
        }
    }
}
