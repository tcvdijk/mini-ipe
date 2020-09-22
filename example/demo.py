# Demonstrates various features in one drawing.

from miniipe import Document, RotateAt, Matrix, polyline, ellipse

# Make a miniipe.Document
doc = Document()
doc.import_stylefile()
doc.add_layout( page=(620,850) )
doc.add_layer('alpha')

# Text
doc.text( (64,768), 'Hello, this is miniipe!', size='Huge' )

# Plot a function
doc.add_layer('plot')
from math import sin, cos, atan2, pi
def f(x): return 400 + x*sin(x/30)
points = [ (x,f(x)) for x in range(500) ]
doc.path( polyline(points), stroke='black', layer='plot' )

# Place a symbol every so many points
fewer_points = points[::40]
doc.add_layer('points')
for p in fewer_points:
    doc.use(p,layer='points')

# Draw a Koch fractal between them
def pairs(xs): return zip(xs[0::],xs[1::])
def left(p): return (-p[1],p[0])
def lerp(p,q,a): return ( a*p[0]+(1-a)*q[0], a*p[1]+(1-a)*q[1] )
def koch_summit(p,q):
    base = lerp(p,q,0.5)
    koch_factor = sin(pi/3)/3
    offset = left( (q[0]-p[0], q[1]-p[1]) )
    return (base[0]+koch_factor*offset[0], base[1]+koch_factor*offset[1])
def koch(ps):
    return [ f(pp) for pp in pairs(ps)
                   for f in ( lambda pp: pp[0]
                            , lambda pp: lerp(pp[0],pp[1],0.7)
                            , lambda pp: koch_summit(pp[0],pp[1])
                            , lambda pp: lerp(pp[0],pp[1],0.3)
                            )]
                            
snow = fewer_points + points[-1:]
while len(snow)<2500:
    snow = koch(snow)
doc.add_layer('fractal')
doc.path( polyline(snow), stroke='blue', layer='fractal')

# Add some text at the points
doc.add_layer('labels')
doc.add_layer('circles')
for i,p in enumerate(fewer_points):
    x = p[0]
    deriv = sin(x/30)+x*cos(x/30)/30
    angle = atan2(deriv,1)
    doc.path( ellipse(Matrix(10,0,0,15,0,7.5)),
              stroke='darkgreen',
              pen='fat',
              fill='yellow',
              opacity='50%',
              matrix=RotateAt(p,angle),
              layer='circles' )
    doc.text( (0,5), str(i),
              stroke='red',
              halign='center',
              valign='bottom',
              matrix=RotateAt(p,angle),
              layer='labels' )

# Clean up internal data structures and write file
doc.write('demo.ipe')