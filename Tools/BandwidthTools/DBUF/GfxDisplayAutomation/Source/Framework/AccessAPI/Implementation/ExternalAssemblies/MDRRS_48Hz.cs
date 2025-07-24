using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using System.Diagnostics;
using System.Text.RegularExpressions;

namespace Intel.VPG.Display.Automation
{
    public class MDRRS_48Hz : FunctionalBase, IGetMethod
    {
        public uint RR;
        public object GetMethod(object argMessage)
        {
            string currentRR = argMessage as string;
            Log.Message("Current RR = {0}", currentRR);
            bool returnType = false;
            RR = Convert.ToUInt32(Regex.Match(currentRR, @"\d+").Value);
            Log.Message("RR = {0}", RR);
            if (base.MachineInfo.PlatformDetails.Platform == Platform.HSW)
                returnType =  this.GetRRfromRegHSW();
            else if (base.MachineInfo.PlatformDetails.Platform == Platform.CHV)
                returnType = this.GetRRfromRegCHV();
            else if (base.MachineInfo.PlatformDetails.IsGreaterThan(Platform.BDW))
                returnType = this.GetRRfromRegBDWandSKL();
            else
            {
                Log.Fail("Unsupported Platform");
                return false;
            }
            return returnType;
        }

        private uint CompareRegValue(string argRegValue, string argBitmap)
        {
            uint regValue = Convert.ToUInt32(argRegValue, 16);
            uint bitmap = Convert.ToUInt32(argBitmap, 16);

            string regValueBinary = Convert.ToString(regValue, 2);
            while (regValueBinary.Count() < 32)
            {
                regValueBinary = "0" + regValueBinary;
            }

            string bitmapBinary = Convert.ToString(bitmap, 2);
            while (bitmapBinary.Count() < 32)
            {
                bitmapBinary = "0" + bitmapBinary;
            }

            int startIndex = bitmapBinary.IndexOf('1');
            int lastIndex = bitmapBinary.LastIndexOf('1');

            string value = regValueBinary.Substring(startIndex, lastIndex - startIndex + 1);
            return Convert.ToUInt32(value, 2);
            //  return regValue & bitmap;
        }

        private string ReadRegistryDriverEscape(string argOffset)
        {
            DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
            driverData.input = Convert.ToUInt32(argOffset, 16);
            DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
            DriverEscape driverEscapeObj = new DriverEscape();
            bool status = driverEscapeObj.SetMethod(driverParams);
            string hexvalue = driverData.output.ToString("X");
            Log.Message("The {0} :{1}", argOffset, hexvalue);
            return hexvalue;
        }

        private bool GetRRfromRegHSW()
        {
            #region HSWRegisterDelarations
            string PIPE_LINKM1_EDP = "6F040";
            string PIPE_CONF_EDP = "7F008";
            string PIPE_LINKM2_EDP = "6F048";
            #endregion

            bool flagSwitched = false;
            Log.Verbose("Checking for Switch in RR for platform {0}", base.MachineInfo.PlatformDetails.Platform);

            string linkM1EDP =  ReadRegistryDriverEscape(PIPE_LINKM1_EDP);
            Log.Verbose("PIPE_LINKM1_EDP with offset {0} = {1}", PIPE_LINKM1_EDP, linkM1EDP);
            uint bitMapLinkM1EDP = CompareRegValue(linkM1EDP, "FFFFFF");
            Log.Verbose("Bitmap {0} with FFFFFF = {1}", linkM1EDP, bitMapLinkM1EDP);
            for (int i = 0; i < 10; i++)
            {
                Thread.Sleep(5000);
                string hexValue = ReadRegistryDriverEscape(PIPE_CONF_EDP);
                Log.Verbose("PIPE_CONF_EDP with offset {0} = {1}", PIPE_CONF_EDP, hexValue);
                uint bitMapPipeConfReg = CompareRegValue(hexValue, "100000");
                Log.Verbose("Bitmap {0} with 100000 = {1}", hexValue, bitMapPipeConfReg);
                if (bitMapPipeConfReg.ToString().Equals("1"))
                    Log.Verbose("Current RR = {0}", RR);
                else
                {
                    flagSwitched = true;
                    string regLinkM1edp1 = ReadRegistryDriverEscape(PIPE_LINKM1_EDP);
                    Log.Verbose("PIPE_LINKM1_EDP with offset {0} = {1}", PIPE_LINKM1_EDP, regLinkM1edp1);
                    string regLinkM2edp = ReadRegistryDriverEscape(PIPE_LINKM2_EDP);
                    Log.Verbose("PIPE_LINKM2_EDP with offset {0} = {1}",PIPE_LINKM2_EDP, regLinkM2edp);
                    uint bitMapLinkM2edp = CompareRegValue(regLinkM2edp, "FFFFFF");
                    Log.Verbose("Bitmap {0} with FFFFFF = {1}", regLinkM2edp, bitMapLinkM2edp);
                    uint ratio = bitMapLinkM1EDP / RR;
                    Log.Verbose("ratio = {0}", ratio);
                    uint finalRR = bitMapLinkM2edp / ratio;
                    Log.Message("Switched RR {0}", finalRR);
                    if (finalRR == 48)
                        Log.Success("Switched to {0} Hz", finalRR);
                    else
                        Log.Fail("Switched to {0} Hz", finalRR);
                }
            }
            return flagSwitched;
        }

