using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
namespace Intel.VPG.Display.Automation
{
    class MP_Rotation_Basic_DisableEnable : MP_Rotation_Basic
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestPreCondition()
        {
            curAppliedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay };
            base.ApplyConfig(curAppliedConfig);
            base._angle = new List<uint>() { 180 };
            base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();
            DisableEnableDriver();

            base._angle = new List<uint>() { 270 };
            base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();
            DisableEnableDriver();
        }
        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            if (base.CurrentConfig.SecondaryDisplay != DisplayType.None)
            {
                curAppliedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
                base.ApplyConfig(curAppliedConfig);
                base._angle = new List<uint>() { 180};
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();
                DisableEnableDriver();

                base._angle = new List<uint>() { 270};
                ApplyNonNative();
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();
                DisableEnableDriver();
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            if (base.CurrentConfig.SecondaryDisplay != DisplayType.None)
            {
                curAppliedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
                base.ApplyConfig(curAppliedConfig);
                base._angle = new List<uint>() { 90, 90 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();
                DisableEnableDriver();

                base._angle = new List<uint>() { 0, 270 };
                ApplyNonNative();
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();
                DisableEnableDriver();
            }
        }
        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep3()
        {
            if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
            {
                curAppliedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
                base.ApplyConfig(curAppliedConfig);
                base._angle = new List<uint>() { 90 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();
                DisableEnableDriver();

                base._angle = new List<uint>() { 0};
                ApplyNonNative();
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();
                DisableEnableDriver();
            }
        }
        [Test(Type = TestType.Method, Order = 4)]
        public virtual void TestStep4()
        {
            if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
            {
                curAppliedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
                base.ApplyConfig(curAppliedConfig);
                base._angle = new List<uint>() { 180, 90, 270 };
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();
                DisableEnableDriver();

                base._angle = new List<uint>() { 270, 180, 90 };
                ApplyNonNative();
                base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();
                DisableEnableDriver();
            }
        }
        public void DisableEnableDriver()
        {
            Log.Message(true, "Disable the driver from Device manager.");
            base.AssertDriverState(Features.DisableDriver, DriverState.Disabled, new[] { 1, 1 });

            Thread.Sleep(7000);

            Log.Message(true, "Enable the driver from Device manager.");
            base.AssertDriverState(Features.EnableDriver, DriverState.Running, new[] { 1, 1 });

            if (curAppliedConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone || curAppliedConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Single)
                VerifyPersistance(curAppliedConfig.PrimaryDisplay, base._angle.First());
            else
            {
                uint i = 0;
                base._angle.ForEach(curAngle =>
                {
                    if (i == 0)
                        VerifyPersistance(curAppliedConfig.PrimaryDisplay, curAngle);
                    if (i == 1)
                        VerifyPersistance(curAppliedConfig.SecondaryDisplay, curAngle);
                    if (i == 2)
                        VerifyPersistance(curAppliedConfig.TertiaryDisplay, curAngle);
                    i++;
                });
            }
        }
        public void VerifyPersistance(DisplayType AargDispType, uint argAngle)
        {
            DisplayMode currentMode = base.VerifyRotation(AargDispType);

            if (currentMode.Angle == argAngle)
                Log.Success("Angle {0} is persisted by {1} after driver disable enable", argAngle, AargDispType);
            else
                Log.Fail("Angle {0} is not persisted by {1} after driver disbale enable, current angle {2}", argAngle, AargDispType, currentMode.Angle);
        }
    }
}


