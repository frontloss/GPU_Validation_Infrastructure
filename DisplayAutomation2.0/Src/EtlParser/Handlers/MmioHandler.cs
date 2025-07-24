/**
* @file		MmioHandler.cs
* @brief	Handels all the MMIO read and write events
*
* @author	Rohit Kumar
*/

using Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriver;
using Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriverDisplay;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System;
using System.Collections.Generic;
using System.IO;

namespace EtlParser.Handlers
{
    public class MmioData : CommonData
    {
        private bool _isWrite;
        private uint _offset;
        private uint _data;
        private bool _isCpuMmio;
        public bool IsWrite { get => _isWrite; set => _isWrite = value; }
        public uint Offset { get => _offset; set => _offset = value; }
        public uint Data { get => _data; set => _data = value; }
        public bool IsCpuMmio { get => _isCpuMmio; set => _isCpuMmio = value; }

        public List<MmioData> decodedBufferData1;

        public MmioData(t_MMIO_ReadWrite data, Boolean IsWrite) : base(data)
        {
            this.IsWrite = IsWrite;
            this.Offset = data.Offset;
            this.Data = data.Data;
            this.IsCpuMmio = true;
        }

        public MmioData(Dsb_Prepare_t data, uint offset, uint value) : base(data)
        {
            this.IsWrite = true;
            this.Offset = offset;
            this.Data = value;
            this.IsCpuMmio = false;
        }

        public MmioData(t_DSBInfo data, uint offset, uint value) : base(data)
        {
            this.IsWrite = true;
            this.Offset = offset;
            this.Data = value;
            this.IsCpuMmio = false;
        }

        public MmioData(t_MMIOAccessData data) : base(data)
        {
            this.IsWrite = true;
            this.Offset = data.Offset;
            // Few 8 bit MMIO writes are also getting dumped in this event which are not needed for auto test
            // Dump only 16 bit mmio writes in json file
            if(data.DataSize == 0x2)
                this.Data = BitConverter.ToUInt16(data.Data, 0);
            this.IsCpuMmio = true;
        }
    }

    class MmioHandler
    {
        public Queue<MmioData> mmioDataQueue = new Queue<MmioData>();

        public void ParseAndQueueDsbMmioData(Dsb_Prepare_t data, FlipHandler flipHandler)
        {   // Link to DSB Programming BSPEC : https://gfxspecs.intel.com/Predator/Home/Index/68892
            // Sample BufferData = [0,0,0,0,0,50,244,1,0,0,0,0,140,32,244,1,0,64,8,50,244,1,0,0,0,0,3]
            var decodedBufferData = new List<uint>();
            var dsbBufferData = data.BufferData;

            for (int index1 = 0; index1 < dsbBufferData.Length; index1 += 4)
            {
                // In the ETL Parser, the byte array is converted as an Int array,
                // where each byte is stored within 4 byte value.
                // Only the 1st byte will have meaningful data,
                // hence extracting the LSB Byte and concatenating it to form a 32bit value
                byte[] bytes = new byte[4] {
                    dsbBufferData[index1],
                    dsbBufferData[index1 + 1],
                    dsbBufferData[index1 + 2],
                    dsbBufferData[index1 + 3]
                };

                uint value = (uint)BitConverter.ToInt32(bytes, 0);
                decodedBufferData.Add(value);
            }

            // decodedBufferData = [value, offset, value, offset .....]
            // Skip every alternative entry for looping through the (value, offset) combination
            for (int index1 = 0; index1 < decodedBufferData.Count; index1+=2)
            {
                // Offset contains - Out of 32 bits -
                // First 8 bits - Type of data (Whether it is MMIO or not.)
                // Next 4 bits - Byte En
                // Next 20 bits - Register address offset
                // Hex value of First Byte for MMIO transactions will be 0x1
                uint dsbDataType = (decodedBufferData[index1 + 1] >> 24) & 0xFF;
                if (dsbDataType != 0x01)
                {
                    continue;
                }
                // Extract 20 bits out of 32 bits to get MMIO offset
                uint dsbOffset = (decodedBufferData[index1+1] << (31 - 19)) & 0xFFFFFFFF;
                dsbOffset = (dsbOffset >> (31 - 19 + 0)) & 0xFFFFFFFF;
                uint dsbValue = decodedBufferData[index1];
                // Add DSB MMIO data to MMIO Handler Queue
                this.EnqueueDsbData(data, dsbOffset, dsbValue);
                // Add DSB MMIO data to Flip Handler Queue
                flipHandler.AddDsbMmioData(data, dsbOffset, dsbValue);
            }
        }

