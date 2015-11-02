import xml.etree.cElementTree as ET
import simplejson
import pprint


class ElementToJSON:
    '''
    Takes an xml and turns it into a JSON for easy processing.
    '''
    def __init__(self, xml, strip=1):
        self.xml = xml
        self.strip = strip

    def _breakout_elem(self, elem):
        if hasattr(elem, 'getroot'):
            elem = elem.getroot()
        return simplejson.dumps(self._elem_to_dict(elem))

    def _elem_to_dict(self, elem):
        temp_dict = {}
        for key, value in elem.attrib.items():
            temp_dict['@'+key] = value

        # Loops over subelems to merge them into value. Heavily borrowed.
        for subelem in elem:
            v = self._elem_to_dict(subelem)
            tag = subelem.tag
            value = v[tag]
            try:
                # Adds to the existing list for this particular tag.
                temp_dict[tag].append(value)
            except AttributeError:
                # Turns existing entry into a list.
                temp_dict[tag] = [temp_dict[tag], value]
            except KeyError:
                # Adds a new non-list entry.
                temp_dict[tag] = value
        text = elem.text
        tail = elem.tail
        if self.strip:
            # Ignores leading and trailing whitespaces.
            if text:
                text = text.strip()
            if tail:
                tail = tail.strip()

        if tail:
            temp_dict['#tail'] = tail

        if temp_dict:
            # Uses text element if other attributes exist.
            if text:
                temp_dict['#text'] = text
        else:
            # Text is the value if no other attributes exist.
            temp_dict = text or None
        return {elem.tag: temp_dict}

    def convert(self):
        xml_file = open(self.xml).read()
        elem = ET.fromstring(xml_file)
        return self._breakout_elem(elem)


if __name__ == "__main__":
    test = ElementToJSON("spcrss.xml")
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(test.convert())
