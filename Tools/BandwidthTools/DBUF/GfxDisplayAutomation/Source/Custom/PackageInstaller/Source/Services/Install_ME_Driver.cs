using System.Linq;
using System.IO;
using System.Threading;
using System.Windows.Automation;
using System.Diagnostics;

namespace PackageInstaller
{
    class Install_ME_Driver : InitEnvironment
    {
        public override bool Run()
        {
            if (CommonRoutine.IsSystemRebooted() == false)
            {
                return InstallMEDriver();
            }
            else
            {
                if(VerifyMEDriver() == true)
                    return true;
                else
                {
                    CommonRoutine.ClearRebootFile();
                    return false;
                }
            }
        }

        private bool VerifyMEDriver()
        {
            Log.Messege("Verifying ME Driver Status");
            Process MEInstallProcess = CommonRoutine.StartProcess("wmic", " product where \"Name like '%Management Engine Components%'\" get Name");
            MEInstallProcess.WaitForExit();
            StreamReader reader = MEInstallProcess.StandardOutput;
            string output = reader.ReadToEnd();
            if (output.Contains("Management Engine Components"))
            {
                Log.Messege("ME Driver installed on test machine.");
                return true;
            }
            else
            {
                Log.Messege("ME Driver not installed on test machine.");
                return false;
            }
        }

        private bool InstallMEDriver()
        {
            if (VerifyMEDriver() == true)
                return true;

            if (Parser.CommadData.Count == 0 || Parser.CommadData.Count > 1)
            {
                Log.Fail("Invalid command line.");
                CommonRoutine.Exit(ErrorCode.Fail);
            }
            string dir = Parser.CommadData.First();
            if (!Directory.Exists(dir))
            {
                Log.Fail("ME Driver not found in {0}", dir);
                return false;
            }
            else
            {
                Log.Messege("Installing ME Driver");
                Process installProcess = CommonRoutine.StartProcess(dir + "\\SetupME.exe", " -overwrite -s");
                Thread.Sleep(25000);
                UIABaseHandler uiaBaseHandler = new UIABaseHandler();

                AutomationElement rootElement = AutomationElement.RootElement;
                AutomationElement appElement = null;
                Condition regCondition = null;
                regCondition = new PropertyCondition(AutomationElement.NameProperty, "Install");
                appElement = rootElement.FindFirst(TreeScope.Descendants, regCondition);
                if (appElement != null)
                {
                    AutomationElement elem = UIABaseHandler.SelectElementNameControlType("Install", ControlType.Button);
                    uiaBaseHandler.Invoke(elem);
                    installProcess.WaitForExit();
                    Thread.Sleep(10000);
                    CommonRoutine.Reboot();
                }
            }
            return true;
        }
    }
}
