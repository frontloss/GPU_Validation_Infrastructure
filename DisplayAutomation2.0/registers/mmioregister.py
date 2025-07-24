############################################################################################################
# @file         mmioregister.py
# @addtogroup   PyLibs_HelperLibs
# @section      MMIORegister
# @description  @ref mmioregister.py <br>
#               The script provides platform agnostic generic MMIO read mechanism. The API uses factory design pattern
#               to platform agnostic way of creating register instances dynamically and load register instance from the
#               offset value provides as reg_name.
#
#               Example:
#               plane_ctl = MMIORegister.read("PLANE_CTL_REGISTER", "PLANE_CTL_1_A")
#               print plane_ctl.plane_enable
#
#               result = MMIORegister.dump_register(plane_ctl)
#               print('\n'.join(line for line in result))
#
# @note         Do not modify this wrapper without consent from the author.
# @author       Beeresh
############################################################################################################
import importlib
import logging

from Libs.Core.sw_sim import driver_interface


class MMIORegister(object):

    ##
    # @brief        Helper function to create register instance for the provide platform and offset value
    # @param[in]    module_name - Register name, should be same of script name
    # @param[in]    reg_name - Register instance name, equivalent to interested offset
    # @param[in]    platform - Platform to look for register, based on this parameter register repo will change
    # @param[in]    extra_offset
    # @param[in]    gfx_index, String, adapter index of targeted adapter
    # @return       register instance with current register value
    @staticmethod
    def read(module_name, reg_name, platform="skl", extra_offset=0x0, gfx_index='gfx_0'):
        # dynamically get the register offset value using variable name - reg_name
        instance = MMIORegister.get_instance(module_name, reg_name, platform)
        instance.offset += extra_offset

        # Read mmio register with offset value and assign mmio read value and offset to register instance
        instance.asUint = driver_interface.DriverInterface().mmio_read(instance.offset, gfx_index)

        logging.debug("{0}[{1}] = {2}".format(reg_name, hex(instance.offset), hex(instance.asUint)))

        return instance

    @staticmethod
    def get_instance(module_name, reg_name, platform="skl", reg_val=0):
        class_name = module_name
        platform = platform.lower()

        # namespace to import example: registers.skl.TRANS_CONFIG_REGISTER
        namespace = "registers.{0}.{1}".format(platform, module_name)

        # import namespace to handle of the module
        module = importlib.import_module(namespace)

        # dynamically instantiate the Class type
        class_ = getattr(module, class_name)

        # dynamically instantiate the object from class type
        instance = class_()

        # dynamically get the register offset value using variable name - reg_name
        reg_offset_ = getattr(module, reg_name)

        instance.__setattr__('offset', reg_offset_)
        instance.__setattr__('asUint', reg_val)

        return instance

    ##
    # @brief        Helper function to dump register details with enum values instead of absolute value
    # @param[in]    reg - Register object
    # @return       List of str with register field name and value
    @staticmethod
    def dump_register(reg):
        result = []

        if reg is None:
            logging.error("Parameter is None")
            return ""

        module_name = reg.__module__
        if "REGISTER" not in module_name:
            logging.error("Invalid module name")
            return ""

        module = importlib.import_module(module_name)
        if module is None:
            logging.error("Error in importing module ", module_name)
            return ""

        module_fields = {}
        if module:
            module_fields = {key: value for key, value in module.__dict__.items()
                             if not (key.startswith('__') or key.startswith('_'))}

        for field_name, field_type, bit_size in reg.u._fields_:
            field_value = getattr(reg.u, field_name)
            value_enum = None
            for attr, value in module_fields.items():
                if field_name in attr:
                    match_value = module_fields[attr]
                    if field_value == match_value:
                        value_enum = attr.replace("{0}_".format(field_name), "")
                        break

            if value_enum is not None:
                msg = "{0}:{1}".format(field_name, value_enum)
                result.append(msg)
            else:
                msg = "{0}:{1}".format(field_name, field_value)
                result.append(msg)

        return result


if __name__ == "__main__":
    # transa_reg = MMIORegister.read("TRANS_CONF_REGISTER", "TRANS_CONF_A")
    # print(transa_reg)
    reg = MMIORegister.read("PLANE_CTL_REGISTER", "PLANE_CTL_1_A")
    # reg = PLANE_CTL_REGISTER()

    result = MMIORegister.dump_register(reg)
    print('\n'.join(line for line in result))
