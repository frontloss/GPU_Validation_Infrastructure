namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;

    public class XvyccYcbcr :FunctionalBase, ISet, IGet, IGetMethod
    {
        private List<Ranorex.Unknown> _enableDisable = null;
        public XvyccYcbcr()
        {
            DisplayTabsRepo.Instance.IntelRHDGraphicsControlPanel.Color.FocusEnter();
            XvyccYcbcrRepo.Instance.IntelRHDGraphicsControlPanel.DisplayMainPage.BasicAdvOptions.Children[1].FocusEnter();
            this._enableDisable = XvyccYcbcrRepo.Instance.IntelRHDGraphicsControlPanel.DisplayMainPage.ColorimetryControl.FindChildren<Ranorex.Unknown>().ToList();
        }
        public object GetMethod(object argMessage)
        {
            if (!(_enableDisable.Count == 0))
                return PanelType.XVYCC_YCBCR;
            else
                return PanelType.RGB;
        }
        public object Get
        {
            get 
            {
                for (int idx = 0; idx < this._enableDisable.Count; idx++)
                    if (null != this._enableDisable[idx].Element.GetAttributeValue("ItemStatus"))
                        return ((DecisionActions)(idx - 1));
                return default(DecisionActions);
            }
        }
        public object Set
        {
            set
            {
                int valuee = (int)Enum.Parse(typeof(DecisionActions), value.ToString());
                this._enableDisable[(int)Enum.Parse(typeof(DecisionActions), value.ToString()) + 1].FocusEnter();
            }
        }
    }
}
