# Demonstration of various kinds of splines in Ipe.

from miniipe import Document, polyline, spline, cardinal_spline, clothoid, splinegon

doc = Document()
doc.import_stylefile()
doc.add_layout( page=(400,400) )

# Basic shape
ps = [ (100,100)
     , (100,300)
     , (200,300)
     , (200,200)
     , (300,200)
     , (300,100)
     ]

# Normal splines, which are B-splines
doc.add_layer('spline')
doc.path( spline(ps), stroke='red', layer='spline' )

# A closed polygon, but as a bsline
doc.add_layer('splinegon')
doc.path( splinegon(ps), stroke='orange', layer='splinegon' )

# Cardinal splines are also available, with variable tension [0,1]
doc.add_layer('cardinal spline')
for t in range(11):
    doc.path( cardinal_spline(ps,t/10), stroke='lightblue', layer='cardinal spline' )

doc.add_layer('clothoid')
doc.path( clothoid(ps), stroke='blue', layer='clothoid')

# Overlay the control points
doc.add_layer('input points')
doc.path( polyline(ps), stroke='black', pen='fat', layer='input points' )
for p in ps:
    doc.symbol(p, layer='input points')

doc.write('splines.ipe')