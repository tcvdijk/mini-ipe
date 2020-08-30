import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment, tostring

class document(object):
    ipe = None
    style = None
    layout = None
    page = None

    def __init__(self):
        # base document
        self.ipe = Element('ipe')
        self.ipe.set('version','70212')
        self.ipe.set('creator','mini_ipe')
        # page, layer and view
        self.page = SubElement(self.ipe, 'page')

    def import_stylefile(self,filename="~/.ipe/styles/basic.isy"):
        tree = ET.parse(filename)
        ipestyle = tree.getroot()
        assert ipestyle.tag=="ipestyle", "Expected root of stylefile to by <ipestyle> tag."
        self.ipe.append(ipestyle)

    def add_style(self):
        self.style = SubElement(self.ipe,'ipestyle')
        self.style.set('name','mini_ipe')

    def add_layout(self, origin=(0,0), page=(612,792), frame=None):
        if frame is None:
            frame = page
        self.layout = SubElement(self.style,'layout')
        self.layout.set('paper',str(page[0])+' '+str(page[1]))
        self.layout.set('origin',str(origin[0])+' '+str(origin[1]))
        self.layout.set('frame',str(frame[0])+' '+str(frame[1]))

    def add_mark(self):
        if self.style is None:
            self.add_style()
        symbol = SubElement(self.style,'symbol')
        symbol.set('name','mark/circle(sx)')
        symbol.set('transformations','translations')
        path = SubElement(symbol,'path')
        path.set('fill','sym-stroke')
        path.text = '0.6 0 0 0.6 0 0 e'

    def add_layer(self,name):
        layer = SubElement(self.page,'layer')
        layer.set('name',name)

    def add_view(self,layers,active):
        view = SubElement(self.page,'view')
        view.set('layers',layers)
        view.set('active',active)

    def path(self,ps,color='black',layer='alpha'):
        path = SubElement(self.page,'path')
        path.set('layer',layer)
        path.set('stroke',color)
        instructions = [ str(ps[0][0]), str(ps[0][1]), 'm' ] + [ f(p) for p in ps[1:] for f in [ lambda p: str(p[0]), lambda p: str(p[1]), lambda _: 'l' ] ]
        path.text = ' '.join(instructions)

    def symbol(self,p,name='mark/disk(sx)',color='black',layer='alpha',size='normal'):
        symbol = SubElement(self.page,'use')
        symbol.set('name', name)
        symbol.set('pos', str(p[0])+' '+str(p[1]))
        symbol.set('size', size)
        symbol.set('stroke',color)  

    def write(self,filename):
        # sort the <ipestyle>s before the <page>s
        ipe_order = lambda e: {'ipestyle': 1, 'page': 2}.get( e.tag, 3 )
        self.ipe[:] = sorted(self.ipe, key=ipe_order)
        # sort the page tag: layer < view < content
        page_order = lambda e: {'layer': 1, 'view': 2}.get( e.tag, 3 )
        self.page[:] = sorted(self.page, key=page_order)
        # write out
        ElementTree(self.ipe).write(filename, encoding='utf-8', xml_declaration=True)
