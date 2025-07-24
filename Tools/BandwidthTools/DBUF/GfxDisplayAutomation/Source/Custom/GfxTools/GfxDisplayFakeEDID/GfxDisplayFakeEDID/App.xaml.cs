namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Diagnostics;
    using System.Windows;

    public partial class App : Application
    {
        private void Application_Startup(object sender, StartupEventArgs e)
        {
            this.MainWindow = new FakeEDID();
            SourceViewModel sourceVM = new SourceViewModel();
            sourceVM.View = (IView)this.MainWindow;
            this.MainWindow.DataContext = sourceVM;
            this.MainWindow.Show();
        }
        private void Application_Exit(object sender, ExitEventArgs e)
        {
            Process currentProcess = Process.GetProcessesByName("GfxDisplayFakeEDID").FirstOrDefault();
            if (null != currentProcess)
                currentProcess.Kill();
        }
    }
}
