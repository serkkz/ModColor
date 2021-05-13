bl_info = {"name": "ModColor", 
           "description": "Developed for the Sci-Fantasy Tech Demo",
           "author": "Sergei Korotkov",
           "version": (0, 1),
           "blender": (2, 80, 0),
           "location": "UI", 
           "warning": "Alpha testing",
           "support": "COMMUNITY",
           "wiki_url": "https://github.com/serkkz/ModColor/wiki", 
           "tracker_url": "https://github.com/serkkz/ModColor/issues",
           "category": "Panda3D"}

import bpy

from bpy.props import IntProperty
from bpy.types import PropertyGroup

def update_rcolor(self, context):
    bpy.data.brushes["Draw"].color[0] = bpy.context.scene.modcolor.rcolor / 255

def update_gcolor(self, context):
    bpy.data.brushes["Draw"].color[1] = bpy.context.scene.modcolor.gcolor / 255

def update_bcolor(self, context):
    bpy.data.brushes["Draw"].color[2] = bpy.context.scene.modcolor.bcolor / 255

class Extended(PropertyGroup):
    rcolor : IntProperty(name="Integer", description="Enter an integer", default = 255, min = 0, max = 255, subtype='UNSIGNED', update = update_rcolor)
    gcolor : IntProperty(name="Integer", description="Enter an integer", default = 255, min = 0, max = 255, subtype='UNSIGNED', update = update_gcolor)
    bcolor : IntProperty(name="Integer", description="Enter an integer", default = 255, min = 0, max = 255, subtype='UNSIGNED', update = update_bcolor)
    acolor : IntProperty(name="Integer", description="Enter an integer", default = 255, min = 0, max = 255, subtype='UNSIGNED')

class ApplyСolor(bpy.types.Operator):
    bl_idname = "ui.apply_color"
    bl_label = "Apply_color"

    def execute(self, context):
        mesh = bpy.context.active_object.data
        index = set(v.index for v in mesh.vertices if v.select)
        for loop in mesh.loops:
            if loop.vertex_index in index:
                mesh.vertex_colors.active.data[loop.index].color = [bpy.context.scene.modcolor.rcolor / 255,
                                                                    bpy.context.scene.modcolor.gcolor / 255,
                                                                    bpy.context.scene.modcolor.bcolor / 255,
                                                                    bpy.context.scene.modcolor.acolor / 255]
        return {'FINISHED'}

class ModColor(bpy.types.Panel):
    bl_idname = "MODCOLOR_PT_Panel"
    bl_label = "ModColor"
    bl_category = "ModColor"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    @classmethod
    def poll(cls, context):
        return (bpy.context.object.mode == 'VERTEX_PAINT')

    def draw(self, context):
        layout = self.layout
        options = layout.box()
        mask = options.split()
        mask.prop(context.scene.modcolor, 'rcolor', text='R')
        mask.prop(context.scene.modcolor, 'gcolor', text='G')
        mask.prop(context.scene.modcolor, 'bcolor', text='B')
        mask.prop(context.scene.modcolor, 'acolor', text='A')

        layout.operator("ui.apply_color", text="Apply color")

classes = ( ModColor, Extended, ApplyСolor,)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.modcolor = bpy.props.PointerProperty(type = Extended)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.modcolor