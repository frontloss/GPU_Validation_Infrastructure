namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;

    internal class TestResultList : Dictionary<TestResult, long>
    {
        internal TestResultList()
        {
            Enum.GetValues(typeof(TestResult)).Cast<TestResult>().ToList().ForEach(tR => base.Add(tR, 0));
        }
        internal void Add(TestResult argResult)
        {
            this[argResult]++;
        }
    }
}