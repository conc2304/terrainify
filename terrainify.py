import maya.cmds as cmds
import sys

import constants
import materials
import utils as _
from bpm import BPM_Service
import importlib
from typing import Type, List


importlib.reload(materials)
from materials import Material_Creator


poly_shapes_list = constants.polyShapesList


class Terrainifier:
    def __init__(self):
        self.window_ID = "terrainify_window"
        self.error_window_ID = "terrainify_error_window"
        self.success_window_ID = "terrainify_success_window"
        self.default_dropdown_value = "-- Select A Shape To Start With --"
        self.ui_errors: List[str] = []
        self.bpm_service: Type[BPM_Service]
        self.material_creator: Type[Material_Creator]
        self.form_values = {}

    def create_UI(self):
        if cmds.window(self.window_ID, exists=True):
            cmds.deleteUI(self.window_ID)

        cmds.window(
            self.window_ID, title="Terrainify", widthHeight=(300, 100), sizeable=True
        )

        main_layout = cmds.columnLayout(adjustableColumn=True)

        cmds.separator(h=20)
        cmds.text(l="Build Generative Terrains Quickly", fn="boldLabelFont")
        cmds.text(
            "Choose a a shape to create and then displacement will be added to it."
        )
        cmds.separator(h=20)

        # Create the optionMenuGrp with a set width
        object_type_ui_id = "object_type"
        shape_option_menu = cmds.optionMenuGrp(
            object_type_ui_id,
            l="Shape: ",
        )

        cmds.menuItem(l=self.default_dropdown_value)
        cmds.menuItem(l="Selected Object(s)")
        for item in poly_shapes_list:
            if item["label"] != "Plane":
                continue
            cmds.menuItem(l=item["label"])

        # Create a label for width and height (Plane)
        width_id = "width_field_ty"
        height_id = "height_field_ty"
        bpm_id = "bpm_field_ty"
        bars_id = "bars_field_ty"

        width_field = cmds.intSliderGrp(
            width_id, l="Width: ", min=1, max=100, value=20, field=True
        )
        # This is actually the height value of the plane, but as a user Length makes more sense
        height_field = cmds.intSliderGrp(
            height_id, l="Length: ", min=1, max=100, value=20, field=True
        )

        cmds.separator(h=20)

        # Terrain Coloring
        cmds.text("Color Map the Terrain by Elevation")

        color_high_id = "color_high_id"
        color_high_field = cmds.colorSliderGrp(
            color_high_id,
            l="High: ",
            rgb=(0.779, 0.7795, 0.779),
        )

        color_mid_high_id = "color_mid_high"
        color_mid_high_field = cmds.colorSliderGrp(
            color_mid_high_id,
            l="Mid high: ",
            rgb=(0.193, 0.132, 0.087),
        )

        color_mid_low_id = "color_mid_low"
        color_mid_low_field = cmds.colorSliderGrp(
            color_mid_low_id,
            l="Mid Low: ",
            rgb=(0.121, 0.2375, 0.121),
        )

        color_low_id = "color_low_id"
        color_low__field = cmds.colorSliderGrp(
            color_low_id,
            l="Low: ",
            rgb=(0.0, 0.135, 0.436),
        )

        cmds.separator(h=20)

        # Animation Settings
        cmds.text("Animation Settings")

        bpm_field = cmds.intSliderGrp(
            bpm_id, l="BPM: ", min=1, max=250, value=120, field=True
        )
        bar_field = cmds.intSliderGrp(
            bars_id,
            l="Total Bars to Loop: ",
            min=1,
            max=128,
            value=12,
            field=True,
        )
        movement_field_id = "movement_loops"
        movement_field = cmds.intSliderGrp(
            movement_field_id,
            l="Terrain Movement Loops",
            field=True,
            step=2,
            min=0,
            max=32,
            value=2,
        )
        cmds.separator(h=20)

        cmds.text("Custom Material Name")
        material_name_field_id = "material_name_ty"
        material_name_field = cmds.textField(material_name_field_id)

        cmds.separator(h=20)

        # Add a button to print the selected shape and width
        # Pass in our form field values to the on_submit handler

        submit_button = cmds.button(
            l="Terrainify",
            command=lambda *args: self.on_submit(
                **{
                    "selected_objects": self.get_selected_objects()
                    if (
                        cmds.optionMenuGrp(object_type_ui_id, query=True, value=True)
                        == "Selected Object(s)"
                    )
                    else [],
                    "material_name": cmds.textField(
                        material_name_field_id, query=True, text=True
                    ),
                    object_type_ui_id: cmds.optionMenuGrp(
                        object_type_ui_id, query=True, value=True
                    ),
                    "dimensions": {
                        "width": cmds.intSliderGrp(width_id, query=True, value=True),
                        "height": cmds.intSliderGrp(height_id, query=True, value=True),
                    },
                    "audio": {
                        "bpm": cmds.intSliderGrp(bpm_id, query=True, value=True),
                        "num_bars": cmds.intSliderGrp(bars_id, query=True, value=True),
                        "num_terrain_loops": cmds.intSliderGrp(
                            movement_field_id, query=True, value=True
                        ),
                    },
                    "colors": {
                        "high": cmds.colorSliderGrp(
                            color_high_id, query=True, rgbValue=True
                        ),
                        "mid_high": cmds.colorSliderGrp(
                            color_mid_high_id, query=True, rgbValue=True
                        ),
                        "mid_low": cmds.colorSliderGrp(
                            color_mid_low_id, query=True, rgbValue=True
                        ),
                        "low": cmds.colorSliderGrp(
                            color_low_id, query=True, rgbValue=True
                        ),
                    },
                }
            ),
        )

        cmds.showWindow(self.window_ID)

    def show_success_window(self):
        print("Show Success Window")

        if cmds.window(self.success_window_ID, exists=True):
            cmds.deleteUI(self.success_window_ID)

        # Display the new pop up where our current window is
        current_window_position = cmds.windowPref(
            self.window_ID, q=True, topLeftCorner=True
        )
        x = current_window_position[0]
        y = current_window_position[1]

        print(f"X: {x}, Y: {y}")
        cmds.window(
            self.success_window_ID,
            title="Successful Terrainification!",
            widthHeight=(300, 100),
            sizeable=True,
            topLeftCorner=[x + 10, y + 10],
        )

        # Success Notes
        cmds.columnLayout(adjustableColumn=True)

        cmds.text(l="", height=10)
        cmds.text("Terrainification Complete!", fn="boldLabelFont")
        cmds.text(l="", height=5)

        cmds.text("Here are some useful stats from this run.")

        cmds.text(l="", height=20)
        cmds.text("** NOTE **")
        cmds.text("To view the results you will need view it through the renderView")
        cmds.text("You will also need to have lights in your scene")
        cmds.separator(h=20)

        cmds.text(l="", height=20)

        # Display Relevant Stats
        # Animation Stats
        # bpm_val = *args, **kwargs

        form_values = self.form_values
        print("form_values")
        print(form_values)
        audio_values = form_values.get("audio")
        bpm = audio_values.get("bpm")
        num_bars = audio_values.get("num_bars")
        loops = audio_values.get("num_terrain_loops")

        frame_range = self.bpm_service.get_animation_frame_range(bpm, num_bars)
        animation_stats = {
            "Start Frame": frame_range["start"],
            "End Frame": frame_range["end"],
            "Total Frames": frame_range["total"],
            "Bars": num_bars,
            "BPM": bpm,
            "Terrain Loops": loops,
        }
        # Animated Items
        animated_nodes = {
            "Displacement Shader ['scale']": self.material_creator.displacement_shader,
            "3D Placement ['rotation']": self.material_creator.placement,
        }
        # Materials Created
        material_stats = {
            "Material": self.material_creator.material,
            "Shading Group": self.material_creator.shading_group,
            "3D Placement": self.material_creator.placement,
            "Volume Noise": self.material_creator.volume_noise,
            "Displacement Shader": self.material_creator.displacement_shader,
            "Ramp": self.material_creator.ramp,
        }

        data = {
            "Animation": animation_stats,
            "Animated Items": animated_nodes,
            "Materials Created": material_stats,
        }

        # Loop over all of our data and display them as a individual tables
        for title, data in data.items():
            self.dispay_data_table(data, title)
            cmds.text(l="", height=20)

        cmds.text(l="", height=40)

        close_button = cmds.button(
            l="OK", command=lambda *args: self.on_success_close()
        )
        cmds.showWindow(self.success_window_ID)

    def dispay_data_table(self, data={}, title=""):
        # Create a row layout with two columns

        cmds.text(l=title, h=20, fn="boldLabelFont")
        row_layout = cmds.rowLayout(numberOfColumns=2, columnWidth2=[150, 150])

        # Create a column layout for the first column
        col1_layout = cmds.columnLayout()

        # Add keys to the first column
        for key in data.keys():
            cmds.text(l=key, fn="boldLabelFont")

        # End the first column layout
        cmds.setParent("..")

        # Create a column layout for the second column
        col2_layout = cmds.columnLayout()

        # Add values to the second column
        for value in data.values():
            cmds.text(l=value, fn="plainLabelFont")

        # End the second column layout
        cmds.setParent("..")

        # End the row layout
        cmds.setParent("..")

    def show_error_window(self):
        print("Show Error Window")

        if cmds.window(self.error_window_ID, exists=True):
            cmds.deleteUI(self.error_window_ID)

        # Display the new pop up where our current window is
        current_window_position = cmds.windowPref(
            self.window_ID, q=True, topLeftCorner=True
        )
        x = current_window_position[0]
        y = current_window_position[1]

        print(f"X: {x}, Y: {y}")
        cmds.window(
            self.error_window_ID,
            title="Woops something went wrong",
            widthHeight=(300, 100),
            sizeable=True,
            topLeftCorner=[x + 10, y + 10],
        )

        cmds.columnLayout(adjustableColumn=True)
        num_errors = len(self.ui_errors)
        suffix = "s" if num_errors > 1 else ""
        cmds.text(l="", h=20)
        cmds.text(f"{num_errors} Error{suffix}")
        cmds.text(l="", h=10)
        # Loop over all of the collected errors and display them
        for error in self.ui_errors:
            cmds.text(error)

        cmds.text(l="", height=20)

        close_button = cmds.button(l="OK", command=lambda *args: self.on_error_close())
        cmds.showWindow(self.error_window_ID)

    def on_error_close(self):
        # Close the error window and reset the errors
        cmds.deleteUI(self.error_window_ID)
        self.ui_errors = []

    def on_success_close(self):
        # Close the success window and reset the errors
        cmds.deleteUI(self.success_window_ID)
        self.ui_errors = []
        self.form_values = {}

    def on_submit(self, **kwargs):
        print("On Submit")
        print(kwargs)

        self.form_values = kwargs

        # Handle Validations and raise an error if we don't have what we need to proceed
        selected_object = kwargs.get("object_type")
        if selected_object == self.default_dropdown_value:
            self.ui_errors.append("No Object/Shape Selected")
            print(f"No Object Selected")
            self.show_error_window()
            sys.exit()

        # Create and get the created object
        object = self.create_object_with_material(**kwargs)

        print("Object")
        print(object)

        # Leave window open if we have no object
        if object:
            cmds.deleteUI(self.window_ID)
            self.show_success_window()
        # Show error modal if we have an error
        if len(self.ui_errors) > 0:
            self.show_error_window()

    def create_object_with_material(self, **kwargs):
        selected_object = kwargs.get("object_type")

        dimensions = kwargs.get("dimensions")
        print("Create Object", selected_object)
        print("Dimensions: ", dimensions)

        name_cleaned = _.string_to_slug(kwargs.get("material_name"))
        print(name_cleaned)

        # Add more subdivisions so that we have more detail
        args = {
            "subdivisionsX": dimensions.get("width") * 3,
            "subdivisionsY": dimensions.get("height") * 3,
            **dimensions,
        }

        # Create a new material creator instance with a custom color
        self.material_creator = Material_Creator(name=name_cleaned)

        # TODO - pass in shader settings from form
        self.material_creator.create_shader()

        # TODO at somepoint we should get these values from from the ui instead of our hardcoded values
        volume_attrs = constants.volume_noise_values

        # TODO Fun Acid mode with HSV Color Noise on the Ramp Node

        colors = kwargs.get("colors")
        self.material_creator.set_volume_attrs(volume_attrs)
        self.material_creator.set_ramp_values(**colors)

        # Create and/or assign the material to selected polygons
        self.bpm_service = BPM_Service()

        poly = None
        selected_polygons = []

        # TODO - This could use a refactor, but not mvp
        # Create poly and Assign material
        if selected_object != "Selected Object(s)":
            print("Is not selected objects")
            # Get the method to instantiate the selected shape and create a new primitive
            poly_creator = _.getObjectByKeyValueInList(
                poly_shapes_list, "label", selected_object
            )["cmd"]
            poly_to_terrainify = poly_creator(**args)

            poly = poly_to_terrainify[0]
            cmds.setAttr(f"{poly}.scaleX", 4)
            cmds.setAttr(f"{poly}.scaleY", 4)
            cmds.setAttr(f"{poly}.scaleZ", 4)
            print("poly_to_terrainify")
            print(poly_to_terrainify)
            # cmds.setAttr(f"{poly_to_terrainify[1]}.padding", 4)
            self.material_creator.assign_to_polygon(poly_to_terrainify)

            # UI Animation Values
            animation_values = kwargs.get("audio")
            bpm_value = animation_values.get("bpm") or 120.0
            bars_total = animation_values.get("num_bars") or 8
            loops_total = animation_values.get("num_terrain_loops") or 1

            # Animate the displacement (vertical pop)

            self.bpm_service.animate_object_on_downbeat(
                object_name=self.material_creator.displacement_shader,
                attribute_name="scale",
                bpm=bpm_value,
                num_bars=bars_total,
                beat_start_val=constants.displacement_init_scale * 2,
                beat_end_val=constants.displacement_init_scale * 1,
                anim_beat_length=1,
            )
            # Animate the movement of the terrain as a loop
            self.bpm_service.animate_rotation(
                object_name=self.material_creator.placement,
                attribute_name="rotateX",
                num_bars=bars_total,
                num_loops=loops_total,
                bpm=bpm_value,
            )

        else:
            print("Selected Objects Path")
            selected_objects = kwargs.get("selected_objects")
            print(selected_object)

            for obj in selected_objects:
                self.material_creator.assign_to_polygon(obj)

        # Focus the animations in the playback tray
        print("Handle ReFocusing")
        self.bpm_service.set_playback_options()

        # Select the things we animated along with our object
        objects_to_select = [
            self.material_creator.displacement_shader,
            self.material_creator.placement,
            *selected_polygons,
        ]
        if poly:
            objects_to_select.append(poly)

        # Select all key objects in the UI and return them
        cmds.select(objects_to_select, replace=True)
        return objects_to_select

    def get_selected_objects(self):
        print("List Selected")
        selected_objects = cmds.ls(selection=True, type="transform")
        selected_polygons = []
        for obj in selected_objects:
            shape = cmds.listRelatives(obj, shapes=True)[0]
            print(obj)
            print(shape)
            if cmds.nodeType(shape) == "mesh":
                selected_polygons.append(obj)
        print("SELECTED")
        print(selected_polygons)
        return selected_objects
