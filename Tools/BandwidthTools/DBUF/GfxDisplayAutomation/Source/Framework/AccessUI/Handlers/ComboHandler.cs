namespace Intel.VPG.Display.Automation
{
    using System.Linq;

    public class ComboHandler : FunctionalBase
    {
        private Ranorex.ComboBox _comboBox = null;
        private string _comboName = string.Empty;

        public ComboHandler(Ranorex.ComboBox argCombo, string argComboName)
        {
            this._comboBox = argCombo;
            this._comboName = argComboName;
        }
        public object Get
        {
            get 
            {
                Log.Verbose("Getting SelectedItemText of ComboBox:: {0}", this._comboName);
                return this._comboBox.SelectedItemText; 
            }
        }
        public object Set
        {
            set
            {
                if (this.Visible)
                {
                    Log.Verbose("Setting ComboBox:: {0} to {1}", this._comboName, value);
                    int dispValLen = value.ToString().Length;
                    this._comboBox.SelectedItemIndex = this._comboBox.Items.Where(i => i.Text.Length >= dispValLen).First(i => i.Text.Substring(0, dispValLen).Equals(value.ToString())).Index;
                }
            }
        }
        public object GetAll
        {
            get
            {
                Log.Verbose("Getting all items of ComboBox:: {0}", this._comboName);
                return this._comboBox.Items.Select(i => i.Text).ToList();
            }
        }
        public bool IsEnabled
        {
            get
            {
                Log.Verbose("Getting Enabled of ComboBox:: {0}", this._comboName);
                return this._comboBox.Enabled; 
            }
        }
        public bool Visible
        {
            get
            {
                Log.Verbose("Getting Visible of ComboBox:: {0}", this._comboName);
                return this._comboBox.Visible; 
            }
        }
    }
}