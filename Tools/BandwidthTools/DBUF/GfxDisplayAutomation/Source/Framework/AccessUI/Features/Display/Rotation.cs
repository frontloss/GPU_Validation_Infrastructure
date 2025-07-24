namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Windows.Forms;
    using System.Collections.Generic;

    public class Rotation : FunctionalBase, IGet, ISet, IGetAll
    {
        Dictionary<ScreenOrientation, Ranorex.Unknown> _options = new Dictionary<ScreenOrientation, Ranorex.Unknown>();
        public Rotation()
        {
            IList<Ranorex.Unknown> list = null;
            list = DisplaySettingsRepo.Instance.FormIntelR_Graphics_and_Medi.RotationControl.Children;
            Ranorex.Text rotationText = null;
            string rotation = string.Empty;
            foreach (Ranorex.Unknown u in list)
            {
                if (u.Visible)
                {
                    rotationText = u.FindChild<Ranorex.Text>();
                    rotation = rotationText.TextValue;
                    ScreenOrientation screenorientoption;
                    if (Enum.TryParse(string.Concat("Angle", rotation), out screenorientoption))
                        _options.Add(screenorientoption, u);
                }
            }
        }
        public object Get
        {
            get { return OptionsHandler<ScreenOrientation>.GetEnumName(this._options); }
        }
        public object Set
        {
            set
            {
                ScreenOrientation currOrientation = (ScreenOrientation)this.Get;
                if (currOrientation != (ScreenOrientation)value)
                    OptionsHandler<ScreenOrientation>.SetEnumName((ScreenOrientation)value, this._options);
            }
        }
        public object GetAll
        {
            get { return this._options.Keys.ToList(); }
        }
    }
}