import maya.cmds as cmds
import constants
import utils as _
import importlib

# importlib.reload(constants)
# importlib.reload(_)

poly_shapes_list = constants.polyShapesList
get_object_by_key_value_in_list = _.getObjectByKeyValueInList
window_ID = "terrainify_window"
form_layout = False


def create_object(selected_object):
    print("Creat Object", selected_object)

    poly_creator = get_object_by_key_value_in_list(
        poly_shapes_list, "label", selected_object
    )["cmd"]
    poly_to_terrainify = poly_creator()


def on_submit(**kwargs):
    print("on submit BANANA")
    print(kwargs)

    create_object(kwargs.get("object_type"))
    cmds.deleteUI(window_ID)


def create_UI():
    global form_layout
    # close any existing windows if they are open
    if cmds.window(window_ID, exists=True):
        cmds.deleteUI(window_ID)

    cmds.window(window_ID, title="Banana", widthHeight=(300, 100))
    # cmds.window(window_ID, title="Terrainify", sizeable=True)

    cmds.rowColumnLayout(
        numberOfColumns=1, columnWidth=[(1, 200)], columnOffset=[(1, "right", 5)]
    )

    object_type_ui_id = "object_type"
    option_menu = cmds.optionMenuGrp(
        object_type_ui_id,
        label="Shape: ",
        width=350,
        cc=lambda *args: update_UI(
            cmds.optionMenuGrp(option_menu, query=True, value=True)
        ),
    )

    cmds.menuItem(label="--Select A Shape To Start With--")
    for item in poly_shapes_list:
        if item["label"] != "Cube":
            continue
        cmds.menuItem(label=item["label"])

    form_layout = cmds.formLayout()
    print("form_layout2: ", form_layout)
    cmds.setParent("..")

    # collect all of the form fields and pass them in as args to the on submit handler
    kwargs = {}
    kwargs[object_type_ui_id] = cmds.optionMenuGrp(
        object_type_ui_id, query=True, value=True
    )

    cmds.button(
        label="Terrainify",
        command=lambda *args: on_submit(**kwargs),
    )

    cmds.showWindow(window_ID)


def update_UI(selected_shape):
    global form_layout
    print("update_UI: ", selected_shape)
    # Get the dimensions for the selected shape
    if selected_shape == "Sphere":
        dimensions = [("Radius", "float")]
    elif selected_shape == "Cube":
        dimensions = [("Width", "float"), ("Height", "float"), ("Depth", "float")]
    elif selected_shape == "Box":
        dimensions = [("Width", "float"), ("Height", "float"), ("Depth", "float")]
    elif selected_shape == "Cone":
        dimensions = [("Radius", "float"), ("Height", "float")]
    elif selected_shape == "Plane":
        dimensions = [("Width", "float"), ("Height", "float")]
    elif selected_shape == "Torus":
        dimensions = [("Inner Radius", "float"), ("Outer Radius", "float")]
    elif selected_shape == "Disc":
        dimensions = [("Radius", "float"), ("Inner Radius", "float")]
    else:
        dimensions = []

    # Clear the UI and create new form fields for the selected shape
    # Delete all child elements of the form layout
    print("Form Layout", form_layout)
    children = cmds.formLayout(form_layout, q=True, ca=True)
    print("Children:", children)
    if children:
        cmds.deleteUI(children)
    print("Children2:", children)

    for i, (label, data_type) in enumerate(dimensions):
        print("Dimensions")
        print(i, label, "-", data_type)
        field_name = label + "_field_" + str(i)
        cmds.text(label=label)

        if data_type == "float":
            cmds.floatField(
                field_name,
                value=10,
                minValue=10,
                maxValue=1000,
                precision=0,
                step=1,
            )
        else:
            cmds.intField(name=field_name, value=0)

        # cmds.formLayout(
        #     form_layout,
        #     edit=True,
        #     attachForm=[
        #         (label, "top", 5),
        #         (label, "left", 5),
        #         (field_name, "top", 5),
        #         (field_name, "right", 5),
        #     ],
        # )
        if i == 0:
            cmds.formLayout(
                form_layout, edit=True, attachControl=[(label, "right", 5, field_name)]
            )
