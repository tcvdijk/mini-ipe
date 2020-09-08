from miniipe import Document

# make a miniipe.Document
doc = Document()

# You need a stylefile; you could make your own, or if you give
# no argument, it tries to load ~/.ipe/styles/basic.isy
doc.import_stylefile()

# Make a layer
doc.add_layer("hello world")

# Some preparations specifically for our drawing
from math import sin
def f(x):
    return 100 + 100*sin(x/30)

# a polyline
ps = [ (x,f(x)) for x in range(300) ]
doc.add_path( ps, color='black')

# symbols
for p in ps[::25]:
    doc.add_symbol(p)

# text
doc.add_text( (50,50), 'o hai', stroke='red' )

# write file
doc.write('test.ipe')