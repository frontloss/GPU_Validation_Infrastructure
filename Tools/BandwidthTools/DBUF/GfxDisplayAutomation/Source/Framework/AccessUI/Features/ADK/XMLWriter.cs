namespace Intel.VPG.Display.Automation
{
    using System.IO;
    using System.Xml.Linq;

    internal class XMLWriter
    {
        string resultPath = Directory.GetCurrentDirectory() + @"\ADKResult.xml";
        public void CreateXML(ADK_Parser parser, MachineInfo argMachineInfo)
        {
            XDocument xDoc =
                        new XDocument(
                            new XElement(string.Format("ADKResult_{0}_{1}", argMachineInfo.Platform, argMachineInfo.OS.Type)));
            parser.parseData.ForEach(adkInfo =>
                {
                    xDoc.Root.Add(
                        new XElement("Data",
                            new XElement("Attributes", adkInfo.TestContent),
                            new XElement("SearchKey", adkInfo.keys),
                            new XElement("Benchmark_including_Guardband", adkInfo.benchMarkValue),
                            new XElement("Result_Data", adkInfo.Result_Data),
                            new XElement("Average", adkInfo.average),
                            new XElement("Status", adkInfo.status)
                            ));
                });
            xDoc.Save(resultPath);    
        }
    }
}
