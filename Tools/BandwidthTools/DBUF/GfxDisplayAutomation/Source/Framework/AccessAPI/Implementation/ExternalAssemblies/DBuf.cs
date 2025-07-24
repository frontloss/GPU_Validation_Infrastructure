namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using Microsoft.Win32;
    class DBuf : FunctionalBase, IGetMethod, IGetAllMethod
    {
        public DBuf()
        {
            _dBufNeeded = new Dictionary<PIPE, uint>();
            _actualDBuf = new Dictionary<PIPE, uint>();
            _dbufAllocated = new Dictionary<PIPE, uint>();
            TotalDbuf = 0;
        }

        uint[,] uPlane_CTL = {{ 0, 0, 0},{0,0,0},{0,0,0}};
        uint[,] uScalar_CTL = {{ 0, 0 },{0,0},{0,0}};
        uint[,] uScalar_H = { { 0, 0 }, { 0, 0 }, { 0, 0 } };
        uint[,] uScalar_V = { { 0, 0 }, { 0, 0 }, { 0, 0 } };
        uint[] uPipe_SRC_SZ = { 0, 0, 0 };
        uint[,] uPlane_Size = { { 0, 0, 0 }, { 0, 0, 0 }, { 0, 0, 0 } };
        uint[] uTrans_CONF = { 0, 0, 0, 0};
        uint[] uTrans_DDI = { 0, 0, 0, 0 };
        uint[] uTrans_Htotal = { 0, 0, 0, 0 };
        uint uDsiPLLStatus = 0;
        uint uDsiPLLCtl = 0;
        uint uMIPIaPortStatus = 0;
        uint uMIPIcPortStatus = 0;
        double[] pixelrate = {0, 0, 0};
        uint uMIPIaCtrl = 0;
        uint uMIPIcCtrl = 0;
        uint[] uTRANS_LINKM1 = { 0, 0, 0, 0 };
        uint[] uTRANS_LINKN1 = { 0, 0, 0, 0 };
        double[,] uPlaneBW = { { 0, 0, 0 }, { 0, 0, 0 }, { 0, 0, 0 } };
        double[,] uPlanerate = { { 0, 0, 0 }, { 0, 0, 0 }, { 0, 0, 0 } };
        double[] uPipeBW = { 0, 0, 0 };
        uint pipemax = 3;
        uint planemax = 3;
        uint[] Latency = { 0, 0, 0, 0, 0, 0, 0, 0 };
        uint minlatency = 0;
        double totalbw = 0;
        double arbitratedbw = 0;
        uint wa; // workaround based on arbitrated bandwidth
        bool IsYtileEnabled = false;
        bool[] pipeallocfinal = { false, false, false };
        uint[] pipealloc = { 0, 0, 0 };
        bool[,] planeallocfinal = { { false, false, false }, { false, false, false }, { false, false, false } };
        uint[,] planealloc = {{ 0, 0, 0 },{ 0, 0, 0 },{ 0, 0, 0 }};
        uint uMemoryRank = 1;
        uint uMemoryRankCh0 = 1;
        uint uMemoryRankCh1 = 1;
        uint uNoMemoryChannel = 0;
        uint uArb_Ctl2 = 0;

        private uint totalDbuf;
        public uint TotalDbuf
        {
            get { return totalDbuf; }
            set { totalDbuf = value; }
        }

        public uint MaxDBuf
        {
            get
            {
                if (base.AppManager.MachineInfo.PlatformDetails.Platform == Platform.BXT)
                {
                    return 508;
                }
                if (base.AppManager.MachineInfo.PlatformDetails.Platform == Platform.GLK)
                {
                    return 1020;
                }
                return 892;
            }
        }
        Dictionary<PIPE, uint> _dBufNeeded = null;
        Dictionary<PIPE, uint> _actualDBuf = null;
        Dictionary<PIPE, uint> _dbufAllocated = null;


        public object GetMethod(object argMessage)
        {
            List<PipeDbufInfo> dbufList = argMessage as List<PipeDbufInfo>;
            List<PipeDbufInfo> returnList = new List<PipeDbufInfo>();

            GetDBufNeeded(dbufList);
            
            //if (GetDBufNeeded(dbufList))
            //{
            //    UpdateRemainingDBuf(dbufList);
            //}

            //_dbufAllocated[curDisp.Pipe] = (uint)(_dBufNeeded[curDisp.Pipe];
           // _dbufAllocated.Keys.ToList().ForEach(curPipe =>
            _dBufNeeded.Keys.ToList().ForEach(curPipe =>
            {
                PipeDbufInfo curPipeDbufInfo = dbufList.Where(dI => dI.Pipe == curPipe).Select(dI => dI).FirstOrDefault();
                curPipeDbufInfo.DbufAllocated = _dBufNeeded[curPipe];
                returnList.Add(curPipeDbufInfo);
            });
            return returnList;
        }

        private bool GetDBufNeeded(List<PipeDbufInfo> argDbufList)
        {
            InitializePipeRegisters();
            InitializePlaneRegisters();
            if (base.AppManager.MachineInfo.PlatformDetails.Platform == Platform.BXT || base.AppManager.MachineInfo.PlatformDetails.Platform == Platform.GLK)
            {
                InitializeMipiRegisters();
            }
            totalbw = CalculateSystemMemoryBandwidth();
            arbitratedbw = CalculateArbitratedMemoryBandwidth();
            IsYtileEnabled = CheckforYtile();
            if ((arbitratedbw > (totalbw * 0.2)) && IsYtileEnabled)
                wa = 1;
            else if ((arbitratedbw > (totalbw * 0.35)) && (uMemoryRank == 1) && (uNoMemoryChannel == 2))
                wa = 2;
            else if (arbitratedbw > (totalbw * 0.6))
                wa = 2;

            Latency = CalculateMemorylatency_Gen9();

            uint remainingdbuf = MaxDBuf;
            uint varhar = 0;

            if (argDbufList.First().DisplayConfigType == DisplayConfigType.SD)
            {
                remainingdbuf = remainingdbuf - 32;
                TotalDbuf = TotalDbuf + 32;
                Log.Message("config is sd , remaining {0}", remainingdbuf);
                varhar = 32;
            }
            else
            {
                if (remainingdbuf > (uint)(18 * argDbufList.Count()))
                {
                    remainingdbuf = remainingdbuf - (uint)(18 * argDbufList.Count()); //bun chnage
                    TotalDbuf = TotalDbuf + (uint)(18 * argDbufList.Count()); //bun chnage
                    Log.Message("not sd, remaining dbuf {0}", remainingdbuf);
                    varhar = (uint)(18 * argDbufList.Count()); //hatao bun change
                }
                else
                {
                    Log.Message("HW Cursor is not possible, remaining Dbuf is {0}", remainingdbuf);
                }
            }
            uint[] temppipedbuf = { 0, 0, 0 };
            uint i = 0;

            //while (pipeallocfinal[j] == false)

            argDbufList.ForEach(curDbuf =>
            {
                uint value = 0;
                uint j = 0;
                    value = calculateDBuf(curDbuf, j);
                    value = value + calculateDBuf_OverlayWa(curDbuf, j);
                //value will be sum of all min dbufs required by planes within a pipe. It will be temporary dbuf for that pipe
                //_actualDBuf.Add(curDbuf.Pipe, value);
                //TotalDbuf = TotalDbuf + value;
                //_dBufNeeded[curDbuf.Pipe] = value;
               // Log.Message("{0} ,value:{1} , Total DBuf {2}", curDbuf.DisplayType, value, TotalDbuf);
                uint l = 0;
                if (curDbuf.plane == PLANE.PLANE_A) l = 0;
                if (curDbuf.plane == PLANE.PLANE_B) l = 1;
                if (curDbuf.plane == PLANE.PLANE_C) l = 2;
                temppipedbuf[l] = value;
                
            });

            double[] temppixelrate = pixelrate;
            double temppixelratesum =  0;
            for (i = 0; i < pipemax;i++)
                temppixelratesum = temppixelratesum + temppixelrate[i];

         //   List<int> cases = new List<int>();
          //  cases.Add(0);
          //  cases.Add(1);
          //  cases.Add(2);
         //   uint count = 0;
            uint exit = 0;
            do
            {
                for (i = 0; i < pipemax;i++)
                {
                    uint recompute = 0;
                    if ((pixelrate[i] > 0) && (pipeallocfinal[i] == false))
                    {
                        
                        if ((uint)((temppixelrate[i] * remainingdbuf) / temppixelratesum) < temppipedbuf[i])
                        {
                            pipealloc[i] = temppipedbuf[i];
                            pipeallocfinal[i] = true;
                            remainingdbuf = remainingdbuf - temppipedbuf[i];
                            temppixelrate[i] = 0;
                            temppixelratesum = 0;
                            for (uint k = 0; k < pipemax; k++)
                                temppixelratesum = temppixelratesum + temppixelrate[k];

                            for (uint k = 0; k < i; k++)
                                if ((pixelrate[k] > 0) && pipeallocfinal[k] == false)
                                    recompute = 1;
                            if (recompute == 0)
                            {
                                uint count = 0;
                                for (uint k = i; k < pipemax; k++)
                                    if ((pixelrate[k] > 0) && (pipeallocfinal[k] == false))
                                        count++;
                                if (count == 0)
                                    exit = 1;
                                else continue;
                            }

                        }
                        else
                        {
                            pipealloc[i] = (uint)((temppixelrate[i] * remainingdbuf) / temppixelratesum);
                            uint count = 0;
                            for (uint k = i; k < pipemax; k++)
                                if ((pixelrate[k] > 0) && (pipeallocfinal[k] == false))
                                    count++;
                            if (count == 1)
                            {
                              //  pipeallocfinal[i] = true;
                              //  remainingdbuf = remainingdbuf - temppipedbuf[i];
                                exit = 1;
                            }
                        }

                        if (recompute == 1)
                            break;
                    }
                }

                if (exit == 1)
                    break;

            } while (true);

            pipealloc[0] = pipealloc[0] + MaxDBuf - (pipealloc[0] + pipealloc[1] + pipealloc[2] + varhar);
            
            argDbufList.ForEach(curDbuf =>
            {
                uint l = 0;
                if (curDbuf.plane == PLANE.PLANE_A) l = 0;
                if (curDbuf.plane == PLANE.PLANE_B) l = 1;
                if (curDbuf.plane == PLANE.PLANE_C) l = 2;

                _actualDBuf.Add(curDbuf.Pipe, pipealloc[l]);
                TotalDbuf = TotalDbuf + pipealloc[l];
                _dBufNeeded[curDbuf.Pipe] = pipealloc[l];
  
                l++;
            });
           
            if (TotalDbuf > MaxDBuf)
            {
                Log.Message("Total Dbuf {0} has exceeded max {1}", TotalDbuf, MaxDBuf);
                return false;
            }
            return true;
        }
        private uint calculateDBuf(PipeDbufInfo curDbuf , uint planeid)
        {
            uint dbuf1 = 0;
            uint dbuf2 = 0;
            uint pipeid = 0;
            uint htotal = 0;

            if (curDbuf.plane == PLANE.PLANE_A) pipeid = 0; // plane parameter is actually carrying pipe information so using that to assign pipe id. so PLANE_B == PipeB
            if (curDbuf.plane == PLANE.PLANE_B) pipeid = 1;
            if (curDbuf.plane == PLANE.PLANE_C) pipeid = 2;
            htotal = ((uTrans_Htotal[pipeid] & 0x1FFF0000) >> 16)+1;
            // edp transcoder can be mapped to any pipe , so checking that and updating pixel clock of respective pipe
            if (((uTrans_CONF[3] & 0x80000000) == 0x80000000) && ((uTrans_DDI[3] & 0x80000000) == 0x80000000) && curDbuf.Pipe == PIPE.PIPE_EDP)
            {
                htotal = ((uTrans_Htotal[3] & 0x1FFF0000) >> 16) + 1;
                switch ((uTrans_DDI[3] & 0x00007000) >> 12)
                {
                    case 0:
                        pipeid = 0;
                        break;
                    case 5:
                        pipeid = 1;
                        break;
                    case 6:
                        pipeid = 2;
                        break;
                    default:
                        break;
                }

              }

            if ((base.AppManager.MachineInfo.PlatformDetails.Platform == Platform.BXT || base.AppManager.MachineInfo.PlatformDetails.Platform == Platform.GLK) && (curDbuf.DisplayType == DisplayType.MIPI) && ((uDsiPLLStatus & 0x80000000) == 0x80000000))
            {
                htotal = GetHTotal_MIPIBXT();
                switch ((uMIPIaCtrl & 0x00000380) >> 7)
                {
                    case 0:
                        pipeid = 0;
                        break;
                    case 1:
                        pipeid = 1;
                        break;
                    case 2:
                        pipeid = 2;
                        break;
                }
            }

            uint latencylevel = 0;

            for (uint i = 0; i < 8; i++)
            {
                if (Latency[i] > 30)
                {
                    minlatency = Latency[i];
                    latencylevel = i;
                    break;
                }
            }

            uint pipecount = 0;

            if (pixelrate[0] > 0) pipecount++;
            if (pixelrate[1] > 0) pipecount++;
            if (pixelrate[2] > 0) pipecount++;

            if ((uPlane_CTL[pipeid, planeid] & 0x80000000) == 0)
                return 0;


            // Checking Dbuf for WM
            if (pipecount == 1)
                dbuf1 = CheckWMforDBUF(curDbuf, pipeid , planeid , minlatency , htotal , latencylevel , false);
            else
                dbuf1 = CheckWMforDBUF(curDbuf, pipeid , planeid , Latency[0] , htotal , 0, false);

            uint planewidth = (uPlane_Size[pipeid, planeid] & 0x00001FFF) + 1;
            double Bpp = GetPlaneBpp(pipeid, planeid);
      
            if ((uPlane_CTL[pipeid , planeid] & 0x00001000) == 0x00000000)
            {
                //return 8 + 3;
                dbuf2 = 8;
            }
              
            // Currently 64 bit RGB support not added here
            else if ((uPlane_CTL[pipeid, planeid] & 0x00000001) == 0x00000001) //90 or 270 rotation
            {
                if (Bpp == 1.5)
                dbuf2 = (Convert.ToUInt32(Math.Ceiling((4 * planewidth * 1) / 512.0)) * 8 + 3) + (Convert.ToUInt32(Math.Ceiling((4 * planewidth * 0.5 * 2) / 512.0)) * 4 + 3);
                else if (Bpp == 1)
                dbuf2 = Convert.ToUInt32((Math.Ceiling((4 * planewidth * Bpp) / 512.0) * 8) + 3);
                else if (Bpp == 2)
                dbuf2 = Convert.ToUInt32((Math.Ceiling((4 * planewidth * Bpp) / 512.0) * 4) + 3);
                else if (Bpp == 4)
                dbuf2 = Convert.ToUInt32((Math.Ceiling((4 * planewidth * Bpp) / 512.0) * 2) + 3);
                else if (Bpp == 8)
                dbuf2 = Convert.ToUInt32((Math.Ceiling((4 * planewidth * Bpp) / 512.0) * 1) + 3);
                
            }
            else
            {
                dbuf2 = Convert.ToUInt32((Math.Ceiling((4 * planewidth * Bpp) / 512.0) * 2) + 3);
            }
            
            return Math.Max(dbuf1 , dbuf2);
        }

        private uint calculateDBuf_OverlayWa(PipeDbufInfo curDbuf, uint planeid)
        {
            uint dbuf1 = 0;
            uint dbuf2 = 0;
            uint pipeid = 0;
            uint htotal = 0;

            if (curDbuf.plane == PLANE.PLANE_A) pipeid = 0; // plane parameter is actually carrying pipe information so using that to assign pipe id. so PLANE_B == PipeB
            if (curDbuf.plane == PLANE.PLANE_B) pipeid = 1;
            if (curDbuf.plane == PLANE.PLANE_C) pipeid = 2;
            htotal = ((uTrans_Htotal[pipeid] & 0x1FFF0000) >> 16) + 1;
            // edp transcoder can be mapped to any pipe , so checking that and updating pixel clock of respective pipe
            if (((uTrans_CONF[3] & 0x80000000) == 0x80000000) && ((uTrans_DDI[3] & 0x80000000) == 0x80000000) && curDbuf.Pipe == PIPE.PIPE_EDP)
            {
                htotal = ((uTrans_Htotal[3] & 0x1FFF0000) >> 16) + 1;
                switch ((uTrans_DDI[3] & 0x00007000) >> 12)
                {
                    case 0:
                        pipeid = 0;
                        break;
                    case 5:
                        pipeid = 1;
                        break;
                    case 6:
                        pipeid = 2;
                        break;
                    default:
                        break;
                }

            }

            if ((base.AppManager.MachineInfo.PlatformDetails.Platform == Platform.BXT || base.AppManager.MachineInfo.PlatformDetails.Platform == Platform.GLK) && (curDbuf.DisplayType == DisplayType.MIPI) && ((uDsiPLLStatus & 0x80000000) == 0x80000000))
            {
                htotal = GetHTotal_MIPIBXT();
                switch ((uMIPIaCtrl & 0x00000380) >> 7)
                {
                    case 0:
                        pipeid = 0;
                        break;
                    case 1:
                        pipeid = 1;
                        break;
                    case 2:
                        pipeid = 2;
                        break;
                }
            }

            uint latencylevel = 0;

            for (uint i = 0; i < 8; i++)
            {
                if (Latency[i] > 30)
                {
                    minlatency = Latency[i];
                    latencylevel = i;
                    break;
                }
            }

            uint pipecount = 0;

            if (pixelrate[0] > 0) pipecount++;
            if (pixelrate[1] > 0) pipecount++;
            if (pixelrate[2] > 0) pipecount++;

            if ((uPlane_CTL[pipeid, planeid] & 0x80000000) == 0)
                return 0;


            // Checking Dbuf for WM
            if (pipecount == 1)
                dbuf1 = CheckWMforDBUF(curDbuf, pipeid, planeid, minlatency, htotal, latencylevel , true);
            else
                dbuf1 = CheckWMforDBUF(curDbuf, pipeid, planeid, Latency[0], htotal, 0 , true);

            uint planewidth = (uPlane_Size[pipeid, planeid] & 0x00001FFF) + 1;
            double Bpp = GetPlaneBpp(pipeid, planeid);

            //if ((uPlane_CTL[pipeid, planeid] & 0x00001000) == 0x00000000)
            //{
                //return 8 + 3;
                dbuf2 = 8;
            //}

            //// Currently 64 bit RGB support not added here
            //else if ((uPlane_CTL[pipeid, planeid] & 0x00000001) == 0x00000001) //90 or 270 rotation
            //{
            //    if (Bpp == 1.5)
            //        dbuf2 = (Convert.ToUInt32(Math.Ceiling((4 * planewidth * 1) / 512.0)) * 8 + 3) + (Convert.ToUInt32(Math.Ceiling((4 * planewidth * 0.5 * 2) / 512.0)) * 4 + 3);
            //    else if (Bpp == 1)
            //        dbuf2 = Convert.ToUInt32((Math.Ceiling((4 * planewidth * Bpp) / 512.0) * 8) + 3);
            //    else if (Bpp == 2)
            //        dbuf2 = Convert.ToUInt32((Math.Ceiling((4 * planewidth * Bpp) / 512.0) * 4) + 3);
            //    else if (Bpp == 4)
            //        dbuf2 = Convert.ToUInt32((Math.Ceiling((4 * planewidth * Bpp) / 512.0) * 2) + 3);
            //    else if (Bpp == 8)
            //        dbuf2 = Convert.ToUInt32((Math.Ceiling((4 * planewidth * Bpp) / 512.0) * 1) + 3);

            //}
            //else
            //{
            //    dbuf2 = Convert.ToUInt32((Math.Ceiling((4 * planewidth * Bpp) / 512.0) * 2) + 3);
            //}

            return Math.Max(dbuf1+1, dbuf2);
        }

        private void UpdateRemainingDBuf(List<PipeDbufInfo> argDbufList)
        {
            uint remainingDbuf = MaxDBuf - TotalDbuf;
            Log.Message("remaining dbuf {0}", remainingDbuf);
            uint varHar = 0;
            // if (argDbufList.Where(dI => dI.PlaneA.HWCursorEnable == true).Select(dI => dI).ToList().Count() > 0)
            //{
            
            Log.Message("end of if");
            //  }
            Log.Message("total dbuf {0} , and max dbuf {1}", TotalDbuf, MaxDBuf);
            if (TotalDbuf < MaxDBuf)
            {
                double sum = 0;
                _actualDBuf.Keys.ToList().ForEach(curDisp =>
                {
                    sum = sum + _actualDBuf[curDisp];
                    Log.Message("the sum is {0}", sum);
                });
                // sum = sum + varHar; //change
                argDbufList.ForEach(curDisp =>
                {
                    uint i = 0;
                    if (curDisp.plane == PLANE.PLANE_A) i = 0;
                    if (curDisp.plane == PLANE.PLANE_B) i = 1;
                    if (curDisp.plane == PLANE.PLANE_C) i = 2;

                    Log.Message("the dbufNeeded is {0} for pipe and the remaining is {1} ", _dBufNeeded[curDisp.Pipe], curDisp.Pipe, remainingDbuf);
                    if (curDisp.DisplayType == argDbufList.First().DisplayType && argDbufList.First().DisplayConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Extended)
                    {
                        //only for primary 
                        _dBufNeeded[curDisp.Pipe] = _dBufNeeded[curDisp.Pipe] - curDisp.MinDBufNeeded;
                     // _dbufAllocated[curDisp.Pipe] = (uint)(_dBufNeeded[curDisp.Pipe] + (remainingDbuf * (double)(_dBufNeeded[curDisp.Pipe] / sum))); // re distribution for pipe
_dbufAllocated[curDisp.Pipe] = (uint)(_dBufNeeded[curDisp.Pipe] + (remainingDbuf * pixelrate[i] / (pixelrate[0]+ pixelrate[1]+ pixelrate[2]) ));
                    }
                    else
                    {
                    	// _dbufAllocated[curDisp.Pipe] = (uint)(_dBufNeeded[curDisp.Pipe] + (remainingDbuf * (double)(_dBufNeeded[curDisp.Pipe] / sum))); // re distribution for pipe
_dbufAllocated[curDisp.Pipe] = (uint)(_dBufNeeded[curDisp.Pipe] + (remainingDbuf * pixelrate[i] / (pixelrate[0]+ pixelrate[1]+ pixelrate[2]) ));

                    }
                    Log.Message("{0} {1}", curDisp.Pipe, _dbufAllocated[curDisp.Pipe]);
                });
                uint total = 0;
                _dbufAllocated.Keys.ToList().ForEach(curDisp =>
                {
                    total = _dbufAllocated[curDisp] + total;
                });
                if ((total + varHar) < MaxDBuf)
                {
                    // PIPE priPipe = _dbufAllocated.Keys.ToList().First(); old code
                    PIPE priPipe = PIPE.NONE;
                    argDbufList.ForEach(dI =>
                        {
                            if (dI.plane == PLANE.PLANE_A)
                                priPipe = dI.Pipe;
                        });

                    if (priPipe != PIPE.NONE)
                        Log.Message("Allocating remaing dbuf to {0}", priPipe);
                    else
                        Log.Alert("remaining dbuf is not allocated to any display since PIPE_A is not in config");

                    Log.Message("Adding {0} to {1}", MaxDBuf - (total + varHar), priPipe);
                    _dbufAllocated[priPipe] = _dbufAllocated[priPipe] + (MaxDBuf - (total + varHar));
                }
                Log.Message("After re distributing");
                argDbufList.ForEach(curDisp =>
                {
                    Log.Message("{0} {1}", curDisp.Pipe, _dbufAllocated[curDisp.Pipe]);
                });
            }
        }


        public object GetAllMethod(object argMessage)
        {
            Log.Message(true, "Redistributing to each Plane");
            List<PipeDbufInfo> dbufList = argMessage as List<PipeDbufInfo>;
            InitializePipeRegisters();
            InitializePlaneRegisters();
            if (base.AppManager.MachineInfo.PlatformDetails.Platform == Platform.BXT || base.AppManager.MachineInfo.PlatformDetails.Platform == Platform.GLK)
            {
                InitializeMipiRegisters();
            }
            totalbw = CalculateSystemMemoryBandwidth();
            arbitratedbw = CalculateArbitratedMemoryBandwidth();
            IsYtileEnabled = CheckforYtile();
            if ((arbitratedbw > (totalbw * 0.2)) && IsYtileEnabled)
                wa = 1;
            else if ((arbitratedbw > (totalbw * 0.35)) && (uMemoryRank == 1) && (uNoMemoryChannel == 2))
                wa = 2;
            else if (arbitratedbw > (totalbw * 0.6))
                wa = 2;

            Latency = CalculateMemorylatency_Gen9();
            dbufList.ForEach(curDisp =>
            {
                uint remainingdbuf = curDisp.DbufAllocated;
                uint pipeid = 0;
                if (curDisp.plane == PLANE.PLANE_A) pipeid = 0;
                if (curDisp.plane == PLANE.PLANE_B) pipeid = 1;
                if (curDisp.plane == PLANE.PLANE_C) pipeid = 2;

                Log.Message("{0} {1}", curDisp, remainingdbuf);

                uint[] tempplanedbuf = { 0, 0, 0 };
                //plane A
                if (curDisp.PlaneA.Enabled)
                {
                    uint value = UpdatePlaneDbuf(curDisp ,PLANE.PLANE_A, curDisp.PlaneA.DisplaySurfaceWidth, curDisp.PlaneA.SourcePixelFormat, curDisp.PlaneA.RotationAngle, remainingdbuf, curDisp.PlaneA.TileFormat , 0);
                   tempplanedbuf[0] = value;
                  //  remainingdBuf = remainingdBuf - value;
                    Log.Message("{0} Plane A -> {1} ", curDisp.DisplayType, value);
                }
                if (curDisp.PlaneB.Enabled)
                {
                    uint value = UpdatePlaneDbuf(curDisp ,PLANE.PLANE_B, curDisp.PlaneB.DisplaySurfaceWidth, curDisp.PlaneB.SourcePixelFormat, curDisp.PlaneB.RotationAngle, remainingdbuf, curDisp.PlaneB.TileFormat , 1);
                    tempplanedbuf[1] = value;
                  //  remainingDBuf = remainingDBuf - value;
                    Log.Message("{0} Plane b -> {1} ", curDisp.DisplayType, value);
                }
                else
                {
                    tempplanedbuf[1] = 0;
                }
                if (curDisp.PlaneC.Enabled)
                {
                    uint value = UpdatePlaneDbuf(curDisp ,PLANE.PLANE_C, curDisp.PlaneC.DisplaySurfaceWidth, curDisp.PlaneC.SourcePixelFormat, curDisp.PlaneC.RotationAngle, remainingdbuf, curDisp.PlaneC.TileFormat , 2);
                    tempplanedbuf[2] = value;
                  //  remainingDBuf = remainingDBuf - value;
                    Log.Message("{0} Plane c -> {1} ", curDisp.DisplayType, value);
                }
                else
                {
                    tempplanedbuf[2] = 0;
                }

                for (uint j = 0; j < planemax ; j++ )
                {
                    if ((j < planemax) && ((uPlane_CTL[pipeid, j] & 0x80000000) == 0x80000000))
                    {
                        uPlanerate[pipeid, j] = (((uPlane_Size[pipeid, j] & 0x0FFF0000) >> 16) + 1) * (((uPlane_Size[pipeid, j] & 0x00001FFF)) + 1) * GetPlaneBpp(pipeid, j) * GetDownscalingAmount_Plane(pipeid, j);
                    }
                }
                
                double[] tempplanerate = {uPlanerate[pipeid , 0] , uPlanerate[pipeid , 1] , uPlanerate[pipeid , 2]};
                double tempplaneratesum = 0;
                for (uint i = 0; i < pipemax; i++)
                    tempplaneratesum = tempplaneratesum + tempplanerate[i];

                uint exit = 0;
                do
                {
                    for (uint i = 0; i < planemax; i++)
                    {
                        uint recompute = 0;
                        if ((uPlanerate[pipeid , i] > 0) && (planeallocfinal[pipeid , i] == false))
                        {

                            if ((uint)((tempplanerate[i] * remainingdbuf) / tempplaneratesum) < tempplanedbuf[i])
                            {
                                planealloc[pipeid , i] = tempplanedbuf[i];
                                planeallocfinal[pipeid , i] = true;
                                remainingdbuf = remainingdbuf - tempplanedbuf[i];
                                tempplanerate[i] = 0;
                                tempplaneratesum = 0;
                                for (uint k = 0; k < planemax; k++)
                                    tempplaneratesum = tempplaneratesum + tempplanerate[k];

                                for (uint k = 0; k < i; k++)
                                    if ((uPlanerate[pipeid , k] > 0) && (planeallocfinal[pipeid , k] == false))
                                        recompute = 1;
                                if (recompute == 0)
                                {
                                    uint count = 0;
                                    for (uint k = i; k < planemax; k++)
                                        if ((uPlanerate[pipeid, k] > 0) && (planeallocfinal[pipeid, k] == false))
                                            count++;
                                    if (count == 0)
                                        exit = 1;
                                    else continue;
                                }

                            }
                            else
                            {
                                planealloc[pipeid , i] = (uint)((tempplanerate[i] * remainingdbuf) / tempplaneratesum);
                                uint count = 0;
                                for (uint k = i; k < planemax; k++)
                                    if ((uPlanerate[pipeid , k] > 0) && (planeallocfinal[pipeid , k] == false))
                                        count++;
                                if (count == 1)
                                {
                                    //planeallocfinal[pipeid , k] = true;
                                   // remainingdbuf = remainingdbuf - temppipedbuf[i];
                                    exit = 1;
                                }
                            }

                            if (recompute == 1)
                                break;
                        }
                    }

                    if (exit == 1)
                        break;

                } while (true);

                planealloc[pipeid, 0] = planealloc[pipeid, 0] + curDisp.DbufAllocated - (planealloc[pipeid, 0] + planealloc[pipeid, 1] + planealloc[pipeid, 2]);

                uint sum = curDisp.PlaneA.DbufAllocated + curDisp.PlaneB.DbufAllocated + curDisp.PlaneC.DbufAllocated;
                Log.Message("after re distributing");
                if (remainingdbuf > 0)
                {
                    //curDisp.PlaneA.DbufAllocated = curDisp.PlaneA.DbufAllocated + Convert.ToUInt32(Math.Ceiling(remainingDBuf * curDisp.PlaneA.DbufAllocated / (float)sum));

                    //curDisp.PlaneB.DbufAllocated = curDisp.PlaneB.DbufAllocated + Convert.ToUInt32(Math.Ceiling(remainingDBuf * curDisp.PlaneB.DbufAllocated / (float)sum));

                    //curDisp.PlaneC.DbufAllocated = curDisp.PlaneC.DbufAllocated + Convert.ToUInt32(Math.Ceiling(remainingDBuf * curDisp.PlaneC.DbufAllocated / (float)sum));

                    //curDisp.PlaneA.DbufAllocated = curDisp.PlaneA.DbufAllocated + (remainingdbuf * curDisp.PlaneA.DbufAllocated / sum);

                   // curDisp.PlaneB.DbufAllocated = curDisp.PlaneB.DbufAllocated + (remainingdbuf * curDisp.PlaneB.DbufAllocated / sum);

                    //curDisp.PlaneC.DbufAllocated = curDisp.PlaneC.DbufAllocated + (remainingdbuf * curDisp.PlaneC.DbufAllocated / sum);

                    curDisp.PlaneA.DbufAllocated = planealloc[pipeid, 0];
                    curDisp.PlaneB.DbufAllocated = planealloc[pipeid, 1];
                    curDisp.PlaneC.DbufAllocated = planealloc[pipeid, 2];


                    sum = curDisp.PlaneA.DbufAllocated + curDisp.PlaneB.DbufAllocated + curDisp.PlaneC.DbufAllocated;
                    Log.Message("The Sum is {0} , pipe_allocated {1} and difference is {2}", sum, curDisp.DbufAllocated, curDisp.DbufAllocated - sum);

                    if (curDisp.DbufAllocated > sum)
                    {
                        curDisp.PlaneA.DbufAllocated = curDisp.PlaneA.DbufAllocated + curDisp.DbufAllocated - sum;
                    }
                    Log.Message("{0} Plane A -> {1} ", curDisp.DisplayType, curDisp.PlaneA.DbufAllocated);
                    Log.Message("{0} Plane b -> {1} ", curDisp.DisplayType, curDisp.PlaneB.DbufAllocated);
                    Log.Message("{0} Plane C -> {1} ", curDisp.DisplayType, curDisp.PlaneC.DbufAllocated);

                    if (Math.Abs((int)curDisp.PlaneA.PlaneBufCFGTotalBlock - (int)curDisp.PlaneA.DbufAllocated) > 6)
                        Log.Fail("Plane A programmed dbuf {0} does not match with expected dbuf {1}", curDisp.PlaneA.PlaneBufCFGTotalBlock, curDisp.PlaneA.DbufAllocated);
                    else
                        Log.Success("Plane A programmed dbuf {0} matches with expected dbuf {1} within acceptable error limit of 6", curDisp.PlaneA.PlaneBufCFGTotalBlock, curDisp.PlaneA.DbufAllocated);
                    if (curDisp.PlaneB.Enabled)
                    {
                        if (Math.Abs((int)curDisp.PlaneB.PlaneBufCFGTotalBlock - (int)curDisp.PlaneB.DbufAllocated) > 6)
                            Log.Fail("Plane B programmed dbuf {0} does not match with expected dbuf {1}", curDisp.PlaneB.PlaneBufCFGTotalBlock, curDisp.PlaneB.DbufAllocated);
                        else
                            Log.Success("Plane B programmed dbuf {0} matches with expected dbuf {1} within acceptable error limit of 6", curDisp.PlaneB.PlaneBufCFGTotalBlock, curDisp.PlaneB.DbufAllocated);
                    }
                    if (curDisp.PlaneC.Enabled)
                    {
                        if (Math.Abs((int)curDisp.PlaneC.PlaneBufCFGTotalBlock - (int)curDisp.PlaneC.DbufAllocated) > 6)
                            Log.Fail("Plane C programmed dbuf {0} does not match with expected dbuf {1}", curDisp.PlaneC.PlaneBufCFGTotalBlock, curDisp.PlaneC.DbufAllocated);
                        else
                            Log.Success("Plane C programmed dbuf {0} matches with expected dbuf {1} within acceptable error limit of 6", curDisp.PlaneC.PlaneBufCFGTotalBlock, curDisp.PlaneC.DbufAllocated);
                    }
                }
            });

            return dbufList;
        }
        public uint UpdatePlaneDbuf(PipeDbufInfo curDbuf,PLANE argPlane, uint argDispSurfaceWidth, string argSourcePixelFormat, string argRotation, uint argRemainingDBuf, TileFormat argTileFormat , uint planeid)
        {
            uint value = calculateDBuf(curDbuf , planeid);
            if (value < argRemainingDBuf)
                return value;
            else
                if (argRemainingDBuf >= 8)    // Y-tiling Will fail passing only 8 for X-tiling 
                    return 8;
            return 0;
        }

        private void ReadRegister(uint offset, ref uint regValue)
        {
            DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
            driverData.input = offset;

            DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.DIVAMMIORead, driverData);
            DriverEscape escape = new DriverEscape();

            if (!escape.SetMethod(driverParams))
                Log.Fail("Failed to read Register with offset as {0}", driverData.input);
            else
            {
                Log.Message("Offset: {0} Value from registers = {1}", offset, driverData.output.ToString("X"));
                regValue = driverData.output;
            }
        }

        private void WriteRegister(uint offset, uint regValue)
        {
            DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
            driverData.input = offset;
            driverData.output = regValue;

            DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.DIVAMMIOWrite, driverData);
            DriverEscape escape = new DriverEscape();

            if (!escape.SetMethod(driverParams))
                Log.Fail("Failed to write Register with offset {0} and value: {1}", driverData.input.ToString("X"), driverData.output.ToString("X"));
            else
                Log.Message("Written Offset: {0} with Value: {1}", offset.ToString("X"), driverData.output.ToString("X"));
        }

        private double CalculateSystemMemoryBandwidth()
        {
            double rawsystembw;
            uint uMemoryFreqRegister = 0;
            uint uMemoryChannel0 = 0 ;
            uint uMemoryChannel1 = 0;
            

            if (base.AppManager.MachineInfo.PlatformDetails.Platform == Platform.BXT || base.AppManager.MachineInfo.PlatformDetails.Platform == Platform.GLK)
            {
                ReadRegister((uint)0x147114, ref uMemoryFreqRegister);
                ReadRegister((uint)0x147114, ref uMemoryChannel0);
                ReadRegister((uint)0x147114, ref uMemoryChannel1);

                if ((uMemoryChannel0 & 0x00005000) == 0x00005000)
                {
                    uNoMemoryChannel++;
                }
                if ((uMemoryChannel1 & 0x0000A000) == 0x0000A000)
                {
                    uNoMemoryChannel++;
                }
                rawsystembw = uMemoryFreqRegister & 0x0000003F;
                rawsystembw = rawsystembw * 133.33;
            }
            else
            {
                ReadRegister((uint)0x145E04, ref uMemoryFreqRegister);
                ReadRegister((uint)0x14500C, ref uMemoryChannel0);
                ReadRegister((uint)0x145010, ref uMemoryChannel1);

                if (uMemoryChannel0 > 0)
                {
                    uNoMemoryChannel++;
                }
                if (uMemoryChannel1 > 0)
                {
                    uNoMemoryChannel++;
                }

                rawsystembw = (uMemoryFreqRegister & 0x0000000F) * 133.33 * 2 * 8 * uNoMemoryChannel;

                // if any one slot has dual rank memory , then consider as dual rank
                if (((uMemoryChannel0 & 0x00000400) == 0x00000400) || ((uMemoryChannel0 & 0x04000000) == 0x04000000))
                {
                    uMemoryRankCh0 = 2;
                }

                if (((uMemoryChannel1 & 0x00000400) == 0x00000400) || ((uMemoryChannel1 & 0x04000000) == 0x04000000))
                {
                    uMemoryRankCh1 = 2;
                }

                // if both slots have single rank memory then consider as dual rank
                if ((((uMemoryChannel0 & 0x0000003f) > 0) && ((uMemoryChannel0 & 0x04000000) == 0x00000000)) && (((uMemoryChannel0 & 0x0000003f) > 0) && ((uMemoryChannel0 & 0x00000400) == 0x00000000)))
                {
                    uMemoryRankCh0 = 2;
                }

                if ((((uMemoryChannel1 & 0x0000003f) > 0) && ((uMemoryChannel1 & 0x04000000) == 0x00000000)) && (((uMemoryChannel1 & 0x0000003f) > 0) && ((uMemoryChannel1 & 0x00000400) == 0x00000000)))
                {
                    uMemoryRankCh1 = 2;
                }

                uMemoryRank = Math.Min(uMemoryRankCh0, uMemoryRankCh1);
            }

           return rawsystembw;
        }

        private double CalculateArbitratedMemoryBandwidth()
        {

            double arbitratedbw = 0;

            if (base.AppManager.MachineInfo.PlatformDetails.Platform == Platform.BXT || base.AppManager.MachineInfo.PlatformDetails.Platform == Platform.GLK)
            {
               for (uint i = 0 ; i < pipemax ; i++)
                {
                    if (((uTrans_CONF[i] & 0x80000000) == 0x80000000) && ((uTrans_DDI[i] & 0x80000000) == 0x80000000))
                    {
                        pixelrate[i] = GetPortPLLFrequency_BXT(i);
                    }
                }

                // edp transcoder can be mapped to any pipe , so checking that and updating pixel clock of respective pipe
                if (((uTrans_CONF[3] & 0x80000000) == 0x80000000) && ((uTrans_DDI[3] & 0x80000000) == 0x80000000))
                {
                    switch ((uTrans_DDI[3] & 0x00007000) >> 12)
                    {
                        case 0:
                            pixelrate[0] = GetPortPLLFrequency_BXT(3);
                            break;
                        case 5:
                            pixelrate[1] = GetPortPLLFrequency_BXT(3);
                            break;
                        case 6:
                            pixelrate[2] = GetPortPLLFrequency_BXT(3);
                            break;
                        default:
                            break;
                    }
                }

                //mipi transcoders can be mapped to any pipe , checking that and updating pixel clock of respective pipe

                if ((uMIPIaPortStatus & 0x80000000) == 0x80000000)
                {
                    switch ((uMIPIaCtrl & 0x00000380) >> 7)
                    {
                        case 0:
                            pixelrate[0] = ((uDsiPLLCtl & 0x000000FF) * 19.2 * Math.Pow(2 , (double)(uMIPIaPortStatus & 0x00000001))) / 12 ; 
                            break;
                        case 1:
                            pixelrate[1] = ((uDsiPLLCtl & 0x000000FF) * 19.2 * Math.Pow(2 , (double)(uMIPIaPortStatus & 0x00000001))) / 12 ;
                            break;
                        case 2:
                            pixelrate[2] = ((uDsiPLLCtl & 0x000000FF) * 19.2 * Math.Pow(2, (double)(uMIPIaPortStatus & 0x00000001))) / 12;
                            break;
                        default:
                            break;
                    }
                }
            }

            else // for Gen 9 platforms other than BXT
            {
                for (uint i = 0; i < pipemax; i++)
                {
                    if (((uTrans_CONF[i] & 0x80000000) == 0x80000000) && ((uTrans_DDI[i] & 0x80000000) == 0x80000000))
                    {
                        pixelrate[i] = GetPortPLLFrequency_Gen9(i);
                    }
                }

                // edp transcoder can be mapped to any pipe , so checking that and updating pixel clock of respective pipe
                if (((uTrans_CONF[3] & 0x80000000) == 0x80000000) && ((uTrans_DDI[3] & 0x80000000) == 0x80000000))
                {
                    switch ((uTrans_DDI[3] & 0x00007000) >> 12)
                    {
                        case 0:
                            pixelrate[0] = GetPortPLLFrequency_Gen9(3);
                            break;
                        case 5:
                            pixelrate[1] = GetPortPLLFrequency_Gen9(3);
                            break;
                        case 6:
                            pixelrate[2] = GetPortPLLFrequency_Gen9(3);
                            break;
                        default:
                            break;
                    }
                }
            }

            uint pipecount = 0;

            if (pixelrate[0] > 0) pipecount++;
            if (pixelrate[1] > 0) pipecount++;
            if (pixelrate[2] > 0) pipecount++;


            for (uint i = 0; i < pipemax; i++)
            {
                uint planecount = 0;
                for (uint j = 0; (j < planemax ) && ((uPlane_CTL[i,j] & 0x80000000) == 0x80000000); j++)
                {
                    planecount++;
                    double pipescaling = GetDownscalingAmount_Pipe(i);
                    double planescaling = GetDownscalingAmount_Plane(i , j);
                    double adjustedpixelrate = pixelrate[i] * pipescaling;
                    double adjustedplanerate = adjustedpixelrate * planescaling;
                    double Bpp = GetPlaneBpp(i, j);
                    // we need to consider pipe and plane downscaling , simplifying by checking net downscaling , ignoring whether it is for plane / pipe since both are required finally.
                    uPlaneBW[i,j] = adjustedplanerate * Bpp;
                 }

                uPipeBW[i] = Math.Max(Math.Max(uPlaneBW[i,0],uPlaneBW[i,1]),uPlaneBW[i,2]) * planecount;
            }

            arbitratedbw = Math.Max(Math.Max(uPipeBW[0], uPipeBW[1]), uPipeBW[2]) * pipecount;


            //Watermark w = new Watermark();
            //base.CopyOver(w);
            //w.GetMethod();
                return arbitratedbw;
            
        }

        private double GetPortPLLFrequency_Gen9(uint pipeid)
        {
            uint uDpll1_Cfgcr1 = 0;
            uint uDpll1_Cfgcr2 = 0;
            uint uDpll2_Cfgcr1 = 0;
            uint uDpll2_Cfgcr2 = 0;
            uint uDpll3_Cfgcr1 = 0;
            uint uDpll3_Cfgcr2 = 0;
            uint uDpll_Ctrl1 = 0;
            uint uDpll_Ctrl2 = 0;
            uint[] uPort_Clk_Sel = {0 , 0, 0 ,0 ,0};
            uint transm = 0;
            uint transn = 0;
            double pixelclock = 0;
            uint linkrate = 0;

            ReadRegister((uint)0x6C058, ref uDpll_Ctrl1);
            ReadRegister((uint)0x6C05C, ref uDpll_Ctrl2);
            ReadRegister((uint)0x46100, ref uPort_Clk_Sel[0]);
            ReadRegister((uint)0x46104, ref uPort_Clk_Sel[1]);
            ReadRegister((uint)0x46108, ref uPort_Clk_Sel[2]);
            ReadRegister((uint)0x4610C, ref uPort_Clk_Sel[3]);
            ReadRegister((uint)0x46110, ref uPort_Clk_Sel[4]);
            ReadRegister((uint)0x6C040, ref uDpll1_Cfgcr1);
            ReadRegister((uint)0x6C044, ref uDpll1_Cfgcr2);
            ReadRegister((uint)0x6C048, ref uDpll2_Cfgcr1);
            ReadRegister((uint)0x6C04C, ref uDpll2_Cfgcr2);
            ReadRegister((uint)0x6C050, ref uDpll3_Cfgcr1);
            ReadRegister((uint)0x6C054, ref uDpll3_Cfgcr2);


            if (((uTrans_DDI[pipeid] & 0x07000000) == 0x02000000) || ((uTrans_DDI[pipeid] & 0x07000000) == 0x03000000))
            {
                switch ((uTrans_DDI[pipeid] & 0x70000000) >> 28)   // ddi select
                {
                    case 1:
                        if ((uDpll_Ctrl2 & 0x00000030) >> 4 == 0)  // pll select
                            linkrate = (uDpll_Ctrl1 & 0x0000000E) >> 1;  //link rate select
                        if ((uDpll_Ctrl2 & 0x00000030) >> 4 == 1)
                            linkrate = (uDpll_Ctrl1 & 0x00000380) >> 7;
                        if ((uDpll_Ctrl2 & 0x00000030) >> 4 == 2)
                            linkrate = (uDpll_Ctrl1 & 0x0000E000) >> 13;
                        if ((uDpll_Ctrl2 & 0x00000030) >> 4 == 3)
                            linkrate = (uDpll_Ctrl1 & 0x00380000) >> 19;
                        break;

                    case 2:
                        if ((uDpll_Ctrl2 & 0x00000180) >> 7 == 0)  // pll select
                            linkrate = (uDpll_Ctrl1 & 0x0000000E) >> 1;  //link rate select
                        if ((uDpll_Ctrl2 & 0x00000180) >> 7 == 1)
                            linkrate = (uDpll_Ctrl1 & 0x00000380) >> 7;
                        if ((uDpll_Ctrl2 & 0x00000180) >> 7 == 2)
                            linkrate = (uDpll_Ctrl1 & 0x0000E000) >> 13;
                        if ((uDpll_Ctrl2 & 0x00000180) >> 7 == 3)
                            linkrate = (uDpll_Ctrl1 & 0x00380000) >> 19;
                        break;

                    case 3:
                        if ((uDpll_Ctrl2 & 0x00000C00) >> 10 == 0)  // pll select
                            linkrate = (uDpll_Ctrl1 & 0x0000000E) >> 1;  //link rate select
                        if ((uDpll_Ctrl2 & 0x00000C00) >> 10 == 1)
                            linkrate = (uDpll_Ctrl1 & 0x00000380) >> 7;
                        if ((uDpll_Ctrl2 & 0x00000C00) >> 10 == 2)
                            linkrate = (uDpll_Ctrl1 & 0x0000E000) >> 13;
                        if ((uDpll_Ctrl2 & 0x00000C00) >> 10 == 3)
                            linkrate = (uDpll_Ctrl1 & 0x00380000) >> 19;
                        break;

                    case 4:
                        if ((uDpll_Ctrl2 & 0x00006000) >> 13 == 0)  // pll select
                            linkrate = (uDpll_Ctrl1 & 0x0000000E) >> 1;  //link rate select
                        if ((uDpll_Ctrl2 & 0x00006000) >> 13 == 1)
                            linkrate = (uDpll_Ctrl1 & 0x00000380) >> 7;
                        if ((uDpll_Ctrl2 & 0x00006000) >> 13 == 2)
                            linkrate = (uDpll_Ctrl1 & 0x0000E000) >> 13;
                        if ((uDpll_Ctrl2 & 0x00006000) >> 13 == 3)
                            linkrate = (uDpll_Ctrl1 & 0x00380000) >> 19;
                        break;
                    default:
                        break;
                }

                if (pipeid == 3) // eDP transcoder always maps to ddi_a clock
                {
                    if ((uDpll_Ctrl2 & 0x00000006) >> 1 == 0)  // pll select
                        linkrate = (uDpll_Ctrl1 & 0x0000000E) >> 1;  //link rate select
                    if ((uDpll_Ctrl2 & 0x00000006) >> 1 == 1)
                        linkrate = (uDpll_Ctrl1 & 0x00000380) >> 7;
                    if ((uDpll_Ctrl2 & 0x00000006) >> 1 == 2)
                        linkrate = (uDpll_Ctrl1 & 0x0000E000) >> 13;
                    if ((uDpll_Ctrl2 & 0x00000006) >> 1 == 3)
                        linkrate = (uDpll_Ctrl1 & 0x00380000) >> 19;
                }

                switch (linkrate)
                {
                    case 0:
                        linkrate = 540;
                        break;
                    case 1:
                        linkrate = 270;
                        break;
                    case 2:
                        linkrate = 162;
                        break;
                    case 3:
                        linkrate = 324;
                        break;
                    case 4:
                        linkrate = 216;
                        break;
                    case 5:
                        linkrate = 432;
                        break;
                }

                transm = uTRANS_LINKM1[pipeid] & 0x00FFFFFF;
                transn = uTRANS_LINKN1[pipeid] & 0x00FFFFFF;
                pixelclock = ((double)linkrate * transm) / transn;
            }

            else
            {            // this is for HDMI / DVI . eDP / DP should not enter here
                switch ((uTrans_DDI[pipeid] & 0x70000000) >> 28)   // ddi select
                {
                    case 1:
                        if ((uDpll_Ctrl2 & 0x00000030) >> 4 == 1)
                            pixelclock = GetHDMIFrequency_Gen9(uDpll1_Cfgcr1, uDpll1_Cfgcr2);
                        if ((uDpll_Ctrl2 & 0x00000030) >> 4 == 2)
                            pixelclock = GetHDMIFrequency_Gen9(uDpll2_Cfgcr1, uDpll2_Cfgcr2);
                        if ((uDpll_Ctrl2 & 0x00000030) >> 4 == 3)
                            pixelclock = GetHDMIFrequency_Gen9(uDpll3_Cfgcr1, uDpll3_Cfgcr2);
                        break;

                    case 2:
                        if ((uDpll_Ctrl2 & 0x00000180) >> 7 == 1)
                            pixelclock = GetHDMIFrequency_Gen9(uDpll1_Cfgcr1, uDpll1_Cfgcr2);
                        if ((uDpll_Ctrl2 & 0x00000180) >> 7 == 2)
                            pixelclock = GetHDMIFrequency_Gen9(uDpll2_Cfgcr1, uDpll2_Cfgcr2);
                        if ((uDpll_Ctrl2 & 0x00000180) >> 7 == 3)
                            pixelclock = GetHDMIFrequency_Gen9(uDpll3_Cfgcr1, uDpll3_Cfgcr2);
                        break;

                    case 3:
                        if ((uDpll_Ctrl2 & 0x00000C00) >> 10 == 1)
                            pixelclock = GetHDMIFrequency_Gen9(uDpll1_Cfgcr1, uDpll1_Cfgcr2);
                        if ((uDpll_Ctrl2 & 0x00000C00) >> 10 == 2)
                            pixelclock = GetHDMIFrequency_Gen9(uDpll2_Cfgcr1, uDpll2_Cfgcr2);
                        if ((uDpll_Ctrl2 & 0x00000C00) >> 10 == 3)
                            pixelclock = GetHDMIFrequency_Gen9(uDpll3_Cfgcr1, uDpll3_Cfgcr2);
                        break;

                    case 4:
                        if ((uDpll_Ctrl2 & 0x00006000) >> 13 == 1)
                            pixelclock = GetHDMIFrequency_Gen9(uDpll1_Cfgcr1, uDpll1_Cfgcr2);
                        if ((uDpll_Ctrl2 & 0x00006000) >> 13 == 2)
                            pixelclock = GetHDMIFrequency_Gen9(uDpll2_Cfgcr1, uDpll2_Cfgcr2);
                        if ((uDpll_Ctrl2 & 0x00006000) >> 13 == 3)
                            pixelclock = GetHDMIFrequency_Gen9(uDpll3_Cfgcr1, uDpll3_Cfgcr2);
                        break;
                    default:
                        break;
                }
            }
            return pixelclock;
        }

        private double GetHDMIFrequency_Gen9 (uint reg1, uint reg2)
        {
            uint dcofraction = (reg1 & 0x00FFFE000) >> 9;
            uint dcointeger = (reg1 & 0x000001FF) ;
            uint centralfreq = reg2 & 0x00000003;
            uint p0 = (reg2 & 0x0000001C) >> 2;
            uint p1 = 0;
            uint p2 = (reg2 & 0x00000060) >> 5;
            double dcofreq = 0;


            	if (centralfreq == 0)
                    centralfreq = 9600;
	            else if (centralfreq == 1)
		            centralfreq = 9000;
	            else if (centralfreq == 3)
		            centralfreq = 	8400;
	            else centralfreq = 0;

            if (p0 == 0)
                p0 = 1;
            else if (p0 == 1)
                p0 = 2;
            else if (p0 == 2)
                p0 = 3;
            else if (p0 == 4)
                p0 = 7;
            else
                p0 = 0;

            if ((reg2 & 0x00000080) == 0x00000080)
                p1 = (reg2 & 0x0000FF00) >> 8;
            else
                p1 = 1;

            if (p2 == 0)
                p2 = 5;
            else if (p2 == 1)
                p2 = 2;
            else if (p2 == 2)
                p2 = 3;
            else if (p2 == 3)
                p2 = 1;
            else 
                p2 = 0;

            dcofreq = (double)(dcointeger * 24) + (((double)dcofraction * 24)/ Math.Pow(2,15)) ;
            dcofreq = dcofreq / (p0 * p1 * p2 * 5);

	            
            return dcofreq;
        }

        private double GetPortPLLFrequency_BXT(uint pipeid)
        {
            uint p1 = 1;
            uint p2 = 1;
            uint m2 = 0; 
            uint m2frac = 0;
            uint[] uPort_PLL_0 = {0, 0 , 0};
            uint[] uPort_PLL_2 = {0 , 0, 0};
            uint[] uPort_PLL_Ebb_0 = { 0, 0, 0 };
            double pixelclock;
            uint transm = 0;
            uint transn = 0;



            ReadRegister((uint)0x162100, ref  uPort_PLL_0[0]);
            ReadRegister((uint)0x6C100, ref  uPort_PLL_0[1]);
            ReadRegister((uint)0x6C380, ref  uPort_PLL_0[2]);
            ReadRegister((uint)0x162108, ref  uPort_PLL_2[0]);
            ReadRegister((uint)0x6C108, ref  uPort_PLL_2[1]);
            ReadRegister((uint)0x6C388, ref  uPort_PLL_2[2]);
            ReadRegister((uint)0x162034, ref  uPort_PLL_Ebb_0[0]);
            ReadRegister((uint)0x6C034, ref  uPort_PLL_Ebb_0[1]);
            ReadRegister((uint)0x6C340, ref  uPort_PLL_Ebb_0[2]);

            if (base.AppManager.MachineInfo.PlatformDetails.Platform == Platform.GLK)
            {
                ReadRegister((uint)0x163100, ref  uPort_PLL_0[2]);
                ReadRegister((uint)0x163108, ref  uPort_PLL_2[2]);
                ReadRegister((uint)0x163034, ref  uPort_PLL_Ebb_0[2]);
            }

            switch ((uTrans_DDI[pipeid] & 0x70000000) >> 28) // selecting ddib / ddic and assigning pll parameters accordingly
            {
                case 1:
                    p1 = (uPort_PLL_Ebb_0[1] & 0x0000E000) >> 13;
                    p2 = (uPort_PLL_Ebb_0[1] & 0x00001F00) >> 8;
                    m2 = uPort_PLL_0[1] & 0x000000FF;
                    m2frac = uPort_PLL_2[1] & 0x003FFFFF;
                    break;
                case 2:
                    p1 = (uPort_PLL_Ebb_0[2] & 0x0000E000) >> 13;
                    p2 = (uPort_PLL_Ebb_0[2] & 0x00001F00) >> 8;
                    m2 = uPort_PLL_0[2] & 0x000000FF;
                    m2frac = uPort_PLL_2[2] & 0x003FFFFF;
                    break;
                default:
                    break;
            }

            if (pipeid == 3)
            {
                    p1 = (uPort_PLL_Ebb_0[0] & 0x0000E000) >> 13;
                    p2 = (uPort_PLL_Ebb_0[0] & 0x00001F00) >> 8;
                    m2 = uPort_PLL_0[0] & 0x000000FF;
                    m2frac = uPort_PLL_2[0] & 0x003FFFFF;
            }

            pixelclock = ((m2 + (m2frac / Math.Pow(2,22))) * 400 )/(p1 * p2 * 10);

            if (((uTrans_DDI[pipeid] & 0x07000000) == 0x02000000) || ((uTrans_DDI[pipeid] & 0x07000000) == 0x03000000)) //dpmode
            {
                transm = uTRANS_LINKM1[pipeid] & 0x00FFFFFF;
                transn = uTRANS_LINKN1[pipeid] & 0x00FFFFFF;
                pixelclock = (pixelclock * transm) / transn;
            }

            return pixelclock;
        }

        private void InitializePipeRegisters()
        {
            ReadRegister((uint)0x6001C, ref uPipe_SRC_SZ[0]);
            ReadRegister((uint)0x6101C, ref uPipe_SRC_SZ[1]);
            ReadRegister((uint)0x6201C, ref uPipe_SRC_SZ[2]);
            ReadRegister((uint)0x70008, ref uTrans_CONF[0]);
            ReadRegister((uint)0x71008, ref uTrans_CONF[1]);
            ReadRegister((uint)0x72008, ref uTrans_CONF[2]);
            ReadRegister((uint)0x7F008, ref uTrans_CONF[3]);//edp transcoder
            ReadRegister((uint)0x60400, ref uTrans_DDI[0]);
            ReadRegister((uint)0x61400, ref uTrans_DDI[1]);
            ReadRegister((uint)0x62400, ref uTrans_DDI[2]);
            ReadRegister((uint)0x6F400, ref uTrans_DDI[3]);//edp transcoder
            ReadRegister((uint)0x60040, ref uTRANS_LINKM1[0]);
            ReadRegister((uint)0x61040, ref uTRANS_LINKM1[1]);
            ReadRegister((uint)0x62040, ref uTRANS_LINKM1[2]);
            ReadRegister((uint)0x6F040, ref uTRANS_LINKM1[3]);
            ReadRegister((uint)0x60044, ref uTRANS_LINKN1[0]);
            ReadRegister((uint)0x61044, ref uTRANS_LINKN1[1]);
            ReadRegister((uint)0x62044, ref uTRANS_LINKN1[2]);
            ReadRegister((uint)0x6F044, ref uTRANS_LINKN1[3]);
            ReadRegister((uint)0x68180, ref uScalar_CTL[0,0]);
            ReadRegister((uint)0x68280, ref uScalar_CTL[0,1]);
            ReadRegister((uint)0x68980, ref uScalar_CTL[1,0]);
            ReadRegister((uint)0x68A80, ref uScalar_CTL[1,1]);
            ReadRegister((uint)0x69180, ref uScalar_CTL[2,0]);
            ReadRegister((uint)0x69280, ref uScalar_CTL[2,1]);
            ReadRegister((uint)0x68190, ref uScalar_H[0, 0]);
            ReadRegister((uint)0x68290, ref uScalar_H[0, 1]);
            ReadRegister((uint)0x68990, ref uScalar_H[1, 0]);
            ReadRegister((uint)0x68A90, ref uScalar_H[1, 1]);
            ReadRegister((uint)0x69190, ref uScalar_H[2, 0]);
            ReadRegister((uint)0x69290, ref uScalar_H[2, 1]);
            ReadRegister((uint)0x68190, ref uScalar_V[0, 0]);
            ReadRegister((uint)0x68290, ref uScalar_V[0, 1]);
            ReadRegister((uint)0x68990, ref uScalar_V[1, 0]);
            ReadRegister((uint)0x68A90, ref uScalar_V[1, 1]);
            ReadRegister((uint)0x69190, ref uScalar_V[2, 0]);
            ReadRegister((uint)0x69290, ref uScalar_V[2, 1]);
            ReadRegister((uint)0x60000, ref uTrans_Htotal[0]);
            ReadRegister((uint)0x61000, ref uTrans_Htotal[1]);
            ReadRegister((uint)0x62000, ref uTrans_Htotal[2]);
            ReadRegister((uint)0x6F000, ref uTrans_Htotal[3]);



        }

        private void InitializePlaneRegisters()
        {
            ReadRegister((uint)0x70180, ref uPlane_CTL[0,0]);
            ReadRegister((uint)0x70280, ref uPlane_CTL[0,1]);
            ReadRegister((uint)0x70380, ref uPlane_CTL[0,2]);
            ReadRegister((uint)0x71180, ref uPlane_CTL[1,0]);
            ReadRegister((uint)0x71280, ref uPlane_CTL[1,1]);
            ReadRegister((uint)0x71380, ref uPlane_CTL[1,2]);
            ReadRegister((uint)0x72180, ref uPlane_CTL[2,0]);
            ReadRegister((uint)0x72280, ref uPlane_CTL[2,1]);
            ReadRegister((uint)0x72380, ref uPlane_CTL[2,2]);
            ReadRegister((uint)0x70190, ref uPlane_Size[0,0]);
            ReadRegister((uint)0x70290, ref uPlane_Size[0, 1]);
            ReadRegister((uint)0x70390, ref uPlane_Size[0, 2]);
            ReadRegister((uint)0x71190, ref uPlane_Size[1, 0]);
            ReadRegister((uint)0x71290, ref uPlane_Size[1, 1]);
            ReadRegister((uint)0x71390, ref uPlane_Size[1, 2]);
            ReadRegister((uint)0x72190, ref uPlane_Size[2, 0]);
            ReadRegister((uint)0x72290, ref uPlane_Size[2, 1]);
            ReadRegister((uint)0x72390, ref uPlane_Size[2, 2]);
        }

        private void InitializeMipiRegisters()
        {
            ReadRegister((uint)0x46080, ref uDsiPLLStatus);
            if ((uDsiPLLStatus & 0x80000000) == 0x80000000)
            {
                ReadRegister((uint)0x6B0C0, ref uMIPIaPortStatus);
                ReadRegister((uint)0x6B8C0, ref uMIPIcPortStatus);
                ReadRegister((uint)0x6B104, ref uMIPIaCtrl);
                ReadRegister((uint)0x6B904, ref uMIPIcCtrl);
                ReadRegister((uint)0x161000, ref uDsiPLLCtl);
            }
        }

        private double GetDownscalingAmount_Pipe(uint pipeid)
        {
            double downscale = 1;

            //if scalar is enabled , add to downscale factor if it is pipe scalar or check if planecontext is same as incoming plane id for plane scalars

            if (((uScalar_CTL[pipeid,0] & 0x80000000) != 0) && (((uScalar_CTL[pipeid,0] & 0x0E000000) == 0x00000000)))
            {
                downscale = downscale * Math.Max ((((uScalar_H[pipeid, 0] & 0x00038000) >> 15) + ((uScalar_H[pipeid, 0] & 0x00007FFF) / Math.Pow(2,15))) , 1);
                downscale = downscale * Math.Max ((((uScalar_V[pipeid, 0] & 0x00038000) >> 15) + ((uScalar_V[pipeid, 0] & 0x00007FFF) / Math.Pow(2,15))),  1);
            }

            if (((uScalar_CTL[pipeid, 1] & 0x80000000) != 0) && (((uScalar_CTL[pipeid, 1] & 0x0E000000) == 0x00000000)))
            {
                downscale = downscale * Math.Max((((uScalar_H[pipeid, 1] & 0x00038000) >> 15) + ((uScalar_H[pipeid, 1] & 0x00007FFF) / Math.Pow(2, 15))), 1);
                downscale = downscale * Math.Max((((uScalar_V[pipeid, 1] & 0x00038000) >> 15) + ((uScalar_V[pipeid, 1] & 0x00007FFF) / Math.Pow(2, 15))), 1);
            }

            return downscale;
        }

        private double GetDownscalingAmount_Plane(uint pipeid, uint planeid)
        {
            double downscale = 1;

            //if scalar is enabled , add to downscale factor if it is pipe scalar or check if planecontext is same as incoming plane id for plane scalars

            if (((uScalar_CTL[pipeid, 0] & 0x80000000) != 0) && (((uScalar_CTL[pipeid, 0] & 0x0E000000) != 0x00000000) && (((uScalar_CTL[pipeid, 0] & 0x0E000000) >> 25) == (planeid + 1))))
            {
                downscale = downscale * Math.Max((((uScalar_H[pipeid, 0] & 0x00038000) >> 15) + ((uScalar_H[pipeid, 0] & 0x00007FFF) / Math.Pow(2, 15))), 1);
                downscale = downscale * Math.Max((((uScalar_V[pipeid, 0] & 0x00038000) >> 15) + ((uScalar_V[pipeid, 0] & 0x00007FFF) / Math.Pow(2, 15))), 1);
            }

            if (((uScalar_CTL[pipeid, 1] & 0x80000000) != 0) && (((uScalar_CTL[pipeid, 1] & 0x0E000000) != 0x00000000) && (((uScalar_CTL[pipeid, 1] & 0x0E000000) >> 25) == (planeid + 1))))
            {
                downscale = downscale * Math.Max((((uScalar_H[pipeid, 1] & 0x00038000) >> 15) + ((uScalar_H[pipeid, 1] & 0x00007FFF) / Math.Pow(2, 15))), 1);
                downscale = downscale * Math.Max((((uScalar_V[pipeid, 1] & 0x00038000) >> 15) + ((uScalar_V[pipeid, 1] & 0x00007FFF) / Math.Pow(2, 15))), 1);
            }

            return downscale;
        }


        private double GetPlaneBpp(uint pipeid, uint planeid)
        {

            uint A1 = (uPlane_CTL[pipeid,planeid] & 0x0F000000) >> 24;
            
            switch (A1)
            {
                case 0 :
                    return 2;
                case 1 :
                    return 1.5;
                case 2 :
                    return 4;
                case 4:
                    return 4;
                case 6:
                    return 8;
                case 8:
                    return 4;
                case 10:
                    return 4;
                case 12:
                    return 1;
                case 14:
                    return 2;
                default:
                    return 0;

             } 
                  
         }

        private bool CheckforYtile()
        {

            for (uint i = 0; i < pipemax; i++)
            {
                
                for (uint j = 0; (j < planemax) && ((uPlane_CTL[i, j] & 0x80000000) == 0x80000000); j++)
                {
                    if ((uPlane_CTL[i,j] & 0x00001000) != 0)
                    {
                        return true;
                    }
                }

            }

            return false;
        }

        private uint[] CalculateMemorylatency_Gen9()
        {
            uint[] memlatency = {0,0,0,0,0,0,0,0};
            uint set = 0;
            ReadRegister((uint)0x45004, ref uArb_Ctl2);

            WriteRegister((uint)0x138128 ,(uint)0x00000000);
            WriteRegister((uint)0x13812C ,(uint)0x00000000);
            WriteRegister((uint)0x138124 ,(uint)0x80000006);

            ReadRegister((uint)0x138128 , ref set);

            memlatency[0] = (set & 0x000000FF);
            memlatency[1] = (set & 0x0000FF00) >> 8;
            memlatency[2] = (set & 0x00FF0000) >> 16;
            memlatency[3] = (set & 0xFF000000) >> 24;

            WriteRegister((uint)0x138128 ,(uint)0x00000001);
            WriteRegister((uint)0x13812C ,(uint)0x00000000);
            WriteRegister((uint)0x138124 ,(uint)0x80000006);

            ReadRegister((uint)0x138128 , ref set);

            memlatency[4] = (set & 0x000000FF);
            memlatency[5] = (set & 0x0000FF00) >> 8;
            memlatency[6] = (set & 0x00FF0000) >> 16;
            memlatency[7] = (set & 0xFF000000) >> 24;

            if (memlatency[0] == 0)
            {
                memlatency[0] = memlatency[0] + 2;
                memlatency[1] = memlatency[1] + 2;
                memlatency[2] = memlatency[2] + 2;
                memlatency[3] = memlatency[3] + 2;
                memlatency[4] = memlatency[4] + 2;
                memlatency[5] = memlatency[5] + 2;
                memlatency[6] = memlatency[6] + 2;
                memlatency[7] = memlatency[7] + 2;
            }

            if ((base.AppManager.MachineInfo.PlatformDetails.Platform == Platform.KBL) && ((uArb_Ctl2 & 0x00000008) == 0x00000008))
            {
                memlatency[0] = memlatency[0] + 4;
                memlatency[1] = memlatency[1] + 4;
                memlatency[2] = memlatency[2] + 4;
                memlatency[3] = memlatency[3] + 4;
                memlatency[4] = memlatency[4] + 4;
                memlatency[5] = memlatency[5] + 4;
                memlatency[6] = memlatency[6] + 4;
                memlatency[7] = memlatency[7] + 4;
            }

           return memlatency;
        }

        private uint CheckWMforDBUF(PipeDbufInfo display,  uint pipeid ,uint planeid ,uint latency , uint htotal , uint latencylevel, bool overlaykey)
        {
            double blocks = 0;
            double lines = 0;
            uint nv12 = 0;
        //Method 1
            double Bpp = GetPlaneBpp(pipeid, planeid);
            if (Bpp == 1.5) //NV12 only Y surface is considered for WM . So only 1 byte 
            {
                Bpp = 1;
                nv12 = 1;
            }

            double scaling = GetDownscalingAmount_Pipe(pipeid) * GetDownscalingAmount_Plane(pipeid, planeid);
            double method1 = (latency * pixelrate[pipeid] * scaling * Bpp) / 512;

            if ((wa != 0) && ((uPlane_CTL[pipeid,planeid] & 0x00001000) == 0x00000000))
                method1 = ((latency+15) * pixelrate[pipeid] * scaling * Bpp) / 512;


        // if overlaykey is true , then we assume xtile overlay plane same size as display plane buffer and we return Method 1 value   
            uint planewidth = (uPlane_Size[pipeid, planeid] & 0x00001FFF) + 1;
            double planebytesperline = planewidth * Bpp;
            double planeblocksperline = 0;
            if (overlaykey == true)
            {
                method1 = (latency * pixelrate[pipeid] * scaling * Bpp) / 512;
                if (wa != 0)
                {
                    method1 = ((latency + 15) * pixelrate[pipeid] * scaling * Bpp) / 512;
                    blocks = Math.Round(method1); 
                }
            }
            else
            {
                //Method 2


            if ((uPlane_CTL[pipeid, planeid] & 0x00001000) == 0x00000000) //xtile or linear
                planeblocksperline = Math.Ceiling(planebytesperline / 512);
            else // y tile
                planeblocksperline = Math.Ceiling(4 * planebytesperline / 512)/4;

            double method2 = Math.Ceiling((latency * pixelrate[pipeid] * scaling) / htotal) * planeblocksperline;

            if ((wa != 0) && ((uPlane_CTL[pipeid, planeid] & 0x00001000) == 0x00000000))
                method2 = Math.Ceiling(((latency+15) * pixelrate[pipeid] * scaling) / htotal) * planeblocksperline;

            double Ytilemin = 0;

            if ((uPlane_CTL[pipeid,planeid] & 0x00000001) == 1) //rotated plane
            {
                if (Bpp == 1) Ytilemin = 16 * planeblocksperline;
                if (Bpp == 2) Ytilemin = 8 * planeblocksperline;
            }
            else
            {
                Ytilemin = 4 * planeblocksperline;
            }

            if (wa == 1) Ytilemin = Ytilemin * 2;

            if ((uPlane_CTL[pipeid, planeid] & 0x00001000) == 0x00000000) // xtiled or linear
                blocks = Math.Max(method1, method2);
            else
                blocks = Math.Max(method2, Ytilemin);

            lines = Math.Ceiling(blocks / planeblocksperline);
            blocks = Math.Ceiling(blocks) + 1;

            if ((latencylevel > 0) && ((base.AppManager.MachineInfo.PlatformDetails.Platform != Platform.BXT) || (base.AppManager.MachineInfo.PlatformDetails.Platform != Platform.KBL) || (base.AppManager.MachineInfo.PlatformDetails.Platform == Platform.GLK)))
            {
                if ((uPlane_CTL[pipeid, planeid] & 0x00001000) == 0x00000000) // xtiled or linear
                {
                    blocks = blocks + 1;
                }
                else
                {
                    lines = lines + 4;
                    blocks = lines * planeblocksperline;
                }
                
            }
		}
            //if ((latencylevel > 0) && (base.AppManager.MachineInfo.PlatformEnum == Platform.KBL))
            //{
            //    if ((uPlane_CTL[pipeid, planeid] & 0x00001000) == 0x00000000) // xtiled or linear
            //    {
            //        blocks = blocks + 1;
            //    }
            //    else
            //    {
            //        lines = lines + 1;
            //        blocks = lines * planeblocksperline;
            //    }

            //}
            
            //if (((uPlane_CTL[pipeid, planeid] & 0x00001000) == 0x00001000) && (latencylevel > 0) && (nv12 == 1) && ((base.AppManager.MachineInfo.PlatformEnum == Platform.BXT) || (base.AppManager.MachineInfo.PlatformEnum == Platform.SKL)))
            //{
            //    lines = lines + 4;
            //    blocks = lines * planeblocksperline;
            //}

            return (uint)blocks;
        }

       //Code for MIPI htotal borrowed from Watermark files

        private uint GetHTotal_MIPIBXT()
        {
            uint uHtotal = 0;
            uint lane_cnt = 0, bpp = 0;
            uint HActive, HSync, HFPorch, HBPorch, HSyncStart, HSyncEnd = 0;

            // To calculate HTotal for MIPI in BXT MIPI  

            if (base.MachineInfo.PlatformDetails.Platform == Platform.BXT || base.AppManager.MachineInfo.PlatformDetails.Platform == Platform.GLK)
            {
                uint uMIPI_HSync = 0, uMIPI_HFrontPorch = 0, uMIPI_HBackPorch = 0, uMIPI_HActive = 0, uMIPIA_DSI = 0, uMIPIC_DSI = 0;

                ReadRegister((uint)0x6B028, ref uMIPI_HSync);
                ReadRegister((uint)0x6B02C, ref uMIPI_HFrontPorch);
                ReadRegister((uint)0x6B030, ref uMIPI_HBackPorch);
                ReadRegister((uint)0x6B034, ref uMIPI_HActive);
                ReadRegister((uint)0x6B00C, ref uMIPIA_DSI);
                ReadRegister((uint)0x6B80C, ref uMIPIC_DSI);

                // if ((((uMIPIA_PortCtrl & 0x80000000) == 0x80000000) && (((uMIPIACtrl & 0x00000380) >> 7) == pipeCount))) // CHeck for MIPI A enabld and pipe select
                if (((uMIPIaPortStatus & 0x80000000) == 0x80000000))
                {
                    uint A1 = 0;
                    A1 = (uMIPIA_DSI & 0x00000780) >> 7;

                    if (A1 == 1)
                        bpp = 16;
                    else if (A1 == 3)
                        bpp = 18;
                    else if (A1 == 4)
                        bpp = 24;

                    lane_cnt = uMIPIA_DSI & 0x00000007;

                }
                // if ((((uMIPIC_PortCtrl & 0x80000000) == 0x80000000) && (((uMIPIACtrl & 0x00000380) >> 7) == pipeCount))) // CHeck for MIPI C enabld and pipe select

                //uint A1 = 0;
                //A1 = (uMIPIC_DSI & 0x00000780) >> 7;

                //if (A1 == 1)
                //    bpp = 16;
                //else if (A1 == 3)
                //    bpp = 18;
                //else if (A1 == 4)
                //    bpp = 24;

                //lane_cnt = uMIPIC_DSI & 0x00000007;



                // To convert bytclk to pixelclk

                //ulValue = (ulPixelCount * pThis->m_ucBitsPerPixel) / (pThis->m_ucLaneCount * 8);

                HActive = (uint)Math.Ceiling(((double)uMIPI_HActive * lane_cnt * 8)) / bpp;

                HSync = (uint)Math.Ceiling(((double)uMIPI_HSync * lane_cnt * 8)) / bpp;

                HFPorch = (uint)Math.Ceiling(((double)uMIPI_HFrontPorch * lane_cnt * 8)) / bpp;

                HBPorch = (uint)Math.Ceiling(((double)uMIPI_HBackPorch * lane_cnt * 8)) / bpp;

                // HSyncStart = HFrontPorch + HActive
                HSyncStart = HFPorch + HActive;

                // HSyncEnd = HSync + (HSyncStart - 1)

                HSyncEnd = HSync + HSyncStart - 1;

                //Htotal = HBackPorch + HSyncEnd + 1

                uHtotal = HBPorch + HSyncEnd + 1;

                if (((uMIPIcPortStatus & 0x80000000) == 0x80000000))
                {
                    uHtotal = uHtotal * 2; // Only MIPI A is supported in BXT , if MIPI C is enabled then it should be dual link panel , hence doubling htotal.
                }
                Log.Verbose("\nMIPI HTotal calculated:" + (uHtotal));

            }

            return uHtotal;
        }
        
    }

}
