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

class AutoRootMotionOperator(bpy.types.Operator):
	bl_idname = "autorootmotion.run_operator"
	bl_label = "Run Auto Root Motion"
	bl_description = "Automatically add root bone and motion"
	bl_options = {"REGISTER"}

	def execute(self, context):
		return {"FINISHED"}

class AutoRootMotionPanel(bpy.types.Panel):
	bl_label = "Auto Root Motion"
	bl_idname = "AUTOROOTMOTION_PT_panel"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "AutoRootMotion"

	def draw(self, context):
		layout = self.layout
		layout.operator("autorootmotion.run_operator", text="Run Auto Root Motion")

def register():
	bpy.utils.register_class(AutoRootMotionOperator)
	bpy.utils.register_class(AutoRootMotionPanel)

def unregister():
	bpy.utils.unregister_class(AutoRootMotionOperator)
	bpy.utils.unregister_class(AutoRootMotionPanel)
