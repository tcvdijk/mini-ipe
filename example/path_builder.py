from miniipe import Document, Path

doc = Document()
doc.add_layout( page=(400,400) )

path = Path()
path.move( (100, 100) )
path.line( (100, 200) )
path.arc_cw_fromto( (100,100), (100,200), (200,100) )
path.line( (100, 100) )

doc.path( path )

doc.write('D:/git/mini-ipe/path_builder.ipe')