namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Diagnostics;
    using System.Threading.Tasks;
    using System.Windows.Automation ;
    using System.Linq;
    using System.Collections.Generic;
    using System.Threading;

    internal class LANInstallationDriver : FunctionalBase, IParse, ISetMethod 
    {
        private string _customDriverPath = string.Empty;
        private Task<Process> _processTask = null;
        private AutomationElement _rootElement = null;
        private bool _driverRemoved = false;
       
        private List<Dictionary<string, string>> _elementSequence = new List<Dictionary<string, string>>()
        {
          new Dictionary<string,string>() { {"Install Drivers and Software", null} } ,
          new Dictionary<string,string>() { {"Next >",null} } ,
          new Dictionary<string,string>() { {"I accept the terms in the license agreement","Remove"} } ,
          new Dictionary<string,string>() { {"Next >",null} } ,
          new Dictionary<string,string>() { {"Next >","Remove"} } ,
          new Dictionary<string,string>() { {"Install","Skip"} } ,
          new Dictionary<string,string>() { {"Finish",null} } 
        };

        public void Parse(string[] args)
        {   
            Log.Verbose("LANDriverInstallation Parsing Start");
            if (!args.Length.Equals(0) && args[0].ToLower().Contains("set"))
            {
                if (args.Length > 1)
                    _customDriverPath = args[1];

                this.SetMethod(null);
            }
            else
                this.HelpText();

            Log.Verbose("LANDriverInstallation Parsing end");
        }

        public bool SetMethod(object argMessage)
        {
            Log.Verbose("LANDriverInstallation SetMethod Start");
            if (argMessage != null)
                _customDriverPath = argMessage as string;

            if (StartInstallation())
            {
                Log.Success("Driver Installation completed successful");
                return true;
            }

            Log.Fail("Some problem while Installation Process ");
            return false;
        }

        private bool StartInstallation()
        {
            Log.Verbose("LAN Driver Installation Start");
            string driverPath = this.GetDriverPath;
            if (driverPath.EndsWith(@"\"))
                driverPath = driverPath.Remove(driverPath.Length - 1);

            if (driverPath.Equals(""))
                Log.Abort("LAN DRIVER INSTALLATION FAIL : LAN DRIVER INSTALLATION PATH IS MISSING");

            Log.Verbose("Custom Driver path is : {0} {1} AppConfig Driver path is : {2}", this._customDriverPath, Log.NewLine, driverPath);                       
            this._processTask = Task.Factory.StartNew<Process>(() => CommonExtensions.StartProcess(string.Format(@"{0}\Autorun.exe",driverPath), "-s -overwrite"));
           
            _rootElement = AutomationElement.RootElement;

            if (_rootElement != null)
            {
                Log.Verbose("Root Element found");           
                Thread.Sleep((3) * 1000);
                bool installationStatus = Next(0) ;
                if (_driverRemoved && installationStatus)
                {
                    _driverRemoved = false;
                    Log.Verbose("Driver uninstall successfully AND Installation process starts ");
                    return Next(0);
                }

                return installationStatus;
            }

            Log.Verbose("Automation Root element not found");
            return false;
        }

        private bool Next(int argElementIndex)
        {
            if (argElementIndex == _elementSequence.Count)
                return true;
            if (_elementSequence.ElementAt(argElementIndex).Values.ElementAt(0) != null && _elementSequence.ElementAt(argElementIndex).Values.ElementAt(0).Equals("Skip") && _driverRemoved == true)
                return Next(++argElementIndex);

            uint timer = 0;
            Condition regCondition = null;
            AutomationElement appElement = null;

            while (timer < 48)
            {
                Thread.Sleep((5) * 1000);
                regCondition = new PropertyCondition(AutomationElement.NameProperty, _elementSequence.ElementAt(argElementIndex).Keys.ElementAt(0));
                appElement = _rootElement.FindFirst(TreeScope.Descendants, regCondition);

                if (appElement != null)
                    break;

                if (_elementSequence.ElementAt(argElementIndex).Values.ElementAt(0) != null)
                {
                    regCondition = new PropertyCondition(AutomationElement.NameProperty, _elementSequence.ElementAt(argElementIndex).Values.ElementAt(0));
                    appElement = _rootElement.FindFirst(TreeScope.Descendants, regCondition);

                    if (appElement != null)
                    {
                        Log.Verbose("Driver Uninstallation process going on .... ");
                        _driverRemoved = true;
                        break;
                    }
                }

                timer++;
            }

            if (appElement == null)
                Log.Abort("LAN DRIVER INSTALLATION FAIL : {0} 1] LAN DRIVER INSTALLATION PATH IS WRONG {0} 2] INSTALLATION ELEMENT NOT FOUND {0} 3] LAN ADAPTER IS MISSING", Log.NewLine);

            Log.Verbose("Step : {0} :::: Element : {1} ", argElementIndex + 1, appElement.Current.Name);
            ClickElement(appElement);
            return Next(++argElementIndex);
        }

        private void ClickElement(AutomationElement argElement) 
        {
            if (null != argElement)
            {
                if (argElement.Current.ControlType.Equals(ControlType.RadioButton))
                {
                    SelectionItemPattern pattern = argElement.GetCurrentPattern(SelectionItemPattern.Pattern) as SelectionItemPattern;
                    pattern.Select();
                }
                else if (argElement.Current.ControlType.Equals(ControlType.Button))
                {
                    InvokePattern pattern = argElement.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
                    pattern.Invoke();
                }                
            }
        }

        private string GetDriverPath
        {
            get { return this._customDriverPath.Equals("") ? base.AppSettings.LANDriverPath + "\\" + base.MachineInfo.OS.Type : this._customDriverPath ; }
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append(string.Format(@"..\>Execute LANInstallationDriver set [driverPath --> {1}]" , this.GetDriverPath)).Append(Environment.NewLine);            
            Log.Message(sb.ToString());
        }
    }
}
