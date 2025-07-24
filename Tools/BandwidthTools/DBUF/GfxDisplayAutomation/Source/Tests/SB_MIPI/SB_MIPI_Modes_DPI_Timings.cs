namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using IgfxExtBridge_DotNet;
    using System.Diagnostics;

    class SB_MIPI_Modes_DPI_Timings : SB_Modes_ApplyModes_Basic
    {
        const string DPI_HACTIVE = "DPI_HACTIVE";
        const string DPI_VACTIVE = "DPI_VACTIVE";
        const string MIPI_DUAL_LINK_MODE = "MIPI_DUAL_LINK_MODE";
        Process procNaakuthanthi;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public override void TestStep0()
        {
            if (!base.CurrentConfig.CustomDisplayList.Contains(DisplayType.MIPI))
                Log.Abort("This test requires MIPI as an active display.");
        }

        protected override void VerifyTiming(DisplayMode displayMode)
        {
            if (displayMode.display == DisplayType.MIPI)
            {
                List<PORT> availablePorts = new List<PORT> { PORT.PORTA, PORT.PORTC };
                DisplayInfo displayInfo = this.CurrentConfig.EnumeratedDisplays.Find(dispInfo => dispInfo.DisplayType == displayMode.display);

                StartMouseMovement();

                bool isMipiVideoMode = VerifyRegisters("MIPI_VIDEO_MODE", PIPE.NONE, PLANE.NONE, displayInfo.Port, false);

                StopMouseMovement();

                bool isDualLinkEnabled = !VerifyRegisters(MIPI_DUAL_LINK_MODE, PIPE.NONE, PLANE.NONE, displayInfo.Port, false);
                if (isDualLinkEnabled)
                {
                    Log.Message("Data is driven in Dual Link mode");
                }
                else
                {
                    availablePorts.Clear();
                    availablePorts.Add(displayInfo.Port);
                }

                if (isMipiVideoMode)
                {
                    availablePorts.ForEach(eachPort => VerifyDpiTimings(displayMode, eachPort));
                }
                else
                {
                    Log.Fail("This test is not valid for Cmd Mode MIPI Panels.");
                }            
            }
        }

        private void VerifyDpiTimings(DisplayMode displayMode, PORT port)
        {
            bool isPortraitPanel = displayMode.HzRes > displayMode.VtRes ? false : true;

            uint hactive = GetRegisterValue(DPI_HACTIVE, PIPE.NONE, PLANE.NONE, port);

            uint vactive = GetRegisterValue(DPI_VACTIVE, PIPE.NONE, PLANE.NONE, port);
            
            displayMode = GetTargetResolution(displayMode.display);            

            if (isPortraitPanel)
            {
                displayMode.VtRes /= 2;
            }
            else
            {
                displayMode.HzRes /= 2;
            }

            if (displayMode.HzRes == hactive && displayMode.VtRes == vactive)
            {
                Log.Success("Timings Matched. HActive {0}, VActive: {1}", hactive, vactive);
            }
            else
            {
                Log.Fail("Expected HActive {0}, Observed HActive: {1}", displayMode.HzRes, hactive);
                Log.Fail("Expected VActive {0}, Observed VActive: {1}", displayMode.VtRes, vactive);
            }
        }

        public void StartMouseMovement()
        {
            string PSR_UTILITY_APP = "Naakuthanthi.exe";
            string args = "c:draw e:pixelpath w:300 h:300";

            procNaakuthanthi = new Process();
            procNaakuthanthi.StartInfo.UseShellExecute = false;
            procNaakuthanthi.StartInfo.CreateNoWindow = false;
            procNaakuthanthi.StartInfo.FileName = PSR_UTILITY_APP;
            procNaakuthanthi.StartInfo.Arguments = args;

            procNaakuthanthi.Start();
        }

        public void StopMouseMovement()
        {
            if (!procNaakuthanthi.HasExited)
                procNaakuthanthi.Kill();
        }
    }
}
