# Demonstrates the use of arcs.

from miniipe import Document, Translate, Scale, rectangle, circle, arc_cw, arc_ccw
from math import pi

doc = Document()
doc.import_stylefile()
doc.add_layout( page=(400,320) )

doc.add_layer('waves')
for r in range(1,15):
    doc.path( arc_ccw((0,0),r*r,0,pi/2), stroke='lightblue', opacity='50%', pen='ultrafat', layer='waves' )
    doc.path( arc_ccw((200,0),r*r,0,pi), stroke='lightblue', opacity='50%', pen='ultrafat', layer='waves' )
    doc.path( arc_cw((400,0),r*r,pi,pi/2), stroke='lightblue', opacity='50%', pen='ultrafat', layer='waves' )

dropshadow = Translate( (0,-5) )

doc.add_layer('pie')

pie1 = arc_ccw( (200,200), 100, pi/5, -pi/5, True )
pie2 = arc_cw( (225,200), 100, pi/5, -pi/5, True )

doc.path( pie1, fill='black', opacity='50%', matrix=dropshadow )
doc.path( pie2, fill='black', opacity='50%', matrix=dropshadow )

doc.path( pie1, fill='yellow', stroke='black' )
doc.path( pie2, fill='red', stroke='black' )

Legend = Translate( (24, 268) )
doc.path( rectangle((0,0), (16,16),True), stroke='black', fill='yellow', pen='fat', matrix=Legend)
doc.text( "Pac-Man", pos=(16,0), valign='center',matrix=Legend)
#doc.path( rectangle((0,-32), (16,16),True), stroke='black', fill='red', pen='fat', matrix=Legend)
#doc.text( (16,-32), "Not Pac-Man", valign='center',matrix=Legend)

doc.write('arcs.ipe')