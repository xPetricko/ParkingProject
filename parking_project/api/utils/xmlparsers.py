
import xml.etree.ElementTree as ET

def xmlBoundingBoxParser(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    file_name = root.find("filename").text
    d = [x for x in root if x.tag=="object"]
    bboxes = [[int(x[4][0].text)-1,int(x[4][1].text)-1,int(x[4][2].text)-1,int(x[4][3].text)-1] for x in d]
    return file_name, bboxes
