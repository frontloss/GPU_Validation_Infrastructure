########################################################################################################################
# @file     mode_vic_info.py
# @brief    Python file to maintain Mode VIC Structures
# @author   Veluru, Veena
########################################################################################################################
DEFAULT_VIC_ID = 255

VIC_MODE_INFO = {
    "vic_194_202": {
        "hactive": 7680,
        "vactive": 4320,
        "refresh_rate": 24,
        "pixel_clock": 1188000000,
        "htotal": 11000,
        "vtotal": 4500,
        "interlaced": 1
    },
    "vic_195_203": {
        "hactive": 7680,
        "vactive": 4320,
        "refresh_rate": 25,
        "pixel_clock": 1188000000,
        "htotal": 10800,
        "vtotal": 4400,
        "interlaced": 1
    },
    "vic_196_204": {
        "hactive": 7680,
        "vactive": 4320,
        "refresh_rate": 30,
        "pixel_clock": 1188000000,
        "htotal": 9000,
        "vtotal": 4400,
        "interlaced": 1
    },
    "vic_197_205": {
        "hactive": 7680,
        "vactive": 4320,
        "refresh_rate": 48,
        "pixel_clock": 2376000000,
        "htotal": 11000,
        "vtotal": 4500,
        "interlaced": 1
    },
    "vic_198_206": {
        "hactive": 7680,
        "vactive": 4320,
        "refresh_rate": 50,
        "pixel_clock": 2376000000,
        "htotal": 10800,
        "vtotal": 4400,
        "interlaced": 1
    },
    "vic_199_207": {
        "hactive": 7680,
        "vactive": 4320,
        "refresh_rate": 60,
        "pixel_clock": 2376000000,
        "htotal": 9000,
        "vtotal": 4400,
        "interlaced": 1
    },
    "vic_200_208": {
        "hactive": 7680,
        "vactive": 4320,
        "refresh_rate": 100,
        "pixel_clock": 4752000000,
        "htotal": 10560,
        "vtotal": 4500,
        "interlaced": 1
    },
    "vic_121": {
        "hactive": 5120,
        "vactive": 2160,
        "refresh_rate": 24,
        "pixel_clock": 396000000,
        "htotal": 7500,
        "vtotal": 2200,
        "interlaced": 1
    },
    "vic_122": {
        "hactive": 5120,
        "vactive": 2160,
        "refresh_rate": 25,
        "pixel_clock": 396000000,
        "htotal": 7200,
        "vtotal": 2200,
        "interlaced": 1
    },
    "vic_123": {
        "hactive": 5120,
        "vactive": 2160,
        "refresh_rate": 30,
        "pixel_clock": 396000000,
        "htotal": 6000,
        "vtotal": 2200,
        "interlaced": 1
    },
    "vic_127": {
        "hactive": 5120,
        "vactive": 2160,
        "refresh_rate": 100,
        "pixel_clock": 1485000000,
        "htotal": 6600,
        "vtotal": 2250,
        "interlaced": 1
    },
    "vic_124": {
        "hactive": 5120,
        "vactive": 2160,
        "refresh_rate": 48,
        "pixel_clock": 742500000,
        "htotal": 6250,
        "vtotal": 2475,
        "interlaced": 1
    },
    "vic_125": {
        "hactive": 5120,
        "vactive": 2160,
        "refresh_rate": 50,
        "pixel_clock": 742500000,
        "htotal": 6600,
        "vtotal": 2250,
        "interlaced": 1
    },
    "vic_126": {
        "hactive": 5120,
        "vactive": 2160,
        "refresh_rate": 60,
        "pixel_clock": 742500000,
        "htotal": 5500,
        "vtotal": 2250,
        "interlaced": 1
    },
    "vic_193": {
        "hactive": 5120,
        "vactive": 2160,
        "refresh_rate": 120,
        "pixel_clock": 1485000000,
        "htotal": 5500,
        "vtotal": 2250,
        "interlaced": 1
    },
    "vic_114_116": {
        "hactive": 3840,
        "vactive": 2160,
        "refresh_rate": 48,
        "pixel_clock": 594000000,
        "htotal": 5500,
        "vtotal": 2250,
        "interlaced": 1
    },
    "vic_96_106": {
        "hactive": 3840,
        "vactive": 2160,
        "refresh_rate": 50,
        "pixel_clock": 594000000,
        "htotal": 5280,
        "vtotal": 2250,
        "interlaced": 1
    },
    "vic_97_107": {
        "hactive": 3840,
        "vactive": 2160,
        "refresh_rate": 60,
        "pixel_clock": 594000000,
        "htotal": 4400,
        "vtotal": 2250,
        "interlaced": 1
    },
    "vic_117_119": {
        "hactive": 3840,
        "vactive": 2160,
        "refresh_rate": 100,
        "pixel_clock": 1188000000,
        "htotal": 5280,
        "vtotal": 2250,
        "interlaced": 1
    },
    "vic_118_120": {
        "hactive": 3840,
        "vactive": 2160,
        "refresh_rate": 120,
        "pixel_clock": 1188000000,
        "htotal": 4400,
        "vtotal": 2250,
        "interlaced": 1
    },
    "vic_115": {
        "hactive": 4096,
        "vactive": 2160,
        "refresh_rate": 48,
        "pixel_clock": 594000000,
        "htotal": 5500,
        "vtotal": 2250,
        "interlaced": 1
    },
    "vic_101": {
        "hactive": 4096,
        "vactive": 2160,
        "refresh_rate": 50,
        "pixel_clock": 594000000,
        "htotal": 5280,
        "vtotal": 2250,
        "interlaced": 1
    },
    "vic_218": {
        "hactive": 4096,
        "vactive": 2160,
        "refresh_rate": 100,
        "pixel_clock": 1188000000,
        "htotal": 5280,
        "vtotal": 2250,
        "interlaced": 1
    },
    "vic_219": {
        "hactive": 4096,
        "vactive": 2160,
        "refresh_rate": 120,
        "pixel_clock": 1188000000,
        "htotal": 4400,
        "vtotal": 2250,
        "interlaced": 1
    },
    "vic_212": {
        "hactive": 10240,
        "vactive": 4320,
        "refresh_rate": 30,
        "pixel_clock": 1485000000,
        "htotal": 11000,
        "vtotal": 4500,
        "interlaced": 1
    },
    "vic_215": {
        "hactive": 10240,
        "vactive": 4320,
        "refresh_rate": 60,
        "pixel_clock": 2970000000,
        "htotal": 11000,
        "vtotal": 4500,
        "interlaced": 1
    },
    "vic_216": {
        "hactive": 10240,
        "vactive": 4320,
        "refresh_rate": 100,
        "pixel_clock": 5940000000,
        "htotal": 13200,
        "vtotal": 4500,
        "interlaced": 1
    },
    "vic_217": {
        "hactive": 10240,
        "vactive": 4320,
        "refresh_rate": 120,
        "pixel_clock": 5940000000,
        "htotal": 11000,
        "vtotal": 4500,
        "interlaced": 1
    },
    "vic_201_209": {
      "hactive": 7680,
      "vactive": 4320,
      "refresh_rate": 120,
      "pixel_clock": 4752000000,
      "htotal": 8800,
      "vtotal": 4500,
      "interlaced": 1
    },
    "vic_93_103": {
        "hactive": 3840,
        "vactive": 2160,
        "refresh_rate": 24,
        "pixel_clock": 297000000,
        "htotal": 5500,
        "vtotal": 2250,
        "interlaced": 1
    },
    "vic_94_104": {
        "hactive": 3840,
        "vactive": 2160,
        "refresh_rate": 25,
        "pixel_clock": 297000000,
        "htotal": 5280,
        "vtotal": 2250,
        "interlaced": 1
    },
    "vic_95_105": {
        "hactive": 3840,
        "vactive": 2160,
        "refresh_rate": 30,
        "pixel_clock": 297000000,
        "htotal": 4400,
        "vtotal": 2250,
        "interlaced": 1
    },
    "vic_32_72": {
        "hactive": 1920,
        "vactive": 1080,
        "refresh_rate": 24,
        "pixel_clock": 74250000,
        "htotal": 2750,
        "vtotal": 1125,
        "interlaced": 1
    },
    "vic_33_73": {
        "hactive": 1920,
        "vactive": 1080,
        "refresh_rate": 25,
        "pixel_clock": 74250000,
        "htotal": 2640,
        "vtotal": 1125,
        "interlaced": 1
    },
    "vic_34_74": {
        "hactive": 1920,
        "vactive": 1080,
        "refresh_rate": 30,
        "pixel_clock": 74250000,
        "htotal": 2200,
        "vtotal": 1125,
        "interlaced": 1
    },
    "vic_31_75": {
        "hactive": 1920,
        "vactive": 1080,
        "refresh_rate": 50,
        "pixel_clock": 148500000,
        "htotal": 2640,
        "vtotal": 1125,
        "interlaced": 1
    },
    "vic_16_76": {
        "hactive": 1920,
        "vactive": 1080,
        "refresh_rate": 60,
        "pixel_clock": 148500000,
        "htotal": 2200,
        "vtotal": 1125,
        "interlaced": 1
    },
    "vic_64_77": {
        "hactive": 1920,
        "vactive": 1080,
        "refresh_rate": 100,
        "pixel_clock": 297000000,
        "htotal": 2640,
        "vtotal": 1125,
        "interlaced": 1
    },
    "vic_63_78": {
        "hactive": 1920,
        "vactive": 1080,
        "refresh_rate": 120,
        "pixel_clock": 297000000,
        "htotal": 2200,
        "vtotal": 1125,
        "interlaced": 1
    },
    "vic_5": {
        "hactive": 1920,
        "vactive": 1080,
        "refresh_rate": 60,
        "pixel_clock": 74250000,
        "htotal": 2200,
        "vtotal": 1125,
        "interlaced": 2
    },
    "vic_20": {
        "hactive": 1920,
        "vactive": 1080,
        "refresh_rate": 50,
        "pixel_clock": 74250000,
        "htotal": 2640,
        "vtotal": 1125,
        "interlaced": 2
    },
}
