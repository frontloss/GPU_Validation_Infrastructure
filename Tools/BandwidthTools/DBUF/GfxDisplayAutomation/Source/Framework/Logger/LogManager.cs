namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Xml;
    using System.Text;
    using System.Linq;
    using System.Xml.Xsl;
    using System.Xml.Linq;
    using System.Xml.XPath;
    using System.Collections.Generic;

    internal class LogManager
    {
        private ConsoleFormatter _consoleFormatter = null;
        private long _logNodeIndex = 1;

        internal string RootNodeText { get; set; }
        internal string LogSummaryText { get; set; }
        internal string LogReportText { get; set; }
        internal TestResultList TestResults { get; set; }
        internal string TestName { get; set; }
        internal int LogLevel { get; set; }
        internal bool PostReboot { get; set; }
        internal Func<string> CaptureScreenMethod { get; set; }
        internal bool GenerateDisplayTestLogFile { get; set; }
        internal bool PrintVerboseOnConsole { get; set; }
        internal string CustomPathName { get; set; }
        internal bool IsAlternateLogFile { get; set; }
        internal long LogNodeIndex
        {
            get { return this._logNodeIndex++; }
            set { this._logNodeIndex = value; }
        }
        internal string AlternateFilePath
        {
            get { return string.Concat(Directory.GetCurrentDirectory(), "\\", this.TestName + "_backup", ".xml"); }
        }
        internal string XmlLogDocPath
        {
            get { return string.Concat(Directory.GetCurrentDirectory(), "\\", this.TestName, ".xml"); }
        }
        internal string HTMLReportDocPath
        {
            get { return string.Concat(Directory.GetCurrentDirectory(), "\\", this.TestName, ".html"); }
        }
        internal string XmlCustomLogDocPath
        {
            get { return string.Concat(this.CustomPathName, "\\", this.TestName, ".xml"); }
        }
        internal string HTMLCustomReportDocPath
        {
            get { return string.Concat(this.CustomPathName, "\\", this.TestName, ".html"); }
        }
        internal string TextReportDocPath
        {
            get { return string.Concat(Directory.GetCurrentDirectory(), "\\DisplayTest.log"); }
        }
        internal string HTMLStyle
        {
            get { return string.Concat(Directory.GetCurrentDirectory(), "\\", "HTMLFormatter.xsl"); }
        }
        internal string TextStyle
        {
            get { return string.Concat(Directory.GetCurrentDirectory(), "\\", "TextFormatter.xsl"); }
        }
        internal LogManager()
        {
            this.RootNodeText = "ExecutionLog";
            this.LogSummaryText = "Summary";
            this.LogReportText = "Report";
            this._consoleFormatter = new ConsoleFormatter();
            this.TestResults = new TestResultList();
        }
        internal void GenerateReport()
        {
            if (File.Exists(Path.Combine(Directory.GetCurrentDirectory(), "RunningBatch.flg")))
            {
                string currentTestXML = this.XmlLogDocPath;
                //  string xmlFilePath = Path.Combine(Directory.GetCurrentDirectory(), "ConfigurableTest.xml");
                string batchFileName = "";
                DirectoryInfo dirInfo1 = new DirectoryInfo(Directory.GetCurrentDirectory());
                List<FileInfo> fileInfoList1 = dirInfo1.GetFiles("*.flg").ToList();
                ;
                foreach (FileInfo curFileInfo in fileInfoList1)
                {
                    if (curFileInfo.Name.StartsWith("BatchFileName"))
                    {
                        batchFileName = curFileInfo.Name.Split('.').First().Trim();
                        batchFileName = batchFileName.Remove(0, 13);
                    }
                }

                string xmlFilePath = Path.Combine(Directory.GetCurrentDirectory(), batchFileName + ".xml");
                if (!File.Exists(xmlFilePath))
                {
                    string argTestName = batchFileName;
                    string argLogPath = "";
                    LogManager logManager = new LogManager();
                    logManager.TestName = string.IsNullOrEmpty(argLogPath) ? argTestName : (argTestName + DateTime.Now.ToString("yyyyMMddHHmmss"));
                    // logManager.PathName = string.IsNullOrEmpty(argLogPath) ? Directory.GetCurrentDirectory() : argLogPath;
                    //logManager.DisplayTest = string.IsNullOrEmpty(argLogPath) ? "DisplayTest.log " : string.Concat("DisplayTest_", logManager.TestName, ".log");
                    logManager.LogLevel = 5;
                    logManager.PostReboot = false;
                    logManager.PrintVerboseOnConsole = true;
                    logManager.GenerateDisplayTestLogFile = true;
                    if (logManager.GenerateDisplayTestLogFile)
                        logManager.GenerateDisplayTestLog();
                    LogList logList = new LogList(logManager);
                }

                XDocument doc1 = XDocument.Load(xmlFilePath);
                XElement rootElement1 = doc1.Root;
                IEnumerable<XElement> executionLog1 = rootElement1.Descendants("ExecutionLog");
                IEnumerable<XElement> report1 = rootElement1.Descendants("Report");
                IEnumerable<XElement> log1 = rootElement1.Descendants("Log");
                Log.Verbose("the count is {0}", log1.Count());
                int logCount = log1.Count();
                XDocument doc = XDocument.Load(this.XmlLogDocPath);
                XElement rootElement = doc.Root;
                IEnumerable<XElement> executionLog = rootElement.Descendants("ExecutionLog");
                IEnumerable<XElement> report = rootElement.Descendants("Report");
                IEnumerable<XElement> log = rootElement.Descendants("Log");

                foreach (XElement currentLog in log)
                {
                    if (logCount > 1)
                    {
                        XElement idElement = currentLog.Element("Id");
                        idElement.Value = logCount.ToString();
                        logCount++;
                    }
                    report1.First().Add(currentLog);
                }
                doc1.Save(xmlFilePath);
                if (!File.Exists(Path.Combine(Directory.GetCurrentDirectory(), "RunningLastTestInBatch.flg")))
                {
                    return;
                }
                else
                {
                    this.TestName = batchFileName;
                    //delete the xml files for each test
                    DirectoryInfo dirInfo = new DirectoryInfo(Directory.GetCurrentDirectory());
                    List<FileInfo> fileInfoList = dirInfo.GetFiles("*.xml").ToList();
                    foreach (FileInfo curFileInfo in fileInfoList)
                    {
                        if (curFileInfo.Name != batchFileName + ".xml")
                        {
                            curFileInfo.Delete();
                        }
                    }
                }
            }
            TestResult result = this.GetResult();
            XDocument xDoc = XDocument.Load(this.XmlLogDocPath);
            xDoc.Root.Element(this.LogSummaryText).Element("Result").Value = result.ToString().ToUpper();
            xDoc.Root.Element(this.LogSummaryText).Element("Breakup").Element("Pass").Value = this.TestResults[TestResult.Passed].ToString();
            xDoc.Root.Element(this.LogSummaryText).Element("Breakup").Element("Fail").Value = this.TestResults[TestResult.Failed].ToString();
            xDoc.Root.Element(this.LogSummaryText).Element("Breakup").Element("Sporadic").Value = this.TestResults[TestResult.Sporadic].ToString();

            string firstFailMsg = string.Empty;
            XElement failElement = this.GetExistingElements(xDoc).Where(e => e.Element("Type").Value.Equals(LogType.Fail.ToString())).FirstOrDefault();
            if (null != failElement)
                firstFailMsg = failElement.Element("Data").Value;
            xDoc.Root.Element(this.LogSummaryText).Element("Breakup").Element("FirstFailMsg").Value = firstFailMsg;

            XElement firstTimeElement = this.GetExistingElements(xDoc).Where(e => !string.IsNullOrEmpty(e.Element("Timestamp").Value)).FirstOrDefault();
            XElement lastTimeElement = this.GetExistingElements(xDoc).Where(e => !string.IsNullOrEmpty(e.Element("Timestamp").Value)).LastOrDefault();
            if (null != firstTimeElement && null != lastTimeElement)
            {
                DateTime startTime = Convert.ToDateTime(firstTimeElement.Element("Timestamp").Value);
                DateTime endTime = Convert.ToDateTime(lastTimeElement.Element("Timestamp").Value);
                TimeSpan timeSpan = endTime.Subtract(startTime);
                xDoc.Root.Element(this.LogSummaryText).Element("Breakup").Element("RunTime").Value = string.Concat(timeSpan.Hours, "hrs ", timeSpan.Minutes, "mins ", timeSpan.Seconds, "secs ");
            }

            xDoc.Root.Element(this.LogReportText).Add(
                new XElement("Log",
                            new XElement("Id", this.LogNodeIndex),
                            new XElement("Level"),
                            new XElement("Type"),
                            new XElement("Timestamp"),
                            new XElement("Data"),
                            new XElement("Transformable", true)
                            ));
            xDoc.Root.Element(this.LogReportText).Add(
                new XElement("Log",
                            new XElement("Id", this.LogNodeIndex),
                            new XElement("Level"),
                            new XElement("Type"),
                            new XElement("Timestamp"),
                            new XElement("Data"),
                            new XElement("Transformable", true)
                            ));
            xDoc.Save(this.XmlLogDocPath);

            XPathDocument xPathDoc = new XPathDocument(this.XmlLogDocPath);
            XslCompiledTransform xTrans = new XslCompiledTransform();
            xTrans.Load(this.HTMLStyle);

            XmlTextWriter xWriter = new XmlTextWriter(this.HTMLReportDocPath, null);
            xTrans.Transform(xPathDoc, null, xWriter);
            xWriter.Close();

            if (!string.IsNullOrEmpty(this.CustomPathName) && Directory.Exists(this.CustomPathName))
            {
                if (File.Exists(this.HTMLReportDocPath))
                    File.Copy(this.HTMLReportDocPath, this.HTMLCustomReportDocPath);
                if (File.Exists(this.XmlLogDocPath))
                    File.Copy(this.XmlLogDocPath, this.XmlCustomLogDocPath);
            }

            this.GenerateDisplayTestLog(xPathDoc);
        }
        internal void GenerateDisplayTestLog()
        {
            XDocument xDoc =
                new XDocument(
                    new XElement(this.RootNodeText,
                        new XElement(this.LogSummaryText,
                            new XElement("TestName", this.TestName),
                            new XElement("Result", TestResult.Running),
                            new XElement("Breakup",
                                new XElement("Pass", 0),
                                new XElement("Fail", 0),
                                new XElement("Sporadic", 0)
                                )
                            )
                    ));
            Stream xStream = new MemoryStream();
            xDoc.Save(xStream);
            xStream.Position = 0;
            this.GenerateDisplayTestLog(new XPathDocument(xStream));
        }
        internal void GenerateDisplayTestLog(XPathDocument argXPathDoc)
        {
            if (this.GenerateDisplayTestLogFile)
            {
                if (File.Exists(this.TextReportDocPath))
                    File.Delete(this.TextReportDocPath);
                XslCompiledTransform xTrans = new XslCompiledTransform();
                xTrans.Load(this.TextStyle);

                XmlWriter xWriter = XmlWriter.Create(this.TextReportDocPath, xTrans.OutputSettings);
                xTrans.Transform(argXPathDoc, xWriter);
                xWriter.Close();
            }
        }
        internal string CaptureScreenshot()
        {
            if (null != this.CaptureScreenMethod)
                return this.CaptureScreenMethod();
            return string.Empty;
        }
        internal void PaintOnConsole(LogType argType, string argData)
        {
            Console.ForegroundColor = this._consoleFormatter.GetColor(argType);
            Console.WriteLine(argData);
        }
        internal TestResult GetResult()
        {
            TestResult result = TestResult.Passed;
            LogType logType = LogType.Success;
            if (this.TestResults[TestResult.Failed] > 0)
            {
                result = TestResult.Failed;
                logType = LogType.Fail;
            }
            else if (this.TestResults[TestResult.Failed].Equals(0) && this.TestResults[TestResult.Passed].Equals(0))
            {
                result = TestResult.Custom;
                logType = LogType.Custom;
            }
            StringBuilder resultMsg = new StringBuilder("Test ").Append(result)
                .Append("! #Successes::").Append(this.TestResults[TestResult.Passed])
                .Append(", #Failures::").Append(this.TestResults[TestResult.Failed])
                .Append(", #Sporadicness::").Append(this.TestResults[TestResult.Sporadic]);
            this.PaintOnConsole(logType, resultMsg.ToString());
            return result;
        }
        internal IEnumerable<XElement> GetExistingElements(XDocument argXDoc)
        {
            return argXDoc.Root.Element(this.LogReportText).Elements("Log");
        }
    }
}