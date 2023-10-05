from io import TextIOWrapper
from typing import Any, Callable, Dict, List, Optional, Tuple

import os.path as path
import xml.etree.ElementTree as ET
import zipfile


class DocHeaders:
    def __init__(self):
        self.H1 = "H1"
        self.H2 = "H2"
        self.H3 = "H3"
        self.H4 = "H4"

        self.TEXT = "TEXT"
        self.HEADER_TYPE = "TYPE"
        self.HEADER = "HEADER"
        self.CONTENT = "CONTENT"


headers = DocHeaders()
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def get_section_text(p):
    """Returns the joined text of the text elements under the given paragraph tag"""
    return_val = ''
    text_elems = p.findall('.//w:t', ns)
    if text_elems is not None:
        return_val = ''.join([t.text for t in text_elems])
    return return_val


def get_section_type(p):
    """Returns True if the given paragraph section has been styled as a Heading2"""
    return_val = headers.TEXT
    heading_style_elem = p.find(".//w:pStyle[@w:val='G-Ch1-Head']", ns)
    if heading_style_elem is not None:
        return_val = headers.H1
    heading_style_elem = p.find(".//w:pStyle[@w:val='G-Ch2-Head']", ns)
    if heading_style_elem is not None:
        return_val = headers.H2
    heading_style_elem = p.find(".//w:pStyle[@w:val='G-Ch4-Subheading']", ns)
    if heading_style_elem is not None:
        return_val = headers.H4
    #fixme(guyhod): add H3
    ""

    return return_val


def create_doc_object(header: str, header_type: str):
    return {headers.TEXT: "", headers.HEADER_TYPE: header_type
            , headers.HEADER: header, headers.CONTENT: []}


def parse_docx(doc_path: TextIOWrapper) -> Dict[str, Any]:
    doc = zipfile.ZipFile(doc_path).read('word/document.xml')
    root = ET.fromstring(doc)
    # Microsoft's XML makes heavy use of XML namespaces; thus, we'll need to reference that in our code

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    body = root.find('w:body', ns)  # find the XML "body" tag
    # under the body tag, find all the paragraph sections
    p_sections = body.findall('w:p', ns)

    current_h1 = 0
    current_h2 = None
    current_h4 = None
    sections_parsed = [create_doc_object("Untitled", headers.H1)]

    for s in p_sections:
        section_text = get_section_text(s)
        section_type = get_section_type(s)
        if section_type == headers.H1:
            sections_parsed.append(create_doc_object(section_text, headers.H1))
            current_h1 = len(sections_parsed) - 1
            current_h2 = None
            current_h4 = None

        elif section_type == headers.H2:
            sections_parsed[current_h1][headers.CONTENT].append(
                create_doc_object(section_text, headers.H2))
            current_h2 = len(sections_parsed[current_h1][headers.CONTENT]) - 1
            current_h4 = None

        elif section_type == headers.H4:
            sections_parsed[current_h1][headers.CONTENT][current_h2][headers.CONTENT].append(
                create_doc_object(section_text, headers.H4))
            current_h4 = len(
                sections_parsed[current_h1][headers.CONTENT][current_h2][headers.CONTENT]) - 1

        elif section_type == headers.TEXT:
            if current_h2 is None:
                sections_parsed[current_h1][headers.TEXT] += section_text

            elif current_h4 is None:
                sections_parsed[current_h1][headers.CONTENT][current_h2][headers.TEXT] += section_text

            else:
                sections_parsed[current_h1][headers.CONTENT][current_h2][headers.CONTENT][current_h4][headers.TEXT] += section_text

    return sections_parsed

def translate_header_to_string(header_type:str) -> Optional[str]:
    if header_type == headers.H1:
        return "Header"
    elif header_type == headers.H2:
        return "Title"
    elif header_type == headers.H3:
        return "Subtitle"
    elif header_type == headers.H4:
        return "Subtitle"
    else: 
        return None
    
def chunk_dict(dict_doc:Dict[str, Any], init_string:str="") -> List[str]:
    chunks = []

    for i in range(len(dict_doc)):
        header_string = init_string
        header_type = translate_header_to_string(dict_doc[i][headers.HEADER_TYPE])
        if header_type is not None:
            header_string += f"{header_type}: {dict_doc[i][headers.HEADER]}\n"
        chunks.append(f"{header_string}Text: {dict_doc[i][headers.TEXT]}")
        if dict_doc[i][headers.CONTENT]:
            child_chunks = chunk_dict(dict_doc[i][headers.CONTENT], init_string=header_string)
            chunks += child_chunks
        
    return chunks

def chunk_dict_with_headers(dict_doc:Dict[str, Any], init_string:str="") -> List[Dict[str, str]]:
    chunks = []

    for i in range(len(dict_doc)):
        header_string = init_string
        header_type = translate_header_to_string(dict_doc[i][headers.HEADER_TYPE])
        if header_type is not None:
            header_string += f"{header_type}: {dict_doc[i][headers.HEADER]}\n"
        chunks.append({"header":header_string, "data":f"{header_string}Text: {dict_doc[i][headers.TEXT]}"})
        if dict_doc[i][headers.CONTENT]:
            child_chunks = chunk_dict_with_headers(dict_doc[i][headers.CONTENT], init_string=header_string)
            chunks += child_chunks
        
    return chunks
