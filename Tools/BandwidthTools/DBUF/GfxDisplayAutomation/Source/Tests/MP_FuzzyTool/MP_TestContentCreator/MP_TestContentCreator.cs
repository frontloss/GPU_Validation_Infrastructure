using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Xml;

namespace Intel.VPG.Display.Automation
{
    class MP_TestContentCreator : TestBase
    {
        string[] lines = { "namespace Intel.VPG.Display.Automation", "{", "claaName", "    {", "        [Test(Type = TestType.Method, Order = 1)]", 
                                "        public void SetConfigMethod()", "        {", "            Log.Message(true, \"Set Current config via OS call\");",
                                "            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))",
                                "                Log.Success(\"Config applied successfully\");", "            else",
                                "                Log.Abort(\"Unable to set display config.\");", "        }", "        [Test(Type = TestType.Method, Order = 2)]",
                                "        public void RunTest()", "        {", "            Log.Message(true, \"Fuzzer Tool Invoke\");", 
                                "            FuzzDisplayEscapes(escMajorCode, escMinorCode);", "            Log.Success(\"Test Successfully Completed...\");",
                                "        }", "    }", "}"};

        List<string> commandLineList;
        int testCount = 0;

        [Test(Type = TestType.Method, Order = 1)]
        public void CreateFuzzerTestContent()
        {
            string mapperPath = "Mapper\\FuzzyTool.map";
            string outputPath = Directory.GetCurrentDirectory() + "\\Output";
            if (!File.Exists(mapperPath))
            {
                Log.Abort("Unable to find fuzzer mapper file");
            }
            if (Directory.Exists(outputPath))
            {
                Directory.Delete(outputPath, true);
                Thread.Sleep(2000);
            }
            Directory.CreateDirectory(Directory.GetCurrentDirectory() + "\\Output");
            commandLineList = new List<string>();
            XmlDocument fuzzyTestInfo = new XmlDocument();
            string testName = string.Empty;
            string fileName = string.Empty;

            fuzzyTestInfo.Load(mapperPath);
            XmlNode root = fuzzyTestInfo.SelectSingleNode("/FuzzyTool");
            foreach (XmlNode testInstance in root.ChildNodes)
            {
                testCount++;
                testName = testInstance.Attributes["TestName"].Value;
                lines[2] = "    class " + testName + " : MP_FuzzyBase";
                fileName = outputPath + "\\" + testName + ".cs";
                File.WriteAllLines(fileName, lines);
                if (testCount == root.ChildNodes.Count)
                    commandLineList.Add("Execute.exe " + testName + " SD DP");
                else
                    commandLineList.Add("Execute.exe " + testName + " SD DP" + ",");
            }
            File.WriteAllLines(outputPath + "\\CommandLines.txt", commandLineList);
        }
    }
}
