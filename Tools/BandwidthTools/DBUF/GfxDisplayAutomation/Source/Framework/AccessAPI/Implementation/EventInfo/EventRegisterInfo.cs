namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Xml.Linq;
    using System.Collections.Generic;

    internal class EventRegisterInfo : FunctionalBase, IGetMethod
    {
        public object GetMethod(object argMessage)
        {
            bool status = true;
            string platform = default(string);
            EventInfo eventInfoObject = argMessage as EventInfo;
            eventInfoObject.listRegisters = new List<RegisterInf>();
            if (base.MachineInfo != null)
                platform = base.MachineInfo.PlatformDetails.Platform.ToString();
            else
                Log.Abort("Platform not initialized.");
            
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
                        RegisterInf registerInf = new RegisterInf(factor.Elements("Offset").FirstOrDefault().Value, factor.Elements("Bitmap").FirstOrDefault().Value, factor.Elements("Value").FirstOrDefault().Value, (string)factor.Element("Deviation")?? "0");
                        eventInfoObject.listRegisters.Add(registerInf);
                    }
                }
            }

            if (eventInfoObject.listRegisters.Count == 0)
            {
                Log.Fail("No registers found for event: {0}.", eventInfoObject.eventName);
                status = false;
            }

            foreach(RegisterInf eachRegister in eventInfoObject.listRegisters)
            {
                int rightShiftCount = 0;
                uint currentValue = 0, expectedValue = 0, bitmap = 0, deviation = 0;

                Log.Verbose("Offset: 0x{0} Bitmap: 0x{1} ExpectedValue: 0x{2} Deviation: 0x{3}", eachRegister.Offset, eachRegister.Bitmap, eachRegister.Value, eachRegister.Deviation);
                expectedValue = Convert.ToUInt32(eachRegister.Value, 16);
                deviation = Convert.ToUInt32(eachRegister.Deviation, 16);
                bitmap = Convert.ToUInt32(eachRegister.Bitmap, 16);

                string bitmapBinValue = Convert.ToString(bitmap, 2);
                while (bitmapBinValue.EndsWith("0") != false)
                {
                    bitmapBinValue = bitmapBinValue.Substring(0, bitmapBinValue.Length - 1);
                    rightShiftCount++;
                }

                DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
                driverData.input = Convert.ToUInt32(eachRegister.Offset, 16);
                DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
                DriverEscape escape = new DriverEscape();
                if (!escape.SetMethod(driverParams))
                {
                    status = false;
                    Log.Fail("Failed to read Register with offset as {0}", driverData.input.ToString("X"));
                }
                else
                {
                    currentValue = driverData.output;

                    currentValue &= bitmap;
                    expectedValue &= bitmap;

                    currentValue >>= rightShiftCount;
                    expectedValue >>= rightShiftCount;

                    //add the deviation to the current register value after bitmap.
                    currentValue += deviation;

                    eachRegister.BitmappedValue = currentValue;
                    eachRegister.RegisterValue = driverData.output.ToString("X");
                    Log.Verbose("Register Value: 0x{0}, Current Value after bitmap: 0x{1} Expected Value after bitmap: 0x{2}", driverData.output.ToString("X"), currentValue.ToString("X"), expectedValue.ToString("X"));

                    if(currentValue != expectedValue)
                        status = false;
                }

            }

            eventInfoObject.RegistersMatched = status;

            return eventInfoObject;
        }
    }
}