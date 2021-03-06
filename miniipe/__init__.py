from os.path import expanduser

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment, tostring

from math import sin, cos, sqrt

class Document(object):
    ipe = None
    style = None
    layout = None
    page = None

    def __init__(self):
        """Makes an empty document with a single page in it.
        """
        # base document
        self.ipe = Element('ipe')
        self.ipe.set('version','70212')
        self.ipe.set('creator','miniipe')
        # ipestyle for some of our own stuff
        self.style = SubElement(self.ipe,'ipestyle')
        self.style.set('name','miniipe')
        # always have a page
        self.page = self.add_page()

    ### Pages, notes, layers and views

    def add_page( self
                , title=None
                , section=None
                , subsection=None
                , marked=None
                ):
        page = SubElement(self.ipe,'page')
        maybe_set(page,'title',title)
        maybe_set(page,'section',section)
        maybe_set(page,'subsection',subsection)
        maybe_set_bool(page,'marked',marked)
        return page
    
    def add_notes(self,text,page=None):
        if page is None: page=self.page
        notes = SubElement(self.ipe,'notes')
        notes.text = text
        return notes

    def add_layer( self
                 , name
                 , edit=None
                 , snap=None
                 , data=None
                 , page=None # miniipe parent element
                 ):
        layer = SubElement(self.page,'layer')
        layer.set('name',name)
        maybe_set(layer,'edit',edit)
        maybe_set(layer,'snap',snap)
        maybe_set(layer,'data',data)
        return layer

    def add_view( self
                , layers # list of strings
                , active # list of strings
                , effect=None
                , name=None
                , marked=None
                ):
        view = SubElement(self.page,'view')
        view.set('layers',' '.join(layers))
        view.set('active',' '.join(active))
        maybe_set(view,'effect',effect)
        maybe_set(view,'name',name)
        maybe_set_bool(view,'marked',marked)
        return view

    ### Style things

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

    # Generic style item. Adds it to a specific style tag if
    # given; otherwise adds it to the miniipe style tag.
    def add_style_item(self,tag,name,value,style=None):
        if style is None: style = self.style
        elem = SubElement(style, tag)
        elem.set('name',name)
        elem.set('value',str(value))
        return elem

    # Specific style items: a lot of these are just (name,value)
    # pairs with different tag names, but by including them all,
    # we give the user tab completion in their IDE.
    def add_anglesize(self,name,value,style=None):
        return self.add_style_item('anglesize',name,value)
    def add_arrowsize(self,name,value,style=None):
        return self.add_style_item('arrowsize',name,value)
    def add_bitmap(self,id,width,height,blob,ColorSpace=None,ColorKey=None,BitsPerComponent=None,length=None,Filter=None,encoding=None,alphaLength=None,style=None):
        if style is None: style=self.style
        bitmap = SubElement(self.ipe,'bitmap')
        bitmap.set('id',str(id))
        bitmap.set('width',str(width))
        bitmap.set('height',str(height))
        maybe_set(bitmap,'BitsPerComponent',BitsPerComponent)
        maybe_set(bitmap,'ColorSpace',ColorSpace)
        maybe_set(bitmap,'ColorKey',ColorKey)
        maybe_set(bitmap,'Filter',Filter)
        maybe_set(bitmap,'length',length)
        maybe_set(bitmap,'encoding',encoding)
        maybe_set(bitmap,'alphaLength',alphaLength)
        bitmap.text = blob
        return bitmap
    def add_color(self,name,value,style=None):
        return self.add_style_item('color',name,value)
    def add_color_rgb(self,name,r,g,b,style=None):
        return self.add_color(name,str(r)+' '+str(g)+' '+str(b),style)
    def add_dashstyle(self,name,value,style=None):
        return self.add_style_item('dashstyle',name,value)
    def add_effect(self,name,duration=None,transition=None,effect=None,style=None):
        if style is None: style=self.style
        effecttag = SubElement(style,'effect')
        effecttag.set('name',name)
        maybe_set(effecttag,'duration',duration)
        maybe_set(effecttag,'transition',transition)
        maybe_set(effecttag,'effect',effect)
        return effecttag
    def add_gradient(self,name,type_,coords,extend=None,matrix=None,style=None):
        if style is None: style=self.style
        gradient = SubElement(style,'gradient')
        gradient.set('name',name)
        gradient.set('type',type_)
        gradient.set('coords',coords)
        maybe_set_bool(gradient,'extend',extend)
        if matrix is not None: gradient.set('matrix',matrix)
        return gradient
    def add_gridsize(self,name,value,style=None):
        return self.add_style_item('gridsize',name,str(value))
    def add_latex_preamble(self,latex):
        preamble = SubElement(self.ipe,'preamble')
        preamble.text = latex
        return preamble
    def add_layout(self,origin=(0,0),page=(612,792),frame=None,skip=None,crop=None,style=None):
        if frame is None: frame = page
        if style is None: style = self.style
        layout = SubElement(style,'layout')
        layout.set('paper',str(page[0])+' '+str(page[1]))
        layout.set('origin',str(origin[0])+' '+str(origin[1]))
        layout.set('frame',str(frame[0])+' '+str(frame[1]))
        maybe_set(layout,'skip',skip)
        maybe_set_bool(layout,'crop',crop)
        return layout
    def add_opacity(self,name,value,style=None):
        return self.add_style_item('opacity',name,value,style)
    def add_pagenumberstyle(self,pos,color,size,halign=None,valign=None,style=None):
        if style is None: style = self.style
        pagenumberstyle = SubElement(style,'titlestyle')
        pagenumberstyle.set('pos',str(pos[0])+' '+str(pos[1]))
        pagenumberstyle.set('color',color)
        pagenumberstyle.set('size',str(size))
        maybe_set(pagenumberstyle,'halign',halign)
        maybe_set(pagenumberstyle,'valign',valign)
        return pagenumberstyle
    def add_pathstyle(self,cap=None,join=None,fillrule=None,style=None):
        if style is None: style=self.style
        pathstyle = SubElement(style,'symbol')
        maybe_set(pathstyle,'cap',cap)
        maybe_set(pathstyle,'join',join)
        maybe_set(pathstyle,'fillrule',fillrule)
        return pathstyle
    def add_pen(self,name,value,style=None):
        return self.add_style_item('pen',name,str(value),style)
    def add_symbol(self,name,transformations=None,snap=None,style=None):
        if style is None: style=self.style
        symbol = SubElement(style,'symbol')
        symbol.set('name',name)
        maybe_set(symbol,'transformations',transformations)
        maybe_set_bool(symbol,'snap',snap)
        return symbol
    def add_symbolsize(self,name,value,style=None):
        return self.add_style_item('symbolsize',name,value)
    def add_textpad(self,left,right,top,bottom,style=None):
        if style is None: style = self.style
        textpad = SubElement(style,'textpad')
        textpad.set('left',left)
        textpad.set('right',right)
        textpad.set('top',top)
        textpad.set('bottom',bottom)
        return textpad
    def add_textsize(self,name,value,style=None):
        return self.add_style_item('textsize',name,value)
    def add_textstretch(self,name,value,style=None):
        return self.add_style_item('textstretch',name,value)
    def add_textstyle(self,name,begin,end,style=None):
        if style is None: style = self.style
        textstyle = SubElement(style,'textstyle')
        textstyle.set('name',name)
        textstyle.set('begin',begin)
        textstyle.set('end',end)
        return textstyle
    def add_tiling(self,name,angle,step,width,style=None):
        if style is None: style = self.style
        tiling = SubElement(style,'tiling')
        tiling.set('name',name)
        tiling.set('angle',str(angle)) # in degrees
        tiling.set('step',str(step))
        tiling.set('width',str(width))
        return tiling
    def add_titlestyle(self,pos,color,size,halign=None,valign=None,style=None):
        if style is None: style = self.style
        titlestyle = SubElement(style,'titlestyle')
        titlestyle.set('pos',str(pos[0])+' '+str(pos[1]))
        titlestyle.set('color',color)
        titlestyle.set('size',size)
        maybe_set(titlestyle,'halign',halign)
        maybe_set(titlestyle,'valign',valign)
        return titlestyle


    ### Drawing objects

    def path( self
            , instructions
            , stroke=None
            , fill=None
            , dash=None
            , pen=None
            , cap=None
            , join=None
            , fillrule=None
            , arrow=None
            , rarrow=None
            , opacity=None
            , tiling=None
            , gradient=None
            , layer=None
            , matrix=None
            , pin=None
            , transformation=None
            , parent=None # miniipe DOM parent
            ):
        if parent is None: parent = self.page
        e = SubElement(parent,'path')
        maybe_set(e,'stroke',stroke)
        maybe_set(e,'fill',fill)
        maybe_set(e,'dash',dash)
        maybe_set(e,'pen',pen)
        maybe_set(e,'cap',cap)
        maybe_set(e,'join',join)
        maybe_set(e,'fillrule',fillrule)
        maybe_set(e,'arrow',arrow)
        maybe_set(e,'rarrow',rarrow)
        maybe_set(e,'opacity',opacity)
        maybe_set(e,'tiling',tiling)
        maybe_set(e,'gradient',gradient)
        maybe_set(e,'layer',layer)
        if matrix is not None: e.set('matrix',matrix.tostring())
        maybe_set(e,'pin',pin)
        maybe_set(e,'transformation',transformation)
        e.text = str(instructions)
        return e

    def use( self
           , name='mark/disk(sx)'
           , pos=None
           , stroke=None
           , fill=None
           , pen=None
           , size=None
           , layer=None
           , matrix=None
           , pin=None
           , transformation=None
           , parent=None # miniipe DOM parent
           ):
        if parent is None: parent=self.page
        e = SubElement(self.page,'use')
        e.set('name', name)
        if pos is not None: e.set('pos', str(pos[0])+' '+str(pos[1]))
        maybe_set(e,'stroke',stroke)
        maybe_set(e,'fill',fill)
        maybe_set(e,'pen',pen)
        maybe_set(e,'size',size)
        maybe_set(e,'layer',layer)
        if matrix is not None: e.set('matrix',matrix.tostring())
        maybe_set(e,'pin',pin)
        maybe_set(e,'transformation',transformation)
        return e

    def text( self
            , text
            , stroke=None
            , type_=None
            , size=None
            , pos=None
            , width=None
            , height=None
            , depth=None
            , valign=None
            , halign=None
            , style=None
            , opacity=None
            , layer=None
            , matrix=None
            , pin=None
            , transformation=None
            , parent=None # miniipe DOM parent
            ):
        if parent is None: parent=self.page
        e = SubElement(parent,'text')
        maybe_set(e,'stroke',stroke)
        maybe_set(e,'type',type_)
        maybe_set(e,'size',size)
        if pos is not None: e.set('pos', str(pos[0])+' '+str(pos[1]))
        maybe_set(e,'width',width)
        maybe_set(e,'height', height)
        maybe_set(e,'depth',depth)
        maybe_set(e,'valign',valign)
        maybe_set(e,'halign',halign)
        maybe_set(e,'style',style)
        maybe_set(e,'opacity',opacity)
        maybe_set(e,'layer',layer)
        if matrix is not None: e.set('matrix',matrix.tostring())
        maybe_set(e,'pin',pin)
        maybe_set(e,'transformation',transformation)
        e.text = text
        return e

    def image( self
             , bitmap # int corresponding to the add_bitmap id
             , rect # 4-tuple x1 y1 x2 y2
             , layer=None
             , matrix=None
             , pin=None
             , transformation=None
             , parent=None # miniipe DOM parent
             ):
        if parent is None: parent=self.page
        e = SubElement(parent,'image')
        e.set('bitmap',str(bitmap))
        e.set('rect',' '.join(map(str,rect)))
        maybe_set(e,'layer',layer)
        if matrix is not None: e.set('matrix',matrix.tostring())
        maybe_set(e,'pin',pin)
        maybe_set(e,'transformation',transformation)
        return e

    def group( self
             , clip=None
             , url=None
             , decoration=None
             , layer=None
             , matrix=None
             , pin=None
             , transformation=None
             , parent=None # miniipe DOM parent
             ):
        if parent is None: parent=self.page
        e = SubElement(parent,'group')
        maybe_set(e,'clip',clip)
        maybe_set(e,'url',url)
        maybe_set(e,'decoration',decoration)
        maybe_set(e,'layer',layer)
        if matrix is not None: e.set('matrix',matrix.tostring())
        maybe_set(e,'pin',pin)
        maybe_set(e,'transformation',transformation)
        return e

    ### Sorting object order

    def sort_by_layer(self,order,page=None):
        """Given a list of layer names (order), sorts the objects in a page by layer, back-to-front.
        Puts objects with other layer names (or no layer name) all the way in the back.

        Args:
            order (list of strings): Back to front.
            page (miniipe page, optional): The page that gets sorted. Defaults to None.
        """
        key = {}
        for i, x in enumerate(order): key[x] = i+1
        print(key)
        layer_order = lambda e: key.get(e.get('layer'),0)
        self.sort_objects( layer_order, page )

    def sort_objects(self,key,page=None):
        """Sorts the objects in 'page' by 'key'

        Args:
            key (function): Gets an ElementTree element in the Ipe DOM, returns a value like the normal sort function's key argument.
            page (miniipe page, optional): The page that gets sorted. Defaults to None.
        """
        if page is None: page=self.page
        page[:] = sorted(page, key=key)

    ### Output

    def prepare_output(self):
        """(Internal method; Ipe has certain restrictions on the order in which tags occur in the file, which is ensured here. Internally called by .tostring and .write; should be unnecessary to call from outside.)
        """
        # sort the <ipestyle>s before the <page>s
        ipe_order = lambda e: {'preamble': 1, 'bitmap': 2, 'ipestyle': 3, 'page': 4}.get( e.tag, 5 )
        self.ipe[:] = sorted(self.ipe, key=ipe_order)
        # sort the page tag: layer < view < content
        page_order = lambda e: {'layer': 1, 'view': 2}.get( e.tag, 3 )
        self.page[:] = sorted(self.page, key=page_order)
    def tostring(self):
        """Serialise the Ipe DOM to string.

        Returns:
            string: XML representation of the Ipe DOM
        """
        self.prepare_output()
        return ET.tostring(self.ipe,encoding='unicode', xml_declaration=True, method='xml')
    def write(self,filename):
        """Serialise the Ipe DOM and write it to a file

        Args:
            filename (string): Filename to write to.
        """
        self.prepare_output()
        ElementTree(self.ipe).write(filename, encoding='unicode', xml_declaration=True)

