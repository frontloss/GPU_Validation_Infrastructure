namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.HasINFModify)]
    class MP_Rotation_Independent_S4 : MP_Rotation_Independent_S3
    {
        public MP_Rotation_Independent_S4()
        {
            base._myDictionary = new Dictionary<DisplayConfigType, uint[,]>()
            {
                 { DisplayConfigType.DDC, new uint[,] {{180,0},{90,270},{0,0}}},
                 { DisplayConfigType.TDC, new uint[,] {{180,0,0},{90,270,270},{90,90,270},{0,0,0}}}    
            };
            base._PowerState = PowerStates.S4;
        }
    }
}
