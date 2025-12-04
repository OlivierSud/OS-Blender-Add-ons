import bpy

# Dictionnaire global pour stocker les connexions
stored_connections = {}
# Variable globale pour stocker le matériau à éditer
material_to_edit = None

bl_info = {
    "name": "Toggle Material Output Connection",
    "blender": (5, 0, 0),  # Assurez-vous que cette version correspond à la version de Blender que vous utilisez
    "category": "Material",
    "description": "Toggle connection between Material Output and shaders",
    "author": "Olivier with Chat GPT",
    "location": "Outliner > Header > button |Show UV Maps|",
    "doc_url": "https://oliviersudermann.wixsite.com/olivier-sudermann",
    "Version": "1.0.0",
}

class MaterialOutputMenuOperator(bpy.types.Operator):
    bl_idname = "material.output_menu"
    bl_label = "Material Output Menu"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        def draw_menu(self, context):
            layout = self.layout
            layout.operator("material.disconnect_all", text="Disconnect All Shaders", icon='UNLINKED')
            layout.operator("material.reconnect_all", text="Connect All Shaders", icon='LINKED')
        
        bpy.context.window_manager.popup_menu(draw_menu, title="Material Output", icon='MATERIAL')
        return {'FINISHED'}

class DisconnectAllMaterialOutputOperator(bpy.types.Operator):
    bl_idname = "material.disconnect_all"
    bl_label = "Disconnect All Material Outputs"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        global stored_connections
        
        disconnect_count = 0
        
        # Pour chaque matériau
        for mat in bpy.data.materials:
            if not mat.use_nodes:
                continue
            
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            
            # Trouver le Material Output node
            material_output = None
            for node in nodes:
                if node.type == 'OUTPUT_MATERIAL':
                    material_output = node
                    break
            
            if not material_output:
                continue
            
            # Vérifier si le Material Output est connecté
            input_surface = material_output.inputs.get('Surface')
            is_connected = input_surface and input_surface.is_linked
            
            if is_connected:
                # Récupérer les liens avant de les supprimer
                links_to_remove = [link for link in links if link.to_node == material_output and link.to_socket.name == 'Surface']
                for link in links_to_remove:
                    from_node = link.from_node.name
                    from_socket = link.from_socket.name
                    stored_connections[mat.name] = (from_node, from_socket)
                    links.remove(link)
                    disconnect_count += 1
        
        self.report({'INFO'}, f"{disconnect_count} link(s) disconnected")
        return {'FINISHED'}


class ReconnectAllMaterialOutputOperator(bpy.types.Operator):
    bl_idname = "material.reconnect_all"
    bl_label = "Reconnect All Material Outputs"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        global stored_connections
        
        reconnect_count = 0
        
        # Pour chaque matériau
        for mat in bpy.data.materials:
            if not mat.use_nodes:
                continue
            
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            
            # Trouver le Material Output node
            material_output = None
            for node in nodes:
                if node.type == 'OUTPUT_MATERIAL':
                    material_output = node
                    break
            
            if not material_output:
                continue
            
            to_socket = material_output.inputs.get('Surface')
            if not to_socket:
                continue
            
            # D'abord, utiliser la connexion stockée si elle existe
            if mat.name in stored_connections:
                from_node_name, from_socket_name = stored_connections[mat.name]
                from_node = nodes.get(from_node_name)
                
                if from_node:
                    from_socket = from_node.outputs.get(from_socket_name)
                    if from_socket:
                        links.new(from_socket, to_socket)
                        reconnect_count += 1
                        del stored_connections[mat.name]
                        continue
            
            # Si pas de connexion stockée, chercher le premier shader connecté
            shader_node = None
            for node in nodes:
                if node.type in ('ShaderNodeBsdfPrincipled', 'ShaderNodeBsdfDiffuse', 'ShaderNodeBsdfGlossy', 
                                'ShaderNodeBsdfTransparent', 'ShaderNodeBsdfRefraction', 'ShaderNodeBsdfAnisotropic',
                                'ShaderNodeBsdfVelvet', 'ShaderNodeBsdfToon', 'ShaderNodeSubsurfaceScattering',
                                'ShaderNodeMixShader', 'ShaderNodeAddShader', 'ShaderNodeEmission'):
                    shader_node = node
                    break
            
            # Si aucun shader trouvé par type, chercher n'importe quel nœud avec une output Socket 'SHADER'
            if not shader_node:
                for node in nodes:
                    for output in node.outputs:
                        if output.type == 'SHADER':
                            shader_node = node
                            break
                    if shader_node:
                        break
            
            # Connecter le shader trouvé au Surface du Material Output
            if shader_node:
                # Chercher la première socket SHADER en output
                for socket in shader_node.outputs:
                    if socket.type == 'SHADER':
                        links.new(socket, to_socket)
                        reconnect_count += 1
                        break
        
        self.report({'INFO'}, f"{reconnect_count} link(s) reconnected")
        return {'FINISHED'}


def draw_func(self, context):
    if context.space_data.context == 'MATERIAL':
        layout = self.layout
        layout.operator("material.output_menu", text="Material Output", icon='MATERIAL')

def register():
    bpy.utils.register_class(MaterialOutputMenuOperator)
    bpy.utils.register_class(DisconnectAllMaterialOutputOperator)
    bpy.utils.register_class(ReconnectAllMaterialOutputOperator)
    bpy.types.PROPERTIES_HT_header.append(draw_func)

def unregister():
    bpy.utils.unregister_class(MaterialOutputMenuOperator)
    bpy.utils.unregister_class(DisconnectAllMaterialOutputOperator)
    bpy.utils.unregister_class(ReconnectAllMaterialOutputOperator)
    bpy.types.PROPERTIES_HT_header.remove(draw_func)

if __name__ == "__main__":
    register()
