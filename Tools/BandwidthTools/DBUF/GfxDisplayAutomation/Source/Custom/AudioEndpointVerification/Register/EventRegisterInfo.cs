namespace AudioEndpointVerification
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Xml.Linq;
    using System.Collections.Generic;

    internal class EventRegisterInfo
    {
        public object GetMethod(object argMessage)
        {
            EventInfo eventInfoObject = argMessage as EventInfo;
            eventInfoObject.listRegisters = new List<RegisterInf>();
            string platform = GetPlatformInfo();
            XDocument events = XDocument.Load(string.Concat(Directory.GetCurrentDirectory(), @"\Mapper\Events.map"));
            XDocument subEvents = XDocument.Load(string.Concat(Directory.GetCurrentDirectory(), @"\Mapper\Subevents.map"));
            XDocument factors = XDocument.Load(string.Concat(Directory.GetCurrentDirectory(), @"\Mapper\Factors.map"));
            int count = (from xml in events.Descendants("Events").Elements("Event")
                         where String.Equals(xml.Attribute("name").Value, eventInfoObject.eventName)
                         select xml).First().Elements("Register").Count();

            for (int a = 0; a < count; a++)
            {
                string registerName = (from xml in events.Descendants("Events").Elements("Event")
                                       where String.Equals(xml.Attribute("name").Value, eventInfoObject.eventName)
                                       select xml).First().Elements("Register").ElementAt(a).Value;
                XElement subEvent = (from xml in subEvents.Descendants("SubEvent")
                                     where xml.Attribute("name").Value.Equals(registerName)
                                     select xml).FirstOrDefault();
                string[] values = (from xml in subEvent.Elements("Platform")
                                   where xml.Attribute("Name").Value.Equals(platform)
                                   select xml).FirstOrDefault().Elements("Factor").FirstOrDefault().Value.Split(',');
                foreach (string value in values)
                {
                    XElement factor = (from xml in factors.Descendants("Factor")
                                       where (((xml.Attribute("name").Value.Contains(eventInfoObject.pipe.ToString())) || (xml.Attribute("name").Value.Contains(eventInfoObject.port.ToString())) || (xml.Attribute("name").Value.Contains(eventInfoObject.plane.ToString()))) && (xml.Attribute("id").Value.Equals(value.ToString())))
                                       select xml).FirstOrDefault();

                    if (factor == null)
                        continue;
                    else
                    {
                        RegisterInf registerInf = new RegisterInf(factor.Elements("Offset").FirstOrDefault().Value, factor.Elements("Bitmap").FirstOrDefault().Value, factor.Elements("Value").FirstOrDefault().Value);
                        eventInfoObject.listRegisters.Add(registerInf);
                    }
                }
            }
            return eventInfoObject;
        }
        private string GetPlatformInfo()
        {
            string platform = "";
            switch (CommonExtension.PlatformID)
            {
                case "HSWM":
                case "HSWDT":
                case "HSWU":
                    platform = "HSW";
                    break;
                case "IVBM":
                    platform = "IVB";
                    break;
                case "BDW":
                    platform = "BDW";
                    break;
                case "VLV":
                    platform = "VLV";
                    break;
                case "SKL":
                    platform = "SKL";
                    break;
                case "BXT":
                    platform = "BXT";
                    break;
                case "CHV":
                    platform = "CHV";
                    break;
            }
            return platform;
        }
    }
}