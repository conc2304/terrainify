import maya.cmds as cmds
import os
import sys

# Make sure that wherever we are running this file from in, is in the system paths
JosesPath = "C:\\Users\\josec\\Documents\\maya\\2023\\scripts\\scripts"
current_working_directory = os.getcwd()
print("CWD:  ", current_working_directory)
sys.path.append(JosesPath)


# Run the main script, and reload for Maya freshness
import importlib

import terrainify
import utils
import materials
import constants
import bpm


importlib.reload(terrainify)
importlib.reload(utils)
importlib.reload(materials)
importlib.reload(bpm)
importlib.reload(constants)

terrainify = terrainify.Terrainifier()
terrainify.create_UI()
