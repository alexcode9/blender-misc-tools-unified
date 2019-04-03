import bpy


class UT_PT_ToolsPanel(bpy.types.Panel):
    bl_label = "Select Mesh Objects"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        layout.prop(scn, 'namePartInclude')
        layout.operator("select.meshobjects")
        layout.operator("smartuv.selected")