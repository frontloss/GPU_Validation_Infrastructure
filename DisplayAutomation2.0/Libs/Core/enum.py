#######################################################################################################################
# @file         enum.py
# @brief        Helper file for enums definitions
# @author       Chandrakanth, Pabolu
#######################################################################################################################
import ctypes


##
# @brief        EnumType class
class EnumType(type(ctypes.c_uint)):

    ##
    # @brief        Instantiate members in Dictionary
    # @param[in]    metacls - meta class data
    # @param[in]    name - class name
    # @param[in]    bases - Base Values
    # @param[in]    dict - dictionary of members
    # @return       cls - class object
    def __new__(metacls, name, bases, dict):
        if "_members_" not in dict:
            _members_ = {}
            for key, value in dict.items():
                if not key.startswith("_"):
                    _members_[key] = value
            dict["_members_"] = _members_
        cls = type(ctypes.c_uint).__new__(metacls, name, bases, dict)
        for key, value in cls._members_.items():
            globals()[key] = value
        return cls

    ##
    # @brief        overridden contains method
    # @param[in]    value - Member Value
    # @return       value - True if class contains value parameter, False otherwise
    def __contains__(self, value):
        return value in self._members_.values()

    ##
    # @brief        overridden repr method
    # @return       str - String representation of EnumType class
    def __repr__(self):
        return "<Enum %s>" % self.__name__


##
# @brief        Enum Class
class Enum(ctypes.c_uint, metaclass=EnumType):
    _members_ = {}

    ##
    # @brief        Constructor
    # @param[in]    value - Member Value
    def __init__(self, value):
        for k, v in self._members_.items():
            if v == value:
                self.name = k
                break
        else:
            raise ValueError("No enumeration member with value %r" % value)
        ctypes.c_uint.__init__(self, value)

    ##
    # @brief        Get object that can be used as a function call parameter
    # @param[in]    param - ctypes type object
    # @return       param - ctypes class object
    @classmethod
    def from_param(cls, param):
        if isinstance(param, Enum):
            if param.__class__ != cls:
                raise ValueError("Cannot mix enumeration members")
            else:
                return param
        else:
            return cls(param)

    ##
    # @brief        Overridden repr method
    # @return       str - String representation of Enum class
    def __repr__(self):
        return "<member %s=%d of %r>" % (self.name, self.value, self.__class__)

    ##
    # @brief        Overridden str Method
    # @return       str - String representation of Enum class name
    def __str__(self):
        return self.name

    ##
    # @brief        Overridden eq method
    # @param[in]    other - Comparison object
    # @return       bool - True if both objects are equal, False otherwise
    def __eq__(self, other):
        return self.value == other