        public void ParseAndQueueDsbMmioData(t_DSBInfo data, FlipHandler flipHandler)
        {   // Link to DSB Programming BSPEC : https://gfxspecs.intel.com/Predator/Home/Index/68892
            // Sample BufferData = [0,0,0,0,0,50,244,1,0,0,0,0,140,32,244,1,0,64,8,50,244,1,0,0,0,0,3]
            var decodedBufferData = new List<uint>();
            byte[] dsbBufferData = new byte[data.BufferDwords * sizeof(uint)];
            for (int i = 0; i < data.BufferDwords * sizeof(uint); i++)
                Buffer.BlockCopy(BitConverter.GetBytes((int)data.BufferData[i]), 0, dsbBufferData, i, sizeof(byte));

            for (int index1 = 0; index1 < dsbBufferData.Length; index1 += 4)
            {
                // In the ETL Parser, the byte array is converted as an Int array,
                // where each byte is stored within 4 byte value.
                // Only the 1st byte will have meaningful data,
                // hence extracting the LSB Byte and concatenating it to form a 32bit value
                byte[] bytes = new byte[4] {
                    dsbBufferData[index1],
                    dsbBufferData[index1 + 1],
                    dsbBufferData[index1 + 2],
                    dsbBufferData[index1 + 3]
                };

                uint value = (uint)BitConverter.ToInt32(bytes, 0);
                decodedBufferData.Add(value);
            }

            // decodedBufferData = [value, offset, value, offset .....]
            // Skip every alternative entry for looping through the (value, offset) combination
            for (int index1 = 0; index1 < decodedBufferData.Count; index1 += 2)
            {
                // Offset contains - Out of 32 bits -
                // First 8 bits - Type of data (Whether it is MMIO or not.)
                // Next 4 bits - Byte En
                // Next 20 bits - Register address offset
                // Hex value of First Byte for MMIO transactions will be 0x1
                uint dsbDataType = (decodedBufferData[index1 + 1] >> 24) & 0xFF;
                if (dsbDataType != 0x01)
                {
                    continue;
                }
                // Extract 20 bits out of 32 bits to get MMIO offset
                uint dsbOffset = (decodedBufferData[index1 + 1] << (31 - 19)) & 0xFFFFFFFF;
                dsbOffset = (dsbOffset >> (31 - 19 + 0)) & 0xFFFFFFFF;
                uint dsbValue = decodedBufferData[index1];
                // Add DSB MMIO data to MMIO Handler Queue
                this.EnqueueDsbData(data, dsbOffset, dsbValue);
                // Add DSB MMIO data to Flip Handler Queue
                flipHandler.AddDsbMmioData(data, dsbOffset, dsbValue);
            }
        }
        public void Enqueue(t_MMIO_ReadWrite data, Boolean IsWrite)
        {
            this.mmioDataQueue.Enqueue(new MmioData(data, IsWrite));
        }

        public void Enqueue(t_MMIOAccessData data, Boolean IsWrite)
        {
            this.mmioDataQueue.Enqueue(new MmioData(data));
        }

        public void EnqueueDsbData(Dsb_Prepare_t data, uint offset, uint value)
        {
            this.mmioDataQueue.Enqueue(new MmioData(data, offset, value));
        }

        public void EnqueueDsbData(t_DSBInfo data, uint offset, uint value)
        {
            this.mmioDataQueue.Enqueue(new MmioData(data, offset, value));
        }

        public void DumpJson()
        {
            String mmioDataOutputFile = Environment.CurrentDirectory + "\\" + "mmioData.json";
            // First delete the existing file
            System.IO.File.Delete(mmioDataOutputFile);

            JsonSerializer serializer = new JsonSerializer();
            serializer.Converters.Add(new JavaScriptDateTimeConverter());
            serializer.Converters.Add(new StringEnumConverter());
            serializer.NullValueHandling = NullValueHandling.Ignore;

            using (StreamWriter sw = new StreamWriter(mmioDataOutputFile))
            using (JsonWriter writer = new JsonTextWriter(sw))
            {
                serializer.Serialize(writer, this);
            }
        }
    }
}
