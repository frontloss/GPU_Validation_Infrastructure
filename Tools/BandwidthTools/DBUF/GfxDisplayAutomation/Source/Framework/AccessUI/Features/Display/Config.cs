namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Threading;
    using System;
    using System.Collections.Generic;

    using Ranorex;

    class Config : FunctionalBase, IGet, ISet, IGetAll, IGetAllMethod
    {
        Dictionary<DisplayUnifiedConfig, Ranorex.Unknown> _options = new Dictionary<DisplayUnifiedConfig, Ranorex.Unknown>();
        private ComboBox _comboBox = null;
        private Dictionary<string, ComboBox> _displayComboList = new Dictionary<string, ComboBox>();
        private List<Ranorex.Unknown> _configTextlst = null;
        List<string> stringList = new List<string>();
        private List<Ranorex.Unknown> _horizontalVertical = null;

        public Config()
            : base()
        {
            this._comboBox = MultipleDisplaysRepo.Instance.FormIntelR_Graphics_and_Medi.ComboBoxComboBoxSelectOpMode;
            if ((null == _comboBox) || (!this._comboBox.Visible))
                //if (!this._comboBox.Visible)
                this._configTextlst = MultipleDisplaysRepo.Instance.FormIntelR_Graphics_and_Medi.ModeItemList.FindChildren<Ranorex.Unknown>().ToList();

            this._displayComboList.Add("ComboBoxPrimary", ChooseActiveDisplaysRepo.Instance.FormIntelR_Graphics_and_Medi.ComboBoxComboBoxPrimary);
            this._displayComboList.Add("ComboBoxSecondary", ChooseActiveDisplaysRepo.Instance.FormIntelR_Graphics_and_Medi.ComboBoxComboBoxSecondary);
            this._displayComboList.Add("ComboBoxThird", ChooseActiveDisplaysRepo.Instance.FormIntelR_Graphics_and_Medi.ComboBoxComboBoxThird);
        }
        public object GetAll
        {
            get { return ChooseActiveDisplaysRepo.Instance.FormIntelR_Graphics_and_Medi.ComboBoxComboBoxPrimary.Items.Select(lI => lI.Text).ToList(); }
        }
        public object GetAllMethod(object argMessage)
        {
            string returnList = argMessage as string;

            if (returnList == "DisplayUnifiedConfigList")
            {
                List<DisplayUnifiedConfig> configList = new List<DisplayUnifiedConfig>();
                if ((null != _comboBox) && (this._comboBox.Visible))
                {
                    DisplayUnifiedConfig displayUnifiedType;
                    stringList = _comboBox.Items.Select(lI => lI.Text).ToList();
                    foreach (string displayConfigType in stringList)
                        if (Enum.TryParse<DisplayUnifiedConfig>(displayConfigType, out displayUnifiedType))
                            configList.Add(displayUnifiedType);
                    return configList;
                }
                else
                {
                    for (int idx = 0; idx < this._configTextlst.Count; idx++)
                        configList.Add((DisplayUnifiedConfig)(idx + 1));
                    return configList;
                }
            }
            else
                return ChooseActiveDisplaysRepo.Instance.FormIntelR_Graphics_and_Medi.ComboBoxComboBoxPrimary.Items.Select(lI => lI.Text).ToList();
        }

        public object Get
        {
            get
            {
                DisplayConfig displayConfig = new DisplayConfig();
                DisplayType displayType = DisplayType.None;
                this._displayComboList.ToList().ForEach(kV =>
                {
                    if (kV.Value.Visible)
                    {
                        displayType = base.EnumeratedDisplays.Where(dI => !string.IsNullOrEmpty(dI.CompleteDisplayName) && dI.CompleteDisplayName.Equals(kV.Value.SelectedItemText)).Select(dI => dI.DisplayType).FirstOrDefault();
                        if (displayType != DisplayType.None)
                        {
                            Log.Verbose("Found {0} in {1}", displayType, kV.Key);
                            if (null == displayConfig.DisplayList)
                                displayConfig.DisplayList = new List<DisplayType>();
                            displayConfig.DisplayList.Add(displayType);
                        }
                    }
                });
                displayConfig.PrimaryDisplay = displayConfig.DisplayList.GetDisplay(DisplayHierarchy.Display_1);
                displayConfig.SecondaryDisplay = displayConfig.DisplayList.GetDisplay(DisplayHierarchy.Display_2);
                displayConfig.TertiaryDisplay = displayConfig.DisplayList.GetDisplay(DisplayHierarchy.Display_3);

                DisplayUnifiedConfig unifiedConfigType = this.GetDisplayUnifiedConfig();
                if (unifiedConfigType != DisplayUnifiedConfig.Collage)
                    displayConfig.ConfigType = unifiedConfigType.GetConfigType(displayConfig.DisplayList.Count);
                else
                    displayConfig.ConfigType = GetCollageType();
                Log.Verbose("Config type is {0}~{1}", unifiedConfigType, displayConfig.ConfigType);

                return displayConfig;
            }
        }
        public object Set
        {
            set
            {
                DisplayConfig displayConfig = value as DisplayConfig;
                Log.Message(true, "Config to be set via CUI {0}", displayConfig.GetCurrentConfigStr());
                DisplayUnifiedConfig unifiedConfigType = DisplayExtensions.GetUnifiedConfig(displayConfig.ConfigType);
                DisplayUnifiedConfig assertUnifiedConfigType = this.GetDisplayUnifiedConfig();
                if (unifiedConfigType != assertUnifiedConfigType)
                {
                    this.SetConfigType(unifiedConfigType);
                    assertUnifiedConfigType = this.GetDisplayUnifiedConfig();
                    if (unifiedConfigType != assertUnifiedConfigType)
                    {
                        Log.Alert("Config type not set! Expected {0}~{1} but was {2}", unifiedConfigType, displayConfig.ConfigType, assertUnifiedConfigType);
                        this.SetConfigType(unifiedConfigType);
                    }
                }
                if (unifiedConfigType == DisplayUnifiedConfig.Collage)
                {
                    EnableCollage enableCollage = new EnableCollage();
                    enableCollage.Set = CollageOptions.Enable;
                    this.SetCollageType(displayConfig.ConfigType);
                }
                string actualDisplayName = string.Empty;
                int idx = 0;
                foreach (KeyValuePair<string, ComboBox> kV in this._displayComboList)
                {
                    if (kV.Value.Visible)
                    {
                        if (idx < displayConfig.CustomDisplayList.Count)
                            actualDisplayName = base.EnumeratedDisplays.Where(dI => dI.DisplayType == displayConfig.CustomDisplayList[idx]).Select(dI => dI.CompleteDisplayName).FirstOrDefault();
                        else
                            actualDisplayName = DisplayInfoCollection.Collection.Where(dI => dI.DisplayType == DisplayType.None).Select(dI => dI.DisplayName).FirstOrDefault();

                        Log.Verbose("Setting {0} to {1}", actualDisplayName, kV.Key);
                        kV.Value.SelectedItemIndex = kV.Value.Items.Where(lI => lI.Text.Equals(actualDisplayName)).First().Index;
                    }
                    idx++;
                }
                Thread.Sleep(3000);
            }
        }

        private DisplayUnifiedConfig GetDisplayUnifiedConfig()
        {
            if ((null != _comboBox) && (this._comboBox.Visible))
                return ((DisplayUnifiedConfig)(this._comboBox.SelectedItemIndex + 1));
            else
            {
                for (int idx = 0; idx < this._configTextlst.Count; idx++)
                    if (null != this._configTextlst[idx].Element.GetAttributeValue("ItemStatus"))
                        return ((DisplayUnifiedConfig)(idx + 1));
            }
            return default(DisplayUnifiedConfig);
        }
        internal void SetConfigType(DisplayUnifiedConfig argUnifiedConfigType)
        {
            int configTypeIdx = ((int)argUnifiedConfigType) - 1;
            if ((null != _comboBox) && (this._comboBox.Visible))
            {
                Log.Verbose("Setting {0} via combobox", argUnifiedConfigType);
                this._comboBox.SelectedItemIndex = configTypeIdx;
                Thread.Sleep(10000);
            }
            else
            {
                Log.Verbose("Setting {0} via config Text", argUnifiedConfigType);
                this._configTextlst[configTypeIdx].FocusEnter();
                Thread.Sleep(10000);
            }
            Thread.Sleep(10000);
        }
        private void SetCollageType(DisplayConfigType argConfigType)
        {
            int collageTypeIdx = ((int)argConfigType) - (int)DisplayConfigType.Horizontal;
            ChooseActiveDisplaysRepo.Instance.FormIntelR_Graphics_and_Medi.CollageSelectDisplayOrientation.Children[collageTypeIdx].FocusEnter();
            Delay.Seconds(5);
        }
        private DisplayConfigType GetCollageType()
        {
            this._horizontalVertical = ChooseActiveDisplaysRepo.Instance.FormIntelR_Graphics_and_Medi.CollageSelectDisplayOrientation.FindChildren<Ranorex.Unknown>().ToList();
            for (int idx = 0; idx < this._horizontalVertical.Count; idx++)
                if (null != this._horizontalVertical[idx].Element.GetAttributeValue("ItemStatus"))
                    return ((DisplayConfigType)(idx + (int)DisplayConfigType.Horizontal));
            return DisplayConfigType.None;

        }
    }
}