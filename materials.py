import maya.cmds as cmds
import uuid
import datetime
from typing import Tuple
import constants


class Material_Creator:
    def __init__(self, name=None, material_type="blinn"):
        print("Material Creator Init")
        self.id = self.get_new_uuid()
        self.material_type = material_type
        self.name = name if (name != None and name != "") else "Terrainify"
        print(self.name)
        self.material = None
        self.shading_group = None
        self.placement = None
        self.volume_noise = None
        self.displacement_shader = None
        self.ramp = None

        # Check if this material already exists
        if self.does_custom_material_exist():
            self.id = self.get_new_uuid()
            self.name = f"{self.id}"

    def generate_node_name(self, node_type):
        return f"{self.name}__{node_type}__{self.id}"

    def initialize_nodes(self):
        print("Initialize Nodes")
        # Create the shading nodes we need
        self.material = cmds.shadingNode(
            self.material_type, name=self.generate_node_name("material"), asShader=True
        )
        cmds.setAttr(f"{self.material}.reflectivity", 0.025)
        cmds.setAttr(f"{self.material}.specularRollOff", 0.156334)

        self.placement = cmds.shadingNode(
            "place3dTexture",
            name=self.generate_node_name("place3dTexture"),
            asUtility=True,
        )
        self.volume_noise = cmds.shadingNode(
            "volumeNoise", name=self.generate_node_name("volumeNoise"), asTexture=True
        )
        self.displacement_shader = cmds.shadingNode(
            "displacementShader",
            name=self.generate_node_name("displacementShader"),
            asShader=True,
        )
        # Create a the shadig group
        self.shading_group = cmds.sets(
            name=self.generate_node_name("shadingGroup"),
            empty=True,
            renderable=True,
            noSurfaceShader=True,
        )

        # Create a Ramp Node
        self.ramp = cmds.shadingNode(
            "ramp", name=self.generate_node_name("ramp"), asTexture=True
        )

        # Set the static Scale Attrs for the placement texture node
        # scale = 2.668
        scale = 7  #  TODO this is a value worth testing
        cmds.setAttr(f"{self.placement}.scaleX", scale)
        cmds.setAttr(f"{self.placement}.scaleY", scale)
        cmds.setAttr(f"{self.placement}.scaleZ", scale)

        #  TODO set this for animation
        cmds.setAttr(
            f"{self.displacement_shader}.scale", constants.displacement_init_scale
        )

    def set_volume_attrs(self, volume_attrs):
        print("Set Volume Attrs")
        print(volume_attrs)

        # Assign all of these attributes to the volumeNoise node
        default_attr = {  # must have
            "noiseType": 0,  # perlin noise
            "alphaIsLuminance": 1,
        }

        # TODO at somepoint we should get these values from from the ui instead of our hardcoded values
        for attr, value in volume_attrs.items():
            cmds.setAttr(f"{self.volume_noise}.{attr}", value)

        for attr, value in default_attr.items():
            cmds.setAttr(f"{self.volume_noise}.{attr}", value)

    def set_ramp_values(self, **color_values):
        print("Ramp Values")
        print(color_values)

        entry = "colorEntryList"

        # Get the color values for high, mid, low, and then apply them at the given positions

        low_rgb = color_values.get("low")
        cmds.setAttr(f"{self.ramp}.{entry}[0].color", *low_rgb, type="double3")
        cmds.setAttr(f"{self.ramp}.{entry}[0]position", 0)
        cmds.setAttr(f"{self.ramp}.{entry}[1].color", *low_rgb, type="double3")
        cmds.setAttr(f"{self.ramp}.{entry}[1]position", 0.05)

        mid_low_rgb = color_values.get("mid_low")
        cmds.setAttr(f"{self.ramp}.{entry}[2].color", *mid_low_rgb, type="double3")
        cmds.setAttr(f"{self.ramp}.{entry}[2]position", 0.05)

        cmds.setAttr(f"{self.ramp}.{entry}[3].color", *mid_low_rgb, type="double3")
        cmds.setAttr(f"{self.ramp}.{entry}[3]position", 0.25)

        mid_high_rgb = color_values.get("mid_high")
        cmds.setAttr(f"{self.ramp}.{entry}[4].color", *mid_high_rgb, type="double3")
        cmds.setAttr(f"{self.ramp}.{entry}[4]position", 0.75)

        high_rgb = color_values.get("high")
        cmds.setAttr(f"{self.ramp}.{entry}[5].color", *high_rgb, type="double3")
        cmds.setAttr(f"{self.ramp}.{entry}[5]position", 1)

    def connect_nodes(self):
        print("Connect Nodes")
        # TODO another good control is the displacement shader's scale attribute
        # Connect our material's outColor to the shading group's surfaceShader
        cmds.connectAttr(
            f"{self.material}.outColor",
            f"{self.shading_group}.surfaceShader",
            force=True,
        )

        # Connect the placementTexture nodes worldInverseMatrix attribe to the volumeNoise's placementMatrix attribute
        cmds.connectAttr(
            f"{self.placement}.worldInverseMatrix[0]",
            f"{self.volume_noise}.placementMatrix",
        )

        # Connect the volumeNoise outAlpha to the displacementShader's displacement
        cmds.connectAttr(
            f"{self.volume_noise}.outAlpha", f"{self.displacement_shader}.displacement"
        )

        # Connect the displacementShader to the shading group
        cmds.connectAttr(
            f"{self.displacement_shader}.displacement",
            f"{self.shading_group}.displacementShader",
        )

        # Connect our material to the ramp and the ramp to our color for color re-mapping
        cmds.connectAttr(f"{self.volume_noise}.outAlpha", f"{self.ramp}.uvCoord.vCoord")
        cmds.connectAttr(f"{self.ramp}.outColor", f"{self.material}.color")

    def create_shader(self):
        print("Create shader")
        self.initialize_nodes()
        self.connect_nodes()

    def assign_to_polygon(self, polygon):
        print("Assign Material")

        # Selected Objects come in as a string, but created polygons as an object
        # if it is a string use it as string, else get the first item of the object we want
        poly = polygon[0] if not isinstance(polygon, str) else polygon
        print(poly)
        # Assign the material to the selected polygon
        cmds.select(poly)  # ?? will this have to change depending on the type of poly
        cmds.sets(edit=True, forceElement=self.shading_group)
        cmds.select(clear=True)

    def does_custom_material_exist(self):
        # Look through all of the materials for material by name

        material_name = self.generate_node_name("material")
        print("existence check", material_name)
        for mat in cmds.ls(mat=True):
            print(mat)
        materials: bool = cmds.ls(material_name, mat=True)
        return materials

    def get_new_uuid(self):
        # UUID is long and not human friendly, try date instead
        # Get the current date and time
        now = datetime.datetime.now()

        # Format the date and time
        formatted_date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
        return formatted_date_time

        # Keeping around incase I change my mind and prefer to use uuid agin
        # Dashes and slashes break the parser for some reason
        # new_id = uuid.uuid4()
        # return str(uuid.uuid4()).replace("-", "_")
