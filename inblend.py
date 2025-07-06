# пример — слушатель сокета и обновление костей
import bpy, socket, json, threading, mathutils

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 5055))
sock.setblocking(False)

mapping = {
    11: "shoulder_L",
    12: "shoulder_R",
    13: "elbow_L",
    14: "elbow_R",
    15: "wrist_L",
    16: "wrist_R",
    23: "hip_L",
    24: "hip_R",
    25: "knee_L",
    26: "knee_R",
    27: "ankle_L",
    28: "ankle_R",
}

arm = bpy.data.objects['Armature']

def listen():
    while True:
        try:
            data, _ = sock.recvfrom(65535)
            pts = json.loads(data.decode())
            bpy.app.driver_namespace["pose_data"] = pts
        except:
            pass

threading.Thread(target=listen, daemon=True).start()

def apply_pose(scene):
    pts = bpy.app.driver_namespace.get("pose_data")
    if not pts:
        return
    for idx, bone_name in mapping.items():
        if idx < len(pts):
            lm = pts[idx]
            bone = arm.pose.bones.get(bone_name)
            if bone:
                bone.location = mathutils.Vector((lm['x'], lm['y'], -lm['z'])) * 2

bpy.app.handlers.frame_change_pre.clear()
bpy.app.handlers.frame_change_pre.append(apply_pose)