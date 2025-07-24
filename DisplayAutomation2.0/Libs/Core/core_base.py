############################################################################################################
# @file         core_base.py
# @brief        Base module for core library
# @author       Chandrakanth Pabolu
############################################################################################################


##
# @brief        Pre-defined decorator method
# @param[in]    class_ - target class
# @return       getinstance - class object
def singleton(class_):
    instances = {}

    ##
    # @brief        API to get existing instance of a class
    # @return       object - class object
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance
