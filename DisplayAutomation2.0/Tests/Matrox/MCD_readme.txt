## syntax - OpType and NumOutputs must be placed at first. Configuration item label is case sensitive.

OpType = 2				# Currently validated OpType is 2, i.e. enable MCD. Use other PS scripts for Disable MCD.
NumOutputs = 4			# Number of (display) outputs: has to be 2 or greater, maximum is 16.
DisplayOrder = 0,1,2,3		# which displays are involved: 0 indicates the first. This index number corresponds to Display_Number in the ChildInfo below.
# 						  order matters, "1 0" means display 1 will be viewed as first elected and display 0 is will be viewed as 2nd selected.
# 				** NumOutputs above will decide how many entries in the DisplayOrder list will be selected. if NumOutputs=2, only first 2 in the DisplayOrder are used.
#				Note: The selected Displays should involve Multiple adapters to get this MCD API working. If all Displays are from Single GPU, the API call will fail.

CombinedDesktopWidth = 3840    	 # combined display width
CombinedDesktopHeight = 2160	 # combined display height

#   ChildInfo = Display_Number,{FbSrc},{FbPos},Orientation,{Target Mode}
#     where
# 	 FbSrc = {left,top,right,bottom} : 	Source rect in the frame buffer relative pos. The rect should fit within [ CombinedDesktopWidth x CombinedDesktopHeight ]
#	 FbPos = {left,top,right,bottom} : 	Dest Rect in the Monitor relative position. This rect should fit within Target Mode [ W x H ].
#								  It will match the monitor resolution to fill the whole display.
# 	Display Orientation = 0 (0 rotation), 2 (180 rotation)
# 	Target Mode = {width, height, refresh} : If 0, this means using native target mode instead of custom mode.
#
# 	Note: The below list order does not matter. The 'Display_Number' will need to match 'DisplayOrder' item number above.
#
ChildInfo = 0,{0,0,1920,1080},{0,0,1920,1080}, 0, {1920,1080,60}
ChildInfo = 1,{1920,0,3840,1080},{0,0,1920,1080}, 0, {1920,1080,60}
ChildInfo = 2,{0,1080,1920,2160},{0,0,1920,1080}, 0, {1920,1080,60}
ChildInfo = 3,{1920,1080,3840,2160},{0,0,1920,1080}, 0, {1920,1080,60}