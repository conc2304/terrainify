

To Run Instructions:

Extract the script files:
Unzip the downloaded script files to access their contents.

Add script files to Maya:
There are two methods to add the script files to your Maya environment. You can either:

a. Copy the script files to your Maya scripts folder:
For Windows users, navigate to the following folder and paste the extracted script files:
C:\Users<YOUR_USER>\Documents\maya\2023\scripts

b. Update the Maya scripts file path:
If you prefer to run the scripts from a custom location, you can modify the init.py file to include the appropriate file path. In the init.py file, update the 'JosesPath' variable with the directory where the scripts are located on your computer (this has not been tested on macOS).

Example for Windows:
JosesPath = "C:\Users\josec\Documents\maya\2023\scripts\scripts"
sys.path.append(JosesPath)

Run the script in Maya:
Open Autodesk Maya and follow these steps to execute the script:

a. Open the Script Editor (Window > Script Editor).
b. Go to File > Open Script, and select the init.py file.
c. With the init.py file tab selected, click on the Play/Execute button in the Script Editor.

Upon successful execution, the Terrainify user interface will appear in Maya.


Introduction: The Terrainify Python script is designed to create and manipulate terrain elements in Autodesk Maya, using a custom shading network and animation keyframes based on user-defined parameters. This document provides an overview of the script's functionality and its various components.

Description:

1.) Terrain creation and material assignment:
Terrainify generates a polygonal terrain based on user-defined parameters or assigns materials/shading networks to selected meshes in Maya.

2.) Shading network components:
The script creates a custom shading network, including the following nodes:

- Shading group
- Material
- Displacement shader (converts 2D planes into 3D textures)
- VolumeNoise (produces a grayscale noise image for height mapping)
- Ramp (recolors the grayscale height map with specified colors)
- Placement3D (renders the 3D height map and controls terrain movement)
- BPM service (sets keyframes based on user-configured BPM parameters)
3.)Animation keyframes and functionality:
Terrainify animates the terrain using the following methods:

- Scales the displacement on the beat
- Moves the terrain continuously in a loop
- Sets all keyframe tangents to linear
Note: The BPM Service methods can be applied to any attribute you want to animate. Future plans include making the BPM Service a standalone shelf item for applying BPM-based animations to other elements.

4.) Playback timeline adjustments:
Upon completion, the script adjusts the playback timeline:

- Focuses the playback range between the start and end of the animation
- Sets the animation start and end times based on BPM parameters
-Selects the animated objects to display their keyframes immediately

5.) Error and Success windows:
The script includes error and success windows to inform users of any issues or successful operations.


Things that I would like to add or fix (but out of scope for this class):

- Build a dynamic UI window where selecting a different type of 3D Primitive will update the window to have the respective dimension fields displayed (currently hardcoded to plane dimensions). My initial thought is to close and reopen the window with the new layout anytime the user selects something that should update the UI. But that sounds like an ugly hacky solution and there certainly must be a better way to do this in Maya.
- I would like to find a way to loop the terrain slower but that may require a better way to loop the noise (currently just rotating the placement 3d along an axis once to cause a movement loop). My initial thoughts are to create 2 volumeNoise nodes and essentially crossfade in between them to simulate noise that loops.
- I would love to figure out how to add this to the shelf and run it from the shelf, but I don't see a good way of doing it with multiple files
- I would like to add preconfigured settings for different terrain types (mountains, deserts, tundras ...)
- I would like to add an animation debugging object, ie render a cube to preview the animations before render
- finetune the animations settings

