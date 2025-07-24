namespace Intel.VPG.Display.Automation
{
    using System.Diagnostics;

    static class CommonExtensions
    {
        internal static Process StartProcess(string argFileName, string arguments)
        {
            ProcessStartInfo processStartInfo = new ProcessStartInfo();
            processStartInfo.RedirectStandardOutput = true;
            processStartInfo.RedirectStandardInput = true;
            processStartInfo.UseShellExecute = false;
            processStartInfo.CreateNoWindow = true;
            processStartInfo.WindowStyle = ProcessWindowStyle.Hidden;
            processStartInfo.FileName = argFileName;
            if (!string.IsNullOrEmpty(arguments))
                processStartInfo.Arguments = arguments;
            Process process = new Process();
            process.StartInfo = processStartInfo;
            process.Start();
            return process;
        }
    }
}
