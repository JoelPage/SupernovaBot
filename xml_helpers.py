print("xml_helpers.py")
# Python
import datetime as pyDatetime
import xml.etree.ElementTree as pyElementTree
from xml.dom import minidom as pyMinidom
import re as pyRe
import sys as pySys

def get_node(parent, name):
    if parent != None:
        return parent.find(name)

def get_nodes(parent, name):
    if parent != None:
        return parent.findall(name)

def create_node(parent, name):
    return pyElementTree.SubElement(parent, name)

def create_node_if_exists(parent, name, value):
    if value != None:
        return create_node(parent, name)

def create_and_set_node_text(parent, name, value):
    node = pyElementTree.SubElement(parent, name)
    node.text = f"{value}"

def create_and_set_nodes_text(parent, name, values):
    for value in values:
        create_and_set_node_text(parent, name, value)

def create_and_set_node_text_if_exists(parent, name, value):
    if value != None:
        create_and_set_node_text(parent, name, value)

def create_and_set_node_text_int(parent, name, value):
    valueAsInt = int(value)
    create_and_set_node_text(parent, name, valueAsInt)

def create_and_set_node_text_int_if_exists(parent, name, value):
    if value != None:
        create_and_set_node_text_int(parent, name, value)

def create_and_set_node_text_bool(parent, name, value):
    text = "True" if value else "False"
    create_and_set_node_text(parent, name, text)

def create_and_set_node_text_float(parent, name, value):
    valueAsFloat = float(value)
    create_and_set_node_text(parent, name, valueAsFloat)

def get_value_text(node, name): 
    valueNode = node.find(name)
    if valueNode != None:
        return valueNode.text

def get_value_int(node, name):
    valueNode = node.find(name)
    print(valueNode)
    if valueNode != None:
        valueAsStr = valueNode.text
        return int(valueAsStr)

def get_value_float(node, name):
    valueNode = node.find(name)
    if valueNode != None:
        valueAsStr = valueNode.text
        return float(valueAsStr)

def get_value_datetime(node, name):
    valueNode = node.find(name)
    if valueNode != None:
        valueAsStr = valueNode.text
        valueAsInt = int(valueAsStr)
        return pyDatetime.datetime.fromtimestamp(valueAsInt)

def get_value_bool(node, name):
    valueNode = node.find(name)
    if valueNode != None:
        valueAsStr = valueNode.text
        return True if valueAsStr == "True" else False

def get_values_float(node, name, values):
    if node != None:
        for valueNode in node.findall("reminder"):
            valueAsStr = valueNode.text
            valueAsFloat = float(valueAsStr)
            values.append(valueAsFloat)

def set_attrib_text(node, name, value):
    node.set(name, f"{value}")

def set_attrib_text_if_exists(node, name, value):
    if node != None:
        set_attrib_text(node, name, f"{value}")

def set_attrib_text_int_bytes(node, name, value):
    valueAsBytes = value.encode('utf8')
    valueAsInt = int.from_bytes(valueAsBytes, pySys.byteorder)
    set_attrib_text(node, name, valueAsInt)

def get_attrib_text(node, name):
    if name in node.attrib.keys():
        return node.attrib[name]
     
def get_attrib_float(node, name):
    valueAsStr = get_attrib_text(node, name)
    if valueAsStr != None:
        return float(valueAsStr)

def get_attrib_int(node, name):
    valueAsStr = get_attrib_text(node, name)
    if valueAsStr != None:
        return int(valueAsStr)

def get_attrib_bytes(node, name, numBytes):
    valueAsInt = get_attrib_int(node, name)
    if valueAsInt != None:
        return valueAsInt.to_bytes(numBytes, pySys.byteorder)
        
def get_attrib_unicode(node, name):
    valueAsBytes = get_attrib_bytes(node, name, 3)
    if valueAsBytes != None:
        return valueAsBytes.decode('utf-8')

# https://stackoverflow.com/questions/24813872/creating-xml-documents-with-whitespace-with-xml-etree-celementtree
# Return a pretty-printed XML string for the Element.
# Tried this function before but it produced strange results so I just wrote my own.
def prettify_custom(tree):
    # Read out tree as bytes
    encoding = 'utf-8'
    treeAsBytes = pyElementTree.tostring(tree, encoding)
    # Convert to string
    treeAsString = str(treeAsBytes, encoding)
    # Remove new lines
    splitTree = treeAsString.split("\n")
    treeAsString = "".join(splitTree)
    # find all words enclosed by triangle braces
    # WARNING : This is a bit janky, if someone has a name that includes triangle braces
    # then this logic could break entirely.
    # It also fails when trying to add attributes
    split = pyRe.findall(r"<(.*?)\>", treeAsString)

    # Variables used for producing correct indentation.
    start = 0               # The index into the string we will start searching.
    depth = 0               # The depth of the indentation.
    indentation = "    "    # The spacing used for indentation.
    lastString = ""         # The previous element name.

    for string in split:
        # Apply braces to the string to avoid imperfect matches.
        strToFind = "<" + string + ">"
        # Find the index of this string from start to len(treeAsString)
        index = treeAsString.find(strToFind, start, len(treeAsString))
        # Set the start value past the string
        start = index + len(strToFind)

        # If this is a closing element reduce the depth by 1
        if string.startswith("/"):
            depth -= 1
            # If this element matches the last then perform the indentation
            if not lastString == string[1:]:
                # Split the strings from index, add a new line and indent, then join them together.
                treeAsString = treeAsString[:index] + "\n" + (indentation * depth) + treeAsString[index:]
                # Increase the start index by the length of the indentation
                start = start + len("\n") + len(indentation * depth)

            # Cache this string for the next loop
            lastString = string[1:]
        # If this is an opening element
        else:
            # and if this is not the first element
            if depth != 0:
                # Perform the indentation and increase the start index
                treeAsString = treeAsString[:index] + "\n" + (indentation * depth) + treeAsString[index:]
                start = start + len("\n") + len(indentation * depth)

            # Increase the depth and cache the string
            depth += 1
            lastString = string

    return treeAsString

def prettify_minidom(tree):
    # Read out tree as bytes
    encoding = 'utf-8'
    treeAsBytes = pyElementTree.tostring(tree, encoding)
    # Convert to string
    treeAsString = str(treeAsBytes, encoding)
    # Remove new lines
    splitTree = treeAsString.split("\n")
    # WARNING : removing \n could break strings that contain this.
    # maybe be more appropriate to use regex or something similar.
    treeAsString = "".join(splitTree)

    INDENT = "    "
    reparsed = pyMinidom.parseString(treeAsString)
    return reparsed.toprettyxml(indent=INDENT)

# Write xml string to file
def fileWrite(data, fileName):
    prettyData = prettify_minidom(data)
    file = open(fileName, "wb")

    file.write(bytes(prettyData, "utf-8"))

    file.close()
    
# Read tree from xml file
def fileRead(fileName):
    file = open(fileName, "r")
    tree = pyElementTree.parse(file)
    file.close()
    return tree