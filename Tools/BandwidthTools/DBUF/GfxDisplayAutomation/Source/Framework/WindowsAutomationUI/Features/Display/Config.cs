namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Threading;
    using System;
    using System.Collections.Generic;
    using System.Windows.Automation;

    class Config : FunctionalBase, ISet, IGet, IGetAll, IGetAllMethod
    {
        Dictionary<DisplayUnifiedConfig, AutomationElement> _options = new Dictionary<DisplayUnifiedConfig, AutomationElement>();
        private Dictionary<string, AutomationElement> _displayComboList = new Dictionary<string, AutomationElement>();
        List<string> stringList = new List<string>();
        private AutomationElement element, configComboBoxElement, horizontalVertElement, innerelement = null;
        private AutomationElementCollection elementColnPrimaryComboBox = null;
        private AutomationElement primaryElement, secondaryElement, tertiaryElement;
        int reTry = 0;
        private AutomationElementCollection elementColn = null;
        private AutomationElementCollection elementColnComboBox = null;
        private List<string> menuList = new List<string>();
        UIABaseHandler uiaBaseHandler = new UIABaseHandler();

        public Config()
        {
            Log.Verbose("In Config (Windows Automation UI)");
            configComboBoxElement = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.ComboBoxConfig].AutomationId, ControlType.ComboBox);
            if ((null == configComboBoxElement) || (this.configComboBoxElement.Current.IsOffscreen))
            {
                element = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.Config].AutomationId, ControlType.Custom);
                if (element != null)
                {
                    Condition condition = new AndCondition(new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.Custom),
                        new NotCondition(new PropertyCondition(AutomationElement.ClassNameProperty, "IntelLabelControl")));
                    elementColn = element.FindAll(TreeScope.Descendants, condition);
                    string text = "";
                    foreach (AutomationElement ele in elementColn)
                    {
                        innerelement = TreeWalker.ControlViewWalker.GetFirstChild(ele);
                        text = UIABaseHandler.Value(innerelement).Split(' ').First();
                        DisplayUnifiedConfig unifiedConfigOption;
                        if (Enum.TryParse(text, out unifiedConfigOption))
                            _options.Add(unifiedConfigOption, ele);
                    }
                }
            }
            else
            {
                elementColnComboBox = configComboBoxElement.FindAll(TreeScope.Children, new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.ListItem));
                string text = "";
                foreach (AutomationElement e in elementColnComboBox)
                {
                    text = e.Current.Name.Split(' ').First();
                    DisplayUnifiedConfig unifiedConfigOption;
                    if (Enum.TryParse(text, out unifiedConfigOption))
                        _options.Add(unifiedConfigOption, e);
                }
            }
            ControlType controlType = ControlType.ComboBox;
            while (primaryElement == null && secondaryElement == null && tertiaryElement == null && reTry < 3)
            {
                primaryElement = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.ChoosePrimaryDisplay].AutomationId, ControlType.ComboBox);
                secondaryElement = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.ChooseSecondaryDisplay].AutomationId, ControlType.ComboBox);
                tertiaryElement = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.ChooseTertiaryDisplay].AutomationId, ControlType.ComboBox);
                if (primaryElement == null) Log.Verbose("Failed to fetch the Feature,{0} at {1} attempt, Trying again", Features.ChoosePrimaryDisplay, ++reTry);
                if (secondaryElement == null) Log.Verbose("Failed to fetch the Feature,{0} at {1} attempt, Trying again", Features.ChooseSecondaryDisplay, ++reTry);
                if (tertiaryElement == null) Log.Verbose("Failed to fetch the Feature,{0} at {1} attempt, Trying again", Features.ChooseTertiaryDisplay, ++reTry);
                System.Threading.Thread.Sleep(1000);
                _displayComboList.Add("ComboBoxPrimary", primaryElement);
                _displayComboList.Add("ComboBoxSecondary", secondaryElement);
                _displayComboList.Add("ComboBoxTertiary", tertiaryElement);
            }
        }
        public Config(Features argFeature)
        {
            Log.Verbose("In Config(Features) (Windows Automation UI)");
            element = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.DisplayConfig].AutomationId, ControlType.Custom);
            if (element != null)
            {
                Condition condition = new AndCondition(new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.Custom),
                    new NotCondition(new PropertyCondition(AutomationElement.ClassNameProperty, "IntelLabelControl")));
                elementColn = element.FindAll(TreeScope.Descendants, condition);
                string text = "";
                foreach (AutomationElement ele in elementColn)
                {
                    innerelement = TreeWalker.ControlViewWalker.GetFirstChild(ele);
                    text = UIABaseHandler.Value(innerelement).Split(' ').First();
                    DisplayUnifiedConfig unifiedConfigOption;
                    if (Enum.TryParse(text, out unifiedConfigOption))
                        _options.Add(unifiedConfigOption, ele);
                }
            }
        }
        public object Get
        {
            get
            {
                DisplayConfig displayConfig = new DisplayConfig();
                DisplayType displayType = DisplayType.None;
                this._displayComboList.ToList().ForEach(kV =>
                {
                    if (!(kV.Value.Current.IsOffscreen))
                    {
                        SelectionPattern pattern = kV.Value.GetCurrentPattern(SelectionPattern.Pattern) as SelectionPattern;
                        string displayName = pattern.Current.GetSelection().First().Current.Name;
                        if (!(displayName.Equals("None")))
                        {
                            displayType = base.EnumeratedDisplays.Where(dI => !string.IsNullOrEmpty(dI.CompleteDisplayName) && dI.CompleteDisplayName.Equals(displayName)).Select(dI => dI.DisplayType).FirstOrDefault();
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

        public object GetAll
        {
            get
            {
                elementColnPrimaryComboBox = primaryElement.FindAll(TreeScope.Children, new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.ListItem));
                foreach (AutomationElement e in elementColnPrimaryComboBox)
                {
                    menuList.Add(e.Current.Name);
                }
                return menuList;
            }
        }
        public object GetAllMethod(object argMessage)
        {
            string returnList = argMessage as string;
            List<DisplayUnifiedConfig> configList = new List<DisplayUnifiedConfig>();
            if (returnList == "DisplayUnifiedConfigList")
            {
                if ((null == configComboBoxElement) || (this.configComboBoxElement.Current.IsOffscreen))
                {
                    string text = "";
                    foreach (AutomationElement e in elementColn)
                    {
                        innerelement = TreeWalker.ControlViewWalker.GetFirstChild(e);
                        text = UIABaseHandler.Value(innerelement).Split(' ').First();
                        DisplayUnifiedConfig unifiedConfigOption;
                        if (Enum.TryParse(text, out unifiedConfigOption))
                            configList.Add(unifiedConfigOption);

                    }
                    return configList;
                }
                else
                {
                    string text = "";
                    foreach (AutomationElement e in elementColnComboBox)
                    {
                        text = e.Current.Name.Split(' ').First();
                        DisplayUnifiedConfig unifiedConfigOption;
                        if (Enum.TryParse(text, out unifiedConfigOption))
                            configList.Add(unifiedConfigOption);
                    }
                    return configList;
                }
            }
            else
            {
                elementColnPrimaryComboBox = primaryElement.FindAll(TreeScope.Children, new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.ListItem));
                foreach (AutomationElement e in elementColnPrimaryComboBox)
                {
                    menuList.Add(e.Current.Name);
                }
                return menuList;
            }
        }
        public object Set
        {
            set
            {
                DisplayConfig displayConfig = value as DisplayConfig;
                Log.Message("Config to be set via CUI {0}", displayConfig.GetCurrentConfigStr());
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
                    EnableCollage enableCollage = new EnableCollage(Features.EnableDisableCollage);
                    enableCollage.Set = CollageOptions.Enable;
                    this.SetCollageType(displayConfig.ConfigType);
                }
                int idx = 0;
                string actualDisplayName;
                this._displayComboList.ToList().ForEach(kV =>
                {
                    if (!(kV.Value.Current.IsOffscreen))
                    {
                        if (idx < displayConfig.CustomDisplayList.Count)
                            actualDisplayName = base.EnumeratedDisplays.Where(dI => dI.DisplayType == displayConfig.CustomDisplayList[idx]).Select(dI => dI.CompleteDisplayName).FirstOrDefault();
                        else
                            actualDisplayName = DisplayInfoCollection.Collection.Where(dI => dI.DisplayType == DisplayType.None).Select(dI => dI.DisplayName).FirstOrDefault();

                        Log.Verbose("Setting {0} to {1}", actualDisplayName, kV.Key);
                        ExpandCollapsePattern exPattern = kV.Value.GetCurrentPattern(ExpandCollapsePattern.Pattern) as ExpandCollapsePattern;
                        exPattern.Expand();
                        System.Threading.Thread.Sleep(300);
                        elementColn = kV.Value.FindAll(TreeScope.Children, new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.ListItem));
                        foreach (AutomationElement e in elementColn)
                        {
                            if (e.Current.Name.ToString().Equals(actualDisplayName))
                            {
                                innerelement = e;
                                break;
                            }
                        }
                        uiaBaseHandler.SelectionItem(innerelement);
                        exPattern.Collapse();
                    }
                    idx++;
                });
                Thread.Sleep(3000);
            }
        }
        private DisplayUnifiedConfig GetDisplayUnifiedConfig()
        {
            string text = "";
            if ((null == configComboBoxElement) || (this.configComboBoxElement.Current.IsOffscreen))
            {
                foreach (AutomationElement e in elementColn)
                {
                    if (e.Current.ItemStatus == "Selected")
                    {
                        innerelement = TreeWalker.ControlViewWalker.GetFirstChild(e);
                        text = UIABaseHandler.Value(innerelement).Split(' ').First();
                        DisplayUnifiedConfig unifiedConfigOption;
                        if (Enum.TryParse(text, out unifiedConfigOption))
                            return unifiedConfigOption;
                    }
                }
            }
            else
            {
                SelectionPattern pattern = configComboBoxElement.GetCurrentPattern(SelectionPattern.Pattern) as SelectionPattern;
                text = pattern.Current.GetSelection().First().Current.Name.Split(' ').First();
                DisplayUnifiedConfig unifiedConfigOption;
                if (Enum.TryParse(text, out unifiedConfigOption))
                    return unifiedConfigOption;
            }
            return default(DisplayUnifiedConfig);
        }
        internal void SetConfigType(DisplayUnifiedConfig argUnifiedConfigType)
        {
            if ((null == configComboBoxElement) || (this.configComboBoxElement.Current.IsOffscreen))
            {
                if (_options.ContainsKey(argUnifiedConfigType))
                {
                    uiaBaseHandler.SendKey(_options[argUnifiedConfigType]);
                    Thread.Sleep(10000);
                }
                else
                    Log.Abort("Collage option not present in CUI");
            }
            else
            {
                bool collageFlag = false;
                ExpandCollapsePattern exPattern = configComboBoxElement.GetCurrentPattern(ExpandCollapsePattern.Pattern) as ExpandCollapsePattern;
                exPattern.Expand();
                System.Threading.Thread.Sleep(300);
                elementColnComboBox = configComboBoxElement.FindAll(TreeScope.Children, new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.ListItem));
                foreach (AutomationElement e in elementColnComboBox)
                {
                    if (e.Current.Name.ToString().Contains(argUnifiedConfigType.ToString()))
                    {
                        innerelement = e;
                        collageFlag = true;
                        break;
                    }
                }
                if (collageFlag)
                {
                    uiaBaseHandler.SelectionItem(innerelement);
                    exPattern.Collapse();
                }
                else
                    Log.Abort("Collage option not present in CUI");
                collageFlag = false;
            }
        }
        private void SetCollageType(DisplayConfigType argConfigType)
        {
            horizontalVertElement = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.HorizontalVerticalCollage].AutomationId, ControlType.Custom);
            if (horizontalVertElement != null)
            {
                Condition condition = new AndCondition(new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.Custom),
                    new NotCondition(new PropertyCondition(AutomationElement.ClassNameProperty, "IntelLabelControl")));
                elementColn = horizontalVertElement.FindAll(TreeScope.Descendants, condition);
                string text = "";
                foreach (AutomationElement ele in elementColn)
                {
                    innerelement = TreeWalker.ControlViewWalker.GetFirstChild(ele);
                    text = UIABaseHandler.Value(innerelement);
                    if (text.Contains(argConfigType.ToString()))
                        uiaBaseHandler.SendKey(ele);
                }
            }
        }
        private DisplayConfigType GetCollageType()
        {
            horizontalVertElement = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.HorizontalVerticalCollage].AutomationId, ControlType.Custom);
            if (horizontalVertElement != null)
            {
                Condition condition = new AndCondition(new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.Custom),
                    new NotCondition(new PropertyCondition(AutomationElement.ClassNameProperty, "IntelLabelControl")));
                elementColn = horizontalVertElement.FindAll(TreeScope.Descendants, condition);
                string text = "";
                foreach (AutomationElement e in elementColn)
                {

                    if (e.Current.ItemStatus == "Selected")
                    {
                        innerelement = TreeWalker.ControlViewWalker.GetFirstChild(e);
                        break;
                    }
                }
                string text1 = UIABaseHandler.Value(innerelement);
                text = text1.Substring(0, text1.Length - 2);
                DisplayConfigType displayConfigType;
                if (Enum.TryParse(text, out displayConfigType))
                    return displayConfigType;
                else
                    return DisplayConfigType.None;
            }
            return DisplayConfigType.None;
        }
    }
}


