from typing import Any, Callable, Dict, List, Optional, Tuple

import os.path as path
import xml.etree.ElementTree as ET
import zipfile


class DocHeaders:
    def __init__(self):
        self.H1 = "H1"
        self.H2 = "H2"
        self.H4 = "H4"

        self.TEXT = "TEXT"
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
    ""

    return return_val


def create_doc_object(header: str):
    return {headers.TEXT: "", headers.HEADER: header, headers.CONTENT: []}


def parse_docx(doc_path) -> Dict[str, Any]:
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
    sections_parsed = [create_doc_object("Untitled")]

    for s in p_sections:
        section_text = get_section_text(s)
        section_type = get_section_type(s)
        if section_type == headers.H1:
            sections_parsed.append(create_doc_object(section_text))
            current_h1 = len(sections_parsed) - 1
            current_h2 = None
            current_h4 = None

        elif section_type == headers.H2:
            sections_parsed[current_h1][headers.CONTENT].append(
                create_doc_object(section_text))
            current_h2 = len(sections_parsed[current_h1][headers.CONTENT]) - 1
            current_h4 = None

        elif section_type == headers.H4:
            sections_parsed[current_h1][headers.CONTENT][current_h2][headers.CONTENT].append(
                create_doc_object(section_text))
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
