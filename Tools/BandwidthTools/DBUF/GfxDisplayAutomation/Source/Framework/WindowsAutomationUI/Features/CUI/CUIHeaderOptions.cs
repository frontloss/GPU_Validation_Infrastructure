namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Text;
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Runtime.InteropServices;

    public class CUIHeaderOptions : FunctionalBase, ISet, IParse
    {
        [DllImport("user32.dll")]
        private static extern bool ShowWindowAsync(IntPtr hWnd, int nCmdShow);

        public object Set
        {
            set { this.PerformAction((int)((CUIWindowOptions)value)); }
        }

        private void PerformAction(int argAction)
        {
            Log.Verbose("In CUIHeaderOptions (Windows Automation UI)");
            Process.GetProcesses().Where(p => p.ProcessName.StartsWith("Gfx")).ToList().ForEach(p =>
            {
                Log.Verbose("{0} CUI", (CUIWindowOptions)argAction);
                if ((CUIWindowOptions)argAction == CUIWindowOptions.Close)
                    p.Kill();
                else
                    ShowWindowAsync(p.MainWindowHandle, argAction);
            });
        }
        public void Parse(string[] args)
        {
            CUIWindowOptions cuiWindowOptions;
            if (args.Length > 1 && args[0].Equals("set") && Enum.TryParse(args[1], true, out cuiWindowOptions))
                this.Set = cuiWindowOptions;
            else
                this.HelpText();
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append(@"..\>Execute CUIHeaderOptions set close|Maximize|Restore|Minimize").Append(Environment.NewLine);
            Log.Message(sb.ToString());
        }
    }
}