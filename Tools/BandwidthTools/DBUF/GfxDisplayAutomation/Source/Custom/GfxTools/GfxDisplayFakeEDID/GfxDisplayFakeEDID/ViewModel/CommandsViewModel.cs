namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Windows.Input;
    using System.Collections.Generic;

    public class CommandsViewModel : BaseEntity
    {
        private string _actionMessage = string.Empty;
        private string _fakeEDIDRegKey = string.Empty;
        private string _readEDIDRegKey = string.Empty;
        private SourceViewModel _parentViewMode = null;

        public ICommand ReSyncDisplays { get; private set; }
        public ICommand SelectFile { get; private set; }
        public ICommand ResetScreen { get; private set; }
        public ICommand RebootSystem { get; private set; }

        public CommandsViewModel(SourceViewModel argParentViewModel)
        {
            this._parentViewMode = argParentViewModel;
            this.BootstrapCommands();
        }

        public string FakeEDIDRegKey
        {
            get { return this._fakeEDIDRegKey; }
            set
            {
                this._fakeEDIDRegKey = value;
                base.Notify("FakeEDIDRegKey");
                this.FakeEDIDRegistryActionHandler();
            }
        }
        public string ReadEDIDRegKey
        {
            get { return this._readEDIDRegKey; }
            set
            {
                this._readEDIDRegKey = value;
                base.Notify("ReadEDIDRegKey");
                this.ReadEDIDRegistryActionHandler();
            }
        }
        public string ActionMessage
        {
            get { return this._actionMessage; }
            set
            {
                this._actionMessage = value;
                base.Notify("ActionMessage");
            }
        }

        internal List<string> FakeEDIDRegKeyList
        {
            get { return RegistryActions.ActionList.Keys.Take(3).ToList(); }
        }
        internal List<string> ReadEDIDRegKeyList
        {
            get { return RegistryActions.ActionList.Keys.Skip(3).ToList(); }
        }

        private void BootstrapCommands()
        {
            this.ReSyncDisplays = new Command(() => this._parentViewMode.ReSyncEnumeratedDisplays());
            this.SelectFile = new Command(() => this._parentViewMode.ParametersVM.FakeEDIDFile = CommandActions.SelectFakeEDIDFile());
            this.RebootSystem = new Command(() => this.HandleCommandResult(CommandActions.RebootSystem()));
            this.ResetScreen = new Command(() => this.ResetCommandHandler());
        }
        private void FakeEDIDRegistryActionHandler()
        {
            if (!this.FakeEDIDRegKey.Equals(this._parentViewMode._defaultOption))
            {
                CommandResult commandResult = null;
                RegistryParams regParam = new RegistryParams() { RegistryOption = this.FakeEDIDRegKey };

                if (regParam.RegistryOption.Equals(this.FakeEDIDRegKeyList.Last()))
                    commandResult = CommandActions.PerformRegistryAction(regParam);
                else
                {
                    regParam.FakeEDIDBlock = this._parentViewMode.ParametersVM.FakeEDIDBlock;
                    regParam.FakeEDIDFile = this._parentViewMode.ParametersVM.FakeEDIDFile;
                    string displayPort = this._parentViewMode.ParametersVM.DisplayPort;
                    if (!string.IsNullOrEmpty(regParam.FakeEDIDBlock) && !string.IsNullOrEmpty(regParam.FakeEDIDFile) && !string.IsNullOrEmpty(displayPort))
                    {
                        displayPort = displayPort.Substring(displayPort.LastIndexOf("(") + 1);
                        regParam.PortValue = Convert.ToInt32(displayPort.Split(')').First());
                        regParam.DisplayInfo = this._parentViewMode.DisplayInfoList.Where(dI => dI.PortValue.Equals(regParam.PortValue)).FirstOrDefault();
                        commandResult = CommandActions.PerformRegistryAction(regParam);
                    }
                    else
                        commandResult = new CommandResult() { MessageFormatType = Automation.MessageFormatType.Warning, Result = "Required parameters for adding FakeEDID is not set on screen!" };
                }
                this.HandleCommandResult(commandResult);
            }
        }
        private void ReadEDIDRegistryActionHandler()
        {
            if (!this.ReadEDIDRegKey.Equals(this._parentViewMode._defaultOption))
                this.HandleCommandResult(CommandActions.PerformRegistryAction(new RegistryParams() { RegistryOption = this.ReadEDIDRegKey }));
        }
        private void HandleCommandResult(CommandResult argResult)
        {
            this.ActionMessage = argResult.Result;
            this._parentViewMode.View.FormatActionMessage(argResult.MessageFormatType);
        }
        private void ResetCommandHandler()
        {
            this._parentViewMode.ParametersVM.FakeEDIDFile = string.Empty;
            this.ActionMessage = string.Empty;
            this._parentViewMode.View.ResetControls();
        }
    }
}