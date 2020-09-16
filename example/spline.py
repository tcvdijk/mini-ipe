from miniipe import Document, polyline, spline, cardinal_spline, splinegon

# Make a miniipe.Document
doc = Document()
doc.import_stylefile()
doc.add_layout( page=(400,400) )


ps = [ (100,100)
     , (100,300)
     , (200,300)
     , (200,200)
     , (300,200)
     , (300,100)
     ]

doc.add_layer('spline')
doc.path( spline(ps), stroke='red', layer='spline' )

doc.add_layer('splinegon')
doc.path( splinegon(ps), stroke='orange', layer='splinegon' )

doc.add_layer('cardinal spline')
for t in range(11):
    doc.path( cardinal_spline(ps,t/10), stroke='lightblue', layer='cardinal spline' )

doc.add_layer('input points')
doc.path( polyline(ps), stroke='black', pen='fat', layer='input points' )
for p in ps:
    doc.symbol(p, layer='input points')

doc.write('splines.ipe')