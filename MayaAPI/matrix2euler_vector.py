# Python code
import math
import maya.cmds as mc
import maya.OpenMaya as om
# Define a node to pull a matrix from.
node = 'pCube1'
# Set some rotation values for comparison later:
mc.setAttr('%s.rotate'%node, 15, -45, 1000)
mc.setAttr('%s.scale'%node, 3, 3, 3)

# Change the rot order, to make sure returned euler values are correct:
mc.setAttr('%s.rotateOrder'%node, 3)

#-------------------------------------------
# Part 1: Get a MTransformationMatrix from an object for the sake of the example.
# You can use your own MTransformationMatrix if it already exists of course.

sellist = om.MSelectionList() # makes a selection list empy from om
sellist.add(node) #add our node by variable or name or whatever
mDagPath = om.MDagPath() # create and empty dag path

sellist.getDagPath(0,mDagPath) # fill the dag path with our node
#----------------------------------------
# Create a MFnTransform object for our MDagPath
# and extract a MTransformationMatrix from it:
transformFunc = om.MFnTransform(mDagPath) #mfTransform
mTransformMtx = transformFunc.transformation() # MTransformationMatrix

# Part 2, get the euler values
# Get an MEulerRotation object
eulerRot = mTransformMtx.eulerRotation() # this last is MeulerRotation
#note we dont have to set the rot order here ...

# Convert from radians to degrees
angles = [math.degrees(angle) for angle in(eulerRot.x,eulerRot.y,eulerRot.z)]
print angles,"MTransformationMatrix"