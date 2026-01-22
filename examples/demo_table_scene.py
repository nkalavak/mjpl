# File to evaluate visualization of Panda arm/UR5 and a table with blocks. 

import sys

import mujoco
import mujoco.viewer

# Path to the scene XML file
# XML_PATH = "examples/models/franka_emika_panda/scene_franka_blocks_table.xml"
XML_PATH = "examples/models/universal_robots_ur5e/scene_ur5_blocks_table.xml"

def main():

    # Load model
    model = mujoco.MjModel.from_xml_path(XML_PATH)
    data = mujoco.MjData(model)

    # Launch viewer
    with mujoco.viewer.launch_passive(model, data, show_left_ui=False, show_right_ui=False) as viewer:
        print("Press ESC in the window to exit!")

        while viewer.is_running():
            mujoco.mj_step(model, data)
            viewer.sync()

    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)

