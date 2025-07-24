import glob
modules = []
for module_name in glob.glob("*.py"):
    modules.append(__import__(module_name[:-3]))