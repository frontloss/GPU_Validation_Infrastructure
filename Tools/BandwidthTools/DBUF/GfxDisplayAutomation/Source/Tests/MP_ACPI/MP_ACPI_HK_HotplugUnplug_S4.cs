
namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class MP_ACPI_HK_HotplugUnplug_S4 : MP_ACPI_HK_HotplugUnplug_S3
    {
       public MP_ACPI_HK_HotplugUnplug_S4()
        {
            powerState = PowerStates.S4;
        }
    }
}