### Gradients
# Get a gradient using Document.add_gradient. Add stops here.
# Color has to be three numbers; no symbolic names.
def add_gradient_stop(gradient,offset,color):
    """Add a stop to a gradient.

    Args:
        gradient (miniipe gradient): As returned from add_gradient
        offset (number/string): Offset fraction on the gradient.
        color (string): Color as three numbers separated by whitespace (rgb); no symbolic names.

    Returns:
        [miniipe gradient stop]: The created gradient stop.
    """
    stop = SubElement(gradient,'stop')
    stop.set('offset',str(offset))
    stop.set('color',color) 
    return stop
# The stops a gradient must be sorted by offset
def sort_gradient(gradient):
    """The stops of a gradient must be sorted by offset.
    Call this before serialisation if your stops might not be sorted.

    Args:
        gradient (miniipe gradient): As returned from add_gradient
    """
    gradient[:] = sorted(gradient, key=lambda e: float(e.get('offset')))

### Path instructions: convenience functions

def segment(p1,p2):
    """Path instructions for a single line segment.

    Args:
        p1 (2-typle): (x,y) start position
        p2 (2-tuple): (x,y) end position

    Returns:
        [type]: [description]
    """
    return polyline([p1,p2])
def rectangle(p,size,centered=False):
    """Path instructions for a rectangle.

    Args:
        p (2-tuple): (x,y) position
        size (2-tuple): width, height
        centered (bool, optional): If true, then p is the middle of the rectangle; else p is the bottom-left corner. Defaults to False.

    Returns:
        string: Ipe path instructions
    """
    if centered:
        p = ( p[0]-size[0]/2, p[1]-size[1]/2 )
    return polygon( [p,(p[0],p[1]+size[1]),(p[0]+size[0],p[1]+size[1]),(p[0]+size[0],p[1])] )

