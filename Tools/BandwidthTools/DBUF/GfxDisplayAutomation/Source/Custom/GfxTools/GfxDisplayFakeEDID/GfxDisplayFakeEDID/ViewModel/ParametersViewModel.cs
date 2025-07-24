namespace Intel.VPG.Display.Automation
{
    public class ParametersViewModel : BaseEntity
    {
        private string _fakeEDIDFile = string.Empty;
        private string _displayPort = string.Empty;
        private string _fakeEDIDBlock = string.Empty;
        private SourceViewModel _parentViewMode = null;

        public ParametersViewModel(SourceViewModel argParentViewModel)
        {
            this._parentViewMode = argParentViewModel;
        }

        public string FakeEDIDBlock
        {
            get { return this._fakeEDIDBlock; }
            set
            {
                this._fakeEDIDBlock = value;
                base.Notify("FakeEDIDBlock");
            }
        }
        public string DisplayPort
        {
            get { return this._displayPort; }
            set
            {
                this._displayPort = value;
                base.Notify("DisplayPort");
            }
        }
        public string FakeEDIDFile
        {
            get { return this._fakeEDIDFile; }
            set
            {
                this._fakeEDIDFile = value;
                base.Notify("FakeEDIDFile");
            }
        }
    }
}