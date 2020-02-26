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

# Read tree from xml file
def fileRead(fileName):
    file = open(fileName, "r")
    tree = pyElementTree.parse(file)
    file.close()
    return tree

# Write xml string to file
def fileWrite(data, fileName):
    prettyData = prettify_minidom(data)
    file = open(fileName, "wb")
    file.write(bytes(prettyData, "utf-8"))
    file.close()

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