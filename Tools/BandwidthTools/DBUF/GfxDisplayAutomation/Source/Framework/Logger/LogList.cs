namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Xml.Linq;
    using System.Security;
    using System.Collections.Generic;
    using System.Security.Permissions;
    using System.Diagnostics;

    internal class LogList : List<LogData>
    {
        private LogManager _manager = null;

        internal LogList(LogManager argManager)
        {
            this._manager = argManager;
            string xmlData = null;
            if (File.Exists(this._manager.XmlLogDocPath))
            {
                try
                {
                    xmlData = File.ReadAllText(this._manager.XmlLogDocPath);
                    XDocument xDoc = XDocument.Load(this._manager.XmlLogDocPath);
                }
                catch
                {
                    if (_manager.IsAlternateLogFile)
                    {
                        File.Delete(this._manager.XmlLogDocPath);
                        File.Move(this._manager.AlternateFilePath, this._manager.XmlLogDocPath);
                        xmlData = File.ReadAllText(this._manager.XmlLogDocPath);
                    }
                    else
                        Log.Abort("Unable to parse log file, file got corrupted");
                }
            }
            if (this._manager.PostReboot && File.Exists(this._manager.XmlLogDocPath) && !string.IsNullOrWhiteSpace(xmlData))
            {
                XDocument xDoc = XDocument.Load(this._manager.XmlLogDocPath);
                this.LoadExistingTestResults(xDoc, TestResult.Failed, LogType.Fail);
                this.LoadExistingTestResults(xDoc, TestResult.Passed, LogType.Success);
                this.LoadExistingTestResults(xDoc, TestResult.Sporadic, LogType.Sporadic);
                this._manager.LogNodeIndex = Convert.ToInt32(this._manager.GetExistingElements(xDoc).Last().Element("Id").Value) + 1;
            }
            else
            {
                if (File.Exists(this._manager.XmlLogDocPath))
                    File.Delete(this._manager.XmlLogDocPath);
                this.AssertPermission();
                this.CreateLogDocument(this._manager.LogReportText);
            }
        }
        internal void Record(LogType argType, string argData)
        {
            this.Record(argType, argData, false);
        }
        internal void Record(LogType argType, string argData, bool argIsParent)
        {
            this.Record(argType, argData, false, argIsParent);
        }
        internal void Record(LogType argType, string argData, bool argCaptureScreenShot, bool argIsParent)
        {
            bool transformable = ((int)argType <= this._manager.LogLevel);
            if (this._manager.PrintVerboseOnConsole || transformable)
                this._manager.PaintOnConsole(argType, argData);
            LogData logData = new LogData(argData);
            logData.Transformable = transformable;
            logData.Type = argType;
            if (argCaptureScreenShot)
                logData.Preview = logData.Screenshot = this._manager.CaptureScreenshot();
            logData.Timestamp = DateTime.Now;
            logData.IsParent = argIsParent;
            this.Add(logData);
            this.Flush(logData);
        }

        private void Flush(LogData argLogData)
        {
            if (!File.Exists(this._manager.XmlLogDocPath))
                this.CreateLogDocument(this._manager.LogReportText);

            XDocument xDoc = XDocument.Load(this._manager.XmlLogDocPath);
            xDoc.Root.Element(this._manager.LogReportText).Add(
                new XElement("Log",
                    new XElement("Id", argLogData.Transformable ? this._manager.LogNodeIndex : 0),
                    new XElement("Level", argLogData.IsParent ? "Parent" : "Child"),
                    new XElement("Type", argLogData.Type),
                    new XElement("Timestamp", argLogData.Timestamp.ToString("G")),
                    new XElement("Data", argLogData.Name),
                    new XElement("Transformable", argLogData.Transformable),
                    string.IsNullOrEmpty(argLogData.Screenshot) ? null : new XElement("Screenshot", argLogData.Screenshot),
                    argLogData.Type == LogType.Fail ? new XElement("Error", "Yes") : null,
                    string.IsNullOrEmpty(argLogData.Preview) ? null : new XElement("Preview", argLogData.Preview)
                ));
            xDoc.Save(this._manager.XmlLogDocPath);
            if (_manager.IsAlternateLogFile)
            {
                string arg = "/c copy /v /y " + this._manager.XmlLogDocPath + " " + this._manager.AlternateFilePath;
                StartProcess("cmd.exe", arg).WaitForExit();
            }
        }

        private void CreateLogDocument(string argReportText)
        {
            XDocument xDoc =
                new XDocument(
                    new XElement(this._manager.RootNodeText,
                        new XElement(this._manager.LogSummaryText,
                            new XElement("TestName", this._manager.TestName),
                            new XElement("Result"),
                            new XElement("Breakup",
                                new XElement("Pass"),
                                new XElement("Fail"),
                                new XElement("Sporadic"),
                                new XElement("FirstFailMsg"),
                                new XElement("RunTime")
                                )
                            ),
                        new XElement(argReportText,
                            new XElement("Log",
                                new XElement("Id", this._manager.LogNodeIndex),
                                new XElement("Level"),
                                new XElement("Type"),
                                new XElement("Timestamp"),
                                new XElement("Data"),
                                new XElement("Transformable", true)
                                )
                            )
                    ));
            xDoc.Save(this._manager.XmlLogDocPath);
            if (_manager.IsAlternateLogFile)
            {
                string arg = "/c copy /v /y " + this._manager.XmlLogDocPath + " " + this._manager.AlternateFilePath;
                StartProcess("cmd.exe", arg).WaitForExit();
            }
        }
        private void AssertPermission()
        {
            PermissionSet permissionSet = new PermissionSet(PermissionState.None);
            FileIOPermission ioPermission = new FileIOPermission(FileIOPermissionAccess.Write, this._manager.XmlLogDocPath);
            permissionSet.AddPermission(ioPermission);
        }
        private void LoadExistingTestResults(XDocument argXDoc, TestResult argResult, LogType argType)
        {
            this._manager.TestResults[argResult] = this._manager.GetExistingElements(argXDoc)
                .Where(e => e.Element("Type").Value.Equals(argType.ToString()))
                .Count();
        }

        public Process StartProcess(string argFileName, string arguments)
        {
            ProcessStartInfo processStartInfo = new ProcessStartInfo();
            processStartInfo.RedirectStandardOutput = true;
            processStartInfo.RedirectStandardInput = true;
            processStartInfo.UseShellExecute = false;
            processStartInfo.CreateNoWindow = false;
            processStartInfo.WindowStyle = ProcessWindowStyle.Hidden;
            processStartInfo.FileName = argFileName;
            if (!string.IsNullOrEmpty(arguments))
                processStartInfo.Arguments = arguments;
            Process process = new Process();
            process.StartInfo = processStartInfo;
            process.Start();
            return process;
        }
    }
}