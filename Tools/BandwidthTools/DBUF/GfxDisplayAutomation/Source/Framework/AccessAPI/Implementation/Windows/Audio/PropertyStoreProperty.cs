namespace Intel.VPG.Display.Automation
{
    internal class PropertyStoreProperty
    {
        private PropertyKey _PropertyKey;
        private PropVariant _PropValue;

        internal PropertyStoreProperty(PropertyKey key, PropVariant value)
        {
            _PropertyKey = key;
            _PropValue = value;
        }

        public PropertyKey Key
        {
            get
            {
                return _PropertyKey;
            }
        }

        public object Value
        {
            get
            {
                return _PropValue.Value;
            }
        }
    }
}
