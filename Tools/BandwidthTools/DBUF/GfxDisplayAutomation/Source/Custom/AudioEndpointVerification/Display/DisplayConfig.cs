namespace AudioEndpointVerification
{
    using System.Linq;
    using System.Collections.Generic;
    using System.Text;
    using System.Collections.Generic;
    
    
    public class DisplayConfig
    {
        public Dictionary<string, DisplayType> dispListParam = new Dictionary<string,DisplayType>();
        private List<DisplayType> _customDisplayList = null;

        public DisplayConfigType ConfigType { get; set; }
        public List<DisplayType> DisplayList { get; set; }
        public DisplayType PrimaryDisplay { get; set; }
        public DisplayType SecondaryDisplay { get; set; }
        public DisplayType TertiaryDisplay { get; set; }
        public List<DisplayType> CustomDisplayList
        {
            get
            {
                if (null == this._customDisplayList)
                {
                    this._customDisplayList = new List<DisplayType>();
                    if (this.PrimaryDisplay != DisplayType.None) this._customDisplayList.Add(this.PrimaryDisplay);
                    if (this.SecondaryDisplay != DisplayType.None) this._customDisplayList.Add(this.SecondaryDisplay);
                    if (this.TertiaryDisplay != DisplayType.None) this._customDisplayList.Add(this.TertiaryDisplay);
                }
                return this._customDisplayList;
            }
        }

        public override string ToString()
        {
            StringBuilder PrintConfig = new StringBuilder(string.Empty);
            PrintConfig.Append(ConfigType + " - ");
            PrintConfig.Append(PrimaryDisplay + " ");
            PrintConfig.Append(ConfigType != DisplayConfigType.SD ? ("+ " + SecondaryDisplay + " ") : string.Empty);
            PrintConfig.Append(((ConfigType == DisplayConfigType.TDC) || (ConfigType == DisplayConfigType.TED)) ?
                                            ("+ " + TertiaryDisplay + " ") : string.Empty
                              );
            return PrintConfig.ToString();
        }
    }
}