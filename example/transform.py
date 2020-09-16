# Test our own matrix transformation versus letting Ipe do it.
# Both layers should look the same.

from miniipe import Document, Matrix, polygon
from random import random

doc = Document()
doc.import_stylefile()
doc.add_layout( page=(200,200) )
doc.add_layer('ipe')
doc.add_layer('miniipe')

# basic rectangle
ps = [(-20,-20)
     ,( 20,-20)
     ,( 20, 20)
     ,(-20, 20)]

for _ in range(100):
    # random matrix
    M = Matrix( 2*random()-1, 2*random()-1, 2*random()-1, 2*random()-1, 200*random(), 200*random())
    
    # just give the matrix to Ipe
    doc.path( polygon(ps), matrix=M, stroke='lightblue', pen='ultrafat', layer='ipe')
    
    # or transform it ourselves using Matrix.transform
    tps = list(map( lambda p: M.transform(p), ps ))
    doc.path( polygon(tps), stroke='blue', layer='miniipe' )

doc.write('transform.ipe')