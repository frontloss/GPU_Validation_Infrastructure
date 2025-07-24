namespace Intel.VPG.Display.Automation
{
    using Ranorex;
    using Ranorex.Core;

    class NotificationAreaIcons : FunctionalBase, ISetMethod
    {
        public bool SetMethod(object argMessage)
        {
            Log.Verbose("Launching Notification Area Icons Control Panel");
            CommonExtensions.StartProcess("control", " /name Microsoft.NotificationAreaIcons");
            if (!ControlPanelRepo.Instance.FormControl_Panel.CheckBoxAlways_show_all_icons_an.Checked)
            {
                Log.Verbose("Enabling Show All Icons");
                ControlPanelRepo.Instance.FormControl_Panel.CheckBoxAlways_show_all_icons_an.Click();
            }
            Delay.Seconds(2);
            bool showAllIcons = ControlPanelRepo.Instance.FormControl_Panel.CheckBoxAlways_show_all_icons_an.Checked;
            ControlPanelRepo.Instance.FormControl_Panel.ButtonClose.Press();
            return showAllIcons;
        }
    }
}