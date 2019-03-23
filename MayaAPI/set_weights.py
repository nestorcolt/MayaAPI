from contextlib import  contextmanager
import maya.OpenMaya as om
import maya.OpenMayaAnim as aom
import time

######################################################################################################
@contextmanager
def benchmark():
    # Measures code execution time
    start = time.time()
    yield
    end = time.time()
    print("Code execution time: {}".format(end - start))

######################################################################################################
MESH_BASE = "base"
MESH_TARG = "target"
SKIN = "skinCluster1"
CLUSTER = "thisCluster"
######################################################################################################

def getDag(string_name):
    MSelList = om.MSelectionList()
    MSelList.add(string_name)
    MDag = om.MDagPath()
    MSelList.getDagPath(0, MDag)
    return MDag

def getMObject(string_name):
    MSelList = om.MSelectionList()
    MSelList.add(string_name)
    MObj = om.MObject()
    MSelList.getDependNode(0, MObj)
    return MObj

def get_deformer_set_related(deformer):
    mfn_set = om.MFnSet(deformer.deformerSet())
    members = om.MSelectionList()
    mfn_set.getMembers(members, False)
    dag_path_members = om.MDagPath()
    mo_set_components = om.MObject()
    members.getDagPath(0, dag_path_members, mo_set_components)
    return dag_path_members, mo_set_components

######################################################################################################

def get_def_w(deformer):
    FnDeformer = aom.MFnWeightGeometryFilter(getMObject(deformer))
    mfn_set = om.MFnSet(FnDeformer.deformerSet())
    members = om.MSelectionList()
    mfn_set.getMembers(members, False)
    dag_path_members = om.MDagPath()
    mo_set_components = om.MObject()
    members.getDagPath(0, dag_path_members, mo_set_components)
    MFloatArray = om.MFloatArray()
    FnDeformer.getWeights(0,mo_set_components, MFloatArray)
    return MFloatArray

def set_skin_weights(skin, weights, target):
    mfn_skin = aom.MFnSkinCluster(getMObject(skin))
    _, components = get_deformer_set_related(mfn_skin)
    doubleArrayFromFloat = om.MDoubleArray()
    doubleArrayFromFloat.setLength(weights.length() * 2)
    counter = 0
    #
    for idx in range(0, doubleArrayFromFloat.length(), 2):
        weight = weights[counter]
        inverse_weight = 1.0 - weight
        next_idx = idx + 1
        doubleArrayFromFloat.set(weight, idx)
        doubleArrayFromFloat.set(inverse_weight, next_idx)
        counter += 1
    #
    InfArray = om.MIntArray()
    InfArray.setLength(2)
    [InfArray.set(idx, idx) for idx in  range(2)]
    #
    mfn_skin.setWeights(getDag(target), components , InfArray, doubleArrayFromFloat, False)


######################################################################################################
#
with benchmark():
    weights_array = get_def_w(CLUSTER)
    set_skin_weights(SKIN, weights_array, MESH_TARG)