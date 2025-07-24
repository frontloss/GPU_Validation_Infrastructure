namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    public class CPUStateParam
    {
        public List<CPU_C_STATE> ValidCPUState;
        public bool CheckState;
        public CPUStateParam()
        {
            ValidCPUState = new List<CPU_C_STATE>();
            CheckState = false;
        }
    }
}