def polygon(points):
    """Path instructions for a polygon

    Args:
        points (list of 2-tuples): The vertices of the polygon

    Returns:
        string: Ipe path instructions
    """
    return polyline(points,True)

def polyline(points,closed=False):
    """Path instructions for a polyline

    Args:
        points (list of 2-tuples): The vertices of the polyline
        closed (bool, optional): Close the polyline to a polygon. Defaults to False.

    Returns:
        string: Ipe path instructions
    """
    instructions = [ str(points[0][0]), str(points[0][1]), 'm' ] + [ f(p) for p in points[1:] for f in [ lambda p: str(p[0]), lambda p: str(p[1]), lambda _: 'l ' ] ]
    if closed: instructions = instructions + ['h ']
    return ' '.join(instructions)

def splinegon(points):
    """Path instructions for a splinegon

    Args:
        points (list of 2-tuples): The control points for the splinegon

    Returns:
        string: Ipe path instructions
    """
    instructions = [ f(p) for p in points for f in [ lambda p: str(p[0]), lambda p: str(p[1])] ] + ['u ']
    return ' '.join(instructions)

def spline(points):
    """Path instructions for a spline

    Args:
        points (list of 2-tuples): The control points for the spline

    Returns:
        string: Ipe path instructions
    """
    instructions = [ str(points[0][0]), str(points[0][1]), 'm' ] + [ f(p) for p in points[1:] for f in [ lambda p: str(p[0]), lambda p: str(p[1])] ] + ['c ']
    return ' '.join(instructions)
