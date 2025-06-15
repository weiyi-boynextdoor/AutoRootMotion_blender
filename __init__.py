import bpy
from . import auto_root_motion

bl_info = {
	"name": "Autorootmotion",
	"author": "weiyi",
	"description": "Automatically generate root bone and motion for biped character",
	"blender": (2, 80, 0),
	"version": (0, 0, 1),
	"location": "",
	"warning": "",
	"category": "Generic",
}

class AddRootOperator(bpy.types.Operator):
	bl_idname = "autorootmotion.add_root_operator"
	bl_label = "Add Root Bone"
	bl_description = "Automatically add root bone and motion"
	bl_options = {"REGISTER"}

	def execute(self, context):
		auto_root_motion.add_root_bone()
		return {"FINISHED"}

class AutoRootMotionPanel(bpy.types.Panel):
	bl_label = "Auto Root Motion"
	bl_idname = "AUTOROOTMOTION_PT_panel"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "AutoRootMotion"

	def draw(self, context):
		layout = self.layout
		layout.operator("autorootmotion.add_root_operator", text="Add Root Bone")

def register():
	bpy.utils.register_class(AddRootOperator)
	bpy.utils.register_class(AutoRootMotionPanel)

def unregister():
	bpy.utils.unregister_class(AddRootOperator)
	bpy.utils.unregister_class(AutoRootMotionPanel)
