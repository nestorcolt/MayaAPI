from contextlib import  contextmanager
import maya.OpenMaya as om
import maya.OpenMayaAnim as aom
import time
########################
# API 2017 C ++
"https://help.autodesk.com/view/MAYAUL/2017/ENU/?guid=__cpp_ref_classes_html"
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

def get_componets(deformer):
    mfn_set = om.MFnSet(deformer.deformerSet())
    members = om.MSelectionList()
    mfn_set.getMembers(members, False)
    dag_path_members = om.MDagPath()
    mo_set_components = om.MObject()
    members.getDagPath(0, dag_path_members, mo_set_components)
    return dag_path_members, mo_set_components

######################################################################################################

def get_deformer_weights(deformer):
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
    Inlfuences_count = 2
    mfn_skin = aom.MFnSkinCluster(getMObject(skin))
    _, components = get_componets(mfn_skin)
    doubleArrayFromFloat = om.MDoubleArray()
    doubleArrayFromFloat.setLength(weights.length() * Inlfuences_count)
    #
    idx = 0
    is_done = False
    iterator = iter(weights)
    #
    while not is_done:
        try:
            weight = next(iterator)
            inverse_weight = 1.0 - weight
            next_idx = idx + 1
            doubleArrayFromFloat.set(weight, idx)
            doubleArrayFromFloat.set(inverse_weight, next_idx)
            idx += Inlfuences_count

        except StopIteration:
            is_done = True
    #
    InfArray = om.MIntArray(Inlfuences_count,0)
    [InfArray.set(idx, idx) for idx in  range(Inlfuences_count)]
    mfn_skin.setWeights(getDag(target), components , InfArray, doubleArrayFromFloat, False)

######################################################################################################
#
if __name__ == '__main__':
    #
    with benchmark():
        weights_array = get_deformer_weights(CLUSTER)
        set_skin_weights(SKIN, weights_array, MESH_TARG)