        private bool GetRRfromRegBDWandSKL()
        {
            #region BDWnSKLRegisterDelarations
            string TRANS_LINKM1_EDP = "6F040";
            string TRANS_LINKN1_EDP = "6F044";
            string NV12_PLANE_A_EDP = "70180";
            string NV12_PLANE_B_EDP = "70280";
            string NV12_PLANE_C_EDP = "70380";
            #endregion

            Log.Verbose("Checking for Switch in RR for platform {0}", base.MachineInfo.PlatformDetails.Platform);
            bool flagSwitched = false;
            string regLinkM1edp = ReadRegistryDriverEscape(TRANS_LINKM1_EDP);
            Log.Verbose("TRANS_LINKM1_EDP with offset {0} = {1}", TRANS_LINKM1_EDP, regLinkM1edp);
            string regLinkN1edp = ReadRegistryDriverEscape(TRANS_LINKN1_EDP);
            Log.Verbose("TRANS_LINKN1_EDP with offset {0} = {1}", TRANS_LINKN1_EDP, regLinkN1edp);
            uint bitMapLinkM1edp_1 = CompareRegValue(regLinkM1edp, "FFFFFF");
            Log.Verbose("Bitmap {0} with FFFFFF = {1}", regLinkM1edp, bitMapLinkM1edp_1);
            uint bitMapLinkN1edp_1 = CompareRegValue(regLinkN1edp, "FFFFFF");
            Log.Verbose("Bitmap {0} with FFFFFF = {1}", regLinkN1edp, bitMapLinkN1edp_1);
            for (int i = 0; i < 10; i++)
            {
                Thread.Sleep(5000);
                regLinkM1edp = ReadRegistryDriverEscape(TRANS_LINKM1_EDP);
                Log.Verbose("TRANS_LINKM1_EDP with offset {0} = {1}", TRANS_LINKM1_EDP, regLinkM1edp);
                regLinkN1edp = ReadRegistryDriverEscape(TRANS_LINKN1_EDP);
                Log.Verbose("TRANS_LINKN1_EDP with offset {0} = {1}", TRANS_LINKN1_EDP, regLinkN1edp);
                uint bitMapLinkM1edp_2 = CompareRegValue(regLinkM1edp, "FFFFFF");
                Log.Verbose("Bitmap {0} with FFFFFF = {1}", regLinkM1edp, bitMapLinkM1edp_2);
                uint bitMapLinkN1edp_2 = CompareRegValue(regLinkN1edp, "FFFFFF");
                Log.Verbose("Bitmap {0} with FFFFFF = {1}", regLinkN1edp, bitMapLinkN1edp_2);
                uint ratio = bitMapLinkM1edp_1 / RR;
                Log.Verbose("ratio = {0}", ratio);
                uint finalRR = bitMapLinkM1edp_2 / ratio;
                Log.Verbose("Switched RR = {0}", finalRR);
                flagSwitched = true;
                if (finalRR != RR)
                {
                    flagSwitched = true;
                    if (base.MachineInfo.PlatformDetails.IsGreaterThan(Platform.SKL))
                    {
                        Log.Message(true, "Verify NV12 enabled");
                        uint regReadNV12PlaneA = Convert.ToUInt32(ReadRegistryDriverEscape(NV12_PLANE_A_EDP), 16);
                        uint regReadNV12PlaneB = Convert.ToUInt32(ReadRegistryDriverEscape(NV12_PLANE_B_EDP), 16);
                        uint regReadNV12PlaneC = Convert.ToUInt32(ReadRegistryDriverEscape(NV12_PLANE_C_EDP), 16);
                        uint bitmap = Convert.ToUInt32("8F000000", 16);
                        string valuNV12PlaneA = String.Format("{0:X}", regReadNV12PlaneA & bitmap);
                        string valuNV12PlaneB = String.Format("{0:X}", regReadNV12PlaneB & bitmap);
                        string valuNV12PlaneC = String.Format("{0:X}", regReadNV12PlaneC & bitmap);
                        Log.Verbose("after bitmap = {0}", valuNV12PlaneA);
                        Log.Verbose("after bitmap = {0}", valuNV12PlaneB);
                        Log.Verbose("after bitmap = {0}", valuNV12PlaneC);
                        int count = 0;
                        if (String.Equals(valuNV12PlaneA, "81000000"))
                        {
                            count = count + 1;
                            Log.Success("Plane A in NV12 Color Format");
                        }
                        if (String.Equals(valuNV12PlaneB, "81000000"))
                            count = count + 1;
                        if (String.Equals(valuNV12PlaneC, "81000000"))
                            count = count + 1;
                        if (count > 1)
                            Log.Fail("More than one plane in NV12 color format");
                    }
                }
                Log.Message("Final RR for {0} times is {1}", i, finalRR);
            }
            return flagSwitched;
        }

