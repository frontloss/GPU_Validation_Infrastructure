namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using Microsoft.Win32;
    using System.IO;
    using System.Collections.Generic;

    internal class RegistryInf : FunctionalBase, ISetMethod,IGetMethod
    {
        public bool SetMethod(object argMessage)
        {
            Log.Message(true, "Disable Driver");
            DisableDriver disableDriver = base.CreateInstance<DisableDriver>(new DisableDriver());
            disableDriver.SetMethod(DriverAdapterType.Intel);

            RegistryParams argRegistryParams = (RegistryParams)argMessage;
            Log.Message(true, "Changing the value of {0} in {1} to {2}", argRegistryParams.keyName, argRegistryParams.registryKey, argRegistryParams.value);
            var list = new Dictionary<string, string>();
            Read(argRegistryParams.registryKey, argRegistryParams.keyName, list);
            Log.Message("length of list is {0}",list.Count);
            foreach (var listItem in list)
            {
                string[] splits = listItem.Key.Split('\\');
                string path = splits[1];
                for (int i = 2; i < splits.Length - 1; i++)
                    path = string.Concat(path, "\\", splits[i]);
                Log.Verbose("Path = {0}", path);
                RegistryView registryView = IntPtr.Size.Equals(8) ? RegistryView.Registry64 : RegistryView.Registry32;
                Log.Verbose("RegistryView = {0}", registryView.ToString());
                using (var hklm = RegistryKey.OpenBaseKey(GetHiveFromKey(argRegistryParams.registryKey), registryView))
                using (RegistryKey myKey = hklm.OpenSubKey(path, RegistryKeyPermissionCheck.ReadWriteSubTree))
                {
                    if (argRegistryParams.infChanges == InfChanges.RevertInf)
                        myKey.SetValue(argRegistryParams.keyName, argRegistryParams.value);
                    else
                    {
                        int value = Convert.ToInt32(myKey.GetValue(argRegistryParams.keyName).ToString());
                        if (value == argRegistryParams.value)
                            Log.Message("{0} is already set to {1}", argRegistryParams.keyName, argRegistryParams.value);
                        else
                            myKey.SetValue(argRegistryParams.keyName, argRegistryParams.value);
                    }
                }
            }

            Log.Message(true, "Enable Driver");
            EnableDriver enableDriver = base.CreateInstance<EnableDriver>(new EnableDriver());
            enableDriver.SetMethod(DriverAdapterType.Intel);

            if (argRegistryParams.infChanges == InfChanges.RevertInf)
            {
                Log.Message(true, "Reboot the system");
                PowerEvent powerEvent = new PowerEvent() { CurrentMethodIndex = base.CurrentMethodIndex };
                powerEvent.SetMethod(new PowerParams() { PowerStates = PowerStates.S5, Delay = 10, rebootReason = RebootReason.DriverModify });
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
        public object GetMethod(object argMessage)
        {
            List<int> listValue = new List<int>();        

            RegistryParams argRegistryParams = (RegistryParams)argMessage;
            if (argRegistryParams.infChanges == InfChanges.DeleteInf)
            {
                //disbale driver
                Log.Message(true, "Disable Driver");
                DisableDriver disableDriver = base.CreateInstance<DisableDriver>(new DisableDriver());
                disableDriver.SetMethod(DriverAdapterType.Intel);
            }

            if (argRegistryParams.path != null)
            {
                //Log.Verbose("Reading {0} in {1}\\{2} ", argRegistryParams.keyName, argRegistryParams.registryKey, argRegistryParams.path);
                using (RegistryKey myKey = argRegistryParams.registryKey.OpenSubKey(argRegistryParams.path, RegistryKeyPermissionCheck.ReadWriteSubTree))
                {
                    if (argRegistryParams.infChanges == InfChanges.ReadInf)
                    {
                        int value = Convert.ToInt32(myKey.GetValue(argRegistryParams.keyName).ToString());
                        return value;
                    }
                    if (argRegistryParams.infChanges == InfChanges.DeleteInf)
                    {
                        myKey.DeleteSubKey(argRegistryParams.keyName);
                        Log.Message("deleting sub key {0}", argRegistryParams.keyName);
                    }
                }
            }
            else
            {
                Log.Message(true, "Reading  the value of {0} in {1} ", argRegistryParams.keyName, argRegistryParams.registryKey);
                var list = new Dictionary<string, string>();
                Read(argRegistryParams.registryKey, argRegistryParams.keyName, list);
                Log.Message("length of list is {0}", list.Count);
                foreach (var listItem in list)
                {
                    string[] splits = listItem.Key.Split('\\');
                    string path = splits[1];
                    for (int i = 2; i < splits.Length - 1; i++)
                        path = string.Concat(path, "\\", splits[i]);
                    Log.Verbose("Path = {0}", path);
                    RegistryView registryView = IntPtr.Size.Equals(8) ? RegistryView.Registry64 : RegistryView.Registry32;
                    Log.Verbose("RegistryView = {0}", registryView.ToString());
                    using (var hklm = RegistryKey.OpenBaseKey(GetHiveFromKey(argRegistryParams.registryKey), registryView))
                    using (RegistryKey myKey = hklm.OpenSubKey(path, RegistryKeyPermissionCheck.ReadWriteSubTree))
                    {
                        if (argRegistryParams.infChanges == InfChanges.ReadInf)
                        {
                            int value = Convert.ToInt32(myKey.GetValue(argRegistryParams.keyName).ToString());
                            if (!listValue.Contains(value))
                                listValue.Add(value);
                        }
                        if (argRegistryParams.infChanges == InfChanges.DeleteInf)
                        {
                            myKey.DeleteSubKey(argRegistryParams.keyName);
                            Log.Message("deleting sub key {0}", argRegistryParams.keyName);
                        }
                    }
                }

                if (argRegistryParams.infChanges == InfChanges.DeleteInf)
                {
                    Log.Message(true, "Enable Driver");
                    EnableDriver enableDriver = base.CreateInstance<EnableDriver>(new EnableDriver());
                    enableDriver.SetMethod(DriverAdapterType.Intel);
                }
                if (listValue.Count > 1)
                    Log.Message("Multiple value found");
                else
                    return listValue[0];
            }

            Log.Message("Returning default value -1");
            return -1;
        }
    }
}