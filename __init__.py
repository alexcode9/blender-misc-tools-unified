'''
Created on 3 Jan 2017

@author: Alex
'''

bl_info = {
    "name" : "UnifiedTool",
    "author" : "Alexcode9",
    "description" : "",
    "blender" : (2, 80, 0),
    "location" : "View3D",
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

# def initSceneProperties(scn):
#     bpy.types.Scene.namePartInclude = StringProperty(name="Select by part of name")

#     return

# initSceneProperties(bpy.context.scene)


if __name__ == "__main__":
    register()
