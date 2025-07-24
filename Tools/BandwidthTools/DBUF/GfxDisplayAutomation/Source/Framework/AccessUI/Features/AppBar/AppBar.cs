namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    using Ranorex;

    public class AppBar : FunctionalBase, ISetMethod, IEnabledMethod
    {
        private Dictionary<AppBarOptions, Ranorex.Button> _buttonList = null;
        public Ranorex.Unknown List = null;

        public AppBar()
        {//TODO:: Refactor
            List = AppBarRepo.Instance.FormIntelR_Graphics_and_Medi.AppBarList;

            if (null == this._buttonList)
            {
                this._buttonList = new Dictionary<AppBarOptions, Ranorex.Button>();

                if (List.Children.Count > 1)
                {
                    this._buttonList.Add(AppBarOptions.Apply, AppBarRepo.Instance.FormIntelR_Graphics_and_Medi.ButtonApply);
                    this._buttonList.Add(AppBarOptions.Cancel, AppBarRepo.Instance.FormIntelR_Graphics_and_Medi.ButtonCancel);
                    if (List.Children.Count > 2)
                        this._buttonList.Add(AppBarOptions.RestoreDefault, AppBarRepo.Instance.FormIntelR_Graphics_and_Medi.ButtonRestore_Defaults);
                }
            }
        }
        public bool EnabledMethod(object argMessage)
        {
            bool isEnabled = this._buttonList[(AppBarOptions)argMessage].Enabled;
            Log.Verbose("Enabled status of {0} is {1}", argMessage, isEnabled);
            return isEnabled;
        }
        public bool SetMethod(object argMessage)
        {
            if (this._buttonList.ContainsKey((AppBarOptions)argMessage) && this.EnabledMethod(argMessage))
            {
                Log.Verbose("Setting {0}", argMessage);
                this._buttonList[(AppBarOptions)argMessage].Press();
                //Delay.Seconds(2);
                return true;
            }
            return false;
        }
    }
}