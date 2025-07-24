namespace Intel.VPG.Display.Automation
{
    using System.Diagnostics;

    using Microsoft.Win32;

    internal static class CommandActions
    {
        internal static string SelectFakeEDIDFile()
        {
            OpenFileDialog openDialog = new OpenFileDialog();
            openDialog.Filter = "Bin Files (*.bin)|*.bin|Text Files (*.txt)|*.txt|EDID Files (*.EDID)|*.EDID";
            if (openDialog.ShowDialog().Value)
                return openDialog.FileName;
            return string.Empty;
        }
        internal static CommandResult RebootSystem()
        {
            int initRebootInterval = 15;
            CommandResult rebootResult = new CommandResult();
            rebootResult.Result = string.Format("System will reboot in less than {0} seconds!", initRebootInterval);
            rebootResult.MessageFormatType = MessageFormatType.Warning;
            CommonExtensions.StartProcess("shutdown.exe", string.Format("/f /r /t {0}", initRebootInterval));
            return rebootResult;
        }
        internal static CommandResult PerformRegistryAction(RegistryParams argParam)
        {
            return RegistryActions.ActionList[argParam.RegistryOption](argParam);
        }
    }
}
