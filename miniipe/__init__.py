from os.path import expanduser

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment, tostring

from math import sin, cos

class Document(object):
    ipe = None
    style = None
    layout = None
    page = None

    # Constructor

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

    # Style things

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
        if frame is None: frame = page
        if style is None: style = self.style
        layout = SubElement(style,'layout')
        layout.set('paper',str(page[0])+' '+str(page[1]))
        layout.set('origin',str(origin[0])+' '+str(origin[1]))
        layout.set('frame',str(frame[0])+' '+str(frame[1]))
        return layout

    def add_symbol(self,name,style=None):
        if style is None: style=self.style
        symbol = SubElement('symbol',style)
        symbol.set('name',name)
        return symbol

    def add_color_rgb(self,name,r,g,b,style=None):
        return self.add_color(name,str(r)+' '+str(g)+' '+str(b),style)
    def add_color(self,name,value,style=None):
        if style is None: style = self.style
        color = SubElement(style, 'color')
        color.set('name',name)
        color.set('value',value)
        return color

    def add_dashstyle(self,name,value,style=None):
        if style is None: style = self.style
        dashstyle = SubElement(style,'dashstyle')
        dashstyle.set('name',name)
        dashstyle.set('value',value)
        return dashstyle

    def add_opacity(self,name,value):
        if style is None: style = self.style
        opacity = SubElement(style,'opacity')
        opacity.set('name',name)
        opacity.set('value',str(value))
        return opacity

    def add_textsize(self,name,value,style=None):
        if style is None: style = self.style
        textsize = SubElement(style,'textsize')
        textsize.set('name',name)
        textsize.set('value',value)
        return textsize

    def add_tiling(self,name,angle,step,width,style=None):
        if style is None: style = self.style
        tiling = SubElement(style,'tiling')
        tiling.set('name',name)
        tiling.set('angle',str(angle))
        tiling.set('step',str(step))
        tiling.set('width',str(width))
        return tiling

    def add_latex_preamble(self,latex):
        preamble = SubElement(self.ipe,'preamble')
        preamble.text = latex
        return preamble

    # Layer and view things

    def add_layer(self,name):
        layer = SubElement(self.page,'layer')
        layer.set('name',name)
        return layer

    def add_view(self,layers,active):
        view = SubElement(self.page,'view')
        view.set('layers',layers)
        view.set('active',active)
        return view

    # Drawing things

    def path(self,instructions,matrix=None,stroke='black',fill=None,pen=None, dash=None, arrow=None, rarrow=None, opacity=None, layer=None,closed=False,parent=None):
        if parent is None: parent = self.page
        e = SubElement(parent,'path')
        e.set('stroke',stroke)
        if arrow is not None: e.set('arrow',arrow)
        if dash is not None: e.set('dash',dash)
        if fill is not None: e.set('fill',fill)
        if layer is not None: e.set('layer',layer)
        if matrix is not None: e.set('matrix',matrix.tostring())
        if opacity is not None: e.set('opacity',opacity)
        if pen is not None: e.set('pen',pen)
        if rarrow is not None: e.set('rarrow',rarrow)
        e.text = instructions
        return e

    def symbol(self,pos,name='mark/disk(sx)',stroke='black',size='normal',matrix=None,layer=None):
        e = SubElement(self.page,'use')
        e.set('name', name)
        e.set('pos', str(pos[0])+' '+str(pos[1]))
        e.set('size', size)
        e.set('stroke',stroke)
        if layer is not None: e.set('layer',layer)
        if matrix is not None: e.set('matrix',matrix.tostring())
        return e

    def text(self,pos,text,stroke='black',type='label',size='normal',valign='baseline',halign='left',layer=None,matrix=None,parent=None):
        if parent is None: parent = self.page
        e = SubElement(parent,'text')
        e.set('pos', str(pos[0])+' '+str(pos[1]))
        e.set('halign', halign)
        e.set('size', size)
        e.set('stroke', stroke)
        e.set('type', type)
        e.set('valign', valign)
        if layer is not None: e.set('layer',layer)
        if matrix is not None: e.set('matrix',matrix.tostring())
        e.text = text
        return e

    # Output methods

    def prepare_output(self):
        # sort the <ipestyle>s before the <page>s
        ipe_order = lambda e: {'preamble': 1, 'ipestyle': 2, 'page': 3}.get( e.tag, 4 )
        self.ipe[:] = sorted(self.ipe, key=ipe_order)
        # sort the page tag: layer < view < content
        page_order = lambda e: {'layer': 1, 'view': 2}.get( e.tag, 3 )
        self.page[:] = sorted(self.page, key=page_order)
    def tostring(self):
        self.prepare_output()
        return ET.tostring(self.ipe,encoding='unicode', xml_declaration=True, method='xml')
    def write(self,filename):
        self.prepare_output()
        ElementTree(self.ipe).write(filename, encoding='unicode', xml_declaration=True)

