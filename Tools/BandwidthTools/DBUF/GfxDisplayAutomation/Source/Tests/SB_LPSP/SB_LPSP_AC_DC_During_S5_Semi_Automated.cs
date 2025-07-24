namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Windows.Forms;

    [Test(Type = TestType.HasReboot)]
    class SB_LPSP_AC_DC_During_S5_Semi_Automated : SB_LPSP_AC_DC_During_S3_Semi_Automated 
    {   
        public SB_LPSP_AC_DC_During_S5_Semi_Automated()
        {
            _PowerState = PowerStates.S5;
        }

        [Test(Type = TestType.Method, Order = 1)]
        public override void TestStep1()
        {
            ApplyNativeMode();
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Semi Automated Event");              
            String message = "Switch AC Mode after System go to " + _PowerState;
            PromptMessage(message);
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Power Event {0}", _PowerState);              
            GotoPowerState();
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Check Power State");              
            String abortMessage = "System is Running in DC Mode";
            String successMessage = "System is Running in AC Mode";
            CheckPowerState(PowerLineStatus.Offline, abortMessage, successMessage);
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Verify LPSP Register");              
            LPSPRegisterVerify(true);
        }

        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            Log.Message(true, "Semi Automated Event");              
            String message = "Switch DC Mode after System go to " + _PowerState;
            PromptMessage(message);
        }

        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {                          
            Log.Message(true, "Power Event {0}", _PowerState);                 
            GotoPowerState();
        }

        [Test(Type = TestType.Method, Order = 8)]
        public void TestStep8()
        {
            Log.Message(true, "Check Power State");      
            String abortMessage = "System is Running in AC Mode";
            String successMessage = "System is Running in DC Mode";
            CheckPowerState(PowerLineStatus.Online, abortMessage, successMessage);
        }

        [Test(Type = TestType.Method, Order = 9)]
        public void TestStep9()
        {
            Log.Message(true, "Verify LPSP Register");   
            LPSPRegisterVerify(true);
        }

        [Test(Type = TestType.Method, Order = 10)]
        public void TestStep10()
        {
            ApplyNonNativeMode();
        }

        [Test(Type = TestType.Method, Order = 11)]
        public void TestStep11()
        {
            Log.Message(true, "Semi Automated Event");
            String message = "Switch AC Mode after System go to " + _PowerState;
            PromptMessage(message);
        }

        [Test(Type = TestType.Method, Order = 12)]
        public void TestStep12()
        {
            Log.Message(true, "Power Event {0}", _PowerState);
            GotoPowerState();
        }

        [Test(Type = TestType.Method, Order = 13)]
        public void TestStep13()
        {
            Log.Message(true, "Check Power State");
            String abortMessage = "System is Running in DC Mode";
            String successMessage = "System is Running in AC Mode";
            CheckPowerState(PowerLineStatus.Offline, abortMessage, successMessage);
        }

        [Test(Type = TestType.Method, Order = 14)]
        public void TestStep14()
        {
            Log.Message(true, "Verify LPSP Register");
            LPSPRegisterVerify();
        }

        [Test(Type = TestType.Method, Order = 15)]
        public void TestStep15()
        {
            Log.Message(true, "Semi Automated Event");
            String message = "Switch DC Mode after System go to " + _PowerState;
            PromptMessage(message);
        }

        [Test(Type = TestType.Method, Order = 16)]
        public void TestStep16()
        {
            Log.Message(true, "Power Event {0}", _PowerState);
            GotoPowerState();
        }

        [Test(Type = TestType.Method, Order = 17)]
        public void TestStep17()
        {
            Log.Message(true, "Check Power State");
            String abortMessage = "System is Running in AC Mode";
            String successMessage = "System is Running in DC Mode";
            CheckPowerState(PowerLineStatus.Online, abortMessage, successMessage);
        }

        [Test(Type = TestType.Method, Order = 18)]
        public void TestStep18()
        {
            Log.Message(true, "Verify LPSP Register");
            LPSPRegisterVerify();
        }
    }
}