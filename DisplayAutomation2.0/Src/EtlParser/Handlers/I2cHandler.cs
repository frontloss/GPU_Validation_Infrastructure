/**
* @file     I2cHandler.cs
* @brief    Handles all I2c related transactions
*
* @author   creddyy
*/
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriverDisplay;
using Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDisplayExternal;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System.IO;
using GFX_DISPLAY_EXTERNAL = Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDisplayExternal;
using GFX_DISPLAY_DRIVER = Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriverDisplay;

namespace EtlParser.Handlers
{
    public class I2cData : CommonData
    {
        public bool IsWrite;
        public DD_PORT_TYPES Port;
        public uint Slave;
        public uint Index;
        public uint Flags;
        public uint Size;
        public string Data;

        public I2cData(GFX_DISPLAY_DRIVER.I2C_t data, Boolean IsWrite) : base(data)
        {
            this.IsWrite = IsWrite;
            this.Port = (DD_PORT_TYPES)data.Port;
            this.Slave = data.Slave;
            this.Index = data.Index;
            this.Flags = data.Flags;
            this.Size = data.DataSize;
            this.Data = BitConverter.ToString(data.Data);
        }
        public I2cData(GFX_DISPLAY_EXTERNAL.I2C_t data, Boolean IsWrite) : base(data)
        {
            this.IsWrite = IsWrite;
            this.Port = (DD_PORT_TYPES)data.Port;
            this.Slave = data.Slave;
            this.Index = data.Index;
            this.Flags = data.Flags;
            this.Size = data.DataSize;
            this.Data = BitConverter.ToString(data.Data);
        }
    }
    class I2cHandler
    {
        public Queue<I2cData> i2cDataQueue = new Queue<I2cData>();
        public void Enqueue(GFX_DISPLAY_DRIVER.I2C_t data, Boolean IsWrite)
        {
            this.i2cDataQueue.Enqueue(new I2cData(data, IsWrite));
        }
        public void Enqueue(GFX_DISPLAY_EXTERNAL.I2C_t data, Boolean IsWrite)
        {
            this.i2cDataQueue.Enqueue(new I2cData(data, IsWrite));
        }
        public void DumpJson()
        {
            String i2cDataOutputFile = Environment.CurrentDirectory + "\\" + "I2cData.json";
            // First delete the existing file
            System.IO.File.Delete(i2cDataOutputFile);

            JsonSerializer serializer = new JsonSerializer();
            serializer.Converters.Add(new JavaScriptDateTimeConverter());
            serializer.Converters.Add(new StringEnumConverter());
            serializer.NullValueHandling = NullValueHandling.Ignore;

            using (StreamWriter sw = new StreamWriter(i2cDataOutputFile))
            using (JsonWriter writer = new JsonTextWriter(sw))
            {
                serializer.Serialize(writer, this);
            }
        }
    }
}
