namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    using Ranorex;
    using Ranorex.Core;

    public class ConfirmationPopup : FunctionalBase, ISet
    {
        private Dictionary<DecisionActions, Ranorex.Button> _buttonList = new Dictionary<DecisionActions, Ranorex.Button>();

        public ConfirmationPopup()
        {
            this._buttonList.Add(DecisionActions.No, ConfirmationPopupRepo.Instance.Form__IntelR_Graphics_and_Me.ButtonNo);
            this._buttonList.Add(DecisionActions.Yes, ConfirmationPopupRepo.Instance.Form__IntelR_Graphics_and_Me.ButtonYes);
        }
        public object Set
        {
            set
            {
                Log.Verbose("Setting {0}", value);
                this._buttonList[(DecisionActions)value].Press();
                Delay.Seconds(2);
            }
        }
    }
}