def cardinal_spline(points,tension=0.5):
    """Path instructions for a cardinal spline. The spline interpolates the control points.

    Args:
        points (list of 2-tuples): The control points for the cardinal spline.
        tension (float, optional): Tension of the spline in the range [0,1]. Defaults to 0.5.

    Returns:
        string: Ipe path instructions
    """
    instructions = [ str(points[0][0]), str(points[0][1]), 'm' ] + [ f(p) for p in points[1:] for f in [ lambda p: str(p[0]), lambda p: str(p[1])] ] + [str(tension),'C ']
    return ' '.join(instructions)
def clothoid(points):
    """Path instructions for a clothoid spline. The spline interpolates the control points.

    Args:
        points (list of 2-tuples): The control points for the spline

    Returns:
        string: Ipe path instructions
    """
    instructions = [ str(points[0][0]), str(points[0][1]), 'm' ] + [ f(p) for p in points[1:] for f in [ lambda p: str(p[0]), lambda p: str(p[1])] ] + ['L ']
    return ' '.join(instructions)

def circle(center,radius):
    """Path instructions for a circle.

    Args:
        center (2-tuple): Midpoint of the circle
        radius (float): Radius of the circle

    Returns:
        string: Ipe path instructions
    """
    return ellipse( Matrix(radius,0,0,radius,center[0],center[1]) )

