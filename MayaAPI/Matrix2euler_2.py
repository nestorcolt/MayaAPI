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
#------------#
#get the rotate order from node
rotOrder = mc.getAttr('{}.rotateOrder'.format(node))
# Get the world matrix as a list
matrix1 = mc.getAttr('%s.worldMatrix'%node)
matrix2 = mc.xform(node, q=1, m=1) 
# Create an empty MMatrix:
mMatrix = om.MMatrix() # creaa matrix vacia
# populate the MMatrix object with te matrix list data
om.MScriptUtil.createMatrixFromList(matrix1,mMatrix)

# part 2 ---------------------------
## Convert to MTransformationMatrix to extract rotations:
mTransformMtx = om.MTransformationMatrix(mMatrix)
# Get an MEulerRotation object
eulerRot = mTransformMtx.eulerRotation()
# Update rotate order to match original object, since the orig MMatrix has
# no knoweldge of it:
eulerRot.reorderIt(rotOrder)
#convert from radians to degrees
angles = [math.degrees(angle) for angle in (eulerRot.x, eulerRot.y, eulerRot.z)]
print angles,"MMatrix"
