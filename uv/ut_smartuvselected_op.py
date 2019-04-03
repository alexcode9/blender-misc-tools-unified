import sys
sys.path.insert(0, r'../selections')
sys.path.insert(0, r'../misc')

import bpy
from selections import selectChildrenRecursive
from progress import update_progress


class UT_OT_SmartUVSelectedOperator(bpy.types.Operator):
    bl_idname = "smartuv.selected"
    bl_label = "Smart UV on selected"
    name = "smartuvSelected"

    def execute(self, context):
        ctx = bpy.context
        scn = context.scene
        masterParents = []
        objects = []
        for obj in bpy.context.selected_objects:
            masterParents.append(obj)
        bpy.ops.object.select_all(action='DESELECT')
        for parent in masterParents:
            selectChildrenRecursive(obj)
            for selObj in bpy.context.selected_objects:
                if selObj.type != 'MESH':
                    selObj.select = False
                else:
                    objects.append(selObj)
            for idx, obj in enumerate(objects):
                bpy.ops.object.select_all(action='DESELECT')
                obj.select = True
                bpy.ops.uv.smart_project()
                update_progress("Smart UV Gen", idx * 1 / len(objects))
            bpy.ops.object.select_all(action='DESELECT')
        update_progress("Smart UV Gen", 1)

        return {'FINISHED'}