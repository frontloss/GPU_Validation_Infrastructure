namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Threading;
    using System.Collections.Generic;
    using Ranorex;

    public class SelectDisplay : FunctionalBase, ISet, IGet
    {
        protected ComboBox _comboBox = null;
        private int _retryIdx = 0;

        public SelectDisplay()
            : base()
        {
            this._comboBox = DisplaySettingsRepo.Instance.FormIntelR_Graphics_and_Medi.ComboBoxComboBoxChooseDisplay;
        }

        public SelectDisplay(ComboBox argsCmboBx)
            : base()
        {
            this._comboBox = argsCmboBx;
        }

        public object Set
        {
            set
            {
                DisplayType displayType = (DisplayType)value;
                string actualDisplayName = base.EnumeratedDisplays.Where(dI => dI.DisplayType == displayType).Select(dI => dI.CompleteDisplayName).FirstOrDefault();
                Log.Verbose("ComboBoxChooseDisplay:: Setting to {0}", actualDisplayName);
                this._comboBox.SelectedItemIndex = this._comboBox.Items.Where(lI => lI.Text.Equals(actualDisplayName)).First().Index;
                Thread.Sleep(1500);
                if (this._retryIdx.Equals(0) && displayType != GetDisplayType())
                {
                    Log.Sporadic(true, "SelectDisplay not set! Trying again");
                    this._retryIdx++;

                    List<INavigate> retryNavList = new List<INavigate>()
                    {
                        new Home(),
                        new DisplayTile(),
                        new SubMenuDisplaySettings()
                    };
                    retryNavList.ForEach(iN => iN.Navigate());
                    this.Set = displayType;
                }
            }
        }
        public virtual object Get
        {
            get { return GetDisplayType(); }
        }

        private DisplayType GetDisplayType()
        {
            return base.EnumeratedDisplays.Where(dI => !string.IsNullOrEmpty(dI.CompleteDisplayName) && dI.CompleteDisplayName.Equals(this._comboBox.SelectedItemText)).Select(dI => dI.DisplayType).FirstOrDefault();
        }
    }
}