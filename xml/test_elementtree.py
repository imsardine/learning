# -*- coding: utf-8 -*-
import unittest2 as unittest
from mock import patch
from os import path
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import QName
from StringIO import StringIO

class ModuleTest(unittest.TestCase):

    def setUp(self):
        self.xml_file = path.join(path.dirname(__file__), 'data.xml')

    def test_parse(self):
        tree = ET.parse(open(self.xml_file)) # file
        self.assertIsInstance(tree, ET.ElementTree)

        tree = ET.parse(self.xml_file) # filename
        self.assertIsInstance(tree, ET.ElementTree)

    def test_fromstring(self):
        root = ET.fromstring(open(self.xml_file).read())
        self.assertIsInstance(root, ET.Element)
        self.assertEqual(root.tag, 'data')

    def test_xml(self):
        root = ET.XML(open(self.xml_file).read())
        self.assertIsInstance(root, ET.Element)
        self.assertEqual(root.tag, 'data')

    def test_xmlid(self):
        root, id_map = ET.XMLID(open(self.xml_file).read())
        self.assertIsInstance(root, ET.Element)
        self.assertEqual(root.tag, 'data')
        self.assertEqual(len(id_map), 2)
        self.assertEqual(id_map['S001'].get('name'), 'Jeremy')
        self.assertEqual(id_map['J001'].get('name'), 'Judy')

    @patch('sys.stdout', new_callable=StringIO)
    def test_dump(self, mock_stdout): # to stdout
        root, id_map = ET.XMLID(open(self.xml_file).read())
        ET.dump(id_map['S001'])
        self.assertEqual(mock_stdout.getvalue(), '<student id="S001" lang="English" name="Jeremy">\n      <weight>65</weight>\n      <height>178</height>\n      <cname>Jeremy Kao</cname>\n    </student>\n  \n')

class TestElementTree(unittest.TestCase):

    def setUp(self):
        self.xml_file = path.join(path.dirname(__file__), 'data.xml')

    def test_root(self):
        root = ET.parse(open(self.xml_file)).getroot()
        self.assertIsInstance(root, ET.Element)
        self.assertEqual(root.tag, 'data')

    def test_iteration_all(self): # recursive
        tree = ET.parse(open(self.xml_file))
        nodes = tree.getiterator()
        tags = [node.tag for node in nodes]
        self.assertEqual(tags, ['data', 'students'] + 
                               ['student', 'weight', 'height', 'cname'] * 2 +
                               ['teachers'])
        self.assertEqual(nodes[2].get('name'), 'Judy')
        self.assertEqual(nodes[6].get('name'), 'Jeremy')

    def test_iteration_tag(self):
        tree = ET.parse(open(self.xml_file))
        nodes = tree.getiterator('student') # indirect children
        tags = [node.tag for node in nodes]
        self.assertEqual(tags, ['student'] * 2)
        self.assertEqual(nodes[0].get('name'), 'Judy')
        self.assertEqual(nodes[1].get('name'), 'Jeremy')

class ElementTest(unittest.TestCase):

    def setUp(self):
        xml_file = path.join(path.dirname(__file__), 'data.xml')
        self.root = ET.parse(open(xml_file)).getroot()

    def test_text_types(self): # str or unicode
        cnames = self.root.findall('.//cname')
        self.assertEqual(len(cnames), 2)
        self.assertIsInstance(cnames[0].text, unicode)
        self.assertEqual(cnames[0].text, u'茱蒂')
        self.assertIsInstance(cnames[1].text, str)
        self.assertNotIsInstance(cnames[1].text, unicode)
        self.assertEqual(cnames[1].text, 'Jeremy Kao')

    def test_attributes_get(self):
        judy = self.root.find('.//student')

        # .get()
        self.assertEqual(judy.get('name'), 'Judy')
        self.assertIsNone(judy.get('xyz')) # defaults to None
        self.assertEqual(judy.get('xyz', 'beep!'), 'beep!') # given defaults

        # .attrib
        self.assertEqual(judy.attrib, {'id': 'J001', 'name': 'Judy', 'lang': u'中文'})
        with self.assertRaises(KeyError): # obviously, get() is more handy
            judy.attrib['xyz']

    def test_children_nested_index(self):
        self.assertEqual(self.root[0][1].get('name'), 'Jeremy')

    def test_children_direct(self):
        children = list(self.root[0]) # list(parent)
        self.assertEqual(len(children), 2)
        self.assertEqual([child.get('name') for child in children], ['Judy', 'Jeremy'])

    def test_children_recursive(self):
        tags = [node.tag for node in self.root[0].getiterator()]
        self.assertEqual(tags, ['students'] + ['student', 'weight', 'height', 'cname'] * 2) # inclusive

    def test_children_recursive_tag(self):
        tags = [node.tag for node in self.root[0].getiterator('weight')] # indirect children
        self.assertEqual(tags, ['weight'] * 2)

    def test_find(self):
        # found (element, the first one)
        student = self.root.find('.//student')
        self.assertEqual(student.get('name'), 'Judy')
        
        # not found (None)
        teacher = self.root.find('.//teacher')
        self.assertIsNone(teacher)

    def test_findall(self):
        # found (sequence)
        students = self.root.findall('.//student')
        self.assertEqual(len(students), 2)
        
        # not found (empty)
        teachers = self.root.findall('.//teacher')
        self.assertEqual(len(teachers), 0)

