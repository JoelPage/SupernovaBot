import xml.etree.ElementTree as ET
from xml.dom import minidom
import re as i_re

def create_node(parent, name):
    return ET.SubElement(parent, name)

def create_node_if_exists(parent, name, value):
    if value != None:
        return create_node(parent, name)

def create_and_set_node_text(parent, name, value):
    node = ET.SubElement(parent, name)
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

def set_value_from_node_text(node, name, value):
    valueNode = node.find(name)
    value = valueNode.text

# https://stackoverflow.com/questions/24813872/creating-xml-documents-with-whitespace-with-xml-etree-celementtree
# Return a pretty-printed XML string for the Element.
# Tried this function before but it produced strange results so I just wrote my own.
def prettify_custom(tree):
    # Read out tree as bytes
    encoding = 'utf-8'
    treeAsBytes = ET.tostring(tree, encoding)
    # Convert to string
    treeAsString = str(treeAsBytes, encoding)
    # Remove new lines
    splitTree = treeAsString.split("\n")
    treeAsString = "".join(splitTree)
    # find all words enclosed by triangle braces
    # WARNING : This is a bit janky, if someone has a name that includes triangle braces
    # then this logic could break entirely.
    # It also fails when trying to add attributes
    split = i_re.findall(r"<(.*?)\>", treeAsString)

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
    treeAsBytes = ET.tostring(tree, encoding)
    # Convert to string
    treeAsString = str(treeAsBytes, encoding)
    # Remove new lines
    splitTree = treeAsString.split("\n")
    # WARNING : removing \n could break strings that contain this.
    # maybe be more appropriate to use regex or something similar.
    treeAsString = "".join(splitTree)

    INDENT = "    "
    reparsed = minidom.parseString(treeAsString)
    return reparsed.toprettyxml(indent=INDENT)

# Write xml string to file
def fileWrite(data, fileName):
    prettyData = prettify_minidom(data)
    file = open(fileName, "w")
    file.write(prettyData)
    file.close()
    
# Read tree from xml file
def fileRead(fileName):
    file = open(fileName, "r")
    tree = ET.parse(file)
    file.close()
    return tree
    
# Create Dummy Event
def createDummyEvent(fileName):
    data = ET.Element('data')
    events = ET.SubElement(data, 'events')
    event0 = ET.SubElement(events, 'event')
    event0Name = ET.SubElement(event0, 'name')
    event0Name.text = 'event0abc'
    event1 = ET.SubElement(events, 'event')
    event1Name = ET.SubElement(event1, 'name')
    event1Name.text = 'event1abc'
    
    # Write 
    fileWrite(data, fileName)

#fileName = "events.xml"
#
#createDummyEvent(fileName)
#
# Print all data in Events.xml
#tree = fileRead(fileName)
#root = tree.getroot()
#
#print('\nAll attributes:')
#for elem in root:
#    print(elem.attrib)
#    for subelem in elem:
#        print(subelem.attrib)
#