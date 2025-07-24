namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Xml;
    internal class CPUState : FunctionalBase, ISetMethod, IGetMethod
    {
        public bool SetMethod(object argMessage)
        {
            CSParam PowerParam = argMessage as CSParam;
            if (PowerParam.VerificationTool == CSVerificationTool.BLATool)
            {
                BLATool tool = new BLATool();
                return tool.SetMethod(PowerParam);
            }
            else if (PowerParam.VerificationTool == CSVerificationTool.SocWatch)
            {
                SocWatch scWatch = base.CreateInstance<SocWatch>(new SocWatch());
                return scWatch.SetMethod(PowerParam);
            }
            else
            {
                Log.Fail("Verification tool not specified to check CPU State.");
                return false;
            }
        }

        public object GetMethod(object argMessage)
        {
            CSParam PowerParam = argMessage as CSParam;
            if (PowerParam.VerificationTool == CSVerificationTool.BLATool)
            {
                BLATool tool = base.CreateInstance<BLATool>(new BLATool());
                return tool.GetCPUState(PowerParam.cState);
            }
            else if (PowerParam.VerificationTool == CSVerificationTool.SocWatch)
            {
                SocWatch scWatch = base.CreateInstance<SocWatch>(new SocWatch());
                return scWatch.GetCPUState(PowerParam.cState);
            }
            else
            {
                Log.Fail("Verification tool not specified to check CPU Sytate.");
                return false;
            }
        }
    }
}
