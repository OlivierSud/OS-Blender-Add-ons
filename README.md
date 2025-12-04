# OS-Blender-Add-ons

Collection d'addons Blender pour améliorer votre workflow de modélisation, de gestion des matériaux et des UV maps.

## 📦 Installation

### Installation générale
1. Téléchargez le fichier `.py` de l'addon souhaité
2. Ouvrez Blender → **Edit** → **Preferences** → **Add-ons**
3. Cliquez sur **Install** et sélectionnez le fichier `.py`
4. Activez l'addon en cochant la case

---

## 🔌 Addons disponibles

### 1. Create Mesh Material Library
**Fichier:** `Addons/create_mesh_material_library.py`  
**Catégorie:** Add Mesh  
**Version Blender:** 2.80+

#### Description
Génère un mesh Suzanne (singe) à l'origine de la scène avec tous les matériaux existants du fichier Blender assignés par ordre alphabétique. Idéal pour créer une bibliothèque visuelle de vos matériaux.

#### Utilisation
1. **Accès:** `Shift + A` → **Mesh** → **Material Library** (situé juste en dessous de "Monkey")
2. Un mesh Suzanne est créé à la position (0, 0, 0)
3. Tous les matériaux du fichier sont collectés et triés alphabétiquement
4. Les matériaux sont assignés aux faces du mesh dans l'ordre alphabétique

#### Caractéristiques
- ✅ Mesh positionné à l'origine (0, 0, 0)
- ✅ Placement à la racine de la scène (pas de parent)
- ✅ Tri alphabétique automatique des matériaux
- ✅ Gestion des cas limites (pas de matériaux, plus de matériaux que de faces, etc.)
- ✅ Support de l'undo/redo

#### Notes
- Suzanne possède 500 faces
- Si vous avez plus de 500 matériaux, certains ne seront pas visibles
- Si vous avez moins de 500 matériaux, ils seront répétés en cycle

---

### 2. Toggle Material Output Connection
**Fichier:** `Addons/disable_nodes.py`  
**Catégorie:** Material  
**Version Blender:** 5.0+

#### Description
Permet de déconnecter et reconnecter rapidement tous les shaders des nœuds Material Output dans tous les matériaux du fichier. Utile pour désactiver temporairement le rendu des matériaux ou pour le baking.

#### Utilisation
1. **Accès:** **Properties** → **Material** → Header → Bouton **Material Output**
2. Un menu popup s'affiche avec deux options:
   - **Disconnect All Shaders** : Déconnecte tous les shaders des Material Output
   - **Connect All Shaders** : Reconnecte les shaders précédemment déconnectés

#### Caractéristiques
- ✅ Déconnexion/reconnexion globale de tous les matériaux
- ✅ Mémorisation des connexions pour une reconnexion précise
- ✅ Recherche automatique des shaders si pas de connexion mémorisée
- ✅ Compteur de liens déconnectés/reconnectés
- ✅ Support de l'undo/redo

#### Shaders supportés
- Principled BSDF, Diffuse BSDF, Glossy BSDF
- Transparent BSDF, Refraction BSDF, Anisotropic BSDF
- Velvet BSDF, Toon BSDF, Subsurface Scattering
- Mix Shader, Add Shader, Emission

---

### 3. Display Active UV Map
**Fichier:** `Addons/display_active_uv_map.py`  
**Catégorie:** Object  
**Version Blender:** 2.80+

#### Description
Affiche les UV maps actives de tous les objets mesh sélectionnés dans une fenêtre popup. Permet de visualiser et de changer rapidement l'UV map active pour plusieurs objets.

#### Utilisation
1. **Accès:** **Outliner** → Header → Bouton **Show UV Maps**
2. Sélectionnez un ou plusieurs objets mesh
3. Cliquez sur le bouton **Show UV Maps**
4. Une popup affiche tous les objets sélectionnés avec leurs UV maps
5. Cliquez sur une UV map pour la rendre active

#### Caractéristiques
- ✅ Affichage de toutes les UV maps des objets sélectionnés
- ✅ Changement rapide de l'UV map active
- ✅ Support de la sélection multiple
- ✅ Interface popup claire et organisée
- ✅ Icône GROUP_UVS pour identification rapide

#### Notes
- Fonctionne uniquement avec les objets de type MESH
- Affiche "No selected mesh objects" si aucun mesh n'est sélectionné

---

### 4. Nettoyeur de Matériaux Suffixés
**Fichier:** `Addons/remove_double_material.py`  
**Catégorie:** Material  
**Version Blender:** 4.0+

#### Description
Supprime automatiquement les suffixes (.001, .002, .003, etc.) des matériaux dupliqués et fusionne les doublons. Nettoie votre fichier Blender des matériaux redondants créés lors d'imports ou de duplications.

#### Utilisation
1. **Accès:** **Properties** → **Material** → Header → Bouton **Clean Mats**
2. L'addon analyse tous les objets et matériaux
3. Les matériaux avec suffixes sont remplacés par leur version de base
4. Les matériaux inutilisés avec suffixes sont supprimés

#### Caractéristiques
- ✅ Détection automatique des suffixes (.001, .002, etc.)
- ✅ Remplacement des matériaux dupliqués par leur version originale
- ✅ Suppression des matériaux inutilisés
- ✅ Messages de confirmation dans la console
- ✅ Support de l'undo/redo

#### Exemple
Avant :
- `Material.001` (utilisé sur Cube)
- `Material` (version originale)

Après :
- `Material` (utilisé sur Cube)
- `Material.001` supprimé

---

## 🛠️ Développement

### Structure du projet
```
OS-Blender-Add-ons/
├── Addons/
│   ├── create_mesh_material_library.py
│   ├── disable_nodes.py
│   ├── display_active_uv_map.py
│   └── remove_double_material.py
├── index.html
└── README.md
```

### Auteur
**Olivier Sudermann**  
Développé avec l'assistance de ChatGPT  
🌐 [Site web](https://oliviersudermann.wixsite.com/olivier-sudermann)

---

## 📝 Notes

- Tous les addons supportent l'undo/redo (Ctrl+Z)
- Les addons sont compatibles avec les versions récentes de Blender (2.80+)
- Testez toujours sur une copie de votre fichier avant utilisation en production

---

## 🐛 Support

Pour signaler un bug ou suggérer une amélioration, veuillez créer une issue sur le dépôt GitHub.

---

## 📄 Licence

Ces addons sont fournis tels quels, sans garantie. Utilisez-les à vos propres risques.