class XPathTest(unittest.TestCase):

    def setUp(self):
        xml_file = path.join(path.dirname(__file__), 'data.xml')
        self.root = ET.parse(open(xml_file)).getroot()

    def test_direct_children(self):
        nodes = self.root.findall('student') # if '//' is not used, only direct children are evaluated.
        self.assertEqual(len(nodes), 0)

        nodes = self.root[0].findall('student')
        self.assertEqual(len(nodes), 2)

    def test_indirect_children(self):
        nodes = self.root.findall('.//student')
        self.assertEqual(len(nodes), 2)

        with self.assertRaises(SyntaxError) as ctx:
            self.root.findall('//student')
        self.assertEqual(str(ctx.exception), 'cannot use absolute path on element') # even for the root node

    def test_position(self):
        # n-th
        nodes = self.root[0].findall('./student[1]') # 1-based
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].get('name'), 'Judy')

        # last one
        nodes = self.root[0].findall('./student[last()]')
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].get('name'), 'Jeremy')

        # last n-th
        nodes = self.root[0].findall('./student[last()-1]')
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].get('name'), 'Judy')

    def test_by_child_tag(self):
        nodes = self.root.findall('*[student]') # find the parent
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].tag, 'students')

    def test_by_attribute(self):
        nodes = self.root.findall('.//*[@name]') # don't forget the leading '@'
        self.assertEqual([node.tag for node in nodes], ['student'] * 2)

        nodes = self.root.findall(".//*[@name='Jeremy']") # compare value
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].get('name'), 'Jeremy')

    def test_down_and_up(self):
        nodes = self.root.findall('.//cname/..')
        self.assertEqual(len(nodes), 2)
        self.assertEqual([node.tag for node in nodes], ['student'] * 2)

    def test_invalid_predicates(self):
        with self.assertRaises(SyntaxError) as ctx:
            nodes = self.root.findall(".//*[starts-with(@name, 'J')]")
        self.assertEqual(str(ctx.exception), 'invalid predicate')

        with self.assertRaises(SyntaxError) as ctx:
            nodes = self.root.findall(".//*[contains(@name, 'J')]")
        self.assertEqual(str(ctx.exception), 'invalid predicate')

class ParentTest(unittest.TestCase):

    def setUp(self):
        xml_file = path.join(path.dirname(__file__), 'data.xml')
        self.root = ET.parse(open(xml_file)).getroot()

    def test_parent_xpath_not_work(self): # TODO
        child = self.root[0]
        parent = child.find('../*') # intuitive? doesn't work
        self.assertIsNone(parent)

class NamespaceTest(unittest.TestCase):

    def setUp(self):
        xml_file = path.join(path.dirname(__file__), 'data_ns.xml')
        self.root = ET.parse(open(xml_file)).getroot()

    def test_qname(self):
        ns = 'http://x.y.z/ns'  
        qname = QName(ns, 'fruit')
        self.assertEqual(qname.text, '{http://x.y.z/ns}fruit')
        self.assertEqual(str(qname), '{http://x.y.z/ns}fruit')

    def test_xmlns_only_part_of_serialization(self):
        # xmlns attributes are part of the serialization
        self.assertEquals(self.root.attrib, {'attr': 'value'}) 

    def test_find_qname(self):
        ns, nsa = 'http://x.y.z/ns', 'http://x.y.z/ns/a'

        # default namespace
        color = self.root.find('.//%s' % QName(ns, 'color'))
        self.assertEqual(color.tag, '{http://x.y.z/ns}color') # Clark notation

        self.assertIsNone(self.root.find('.//color'))

        # another namespace
        color_a = self.root.find('.//%s' % QName(nsa, 'color'))
        self.assertEqual(color_a.tag, '{http://x.y.z/ns/a}color')

    def test_find_with_prefix(self):
        with self.assertRaises(SyntaxError) as ctx:
            self.root.find('.//a:color')
        self.assertEquals(str(ctx.exception), "prefix 'a' not found in prefix map")

        # namespaces keyword argument is supported in Python 2.7+ (undocumented)
        # but it leads to the following side-effect...
        color_a = self.root.find('.//a:color', namespaces={'a': 'http://x.y.z/ns/a'})
        self.assertEqual(color_a.tag, '{http://x.y.z/ns/a}color')

        self.assertIsNotNone(self.root.find('.//a:color')) # TODO: why?

    def test_qualified_attrib(self):
        ns, nsa = 'http://x.y.z/ns', 'http://x.y.z/ns/a'
        fruit = self.root.find('.//%s' % QName(ns, 'fruit'))

        # default ns, not qualitifed (TODO: why?)
        self.assertEqual(fruit.get('name'), 'Apple')
        self.assertIsNone(fruit.get(QName(ns, 'name'))) 

        # non-default ns, qualified
        self.assertEqual(fruit.get(QName(nsa, 'name')), 'Apple (a)')

if __name__ == '__main__':
    unittest.main()

