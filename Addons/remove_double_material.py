bl_info = {
    "name": "Nettoyeur de matériaux suffixés",
    "author": "Ton Nom",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "Properties > Material > Header",
    "description": "Supprime les suffixes (.001, .002...) des matériaux et fusionne les doublons",
    "category": "Material",
}

import bpy
import re

# --- Ton script ---
def nettoyer_materials(context):
    def strip_suffix(name):
        return re.sub(r"\.\d{3}$", "", name)

    for obj in bpy.data.objects:
        if not obj.data or not hasattr(obj.data, "materials"):
            continue
        for i, mat in enumerate(obj.data.materials):
            if mat is None:
                continue
            base_name = strip_suffix(mat.name)
            if base_name in bpy.data.materials and mat.name != base_name:
                print(f"Remplace {mat.name} par {base_name} sur {obj.name}")
                obj.data.materials[i] = bpy.data.materials[base_name]

    for mat in list(bpy.data.materials):
        if re.search(r"\.\d{3}$", mat.name) and mat.users == 0:
            print(f"Supprime {mat.name}")
            bpy.data.materials.remove(mat)


# --- Opérateur ---
class MATERIAL_OT_clean_suffix(bpy.types.Operator):
    bl_idname = "material.clean_suffix"
    bl_label = "Nettoyer les matériaux"
    bl_description = "Supprime les suffixes inutiles (.001, .002...) et fusionne les doublons"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        nettoyer_materials(context)
        self.report({'INFO'}, "Nettoyage des matériaux terminé")
        return {"FINISHED"}


# --- Bouton dans le header (à côté de celui de Toggle Use Nodes) ---
def draw_clean_button(self, context):
    if context.space_data.context == 'MATERIAL':
        layout = self.layout
        layout.operator("material.clean_suffix", text="Clean Mats", icon="BRUSH_DATA")


def register():
    bpy.utils.register_class(MATERIAL_OT_clean_suffix)
    bpy.types.PROPERTIES_HT_header.append(draw_clean_button)


def unregister():
    bpy.types.PROPERTIES_HT_header.remove(draw_clean_button)
    bpy.utils.unregister_class(MATERIAL_OT_clean_suffix)


if __name__ == "__main__":
    register()
