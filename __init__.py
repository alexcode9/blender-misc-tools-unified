'''
Created on 3 Jan 2017

@author: Alex
'''

bl_info = {
    "name" : "UnifiedTool",
    "author" : "Alexcode9",
    "description" : "",
    "blender" : (2, 80, 0),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

import bpy
import time, sys
from bpy.props import *

from . import auto_load

auto_load.init()

def register():
    auto_load.register()

def unregister():
    auto_load.unregister()


def update_progress(job_title, progress):
    length = 20  # modify this to change the length
    block = int(round(length * progress))
    msg = "\r{0}: [{1}] {2}%".format(job_title, "#" * block + "-" * (length - block), round(progress * 100, 2))
    if progress >= 1: msg += " DONE\r\n"
    sys.stdout.write(msg)
    sys.stdout.flush()


def initSceneProperties(scn):
    bpy.types.Scene.namePartInclude = StringProperty(name="Select by part of name")

    return


initSceneProperties(bpy.context.scene)


def selectChildrenRecursive(obj):
    childNum = len(obj.children)

    if childNum > 0:
        for i in range(0, childNum):
            obj.children[i].select = True
            selectChildrenRecursive(obj.children[i])


class ToolsPanel(bpy.types.Panel):
    bl_label = "Select Mesh Objects"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        layout.prop(scn, 'namePartInclude')
        layout.operator("select.meshobjects")
        layout.operator("smartuv.selected")


class OBJECT_OT_SelectMeshObject(bpy.types.Operator):
    bl_idname = "select.meshobjects"
    bl_label = "Select"
    name = "selectmeshobjects"

    def execute(self, context):
        ctx = bpy.context
        scn = context.scene
        nameIncl = scn.namePartInclude
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


class OBJECT_OT_SmartUVSelected(bpy.types.Operator):
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


bpy.utils.register_module(__name__)
