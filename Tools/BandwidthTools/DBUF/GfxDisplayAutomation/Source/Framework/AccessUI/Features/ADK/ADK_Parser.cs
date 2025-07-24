namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Xml;
    using System.Linq;
    using System.Collections.Generic;
    using System.Text.RegularExpressions;

    internal class ADK_Parser : FunctionalBase
    {
        public List<ADKInformation> parseData;
        private string ResultFilePath;

        internal void Init(string csvFilePath)
        {
            ResultFilePath = csvFilePath;
            Log.Verbose("Featching result from {0} path", csvFilePath);
            if (csvFilePath == string.Empty)
            {
                Log.Abort("File not found !!!!");
            }
            parseData = new List<ADKInformation>();
            ManipulateBenchmarkValue();
            ParseData();
        }

        private void ManipulateBenchmarkValue()
        {
            XmlDocument benchmarkValue = new XmlDocument();
            benchmarkValue.Load("Mapper\\ADK_Benchmark_Data.map");
            XmlElement root = benchmarkValue.DocumentElement;
            foreach (XmlNode fieldName in root.ChildNodes)
            {
                ADKInformation data = new ADKInformation();
                data.noOfDuration = Convert.ToInt16(root.Attributes["iteration"].Value);
                data.TestContent = fieldName.Name;

                foreach (XmlNode attribute in fieldName.Attributes)
                {
                    if (attribute.Name == "field")
                        data.field = attribute.Value;
                    else if (attribute.Name == "activity")
                        data.activity = attribute.Value;
                    else
                        data.activity = "";
                }
                foreach (XmlNode platform in fieldName.ChildNodes)
                {
                    if (base.MachineInfo.Platform == Convert.ToString(platform.Attributes["id"].Value))
                    {
                        if (Convert.ToString(platform.Attributes.GetNamedItem("key")) == "")
                        {
                            data.keys = base.MachineInfo.Driver.DeviceID;
                        }
                        else
                        {
                            data.keys = platform.Attributes["key"].Value;
                        }
                        foreach (XmlAttribute OS in platform.FirstChild.Attributes)
                        {
                            if (base.MachineInfo.OS.Type == OS.Name)
                                data.benchMarkValue = Convert.ToInt16(OS.Value);
                        }
                        break;
                    }
                }
                parseData.Add(data);
            }

        }

        private void ParseData()
        {
            string[] lines = File.ReadAllLines(ResultFilePath);
            bool textFound = false;
            List<string> temp;
            foreach (ADKInformation benchvalue in parseData)
            {
                temp = new List<string>();
                textFound = false;
                foreach (string eachFileLine in lines)
                {
                    if (eachFileLine.Contains(benchvalue.field))
                        textFound = true;
                    if (textFound)
                        temp.Add(eachFileLine);
                    if (textFound)
                        if (eachFileLine == string.Empty)
                            break;
                }
                temp.RemoveAt(0);
                Parse(benchvalue, temp);
            }
        }

        private void Parse(ADKInformation benchvalue, List<string> lines)
        {
            string[] data;
            //double sum = 0;
            List<double> responsivenessData = new List<double>();
            benchvalue.Result_Data = null;
            bool found = false;
            foreach (string line in lines)
            {
                data = line.Trim().Split(new[] { ',', '\t' });
                if (line.ToLower().Contains(benchvalue.keys.ToLower()))
                {
                    if (benchvalue.activity != null)
                    {
                        if (line.Contains(benchvalue.activity))
                        {
                            Log.Message("Attribute {0} and key {1} found", benchvalue.TestContent, benchvalue.keys);
                            for (int durationCount = 1; durationCount <= benchvalue.noOfDuration; durationCount++)
                            {
                                string value = Convert.ToString(data[data.Count() - durationCount]);
                                if (value.Contains('*'))
                                {
                                    value = value.Split('*').First();
                                }
                                benchvalue.Result_Data += value + ", ";
                                responsivenessData.Add(Convert.ToDouble(value));
                            }
                            benchvalue.average = GetOlympicAvg(responsivenessData, benchvalue.benchMarkValue);
                            if (benchvalue.average != 0 && benchvalue.average < benchvalue.benchMarkValue)
                            {
                                benchvalue.status = "PASS";
                                Log.Success("{0} Benchmark: {1} Average: {2}", benchvalue.TestContent,
                                benchvalue.benchMarkValue, benchvalue.average);
                            }
                            else
                            {
                                benchvalue.status = "FAIL";
                                Log.Fail("{0} Benchmark: {1} Average: {2}", benchvalue.TestContent,
                                benchvalue.benchMarkValue, benchvalue.average);
                            }
                            found = true;
                        }
                    }
                    else
                    {
                        Log.Message("Attribute {0} and key {1} found", benchvalue.TestContent, benchvalue.keys);
                        for (int durationCount = 1; durationCount <= benchvalue.noOfDuration; durationCount++)
                        {
                            string value = Convert.ToString(data[data.Count() - durationCount]);
                            if (value.Contains('*'))
                            {
                                value = value.Split('*').First();
                            }
                            else if (value == "")
                            {
                                value = "0";
                            }
                            benchvalue.Result_Data += value + ", ";
                            responsivenessData.Add(Convert.ToDouble(value));
                        }
                        benchvalue.average = GetOlympicAvg(responsivenessData, benchvalue.benchMarkValue);
                        if (benchvalue.average != 0 && benchvalue.average < benchvalue.benchMarkValue)
                        {
                            benchvalue.status = "PASS";
                            Log.Success("{0} Benchmark: {1} Average: {2}", benchvalue.TestContent,
                                benchvalue.benchMarkValue, benchvalue.average);
                        }
                        else
                        {
                            benchvalue.status = "FAIL";
                            Log.Fail("{0} Benchmark: {1} Average: {2}", benchvalue.TestContent,
                                benchvalue.benchMarkValue, benchvalue.average);
                        }
                        found = true;
                    }
                }
                if (found)
                    break;
            }
            if (benchvalue.status == null)
            {
                benchvalue.Result_Data = "0";
                benchvalue.status = "NOT RUN";
                Log.Fail(true, "{0} not initiated on the test system", benchvalue.TestContent);
            }
        }

        private double GetOlympicAvg(List<double> responsivenessData, int benchvalue)
        {
            double sum = 0;
            double higherResponsivenessValue = responsivenessData.Max();
            if (higherResponsivenessValue > benchvalue)
            {
                Log.Verbose("Taking olympic average by removing max {0} and min {1} values", responsivenessData.Max(), responsivenessData.Min());
                responsivenessData.Remove(responsivenessData.Min());
                responsivenessData.Remove(responsivenessData.Max());
            }
            foreach (double value in responsivenessData)
            {
                sum = sum + value;
            }
            Log.Verbose("taking average of {0} data", responsivenessData.Count.ToString());
            return Math.Round(sum / responsivenessData.Count, 2, MidpointRounding.AwayFromZero);
        }
    }
}