        private bool GetRRfromRegCHV()
        {
            #region CHVRegisterDelarations
            string DP_C = "1E4200";
            string TransBDPLinkM1 = "1E1040";
            string PIPEBCONF = "1F1008";
            string TransBDPLinkM2 = "1E1048";
            #endregion

            Log.Verbose("Checking for Switch in RR for platform {0}", base.MachineInfo.PlatformDetails.Platform);
            bool flagSwitched = false;

            string regDpC = ReadRegistryDriverEscape(DP_C);
            Log.Verbose("DP_C with offset {0} = {1}", DP_C, regDpC);
            uint bitMapDpC = CompareRegValue(regDpC, "80000000");
            Log.Verbose("Bitmap {0} with 80000000 = {1}", regDpC, bitMapDpC);
            if (bitMapDpC.ToString().Equals("1"))
            {
                uint bitMapcheckPipe = CompareRegValue(regDpC, "300000");
                Log.Verbose("Bitmap {0} with 300000 = {1}", regDpC, bitMapcheckPipe);
                if (bitMapcheckPipe.ToString().Equals("1"))
                {

                    string regLinkM1edpTransB = ReadRegistryDriverEscape(TransBDPLinkM1);
                    Log.Verbose("TransBDPLinkM1 with offset {0} = {1}", TransBDPLinkM1, regLinkM1edpTransB);
                    uint bitMapLinkM1edpTransB = CompareRegValue(regLinkM1edpTransB, "FFFFFF");
                    Log.Verbose("Bitmap {0} with FFFFFF = {1}", regLinkM1edpTransB, bitMapLinkM1edpTransB);
                    for (int i = 0; i < 10; i++)
                    {
                        Thread.Sleep(10000);
                        string regConfPipeB = ReadRegistryDriverEscape(PIPEBCONF);
                        Log.Verbose("PIPEBCONF with offset {0} = {1}", PIPEBCONF, regConfPipeB);
                        uint bitMapConfPipeB = CompareRegValue(regConfPipeB, "4000");
                        Log.Verbose("Bitmap {0} with 4000 ={1}", regConfPipeB, bitMapConfPipeB);
                        if (bitMapConfPipeB.ToString().Equals("0"))
                            Log.Message("Current RR = {0}", RR);
                        else
                        {
                            string regLinkM1edpTransB_1 = ReadRegistryDriverEscape(TransBDPLinkM1);
                            Log.Verbose("TransBDPLinkM1 with offset {0} = {1}", TransBDPLinkM1, regLinkM1edpTransB_1);
                            uint bitMapLinkM1edpTransB_1 = CompareRegValue(regLinkM1edpTransB_1, "FFFFFF");
                            Log.Verbose("Bitmap {0} with FFFFFF = {1}", regLinkM1edpTransB_1, bitMapLinkM1edpTransB_1);
                            string regLinkM2edpTransB_1 = ReadRegistryDriverEscape(TransBDPLinkM2);
                            Log.Verbose("TransBDPLinkM2 with offset {0} = {1}", TransBDPLinkM2, regLinkM2edpTransB_1);
                            uint bitMapLinkM2edpTransB_2 = CompareRegValue(regLinkM2edpTransB_1, "FFFFFF");
                            Log.Verbose("Bitmap {0} with FFFFFF = {1}", regLinkM2edpTransB_1, bitMapLinkM2edpTransB_2);
                            uint ratio = bitMapLinkM1edpTransB_1 / RR;
                            Log.Verbose("ratio = {0}", ratio);
                            uint finalRR = bitMapLinkM2edpTransB_2 / ratio;
                            Log.Verbose("finalRR = {0}", finalRR);
                            Log.Verbose("Switched to {0}", finalRR);
                            flagSwitched = true;
                        }
                    }
                }
                else
                    Log.Message("eDP/DP on Port-C is not attached to Pipe - B");
            }
            else
            {
                Log.Message("eDP/DP on Port-C is not enabled ");
            }

            return flagSwitched;
        }

    }
}


