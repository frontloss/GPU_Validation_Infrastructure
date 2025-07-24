namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;

    using Ranorex;

    public class SetDisplayFullName : FunctionalBase, ISetNoArgs
    {
        public bool SetNoArgs()
        {
            ComboBox combo = ChooseActiveDisplaysRepo.Instance.FormIntelR_Graphics_and_Medi.ComboBoxComboBoxPrimary;
            if (combo.Visible)
            {
                List<string> dispNames = combo.Items.Select(lI => lI.Text).ToList();
                PrepareMultipleDisplayTypes(DisplayType.HDMI, dispNames);
                PrepareMultipleDisplayTypes(DisplayType.DP, dispNames);
                PrepareMultipleDisplayTypes(DisplayType.EDP, dispNames);
                PrepareMultipleDisplayTypes(DisplayType.CRT, dispNames);
                return true;
            }
            return false;
        }

        private void PrepareMultipleDisplayTypes(DisplayType argDisplayType, List<string> argAllDisplaysList)
        {
            string dispTypeText = DisplayInfoCollection.Collection.Where(dI => dI.DisplayType == argDisplayType).Select(dI => dI.DisplayName).FirstOrDefault();
            List<string> multipleDisplayTypes = argAllDisplaysList.Where(dStr => dStr.Contains(dispTypeText)).Select(dStr => dStr).ToList();
            DisplayInfo displayInfo = null;
            string dispTypeConcatText = string.Empty;
            for (int idx = multipleDisplayTypes.Count; idx > 0; idx--)
            {
                dispTypeConcatText = idx.Equals(1) ? dispTypeText : string.Concat(dispTypeText, " ", idx);
                Log.Verbose("Identifying full display name for {0}", dispTypeConcatText);
                if (multipleDisplayTypes[idx - 1].StartsWith(dispTypeConcatText))
                {
                    displayInfo = DisplayInfoCollection.Collection.Where(dI => dI.DisplayName.Equals(dispTypeConcatText)).FirstOrDefault();
                    displayInfo.CompleteDisplayName = multipleDisplayTypes[idx - 1];
                    multipleDisplayTypes.RemoveAt(idx - 1);
                }
            }
        }
    }
}