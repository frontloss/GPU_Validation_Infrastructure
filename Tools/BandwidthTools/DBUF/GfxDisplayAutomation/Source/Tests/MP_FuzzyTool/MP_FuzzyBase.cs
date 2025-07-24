namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Text.RegularExpressions;
    using System.Xml;
    using System.Runtime.InteropServices;

    class MP_FuzzyBase : TestBase
    {
        public int escMajorCode = 0;
        public int escMinorCode = 0;

        [DllImport("FuzzingTool.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern void FuzzDisplayEscapes(int escMajorCode, int escMinorCode);

        #region PreCondition
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void FuzzyToolPrerequest()
        {
            string testName = CommonExtensions._cmdLineArgs.First();
            XmlDocument fuzzyTestInfo = new XmlDocument();
            fuzzyTestInfo.Load("Mapper\\FuzzyTool.map");
            XmlNode root = fuzzyTestInfo.SelectSingleNode("/FuzzyTool");
            foreach (XmlNode testInstance in root.ChildNodes)
            {
                if (testInstance.Attributes["TestName"].Value == testName)
                {
                    escMajorCode = Convert.ToInt32(testInstance.Attributes["MajorCode"].Value);
                    Log.Verbose("ulEscMajorCode is: {0}", escMajorCode);
                    escMinorCode = Convert.ToInt32(testInstance.Attributes["MinorCode"].Value);
                    Log.Verbose("ulEscMinorCode is: {0}", escMinorCode);
                    break;
                }
            }
        }
        #endregion 
    }
}