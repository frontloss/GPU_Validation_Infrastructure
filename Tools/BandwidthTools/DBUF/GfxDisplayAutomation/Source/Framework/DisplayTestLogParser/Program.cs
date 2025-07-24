namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Xml.Linq;
    using System.Collections.Generic;
    using System.Text.RegularExpressions;

    class Program
    {
        static bool _alertsFound = false;
        static string _testName = string.Empty;

        enum MeasurementCriteria
        {
            Pass,
            Fail,
            Sporadic,
            Skip,
            Error,
            TDRPass,
            TDRFail
        }
        enum ReportResult
        {
            Passed,
            Failed,
            Custom,
            Running
        }
        enum TestResult
        {
            P,
            F,
            E
        }
        static void Main(string[] args)
        {
            TestResult testResult = TestResult.E;
            string resultDesc = string.Empty;
            Dictionary<MeasurementCriteria, long> logResults = new Dictionary<MeasurementCriteria, long>();
            Enum.GetNames(typeof(MeasurementCriteria)).ToList().ForEach(c => logResults.Add((MeasurementCriteria)Enum.Parse(typeof(MeasurementCriteria), c, true), 0));

            try
            {
                if (null != args && !args.Length.Equals(0))
                {
                    if (File.Exists(args.First()))
                    {
                        string testXMLFile = string.Empty;
                        StreamReader reader = File.OpenText(args.First());
                        string line = string.Empty;
                        while ((line = reader.ReadLine()) != null)
                        {
                            Match testNameCriteria = Regex.Match(line, @"^Detailed.+:\s(.+)");
                            if (testNameCriteria.Success && testNameCriteria.Groups.Count.Equals(2))
                            {
                                testXMLFile = testNameCriteria.Groups[1].Value;
                                break;
                            }
                        }
                        reader.Close();
                        _testName = testXMLFile.Replace(".xml", string.Empty);
                        if (File.Exists(testXMLFile))
                        {
                            XDocument xDoc = XDocument.Load(testXMLFile);
                            XElement xSummary = xDoc.Root.Element("Summary");
                            XElement xBreakup = xSummary.Element("Breakup");
                            IEnumerable<XElement> xLogs = xDoc.Root.Element("Report").Elements("Log");

                            logResults[MeasurementCriteria.Pass] = ToLong(xBreakup.Element("Pass").Value);
                            logResults[MeasurementCriteria.Fail] = ToLong(xBreakup.Element("Fail").Value);
                            XElement xSporadic = xBreakup.Element("Sporadic");
                            if (null != xSporadic)
                                logResults[MeasurementCriteria.Sporadic] = ToLong(xSporadic.Value);
                            else
                            {
                                xSporadic = xLogs.Where(e => e.Element("Type").Value.Equals("Alert")).FirstOrDefault();
                                if (null != xSporadic)
                                {
                                    logResults[MeasurementCriteria.Sporadic] += 1;
                                    _alertsFound = true;
                                }
                            }

                            testResult = GetTestResult(xSummary.Element("Result").Value);

                            string failMsg = string.Empty;
                            XElement xFailMsg = xBreakup.Element("FirstFailMsg");
                            if (null == xFailMsg)
                            {
                                xFailMsg = xLogs.Where(e => e.Element("Type").Value.Equals("Fail")).FirstOrDefault();
                                if (null != xFailMsg)
                                    failMsg = xFailMsg.Element("Data").Value;
                            }
                            else
                                failMsg = xFailMsg.Value;

                            GeneratePAVEXML(logResults, RecordFailMessage(logResults, testResult, failMsg), testResult);
                        }
                        else
                        {
                            line = string.Empty;
                            reader = File.OpenText(args.First());
                            while ((line = reader.ReadLine()) != null)
                            {
                                Match measurementLine = Regex.Match(line, @"^#.+");
                                if (measurementLine.Success)
                                {
                                    Match measurementValue = Regex.Match(measurementLine.Value, @"^.+\s.+\s(.+):\s(\d+)");
                                    if (measurementValue.Success && measurementValue.Groups.Count.Equals(3))
                                    {
                                        MeasurementCriteria criteria = (MeasurementCriteria)Enum.Parse(typeof(MeasurementCriteria), measurementValue.Groups[1].Value, true);
                                        logResults[criteria] = ToLong(measurementValue.Groups[2].Value);
                                    }
                                }

                                Match resultLine = Regex.Match(line, @"^\*+.+\t(.+?)\*+");
                                if (resultLine.Success && resultLine.Groups.Count.Equals(2))
                                {
                                    testResult = GetTestResult(resultLine.Groups[1].Value);
                                    resultDesc = RecordFailMessage(logResults, testResult);
                                }
                            }

                            GeneratePAVEXML(logResults, resultDesc, testResult);
                        }
                    }
                    else
                        throw new Exception(string.Format("No {0} found!", args.First()));
                }
                else
                    throw new Exception("No TestLog file argument passed in TV!");
            }
            catch (Exception ex)
            {
                string failDesc = ex.Message;
                if (null != ex.InnerException)
                    failDesc = string.Concat(failDesc, "<br />Inner Ex:: ", ex.InnerException.Message);
                GeneratePAVEXML(logResults, RecordFailMessage(logResults, testResult, failDesc), testResult);
            }
        }
        static void GeneratePAVEXML(Dictionary<MeasurementCriteria, long> argLogResults, string argResultDesc, TestResult argTestResult)
        {
            string paveResultXML = string.Concat(Directory.GetParent(Directory.GetCurrentDirectory()).Root, "PAVEResult.XML");
            string testResultStr = "TestResult";
            string measurementsStr = "Measurements";
            XDocument xDoc =
                new XDocument(
                    new XElement("ROOT",
                        new XElement(testResultStr,
                            new XElement("Description", argResultDesc),
                            new XElement(measurementsStr),
                            new XElement("FilePathList"),
                            new XElement("FinalResult", argTestResult)
                            )
                    ));

            argLogResults.ToList().ForEach(kV =>
            {
                if (kV.Key != MeasurementCriteria.Sporadic)
                {
                    xDoc.Root.Element(testResultStr).Element(measurementsStr).Add(
                        new XElement("Measurement",
                            new XAttribute("name", string.Concat(kV.Key, "Count")), kV.Value)
                            );
                }
            });

            xDoc.Save(paveResultXML);
        }
        static string RecordFailMessage(Dictionary<MeasurementCriteria, long> argLogResults, TestResult argResult)
        {
            return RecordFailMessage(argLogResults, argResult, string.Empty);
        }
        static string RecordFailMessage(Dictionary<MeasurementCriteria, long> argLogResults, TestResult argResult, string argFailDesc)
        {
            if (argResult == TestResult.F)
                return RecordFailMessage(string.Empty, argFailDesc);
            else if (argResult == TestResult.E)
            {
                argLogResults[MeasurementCriteria.Error] += 1;
                return RecordFailMessage("Test Errored : ", argFailDesc);
            }
            else if (argResult == TestResult.P)
            {
                if (!argLogResults[MeasurementCriteria.Sporadic].Equals(0))
                    return RecordFailMessage("Test Passed : ", _alertsFound ? "Alert statements observed in log!" : "Sporadicness observed!");
                else
                    return RecordFailMessage("Test Passed : ", string.Concat(_testName, " successful"));
            }
            else
                return string.Empty;
        }
        static string RecordFailMessage(string argResultDesc, string argFailDesc)
        {
            if (string.IsNullOrEmpty(argFailDesc))
                return string.Concat(argResultDesc, "no description found!");
            else
                return string.Concat(argResultDesc, argFailDesc);
        }
        static TestResult GetTestResult(string argResult)
        {
            ReportResult result = ReportResult.Running;
            Dictionary<ReportResult, TestResult> testResults = new Dictionary<ReportResult, TestResult>();
            testResults.Add(ReportResult.Custom, TestResult.E);
            testResults.Add(ReportResult.Failed, TestResult.F);
            testResults.Add(ReportResult.Passed, TestResult.P);
            testResults.Add(ReportResult.Running, TestResult.E);
            if (Enum.TryParse(argResult, true, out result))
                return testResults[result];
            return testResults[ReportResult.Running];
        }
        static long ToLong(string argContext)
        {
            long val = 0;
            if (long.TryParse(argContext, out val))
                return val;
            return 0;
        }
    }
}