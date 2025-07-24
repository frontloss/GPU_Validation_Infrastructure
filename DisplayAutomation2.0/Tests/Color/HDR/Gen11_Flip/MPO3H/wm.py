import csv
import logging
import math
import os
import subprocess
import sys

from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env.test_context import TestContext
from Tests.MPO.Flip.GEN11.MPO3H import register_verification


class REGISTER_PIXELFORMAT(object):
    YUV422_8BPC = 0
    YUV420_8BPC = 2
    RGB2101010 = 4
    YUV420_10BPC = 6
    RGB8888 = 8
    YUV420_12BPC = 10
    RGB16_FLOAT = 12
    YUV420_16BPC = 14
    YUV444_8BPC = 16  #####
    RGB16_UINT = 18  #####
    RGB2101010_XRBIAS = 20
    INDEXED_8BIT = 24
    RGB565 = 28
    YUV422_10BPC = 1
    YUV422_12BPC = 3
    YUV422_16BPC = 5
    YUV444_10BPC = 7
    YUV444_12BPC = 9
    YUV444_16BPC = 11


class Watermark(object):
    display_config = None
    current_config = None
    current_mode = [0, 0, 0]
    source_id = [0, 0, 0]
    pixel_clk = [0, 0, 0]
    ipfile = None
    opfile = None

    def setup(self, testname):
        testname = testname.replace('.py', '.csv')
        path = os.path.join(os.getcwd(), 'Logs')
        self.ipfile = path + '\\WM_input' + testname
        # print self.ipfile
        # print os.path.basename(testname)
        with open(self.ipfile, 'a') as csvfile:
            csvfile.truncate()
            csvfile.close()
        self.opfile = path + '\\WM_output' + testname
        with open(self.opfile, 'a') as csvfile:
            csvfile.truncate()
            csvfile.close()

    # Function to read the register detaisl from file and copy it to a dict (regname,offset)
    def readBaseRegistersFile(self):
        path = os.path.join(TestContext.root_folder(), os.path.join('Tests\MPO\Flip\GEN11\MPO3H', 'registers.txt'))
        with open(path, "r") as text:
            return dict(line.strip().split() for line in text)

    def readBitMapsFile(self):
        path = os.path.join(TestContext.root_folder(), os.path.join('Tests\MPO\Flip\GEN11\MPO3H', 'bitmaps.txt'))
        with open(path, "r") as text:
            return dict(line.strip().split() for line in text)

    def getFirstSetBitPos(self, n):
        ret = math.log(n & -n, 2)
        return ret

    def getBitmapValue(self, regValue, bitmap):
        shiftFactor = self.getFirstSetBitPos(int(bitmap, 16))
        value = (regValue & int(bitmap, 16)) >> int(shiftFactor)
        return value

    def regRead(self, offset):
        reg_val = driver_interface.DriverInterface().mmio_read(int(offset, 16), 'gfx_0')
        print(int(offset, 16), reg_val)
        return reg_val

    def compareRegisterValue(self, regValue, expectedValue, bitmap):
        # print "BitMap -->" ,hex(int(bitmap,16))
        shiftFactor = self.getFirstSetBitPos(int(bitmap, 16))
        # print"Shift Factor -->" ,shiftFactor
        value = (regValue & int(bitmap, 16)) >> int(shiftFactor)
        # print "val --> :",value
        if (value == expectedValue):
            return True, value
        else:
            return False, value

    def getHVTotalValue(self, baseRegister, pipeID, bitMaps):
        register = hex(int(baseRegister, 16) + (pipeID * 0x1000))
        regVal = self.regRead(register)
        ddireg = hex(int("0x60400", 16) + (pipeID * 0x1000))
        ddiregVal = self.regRead(ddireg)
        # print " Register : %x Reg va; : %x ",register,regVal
        if (ddiregVal & 0x80000000 == 0):
            register = hex(int(baseRegister, 16) + (pipeID * 0xF000))
            regVal = self.regRead(register)
        val = self.getBitmapValue(regVal, bitMaps)
        return val

    def getLinetimeRegValue(self, baseRegister, pipeID, bitMaps):
        register = hex(int(baseRegister, 16) + (pipeID * 0x4))
        regVal = self.regRead(register)
        # print"Register*************",register
        val = self.getBitmapValue(regVal, bitMaps)
        return val

    def getPlaneRegValue(self, baseRegister, pipeID, planeID, bitMaps):
        register = hex(int(baseRegister, 16) + (pipeID * 0x1000) + (planeID * 0x100))
        regVal = self.regRead(register)
        # print"Register*************",register
        val = self.getBitmapValue(regVal, bitMaps)
        return val

    def getCursorRegValue(self, baseRegister, pipeID, bitMaps):
        register = hex(int(baseRegister, 16) + (pipeID * 0x1000))
        regVal = self.regRead(register)
        # print"Register*************",register
        val = self.getBitmapValue(regVal, bitMaps)
        return val

    def getScalarRegValue(self, baseRegister, pipeID, scalarID, bitMaps):
        register = hex(int(baseRegister, 16) + (scalarID * 0x100) + (pipeID * 0x800))
        regVal = self.regRead(register)
        val = self.getBitmapValue(regVal, bitMaps)
        return val

    def getWMRegValue(self, baseRegister, pipeID, planeID, wmLevel, bitMaps):
        register = hex(int(baseRegister, 16) + (pipeID * 0x1000) + (planeID * 0x100) + (0x4 * wmLevel))
        regVal = self.regRead(register)
        val = self.getBitmapValue(regVal, bitMaps)
        return val

    def getCursorWMRegValue(self, baseRegister, pipeID, wmLevel, bitMaps):
        register = hex(int(baseRegister, 16) + (pipeID * 0x1000) + (0x4 * wmLevel))
        regVal = self.regRead(register)
        val = self.getBitmapValue(regVal, bitMaps)
        return val

    def get_display_info(self):
        self.display_config = DisplayConfiguration()
        self.current_config = self.display_config.get_current_display_configuration()
        noOfDisplays = self.current_config.numberOfDisplays
        for index in range(0, noOfDisplays):
            self.source_id[index] = self.current_config.displayPathInfo[index].sourceId
            self.current_mode[index] = self.display_config.get_current_mode(
                self.current_config.displayPathInfo[index].targetId)
            self.pixel_clk[index] = self.current_mode[index].pixelClock_Hz

        print(self.source_id)
        print(self.current_mode)
        print(self.pixel_clk)

    def getBPPFromPixelFormat(self, pixel_format, planeID):
        bpp = 0
        if (pixel_format in (
                REGISTER_PIXELFORMAT.RGB16_FLOAT, REGISTER_PIXELFORMAT.RGB16_UINT, REGISTER_PIXELFORMAT.YUV444_12BPC,
                REGISTER_PIXELFORMAT.YUV444_16BPC)):
            bpp = 8
        elif (pixel_format == REGISTER_PIXELFORMAT.YUV420_8BPC):
            if (planeID > 4):
                bpp = 1
            else:
                bpp = 2
        elif (pixel_format in (
                REGISTER_PIXELFORMAT.YUV420_10BPC, REGISTER_PIXELFORMAT.YUV420_12BPC,
                REGISTER_PIXELFORMAT.YUV420_16BPC)):
            if (planeID > 4):
                bpp = 2
            else:
                bpp = 4
        elif (pixel_format == REGISTER_PIXELFORMAT.YUV422_8BPC):
            bpp = 2
        else:
            bpp = 4
        return bpp

    def getCursorBPPFromMode(self, mode):
        bpp = 0
        if ((mode == 2) or (mode == 3) or (mode >= 7)):
            bpp = 4
        else:
            bpp = 1
        return bpp

    def getCursorSizeFromMode(self, mode):
        size = 0
        if ((mode == 4) or (mode == 5) or (mode == 6) or (mode == 7) or (mode == 36) or (mode == 39)):
            size = 64
        elif ((mode == 2) or (mode == 34) or (mode == 37)):
            size = 128
        elif ((mode == 3) or (mode == 35) or (mode == 38)):
            size = 256
        return size

    def getScaleFactor(self, pipeID, planeID):
        scalarEnabled = 0
        scalarID = None
        baseRegisters = self.readBaseRegistersFile()
        bitMaps = self.readBitMapsFile()
        baseRegister = baseRegisters['PS_CTL_BASE']
        register1 = hex(int(baseRegister, 16) + (pipeID * 0x800))  # Pipe Scalar 1
        register2 = hex(int(baseRegister, 16) + 0x100 + (pipeID * 0x800))  # Pipe Scalar 2
        regValue1 = self.regRead(register1)
        regValue2 = self.regRead(register2)

        planeWidth = self.getPlaneRegValue(baseRegisters['PLANE_SIZE_BASE'], pipeID, planeID,
                                           bitMaps['PLANE_WIN_SIZE_WIDTH'])
        planeHeight = self.getPlaneRegValue(baseRegisters['PLANE_SIZE_BASE'], pipeID, planeID,
                                            bitMaps['PLANE_WIN_SIZE_HEIGHT'])

        result1, programmedValue1 = self.compareRegisterValue(regValue1, 1, bitMaps['PS_ENABLE'])
        result2, programmedValue2 = self.compareRegisterValue(regValue2, 1, bitMaps['PS_ENABLE'])

        if (result1 is True):  # Scalar1 enabled
            result, programmedValue = self.compareRegisterValue(regValue1, (planeID + 1), bitMaps['PS_BINDING'])
            if (result is True):  # Scalar1 tied to planeID
                scalarID = 0
                scalarEnabled = 1

        elif (result2 is True):  # Scalar2 enabled
            result, programmedValue = self.compareRegisterValue(regValue2, (planeID + 1), bitMaps['PS_BINDING'])
            if (result is True):  # Scalar2 tied to planeID
                scalarID = 1
                scalarEnabled = 1
        else:
            logging.info("No Scalars Enabled")

        if (scalarEnabled == 1):
            scalar_x = self.getScalarRegValue(baseRegisters['PS_WIN_SIZE_BASE'], pipeID, scalarID,
                                              bitMaps['PS_WIN_SIZE_X'])
            scalar_y = self.getScalarRegValue(baseRegisters['PS_WIN_SIZE_BASE'], pipeID, scalarID,
                                              bitMaps['PS_WIN_SIZE_Y'])
            print(planeWidth, planeHeight, scalar_x, scalar_y)
            hScale = planeWidth / float(scalar_x)
            vScale = planeHeight / float(scalar_y)
        else:
            hScale = 1
            vScale = 1
        return hScale, vScale

    def getYPlaneMappingForPlanarFormats(self, pipeID, planeID):
        YPlaneID = 0
        baseRegisters = self.readBaseRegistersFile()
        bitMaps = self.readBitMapsFile()
        pixelFormat = self.getPlaneRegValue(baseRegisters['PLANE_CTL_BASE'], pipeID, planeID,
                                            bitMaps['SOURCE_PIXEL_FORMAT'])
        width = self.getPlaneRegValue(baseRegisters['PLANE_SIZE_BASE'], pipeID, planeID,
                                      bitMaps['PLANE_WIN_SIZE_WIDTH'])

        if (pixelFormat in (REGISTER_PIXELFORMAT.YUV420_8BPC, REGISTER_PIXELFORMAT.YUV420_10BPC,
                            REGISTER_PIXELFORMAT.YUV420_12BPC, REGISTER_PIXELFORMAT.YUV420_16BPC)):
            if (planeID < 3 and width <= 4096):
                baseRegister = baseRegisters['PLANE_CUS_CTL']
                register = hex(int(baseRegister, 16) + (pipeID * 0x1000) + (planeID * 0x100))
                regValue = self.regRead(register)
                result, programmedValue = self.compareRegisterValue(regValue, 1, bitMaps['CUS_ENABLE'])
                if (result is True):
                    result, programmedValue = self.compareRegisterValue(regValue, 1, bitMaps['CUS_YBINDING'])
                    if (programmedValue == 0):
                        YPlaneID = 5
                    elif (programmedValue == 1):
                        YPlaneID = 6
                else:
                    logging.error("CUS not enabled for pixel format : %d Plane- %d",
                                  register_verification.mapSBPixelFormat_RegisterFormat(pixelFormat), planeID + 1)
            elif (planeID >= 3 or width > 4096):
                baseRegister = baseRegisters['PS_CTL_BASE']
                register1 = hex(int(baseRegister, 16) + (pipeID * 0x800))  # Scalar 1
                register2 = hex(int(baseRegister, 16) + 0x100 + (pipeID * 0x800))  # Scalar 2
                regValue1 = self.regRead(register1)
                regValue2 = self.regRead(register2)

                result1, programmedValue1 = self.compareRegisterValue(regValue1, 1, bitMaps['PS_ENABLE'])
                result2, programmedValue2 = self.compareRegisterValue(regValue2, 1, bitMaps['PS_ENABLE'])
                if (result1 is True):  # Scalar1 enabled
                    result, programmedValue = self.compareRegisterValue(regValue1, (planeID + 1), bitMaps['PS_BINDING'])
                    if (result is True):  # Scalar1 tied to planeID
                        scalarID = 0
                        result, programmedValue = self.compareRegisterValue(regValue1, 0, bitMaps['PS_YBINDING'])
                        if (programmedValue is 6):
                            YPlaneID = 5
                        elif (programmedValue is 7):
                            YPlaneID = 6
                elif (result2 is True):  # Scalar2 enabled
                    result, programmedValue = self.compareRegisterValue(regValue2, (planeID + 1), bitMaps['PS_BINDING'])
                    if (result is True):  # Scalar2 tied to planeID
                        scalarID = 1
                        result, programmedValue = self.compareRegisterValue(regValue2, 0, bitMaps['PS_YBINDING'])
                        if (programmedValue is 6):
                            YPlaneID = 5
                        elif (programmedValue is 7):
                            YPlaneID = 6
            else:
                logging.error("No Scalars enabled - CUS also not enabled!!!")

        return YPlaneID

    def verifyMinDBUFRequirement(self, planeID, pipeID):
        baseRegisters = self.readBaseRegistersFile()
        bitMaps = self.readBitMapsFile()
        tiling = self.getPlaneRegValue(baseRegisters['PLANE_CTL_BASE'], pipeID, planeID, bitMaps['TILING'])
        buf_start = self.getPlaneRegValue(baseRegisters['PLANE_BUF_CFG'], pipeID, planeID, bitMaps['DBUF_START'])
        buf_end = self.getPlaneRegValue(baseRegisters['PLANE_BUF_CFG'], pipeID, planeID, bitMaps['DBUF_END'])
        dbuf_plane = buf_end - buf_start + 1  # Plane Buff alloction
        if (tiling >= 4):  # Y Tile
            minScanLines = 8
            planeWidth = self.getPlaneRegValue(baseRegisters['PLANE_SIZE_BASE'], pipeID, planeID,
                                               bitMaps['PLANE_WIN_SIZE_WIDTH'])
            pixel_format = self.getPlaneRegValue(baseRegisters['PLANE_CTL_BASE'], pipeID, planeID,
                                                 bitMaps['SOURCE_PIXEL_FORMAT'])
            bpp = self.getBPPFromPixelFormat(pixel_format, planeID)  # Index 13 - Plane
            # TODO - minscanlines based on rotation
            # PlaneMinAlloc = Ceiling [(4*Plane width*Bpp)/512] * MinScanLines/4 + 3
            min_dbuf = math.ceil((4 * planeWidth * bpp) / 512) * minScanLines / 4 + 3
        else:
            min_dbuf = 8

        if (dbuf_plane < min_dbuf):
            logging.debug("DBUF programmed : %d MinDBUFcalculated : %d", dbuf_plane, min_dbuf)
            logging.error("Pipe : %d Plane  %d MinDBUF requirement not satisfied!!", pipeID, planeID)
        return

    def fill_csvInput(self, pipeID, planeID):
        csv_input = []
        # print"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Start^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
        baseRegisters = self.readBaseRegistersFile()
        bitMaps = self.readBitMapsFile()
        self.get_display_info()
        csv_input.append(self.pixel_clk[pipeID])  # Index 0 - PixelClock
        csv_input.append(0)  # Index 1 - Interlaced. By default set to 0
        csv_input.append(
            self.getHVTotalValue(baseRegisters['TRANS_HTOTAL'], pipeID, bitMaps['HV_TOTAL']) + 1)  # Index 2 - HTotal
        csv_input.append(
            self.getHVTotalValue(baseRegisters['TRANS_VTOTAL'], pipeID, bitMaps['HV_TOTAL']) + 1)  # Index 3 - VTotal
        csv_input.append(1)  # Index 4 - Pipe HScale. By default set to 1
        csv_input.append(1)  # Index 5 - Pipe VScale. By default set to 1
        csv_input.append(0)  # Index 6 - YUV420 Bypass mode. By default set to 0
        csv_input.append(hex(0x23120200))  # Index 7 - Latencies Set 1
        csv_input.append(hex(0xFF646450).rstrip("L"))  # Index 8 - Latencies Set 2
        csv_input.append(20)  # Index 9 - Trans WM by default set to 20
        csv_input.append(self.getPlaneRegValue(baseRegisters['PLANE_CTL_BASE'], pipeID, planeID,
                                               bitMaps['PLANE_ENABLE']))  # Index 10 - PlaneEnable
        buf_start = self.getPlaneRegValue(baseRegisters['PLANE_BUF_CFG'], pipeID, planeID, bitMaps['DBUF_START'])
        buf_end = self.getPlaneRegValue(baseRegisters['PLANE_BUF_CFG'], pipeID, planeID, bitMaps['DBUF_END'])
        csv_input.append(buf_end - buf_start + 1)  # Index 11 - Plane Buff alloction
        tiling = self.getPlaneRegValue(baseRegisters['PLANE_CTL_BASE'], pipeID, planeID, bitMaps['TILING'])
        if (tiling >= 4):  # Index 12 - Tiling formt
            csv_input.append(1)
        elif (tiling == 0):
            csv_input.append(2)
        elif (tiling == 1):
            csv_input.append(0)
        pixel_format = self.getPlaneRegValue(baseRegisters['PLANE_CTL_BASE'], pipeID, planeID,
                                             bitMaps['SOURCE_PIXEL_FORMAT'])
        csv_input.append(self.getBPPFromPixelFormat(pixel_format, planeID))  # Index 13 - Plane
        csv_input.append(0)  # Index 14 - Plane Rotation . By default set to 0
        csv_input.append(self.getPlaneRegValue(baseRegisters['PLANE_SIZE_BASE'], pipeID, planeID,
                                               bitMaps['PLANE_WIN_SIZE_WIDTH']) + 1)  # Index 15 - Plane Horz SIze
        csv_input.append(self.getPlaneRegValue(baseRegisters['PLANE_SIZE_BASE'], pipeID, planeID,
                                               bitMaps['PLANE_WIN_SIZE_HEIGHT']) + 1)  # Index 16 - Plane Vert Size
        HScale, VScale = self.getScaleFactor(pipeID, planeID)
        csv_input.append(HScale)  # Index 17 - Horz Scale
        csv_input.append(VScale)  # Index 18 - Vert Scale
        csv_input.append(0)  # Index 19 - Render Compression . By default set to 0
        with open(self.ipfile, 'a') as csvfile:
            reader = csv.writer(csvfile, delimiter=',')
            reader.writerow((csv_input))

    def fill_csvInput_cursor(self, pipeID):
        csv_input = []
        # print"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Start^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
        baseRegisters = self.readBaseRegistersFile()
        bitMaps = self.readBitMapsFile()
        self.get_display_info()
        csv_input.append(self.pixel_clk[pipeID])  # Index 0 - PixelClock
        csv_input.append(0)  # Index 1 - Interlaced. By default set to 0
        csv_input.append(
            self.getHVTotalValue(baseRegisters['TRANS_HTOTAL'], pipeID, bitMaps['HV_TOTAL']) + 1)  # Index 2 - HTotal
        csv_input.append(
            self.getHVTotalValue(baseRegisters['TRANS_VTOTAL'], pipeID, bitMaps['HV_TOTAL']) + 1)  # Index 3 - VTotal
        csv_input.append(1)  # Index 4 - Pipe HScale. By default set to 1
        csv_input.append(1)  # Index 5 - Pipe VScale. By default set to 1
        csv_input.append(0)  # Index 6 - YUV420 Bypass mode. By default set to 0
        csv_input.append(hex(0x23120200))  # Index 7 - Latencies Set 1
        csv_input.append(hex(0xFF646450).rstrip("L"))  # Index 8 - Latencies Set 2
        csv_input.append(20)  # Index 9 - Trans WM by default set to 20
        cursormode = self.getCursorRegValue(baseRegisters['CURSOR_CTL_BASE'], pipeID, bitMaps['CURSOR_MODE'])
        if (cursormode > 0):  # Index 10 - PlaneEnable
            csv_input.append(1)
        else:
            csv_input.append(0)
        buf_start = self.getCursorRegValue(baseRegisters['CURSOR_BUF_CFG'], pipeID, bitMaps['DBUF_START'])
        buf_end = self.getCursorRegValue(baseRegisters['CURSOR_BUF_CFG'], pipeID, bitMaps['DBUF_END'])
        csv_input.append(buf_end - buf_start + 1)  # Index 11 - Plane Buff alloction
        csv_input.append(0)  # Index 12 - Tiling formt , linear for cursor
        csv_input.append(self.getCursorBPPFromMode(cursormode))  # Index 13 - Plane BPP
        csv_input.append(0)  # Index 14 - Plane Rotation . By default set to 0
        csv_input.append(self.getCursorSizeFromMode(cursormode))  # Index 15 - Plane Horz SIze
        csv_input.append(self.getCursorSizeFromMode(cursormode))  # Index 16 - Plane Vert Size
        csv_input.append(1)  # Index 17 - Horz Scale
        csv_input.append(1)  # Index 18 - Vert Scale
        csv_input.append(0)  # Index 19 - Render Compression . By default set to 0
        with open(self.ipfile, 'a') as csvfile:
            reader = csv.writer(csvfile, delimiter=',')
            reader.writerow((csv_input))

    def RunWMExcel(self):
        xlsfile = os.path.abspath(os.path.join(os.path.dirname(__file__), "MPO3H\Gen11WM.xls"))
        input_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "MPO3H\WM_input.csv"))
        output_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "MPO3H\WM_output.csv"))
        args = "Gen11WMXlsReaderWriter.exe " + xlsfile + " " + input_file + " " + output_file
        subprocess.call(args)

    def fill_csvOutput(self, pipeID, planeID):
        csv_output = []
        baseRegisters = self.readBaseRegistersFile()
        bitMaps = self.readBitMapsFile()

        for wmLevel in range(0, 8):
            if (self.getWMRegValue(baseRegisters['PLANE_WM'], pipeID, planeID, wmLevel, bitMaps['WM_ENABLE']) == 1):
                csv_output.append('True')
            else:
                csv_output.append('False')
            csv_output.append(
                self.getWMRegValue(baseRegisters['PLANE_WM'], pipeID, planeID, wmLevel, bitMaps['WM_IGNORELINES']))
            csv_output.append(
                self.getWMRegValue(baseRegisters['PLANE_WM'], pipeID, planeID, wmLevel, bitMaps['WM_LINES']))
            csv_output.append(
                self.getWMRegValue(baseRegisters['PLANE_WM'], pipeID, planeID, wmLevel, bitMaps['WM_BLOCKS']))
            print("Level :", wmLevel)

        if (self.getPlaneRegValue(baseRegisters['PLANE_TRANS_WM'], pipeID, planeID, bitMaps['WM_ENABLE']) == 1):
            csv_output.append('True')
        else:
            csv_output.append('False')

        csv_output.append(self.getPlaneRegValue(baseRegisters['PLANE_TRANS_WM'], pipeID, planeID, bitMaps['WM_BLOCKS']))
        csv_output.append(self.getLinetimeRegValue(baseRegisters['WM_LINETIME'], pipeID, bitMaps['WM_LINETIME']))

        with open(self.opfile, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow((csv_output))

    def fill_csvOutput_cursor(self, pipeID):
        csv_output = []
        baseRegisters = self.readBaseRegistersFile()
        bitMaps = self.readBitMapsFile()

        for wmLevel in range(0, 8):
            if (self.getCursorWMRegValue(baseRegisters['CUR_WM'], pipeID, wmLevel, bitMaps['WM_ENABLE']) == 1):
                csv_output.append('True')
            else:
                csv_output.append('False')
            csv_output.append(
                self.getCursorWMRegValue(baseRegisters['CUR_WM'], pipeID, wmLevel, bitMaps['WM_IGNORELINES']))
            csv_output.append(self.getCursorWMRegValue(baseRegisters['CUR_WM'], pipeID, wmLevel, bitMaps['WM_LINES']))
            csv_output.append(self.getCursorWMRegValue(baseRegisters['CUR_WM'], pipeID, wmLevel, bitMaps['WM_BLOCKS']))
            print("Level :", wmLevel)

        if (self.getCursorRegValue(baseRegisters['CUR_TRANS_WM'], pipeID, bitMaps['WM_ENABLE']) == 1):
            csv_output.append('True')
        else:
            csv_output.append('False')

        csv_output.append(self.getCursorRegValue(baseRegisters['CUR_TRANS_WM'], pipeID, bitMaps['WM_BLOCKS']))
        csv_output.append(self.getLinetimeRegValue(baseRegisters['WM_LINETIME'], pipeID, bitMaps['WM_LINETIME']))

        with open(self.opfile, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow((csv_output))

    def CompareWMValuesWithGoldenData(self):
        programmed_wm = []
        ref_wm = []

        with open('.\\MPO3H\\WM_output.csv', 'rb') as f1:
            reader1 = csv.reader(f1)
            programmed_wm = list(reader1)

        with open('.\\MPO3H\\WM_ref.csv', 'rb') as f2:
            reader2 = csv.reader(f2)
            ref_wm = list(reader2)

        for reg_row, ref_row in zip(programmed_wm, ref_wm):
            if (reg_row != ref_row):
                print("Not matching !!!!")
                print("\n ", reg_row)
                print("\n", ref_row)

    def GenerateRefData(self):
        input = []
        ref_wm = []
        with open('.\\MPO3H\\WM_ref.csv', 'a') as csvfile:
            csvfile.truncate()
            csvfile.close()
        with open('.\\MPO3H\\WM_input.csv', 'rb') as f1:
            reader1 = csv.reader(f1)
            input = list(reader1)
        print(input)
        for row in input:
            with open('.\\MPO3H\\EXE_input.csv', 'wb') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(row)
                csvfile.close()
            self.RunWMExcel()
            with open('.\\MPO3H\\EXE_output.csv', 'rb') as f:
                reader = csv.reader(f)
                ref_wm = list(reader)
                f.close()
            with open('.\\MPO3H\\WM_ref.csv', 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows((ref_wm))
                csvfile.close()


if __name__ == "__main__":
    FORMAT = '%(asctime)-15s %(levelname)s  [%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s'
    logging.basicConfig(filename="cdclk_skl.log", stream=sys.stderr, level="DEBUG", format=FORMAT)
    wm = Watermark()
    wm.get_display_info()
    wm.setup('SinglePlane')
    # wm.fill_csvInput(2,0)

    # wm.fill_csvOutput(0,0)

    # wm.GenerateRefData()

    # wm.CompareWMValuesWithGoldenData()

    # wm.get_memory_latency()
