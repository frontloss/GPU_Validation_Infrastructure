namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;

    public class DTCMHelper
    {
        private DTCMAccess _accessMode;
        private Dictionary<DTCMAccess, List<System.Action>> _dtcmActions = null;
        private IApplicationManager _manager = null;
        private Action _dtcmAction = Action.GetAll;

        public DTCMHelper(IApplicationManager argManager, DTCMAccess argAccessMode)
        {
            this._manager = argManager;
            this._accessMode = argAccessMode;
        }
        public Action GetAction
        {
            set { this._dtcmAction = value; }
        }
        public bool IsFeatureVisible(Features argFeature)
        {
            List<string> navList = argFeature.GetNavigationList().Values.Select(i => i.Replace("_", " ")).ToList();
            this.PerformDTCMAction(0);
            bool exists = AccessInterface.GetFeature<bool, string, List<string>>(Features.DTCMFeature, Action.VisibleMethod, Source.Default, navList.Last(), navList.Take(navList.Count - 1).ToList());
            this.PerformDTCMAction(1);
            return exists;
        }
        public R GetDTCMAction<R>(Features argFeature)
        {
            Log.Verbose("Preparing Navigation List for {0}", argFeature);
            List<string> navList = argFeature.GetNavigationList().Values.Select(i => i.Replace("_", " ")).ToList();
            this.PerformDTCMAction(0);
            R result = AccessInterface.GetFeature<R, List<string>>(Features.DTCMFeature, this._dtcmAction, navList);
            this.PerformDTCMAction(1);
            return result;
        }
        public void SetDTCMAction<V>(Features argFeature, V argValue)
        {
            Log.Verbose("Preparing Navigation List for {0}", argFeature);
            List<string> navList = argFeature.GetNavigationList().Values.Select(i => i.Replace("_", " ")).ToList();
            this.PerformDTCMAction(0);
            AccessInterface.SetFeature<V, List<string>>(Features.DTCMFeature, Action.Set, argValue, navList);
            this.PerformDTCMAction(1);
        }

        private void PerformDTCMAction(int argOrder)
        {
            System.Action action = this.DTCMActions[this._accessMode][argOrder];
            if (null != action)
                action();
        }
        private void ShowTrayIcon()
        {
            AccessInterface.SetFeature(Features.DTCMTrayIcon, Action.Set, "DTCM");
        }
        private void ShowDTCMDesktop()
        {
            AccessInterface.SetFeature(Features.DTCMShowDesktop, Action.Set, "DTCM");
        }
        private void RestoreDTCMDesktop()
        {
            AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Restore);
        }
        private Dictionary<DTCMAccess, List<System.Action>> DTCMActions
        {
            get
            {
                if (null == this._dtcmActions)
                {
                    this._dtcmActions = new Dictionary<DTCMAccess, List<System.Action>>();
                    this._dtcmActions.Add(DTCMAccess.Desktop, new List<System.Action>() { this.ShowDTCMDesktop, this.RestoreDTCMDesktop });
                    this._dtcmActions.Add(DTCMAccess.Tray, new List<System.Action>() { this.ShowTrayIcon, this.RestoreDTCMDesktop });
                }
                return this._dtcmActions;
            }
        }
        private IAccessInterface AccessInterface
        {
            get { return this._manager.AccessInterface; }
        }
    }
}
