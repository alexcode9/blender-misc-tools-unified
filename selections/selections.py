import bpy

def selectChildrenRecursive(obj):
    childNum = len(obj.children)

    if childNum > 0:
        for i in range(0, childNum):
            obj.children[i].select = True
            selectChildrenRecursive(obj.children[i])