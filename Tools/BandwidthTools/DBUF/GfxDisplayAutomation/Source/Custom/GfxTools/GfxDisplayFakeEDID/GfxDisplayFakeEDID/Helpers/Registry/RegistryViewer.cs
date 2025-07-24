namespace Intel.VPG.Display.Automation
{
    using System;

    using Microsoft.Win32;

    static class RegistryViewer
    {
        private static RegistryKey _baseKey = null;
        
        internal static RegistryCommands Init(RegistryHive argHive, string argPath)
        {
            _baseKey = RegistryKey.OpenBaseKey(argHive, RegistryView.Default);
            if (null == _baseKey)
                throw new Exception(string.Format("Unable to Open registry hive {0}", argHive));
            RegistryKey subKey = _baseKey.OpenSubKey(argPath, true);
            if (null == subKey)
                throw new Exception(string.Format("Unable to Open registry path {0}", argPath));

            return new RegistryCommands(subKey);
        }
        internal static RegistryKey OpenSubKey(string argPath)
        {
            RegistryKey subKey = _baseKey.OpenSubKey(argPath, true);
            if (null == subKey)
                throw new Exception(string.Format("Unable to Open registry path {0}", argPath));
            return subKey;
        }
    }
}
