# ##### BEGIN LICENSE BLOCK #####
#
# This program is licensed under The MIT License:
# see LICENSE for the full license text
#
# ##### END LICENSE BLOCK #####

import os
import datetime
import math
import bpy
import mathutils

######################################################
# EXPORT MAIN FILES
######################################################


def export_prefab(file, shape_name, collision_type, decal_type, data_source):
    items = []

    items.append('//--- OBJECT WRITE BEGIN ---')
    items.append('$ThisPrefab = new SimGroup() {')
    items.append('  canSave = "1";')
    items.append('  canSaveDynamicFields = "1";')
    items.append('  groupPosition = "0 0 0";\n')

    for ob in data_source:

        # get euler
        object_euler = ob.rotation_euler.copy()

        # use transposed matrix, original one does not work
        matrix = object_euler.to_matrix().transposed()

        collision_type_name = "Not Set"
        if collision_type == "0":
            collision_type_name = "Collision Mesh"
        elif collision_type == "1":
            collision_type_name = "Visible Mesh"
        elif collision_type == "2":
            collision_type_name = "Visible Mesh Final"
        elif collision_type == "3":
            collision_type_name = "Bounds"
        elif collision_type == "4":
            collision_type_name = "None"

        decal_type_name = "Not Set"
        if decal_type == "0":
            decal_type_name = "Collision Mesh"
        elif decal_type == "1":
            decal_type_name = "Visible Mesh"
        elif decal_type == "2":
            decal_type_name = "Visible Mesh Final"
        elif decal_type == "3":
            decal_type_name = "Bounds"
        elif decal_type == "4":
            decal_type_name = "None"

        rotationMatrixString = '"' + str(matrix[0][0]) + ' ' + str(matrix[0][1]) + ' ' + str(matrix[0][2]) + ' ' + str(matrix[1][0]) + ' ' + str(
            matrix[1][1])+ ' ' + str(matrix[1][2]) + ' ' + str(matrix[2][0]) + ' ' + str(matrix[2][1]) + ' ' + str(matrix[2][2]) + '"'

        items.append(
            '  new TSStatic() {\n' +
            '    shapeName = "' + shape_name + '";\n' +
            '    position = "' + str(ob.location[0]) + ' ' + str(ob.location[1]) + ' ' + str(ob.location[2]) + '";\n' +
            '    rotationMatrix = ' + rotationMatrixString + ';\n' +
            '    scale = "' + str(ob.scale[0]) + ' ' + str(ob.scale[1]) + ' ' + str(ob.scale[2]) + '";\n' +
            '    decalType = "' + decal_type_name + '";\n' +
            '    collisionType = "' + collision_type_name + '";\n' +
            '  };\n'
        )

    items.append('};')
    items.append('//--- OBJECT WRITE END ---')

    # write to file
    file.write("\n".join(items))
    file.close()
    return


######################################################
# EXPORT
######################################################
def save_prefab(filepath,
                shape_name,
                collision_type,
                decal_type,
                selection_only,
                context):

    print("exporting prefab: %r..." % (filepath))

    time1 = datetime.datetime.now()

    # get data source
    data_source = bpy.data.objects
    if selection_only:
        data_source = bpy.context.selected_objects

    # write prefab
    file = open(filepath, 'w')
    export_prefab(file, shape_name, collision_type, decal_type, data_source)

    # prefab export complete
    print(" done in %.4f sec." % (datetime.datetime.now() - time1).total_seconds())


def save(operator,
         context,
         filepath="",
         shape_name="none",
         collision_type="0",
         decal_type="1",
         selection_only=False
         ):

    # check item length
    if len(shape_name) == 0:
        shape_name = "No shape path set"

    # save prefab
    save_prefab(filepath,
                shape_name,
                collision_type,
                decal_type,
                selection_only,
                context,
                )

    return {'FINISHED'}
