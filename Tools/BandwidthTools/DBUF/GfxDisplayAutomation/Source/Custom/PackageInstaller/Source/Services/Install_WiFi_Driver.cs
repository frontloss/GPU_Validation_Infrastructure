using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Windows.Automation;
using System.Threading.Tasks;

namespace PackageInstaller
{
    class Install_WiFi_Driver : InitEnvironment
    {
        public override bool Run()
        {
            return InstallWiFiDriver();
        }

        private bool InstallWiFiDriver()
        {
            if (Parser.CommadData.Count == 0 || Parser.CommadData.Count > 1)
            {
                Log.Fail("Invalid command line.");
                CommonRoutine.Exit(ErrorCode.Fail);
                return false;
            }

            string dir = Parser.CommadData.First();
            if (!Directory.Exists(dir))
            {
                Log.Fail("WiFi Driver not found in {0}", dir);
                return false;
            }
            else
            {
                Log.Messege("Installing WiFi Driver");
                Process installProcess = CommonRoutine.StartProcess(dir + "\\Setup.exe", " -s");
                Log.Messege("Wait for Max 6 minutes..");
                for (int i = 0; i < 36; i++)
                {
                    Thread.Sleep(10000);
                    UIABaseHandler uiaBaseHandler = new UIABaseHandler();
                    AutomationElement rootElement = AutomationElement.RootElement;
                    AutomationElement appElement = null;
                    Condition regCondition = null;
                    regCondition = new PropertyCondition(AutomationElement.NameProperty, "Install");
                    appElement = rootElement.FindFirst(TreeScope.Descendants, regCondition);
                    if (appElement != null)
                    {
                        Thread.Sleep(3000);
                        AutomationElement elem = UIABaseHandler.SelectElementNameControlType("Install", ControlType.Button);
                        uiaBaseHandler.SendKey(elem);
                        installProcess.WaitForExit();
                        if (installProcess.HasExited)
                            break;
                    }
                    if (installProcess.HasExited)
                        break;
                }
                if (installProcess.HasExited)
                {
                    Thread.Sleep(15000); //buffer wait.
                    return true;
                }
                else
                    return false;
            }
        }
    }
}
