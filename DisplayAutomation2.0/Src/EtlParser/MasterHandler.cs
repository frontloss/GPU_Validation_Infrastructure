/**
* @file		MasterHandler.cs
* @brief	Contains MasterHandler class responsible for registering all the callbacks for ETL events
*
* @author	Rohit Kumar
*/

using EtlParser.Handlers;
using Microsoft.Diagnostics.Tracing;
using Microsoft.Diagnostics.Tracing.Parsers;
using Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriver;
using Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriverDisplay;
using System;
using GFX_DISPLAY_EXTERNAL = Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDisplayExternal;
using GFX_DISPLAY_DRIVER = Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriverDisplay;

namespace EtlParser
{
    /// <summary>
    /// MasterHandler class contains the wrapper functions for all the tagged events from IntelGfxDriver and IntelGfxDriverDisplay. 
    /// Wrapper function is responsible to do small operations on the incoming data or to forward the call to respective handler. MasterHandler class
    /// contains objects for all the handlers.
    /// </summary>
    class MasterHandler
    {
        public ParserConfig config;

        public DbgMsgHandler dbgMsgHandler = new DbgMsgHandler();
        public VbiHandler vbiHandler = new VbiHandler();
        public FlipHandler flipHandler = new FlipHandler();
        public DisplayDiagnosticsHandler displayDiagnosticsHandler = new DisplayDiagnosticsHandler();
        public MmioHandler mmioHandler = new MmioHandler();
        public DpcdHandler dpcdHandler = new DpcdHandler();
        public FunctionHandler functionHandler = new FunctionHandler();
        public CommonHandler commonHandler = new CommonHandler();
        public InterruptHandler interruptHandler = new InterruptHandler();
        public DpstHandler dpstHandler = new DpstHandler();
        public I2cHandler i2cHandler = new I2cHandler();
        public PsrHandler psrHandler = new PsrHandler();
        public DisplayDetectHandler displayDetectHandler = new DisplayDetectHandler();

        public MasterHandler(ParserConfig config)
        {
            this.config = config;
        }

