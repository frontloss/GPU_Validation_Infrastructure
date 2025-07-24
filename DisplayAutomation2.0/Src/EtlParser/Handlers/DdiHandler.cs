/**
* @file		DdiHandler.cs
* @brief	
*
* @source   GfxInstrumentationAnalyzer\DisplayAnalysis\Trackers
*/

using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;

namespace EtlParser.Handlers
{
    public class DdiData
    {
        private int _ThreadID;
        private double _StartTime;
        private double _EndTime;
        private double swappedTime;
        private uint _CPUStall;
        private uint _ThreadSleep;
        private uint _Status;
        private uint _Irql;
        private string _PrimaryFunction = null;

        private List<FunctionData> _functionHistory = new List<FunctionData>();
        private List<DpcdData> _dpcdHistory = new List<DpcdData>();
        private List<MmioData> _mmioHistory = new List<MmioData>();
        public DD_DIAG_SOURCE_DDI Ddi;

        Dictionary<uint, MmioData> MmioCoalesce = new Dictionary<uint, MmioData>();
        public ReadOnlyCollection<MmioData> mmioHistory { get => new ReadOnlyCollection<MmioData>(_mmioHistory); }
        public ReadOnlyCollection<DpcdData> dpcdHistory { get => new ReadOnlyCollection<DpcdData>(_dpcdHistory); }
        public ReadOnlyCollection<FunctionData> functionHistory { get => new ReadOnlyCollection<FunctionData>(_functionHistory); }
        public DdiData(int ThreadID, DD_DIAG_SOURCE_DDI Ddi, double StartTime, uint Irql)
        {
            this.Ddi = Ddi;
            this._ThreadID = ThreadID;
            this._StartTime = StartTime;
            this._Irql = Irql;
            _mmioHistory.Clear();
            _dpcdHistory.Clear();
            _functionHistory.Clear();
        }
        public double ExecTime
        {
            get
            {
                return _EndTime - _StartTime;
            }
        }
        public uint Irql { get => _Irql; }
        public double EndTime { get => _EndTime; set => _EndTime = value; }
        public double StartTime { get => _StartTime; }
        public int ThreadID { get => _ThreadID; }
        public double SwappedTime { get => swappedTime; set => swappedTime = value; }
        public uint CPUStall { get => _CPUStall; set => _CPUStall = value; }
        public uint ThreadSleep { get => _ThreadSleep; set => _ThreadSleep = value; }
        public uint Status { get => _Status; set => _Status = value; }
        public string primaryFunction { get => _PrimaryFunction; private set => _PrimaryFunction = value; }
        public Boolean IsFailed
        {
            get
            {
                switch (Ddi)
                {
                    case DD_DIAG_SOURCE_DDI.DDI_DISPATCH_IO_REQUEST:
                        return Status == 0 ? true : false;
                    default:
                        return (Status & 0x80000000) != 0;
                }
            }
        }
        public void MmioAccess(MmioData MmData)
        {
            MmioData LastMmioTransaction = null;


            if (false == MmData.IsWrite)
            {
                LastMmioTransaction = null;
                if (_mmioHistory.Count > 0)
                {
                    if (_mmioHistory[_mmioHistory.Count - 1].Offset == MmData.Offset)
                    {
                        LastMmioTransaction = _mmioHistory[_mmioHistory.Count - 1];
                    }
                }
                if (null == LastMmioTransaction)
                {
                    // no entry. Add this read.
                    _mmioHistory.Add(MmData);
                }
                else
                {
                    if (LastMmioTransaction.Data != MmData.Data)
                    {
                        // CHange in data. Add this entry

                        _mmioHistory.Add(MmData);
                    }
                    else
                    {
                    }
                }
            }
            else
            {
                // Add this read.
                _mmioHistory.Add(MmData);
            }
        }
        public void AuxAccess(DpcdData AuxData)
        {
            // Add every writes to the history
            _dpcdHistory.Add(AuxData);
        }
        public void FunctionStatus(FunctionData Data)
        {
            if (primaryFunction == null)
            {
                primaryFunction = Data.Name;
            }
            //if (Data.isExit)
            {
                _functionHistory.Add(Data);
            }
        }
    }
    public class DdiHandler
    {
        public Queue<DdiData> ddiDataQueue = new Queue<DdiData>();
        protected Dictionary<int, Stack<DdiData>> ThreadTracker = new Dictionary<int, Stack<DdiData>>();
        public void DdiEntry(int ThreadID, DD_DIAG_SOURCE_DDI Ddi, double TimeStamp, uint Irql)
        {
            Stack<DdiData> ddiDataStack = null;
            DdiData ddiData = null;

            // Check if there is an entry present
            bool ContainsKey = ThreadTracker.TryGetValue(ThreadID, out ddiDataStack);
            if (null == ddiDataStack)
            {
                ddiDataStack = new Stack<DdiData>();
            }

            // Check if there is DDI getting called on the same thread
            if (ddiDataStack.Count > 0)
            {
                DD_DIAG_SOURCE_DDI PeekDdi = ddiDataStack.Peek().Ddi;
                // Flip will be called on the DMA complete DPC. Its not an info. So Skip printing that
                if ((DD_DIAG_SOURCE_DDI.DDI_SETVIDPNSOURCEADDRESSWITHMULTIPLANEOVERLAY3 == Ddi) && (DD_DIAG_SOURCE_DDI.DPC == PeekDdi))
                {
                    // Do nothing
                }
                else if ((DD_DIAG_SOURCE_DDI.DDI_DISPATCH_IO_REQUEST == Ddi)) // && (DD_DIAG_SOURCE_DDI.DPC == PeekDdi))
                {
                    // Do nothing
                }
                else
                {
                    Console.WriteLine("{0} Swapped another Ddi({1})", Ddi, PeekDdi);
                }
            }
            ddiData = new DdiData(ThreadID, Ddi, TimeStamp, Irql);
            this.ddiDataQueue.Enqueue(ddiData);

            // Add the new Execution data to the Stack
            ddiDataStack.Push(ddiData);
            if (false == ContainsKey)
            {
                ThreadTracker.Add(ThreadID, ddiDataStack);
            }
        }
        public void DdiExit(int ThreadID, DD_DIAG_SOURCE_DDI Ddi, double TimeStamp, uint Status)
        {
            Stack<DdiData> ExecStack = null;
            //HistogramEntry HistoEntry = null;
            DdiData ExecData = null;
            DdiData ParentData = null;
            // Check if there is an entry present
            bool ContainsKey = ThreadTracker.TryGetValue(ThreadID, out ExecStack);
            if (null == ExecStack)
            {
                Console.WriteLine("Stack not created for DDI {0} exit @ TID {1}", Ddi, ThreadID);
                return;
            }

            if (0 == ExecStack.Count)
            {
                Console.WriteLine("Stack created but no data for DDI {0} exit @ TID {1}", Ddi, ThreadID);
                return;
            }
            // Popout the DDI at the top of the stack
            ExecData = ExecStack.Pop();
            if (ExecData.Ddi != Ddi)
            {
                Console.WriteLine("{0} closing {1} ", Ddi, ExecData.Ddi);
            }
            // Update the end time and Status
            ExecData.EndTime = TimeStamp;
            ExecData.Status = Status;
            // Update the relative execution time as the thread swap time for the parent
            if (ExecStack.Count > 0)
            {
                DD_DIAG_SOURCE_DDI PeekDdi = ExecStack.Peek().Ddi;
                // Flip will be called on the DMA complete DPC. Its not an info. So Skip printing that
                if ((DD_DIAG_SOURCE_DDI.DDI_SETVIDPNSOURCEADDRESSWITHMULTIPLANEOVERLAY3 == Ddi) && (DD_DIAG_SOURCE_DDI.DPC == PeekDdi))
                {
                    // Do nothing
                }
                else if ((DD_DIAG_SOURCE_DDI.DDI_DISPATCH_IO_REQUEST == Ddi) && (DD_DIAG_SOURCE_DDI.DPC == PeekDdi))
                {
                    // Do nothing
                }
                else
                {
                    Console.WriteLine("Swapped Time : {0} << {1}", ExecData.ExecTime, ExecStack.Count);
                }
                ParentData = ExecStack.Peek();
                ParentData.SwappedTime += ExecData.ExecTime;
            }
        }
    }
}
