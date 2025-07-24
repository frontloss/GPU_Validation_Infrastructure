namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;

    public class Scaling : FunctionalBase, IGet, ISet, IGetAll
    {
        private Dictionary<ScalingOptions, Ranorex.Unknown> _options = new Dictionary<ScalingOptions, Ranorex.Unknown>();

        public Scaling()
        {
            IList<Ranorex.Unknown> list = DisplaySettingsRepo.Instance.FormIntelR_Graphics_and_Medi.ScalingControl.Children;
            string scaling = string.Empty;
            ScalingOptions scalingOption;
            Ranorex.Text scalingText = null;
            foreach (Ranorex.Unknown u in list)
            {
                scalingText = u.FindChild<Ranorex.Text>();
                scaling = scalingText.TextValue.Replace(" ", "_");
                if (Enum.TryParse(scaling, out scalingOption))
                    _options.Add(scalingOption, u);
            }
        }
        public Object Get
        {
            get { return OptionsHandler<ScalingOptions>.GetEnumName(_options); }
        }
        public Object Set
        {
            set { OptionsHandler<ScalingOptions>.SetEnumName((ScalingOptions)value, _options); }
        }
        public object GetAll
        {
            get { return this._options.Keys.ToList(); }
        }
    }
}