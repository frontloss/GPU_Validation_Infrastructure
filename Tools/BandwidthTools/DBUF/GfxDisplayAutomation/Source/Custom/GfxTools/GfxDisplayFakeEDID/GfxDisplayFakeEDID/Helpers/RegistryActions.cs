namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Collections.Generic;

    using Microsoft.Win32;

    internal static class RegistryActions
    {
        private static Dictionary<string, Func<RegistryParams, CommandResult>> _actionList = null;
        private static string _readEDIDKey = "ReadEDIDFromRegistry";
        private static string _fakeEDIDKey = "FakeEDID_";

        internal static Dictionary<string, Func<RegistryParams, CommandResult>> ActionList
        {
            get
            {
                if (null == _actionList)
                {
                    _actionList = new Dictionary<string, Func<RegistryParams, CommandResult>>();
                    _actionList.Add("AddAll Keys", AddAllKeys);
                    _actionList.Add("AddAll Keys & Enable EDID", AddAllNEnableKeys);
                    _actionList.Add("RemoveAll Keys", RemoveAllKeys);
                    _actionList.Add("Enable Key", EnableKey);
                    _actionList.Add("Disable Key", DisableKey);
                }
                return _actionList;
            }
        }

        private static CommandResult AddAllNEnableKeys(RegistryParams argParam)
        {
            CommandResult addNEnableResult = new CommandResult();
            AddAllKeys(argParam, addNEnableResult);
            return addNEnableResult;
        }
        private static CommandResult AddAllKeys(RegistryParams argParam)
        {
            CommandResult addResult = new CommandResult();
            AddAllKeys(argParam, addResult);
            return addResult;
        }
        private static void AddAllKeys(RegistryParams argParam, CommandResult argResult)
        {
            if (File.Exists(argParam.FakeEDIDFile))
            {
                byte[] fakeEDIDData = File.ReadAllBytes(argParam.FakeEDIDFile);
                if (null != fakeEDIDData && (fakeEDIDData.Length.Equals(128) || fakeEDIDData.Length.Equals(256)))
                {
                    byte[] fakeBlock = null;
                    if (argParam.EDIDBlockType == EDIDBlockType.Base)
                    {
                        fakeBlock = fakeEDIDData.Take(128).ToArray();
                        SetFakeEDIDData(argParam.DisplayInfo.ManufacturerInfo, fakeBlock, BaseBlockValues.Manufacturer);
                        SetFakeEDIDData(argParam.DisplayInfo.ProductInfo, fakeBlock, BaseBlockValues.Product);
                        UpdateChecksum(fakeBlock);
                    }
                    else
                    {
                        if (fakeEDIDData.Length.Equals(256))
                        {
                            if (argParam.EDIDBlockType == EDIDBlockType.CEA_Extension)
                                fakeBlock = fakeEDIDData.Skip(128).ToArray();
                            else if (argParam.EDIDBlockType == EDIDBlockType.Both)
                            {
                                fakeBlock = fakeEDIDData;
                                SetFakeEDIDData(argParam.DisplayInfo.ManufacturerInfo, fakeBlock, BaseBlockValues.Manufacturer);
                                SetFakeEDIDData(argParam.DisplayInfo.ProductInfo, fakeBlock, BaseBlockValues.Product);
                                UpdateChecksum(fakeBlock);
                            }
                        }
                        else
                        {
                            argResult.Result = "FakeEDID File does not have CEA extension block!";
                            argResult.MessageFormatType = MessageFormatType.Warning;
                        }
                    }

                    if (null != fakeBlock)
                    {
                        RegistryCommands regCommands = GetRegistryHandle(argResult);
                        if (null != regCommands)
                        {
                            string fakeEDIDKey = string.Format("{0}{1}_{2}_{3}_{4}", _fakeEDIDKey, argParam.PortValue, (int)argParam.EDIDBlockType - 1, argParam.DisplayInfo.ManufacturerName, argParam.DisplayInfo.ProductCode);
                            if (!regCommands.Exists(fakeEDIDKey))
                            {
                                RemoveRegKeys(regCommands, _fakeEDIDKey);
                                regCommands.WriteBinary(fakeEDIDKey, fakeBlock);
                                argResult.Result = string.Concat(fakeEDIDKey, " created.");
                                argResult.MessageFormatType = MessageFormatType.Information;
                            }
                            else
                            {
                                argResult.Result = string.Concat(fakeEDIDKey, " already exists!");
                                argResult.MessageFormatType = MessageFormatType.Warning;
                            }

                            if (!regCommands.Exists(_readEDIDKey))
                            {
                                RemoveRegKeys(regCommands, _readEDIDKey);
                                regCommands.WriteDWord(_readEDIDKey, 0);
                                if (argParam.RegistryOption.Equals(_actionList.Keys.First()))
                                    argResult.Result = string.Concat(argResult.Result, " ", _readEDIDKey, " created, enable ReadEDID required!");
                                else
                                {
                                    CommandResult enableResult = EnableDisableKey(1, "enabled");
                                    if (enableResult.MessageFormatType == MessageFormatType.Warning)
                                    {
                                        argResult.Result = enableResult.Result;
                                        argResult.MessageFormatType = MessageFormatType.Warning;
                                    }
                                    else
                                        argResult.Result = string.Concat(argResult.Result, " ", _readEDIDKey, " created & enabled. Restart reqd!");
                                }
                            }
                        }
                    }
                }
                else
                {
                    argResult.Result = "FakeEDID File supplied is not valid!";
                    argResult.MessageFormatType = MessageFormatType.Warning;
                }
            }
            else
            {
                argResult.Result = "FakeEDID File supplied does not exist!";
                argResult.MessageFormatType = MessageFormatType.Warning;
            }
        }
        private static CommandResult EnableKey(RegistryParams argParam)
        {
            return EnableDisableKey(1, "enabled");
        }
        private static CommandResult DisableKey(RegistryParams argParam)
        {
            return EnableDisableKey(0, "disabled");
        }
        private static CommandResult RemoveAllKeys(RegistryParams argParam)
        {
            CommandResult removeResult = new CommandResult();
            RegistryCommands regCommands = GetRegistryHandle(removeResult);
            if (null != regCommands)
            {
                List<string> keys = RemoveRegKeys(regCommands, _fakeEDIDKey);
                if (null != keys)
                    keys.AddRange(RemoveRegKeys(regCommands, _readEDIDKey));
                else
                    keys = RemoveRegKeys(regCommands, _readEDIDKey);
                if (null != keys && !keys.Count.Equals(0))
                    removeResult.Result = string.Concat(string.Join(", ", keys.ToArray()), " removed. System restart required.");
                else
                    removeResult.Result = "No Registry Keys found!";
                removeResult.MessageFormatType = MessageFormatType.Information;
            }
            return removeResult;
        }
        private static List<string> RemoveRegKeys(RegistryCommands argRegCommands, string argValueKey)
        {
            if (null != argRegCommands)
            {
                List<string> keys = argRegCommands.GetValueKeys(argValueKey);
                if (null != keys && !keys.Count.Equals(0))
                {
                    keys.ForEach(key => argRegCommands.Delete(key));
                    return keys;
                }
            }
            return null;
        }
        private static void SetFakeEDIDData(byte[] argSourceEDID, byte[] argFakeEDID, BaseBlockValues argStartIdx)
        {
            for (int idx = 0; idx < argSourceEDID.Length; idx++)
                argFakeEDID[idx + (int)argStartIdx] = argSourceEDID[idx];
        }
        private static void UpdateChecksum(byte[] argEDID)
        {
            byte sumTotal = 0;
            for (int idx = 0; idx < 127; idx++)
                sumTotal += argEDID[idx];
            argEDID[127] = (byte)(0xff - (int)sumTotal + 1);
        }
        private static RegistryCommands GetRegistryHandle(CommandResult argResult)
        {
            string driverKey = DisplayActions.GetDriverKey();
            if (!string.IsNullOrEmpty(driverKey))
            {
                string regPath = string.Concat(@"SYSTEM\ControlSet001\Control\Class\", driverKey);
                return RegistryViewer.Init(RegistryHive.LocalMachine, regPath);
            }
            else
            {
                argResult.Result = "Driver key is empty. Check driver installation!";
                argResult.MessageFormatType = MessageFormatType.Warning;
            }
            return null;
        }
        private static CommandResult EnableDisableKey(int argStatusValue, string argStatusText)
        {
            CommandResult commandResult = new CommandResult();
            RegistryCommands regCommands = GetRegistryHandle(commandResult);
            if (null != regCommands)
            {
                if (regCommands.Exists(_readEDIDKey))
                {
                    if (regCommands.Read<int>(_readEDIDKey).Equals(argStatusValue))
                    {
                        commandResult.Result = string.Format("{0} already {1}!", _readEDIDKey, argStatusText);
                        commandResult.MessageFormatType = MessageFormatType.Warning;
                    }
                    else
                    {
                        regCommands.WriteDWord(_readEDIDKey, argStatusValue);
                        commandResult.Result = string.Format("{0} {1}. System restart required.", _readEDIDKey, argStatusText);
                        commandResult.MessageFormatType = MessageFormatType.Information;
                    }
                }
                else
                {
                    commandResult.Result = string.Concat(_readEDIDKey, " doesnt exist. Choose Add Key option!");
                    commandResult.MessageFormatType = MessageFormatType.Warning;
                }
            }
            return commandResult;
        }
    }
}