def arc(center,radius,a1,a2,cw=False,wedge=False):
    """Path instructions for a clockwise arc.

    Args:
        center (2-tuple): Midpoint of the circle
        radius (float): Radius of the circle
        a1 (float): Start angle of the arc (counterclockwise radians, 0=right)
        a2 (float): End angle of the arc (counterclockwise radians, 0=right)
        cw (bool, optional): Clockwise arc? Counterclockwise if False.
        wedge (bool, optional): Close the arc as a wedge to the midpoint? Defaults to False.

    Returns:
        string: Ipe path instructions
    """
    sx = center[0] + radius*cos(a1)
    sy = center[1] + radius*sin(a1)
    ex = center[0] + radius*cos(a2)
    ey = center[1] + radius*sin(a2)
    instructions = [str(sx), str(sy),'m',str(radius),'0 0',str(-radius) if cw else str(radius),str(center[0]),str(center[1]),str(ex),str(ey),'a ']
    if wedge:
        instructions += [ str(center[0]), str(center[1]), 'l h ' ]
    return ' '.join(instructions)
def arc_fromto(center,p,q,cw=False,wedge=False):
    dx = center[0]-p[0]
    dy = center[1]-p[1]
    radius = sqrt(dx*dx+dy*dy)
    instructions = [str(p[0]), str(p[1]),'m',str(Matrix(radius,0,0,-radius,center[0],center[1])),str(q[0]),str(q[1]),'a ']
    if wedge:
        instructions += [ str(center[0]), str(center[1]), 'l h ' ]
    return ' '.join(instructions)

def ellipse(matrix):
    """Path instructions for an ellipse.

    Args:
        matrix (Matrix): Transformation matrix from a unit circle to the desired ellipse.

    Returns:
        string: Ipe path instructions
    """
    return matrix.tostring() + ' e '

### Path instructions: fluent builder interface

