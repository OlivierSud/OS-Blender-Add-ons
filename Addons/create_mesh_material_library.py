bl_info = {
    "name": "Create Mesh Material Library",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > Material Library",
    "description": "Creates a Suzanne mesh with all existing materials assigned alphabetically",
    "category": "Add Mesh",
}

import bpy
from bpy.types import Operator


class MESH_OT_create_material_library(Operator):
    """Create Suzanne mesh with all materials from the file"""
    bl_idname = "mesh.create_material_library"
    bl_label = "Material Library"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Create Suzanne mesh at origin
        bpy.ops.mesh.primitive_monkey_add(
            size=2,
            location=(0, 0, 0),
            rotation=(0, 0, 0)
        )
        
        # Get the newly created object
        obj = context.active_object
        
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "Failed to create mesh")
            return {'CANCELLED'}
        
        # Ensure we're at the root of the scene (no parent)
        obj.parent = None
        
        # Get all materials from the file and sort alphabetically
        all_materials = sorted(bpy.data.materials, key=lambda m: m.name)
        
        if not all_materials:
            self.report({'WARNING'}, "No materials found in the file")
            return {'FINISHED'}
        
        # Clear existing material slots
        obj.data.materials.clear()
        
        # Add all materials to the object
        for mat in all_materials:
            obj.data.materials.append(mat)
        
        # Switch to edit mode to assign materials to faces
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Get mesh data
        mesh = obj.data
        num_faces = len(mesh.polygons)
        num_materials = len(all_materials)
        
        # Assign materials to faces in alphabetical order
        for i, face in enumerate(mesh.polygons):
            # Cycle through materials if there are more faces than materials
            material_index = i % num_materials
            face.material_index = material_index
        
        # Return to object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        self.report({'INFO'}, f"Created Suzanne with {num_materials} materials assigned to {num_faces} faces")
        
        return {'FINISHED'}


def menu_func(self, context):
    """Add menu entry in Add > Mesh menu"""
    self.layout.separator()
    self.layout.operator(
        MESH_OT_create_material_library.bl_idname,
        text="Material Library",
        icon='MONKEY'
    )


def register():
    """Register addon"""
    bpy.utils.register_class(MESH_OT_create_material_library)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    """Unregister addon"""
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    bpy.utils.unregister_class(MESH_OT_create_material_library)


if __name__ == "__main__":
    register()
