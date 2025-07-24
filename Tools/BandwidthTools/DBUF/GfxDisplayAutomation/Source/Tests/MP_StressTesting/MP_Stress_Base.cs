namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading;
    using System.Xml;

    class MP_Stress_Base : TestBase
    {
        internal int StressCycle = 0;
        internal string TestName = string.Empty;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void StressTestingPrerequest()
        {
            GetTestAttribute();
        }

        private void GetTestAttribute()
        {
            TestName = base.ApplicationManager.ParamInfo.Get<String>(ArgumentType.TestName);
            XmlDocument benchmarkValue = new XmlDocument();
            benchmarkValue.Load("Mapper\\StressParam.map");
            XmlNode eventBenchmarkRoot = benchmarkValue.SelectSingleNode("/Data");
            foreach (XmlNode chNode in eventBenchmarkRoot.ChildNodes)
            {
                if (TestName.Equals(Convert.ToString(chNode.Attributes["name"].Value)))
                {
                    StressCycle = Convert.ToInt32(chNode.Attributes["cycle"].Value);
                    break;
                }
            }
            if (StressCycle == 0)
            {
                Log.Abort("Could not found stress test attribute in StressParam.map file");
            }
        }
    }
}
