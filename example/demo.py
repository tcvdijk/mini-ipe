from miniipe import Document

# Make a miniipe.Document
doc = Document()

# You need a stylefile. You could give the filename of your own
# stylefile as argument, or if you give # no argument, this method
# tries to load ~/.ipe/styles/basic.isy
doc.import_stylefile()

# Make a layer
doc.add_layer("alpha")

# Plot a function
from math import sin, pi
def f(x): return 300 + x*sin(x/30)
points = [ (100+x,f(x)) for x in range(300) ]
doc.add_path( points, color='black' )

# Place a symbol at every 25th point
for p in points[::25]:
    doc.add_symbol(p)

# Draw a Koch fractal
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
#snow = [(100,200), (200,288), (300,200),(100,200)]
snow = points[::25] + points[-1:]
while len(snow)<1000:
    snow = koch(snow)
doc.add_path( snow, color='blue')

# Add some text
for p in points[::25]:
    doc.add_text( p, 'hallo wereld', stroke='red' )

# Clean up internal data structures and write file
doc.write('demo.ipe')