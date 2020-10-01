from miniipe import Document, Path, Translate, segment, arc_fromto
from math import sqrt

doc = Document()
doc.add_layout( page=(1536,320) )

p1 = (100,100)
p2 = (100,200)
p3 = (200,200)

doc.text( 'Use helper functions for separate paths.', pos=(128,32), halign='center' )
doc.path( segment(p1,p2), pen=16 )
doc.path( arc_fromto(p1,p2,p3,cw=True ), pen=16 )
doc.path( segment(p3,p1), pen=16 )

M=Translate((256,0))
doc.text( 'Use helper functions and concatenate; make 1 object.', pos=(128,32), halign='center', matrix=M )
instructions = segment(p1,p2) + arc_fromto(p1,p2,p3,cw=True) + segment(p3,p1)
doc.path( instructions, matrix=M, pen=16 )

M=Translate((512,0))
doc.text( 'Use Path object; `move\' everywhere.', pos=(128,32), halign='center', matrix=M )
path = Path()
path.move( p1 )
path.line( p2 )
path.arc_fromto( p1, p2, p3, cw=True )
path.move(p3)
path.line( p1 )
doc.path( path, matrix=M, pen=16 )

M=Translate((768,0))
doc.text( 'Use Path object; keep going.', pos=(128,32), halign='center', matrix=M )
path = Path()
path.move( p1 )
path.line( p2 )
path.arc_to( p1, p3, cw=True )
path.line( p1 )
doc.path( path, matrix=M, pen=16 )

M=Translate((1024,0))
doc.text( 'Use Path object; close at the end.', pos=(128,32), halign='center', matrix=M )
path = Path()
path.move( p1 )
path.line( p2 )
path.arc_to( p1, p3, cw=True )
path.line( p1 )
path.close()
doc.path( path, matrix=M, pen=16 )

M=Translate((1280,0))
doc.text( 'Use Path\'s fluent interface; exact same output.', pos=(128,32), halign='center', matrix=M )
path = Path().move( p1 ).line( p2 ).arc_to( p1, p3, cw=True ).line( p1 ).close()
doc.path( path, matrix=M, pen=16 )

doc.write('path_builder.ipe')