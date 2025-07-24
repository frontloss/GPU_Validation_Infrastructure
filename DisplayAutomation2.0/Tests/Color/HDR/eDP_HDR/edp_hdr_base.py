import win32serviceutil
import time

from Libs.Core import display_essential
from Tests.Color import color_common_utility
from Tests.Color import color_common_constants
from Tests.Color.HDR.eDP_HDR import edp_hdr_utility
from Tests.Color.color_common_base import *


class eDPHDRBase(ColorCommonBase):
	@reboot_helper.__(reboot_helper.setup)
	def setUp(self):
		super().setUp()
		##
		# Perform a driver restart to capture the HDRCaps Details
		restart_status, reboot_required = display_essential.restart_gfx_driver()
		win32serviceutil.RestartService("Display Enhancement Service")
		##
		# Check Power Mode  for DC or AC to check the HDR Option temporarily disabled
		result, status = color_common_utility.check_and_apply_power_mode()
		if status:
			logging.info(result)
		else:
			self.fail(result)

	@reboot_helper.__(reboot_helper.teardown)
	def tearDown(self):
		##
		# Set default brightness at 100 at the end of the test
		color_common_utility.set_os_brightness(100, delay=0)
		##
		# Apply Unity Gamma at the end of the test after disabling HDR(Done as part of OSHDR tearDown())
		color_common_utility.apply_unity_gamma()
		super().tearDown()



