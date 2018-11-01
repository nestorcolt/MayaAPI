import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as mpx

#################################################################################################
# Globals:
NODE_NAME = "wheelNode"
NODE_ID = om.MTypeId(0x100fff)

#################################################################################################


class WheelNode(mpx.MPxNode):

    inRadius = om.MObject()
    inTranslate = om.MObject()
    outRotate = om.MObject()

    def __init__(self):
        super(WheelNode, self).__init__()

    def compute(self, plug, dataBlock):
        """
        rotate = translate / (2 * 3.14 * radius) * (-360)
        """

        if plug == WheelNode.outRotate:

            dataHandleRadius = dataBlock.inputValue(WheelNode.inRadius)
            dataHandleTranslate = dataBlock.inputValue(WheelNode.inTranslate)
            #
            inRadiusValue = dataHandleRadius.asFloat()
            inTranslateValue = dataHandleTranslate.asFloat()
            #
            self.outRotate = float(inTranslateValue) / float(2 * 3.14 * inRadiusValue) * (-360)
            #
            dataHandleRotate = dataBlock.outputValue(WheelNode.outRotate)
            dataHandleRotate.setFloat(self.outRotate)
            dataBlock.setClean()

        else:
            return om.kUnknownParameter


#################################################################################################


def nodeInitializer():
    # 1 creating a function set for numeric attributes
    MFnAttr = om.MFnNumericAttribute()

    # 2 creating attributes
    WheelNode.inRadius = MFnAttr.create("radius", "r", om.MFnNumericData.kFloat, 0.0)
    MFnAttr.setReadable(1)
    MFnAttr.setWritable(1)
    MFnAttr.setStorable(1)
    MFnAttr.setKeyable(1)
    #
    WheelNode.inTranslate = MFnAttr.create("translate", "t", om.MFnNumericData.kFloat, 0.0)
    MFnAttr.setReadable(1)
    MFnAttr.setWritable(1)
    MFnAttr.setStorable(1)
    MFnAttr.setKeyable(1)
    #
    WheelNode.outRotate = MFnAttr.create("rotate", "r", om.MFnNumericData.kFloat)
    MFnAttr.setReadable(1)
    MFnAttr.setWritable(0)
    MFnAttr.setStorable(0)
    MFnAttr.setKeyable(0)

    # 3 Attaching the attributes to the node
    WheelNode.addAttribute(WheelNode.inRadius)
    WheelNode.addAttribute(WheelNode.inTranslate)
    WheelNode.addAttribute(WheelNode.outRotate)

    # 4 Design circuitry
    WheelNode.attributeAffects(WheelNode.inRadius, WheelNode.outRotate)
    WheelNode.attributeAffects(WheelNode.inTranslate, WheelNode.outRotate)


def nodeCreator():
    return mpx.asMPxPtr(WheelNode())


def initializePlugin(mobject):
    MPlugin = mpx.MFnPlugin(mobject)
    try:
        MPlugin.registerNode(NODE_NAME, NODE_ID, nodeCreator, nodeInitializer)
    except:
        sys.stderr.write("Failed to register node: %s\n" % NODE_NAME)


def uninitializePlugin(mobject):
    MPlugin = mpx.MFnPlugin(mobject)
    try:
        MPlugin.deregisterNode(NODE_NAME)
    except:
        sys.stderr.write("Failed to unregister node: %s\n" % NODE_NAME)
