namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Text;

    class DeepColor : FunctionalBase, ISet, IParse
    {
        private Dictionary<DeepColorOptions, Action<Process>> _playBackOptions = null;
        private Dictionary<DeepColorAppType, DeepColorBase> _apps = null;

        public object Set
        {
            set
            {
                //base.CurrentConfig
                DeepColorParams tempParams = value as DeepColorParams;
                DeepColorBase app = this.GetApplication(tempParams.DeepColorAppType);
                this.OptionsAvailable(app);
                app.GetMode = base.GetDisplayModeByDisplayType;
                app.DeepcolorParams = tempParams;
                this._playBackOptions[app.DeepcolorParams.DeepColorOptions](app.Instance(base.AppSettings, base.CurrentMethodIndex));
            }
        }

        private void OptionsAvailable(DeepColorBase argApp)
        {
            if (null == this._playBackOptions)
            {
                _playBackOptions = new Dictionary<DeepColorOptions, Action<Process>>();
                _playBackOptions.Add(Automation.DeepColorOptions.Close, argApp.Close);
                _playBackOptions.Add(Automation.DeepColorOptions.Enable, argApp.EnableDeepColor);
                _playBackOptions.Add(Automation.DeepColorOptions.Disable, argApp.DisableDeepColor);
                _playBackOptions.Add(Automation.DeepColorOptions.Move, argApp.Move);
            }
        }
        private DeepColorBase GetApplication(DeepColorAppType appType)
        {
            if (null == this._apps)
            {
                this._apps = new Dictionary<DeepColorAppType, DeepColorBase>();
                this._apps.Add(DeepColorAppType.DPApplet, new DisplayPortapplet());
                this._apps.Add(DeepColorAppType.FP16, new Instance_HLSL());
                this._apps.Add(DeepColorAppType.N10BitScanOut, new N10BitScanout());
            }
            return this._apps[appType];
        }

        public void Parse(string[] args)
        {
            if (args.Length >= 3 && args[0].ToLower().Contains("set"))
            {
                DeepColorParams tempParams = new DeepColorParams();
                DeepColorAppType tempAppType = DeepColorAppType.None;
                DeepColorOptions tempOptions = DeepColorOptions.None;

                if(Enum.TryParse<DeepColorAppType>(args[1], true, out tempAppType)&& Enum.TryParse<DeepColorOptions>(args[2], true, out tempOptions))
                {
                    tempParams.DeepColorAppType = tempAppType;
                     tempParams.DeepColorOptions = tempOptions;
                }
                else
                {
                    this.HelpText();
                }

                if (args.Length > 3)
                {
                    DisplayHierarchy tempHierarchy = DisplayHierarchy.Unsupported;
                    if (Enum.TryParse<DisplayHierarchy>(args[3], true, out tempHierarchy))
                    {
                        tempParams.DisplayHierarchy = tempHierarchy;
                        tempParams.CurrentConfig = base.CurrentConfig;
                    }
                    else
                    {
                        this.HelpText();
                    }
                }
                DeepColorBase app = this.GetApplication(tempParams.DeepColorAppType);
                this.OptionsAvailable(app);
                app.GetMode = base.GetDisplayModeByDisplayType;
                app.DeepcolorParams = tempParams;
                this._playBackOptions[app.DeepcolorParams.DeepColorOptions](app.Instance(base.AppSettings, base.CurrentMethodIndex));
            }
            else
                this.HelpText();
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("..\\>Problem with Commandline Parameters. \n Please type : Execute.exe DeepColorApp set <FP16/DPApplet/N10BitScanOut> <Enable/Disable/Move/Close> [Display_2/Display_3]").Append(Environment.NewLine);
            sb.Append("For example : Execute.exe DeepColor set DPApplet Enable");
            sb.Append("For example : Execute.exe DeepColor set FP16 Move Display_2");
            Log.Message(sb.ToString());
        }

    }
}