import xml.etree.ElementTree as ET
from xml.dom import minidom

# https://stackoverflow.com/questions/24813872/creating-xml-documents-with-whitespace-with-xml-etree-celementtree
# Return a pretty-printed XML string for the Element.
def prettify(xmlStr):
    INDENT = "    "
    rough_string = ET.tostring(xmlStr, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent=INDENT)

# Write xml string to file
def fileWrite(data, fileName):
    prettyData = prettify(data)
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
    event0.set('name', 'event0')
    event0.text = 'event0abc'
    event1 = ET.SubElement(events, 'event')
    event1.set('name', 'event1')
    event1.text = 'event1abc'
    
    # Write 
    fileWrite(data, fileName)

fileName = "events.xml"

createDummyEvent(fileName)

# Print all data in Events.xml
tree = fileRead(fileName)
root = tree.getroot()

print('\nAll attributes:')
for elem in root:
    print(elem.attrib)
    for subelem in elem:
        print(subelem.attrib)
