namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;

    using Microsoft.Win32;

    class RegistryCommands : IDisposable
    {
        private RegistryKey _subKey = null;
        List<string> _pathsList;

        internal RegistryKey SubKey
        {
            set { this._subKey = value; }
            get { return this._subKey; }
        }
        internal RegistryCommands(RegistryKey argSubKey)
        {
            this._subKey = argSubKey;
        }
        internal RegistryKey Create(string argKey)
        {
            return this._subKey.CreateSubKey(argKey);
        }
        internal T Read<T>(string argKey)
        {
            return (T)this._subKey.GetValue(argKey);
        }
        internal void Write<T>(string argKey, T argValue)
        {
            this.Write<T>(this._subKey, argKey, argValue);
        }
        internal void WriteDWord<T>(string argKey, T argValue)
        {
            this._subKey.SetValue(argKey, argValue, RegistryValueKind.DWord);
        }
        internal void WriteBinary<T>(string argKey, T argValue)
        {
            this._subKey.SetValue(argKey, argValue, RegistryValueKind.Binary);
        }
        internal void Delete(string argValueKey)
        {
            this._subKey.DeleteValue(argValueKey);
        }
        internal bool Exists(string argSubKey)
        {
            return this._subKey.GetValueNames().Contains(argSubKey);
        }
        internal bool Exists(RegistryKey argSubKey, string argValueKey)
        {
            return (null != argSubKey.GetValue(argValueKey));
        }
        internal List<string> GetValueKeys(string argValueKey)
        {
            return this._subKey.GetValueNames().Where(key => key.StartsWith(argValueKey)).ToList();
        }
        public void Dispose()
        {
            if (null == this._subKey)
                this._subKey.Close();
        }

        private void Write<T>(RegistryKey argSubKey, string argKey, T argValue)
        {
            if (!this.Exists(argSubKey, argKey))
                throw new Exception(string.Format("Unable to Write {0}:{1} to registry", argKey, argValue));
            argSubKey.SetValue(argKey, argValue);
        }
    }
}
