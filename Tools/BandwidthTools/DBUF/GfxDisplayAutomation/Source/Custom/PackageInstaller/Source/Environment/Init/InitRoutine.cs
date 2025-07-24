namespace PackageInstaller
{
    public static class InitRoutine
    {
        public static SystemInfo Run()
        {
            SystemInfo systemInfo = new SystemInfo();
            OSInformation OSInfo = new OSInformation();
            systemInfo.OS = OSInfo.Get();

            return systemInfo;
        }
    }
}
