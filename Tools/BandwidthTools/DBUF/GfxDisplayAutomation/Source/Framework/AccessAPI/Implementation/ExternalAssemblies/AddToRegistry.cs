namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using Microsoft.Win32;
    using System.IO;
    using System.Collections.Generic;

    internal class AddToRegistry : FunctionalBase, ISetMethod
    {
        public bool SetMethod(object argMessage)
        {
            RegistryParams argRegistryParams = (RegistryParams)argMessage;
            Microsoft.Win32.RegistryKey key;
            switch (argRegistryParams.registryKey.ToString())
            {
                case "HKEY_CURRENT_USER": key = Microsoft.Win32.Registry.CurrentUser.CreateSubKey(argRegistryParams.path);
                    key.SetValue(argRegistryParams.keyName, argRegistryParams.value);
                    break;
                case "HKEY_LOCAL_MACHINE": key = Microsoft.Win32.Registry.LocalMachine.CreateSubKey(argRegistryParams.path);
                    key.SetValue(argRegistryParams.keyName, argRegistryParams.value);

                    break;

            }

            return true;
        }
        private void Read(RegistryKey root, string searchKey, IDictionary<string, string> values)
        {
            foreach (string keyName in root.GetSubKeyNames())
            {
                try
                {
                    using (RegistryKey key = root.OpenSubKey(keyName))
                    {
                        Read(key, searchKey, values);
                    }
                }
                catch (System.Security.SecurityException e) { }
            }
            foreach (var value in root.GetValueNames())
            {
                if (value.Equals(searchKey))
                {
                    values.Add(string.Format("{0}\\{1}", root, value), (root.GetValue(value) ?? "").ToString());
                }
            }
        }
        private RegistryHive GetHiveFromKey(RegistryKey argKey)
        {
            switch (argKey.ToString())
            {
                case "HKEY_CURRENT_USER": return RegistryHive.CurrentUser;
                case "HKEY_CURRENT_CONFIG": return RegistryHive.CurrentConfig;
                case "HKEY_CLASSES_ROOT": return RegistryHive.ClassesRoot;
                case "HKEY_LOCAL_MACHINE": return RegistryHive.LocalMachine;
                case "HKEY_PERFORMANCE_DATA": return RegistryHive.PerformanceData;
                case "HKEY_USERS": return RegistryHive.Users;
                default: throw new Exception("Unsupported hive passed as parameter");             
            }
        }
    }
}