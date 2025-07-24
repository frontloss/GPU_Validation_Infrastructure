namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Threading.Tasks;
    using System.Collections.Generic;
    using System.Collections.ObjectModel;

    public class SourceViewModel : BaseEntity
    {
        private ParametersViewModel _parametersVM = null;
        private CommandsViewModel _commandsVM = null;
        private ObservableCollection<string> _enumeratedDisplays = null;

        internal string _defaultOption = "(None)";
        internal List<DisplayInfo> DisplayInfoList { get; set; }

        public SourceViewModel()
        {
            this.ReSyncEnumeratedDisplays();
        }

        internal void ReSyncEnumeratedDisplays()
        {
            this.EnumeratedDisplays = new ObservableCollection<string>() { "(Loading...)" };
            Task.Factory.StartNew(() =>
            {
                this.DisplayInfoList = DisplayActions.EnumerateAllDisplays();
                this.EnumeratedDisplays = new ObservableCollection<string>(this.DisplayInfoList.Select(dI => string.Format("{0} ({1}) - {2} ({3})", dI.CompleteDisplayName, dI.ActiveStatus, dI.Port, dI.PortValue)).ToList());
                this.EnumeratedDisplays.Insert(0, _defaultOption);
                this.View.SetEnumeratedDisplayToDefault();
            });
        }

        public ObservableCollection<string> EnumeratedDisplays
        {
            get { return this._enumeratedDisplays; }
            set
            {
                this._enumeratedDisplays = value;
                base.Notify("EnumeratedDisplays");
            }
        }
        public List<string> EDIDBlockList
        {
            get { return new List<string>() { _defaultOption, "Base", "CEA Extension", "Both" }; }
        }
        public List<string> FakeEDIDRegKeyList
        {
            get
            {
                List<string> fakeEDIDRegKeyList = this.CommandsVM.FakeEDIDRegKeyList;
                fakeEDIDRegKeyList.Insert(0, _defaultOption);
                return fakeEDIDRegKeyList;
            }
        }
        public List<string> ReadEDIDRegKeyList
        {
            get
            {
                List<string> readEDIDRegKeyList = this.CommandsVM.ReadEDIDRegKeyList;
                readEDIDRegKeyList.Insert(0, _defaultOption);
                return readEDIDRegKeyList;
            }
        }

        public ParametersViewModel ParametersVM
        {
            get { if (null == this._parametersVM) this._parametersVM = new ParametersViewModel(this); return this._parametersVM; }
        }
        public CommandsViewModel CommandsVM
        {
            get { if (null == this._commandsVM) this._commandsVM = new CommandsViewModel(this); return this._commandsVM; }
        }
        public IView View { get; set; }
    }
}