# Path instructions

def polygon(points):
    return polyline(points,True)

def polyline(points,closed=False):
    instructions = [ str(points[0][0]), str(points[0][1]), 'm' ] + [ f(p) for p in points[1:] for f in [ lambda p: str(p[0]), lambda p: str(p[1]), lambda _: 'l' ] ]
    if closed: instructions = instructions + ['h']
    return ' '.join(instructions)

def splinegon(points):
    instructions = [ f(p) for p in points for f in [ lambda p: str(p[0]), lambda p: str(p[1])] ] + ['u']
    return ' '.join(instructions)


def spline(points):
    instructions = [ str(points[0][0]), str(points[0][1]), 'm' ] + [ f(p) for p in points[1:] for f in [ lambda p: str(p[0]), lambda p: str(p[1])] ] + ['c']
    return ' '.join(instructions)
def cardinal_spline(points,tension=0.5):
    instructions = [ str(points[0][0]), str(points[0][1]), 'm' ] + [ f(p) for p in points[1:] for f in [ lambda p: str(p[0]), lambda p: str(p[1])] ] + [str(tension),'C']
    return ' '.join(instructions)

def circle(center,radius):
    return ellipse( Matrix(radius,0,0,radius,center[0],center[1]) )

def ellipse(matrix):
    return matrix.tostring() + ' e'

# Helper class for matrices.
# Matrix multiplication with operator @

class Matrix(object):
    m11 = 1; m12 = 0
    m21 = 0; m22 = 1
    t1  = 0; t2  = 0
    def __init__(self,m11,m12,m21,m22,t1,t2):
        self.m11 = m11
        self.m12 = m12
        self.m21 = m21
        self.m22 = m22
        self.t1 = t1
        self.t2 = t2
    def __matmul__(self,other):
        return Matrix( self.m11 * other.m11 + self.m12 * other.m21,   self.m11 * other.m12 + self.m12 * other.m22,
                       self.m21 * other.m11 + self.m22 * other.m21,   self.m21 * other.m12 + self.m22 * other.m22,
                       self.m11 * other.t1  + self.m12 * other.t2 + self.t1,
                       self.m21 * other.t1  + self.m22 * other.t2 + self.t2 )
    def tostring(self):
        return str(self.m11)+' '+str(self.m21)+' '+str(self.m12)+' '+str(self.m22)+' '+str(self.t1)+' '+str(self.t2)

def Identity():
    return Matrix(1,0,0,1,0,0)
def Translate(p):
    return Matrix(1,0,0,1,p[0],p[1])
def Scale(s):
    return Matrix(s,0,0,s,0,0)
def Rotate(a):
    return Matrix(cos(a),-sin(a),sin(a),cos(a), 0, 0)
def RotateAt(p,a):
    return Matrix(cos(a),-sin(a),sin(a),cos(a), p[0], p[1])