from os.path import expanduser

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment, tostring

class Document(object):
    ipe = None
    style = None
    layout = None
    page = None

    def __init__(self):
        # base document
        self.ipe = Element('ipe')
        self.ipe.set('version','70212')
        self.ipe.set('creator','miniipe')
        # ipestyle for some of our own stuff
        self.style = SubElement(self.ipe,'ipestyle')
        self.style.set('name','miniipe')
        # page, layer and view
        self.page = SubElement(self.ipe, 'page')


    def import_stylefile(self,filename=None):
        if filename is None:
            filename = expanduser('~/.ipe/styles/basic.isy')
        tree = ET.parse(filename)
        ipestyle = tree.getroot()
        assert ipestyle.tag=="ipestyle", "Expected root of stylefile to by <ipestyle> tag."
        self.ipe.append(ipestyle)


    def add_style(self, name):
        style = SubElement(self.ipe, name)
        style.set('name',name)
        return style

    def add_layout(self, origin=(0,0), page=(612,792), frame=None, style=None):
        if frame is None:
            frame = page
        if style is None:
            style = self.style
        layout = SubElement(self.style,'layout')
        layout.set('paper',str(page[0])+' '+str(page[1]))
        layout.set('origin',str(origin[0])+' '+str(origin[1]))
        layout.set('frame',str(frame[0])+' '+str(frame[1]))
        return layout

    def add_layer(self,name):
        layer = SubElement(self.page,'layer')
        layer.set('name',name)
        return layer

    def add_view(self,layers,active):
        view = SubElement(self.page,'view')
        view.set('layers',layers)
        view.set('active',active)
        return view

    def add_path(self,points,color='black',layer=None):
        e = SubElement(self.page,'path')
        e.set('stroke',color)
        if layer is not None: e.set('layer',layer)
        instructions = [ str(points[0][0]), str(points[0][1]), 'm' ] + [ f(p) for p in points[1:] for f in [ lambda p: str(p[0]), lambda p: str(p[1]), lambda _: 'l' ] ]
        e.text = ' '.join(instructions)
        return e

    def add_symbol(self,pos,name='mark/disk(sx)',stroke='black',size='normal',layer=None):
        e = SubElement(self.page,'use')
        e.set('name', name)
        e.set('pos', str(pos[0])+' '+str(pos[1]))
        e.set('size', size)
        e.set('stroke',stroke)
        if layer is not None: e.set('layer',layer)
        return e

    def add_text(self,pos,text,stroke='black',type='label',valign='baseline',layer=None):
        e = SubElement(self.page,'text')
        e.set('pos', str(pos[0])+' '+str(pos[1]))
        e.set('stroke', stroke)
        e.set('type', type)
        e.set('valign', valign)
        if layer is not None: e.set('layer',layer)
        e.text = text
        return e


    def write(self,filename):
        # sort the <ipestyle>s before the <page>s
        ipe_order = lambda e: {'ipestyle': 1, 'page': 2}.get( e.tag, 3 )
        self.ipe[:] = sorted(self.ipe, key=ipe_order)
        # sort the page tag: layer < view < content
        page_order = lambda e: {'layer': 1, 'view': 2}.get( e.tag, 3 )
        self.page[:] = sorted(self.page, key=page_order)
        # write out
        ElementTree(self.ipe).write(filename, encoding='utf-8', xml_declaration=True)
