# ##### BEGIN LICENSE BLOCK #####
#
# This program is licensed under The MIT License:
# see LICENSE for the full license text
#
# ##### END LICENSE BLOCK #####

bl_info = {
    "name": "BeamNG *.prefab TSStatic Exporter",
    "author": "BeamNG / dmn",
    "version": (0, 0, 2),
    "blender": (2, 77, 0),
    "location": "File > Export",
    "description": "Export prefab files",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.7/Py/"
                "Scripts/Import-Export/prefab",
    "support": 'COMMUNITY',
    "category": "Export"}

import bpy
from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    StringProperty,
    CollectionProperty,
)
from bpy_extras.io_utils import (
    ImportHelper,
    ExportHelper,
)


class ExportPrefab(bpy.types.Operator, ExportHelper):
    """Export to prefab file format (.prefab)"""
    bl_idname = "export_scene.prefab"
    bl_label = 'Export prefab'

    filename_ext = ".prefab"
    filter_glob = StringProperty(
        default="*.prefab",
        options={'HIDDEN'},
    )

    shape_name = StringProperty(
        name="Shape Path",
        description="This will be the exported mesh in the *.prefab file",
        default=""
    )

    selection_only = BoolProperty(
        name="Selection Only",
        description="Export only selected elements",
        default=True
    )

    collision_type = EnumProperty(
        name="Collision Type",
        description="Which collision type to use",
        items={
            ("0", "Collision Mesh", ""),
            ("1", "Visible Mesh", ""),
            ("2", "Visible Mesh Final", ""),
            ("3", "Bounds", ""),
            ("4", "None", ""),
        },
        default="0"
    )

    decal_type = EnumProperty(
        name="Decal Type",
        description="Which decal type to use",
        items={
            ("0", "Collision Mesh", ""),
            ("1", "Visible Mesh", ""),
            ("2", "Visible Mesh Final", ""),
            ("3", "Bounds", ""),
            ("4", "None", ""),
        },
        default="0"
    )

    def draw(self, context):
        layout = self.layout
        sub = layout.row()
        sub.prop(self, "shape_name")
        sub = layout.row()
        sub.prop(self, "collision_type")
        sub = layout.row()
        sub.prop(self, "decal_type")
        sub = layout.row()
        sub.prop(self, "selection_only")

    def execute(self, context):
        from . import export_prefab

        keywords = self.as_keywords(ignore=("axis_forward",
                                            "axis_up",
                                            "filter_glob",
                                            "check_existing",
                                            ))

        return export_prefab.save(self, context, **keywords)


# Add to a menu
def menu_func_export(self, context):
    self.layout.operator(ExportPrefab.bl_idname,
                         text="BeamNG prefab (*.prefab)")


def register():
    bpy.utils.register_module(__name__)

    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_module(__name__)

    bpy.types.INFO_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()
