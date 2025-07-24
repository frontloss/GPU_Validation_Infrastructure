namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Runtime.InteropServices;
    internal class PropertyStore
    {
        private IPropertyStore _Store;

        public int Count
        {
            get
            {
                int Result;
                Marshal.ThrowExceptionForHR(_Store.GetCount(out Result));
                return Result;
            }
        }

        public PropertyStoreProperty this[int index]
        {
            get
            {
                PropVariant result;
                PropertyKey key = Get(index);
                Marshal.ThrowExceptionForHR(_Store.GetValue(ref key, out result));
                return new PropertyStoreProperty(key, result);
            }
        }

        public bool Contains(Guid guid)
        {
            for (int i = 0; i < Count; i++)
            {
                PropertyKey key = Get(i);
                if (key.fmtid == guid)
                    return true;
            }
            return false;
        }

        public PropertyStoreProperty this[Guid guid]
        {
            get
            {
                PropVariant result;
                for (int i = 0; i < Count; i++)
                {
                    PropertyKey key = Get(i);
                    if (key.fmtid == guid)
                    {
                        Marshal.ThrowExceptionForHR(_Store.GetValue(ref key, out result));
                        return new PropertyStoreProperty(key, result);
                    }
                }
                return null;
            }
        }

        public PropertyKey Get(int index)
        {
            PropertyKey key;
            Marshal.ThrowExceptionForHR( _Store.GetAt(index, out key));
            return key;
        }

        public PropVariant GetValue(int index)
        {
            PropVariant result;
            PropertyKey key = Get(index);
            Marshal.ThrowExceptionForHR(_Store.GetValue(ref key, out result));
            return result;
        }

        internal PropertyStore(IPropertyStore store)
        {
            _Store = store;
        }
    }
}
