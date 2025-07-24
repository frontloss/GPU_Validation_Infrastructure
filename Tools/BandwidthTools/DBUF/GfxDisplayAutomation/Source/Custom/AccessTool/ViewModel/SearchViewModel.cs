using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Windows.Input;
using System.IO;

namespace Intel.VPG.Display.Automation
{
    public class SearchViewModel : BaseEntity
    {
        private  string testName;
        private List<string> featureList = default(List<string>);
        private  string featureSelected = default(string);
        private  string interfaceSelected = default(string);
        private ObservableCollection<Interface> interfaceList = default(ObservableCollection<Interface>);
        private List<string> commandLineList = default(List<string>);
        private string executionMode = default(string);
        private string errorMessage = default(string);

        #region visibility
        private bool parameterVisibility = default(bool);
        private bool commandLineVisibility = default(bool);
        private bool interfaceGroupVisibility = default(bool);
        private bool featureListVisibility = default(bool);       
        #endregion

        public IView View { get; set; }
        private  Parameter parameterContents = default(Parameter);            
        public   Dictionary<string, string> parameterValue = default(Dictionary<string, string>);

        private string featureSelectedByWeb = default(String);        
        private string interfaceSelectedByWeb = default(String);
        
        public ICommand New { get; private set; }
        public ICommand Open { get; private set; }
        public ICommand InterfaceSelectedCommand { get; private set; }
        public ICommand AddCommand { get; private set; }
        public ICommand ExecutionModeCommand { get; private set; }
        public ICommand ExecuteCommand { get; private set; }
        public ICommand CommandLineDelete { get; private set; }
        public ICommand LogHyperLink { get; private set; }

        public SearchViewModel()
        {
            this.New = new DelegateCommand(
                new Action<object>(parameter =>
                {
                    DelegateCommand_New(parameter);              
                }));
            this.Open = new DelegateCommand(
                new Action<object>(parameter =>
                {
                    DelegateCommand_Open(parameter);                    
                }));
            this.InterfaceSelectedCommand = new DelegateCommand(
                new Action<object>(parameter =>
                    {
                        this.View.ClearParameterUiElementFromGrid();
                        DelegateCommand_InterfaceSelected(parameter);
                        this.View.AddParameterUiElementToGrid();
                        this.ErrorMessage = "";
                    }));
            this.AddCommand = new DelegateCommand(
                new Action<object>(parameter =>
                {
                    DelegateCommand_AddCommandLine(FeatureSelected,InterfaceSelected);
                    this.View.AddComboBoxItem();
                }));
            this.ExecutionModeCommand = new DelegateCommand(
                new Action<object>(parameter =>
                {
                    this.ExecutionMode = parameter.ToString();
                }));
            this.ExecuteCommand = new DelegateCommand(
                new Action<object>(parameter =>
                {
                    this.ErrorMessage = DelegateCommand_ExecuteTest(CommandLineList, TestName, ExecutionMode);                                                       
                }));
            this.CommandLineDelete = new DelegateCommand(
                new Action<object>(parameter =>
                {
                    this.View.DeleteCommandFromListBox();
                }));
            this.LogHyperLink = new DelegateCommand(
               new Action<object>(parameter =>
               {
                   DelegateCommand_LogHyperlink();
               }));
            commandLineList = new List<string>();
            
        }     
        #region ICommandImplementation
        private void DelegateCommand_New(object parameter)
        {
            var feature = DataProvider.GetFeatureList();
            this.FeatureList = new List<string>(feature);

            this.TestName = "";
            this.ErrorMessage = "";
            this.InterfaceList = new ObservableCollection<Interface>();
            this.View.ClearParameterUiElementFromGrid();
           // this.parameterContents = new Parameter();
           this.parameterValue = new Dictionary<string, string>();;
            this.CommandLineList = new List<string>();
            Parameter paramObj = new Parameter();
            paramObj.ParameterData = new Dictionary<string, List<string>>();
            this.ParameterContents = paramObj;
        }
        private void DelegateCommand_Open(object parameter)
        {
            if (this.FeatureList == null)
                DelegateCommand_New(parameter);
            else
            {
                this.TestName = "";
                this.ErrorMessage = "";
                this.InterfaceList = new ObservableCollection<Interface>();
                this.View.ClearParameterUiElementFromGrid();
               // this.parameterContents = new Parameter();
                parameterValue = new Dictionary<string, string>();
                this.CommandLineList = new List<string>();
                Parameter paramObj = new Parameter();
                paramObj.ParameterData = new Dictionary<string, List<string>>();
                this.ParameterContents = paramObj;
            }
            this.View.OpenBatchFile();
        }
        public void DelegateCommand_InterfaceSelected(object parameter)
        {
            this.InterfaceSelected = parameter as string;            
            List<string> parameterList = DataProvider.GetParameterList(this.InterfaceSelected);
            Dictionary<string, List<string>> temp = new Dictionary<string, List<string>>();
            for (int index = 0; index < parameterList.Count(); index++)
            {
                string curString = parameterList.ElementAt(index);
                List<String> paramArray = curString.Split(':').ToList();
                string paramName = paramArray.ElementAt(0);
                string paramLabel = paramArray.ElementAt(1) + ": ";
                List<string> enumValue = DataProvider.AddUiElement(paramName);
                if (enumValue == default(List<string>))
                {
                    temp.Add(paramLabel, enumValue);
                }
                else
                {
                    temp.Add(paramLabel, enumValue);
                }
            }
            parameterValue = new Dictionary<string, string>();

            Parameter paramObj = new Parameter();
            paramObj.ParameterData = new Dictionary<string, List<string>>();
            paramObj.ParameterData = temp;
            this.ParameterContents = paramObj;            
        }
        public bool DelegateCommand_AddCommandLine(string argFeatureName,string argInterfaceName)
        {
            if (argFeatureName != default(string) && argInterfaceName != default(string))
            {
                string command = DataProvider.GenerateCommandLine(parameterValue, argFeatureName, argInterfaceName);
                List<string> comLineList = this.CommandLineList;
                comLineList.Add(command);
                this.CommandLineList = new List<string>(comLineList);
                return true;
            }
            return false;
        }
        public string DelegateCommand_ExecuteTest(List<string> argCommandLienList,string argTestName,string argExecutionMode)
        {
            string message = "";
            if (argTestName == "")
                message = "Enter Test Name";
            else if (argCommandLienList.Count() == 0)
                message = "Command line does not contain any entry";
            else
            {
                message = DataProvider.ExecuteTest(CommandLineList, TestName, ExecutionMode);
            }
            return message;
        }
        public void DelegateCommand_LogHyperlink()
        {
            if (this.TestName != null)
            {
                String batchFileName = this.TestName.Split('.').First().Trim();
                String path = DataProvider.GetCurrentDirectory() + "\\" + batchFileName + ".html";
                if (File.Exists(path))
                    System.Diagnostics.Process.Start(path);
            }
        }
        public  bool UpdateParameterDictionary(string argParameter, string argParamValue)
        {
            if (parameterValue.ContainsKey(argParameter))
            {
                parameterValue[argParameter] = argParamValue;
                return true;
            }
            return false;
        }
        #endregion
        public string TestName
        {
            get { return testName; }
            set
            {
                testName = value;
                Notify("TestName");
                this.ErrorMessage = "";
            }
        }       
        public List<String> FeatureList
        {
            get { return this.featureList; }
            set
            {
                this.featureList = new List<string>();
                this.featureList = value;
                Notify("FeatureList");
                if (featureList.Count() > 0)
                    this.FeatureListVisibility = true;
                else
                    this.FeatureListVisibility = false;
            }
        }
        public string FeatureSelected
        {
            get { return featureSelected; }
            set
            {
                featureSelected = value;
                Notify("FeatureSelected");
                this.ErrorMessage = "";
                this.View.ClearParameterUiElementFromGrid();

                Parameter paramObj = new Parameter();
                paramObj.ParameterData = new Dictionary<string, List<string>>();
                this.ParameterContents = paramObj;
                List<string> featureData = DataProvider.GetInterfaceList(featureSelected);
                ObservableCollection<Interface> myList = new ObservableCollection<Interface>();
                for (int index = 0; index < featureData.Count(); index++)
                {
                    Interface obj = new Interface(featureData.ElementAt(index).ToString());
                    myList.Add(obj);
                }
                this.InterfaceList = myList;
            }
        }
        public string InterfaceSelected
        {
            get { return interfaceSelected; }
            set
            {
                interfaceSelected = value;
                Notify("InterfaceSelected");                
            }
        }

