from miniipe import Document, Rotate, Translate, Scale, polyline

# Make a miniipe.Document
doc = Document()
doc.import_stylefile()
doc.add_layout( page=(640,640) )
doc.add_layer('alpha')

# Iteratively tweak a transformation matrix.
# (Matrix multiplication with the @ operator.)
M = Translate( (300,300) )
for _ in range(207):
    doc.symbol( (0,0), name='mark/cross(sx)', matrix=M )
    ps = [(10,0),(20,0),(19,1),(19,-1),(20,0)]
    doc.path( polyline(ps), matrix=M)
    M @= Rotate(0.1) @ Translate( (3,1) ) @ Scale(1.01)


doc.write('matrix_fun.ipe')