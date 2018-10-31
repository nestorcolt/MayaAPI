import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as mpx

#################################################################################################
# Globals:

COMMAND_NAME = "pluginCommand"

#################################################################################################


class PlugInCommand(mpx.MPxCommand):

    def __init__(self):
        super(PlugInCommand, self).__init__()

    def doIt(self, argList):
        print("doing it...")


#################################################################################################

# Command Creator
def cmdCreator():
    return mpx.asMPxPtr(PlugInCommand())


# Initialize the script plug-iN
def initializePlugin(MObject):
    MPlugin = mpx.MFnPlugin(MObject)
    try:
        MPlugin.registerCommand(COMMAND_NAME, cmdCreator)
    except:
        sys.stderr.write("Failed to initialize command name: %s\n" % COMMAND_NAME)


# un-Initialize the script plug-iN
def uninitializePlugin(MObject):
    MPlugin = mpx.MFnPlugin(MObject)
    try:
        MPlugin.deregisterCommand(COMMAND_NAME)
    except:
        sys.stderr.write("Failed to unitialize command name: %s\n" % COMMAND_NAME)


#
#################################################################################################