        public ObservableCollection<Interface> InterfaceList
        {
            get { return interfaceList; }
            set
            {
                interfaceList = value;
                Notify("InterfaceList");
                if (interfaceList.Count() > 0)
                    this.InterfaceGroupVisibility = true;
                else
                    this.InterfaceGroupVisibility = false;
            }
        }
        public List<string> CommandLineList
        {
            get { return commandLineList; }
            set
            {
                commandLineList = new List<string>();                
                    commandLineList = value;
                    if (commandLineList.Count() == 0)
                    {
                        this.View.ClearCommandLineListBox();
                        this.CommandLineVisibility = false;
                    }
                    else
                        this.CommandLineVisibility = true;
            }
        }
        public string ExecutionMode
        {
            get { return executionMode; }
            set
            {
                executionMode = value;
                Notify("ExecutionMode");              
            }
        }
        public string ErrorMessage
        {
            get { return errorMessage; }
            set { errorMessage = value;
            Notify("ErrorMessage");
            }
        }
        public bool ParameterVisibility
        {
            get { return parameterVisibility; }
            set { parameterVisibility = value;
            Notify("ParameterVisibility");
            }
        }
        public bool CommandLineVisibility
        {
            get { return commandLineVisibility; }
            set { commandLineVisibility = value;
            Notify("CommandLineVisibility");
            }
        }
        public Parameter ParameterContents
        {
            get { return parameterContents; }
            set { parameterContents = value;
            Notify("ParameterContents");
            if (parameterContents.ParameterData.Count()> 0)
                this.ParameterVisibility = true;
            else
                this.ParameterVisibility = false;
            }
        }
        public bool InterfaceGroupVisibility
        {
            get { return interfaceGroupVisibility; }
            set { interfaceGroupVisibility = value;
            Notify("InterfaceGroupVisibility");
            }
        }
        public bool FeatureListVisibility
        {
            get { return featureListVisibility; }
            set { featureListVisibility = value;
            Notify("FeatureListVisibility");
            }
        }
        public string FeatureSelectedByWeb
        {
            get { return featureSelectedByWeb; }
            set { featureSelectedByWeb = value; }
        }
        public string InterfaceSelectedByWeb
        {
            get { return interfaceSelectedByWeb; }
            set { interfaceSelectedByWeb = value; }
        }
    }
}



