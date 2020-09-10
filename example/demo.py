from miniipe import Document, RotateAt

# Make a miniipe.Document
doc = Document()

# You need a stylefile. You could give the filename of your own
# stylefile as argument, or if you give # no argument, this method
# tries to load ~/.ipe/styles/basic.isy
doc.import_stylefile()

doc.add_layout( page=(620,850) )

# Make a layer
doc.add_layer('alpha')
doc.add_text( (64,768), 'Hello, this is miniipe!', size='Huge' )


# Plot a function
doc.add_layer('plot')
from math import sin, cos, atan2, pi
def f(x): return 400 + x*sin(x/30)
points = [ (x,f(x)) for x in range(500) ]
doc.add_path( points, color='black', layer='plot' )

# Place a symbol every so many points
stride = 40
doc.add_layer('points')
for p in points[::stride]:
    doc.add_symbol(p,layer='points')

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
                            
snow = points[::stride] + points[-1:]
while len(snow)<2500:
    snow = koch(snow)
doc.add_layer('fractal')
doc.add_path( snow, color='blue', layer='fractal')

# Add some text at the points
doc.add_layer('labels')
for i,p in enumerate(points[::stride]):
    x = p[0]
    deriv = sin(x/30)+x*cos(x/30)/30
    angle = atan2(deriv,1)
    doc.add_text( (0,5), str(i),
                  stroke='red',
                  halign='center',
                  valign='bottom',
                  matrix=RotateAt(p,angle),
                  layer='labels' )

# Clean up internal data structures and write file
doc.write('demo.ipe')