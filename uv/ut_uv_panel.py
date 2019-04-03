import bpy


class UT_PT_UVPanel(bpy.types.Panel):
    bl_label = "UV"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        layout.operator("smartuv.selected")