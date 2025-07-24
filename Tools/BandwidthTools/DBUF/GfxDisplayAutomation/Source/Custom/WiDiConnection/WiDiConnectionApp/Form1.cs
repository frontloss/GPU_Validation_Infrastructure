using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Text;
using IntelWiDiLib;
using System.Windows.Forms;
using System.Xml;
using System.IO;
using System.Threading;
using System.Runtime.InteropServices;

namespace WiDiConnectionApp
{
    public partial class Form1 : Form
    {
        WiDiExtensionsClass WiDi;
        public Form1()
        {
            
            InitializeComponent();
            DoConnection();
        }

        void DoConnection()
        {
            string msg;
            string adapterId = string.Empty;
            #region Get Adapter from Map file
            try
            {
                XmlDocument benchmarkValue = new XmlDocument();
                benchmarkValue.Load("Mapper\\WiDiData.map");
                XmlNode eventBenchmarkRoot = benchmarkValue.SelectSingleNode("/Data/Adapter");
                adapterId = eventBenchmarkRoot.Attributes["ReceverId"].Value.ToUpper();
            }
            catch { }
            if (string.IsNullOrEmpty(adapterId))
            {
                Logger.WriteLog("Found adapter ID {0} from WiDiData.map file");
            }
            #endregion

            WiDiParam widiParam = new WiDiParam();
            widiParam.AdapterIds = new List<string>();

            File.Delete(Logger.WidiLogPath);
            File.Delete("WiDiConnectionLogs.xml");
            Logger.WriteLog("******************* WIDI CONNECTION LOG *******************");
            Logger.WriteLog("");

            KillProcess();
            Logger.WriteLog("Registring Interop.IntelWiDiLib.dll");
            if (!Directory.Exists(@"C:\Program Files (x86)\Intel Corporation\Intel WiDi Extensions SDK"))
            {
                string fileName = Directory.GetCurrentDirectory() + @"\WiDi Extensions SDK 1.1.0.10 PV" + @"\setup";
                StartProcess(fileName, "/passive").WaitForExit();
            }
            Logger.WriteLog("Registration completed");
            Logger.WriteLog("Registration completed");

            try
            {
                WiDi = new WiDiExtensionsClass();
                Thread.Sleep(2000);
            }
            catch (COMException ex)
            {
                msg = "Unable to find the Intel WiDi Extensions Library! Please"
                 + "make sure that IntelWiDiExtensions.dll has been registered on the system. ("
                 + ex.ErrorCode.ToString() + ")";
                Logger.WriteLog(msg);
            }
            catch (Exception ex)
            {
                msg = "An unknown error occurred during startup. Please contact support." + ex.ToString();
                Logger.WriteLog(msg);
            }

            if (InitializeAdapter(widiParam))
            {
                ScanAdapters(widiParam);
                if (widiParam.AdapterIds.Count > 0)
                {
                    if (widiParam.AdapterIds.Select(DT => DT.Contains(adapterId.ToUpper())).First())
                        Connect(widiParam, widiParam.AdapterIds.Find(DT => DT.Contains(adapterId)));
                    else
                    {
                        foreach (string adapter in widiParam.AdapterIds)
                        {
                            Connect(widiParam, adapter);
                            if (widiParam.ConnectionStatus == Initialize.Success)
                            {
                                break;
                            }
                        }
                    }
                    if (widiParam.ConnectionStatus != Initialize.Success)
                        Logger.WriteLog("WiDi connection failed");
                    else
                        Logger.WriteLog("connected...");
                }
                else
                    Logger.WriteLog("could not find any adapter on the system to connect");
            }
            WriteXMLData(widiParam);
        }

        private void KillProcess()
        {
            Process[] pocList = Process.GetProcessesByName("WiDiConnectionApp");
            foreach (Process widiProcess in pocList)
            {
                string arg = "/pid " + widiProcess.Id;
                Process.Start("TASKKILL", arg);
            }
        }

