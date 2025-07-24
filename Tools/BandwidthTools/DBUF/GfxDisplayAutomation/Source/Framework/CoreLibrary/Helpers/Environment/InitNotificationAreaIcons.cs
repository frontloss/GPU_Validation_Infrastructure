namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;

    class InitNotificationAreaIcons : InitEnvironment
    {
        private string naiFlg = string.Empty;

        public InitNotificationAreaIcons(IApplicationManager argManager)
            : base(argManager)
        {
            this.naiFlg = string.Format(@"{0}\nai.flg", Directory.GetParent(Directory.GetCurrentDirectory()));
        }
        public bool NAIFlgExists
        {
            get { return File.Exists(this.naiFlg); }
        }
        public override void DoWork()
        {
            int notifFlg = 0;
            if (this.NAIFlgExists)
            {
                string data = File.ReadAllText(this.naiFlg);
                if (!string.IsNullOrEmpty(data.Trim()))
                    notifFlg = Convert.ToInt32(data.Trim());
            }
            if (notifFlg.Equals(0) && AccessInterface.SetFeature<bool, string>(Features.NotificationAreaIcons, Action.SetMethod, string.Empty))
                File.WriteAllText(this.naiFlg, "1");
        }
    }
}