import sys
sys.path.insert(0, r'../selections')

import bpy
from selections import selectChildrenRecursive


class UT_OT_SelectMeshObjectOperator(bpy.types.Operator):
    bl_idname = "select.meshobjects"
    bl_label = "Select Mesh objects"
    name = "selectmeshobjects"

    def execute(self, context):
        ctx = bpy.context
        scn = context.scene
        nameIncl = "" #scn.namePartInclude
        masterParents = []
        objToDelete = []

        if nameIncl != "":
            self.report({'INFO'}, "debug")
            bpy.ops.object.select_pattern(pattern="*" + nameIncl + "*", extend=False)
            for obj in bpy.context.selected_objects:
                if obj.type != 'MESH':
                    obj.select = False
            bpy.context.scene.objects.active = ctx.selected_objects[0];
            # TO BE CONTINUED
        else:
            for obj in bpy.context.selected_objects:
                masterParents.append(obj)
            bpy.ops.object.select_all(action='DESELECT')
            for parent in masterParents:
                print(masterParents)
                print(parent)
                selectChildrenRecursive(parent)
                for selObj in bpy.context.selected_objects:
                    if selObj.type != 'MESH':
                        objToDelete.append(selObj)
                        selObj.select = False
                bpy.context.scene.objects.active = ctx.selected_objects[0];
                bpy.ops.object.join()
                bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
                bpy.context.scene.objects.active = parent
                bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
                bpy.ops.object.select_all(action='DESELECT')
                for delObj in objToDelete:
                    delObj.select = True
                bpy.ops.object.delete(use_global=False)
                bpy.ops.object.select_all(action='DESELECT')

        return {'FINISHED'}