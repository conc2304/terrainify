import re


def getObjectByKeyValueInList(list, key, value):
    for obj in list:
        if obj[key] == value:
            return obj
    return None


def string_to_slug(str):
    # Convert the string to lowercase
    str = str.lower()

    # Replace any non-alphanumeric characters with an underscore
    str = re.sub(r"[^a-z0-9]+", "_", str)

    # Remove consecutive hyphens or consecutive underscores
    str = re.sub(r"-{2,}", "_", str)
    str = re.sub(r"_{2,}", "_", str)

    # Remove hyphens or underscores from the start and end of the string
    str = str.strip("-")
    str = str.strip("_")

    # Materials can't start with numbers so add an underscore to the name
    if starts_with_number(str):
        str = "_" + str

    return str


def starts_with_number(str):
    if len(str) == 0:
        return False
    return str[0].isdigit()
