from miniipe import Document

# Make a miniipe.Document
doc = Document()

# You need a stylefile. You could give the filename of your own
# stylefile as argument, or if you give # no argument, this method
# tries to load ~/.ipe/styles/basic.isy
doc.import_stylefile()

# Make a layer
doc.add_layer("alpha")

# Some preparations specifically for our drawing
from math import sin
def f(x):
    return 100 + 100*sin(x/30)

# Add a polyline path
points = [ (x,f(x)) for x in range(300) ]
doc.add_path( points, color='black' )

# Place a symbol at every 25th point
for p in points[::25]:
    doc.add_symbol(p)

# Add some text
doc.add_text( (50,50), 'hallo wereld', stroke='red' )

# Clean up internal data structures and write file
doc.write('test.ipe')