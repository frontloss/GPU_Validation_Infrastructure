namespace Intel.VPG.Display.Automation
{
    using System;

    public class MachineInfo
    {
        public string Name { get; set; }
        public string BIOSVersion { get; set; }
        public DriverInfo Driver { get; set; }
        public OSInfo OS { get; set; }
        public string PhysicalMemory { get; set; }
        public PlatformDetails PlatformDetails { get; set; }
    }
}