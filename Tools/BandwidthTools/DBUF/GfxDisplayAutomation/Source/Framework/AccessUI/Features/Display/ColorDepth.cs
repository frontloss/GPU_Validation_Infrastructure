namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;

    public class ColorDepth : FunctionalBase, IGet, ISet, IGetAll
    {
        private Dictionary<ColorDepthOptions, Ranorex.Unknown> _options = new Dictionary<ColorDepthOptions, Ranorex.Unknown>();

        public ColorDepth()
        {
            IList<Ranorex.Unknown> list = DisplaySettingsRepo.Instance.FormIntelR_Graphics_and_Medi.ColorDepthControl.Children;
            string colorDepth = string.Empty;
            ColorDepthOptions colorDepthOption;
            Ranorex.Text colorDepthText = null;
            foreach (Ranorex.Unknown u in list)
            {
                colorDepthText = u.FindChild<Ranorex.Text>();
                colorDepth = colorDepthText.TextValue.Replace(" ", "_");
                colorDepth = String.Concat("_",colorDepth);
                if (Enum.TryParse(colorDepth, out colorDepthOption))
                    _options.Add(colorDepthOption, u);
            }
        }
        public Object Get
        {
            get { return OptionsHandler<ColorDepthOptions>.GetEnumName(_options); }
        }
        public Object Set
        {
            set { OptionsHandler<ColorDepthOptions>.SetEnumName((ColorDepthOptions)value, _options); }
        }
        public object GetAll
        {
            get { return this._options.Keys.ToList(); }
        }
    }
}