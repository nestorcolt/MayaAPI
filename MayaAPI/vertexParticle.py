import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as mpx
import maya.OpenMayaFX as ofx


#################################################################################################
# Globals:
COMMAND_NAME = "vertexParticles"

# Flags:
kHelpFlag = "-h"
kHelpLongFlag = "-help"
#
kSparseFlag = "-s"
kSparseLongFlag = "-sparce"
#
HELP_MESSAGE = "This will add a particle to each mesh vertex"
#################################################################################################


class PlugInCommand(mpx.MPxCommand):

    sparse = None
    MObjParticle = None

    def __init__(self):
        super(PlugInCommand, self).__init__()

    #################################################################################################

    def doIt(self, argList):
        print("doing it...")

        self.argumentParser(argList)
        if self.sparse is not None:
            self.redoIt()
        #
        return

    #################################################################################################

    def isUndoable(self):
        return True

    #################################################################################################

    def undoIt(self):

        mFnDagNode = om.MFnDagNode(self.MObjParticle)
        mDagMod = om.MDagModifier()
        mDagMod.deleteNode(mFnDagNode.parent(0))
        mDagMod.doIt()

    #################################################################################################

    def redoIt(self):
        MSel = om.MSelectionList()
        MDag = om.MDagPath()
        MfnMesh = om.MFnMesh()
        om.MGlobal.getActiveSelectionList(MSel)

        if MSel.length() >= 1:
            try:
                MSel.getDagPath(0, MDag)
                MfnMesh.setObject(MDag)
            except:
                om.MGlobal.displayError("Select a poly mesh")
                return
        else:
            om.MGlobal.displayError("Select mesh object in scene")
            return
        #
        MPointArray = om.MPointArray()
        MfnMesh.getPoints(MPointArray, om.MSpace.kWorld)
        #
        MFnParticle = ofx.MFnParticleSystem()
        self.MObjParticle = MFnParticle.create()
        MFnParticle = ofx.MFnParticleSystem(self.MObjParticle)
        #
        #
        counter = 0

        for idx in range(MPointArray.length()):
            if idx % self.sparse == 0:
                MFnParticle.emit(MPointArray[idx])
                counter += 1

        om.MGlobal.displayInfo("Total points: {}".format(counter))
        MFnParticle.saveInitialState()

    #################################################################################################

    def argumentParser(self, argList):

        syntax = self.syntax()
        #
        try:
            parsedArguments = om.MArgDatabase(syntax, argList)
        except:
            return

        if parsedArguments.isFlagSet(kSparseFlag):
            self.sparse = parsedArguments.flagArgumentDouble(kSparseFlag, 0)

        if parsedArguments.isFlagSet(kSparseLongFlag):
            self.sparse = parsedArguments.flagArgumentDouble(kSparseLongFlag, 0)

        if parsedArguments.isFlagSet(kHelpFlag):
            self.setResult(HELP_MESSAGE)

        if parsedArguments.isFlagSet(kHelpLongFlag):
            self.setResult(HELP_MESSAGE)


#################################################################################################
#
#
#

# Command Creator
def cmdCreator():
    return mpx.asMPxPtr(PlugInCommand())


# Syntax Creator
def syntaxCreator():
    syntax = om.MSyntax()
    # add flgas
    syntax.addFlag(kHelpFlag, kHelpLongFlag)
    syntax.addFlag(kSparseFlag, kSparseLongFlag, om.MSyntax.kDouble)
    return syntax


# Initialize the script plug-iN
def initializePlugin(MObject):
    MPlugin = mpx.MFnPlugin(MObject)
    try:
        MPlugin.registerCommand(COMMAND_NAME, cmdCreator, syntaxCreator)
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
