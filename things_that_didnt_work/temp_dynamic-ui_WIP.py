import maya.cmds as cmds


def create_ui():
    window_name = "dynamic_ui_example"
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)

    cmds.window(window_name, title="Dynamic UI Example", sizeable=True)

    main_layout = cmds.columnLayout(adjustableColumn=True)

    # Create the optionMenuGrp with a set width
    shape_option_menu = cmds.optionMenuGrp(label="Shape", width=150)
    cmds.menuItem(label="Cube")
    cmds.menuItem(label="Sphere")
    cmds.menuItem(label="Cylinder")

    # Create the floatField for width, but don't show it yet
    ffg = cmds.floatFieldGrp(label="Width", numberOfFields=1, visible=False)
    print("FFG", ffg)
    # add custom attribute to ffg
    cmds.addAttr(ffg, longName="t_ID", dataType="string")
    # set value of the custom attribute
    cmds.setAttr(ffg + ".t_ID", "width_field", type="string")

    print("width_field: ", ffg)

    cmds.separator(height=20, style="none")

    # Add a button to print the selected shape and width
    cmds.button(label="Terrainify", command=on_submit)

    cmds.showWindow(window_name)

    # Set up a callback to show/hide the width field based on the selected shape
    cmds.optionMenuGrp(shape_option_menu, edit=True, changeCommand=on_shape_change)


def on_shape_change(shape):
    width_field = "width_field"
    found_float_field_grp = cmds.ls("*.%s" % "width_field", type="floatFieldGrp")[0]
    if shape == "Cube":
        cmds.showControl(found_float_field_grp)
        # cmds.floatFieldGrp(width_field, edit=True, visible=True)
    else:
        cmds.floatFieldGrp(width_field, edit=True, visible=False)


def on_submit(*args):
    shape = cmds.optionMenuGrp("shape_option_menu", query=True, value=True)
    width = cmds.floatFieldGrp("width_field", query=True, value1=True)
    print("Shape:", shape, "Width:", width)
