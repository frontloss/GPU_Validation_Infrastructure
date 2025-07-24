namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System.Threading;

    [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.HasINFModify)]
    class MP_Rotation_Independent_S3 : MP_Rotation_Independent_Basic
    {
        protected PowerStates _PowerState;
        public MP_Rotation_Independent_S3()
        {
            _PowerState = PowerStates.S3;
            base._myDictionary = new Dictionary<DisplayConfigType, uint[,]>()
            {
                 { DisplayConfigType.DDC, new uint[,] {{180,0},{90,270},{180,0}}},
                 { DisplayConfigType.TDC, new uint[,] {{180,0,0},{90,270,270},{180,0,0},{90,270,270}}}    
            };
        }

        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            uint[,] workingAngles = _myDictionary[base.CurrentConfig.ConfigType];

            for (uint idx = 0; idx <= workingAngles.GetUpperBound(0); idx++)
            {
                List<DisplayMode> modeList = PerformIndependentRotation(idx);
                PowerEvent();
                Thread.Sleep(5000);
                VerifyPersistance(modeList);

            }
        }
        protected void PowerEvent()
        {
            Log.Message("Goto {0} and resume.", this._PowerState);
            this._powerParams = new PowerParams() { Delay = 30 };
            base.InvokePowerEvent(this._powerParams, this._PowerState);
        }

        protected void VerifyPersistance(List<DisplayMode> argModeList)
        {
            argModeList.ForEach(curMode =>
            {
                DisplayMode actualMode = VerifyRotation(curMode.display, curMode);
                if (actualMode.Angle != curMode.Angle)
                {
                    Log.Fail(false, "Mode not persisting for display {0}: SetMode - {1}, CurrentMode - {2}. Trying again!", actualMode.display, curMode.GetCurrentModeStr(false), actualMode.GetCurrentModeStr(false));
                }
                else
                    Log.Success("Mode is persisting for display {0}: {1}", actualMode.display, actualMode.GetCurrentModeStr(false));

            });
        }
    }
}