        /// <summary>
        /// Process function is responsible to create ETWTraceEventSource from given ETL file and register all the callbacks. 
        /// </summary>
        /// <param name="inputFile">Full path of ETL file</param>
        public void Process(String inputFile)
        {
            // @todo validate inputFile

            // Create ETWTraceEventSource from given ETL file
            using (var source = new ETWTraceEventSource(inputFile))
            {
                // Use TraceEventParsers defined in Gfx Driver
                IntelGfxDriverTraceEventParser GfxParser = new IntelGfxDriverTraceEventParser(source);
                IntelGfxDriverPerfAnalysisTraceEventParser GfxInstrumentationParser = new IntelGfxDriverPerfAnalysisTraceEventParser(source);
                IntelGfxDriverDisplayTraceEventParser GfxDisplayParser = new IntelGfxDriverDisplayTraceEventParser(source);
                IntelGfxDisplayExternalTraceEventParser GfxDisplayExternalParser = new IntelGfxDisplayExternalTraceEventParser(source);

                // *********************************************************************
                // Yangra Events
                // *********************************************************************

                // ETL file details
                this.commonHandler.Enqueue(source);

                // All
                // GfxDisplayParser.All += GfxDisplayParserAll;

                // Assert
                GfxDisplayParser.DisplayAssert += GfxDisplayParserDisplayAssert;

                // Diagnostics
                if (this.config.Diag)
                {
                    GfxDisplayParser.DisplayDiagnostics += GfxDisplayParserDisplayDiagnostics;
                    GfxDisplayParser.DisplayDiagnosticsMayDay += GfxDisplayParserDisplayDiagnostics;
                    GfxDisplayParser.DisplayDiagnosticsError += GfxDisplayParserDisplayDiagnostics;
                    GfxDisplayParser.DisplayDiagnosticsWarning += GfxDisplayParserDisplayDiagnostics;
                    GfxDisplayParser.DisplayDiagnosticsInfo += GfxDisplayParserDisplayDiagnostics;
                }

                // VBI
                if (this.config.Vbi)
                {
                    GfxDisplayParser.VBlankInterruptPipeA += GfxDisplayParserVBlankInterruptPipe;
                    GfxDisplayParser.VBlankInterruptPipeB += GfxDisplayParserVBlankInterruptPipe;
                    GfxDisplayParser.VBlankInterruptPipeC += GfxDisplayParserVBlankInterruptPipe;
                    GfxDisplayParser.VBlankInterruptPipeD += GfxDisplayParserVBlankInterruptPipe;
                }

                // Debug Print
                if (this.config.DbgMsg)
                {
                    GfxDisplayParser.DebugPrint += GfxDisplayParserDebugPrint;
                }

                // Function Track
                if (this.config.Function)
                {
                    GfxDisplayParser.FunctionTrack += GfxDisplayParserFunctionTrack;
                }

                // Flip
                if (this.config.Flip)
                {
                    GfxParser.Mpo3FlipStart += GfxDisplayParserMpo3FlipStartLegacy;
                    GfxParser.Mpo3FlipStop += GfxDisplayParserMpo3FlipStopLegacy;
                    GfxParser.Mpo3FlipPlane += GfxDisplayParserMpo3FlipPlaneLegacy;

                    GfxDisplayParser.Mpo3FlipStart += GfxDisplayParserMpo3FlipStart;
                    GfxDisplayParser.Mpo3FlipStop += GfxDisplayParserMpo3FlipStop;
                    GfxDisplayParser.Mpo3FlipPlane += GfxDisplayParserMpo3FlipPlane;
                    GfxDisplayParser.Mpo3FlipInfo += GfxDisplayParserMpo3FlipInfo;

                    GfxDisplayParser.FlipAllParam += GfxDisplayParserFlipAllParam;
                    GfxDisplayParser.FlipSync += GfxDisplayParserFlipSync;
                    GfxDisplayParser.FlipAsync += GfxDisplayParserFlipAsync;

                    GfxDisplayParser.NotifyVSync += GfxDisplayParserNotifyVSync;
                    GfxDisplayParser.NotifyVSyncPlane += GfxDisplayParserNotifyVSyncPlane;
                }

                // MMIO
                if (this.config.Mmio)
                {
                    GfxParser.MMIORead_Dword += GfxParserMmioReadDword;
                    GfxParser.MMIOWrite_Dword += GfxParserMmioWriteDword;
                    GfxParser.MMIOWrite += GfxParserMmioWrite;
                }

                //OsModeTarget
                GfxDisplayParser.TranslatedOsModeTarget += GfxParserTranslatedOsModeTarget;

                // DPCD
                GfxDisplayParser.AuxDPCDRead += GfxDisplayParserAuxDPCDRead;
                GfxDisplayParser.AuxDPCDWrite += GfxDisplayParserAuxDPCDWrite;
                GfxDisplayParser.I2CAuxRead += GfxDisplayParserI2CAuxRead;
                GfxDisplayParser.I2CAuxWrite += GfxDisplayParserI2CAuxWrite;

                // DPCD Display External Events
                GfxDisplayExternalParser.AuxRead += GfxDisplayExternalParserAuxRead;
                GfxDisplayExternalParser.AuxWrite += GfxDisplayExternalParserAuxWrite;
                GfxDisplayExternalParser.I2CAuxRead += GfxDisplayExternalParserI2CAuxRead;
                GfxDisplayExternalParser.I2CAuxWrite += GfxDisplayExternalParserI2CAuxWrite;

                // I2C
                GfxDisplayParser.I2CRead += GfxDisplayParserI2CRead;
                GfxDisplayParser.I2CWrite += GfxDisplayParserI2CWrite;

                // I2C Display External Events
                GfxDisplayExternalParser.I2CRead += GfxDisplayExternalParserI2CRead;
                GfxDisplayExternalParser.I2CWrite += GfxDisplayExternalParserI2CWrite;

                // DPST
                GfxDisplayParser.DisplayPcPhaseCoordinatorApplyStart += GfxDisplayParserDpstPhasing;
                GfxDisplayParser.DisplayPcPhaseCoordinatorApplyFinish += GfxDisplayParserDpstPhasing;
                GfxDisplayParser.DisplayPcPhaseCoordinatorProgramStart += GfxDisplayParserDpstPhasing;

                // SFSU
                GfxDisplayParser.SelectiveFetchInfo += GfxDisplayParserSelectiveFetchInfo;
                GfxDisplayParser.DisplayPcPsrPrClient += GfxDisplayParserPsrClientEvent;
                GfxDisplayParser.DisplayPcPsrPrProcess += GfxDisplayParserPcPsrPrProcess;

                // SetTiming
                GfxDisplayParser.SetTiming += GfxDisplayParserSetTiming;
                GfxDisplayParser.SetTimingOsState += GfxDisplayParserSetTimingOsState;

                // System details
                GfxDisplayParser.SystemDetailsTranscoder += GfxDisplayParserSystemDetailsCcd;
                GfxDisplayParser.SystemDetailsInfo += GfxDisplayParserSystemDetailsInfo;

                // VRR
                GfxDisplayParser.VrrEnableDisableStatusDisable += GfxDisplayParserVrrEnableDisableStatusDisable;
                GfxDisplayParser.VrrEnableDisableStatusEnable += GfxDisplayParserVrrEnableDisableStatusEnable;
                GfxDisplayParser.VrrAdaptiveBalance += GfxDisplayParserVrrAdaptiveBalance;
                GfxDisplayParser.VrrAdaptiveBalanceApply += GfxDisplayParserVrrAdaptiveBalanceApply;
                GfxDisplayParser.VrrAdaptiveBalanceHwCounterMismatch += GfxDisplayParserVrrAdaptiveBalanceHwCounterMismatch;
                GfxDisplayParser.VrrEnableDisableStatusInfo += GfxDisplayParserVrrEnableDisableStatusInfo;


                //DC_STATE
                GfxDisplayParser.DCStateInfo += GfxDisplayParserDcStateInfo;

                //PPS
                GfxDisplayParser.PanelPowerSeq += GfxDisplayParserPpsInfo;

                //SetTimingColor
                GfxDisplayParser.SetTimingColor += GfxDisplayParserSetTimingColor;

                //DisplayBrightness3
                GfxDisplayParser.DisplayBrightness3Write += GfxDisplayParserDisplayBrightness3Write;
                GfxParser.Brightness3Write += GfxDisplayParserDisplayBrightness3Write;

                //SetAdjustedColorimetry
                GfxDisplayParser.ColorSetAdjustedColorimetryColor += GfxDisplayParserSetAdjustedColorimetryInfo;

                //HDRDisplayCaps
                GfxDisplayParser.DisplayCapsColor += GfxDisplayParserHDRDisplayCaps;

                //OsGiven1dLut
                GfxParser.OsOneDLUTData += GfxParserOSGivenOneDLUT;

                //OsGiven1dLutParams
                GfxParser.OsOneDLUTParams += GfxParserOSOneDLUTParam;

                //OsGivenCSC
                GfxDisplayParser.CSCDataColor += GfxDisplayParserOSGivenCSC;

                //DSBInitialize
                GfxDisplayParser.DisplayStateBufferInitialize += GfxDisplayParserDSBInitialize;

                //HDRMetadataColor
                GfxDisplayParser.HDRMetadataColor += GfxDisplayParserHDRMetadataColor;
                GfxDisplayParser.HDRMetadataPlane += GfxDisplayParserHDRMetadataColor;

                //DFTFlipAddress
                GfxDisplayParser.FlipSync += GfxDisplayParserDFTFlipAddress;

                //DFTFlipAddress
                GfxDisplayParser.FlipAsync += GfxDisplayParserDFTFlipAsyncAddress;

                //FeatureStatus
                GfxDisplayParser.FeatureStatus += GfxDisplayParserFeatureStatus;

                //SPI
                GfxDisplayParser.HotPlugDetectSPI += GfxDisplayParserSpiEvent;

                //CancelFlip
                GfxDisplayParser.CancelFlip += GfxDisplayParserCancelFlip;

                GfxDisplayParser.DisplayBrightness3Process += GfxDisplayParserBlcDdi3OptimizationInfo;
                GfxParser.Brightness3Optimize += GfxDisplayParserBlcDdi3OptimizationInfo;

                //PwrConsD0D3StateChange
                GfxDisplayParser.DisplayPcUtilInfo += GfxDisplayPwrConsD0D3StateChange;

                //TargetMode
                GfxDisplayParser.TargetMode += GfxDisplayParserTargetMode;

                //DisplayCaps
                GfxDisplayParser.DisplayCapsRxCaps += GfxDisplayParserDpRxCaps;

                //SetInterruptTargetPresentId
                GfxDisplayParser.SetInterruptTargetPresentId += GfxDisplayParserSetInterruptTargetPresentId;

                //NotifyVsyncLogBufferExtension
                GfxDisplayParser.NotifyVsyncLogBufferExtension += GfxDisplayParserNotifyVsyncLogBufferExtension;

                //NotifyVsyncLogBufferPlane
                GfxDisplayParser.NotifyVsyncLogBufferPlane += GfxDisplayParserNotifyVsyncLogBufferPlane;

                //RRSwitching
                GfxDisplayParser.RrSwitchCapsFixedRxCaps += GfxDisplayParsersRrSwitchCapsFixedInfo;

                //HWFlipQMode
                GfxDisplayParser.FlipQMode += GfxDisplayParserHWFlipQMode;

                //RrSwitch - Info
                GfxDisplayParser.RrSwitch += GfxDisplayParserRrSwitchInfo;

                //RrSwitch - Program
                GfxDisplayParser.RrSwitchProgram += GfxDisplayParserRrSwitchProgram;

                //FmsStatus
                GfxDisplayParser.FmsStatusInfo += GfxDisplayParserFmsStatusInfo;

                //ProcessConfigTable
                GfxDisplayParser.ProcessConfigTableEntry += GfxDisplayParserProcessConfigTable;

                //FlipProcessDetails
                GfxDisplayParser.FlipProcessDetailsInfo += GfxDisplayParserFlipProcessDetails;

                //HwPlaneToLayerIndex
                GfxDisplayParser.HwPlaneToLayerIndex += GfxDisplayParserHwPlaneToLayerIndex;

                //FeatureControl
                GfxDisplayParser.FeatureControl += GfxDisplayParserFeatureControl;

                //DFTFlipAllParam
                GfxDisplayParser.FlipAllParam += GfxDisplayParserDFTFlipAllParam;

                //ScanlineInterrupt
                GfxDisplayParser.ScanlineInterrupt += GfxDisplayParserScanlineInterrupt;

                //Scaler
                GfxDisplayParser.Scaler += GfxDisplayParserScaler;
                GfxDisplayParser.ScalerPlane += GfxDisplayParserScalerPlane;

                // *********************************************************************
                // Legacy Events
                // *********************************************************************

                // All
                // GfxParser.All += GfxDisplayParserAll;
                GfxParser.DxgkDdiStartDeviceStop += GfxParserDxgkDdiStartDeviceStop;
                GfxParser.DxgkDdiSetTimingsFromVidPnStart += GfxParserDxgkDdiSetTimingsFromVidPnStart;
                GfxParser.DxgkDdiSetTimingsFromVidPnStop += GfxParserDxgkDdiSetTimingsFromVidPnStop;
                GfxParser.DxgkDdiControlInterrupt += GfxParserDxgkDdiControlInterrupt1;
                GfxParser.DxgkDdiControlInterrupt2 += GfxParserDxgkDdiControlInterrupt2;
                GfxParser.DxgkDdiControlInterrupt3 += GfxParserDxgkDdiControlInterrupt3;
                GfxParser.DSB += GfxParserDSB;
                GfxDisplayParser.SendInfoFrame += GfxDisplayParserSendInfoFrame;

                // DDI Tracking
                GfxParser.DdiProfilerStart += GfxParserDdiProfilerStart;
                GfxParser.DdiProfilerStop += GfxParserDdiProfilerStop;

                // DP LinkTraining
                GfxParser.DP_LinkTrainingStart += GfxParserDpLinkTrainingStart;
                GfxParser.DP_LinkTrainingStop += GfxParserDpLinkTrainingStop;
                GfxParser.DP_LinkTrainingFastLinkTraining += GfxParserDpFastLinkTraining;

                // DMRRS
                GfxParser.GfxCheckPresentDurationSupport += GfxParserGfxCheckPresentDurationSupport;
                GfxParser.GfxCheckPresentDurationSupportStop += GfxParserGfxCheckPresentDurationSupportStop;

                //DisplayDetect
                GfxParser.DxgkDdiQueryConnectionChange += GfxParser_DxgkDdiQueryConnectionChange;
                GfxDisplayParser.HotPlugDetectLiveState += GfxDisplayParserHotPlugDetectLiveState;

                //cursor
                GfxParser.DxgkDdiSetPointerPosition += GfxParser_DxgkDdiSetPointerPosition;
                GfxParser.DxgkDdiSetPointerShapeStart += GfxParser_DxgkDdiSetPointerShapeStart;


                // Iterate over the file, calling the callbacks.
                source.Process();

                // After processing all the events, dump the handler output in respective json files
                if (this.config.DbgMsg) this.dbgMsgHandler.DumpJson();
                if (this.config.Vbi) this.vbiHandler.DumpJson();
                if (this.config.Flip) this.flipHandler.DumpJson();
                if (this.config.Diag) this.displayDiagnosticsHandler.DumpJson();
                if (this.config.Mmio) this.mmioHandler.DumpJson();
                if (this.config.Dpcd) this.dpcdHandler.DumpJson();
                if (this.config.Function) this.functionHandler.DumpJson();
                if (this.config.CommonEvents) this.commonHandler.DumpJson();
                if (this.config.Interrupt) this.interruptHandler.DumpJson();
                if (this.config.Dpst) this.dpstHandler.DumpJson();
                if (this.config.I2c) this.i2cHandler.DumpJson();
                if (this.config.Psr) this.psrHandler.DumpJson();
                if (this.config.Detection) this.displayDetectHandler.DumpJson();
            }
        }