class Path(object):
    """String-builder-like object for Ipe path instructions."""

    def __init__(self):
        self.prefix = ''
        self.tokens = []
    def __str__(self):
        return self.prefix + ' '.join(self.tokens)
    def commit(self):
        """Destructively join all tokens currently in the list. Speeds up subsequent serialisations, but now the list of tokens is no longer available for manipulation.
        """
        self.prefix = ' '.join([self.prefix]+self.tokens)
        self.tokens = []

    def token(self,t):
        """Append a token to the list.

        Args:
            t (string): Token to add

        Returns:
            Path: Fluent return of the Path object
        """
        self.tokens.append(str(t))
        return self
    def point(self,p):
        """Append a point to the list.

        Args:
            p (2-tuple): Point to add

        Returns:
            Path: Fluent return of the Path object
        """
        return self.token(p[0]).token(p[1])
    def matrix(self,M):
        """Append a matrix to the list.

        Args:
            M (Matrix): Matrix to add

        Returns:
            Path: Fluent return of the Path object
        """
        return self.token(M.tostring())

    def move(self,p):
        """Move the pen.

        Args:
            p (2-tuple): The point to move to.

        Returns:
            Path: Fluent return of the Path object
        """
        return self.point(p).token('m')
    def line(self,p):
        """Draw a straight line segment.

        Args:
            p (2-tuple): The point to move to.

        Returns:
            Path: Fluent return of the Path object
        """
        return self.point(p).token('l')


    def ellipse(self,M):
        """Draw an ellipse.

        Args:
            M (Matrix): The matrix that transforms a unit circle to the desired ellipse.

        Returns:
            Path: Fluent return of the Path object.
        """
        return self.token(M.tostring()).token('e')

    def arc_fromto(self, center, p, q, cw=False):
        """Draw a circular arc from point a to point b, where center is the midpoint of the circle.

        Args:
            center (2-tuple): midpoint of the circle
            p (2-tuple): first point
            q (2-typle): second point
            cw (bool, optional): Does the arc go clockwise? Counterclockwise if False. Defaults to False.

        Returns:
            Path: Fluent return of the path object
        """
        dx = center[0]-q[0]
        dy = center[1]-q[1]
        radius = sqrt(dx*dx+dy*dy)
        return self.move(p).token(Matrix(radius,0,0,-radius if cw else radius,center[0],center[1])).point(q).token('a')

    def arc_to(self, center, p, cw=False):
        """Draw a circular arc from the current point to p, where center is the midpoint of the circle.

        Args:
            center (2-tuple): midpoint of the circle
            p (2-tuple): point
            cw (bool, optional): Does the arc go clockwise? Counterclockwise if False. Defaults to False.

        Returns:
            Path: Fluent return of the path object
        """
        dx = center[0]-p[0]
        dy = center[1]-p[1]
        radius = sqrt(dx*dx+dy*dy)
        return self.token(Matrix(radius,0,0,-radius if cw else radius,center[0],center[1])).point(p).token('a')

    def close_spline(self):
        """Close a spline; should be preceded by a sequence of point calls for the control points.

        Returns:
            Path: Fluent return of the Path object.
        """
        return self.token('c')
    def close(self):
        """Close the path.

        Returns:
            Path: Fluent return of the Path object.
        """
        return self.token('h')


### Helper class for matrices.
# Matrix multiplication with operator @

class Matrix(object):
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
    def transform(self,p):
        x = p[0]; y = p[1]
        return ( self.m11*x + self.m12*y + self.t1, self.m21*x + self.m22*y + self.t2 )
    def tostring(self):
        return str(self.m11)+' '+str(self.m21)+' '+str(self.m12)+' '+str(self.m22)+' '+str(self.t1)+' '+str(self.t2)
    def __str__(self):
        return self.tostring()

def Identity():
    return Matrix(1,0,0,1,0,0)
def Translate(p):
    return Matrix(1,0,0,1,p[0],p[1])
def Scale(s):
    return Matrix(s,0,0,s,0,0)
def Stretch(x,y):
    return Matrix(x,0,0,y,0,0)
def Rotate(a):
    return Matrix(cos(a),-sin(a),sin(a),cos(a), 0, 0)
def RotateAt(p,a):
    return Matrix(cos(a),-sin(a),sin(a),cos(a), p[0], p[1])

### Helper for Symbol names

def symbol_name(base,stroke=False,fill=False,pen=False,size=False):
    return base + '(' + ('s' if stroke else '') + ('f' if fill else '') + ('p' if pen else '') + ('x' if size else '') + ')'

### DOM helper

def maybe_set(e,name,value):
    if value is not None: e.set(name,str(value))
def maybe_set_bool(e,name,value):
    if value is not None: e.set(name,'yes' if value else 'no')