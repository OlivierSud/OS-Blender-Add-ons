bl_info = {
    "name": "Display Active UV Map",
    "blender": (2, 80, 0),
    "category": "Object",
    "description": "Display active UV map in a pop up list",
    "author": "Olivier with Chat GPT",
    "location": "Outliner > Header > button |Show UV Maps|",
    "doc_url": "https://oliviersudermann.wixsite.com/olivier-sudermann",
    "Version": "1.0.0",
}

import bpy

# Propriété de scène pour activer/désactiver l'affichage du nom de la carte UV
def update_uv_map_display(self, context):
    for area in bpy.context.screen.areas:
        if area.type == 'OUTLINER':
            area.tag_redraw()

bpy.types.Scene.show_uv_map_name = bpy.props.BoolProperty(
    name="Show UV Map Name",
    description="Display active UV map name next to the mesh name",
    default=True,
    update=update_uv_map_display,
)

class OUTLINER_OT_show_uv_maps(bpy.types.Operator):
    bl_idname = "outliner.show_uv_maps"
    bl_label = "Show UV Maps"

    def execute(self, context):
        return context.window_manager.invoke_popup(self, width=400)

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        if scene.show_uv_map_name:
            selected_objects = [obj for obj in scene.objects if obj.select_get() and obj.type == 'MESH']
            if not selected_objects:
                layout.label(text="No selected mesh objects")
            for obj in selected_objects:
                layout.label(text=obj.name)
                row = layout.row()
                if obj.data.uv_layers:
                    for uv_map in obj.data.uv_layers:
                        row.prop(uv_map, "active", text=uv_map.name)

def draw_header(self, context):
    layout = self.layout
    row = layout.row(align=True)
    row.label(text="", icon='NONE')  # Spacer to push items to the left
    row.operator(OUTLINER_OT_show_uv_maps.bl_idname, icon='GROUP_UVS', text="Show UV Maps")
    row.label(text="        ", icon='NONE')  # Spacer to push items to the right

def register():
    bpy.utils.register_class(OUTLINER_OT_show_uv_maps)
    bpy.types.OUTLINER_HT_header.append(draw_header)
    bpy.types.Scene.show_uv_map_name = bpy.props.BoolProperty(
        name="Show UV Map Name",
        description="Display active UV map name next to the mesh name",
        default=True,
        update=update_uv_map_display,
    )

def unregister():
    bpy.utils.unregister_class(OUTLINER_OT_show_uv_maps)
    bpy.types.OUTLINER_HT_header.remove(draw_header)
    del bpy.types.Scene.show_uv_map_name

if __name__ == "__main__":
    register()
