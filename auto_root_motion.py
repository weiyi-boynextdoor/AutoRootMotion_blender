import bpy
import bmesh
from mathutils import Vector, Matrix
import math

def add_root_bone():
	bpy.ops.object.mode_set(mode="OBJECT")
	armature_obj = bpy.context.active_object
	if not armature_obj or armature_obj.type != "ARMATURE":
		print("Please select an armature object")
		return False
	armature = armature_obj.data
	if len(armature.bones) == 0:
		print("No bones found in the armature")
		return False

	if armature.bones[0].name.lower() == "root":
		return True  # Root bone already exists

	# Enter Edit mode to add bones
	bpy.context.view_layer.objects.active = armature_obj
	bpy.ops.object.mode_set(mode="EDIT")

	# pelvis_names = ["Hips", "pelvis", "Pelvis", "mixamorig:Hips"]
	pelvis_bone = armature.edit_bones[0]

	# Create root bone
	root_bone = armature.edit_bones.new("root")
	root_bone.head = Vector((0, 0, 0))
	root_bone.tail = root_bone.head.copy()
	root_bone.tail.y += pelvis_bone.head.y * 0.5

	# Make pelvis a child of root
	pelvis_bone.parent = root_bone
	pelvis_bone.use_connect = False

	# After returning to object mode, the bones will be reordered and make root bone the first
	bpy.ops.object.mode_set(mode="OBJECT")


	# Switch to Pose mode for animation work
	# bpy.ops.object.mode_set(mode="POSE")

	# Process animations if they exist
	# if armature_obj.animation_data and armature_obj.animation_data.action:
	# 	process_animation_for_root_motion(armature_obj, pelvis_bone.name)

	# print("Root bone added successfully!")
	# return True

def process_animation_for_root_motion(armature_obj, pelvis_name):
	"""
	Transfers horizontal movement from pelvis to root bone
	while keeping pelvis vertical movement and rotations
	"""
	action = armature_obj.animation_data.action
	if not action:
		return

	print("Processing animation for root motion...")

	# Find pelvis location curves
	pelvis_loc_curves = {}
	root_loc_curves = {}

	for fcurve in action.fcurves:
		if fcurve.data_path == f'pose.bones["{pelvis_name}"].location':
			pelvis_loc_curves[fcurve.array_index] = fcurve

	if not pelvis_loc_curves:
		print("No location animation found on pelvis")
		return

	# Create location curves for root bone
	for axis in [0, 1]:  # X and Y axes only
		if axis in pelvis_loc_curves:
			# Create root bone location curve
			root_curve = action.fcurves.new('pose.bones["Root"].location', index=axis)
			root_loc_curves[axis] = root_curve

			# Copy keyframes from pelvis to root
			pelvis_curve = pelvis_loc_curves[axis]
			for keyframe in pelvis_curve.keyframe_points:
				root_curve.keyframe_points.insert(keyframe.co.x, keyframe.co.y)

			# Set interpolation mode
			for keyframe in root_curve.keyframe_points:
				keyframe.interpolation = "LINEAR"

			# Zero out horizontal movement on pelvis
			for keyframe in pelvis_curve.keyframe_points:
				keyframe.co.y = 0

	# Update the action
	action.fcurves.update()
	print("Animation processing complete!")

def batch_process_mixamo_files(directory_path):
	"""
	Batch process multiple Mixamo FBX files in a directory
	"""
	import os

	if not os.path.exists(directory_path):
		print(f"Directory not found: {directory_path}")
		return

	fbx_files = [f for f in os.listdir(directory_path) if f.lower().endswith(".fbx")]

	for fbx_file in fbx_files:
		print(f"\nProcessing: {fbx_file}")

		# Clear existing mesh objects
		bpy.ops.object.select_all(action="SELECT")
		bpy.ops.object.delete(use_global=True)

		# Import FBX
		filepath = os.path.join(directory_path, fbx_file)
		bpy.ops.import_scene.fbx(filepath=filepath)

		# Find and process armature
		armatures = [obj for obj in bpy.context.scene.objects if obj.type == "ARMATURE"]

		if armatures:
			bpy.context.view_layer.objects.active = armatures[0]
			armatures[0].select_set(True)

			# Add root bone
			if add_root_bone():
				# Export processed file
				output_path = os.path.join(directory_path, f"processed_{fbx_file}")
				bpy.ops.export_scene.fbx(
					filepath=output_path,
					use_selection=False,
					bake_anim=True,
					bake_anim_use_all_bones=True,
					bake_anim_use_nla_strips=False,
					bake_anim_use_all_actions=False
				)
				print(f"Exported: processed_{fbx_file}")

def create_ue5_compatible_skeleton():
	"""
	Creates a UE5-compatible skeleton setup with proper naming conventions
	"""
	armature_obj = bpy.context.active_object
	if not armature_obj or armature_obj.type != "ARMATURE":
		return False

	bpy.ops.object.mode_set(mode="EDIT")
	armature = armature_obj.data

	# UE5 expects specific bone names for mannequin compatibility
	bone_mapping = {
		"mixamorig:Hips": "pelvis",
		"mixamorig:Spine": "spine_01",
		"mixamorig:Spine1": "spine_02",
		"mixamorig:Spine2": "spine_03",
		"mixamorig:Neck": "neck_01",
		"mixamorig:Head": "head",
		"mixamorig:LeftShoulder": "clavicle_l",
		"mixamorig:LeftArm": "upperarm_l",
		"mixamorig:LeftForeArm": "lowerarm_l",
		"mixamorig:LeftHand": "hand_l",
		"mixamorig:RightShoulder": "clavicle_r",
		"mixamorig:RightArm": "upperarm_r",
		"mixamorig:RightForeArm": "lowerarm_r",
		"mixamorig:RightHand": "hand_r",
		"mixamorig:LeftUpLeg": "thigh_l",
		"mixamorig:LeftLeg": "calf_l",
		"mixamorig:LeftFoot": "foot_l",
		"mixamorig:RightUpLeg": "thigh_r",
		"mixamorig:RightLeg": "calf_r",
		"mixamorig:RightFoot": "foot_r"
	}

	# Rename bones
	for old_name, new_name in bone_mapping.items():
		if old_name in armature.edit_bones:
			armature.edit_bones[old_name].name = new_name

	bpy.ops.object.mode_set(mode="OBJECT")
	return True