        private void WriteXMLData(WiDiParam widiParam)
        {
            System.Xml.Serialization.XmlSerializer writer =
                new System.Xml.Serialization.XmlSerializer(typeof(WiDiParam));
            System.IO.StreamWriter file = new System.IO.StreamWriter("WiDiConnectionLogs.xml");
            writer.Serialize(file, widiParam);
            file.Close();
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

        private void convertWiDiReasonCodetoString(int h, out string s)
        {
            if (h == (int)IntelWiDiLib.ReasonCode.RC_SUCCESS)
                s = "WiDi RC:  Success";
            else if (h == (int)IntelWiDiLib.ReasonCode.RC_UNKNOWN)
                s = "WiDi RC:  RC_UNKNOWN";
            else if (h == (int)IntelWiDiLib.ReasonCode.RC_ADAPTER_NOT_FOUND)
                s = "WiDi RC:  RC_ADAPTER_NOT_FOUND";
            else if (h == (int)IntelWiDiLib.ReasonCode.RC_CONNECTION_CANCELLED)
                s = "WiDi RC:  RC_CONNECTION_CANCELLED";
            else if (h == (int)IntelWiDiLib.ReasonCode.RC_USER_DISCONNECTED)
                s = "WiDi RC:  RC_USER_DISCONNECTED";
            else if (h == (int)IntelWiDiLib.ReasonCode.RC_CONNECTION_DROPPED)
                s = "WiDi RC:  RC_CONNECTION_DROPPED";
            else if (h == (int)IntelWiDiLib.ReasonCode.RC_WIDI_APP_NOT_FOUND)
                s = "WiDi RC:  RC_WIDI_APP_NOT_FOUND";
            else if (h == (int)IntelWiDiLib.ReasonCode.RC_WIDI_FAILED_TO_START)
                s = "WiDi RC:  RC_WIDI_FAILED_TO_START";
            else if (h == (int)IntelWiDiLib.ReasonCode.RC_WIDI_FAILED_TO_CONNECT)
                s = "WiDi RC:  RC_WIDI_FAILED_TO_CONNECT";
            else if (h == (int)IntelWiDiLib.ReasonCode.RC_WIDI_FAILED_TO_DISCONNECT)
                s = "WiDi RC:  RC_WIDI_FAILED_TO_DISCONNECT";
            else if (h == (int)IntelWiDiLib.ReasonCode.RC_ALREADY_CONNECTED)
                s = "WiDi RC:  RC_ALREADY_CONNECTED";
            else if (h == (int)IntelWiDiLib.ReasonCode.RC_NOT_CONNECTED)
                s = "WiDi RC:  RC_NOT_CONNECTED";
            else if (h == (int)IntelWiDiLib.ReasonCode.RC_SCAN_IN_PROGRESS)
                s = "WiDi RC:  RC_SCAN_IN_PROGRESS";
            else if (h == (int)IntelWiDiLib.ReasonCode.RC_UNABLE_TO_START_SCAN)
                s = "WiDi RC:  RC_UNABLE_TO_START_SCAN";
            else if (h == (int)IntelWiDiLib.ReasonCode.RC_NO_DEFAULT_ADAPTER)
                s = "WiDi RC:  RC_NO_DEFAULT_ADAPTER";
            else if (h == (int)IntelWiDiLib.ReasonCode.RC_WIDI_APPLICATION_ERROR)
                s = "WiDi RC:  RC_WIDI_APPLICATION_ERROR";
            else if (h == (int)IntelWiDiLib.ReasonCode.RC_CONNECT_CANCELLED_SCAN)
                s = "WiDi RC:  RC_CONNECT_CANCELLED_SCAN";
            else if (h == (int)IntelWiDiLib.ReasonCode.RC_INTERNAL_ERROR)
                s = "WiDi RC:  RC_INTERNAL_ERROR";
            else
                s = "WiDi RC:  Unknown reason code";
        }

        private void convertWiDiResulttoString(int h, out string s)
        {
            if (h == (int)IntelWiDiLib.ReturnCode.S_SUCCESS)
                s = "WiDi:  Success";
            else if (h == (int)IntelWiDiLib.ReturnCode.S_ALREADY_INITIALIZED)
                s = "WiDi Success:  S_ALREADY_INITIALIZED";
            else if (h == (int)IntelWiDiLib.ReturnCode.E_NOT_INITIALIZED)
                s = "WiDi Erorr:  E_NOT_INITIALIZED";
            else if (h == (int)IntelWiDiLib.ReturnCode.E_WIDI_AGENT_NOT_FOUND)
                s = "WiDi Error:  E_WIDI_AGENT_NOT_FOUND";
            else if (h == (int)IntelWiDiLib.ReturnCode.E_NOT_CONNECTED)
                s = "WiDi Error:  E_NOT_CONNECTED";
            else if (h == (int)IntelWiDiLib.ReturnCode.E_ADAPTER_NOT_FOUND)
                s = "WiDi Error:  E_ADAPTER_NOT_FOUND";
            else if (h == (int)IntelWiDiLib.ReturnCode.E_INTERNAL_ERROR)
                s = "WiDi Error:  E_INTERNAL_ERROR";
            else if (h == (int)IntelWiDiLib.ReturnCode.E_INVALID_PARAMETER)
                s = "WiDi Error:  E_INVALID_PARAMETER";
            else if (h == (int)IntelWiDiLib.ReturnCode.E_CONNECTED)
                s = "WiDi Error:  E_CONNECTED";
            else if (h == (int)IntelWiDiLib.ReturnCode.E_KEY_NOT_SUPPORTED)
                s = "WiDi Error:  E_KEY_NOT_SUPPORTED";
            else if (h == (int)IntelWiDiLib.ReturnCode.E_NOT_IMPL)
                s = "WiDi Error:  E_NOT_IMPL";
            else if (h == (int)IntelWiDiLib.ReturnCode.E_NO_SCAN_WHILE_CONNECTED)
                s = "WiDi Error:  E_NO_SCAN_WHILE_CONNECTED";
            else if (h == (int)IntelWiDiLib.ReturnCode.E_ALREADY_INITIALIZED)
                s = "WiDi Error:  E_ALREADY_INITIALIZED";
            else if (h == (int)IntelWiDiLib.ReturnCode.E_INVALID_WIDIVERSION)
                s = "WiDi Error:  E_INVALID_WIDIVERSION";
            else if (h == (int)IntelWiDiLib.ReturnCode.E_SCAN_IN_PROGRESS)
                s = "WiDi Error:  E_SCAN_IN_PROGRESS";
            else if (h == (int)IntelWiDiLib.ReturnCode.E_UNABLE_TO_START_SCAN)
                s = "WiDi Error:  E_UNABLE_TO_START_SCAN";
            else if (h == (int)IntelWiDiLib.ReturnCode.E_NO_DEFAULT_ADAPTER)
                s = "WiDi Error:  E_NO_DEFAULT_ADAPTER";
            else if (h == (int)IntelWiDiLib.ReturnCode.E_WIDI_APPLICATION_ERROR)
                s = "WiDi Error:  E_WIDI_APPLICATION_ERROR";
            else if (h == (int)IntelWiDiLib.ReturnCode.E_INITIALIZING)
                s = "WiDi Error:  E_INITIALIZING";
            else if (h == (int)IntelWiDiLib.ReturnCode.E_ADAPTER_TYPE)
                s = "WiDi Error:  E_ADAPTER_TYPE";
            else if (h == (int)IntelWiDiLib.ReturnCode.E_INVALID_DISPLAY_TOPOLOGY)
                s = "WiDi Error:  E_INVALID_DISPLAY_TOPOLOGY";
            else if (h == (int)IntelWiDiLib.ReturnCode.E_MUST_SCAN)
                s = "WiDi Error:  E_MUST_SCAN";
            else
                s = "WiDi Error:  Unknown error";
        }

        private bool InitializeAdapter(WiDiParam widiParam)
        {
            try
            {
                IntPtr handle = Handle;
                Logger.WriteLog("window handle " + handle);
                WiDi.Initialize((uint)handle.ToInt64());
                widiParam.InitializeStatus = Initialize.Success;
                Logger.WriteLog("Initialization: S_SUCCESS");
                Thread.Sleep(4000);
                return true;
            }
            catch (COMException ex)
            {
                string sTemp;
                convertWiDiResulttoString(ex.ErrorCode, out sTemp);
                widiParam.InitializeStatus = Initialize.Fail;
                Logger.WriteLog("Initialization Failed, error code  " + sTemp);
            }
            catch (Exception ex)
            {
                widiParam.InitializeStatus = Initialize.Fail;
                Logger.WriteLog("An unknown error occurred during startup. Please contact support." + ex.ToString());
            }
            return false;
        }

        private void ScanAdapters(WiDiParam widiParam)
        {
            try
            {
                WiDi.StartScanForAdapters();
                Thread.Sleep(4000);
                string adapterList;
                WiDi.GetAdapterList("AllOnTheNetwork", "All", out adapterList);
                if (string.IsNullOrEmpty(adapterList))
                {
                    Logger.WriteLog("Could not find any adapter");
                    return;
                }
                string[] IDs = adapterList.Split(',');
                List<string> filterlist = FilterAdapterList();
                foreach (string eachId in IDs)
                {
                    if (filterlist.Count > 0)
                    {
                        foreach (string temp in filterlist)
                        {
                            if (eachId.Contains(temp.ToUpper()))
                                widiParam.AdapterIds.Add(eachId.Trim());
                        }
                    }
                    else
                        widiParam.AdapterIds.Add(eachId.Trim());
                }
                Logger.WriteLog("Scan Started S_SUCCESS");
            }
            catch (COMException ex)
            {
                string sTemp;
                convertWiDiResulttoString(ex.ErrorCode, out sTemp);
                Logger.WriteLog("Scan Failed, error code  " + sTemp);
            }
        }

        private List<string> FilterAdapterList()
        {
            List<string> monIDList = new List<string>();
            Process monitorID_process = StartProcess("devcon.exe", "find *");
            while (!monitorID_process.StandardOutput.EndOfStream)
            {
                string line = monitorID_process.StandardOutput.ReadLine().ToLower();
                if (line.Contains("swd\\wifidirect"))
                {
                    string[] Info = line.Split(':');
                    if (!string.IsNullOrEmpty(Info.Last()))
                    {
                        string[] receverID = Info.Last().Trim().Split(new[] { ' ', '-' });
                        monIDList.Add(receverID[1]);
                    }
                }
            }
            return monIDList;
        }

        private bool Connect(WiDiParam widiParam, string adapter)
        {
            Logger.WriteLog("Try to connect with adapter " + adapter);
            try
            {
                WiDi.StartConnectionToAdapter(adapter, 0, 0, SM.Invalid);
                widiParam.ConnectionStatus = Initialize.Success;
            }
            catch (COMException ex)
            {
                string sTemp;
                convertWiDiResulttoString(ex.ErrorCode, out sTemp);
                Logger.WriteLog("StartConnectiontoAdapter Failed, error code  " + sTemp);
                widiParam.ConnectionStatus = Initialize.Fail;
            }
            return false;
        }

    }
}
