# Demonstrates the use of transformation matrices.

from miniipe import Document, Rotate, Translate, Scale, polyline

doc = Document()
doc.import_stylefile()
doc.add_layout( page=(640,640) )
doc.add_layer('alpha')

# Iteratively tweak a transformation matrix.
# (Matrix multiplication with the @ operator.)
ps = [(10,0),(20,0),(19,1),(19,-1),(20,0)]
M = Translate( (300,300) )
for _ in range(207):
    doc.symbol( (0,0), name='mark/cross(sx)', matrix=M )
    doc.path( polyline(ps), matrix=M)
    M @= Rotate(0.1) @ Translate( (3,1) ) @ Scale(1.01)


doc.write('matrix_fun.ipe')