        // *********************************************************************
        // Yangra Event Callbacks
        // *********************************************************************

        void GfxDisplayParserAll(TraceEvent data)
        {

        }

        void GfxDisplayParserDisplayAssert(Assert_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        void GfxDisplayParserDebugPrint(DebugPrint_t data)
        {
            this.dbgMsgHandler.Enqueue(data);
        }
        void GfxDisplayParserFunctionTrack(FunctionTrack_t data)
        {
            this.functionHandler.Enqueue(data);
        }
        void GfxDisplayParserDisplayDiagnostics(DiagnosticData_t data)
        {
            displayDiagnosticsHandler.DiagnosticDataProcessor(data);
        }
        void GfxDisplayParserVBlankInterruptPipe(PipeVBI_t data)
        {
            this.vbiHandler.Enqueue(data);
        }

        void GfxDisplayParserMpo3FlipStart(Mpo3FlipIn_t data)
        {
            this.flipHandler.StartFlip(data);
        }
        void GfxDisplayParserMpo3FlipStartLegacy(t_Mpo3FlipIn data)
        {
            this.flipHandler.StartFlip(data);
        }
        void GfxDisplayParserMpo3FlipStop(Mpo3FlipOut_t data)
        {
            this.flipHandler.StopFlip(data);
        }
        void GfxDisplayParserMpo3FlipStopLegacy(t_Mpo3FlipOut data)
        {
            this.flipHandler.StopFlip(data);
        }
        void GfxDisplayParserMpo3FlipPlane(Mpo3FlipPlaneIn_t data)
        {
            this.flipHandler.AddPlaneInfo(data);
        }
        void GfxDisplayParserMpo3FlipPlaneLegacy(t_Mpo3FlipPlaneIn data)
        {
            this.flipHandler.AddPlaneInfo(data);
        }
        private void GfxDisplayParserMpo3FlipInfo(Mpo3FlipPlaneDetails_t data)
        {
            this.flipHandler.AddPlaneDetails(data);
        }

        void GfxDisplayParserFlipAllParam(FlipAllParam_t data)
        {
            this.flipHandler.AddFlipDetails(data);
        }
        void GfxDisplayParserFlipSync(FlipAddress_t data)
        {
            this.flipHandler.AddFlipDetails(data, false);
        }
        void GfxDisplayParserFlipAsync(FlipAddress_t data)
        {
            this.flipHandler.AddFlipDetails(data, true);
        }
        void GfxDisplayParserNotifyVSync(NotifyVSyncMpo2_Info_t data)
        {
            this.flipHandler.AddNotifyVSyncInfo(data);
        }
        void GfxDisplayParserNotifyVSyncPlane(NotifyVSyncMpo2_Layer_t data)
        {
            this.flipHandler.AddNotifyVSyncLayer(data);
        }
        private void GfxParserMmioReadDword(t_MMIO_ReadWrite data)
        {
            this.mmioHandler.Enqueue(data, false);
            this.flipHandler.AddMmioData(data, false);
        }
        private void GfxParserMmioWriteDword(t_MMIO_ReadWrite data)
        {
            this.mmioHandler.Enqueue(data, true);
            this.flipHandler.AddMmioData(data, true);
        }
        private void GfxParserMmioWrite(t_MMIOAccessData data)
        {

            this.mmioHandler.Enqueue(data, true);
            this.flipHandler.AddMmioWriteData(data);
        }
        private void GfxDisplayParserI2CWrite(GFX_DISPLAY_DRIVER.I2C_t data)
        {
            this.i2cHandler.Enqueue(data, true);
        }

        private void GfxDisplayExternalParserI2CWrite(GFX_DISPLAY_EXTERNAL.I2C_t data)
        {
            this.i2cHandler.Enqueue(data, true);
        }

        private void GfxDisplayParserI2CRead(GFX_DISPLAY_DRIVER.I2C_t data)
        {
            this.i2cHandler.Enqueue(data, false);
        }

        private void GfxDisplayExternalParserI2CRead(GFX_DISPLAY_EXTERNAL.I2C_t data)
        {
            this.i2cHandler.Enqueue(data, false);
        }

        private void GfxDisplayParserI2CAuxWrite(GFX_DISPLAY_DRIVER.Aux_t data)
        {
            this.dpcdHandler.Enqueue(data, true);
        }

        private void GfxDisplayExternalParserI2CAuxWrite(GFX_DISPLAY_EXTERNAL.Aux_t data)
        {
            this.dpcdHandler.Enqueue(data, true);
        }

        private void GfxDisplayParserI2CAuxRead(GFX_DISPLAY_DRIVER.Aux_t data)
        {
            this.dpcdHandler.Enqueue(data, false);
        }

        private void GfxDisplayExternalParserI2CAuxRead(GFX_DISPLAY_EXTERNAL.Aux_t data)
        {
            this.dpcdHandler.Enqueue(data, false);
        }

        private void GfxDisplayParserAuxDPCDWrite(GFX_DISPLAY_DRIVER.Aux_t data)
        {
            this.dpcdHandler.Enqueue(data, true);
        }

        private void GfxDisplayExternalParserAuxWrite(GFX_DISPLAY_EXTERNAL.Aux_t data)
        {
            this.dpcdHandler.Enqueue(data, true);
        }

        private void GfxDisplayParserAuxDPCDRead(GFX_DISPLAY_DRIVER.Aux_t data)
        {
            this.dpcdHandler.Enqueue(data, false);
        }

        private void GfxDisplayExternalParserAuxRead(GFX_DISPLAY_EXTERNAL.Aux_t data)
        {
            this.dpcdHandler.Enqueue(data, false);
        }

        private void GfxDisplayParserSetTiming(ProtocolSetTimingData_t data)
        {
            this.commonHandler.Enqueue(data);
        }
        private void GfxDisplayParserSetTimingOsState(OsSetTiming_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayParserSystemDetailsCcd(CcdSetTimingData_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayParserSystemDetailsInfo(SystemInfo_t data)
        {
            //this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayParserVrrEnableDisableStatusEnable(VrrEnableParams_t data)
        {
            this.commonHandler.Enqueue(data);
        }
        private void GfxDisplayParserVrrEnableDisableStatusDisable(VrrDisableParams_t data)
        {
            this.commonHandler.Enqueue(data);
        }
        private void GfxDisplayParserVrrEnableDisableStatusInfo(VrrStatusParams_t data)
        {
            this.commonHandler.Enqueue(data);
        }
        private void GfxDisplayParserVrrAdaptiveBalance(VrrAdaptiveBalanceBalance_t data)
        {
            this.commonHandler.Enqueue(data);
        }
        private void GfxDisplayParserVrrAdaptiveBalanceApply(VrrAdaptiveBalanceApply_t data)
        {
            this.commonHandler.Enqueue(data);
        }
        private void GfxDisplayParserVrrAdaptiveBalanceHwCounterMismatch(VrrAdaptiveBalanceHwCounterMismatch_t data)
        {
            this.commonHandler.Enqueue(data);
        }


        private void GfxDisplayParserSelectiveFetchInfo(SelectiveFetchInfo_t data)
        {
            this.commonHandler.Enqueue(data);
        }
        private void GfxDisplayParserDcStateInfo(DCStateRequest_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayParserPpsInfo(Pps_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayParserDpstPhasing(PhaseCoordinatorContextData_t data)
        {
            this.dpstHandler.Enqueue(data);
        }

        private void GfxDisplayParserDpstPhasing(PhaseCoordinatorProgramAdjustData_t data)
        {
            this.dpstHandler.Enqueue(data);
        }

        private void GfxDisplayParserSetTimingColor(ColorPixelDescPipe_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayParserSetAdjustedColorimetryInfo(SetAdjustedColorimetry_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayParserHDRDisplayCaps(HDRCaps_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayParserDisplayBrightness3Write(BlcDdi3Set_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayParserDisplayBrightness3Write(t_BlcDdi3Set data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxParserOSGivenOneDLUT(t_OsGiven1dLut data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxParserOSOneDLUTParam(t_OsOneDLUT_Param data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayParserOSGivenCSC(OSGivenCSC_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayParserDSBInitialize(Dsb_Prepare_t data)
        {
            this.commonHandler.Enqueue(data);
            this.mmioHandler.ParseAndQueueDsbMmioData(data, this.flipHandler);
        }

        private void GfxDisplayParserHDRMetadataColor(HdrStaticMetadata_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayParserDFTFlipAddress(FlipAddress_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayParserDFTFlipAsyncAddress(FlipAddress_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxParserDxgkDdiStartDeviceStop(t_DxgkDdiStartDeviceExit data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayParserPsrClientEvent(PsrPrClientEvent_t data)
        {
            this.psrHandler.Enqueue(data);
        }

        private void GfxDisplayParserPcPsrPrProcess(PsrPrEvents_t data)
        {
            this.psrHandler.Enqueue(data);
        }

        private void GfxDisplayParserSendInfoFrame(AVI_InfoFrameData data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxParserTranslatedOsModeTarget(OsTargetMode_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayParserFeatureStatus(FeatureStatus_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayParserSpiEvent(SPI_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayParserCancelFlip(CancelFlip_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayParserBlcDdi3OptimizationInfo(BlcDdi3Optimization_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayParserBlcDdi3OptimizationInfo(t_BlcDdi3Optimization data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayPwrConsD0D3StateChange(DisplayPwrConsD0D3StateChangeData_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayParserTargetMode(Target_Mode_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayParserDpRxCaps(DPRxCaps_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxDisplayParserSetInterruptTargetPresentId(SetInterruptTargetPresentId_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        void GfxDisplayParserNotifyVsyncLogBufferExtension(NotifyVsyncLogBuffer_Plane_Ext_t data)
        {
            this.commonHandler.Enqueue(data);
        }
        void GfxDisplayParserNotifyVsyncLogBufferPlane(NotifyVsyncLogBuffer_Plane_t data)
        {
            this.commonHandler.Enqueue(data);
        }
        void GfxDisplayParserHWFlipQMode(FlipQMode_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        void GfxDisplayParserRrSwitchInfo(RrSwitchState_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        void GfxDisplayParserRrSwitchProgram(RrSwitchProgram_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        void GfxDisplayParserFmsStatusInfo(FmsModesetStatus_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        void GfxDisplayParserProcessConfigTable(ProcessConfigTableEntry_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        void GfxDisplayParserFlipProcessDetails(FlipProcessDetails_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        void GfxDisplayParserHwPlaneToLayerIndex(LayerToPlaneMap_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        void GfxDisplayParserFeatureControl(FeatureControl_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        void GfxDisplayParserDFTFlipAllParam(FlipAllParam_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        void GfxDisplayParserScanlineInterrupt(Pipe_t data)
        {
            this.interruptHandler.Enqueue(data);
        }

        void GfxParser_DxgkDdiSetPointerPosition(t_DdiSetPointerPosition data)
        {
            this.commonHandler.Enqueue(data);
        }

        void GfxParser_DxgkDdiSetPointerShapeStart(t_DxgkDdiSetPointerShapeEntry data)
        {
            this.commonHandler.Enqueue(data);
        }

        void GfxDisplayParserScaler(ScalerForFlip_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        void GfxDisplayParserScalerPlane(ScalerEnableDisable_t data)
        {
            this.commonHandler.Enqueue(data);
        }
        // *********************************************************************
        // Legacy Events Callbacks
        // *********************************************************************

        private double linkTrainingTime = 0;
        private double modeSetStartTime = 0;

        // DxgkDdiSetTimingsFromVidPn
        private void GfxParserDxgkDdiSetTimingsFromVidPnStart(t_DxgkDdiSetTimingsFromVidPn_Entry data)
        {
            this.modeSetStartTime = data.TimeStampRelativeMSec;
        }

        private void GfxParserDxgkDdiSetTimingsFromVidPnStop(EmptyTraceData data)
        {
            string msg = "GfxParserDxgkDdiSetTimingsFromVidPn:";
            if (this.modeSetStartTime != 0)
            {
                msg += "StartTime=" + this.modeSetStartTime + ",EndTime=" + data.TimeStampRelativeMSec + ",ModeSetTime=" + (data.TimeStampRelativeMSec - this.modeSetStartTime);
            }
            else
            {
                msg += "EndTime=" + data.TimeStampRelativeMSec;
            }
            this.commonHandler.Enqueue(msg);
            this.modeSetStartTime = 0;
        }

        private void GfxParserDxgkDdiControlInterrupt1(t_DxgkDdiControlInterruptEntry data)
        {
            this.interruptHandler.Enqueue(data);
        }
        private void GfxParserDxgkDdiControlInterrupt2(t_DxgkDdiControlInterrupt2Entry data)
        {
            this.interruptHandler.Enqueue(data);
        }

        private void GfxParserDxgkDdiControlInterrupt3(t_DxgkDdiControlInterrupt3Info data)
        {
            this.interruptHandler.Enqueue(data);
        }

        private void GfxParserDSB(t_DSBInfo data)
        {
            this.commonHandler.Enqueue(data);
            this.mmioHandler.ParseAndQueueDsbMmioData(data, this.flipHandler);
        }
        private void GfxDisplayParsersRrSwitchCapsFixedInfo(RrSwitchCapsFixed_t data)
        {
            this.commonHandler.Enqueue(data);
        }

        // DDI Tracking
        private void GfxParserDdiProfilerStart(t_DdiProfiler_Start data)
        {
            this.displayDiagnosticsHandler.ddiHandler.DdiEntry(data.ThreadID, (DD_DIAG_SOURCE_DDI)data.DdiName, data.TimeStampRelativeMSec, data.IRQL);
        }

        private void GfxParserDdiProfilerStop(t_DdiProfiler_Stop data)
        {
            this.displayDiagnosticsHandler.ddiHandler.DdiExit(data.ThreadID, (DD_DIAG_SOURCE_DDI)data.DdiName, data.TimeStampRelativeMSec, data.Status);
        }

        // DP Link Training
        private void GfxParserDpFastLinkTraining(t_DP_LinkTraining_FastLinkTraining data)
        {
            this.commonHandler.Enqueue(data);
        }
        private void GfxParserDpLinkTrainingStart(t_DP_LinkTraining_Start data)
        {
            this.linkTrainingTime = data.TimeStampRelativeMSec;
        }
        private void GfxParserDpLinkTrainingStop(t_DP_LinkTraining_Stop data)
        {
            if (this.linkTrainingTime != 0)
            {
                this.linkTrainingTime = data.TimeStampRelativeMSec - this.linkTrainingTime;
            }
            this.commonHandler.Enqueue(data, this.linkTrainingTime);
            this.linkTrainingTime = 0;
        }

        private void GfxParserGfxCheckPresentDurationSupport(t_GfxCheckPresentDurationSupportInfo data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxParserGfxCheckPresentDurationSupportStop(t_CheckPresentDurationSupportExit data)
        {
            this.commonHandler.Enqueue(data);
        }

        private void GfxParser_DxgkDdiQueryConnectionChange(t_QueryConnectionChange data)
        {
            this.displayDetectHandler.Enqueue(data);
        }

        private void GfxDisplayParserHotPlugDetectLiveState(HPDLiveState_t data)
        {
            this.displayDetectHandler.Enqueue(data);
        }

    }
}