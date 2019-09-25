import xml.etree.ElementTree as ET
from xml.dom import minidom

# https://stackoverflow.com/questions/24813872/creating-xml-documents-with-whitespace-with-xml-etree-celementtree
# Return a pretty-printed XML string for the Element.
def prettify(xmlStr):
    INDENT = "    "
    rough_string = ET.tostring(xmlStr, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent=INDENT)

data = ET.Element('data')
events = ET.SubElement(data, 'events')
event0 = ET.SubElement(events, 'event')
event0.set('name', 'event0')
event0.text = 'event0abc'
event1 = ET.SubElement(events, 'event')
event1.set('name', 'event1')
event1.text = 'event1abc'

prettified_xmlStr = prettify(data)
wFile = open("events.xml", "w")
wFile.write(prettified_xmlStr)
wFile.close()

rFile = open("events.xml", "r")
tree = ET.parse(rFile)
root = tree.getroot()

print('\nAll attributes:')
for elem in root:
    print(elem.attrib)
    for subelem in elem:
        print(subelem.attrib)
        
rFile.close()
