namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Text;

    class HDCP : FunctionalBase, ISet//, IParse
    {
        private Dictionary<HDCPOptions, Action<Process>> _hdcpkOptions = null;
        private static Dictionary<HDCPApplication, HDCPBase> _apps = null;

        public object Set
        {
            set
            {
                HDCPParams tempParams = value as HDCPParams;
                HDCPBase app = this.GetApplication(tempParams.HDCPApplication);
                this.OptionsAvailable(app);
                app.GetMode = base.GetDisplayModeByDisplayType;
                app.HDCPParams = tempParams;
                app.AppSettings = base.AppSettings;
                this._hdcpkOptions[app.HDCPParams.HDCPOptions](app.Instance(app.HDCPParams.HDCPPlayerInstance));
            }
        }

        private void OptionsAvailable(HDCPBase argApp)
        {
            if (null == this._hdcpkOptions)
            {
                _hdcpkOptions = new Dictionary<HDCPOptions, Action<Process>>();
                _hdcpkOptions.Add(HDCPOptions.Close, argApp.Close);
                _hdcpkOptions.Add(HDCPOptions.Move, argApp.Move);
                _hdcpkOptions.Add(HDCPOptions.ActivateHDCP, argApp.ActivateHDCP);
                _hdcpkOptions.Add(HDCPOptions.DeactivateHDCP, argApp.DeactivateHDCP);
                _hdcpkOptions.Add(HDCPOptions.QueryGlobalProtectionLevel, argApp.QueryGlobalProtectionLevel);
                _hdcpkOptions.Add(HDCPOptions.QueryLocalProtectionLevel, argApp.QueryLocalProtectionLevel);
                _hdcpkOptions.Add(HDCPOptions.SetSRM, argApp.SetSRM);
                _hdcpkOptions.Add(HDCPOptions.GetSRMVersion, argApp.GetSRMVersion);
                _hdcpkOptions.Add(HDCPOptions.ActivateACP, argApp.ActivateACP);
                _hdcpkOptions.Add(HDCPOptions.ActivateCGMSA, argApp.ActivateCGMSA);
            }
        }
        private HDCPBase GetApplication(HDCPApplication appType)
        {
            if (null == _apps)
            {
                _apps = new Dictionary<HDCPApplication, HDCPBase>();
                _apps.Add(HDCPApplication.OPMTester, new OPMTester());
            }
            return _apps[appType];
        }

        //public void Parse(string[] args)
        //{
        //    if (args.Length >= 3 && args[0].ToLower().Contains("set"))
        //    {
        //        HDCPParams tempParams = new HDCPParams();
        //        HDCPApplication tempAppType = HDCPApplication.None;
        //        HDCPOptions tempOptions = HDCPOptions.None;
        //        HDCPPlayerInstance playerInstance = HDCPPlayerInstance.Player_1;

        //        if (Enum.TryParse<HDCPApplication>(args[1], true, out tempAppType) && Enum.TryParse<HDCPOptions>(args[2], true, out tempOptions))
        //        {
        //            tempParams.HDCPApplication = tempAppType;
        //            tempParams.HDCPOptions = tempOptions;
        //        }
        //        else
        //        {
        //            this.HelpText();
        //        }

        //        if (args.Length > 3)
        //        {
        //            DisplayHierarchy tempHierarchy = DisplayHierarchy.Unsupported;
        //            if (Enum.TryParse<DisplayHierarchy>(args[3], true, out tempHierarchy))
        //            {
        //                tempParams.DisplayHierarchy = tempHierarchy;
        //                tempParams.CurrentConfig = base.CurrentConfig;
        //            }
        //            else
        //            {
        //                this.HelpText();
        //            }
        //        }
        //        HDCPBase app = this.GetApplication(tempParams.HDCPApplication);
        //        this.OptionsAvailable(app);
        //        app.GetMode = base.GetDisplayModeByDisplayType;
        //        app.HDCPParams = tempParams;
        //        this._hdcpkOptions[app.HDCPParams.HDCPOptions](app.Instance(playerInstance));
        //    }
        //    else
        //        this.HelpText();
        //}

        //private void HelpText()
        //{
        //    StringBuilder sb = new StringBuilder();
        //    sb.Append("..\\>Problem with Commandline Parameters. \n Please type : Execute.exe HDCP set OPMTester <Enable/Disable/Move/Close> [Display_2/Display_3]").Append(Environment.NewLine);
        //    sb.Append("For example : Execute.exe HDCP set OPMTester Enable");
        //    sb.Append("For example : Execute.exe HDCP set OPMTester Move Display_2");
        //    Log.Message(sb.ToString());
        //}

    }
}