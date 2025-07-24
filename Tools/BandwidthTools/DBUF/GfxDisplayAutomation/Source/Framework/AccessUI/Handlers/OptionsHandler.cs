namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;

    public static class OptionsHandler<T>
    {
        public static T GetEnumName(Dictionary<T, Ranorex.Unknown> argOptions)
        {
            return argOptions.Where(kV => null != kV.Value.Element.GetAttributeValue("ItemStatus")).Select(kV => kV.Key).FirstOrDefault();
        }
        public static void SetEnumName(T argValue, Dictionary<T, Ranorex.Unknown> argOptions)
        {
            argOptions[argValue].FocusEnter();
        }
        public static bool IsEnabled(T argValue, Dictionary<T, Ranorex.Unknown> argOptions)
        {
            return argOptions[argValue].Enabled;
        }
        public static bool IsVisible(T argValue, Dictionary<T, Ranorex.Unknown> argOptions)
        {
            return argOptions[argValue].Visible;
        }
    }
}