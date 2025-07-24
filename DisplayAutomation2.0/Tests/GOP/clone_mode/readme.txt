Pre OS

Go to UEFI shell -> Run 'fs1:' -> Run 'pre_boot.nsh'


1. pre_boot.nsh -> This will execute the below files in order.
	get_tenh_offset.nsh
	generate_mmio_commands_dump.py
	mmio_dump_commands_nsh.nsh
	map_mmio_values_and_offsets_into_json.py

2. get_tenh_offset.nsh ->  Got the 10h offset in realtime dumped to  tenh_offset.txt file in UEFI shell using the
   command "mm -w 8 -n -pci 20010 > tenh_offset.txt".

	tenh_offset.txt -> It has the 10h value without the last bit changed to 0.

	clone_mmio_offsets.json -> which has required offsets of eDP+HDMI+DP

3. generate_mmio_commands_dump.py ->
	a. Changed the last bit of the 10h offest that we dumped to the tenh_offset.txt file to '0'. This gives the base
	   address.
	b. After getting the base address, we are adding each offset from the clone_mmio_offsets.json to the base address and the
	   resulted values are stored in a list.
	c. Using the values in the above resulted list, we generate a mmio_dump_commands_nsh.nsh file which will contain the
	   commands with the below format.
		mm -w 4 {value_from_list} >> mmio_raw_dump.txt

4. mmio_dump_commands_nsh.nsh -> By running the above generated mmio_dump_commands_nsh.nsh file, a mmio_raw_dump.txt
                                 file gets generated which will contain the MMIO value for each offset.

	mmio_raw_dump.txt -> This contains MMIO Values for each offset.

5. map_mmio_values_and_offsets_into_json.py -> Using the above generated mmio_raw_dump.txt and clone_mmio_offsets.json files, we
                                               map the MMIO values with their corresponding offsets and generated a
                                               final mmio_dump.json file (final MMIO dump).

	mmio_dump.json -> Contains MMIO values with their corresponding offsets and their names.


POST OS

After booting, to run the below python scripts (.py files) in order, we need to run post_boot.py

1. clone_Pipe_verification.py -> Verifying the Expected value of a MMIO offset (related to Pipe) taken from the
                                       mmio_dump.json(in Pre_boot) with the Actual output and making the test Pass or
                                       Fail based on the verification results. The Verification results are dumped into
                                       clone_pipe_verification.log file.

2. clone_Port_verification.py -> Verifying the Expected value of a MMIO offset (related to Plane) taken from the
                                       mmio_dump.json(in Pre_boot) with the Actual output and making the test Pass or
                                       Fail based on the verification results. The Verification results are dumped into
                                       clone_plane_verification.log file.

3. clone_Port_verification.py -> Verifying the Expected value of a MMIO offset (related to Port) taken from the
                                       mmio_dump.json(in Pre_boot) with the Actual output and making the test Pass or
                                       Fail based on the verification results. The Verification results are dumped into
                                       clone_port_verification.log file.

4. clone_Transcoder_verification.py -> Verifying the Expected value of a MMIO offset (related to Transcoder) taken
                                             from the mmio_dump.json(in Pre_boot) with the Actual output and making the
                                             test Pass or Fail based on the verification results. The Verification
                                             results are dumped into clone_transcoder_verification.log file.

post_boot.py -> This will take port as command line argument in case of DP/ HDMI. But for eDP case default argument is
                already passed.

                To run post_boot.py follow below instructions.

                For clone eDP+HDMI / eDP+DP: post_boot.py -<port>
                Port mapping for DP:
                    TCP0: USBC0
                    TCP1: USBC0
                    TCP2: USBC0
                    TCP3: USBC0

                Port mapping for HDMI:
                    TCP0: USBC0
                    TCP1: USBC1
                    TCP2: USBC2
                    TCP3: USBC3