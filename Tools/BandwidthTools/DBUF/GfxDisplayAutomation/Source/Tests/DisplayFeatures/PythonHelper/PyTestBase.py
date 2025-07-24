import sys, traceback
import clr
import time
import string
import os
import shutil as FileUtil
import glob
import platform
from System.IO import Directory


#Setting Framework Folder as Current Working Directory.
#refPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../Framework")
#sys.path.append(refPath)
parentPath = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
#refPath = os.path.join(parentPath, "PythonHelper")
sys.path.append(parentPath)
#Directory.SetCurrentDirectory(refPath)


clr.AddReference(r"PythonExecute.dll")
from Intel.VPG.Display.Automation import PythonExecute
from Intel.VPG.Display.Automation import *
from ConfigurationProxy import *


class PyTestBase(PythonExecute):
    def __init__(self):       
        proxy = ConfigurationProxy(r"PythonExecute.dll.config")
        proxy.InjectToConfigurationManager()
        self.Init("SB_Config_Basic_Port_Check")
        self.PassCount = 0
        self.FailCount = 0
        self.SkipCount = 0
        self.ErrorCount = 0
        self.TDRPassCount = 0
        self.TDRFailCount = 0
   
        
    def TearDown(self):
        self.DeInit()

    def GeneratePaveXML(self, TestName):
        root = ET.Element("ROOT")
        TestResult = ET.SubElement(root, "TestResult")

        ET.SubElement(TestResult, "Description").text = TestName
        Measurements = ET.SubElement(TestResult, "Measurements")
        ET.SubElement(Measurements, "Measurement", name="PassCount").text = self.PassCount.ToString()
        ET.SubElement(Measurements, "Measurement", name="FailCount").text = self.FailCount.ToString()
        ET.SubElement(Measurements, "Measurement", name="SkipCount").text = self.SkipCount.ToString()
        ET.SubElement(Measurements, "Measurement", name="ErrorCount").text = self.ErrorCount.ToString()
        ET.SubElement(Measurements, "Measurement", name="TDRPassCount").text = self.TDRPassCount.ToString()
        ET.SubElement(Measurements, "Measurement", name="TDRFailCount").text = self.TDRFailCount.ToString()
        ET.SubElement(TestResult, "FilePathList")
        if self.FailCount == 0:
            ET.SubElement(TestResult, "FinalResult").text = "P"
        else:
            ET.SubElement(TestResult, "FinalResult").text = "F"
        tree = ET.ElementTree(root)
        tree.write("../PAVEResult.XML")
    def MoveLogFiles(self):
        FileUtil.copy("./DisplayTestLogParser.exe", "../")
        for file in glob.glob("./*.html"):
            FileUtil.copy(file, "../")
        for file in glob.glob("./*.xml"):
            FileUtil.copy(file, "../")
        for file in glob.glob("./*.log"):
            FileUtil.copy(file, "../")

'''
Unit test method to ensure PyTestBase is sane
'''
def selfCheck():
    obj = PyTestBase()
    time.sleep(5)
    
    regValue = clr.Reference[int]()
    obj.GetRegisterValue(0x70180, regValue)
    
    status = obj.VerifyRegisters("EDP_ENABLED", "EDP");

    offset = clr.Reference[int]();
    bitmap = clr.Reference[int]();
    expectedValue= clr.Reference[int]();
    obj.GetEventRegisterInfo("PIPE_SELECT", "EDP", "none", offset, bitmap, expectedValue); 


    obj.SetConfig("SD", "EDP", "none", "none")

    configType = clr.Reference[str]()
    pri = clr.Reference[str]()
    sec = clr.Reference[str]()
    ter = clr.Reference[str]()
    obj.GetConfig(configType, pri, sec, ter)

    print("ConfigType: ", configType.Value) 
    print("pri: ", pri.Value)
    print("sec: ", sec.Value)
    print("ter: ", ter.Value)

    obj.SetMode("EDP", 1024, 768, 60, 0, 32, "Center_Image")

    x = clr.Reference[int]()
    y = clr.Reference[int]()
    rr = clr.Reference[int]()
    angle = clr.Reference[int]()
    bpp = clr.Reference[int]()
    scaling = clr.Reference[str]()
    obj.GetMode("EDP", x, y, rr, angle, bpp, scaling)

    print("x: ", x.Value) 
    print("y: ", y.Value)
    print("rr: ", rr.Value)
    print("angle: ", angle.Value)
    print("bpp: ", bpp.Value)
    print("scaling: ", scaling.Value)

    obj.GoToPowerState("S3", 30)

    r = clr.Reference[int]()
    obj.GetCRC("EDP", True, r)
    print("CRC Value is: ", hex(r.Value)) 

    obj.TearDown();


if __name__ == "__main__":
    selfCheck()

